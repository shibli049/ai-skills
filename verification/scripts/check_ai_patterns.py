#!/usr/bin/env python3
"""Flag common AI-writing tells in a draft.

Verification helper for the humanize-writing skill. It is not part of the
skill itself: use it to spot-check output while developing or testing the
skill. The patterns come from Wikipedia:Signs of AI writing.

Usage:
    python check_ai_patterns.py draft.md
    python check_ai_patterns.py --doc README.md      # technical docs
    echo "some text" | python check_ai_patterns.py -

--doc skips checks that misfire on reference material (bold labels, lists,
repeated technical terms, sentence rhythm) but keeps the prose tells.

Code blocks and inline code are skipped. Exit code is 1 if anything was
flagged, 0 if the draft is clean. Findings are hints: a human still decides.
"""

import re
import statistics
import sys
from collections import Counter

AI_WORDS = [
    "additionally", "align with", "aligns with", "boasts", "boast", "bolstered", "bolster",
    "crucial", "deep dive", "delve", "delves", "delving", "emphasizing", "enduring",
    "enhance", "enhances", "enhancing", "enhanced", "foster", "fosters", "fostering",
    "garner", "garnered", "highlighting", "interplay", "intricate", "intricacies",
    "landscape", "meticulous", "meticulously", "pivotal", "robust", "showcase",
    "showcases", "showcasing", "tapestry", "testament", "underscore", "underscores",
    "underscoring", "underscored", "valuable", "vibrant", "leverage", "leveraging",
    "multifaceted", "seamless", "seamlessly", "nestled", "groundbreaking", "renowned",
    "profound", "exemplifies", "realm", "paramount", "furthermore", "moreover",
    "notably", "utilize", "utilizes", "utilizing", "quietly", "universally",
    "game-changer", "game changer", "cutting-edge", "unlock", "unleash", "elevate",
    "empower", "embark", "navigate the", "ever-evolving", "ever-changing",
]

STOCK_PHRASES = [
    r"stands as", r"serves as", r"is a testament", r"is a reminder",
    r"(?:crucial|pivotal|vital|significant|key) (?:role|moment)",
    r"reflects broader", r"setting the stage", r"evolving landscape", r"focal point",
    r"indelible mark", r"deeply rooted", r"in the heart of", r"rich (?:history|heritage|tapestry|culture)",
    r"diverse array", r"commitment to", r"natural beauty",
    r"in connection with", r"in association with", r"(?:is|are|was|were|became) associated with",
    r"experts (?:argue|say|believe)", r"observers have", r"industry reports", r"some critics",
    r"despite (?:these|its|their) challenges", r"faces (?:several|numerous|many) challenges",
    r"future (?:outlook|prospects)",
    r"it'?s (?:important|worth|crucial|critical) to (?:note|remember|consider|mention)",
    r"worth noting", r"in (?:summary|conclusion)", r"^overall,", r"^ultimately,",
    r"i hope this (?:helps|message finds you)", r"certainly!", r"of course!", r"great question",
    r"you'?re absolutely right", r"would you like me to", r"let me know if",
    r"is there anything else", r"here(?:'s| is) (?:a|an|the) ", r"feel free to",
    r"as an ai", r"as of my last", r"based on (?:the )?available information",
    r"not widely (?:documented|available|disclosed)", r"while specific details are",
    r"plays? a (?:key|vital|crucial|significant|important) role",
    r"at the end of the day", r"when it comes to", r"in today'?s (?:fast-paced|digital|modern)",
    r"a (?:wide|broad) range of", r"dive (?:into|deeper)", r"let'?s dive", r"buckle up",
    r"the world of", r"look no further", r"without further ado", r"needless to say",
    r"in order to", r"the fact that",
    r"good (?:question|thing to ask)", r"great point", r"fair question",
    r"here'?s the (?:longer|short) version", r"the short version:", r"here'?s why",
    r"let'?s break (?:it|this) down", r"in a nutshell",
    r"\bactually\b", r"\bbasically\b",
    r"the hard way", r"bites? you", r"works on my machine", r"low-hanging fruit",
    r"move the needle", r"under the hood", r"out of the box",
    r"that'?s all it does",
]

NEG_PARALLEL = [
    r"\bnot only\b[^.]*\bbut\b",
    r"\bnot just\b[^.]*[,;:—–-]\s*(?:it|they|but)\b",
    r"\b(?:it|this|that)(?:'s| is| isn't| is not)\s+(?:not\s+)?(?:just\s+)?(?:about\s+)?[^.,;—]{1,40}\s*[,;—–-]\s*(?:it|this|that)(?:'s| is)\b",
    r"\b(?:isn'?t|wasn'?t|aren'?t)\b[^.]{1,40}[,;—–-]\s*(?:it|they)(?:'s| is| are|'re| was)\b",
    r"\b(?:don'?t|doesn'?t|didn'?t|won'?t) just\b",
    r"\brather than (?:simply|merely|just)\b",
]

TRAILING_PARTICIPLE = re.compile(
    r",\s+(?:highlighting|underscoring|emphasizing|reflecting|symbolizing|showcasing|"
    r"ensuring|fostering|cultivating|contributing to|enhancing|encompassing|"
    r"demonstrating|illustrating|marking|creating a|making it|solidifying|cementing)\b",
    re.I,
)

STOPWORDS = set("""
a an the and or but if of to in on at by for with from as is are was were be been being
it its this that these those i you he she we they them me my your our their his her
not no so do does did have has had can could will would should may might must just
than then there here what which who whom when where why how all any some each more most
very also only into out up down over about after before again one two s t don isn
""".split())

EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿✅❌⭐]")


def strip_code(text):
    text = re.sub(r"```.*?```", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", text)


DOC_SKIP = {
    "bold inline-header list item", "bold overuse", "list of three (check it's needed)",
    "repeated word in sentence", "flat rhythm", "repeated sentence opener",
}


def check(text, doc=False):
    findings = []
    lines = strip_code(text).split("\n")

    seen = set()

    def add(lineno, kind, detail):
        if doc and kind in DOC_SKIP:
            return
        if (lineno, kind) in seen and kind != "AI vocabulary" and kind != "stock phrase":
            return
        seen.add((lineno, kind))
        findings.append((lineno, kind, detail))

    word_re = {w: re.compile(r"\b" + re.escape(w) + r"\b", re.I) for w in AI_WORDS}
    phrase_re = [re.compile(p, re.I | re.M) for p in STOCK_PHRASES]
    neg_re = [re.compile(p, re.I) for p in NEG_PARALLEL]

    bold_count = 0
    for i, line in enumerate(lines, 1):
        if "—" in line:
            add(i, "em dash", "replace with comma, colon, parentheses, or a new sentence")
        if "–" in line or re.search(r"\s--?\s", line):
            add(i, "dash", "en dash or spaced hyphen used as a dash")
        for w, rx in word_re.items():
            if rx.search(line):
                add(i, "AI vocabulary", w)
        for rx in phrase_re:
            m = rx.search(line.strip())
            if m:
                add(i, "stock phrase", m.group(0).strip())
        for rx in neg_re:
            m = rx.search(line)
            if m:
                add(i, "negative parallelism", m.group(0)[:60])
        if re.match(r"\s*(?:(?:[-*\u2022]|\d+\.)\s+)?[A-Z][^.?!]{0,60}\?\s+\S", line):
            add(i, "rhetorical question lead-in", line.strip()[:60])
        m = TRAILING_PARTICIPLE.search(line)
        if m:
            add(i, "trailing -ing commentary", m.group(0).strip(", "))
        if EMOJI.search(line):
            add(i, "emoji", "")
        if re.match(r"\s*[-*\d.]+\s+\*\*[^*]+:\*\*|\s*[-*\d.]+\s+\*\*[^*]+\*\*:", line):
            add(i, "bold inline-header list item", "")
        bold_count += len(re.findall(r"\*\*[^*]+\*\*", line))
        if re.search(r"\b(\w+)(?:\s+\w+){0,2}\s*,\s*\w+(?:\s+\w+){0,2}\s*,\s*(?:and|or)\s+\w+", line):
            add(i, "list of three (check it's needed)", "")
        if re.search(r"\[[A-Z][^\]]{2,40}\]", line) and not re.search(r"\]\(", line):
            add(i, "placeholder?", re.search(r"\[[A-Z][^\]]{2,40}\]", line).group(0))

        # word repetition inside a sentence
        for sentence in re.split(r"(?<=[.!?])\s+", line):
            words = [w.lower() for w in re.findall(r"[A-Za-z']+", sentence)]
            counts = Counter(w for w in words if w not in STOPWORDS and len(w) > 3 and "'" not in w)
            repeated = [w for w, c in counts.items() if c > 1]
            if repeated:
                add(i, "repeated word in sentence", ", ".join(repeated))

    if bold_count > 3:
        add(0, "bold overuse", f"{bold_count} bold spans")

    prose = " ".join(l for l in lines if l.strip() and not l.lstrip().startswith(("#", "-", "*", "|", ">")))
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", prose) if len(s.split()) > 2]
    if len(sentences) >= 6:
        lengths = [len(s.split()) for s in sentences]
        sd = statistics.pstdev(lengths)
        if sd < 4:
            add(0, "flat rhythm", f"sentence lengths barely vary (stdev {sd:.1f}); mix short and long")
        openers = Counter(s.split()[0].lower() for s in sentences)
        for w, c in openers.items():
            if c >= 3 and c / len(sentences) > 0.25:
                add(0, "repeated sentence opener", f"'{w}' starts {c} sentences")

    return findings


def main():
    args = sys.argv[1:]
    doc = "--doc" in args
    args = [a for a in args if a != "--doc"]
    if len(args) != 1:
        print(__doc__)
        sys.exit(2)
    path = args[0]
    text = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
    findings = check(text, doc=doc)
    if not findings:
        print("No AI-writing patterns flagged.")
        sys.exit(0)
    for lineno, kind, detail in findings:
        where = f"line {lineno}" if lineno else "whole text"
        print(f"{where}: {kind}" + (f" ({detail})" if detail else ""))
    print(f"\n{len(findings)} finding(s). Review each; not every hit is wrong.")
    sys.exit(1)


if __name__ == "__main__":
    main()
