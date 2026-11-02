# ATS: what matters and how much

Applicant Tracking Systems (Workday, Greenhouse, Lever, SmartRecruiters, iCIMS, Taleo; in the Nordics often Teamtailor, Varbi, ReachMee, Jobylon) parse the CV into structured fields and let recruiters filter or search by keyword. Most do not auto-reject on a score; the real risks are (a) the parser garbling the CV so the profile looks empty or wrong, and (b) the CV not containing the literal terms a recruiter searches for.

## Severity of common findings

| Finding | Severity | Why / fix |
|---|---|---|
| No extractable text (scanned image, text as vector outlines, Canva export flattened) | Critical | Parser sees nothing. Re-export from Word/Google Docs/LaTeX with real text. |
| Multi-column layout | High | Reading order often interleaves columns: job titles end up next to the wrong dates, skills merge into experience. Use single column; a narrow sidebar is the most common culprit. |
| Tables / text boxes used for layout | High | Many parsers skip text boxes entirely or read cells out of order. |
| Contact info only in header/footer | Medium–High | Some parsers ignore header/footer regions; put email/phone/links in the body. |
| Non-standard section headings ("My Journey", "What I bring", "Toolbox") | Medium | Parser can't map to Experience/Skills. Use "Experience" / "Work Experience", "Skills" / "Technical Skills", "Education", "Projects", "Certifications", "Languages". |
| Inconsistent or ambiguous dates ("'19–now", "Spring 2020") | Medium | Breaks tenure calculation. Use "MMM YYYY – MMM YYYY" or "MM/YYYY", "Present" for current. Be consistent. |
| Skill bars, stars, icons for skills | Medium | Invisible to ATS, meaningless to humans. Replace with grouped text. |
| Images, logos, photo | Low–Medium | Ignored by parser; photo is market-dependent (see markets.md). Logos waste space. |
| Text layer has no spaces (words run together on extraction; common with some LaTeX templates and design tools) | High | Keyword search for "Spring Boot" fails on "LedbackendteamSpringBoot". LaTeX: add `\pdfgentounicode=1` and `\input{glyphtounicode}`, or switch font package; other tools: re-export. Check by copy-pasting text from the PDF. |
| Page size not A4/Letter (e.g. 595×900pt) | Medium | Prints cropped or scaled. Use A4 for EU/UK/Sweden, US Letter for US/Canada. Letter in Sweden is a small issue, not a blocker. |
| Letter-spaced headings ("E X P E R I E N C E") | Medium | Some extractors keep the spaces, so the parser can't recognise the section. Use normal spacing; style with size/weight. |
| Hidden or mismatched links (link text says one URL, target is another) | Medium | Looks careless or suspicious. Check every link target. |
| Contact details only inside a letterhead image | Medium | Parser finds no contact at all. Put them as text (for consultant profiles: the consultancy's contact). |
| Fonts not embedded (esp. symbol/icon fonts like ZapfDingbats, FontAwesome) | Medium | Icons, dots and bullets can render as empty boxes on the recruiter's screen. Re-export with fonts embedded. Standard Helvetica/Times not embedded is usually fine. |
| Unusual fonts, ligatures, special bullets (➤, ★) | Low | Usually fine; occasional garbled characters. Stick to standard fonts and •/–. |
| File type | Low | PDF (text-based) and DOCX both fine for modern ATS. Follow the posting if it specifies. Name the file `Firstname-Lastname-CV.pdf`. |
| Length | Market-dependent | See markets.md. ATS doesn't care; recruiters do. |

## Keywords

- ATS search is mostly literal. Write the term the job ad uses and, for common acronyms, both forms once: "Continuous Integration/Continuous Delivery (CI/CD)", "Kubernetes (AKS)", "Amazon Web Services (AWS)".
- Keywords should appear **in context** in experience bullets, not only in a skills list. Recruiters and hiring managers both discount a skill that appears only in a list.
- Don't keyword-stuff or use white/hidden text — modern parsers and recruiters catch it and it reads as dishonest.
- Version numbers rarely matter except where they signal currency (Java 17/21, Spring Boot 3, Angular vs AngularJS).

## Interpreting the script

`scripts/ats_check.py` uses pdfplumber/python-docx heuristics. Column detection looks at x-positions of words; it can false-positive on right-aligned dates (which are fine). Check the extracted-text sample: if lines read in a sensible order, layout is OK regardless of the heuristic.
