#!/usr/bin/env python3
"""ATS parse check for CVs (PDF or DOCX).

Shows roughly what an Applicant Tracking System extracts from the file and
flags layout features that commonly break parsing. Heuristic, not a verdict.

Usage:
    python3 ats_check.py cv.pdf [--job-ad job.txt] [--json] [--max-chars 3000]

Requires: pdfplumber (PDF), python-docx (DOCX). Falls back to pdftotext.
"""
import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

STANDARD_HEADINGS = {
    "summary", "profile", "professional summary", "about", "about me",
    "experience", "work experience", "professional experience", "employment",
    "employment history", "career history",
    "skills", "technical skills", "core skills", "key skills", "competencies",
    "education", "projects", "selected projects", "personal projects",
    "open source", "certifications", "certificates", "licenses & certifications",
    "languages", "publications", "awards", "volunteering", "interests",
    "courses", "training", "achievements", "contact",
}
EXPECTED_CORE = {
    "experience": ["experience", "employment", "career history", "work history"],
    "skills": ["skills", "competencies", "technologies", "tech stack"],
    "education": ["education"],
}
SKILL_BAR_CHARS = set("●○◉◯★☆▪▫■□")
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE_RE = re.compile(r"(\+?\d[\d\s().-]{7,}\d)")
LINKEDIN_RE = re.compile(r"linkedin\.com/in/[\w-]+", re.I)
GITHUB_RE = re.compile(r"github\.com/[\w-]+", re.I)
URL_RE = re.compile(r"https?://\S+|www\.\S+", re.I)
DATE_PATTERNS = {
    "Mon YYYY": re.compile(r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?\s+(19|20)\d{2}\b", re.I),
    "MM/YYYY": re.compile(r"\b(0?[1-9]|1[0-2])[/.-](19|20)\d{2}\b"),
    "YYYY-MM": re.compile(r"\b(19|20)\d{2}-(0[1-9]|1[0-2])\b"),
    "'YY": re.compile(r"[‘’']\d{2}\b"),
}
YEAR_ONLY = re.compile(r"\b(19|20)\d{2}\s*[–-]\s*((19|20)\d{2}|present|current|now|ongoing|today|nu|pågående)\b", re.I)

STOP = set("""a an the and or of to in for on with at by from as is are be will
you your we our this that it its they their have has into using use etc can
must should would able other such per within across about including include
experience years year work working team teams role looking candidate strong good
knowledge skills skill plus nice understanding ability new also well like
what who how why where when we're you'll you'd looking build design run own
improve drive mentor strong fluent good great solid deep proven hands-on
engineer engineers developer developers senior junior lead platform services
service join help make get take want need hybrid remote office
""".split())
ADJ_PREFIX = re.compile(r"^(strong|good|solid|deep|proven|fluent|excellent|apache)\s+", re.I)


def extract_pdf(path):
    info = {"pages": 0, "images": 0, "multi_column_pages": [], "tables": 0,
            "header_footer_contact": False, "chars_per_page": [], "fonts": Counter()}
    text_parts = []
    try:
        import pdfplumber
    except ImportError:
        out = subprocess.run(["pdftotext", "-layout", str(path), "-"],
                             capture_output=True, text=True)
        info["note"] = "pdfplumber not installed; used pdftotext, layout checks skipped"
        return out.stdout, info
    with pdfplumber.open(path) as pdf:
        info["pages"] = len(pdf.pages)
        if pdf.pages:
            w0, h0 = round(pdf.pages[0].width), round(pdf.pages[0].height)
            info["page_size"] = "A4" if (w0, h0) in {(595, 842), (596, 842)} else "US Letter" if (w0, h0) == (612, 792) else f"{w0}x{h0}pt"
        for i, page in enumerate(pdf.pages, 1):
            t = page.extract_text() or ""
            for h in (page.hyperlinks or []):
                uri = h.get("uri")
                if uri:
                    info.setdefault("links", []).append(uri)
            text_parts.append(t)
            info["chars_per_page"].append(len(t.strip()))
            info["images"] += len(page.images)
            try:
                info["tables"] += len(page.find_tables())
            except Exception:
                pass
            bars = [r for r in page.rects if r["height"] <= 6 and 15 <= r["width"] <= page.width * 0.4]
            from collections import Counter as _C
            # rating bars: same height, stacked at the same x, with several different
            # fill widths; divider lines have one width and are ignored
            groups = {}
            for r in bars:
                groups.setdefault((round(r["height"], 1), round(r["x0"])), set()).add(round(r["width"]))
            if any(len(ws) >= 3 for ws in groups.values()):
                info["drawn_bar_pages"] = info.get("drawn_bar_pages", []) + [i]
            words = page.extract_words(extra_attrs=["fontname"]) or []
            for w in words:
                info["fonts"][re.sub(r"^[A-Z]{6}\+", "", w.get("fontname", ""))] += 1
            # column heuristic: a real second column has many rows whose
            # right-hand segment STARTS at the same x (left-aligned gutter).
            # Right-aligned dates/locations start at varying x, so they don't count.
            if words:
                width = page.width
                rows = {}
                for w in words:
                    rows.setdefault(round(w["top"] / 4), []).append(w)
                starts = []
                for ws in rows.values():
                    ws.sort(key=lambda w: w["x0"])
                    for a, b in zip(ws, ws[1:]):
                        if b["x0"] - a["x1"] > 18 and width * 0.25 < b["x0"] < width * 0.75:
                            starts.append(round(b["x0"] / 3))
                            break
                gutter = bool(starts) and Counter(starts).most_common(1)[0][1] >= 6
                # sidebar layouts: rows of the two columns don't share a baseline,
                # so also look for two clusters of line-start x far apart
                line_starts = Counter(round(min(w["x0"] for w in ws) / 6) for ws in rows.values())
                main_x, main_n = line_starts.most_common(1)[0]
                main_x *= 6
                left_rows = sum(n for x, n in line_starts.items() if x * 6 < main_x - width * 0.12)
                # dominant text column starts well right of other text that has its own rows
                sidebar = main_n >= 8 and main_x > width * 0.25 and left_rows >= 6
                if gutter or sidebar:
                    info["multi_column_pages"].append(i)
                # header/footer: top 7% / bottom 7%
                hf = [w["text"] for w in words
                      if w["top"] < page.height * 0.07 or w["bottom"] > page.height * 0.93]
                hf_text = " ".join(hf)
                if EMAIL_RE.search(hf_text) or PHONE_RE.search(hf_text):
                    info["hf_contact_text"] = hf_text[:200]
                    info["header_footer_contact"] = True
    info["fonts"] = dict(info["fonts"].most_common(5))
    try:
        out = subprocess.run(["pdffonts", str(path)], capture_output=True, text=True, timeout=20).stdout
        not_emb = []
        for line in out.splitlines()[2:]:
            cols = line.split()
            # columns: name type... encoding emb sub uni objID gen -> emb is 5th from end
            if len(cols) >= 7 and cols[-5] == "no":
                not_emb.append(cols[0])
        info["fonts_not_embedded"] = not_emb
    except Exception:
        pass
    return "\n".join(text_parts), info


def extract_docx(path):
    import docx
    d = docx.Document(str(path))
    info = {"pages": None, "images": 0, "tables": len(d.tables),
            "text_boxes": 0, "header_footer_contact": False, "multi_column_pages": []}
    parts = [p.text for p in d.paragraphs]
    for t in d.tables:
        for row in t.rows:
            parts.append(" | ".join(c.text for c in row.cells))
    xml = d.element.xml
    info["text_boxes"] = xml.count("<w:txbxContent")
    info["images"] = xml.count("<pic:pic")
    cols = re.findall(r'<w:cols [^>]*w:num="(\d+)"', xml)
    if any(int(c) > 1 for c in cols):
        info["multi_column_pages"] = ["section columns > 1"]
    hf = []
    for s in d.sections:
        for part in (s.header, s.footer):
            hf.extend(p.text for p in part.paragraphs)
    hf_text = " ".join(hf)
    if EMAIL_RE.search(hf_text) or PHONE_RE.search(hf_text):
        info["header_footer_contact"] = True
        info["hf_contact_text"] = hf_text[:200]
    return "\n".join(parts), info


def find_headings(text):
    found, nonstandard = [], []
    for line in text.splitlines():
        first = line.strip().lower()
        for h in sorted(STANDARD_HEADINGS, key=len, reverse=True):
            ls = line.strip()
            if (first.startswith(h + " ") and ls[:len(h)].isupper()) or \
               (first.endswith(" " + h) and ls[-len(h):].isupper()):
                found.append(h.upper()); break
        s = line.strip().strip(":").strip()
        if not s or len(s) > 40 or len(s.split()) > 5:
            continue
        low = s.lower()
        is_capsish = s.isupper() or (s.istitle() and len(s.split()) <= 4)
        if low in STANDARD_HEADINGS:
            found.append(s)
            continue
        elif is_capsish and s.isupper() and not re.search(r"\d", s) and len(s) > 3:
            nonstandard.append(s)
    found = list(dict.fromkeys(found))
    return found, nonstandard


def keywords(text):
    toks = re.findall(r"[A-Za-z][A-Za-z0-9+#./-]{1,}", text)
    out = Counter()
    for t in toks:
        t2 = t.strip("./-").lower()
        if len(t2) < 2 or t2 in STOP:
            continue
        out[t2] += 1
    # bigrams for things like "spring boot", "event driven"
    words = [w.lower() for w in re.findall(r"[A-Za-z][A-Za-z0-9+#]*", text)]
    for a, b in zip(words, words[1:]):
        if a not in STOP and b not in STOP:
            out[f"{a} {b}"] += 1
    return out


def job_match(cv_text, ad_text):
    ad = keywords(ad_text)
    cv_low = cv_text.lower()
    # candidate terms: appear in ad, look techy (cap/acronym/symbol) or repeated
    raw_terms = set(re.findall(r"\b[A-Z][A-Za-z0-9+#.]*(?:\s[A-Z][A-Za-z0-9+#.]*)?\b|\b[A-Za-z]+[+#/.][A-Za-z0-9+#]*\b", ad_text))
    terms = set()
    for t in raw_terms:
        t = ADJ_PREFIX.sub("", t.strip()).lower()
        parts = t.split()
        if len(t) > 1 and t not in STOP and not all(w in STOP for w in parts):
            terms.add(t)
    # split CI/CD style into a single term kept as-is
    terms = {t for t in terms if t not in {"ci", "cd"}} | ({"ci/cd"} if re.search(r"ci\s*/\s*cd", ad_text, re.I) else set())
    terms |= {k for k, v in ad.items() if v >= 2 and " " not in k}
    present = sorted(t for t in terms if re.search(r"(?<![a-z])" + re.escape(t) + r"(?![a-z])", cv_low))
    missing = sorted(t for t in terms if t not in present)
    return {"ad_terms_checked": len(terms), "present": present, "missing": missing,
            "note": "Literal match only; review 'missing' by hand — many are generic words or synonyms (K8s/Kubernetes)."}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cv")
    ap.add_argument("--job-ad")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--max-chars", type=int, default=3000)
    a = ap.parse_args()
    p = Path(a.cv)
    ext = p.suffix.lower()
    if ext == ".pdf":
        text, info = extract_pdf(p)
    elif ext == ".docx":
        text, info = extract_docx(p)
    elif ext in (".txt", ".md"):
        text, info = p.read_text(errors="ignore"), {"note": "plain text — layout checks skipped"}
    else:
        print(f"Unsupported file type {ext}; convert to PDF or DOCX.", file=sys.stderr)
        sys.exit(2)

    words = len(text.split())
    findings = []
    def add(sev, msg):
        findings.append({"severity": sev, "finding": msg})

    if words < 80:
        add("CRITICAL", f"Only {words} words extracted — the file is probably an image/scan or text is outlined. ATS will see almost nothing.")
    cpp = info.get("chars_per_page") or []
    for i, c in enumerate(cpp, 1):
        if c < 50:
            add("HIGH", f"Page {i} has almost no extractable text ({c} chars) — image-only page?")
    if info.get("multi_column_pages"):
        add("HIGH", f"Possible multi-column layout ({info['multi_column_pages']}). Check the extracted text below reads in order.")
    ne = info.get("fonts_not_embedded") or []
    base14 = ("helvetica", "times", "courier")
    risky = [f for f in ne if not f.lower().startswith(base14)]
    if ne and not risky:
        add("LOW", f"Standard fonts not embedded ({ne}) — usually fine, viewers substitute them.")
    if risky:
        add("MEDIUM", f"Fonts not embedded: {risky}. Symbols/icons may render as boxes on the recruiter's machine; re-export with fonts embedded (Word: 'Embed fonts in file' / 'PDF/A').")
    ps = info.get("page_size")
    if ps and ps not in ("A4", "US Letter"):
        add("MEDIUM", f"Non-standard page size ({ps}) — prints badly and may scale oddly. Use A4 for EU/UK, US Letter for US/Canada.")
    elif ps == "US Letter":
        add("LOW", "US Letter page size — fine for US/Canada; use A4 for Sweden/EU/UK.")
    if info.get("tables"):
        add("MEDIUM", f"{info['tables']} table(s) detected. Fine for small things; risky if used for overall layout.")
    if info.get("text_boxes"):
        add("HIGH", f"{info['text_boxes']} text box(es) — many ATS skip text-box content.")
    if info.get("header_footer_contact"):
        body_has_email = bool(EMAIL_RE.search(text)) if ext == ".docx" else None
        if body_has_email:
            pass  # duplicated in body: fine
        elif ext == ".docx":
            add("MEDIUM", "Contact details only in header/footer — some parsers ignore those regions; put them in the body.")
        else:
            add("LOW", "Contact details sit near the top/bottom page edge. If they are in a real PDF header/footer (not body text), some parsers skip them — check the source document.")
    if info.get("images"):
        add("LOW", f"{info['images']} image(s) (photo/logos/icons) — ignored by ATS; icon-only contact info would be lost.")
    dingbats = any("dingbat" in f.lower() or "fontawesome" in f.lower() for f in (info.get("fonts") or {}))
    alt = ""
    if ext == ".pdf":
        try:
            alt = subprocess.run(["pdftotext", str(p), "-"], capture_output=True, text=True, timeout=20).stdout
        except Exception:
            pass
    spaced = re.findall(r"(?m)^\s*((?:[A-Z&]{1,2} ){3,}[A-Z&]{1,2})\s*$", text + "\n" + alt)
    if spaced:
        add("MEDIUM", f"Letter-spaced headings extract as separate letters in at least one common extractor {spaced[:4]} — some parsers won't match them to standard sections. Use normal letter spacing (style with size/weight instead).")
    links = list(dict.fromkeys(info.get("links") or []))
    if links:
        text_low = text.lower()
        profile_links = [u for u in links if not u.startswith(("mailto:", "tel:"))]
        hidden = [u for u in profile_links if re.sub(r"^(https?://)?(www\.)?", "", u.lower()).rstrip("/") not in text_low]
        if hidden:
            add("LOW", f"Links only clickable, not visible as full text (lost on print/parse): {hidden[:6]}. Also verify each points where you expect.")
    if info.get("drawn_bar_pages"):
        add("LOW", f"Many thin bar shapes on page(s) {info['drawn_bar_pages']} — possibly graphical skill/language bars (or just divider lines). Check the rendered page; bars are invisible to ATS.")
    long_tokens = [t for t in text.split() if len(t) > 30 and not URL_RE.match(t) and not EMAIL_RE.match(t)]
    if len(long_tokens) >= 5:
        add("HIGH", f"{len(long_tokens)} run-together words (e.g. {long_tokens[0][:40]!r}) — the PDF text layer has no real spaces (common with some LaTeX/design exports). Some ATS will fail keyword matches. Re-export, or for LaTeX add \\pdfgentounicode / use a different font setup.")
    rating_run = re.search(r"[●○◉◯★☆▪▫■□]{3,}", text)
    lllln = re.search(r"\b[ln]{5}\b", text)
    if dingbats and not (rating_run or lllln):
        add("LOW", "Icon/symbol font in use (e.g. Font Awesome, ZapfDingbats) — icons extract as junk characters; make sure no information (phone, email, links, levels) exists only as an icon.")
    if rating_run or lllln:
        add("MEDIUM", "Rating symbols in a row (e.g. ●●●○○) or a symbol font found — likely skill ratings; unreadable to ATS. (Single ● bullets are fine.)")
    if "�" in text or re.search(r"\(cid:\d+\)", text):
        add("MEDIUM", "Garbled characters in extraction (font encoding) — some text may be unreadable to ATS.")

    contacts = {
        "email": EMAIL_RE.findall(text)[:2],
        "phone": [m.strip() for m in PHONE_RE.findall(text)][:2],
        "linkedin": LINKEDIN_RE.findall(text)[:1],
        "github": GITHUB_RE.findall(text)[:1],
        "other_urls": [u for u in URL_RE.findall(text) if "linkedin" not in u.lower() and "github" not in u.lower()][:3],
    }
    if not contacts["email"]:
        add("HIGH", "No email address detected in text.")
    if not contacts["phone"]:
        add("LOW", "No phone number detected.")
    if not contacts["linkedin"]:
        add("LOW", "No LinkedIn URL detected as text (icon links are invisible to ATS).")

    found, nonstd = find_headings(text)
    low_found = " ".join(h.lower() for h in found)
    for core, alts in EXPECTED_CORE.items():
        if not any(alt in low_found for alt in alts):
            add("MEDIUM", f"No standard '{core.title()}' heading detected.")
    if nonstd:
        add("LOW", f"Uppercase lines that may be non-standard headings: {nonstd[:8]}")

    date_counts = {k: len(r.findall(text)) for k, r in DATE_PATTERNS.items()}
    date_counts["YYYY–YYYY"] = len(YEAR_ONLY.findall(text))
    used = {k: v for k, v in date_counts.items() if v}
    if len(used) > 1:
        add("LOW", f"Mixed date formats: {used}. Pick one.")

    pages = info.get("pages")
    report = {
        "file": str(p), "pages": pages, "words": words,
        "fonts": info.get("fonts"), "contacts_detected": contacts,
        "standard_headings_found": found, "hyperlinks": list(dict.fromkeys(info.get("links") or [])), "date_formats": used,
        "findings": findings,
        "extracted_text_sample": text[: a.max_chars],
    }
    if info.get("note"):
        report["note"] = info["note"]
    if a.job_ad:
        report["job_ad_match"] = job_match(text, Path(a.job_ad).read_text(errors="ignore"))

    if a.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return
    print(f"== ATS check: {p.name} ==")
    print(f"Pages: {pages}  Size: {info.get('page_size')}  Words: {words}  Fonts: {info.get('fonts')}")
    print(f"Contacts: {json.dumps(contacts, ensure_ascii=False)}")
    print(f"Standard headings: {found}")
    if info.get("links"):
        print(f"Hyperlinks: {list(dict.fromkeys(info['links']))}")
    print(f"Date formats: {used}")
    print("\n-- Findings --")
    if not findings:
        print("No parse problems detected.")
    for f in sorted(findings, key=lambda x: ["CRITICAL", "HIGH", "MEDIUM", "LOW"].index(x["severity"])):
        print(f"[{f['severity']}] {f['finding']}")
    if a.job_ad:
        jm = report["job_ad_match"]
        print(f"\n-- Job ad keyword match ({len(jm['present'])}/{jm['ad_terms_checked']} literal) --")
        print("Present:", ", ".join(jm["present"]))
        print("Missing:", ", ".join(jm["missing"]))
        print(jm["note"])
    print(f"\n-- Extracted text (first {a.max_chars} chars, as an ATS would read it) --")
    print(text[: a.max_chars])


if __name__ == "__main__":
    main()
