# Catalog of AI writing patterns

Source: [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), read October 2026. Wikipedia editors compiled the list to spot chatbot text in articles. Every pattern from the page is here, grouped the same way. Patterns that only matter for Wikipedia markup are listed briefly at the end.

Use this file in two ways: skim it before writing something long, and check a finished draft against it. Each entry gives the tell, what it looks like, and what to write instead.

## Contents

1. Content patterns
2. Language and grammar
3. Style and formatting
4. Chat leakage (text meant for the user, not the reader)
5. Older tells that still give text away (5b: other stock patterns from review)
6. What human writing tends to have
7. Wikipedia-only markup tells
8. Things that are NOT reliable tells

---

## 1. Content patterns

The root cause behind most of these: a model drifts toward the statistically safest sentence. Specific, odd facts ("invented the first train-coupling device") get smoothed into generic praise ("a revolutionary titan of industry"). Each pattern below is a symptom of that.

### 1.1 Inflated significance, legacy, broader trends
Tacking on claims that an ordinary fact represents or contributes to something bigger.
- Phrases: *stands/serves as, is a testament/reminder, a crucial/pivotal/vital/significant/key role/moment, underscores/highlights its importance, reflects broader, symbolizing its ongoing/enduring/lasting, contributing to the, setting the stage for, marking/shaping the, represents/marks a shift, key turning point, evolving landscape, focal point, indelible mark, deeply rooted, this distinction matters because*.
- Also: placing the subject amid "broader debates" or "public discussions", "raising philosophical questions", "prompted broader reflection".
- Also: admitting a subject is minor, then praising its importance anyway.
- Also: belaboring links to "the broader ecosystem" or conservation, research, or preservation efforts that may not exist.
- Instead: state the fact. If it really did matter, say what changed and for whom, with a number or name.

### 1.2 Canned emphasis on notability and media coverage
Proving importance by listing where something was covered and what kind of outlet it was.
- Phrases: *independent coverage, local/regional/national media outlets, trade publications, cited/featured/profiled in, other prominent media outlets, written by a leading expert, maintains an active social media presence, was identified by*.
- Instead: cite the specific source for the specific claim, or drop it.

### 1.3 Superficial analysis (trailing participle commentary)
A fact followed by a comma and an "-ing" clause that interprets it.
- Phrases: *highlighting/underscoring/emphasizing..., ensuring..., reflecting/symbolizing..., contributing to..., cultivating/fostering..., encompassing..., enhancing..., valuable insights, align/resonate with*.
- Example: "The population was 56,998, *creating a lively community within its borders*."
- Instead: end the sentence at the fact. Add analysis only if you can back it, and give it its own sentence.

### 1.4 Promotional, travel-brochure language
- Words: *boasts a, vibrant, rich (heritage/history), profound, enhancing, showcasing, exemplifies, commitment to, natural beauty, nestled, in the heart of, groundbreaking, renowned, featuring, diverse array, seamless/seamlessly, gateway to, every traveller's journey*.
- Press-release tone about people and companies: "emphasized the company's commitment to sustainability, customer focus, and prosperity".
- Instead: neutral, concrete description. "The town has a weekly market" beats "the town boasts a vibrant market scene".

### 1.5 Vague connection or association
Hedging a direct relationship into a fuzzy one.
- Phrases: *in connection with, connected with/to, in association with, associated with, became associated with*.
- Example: "He became associated with musical education in Knokke-Heist" when he *taught violin* there.
- Instead: say the relationship. Taught, ran, founded, worked for, wrote.

### 1.6 Vague attributions and overgeneralized opinions (weasel words)
- Phrases: *industry reports, observers have cited, experts argue, some critics argue, researchers and conservationists, described in scholarship, modern researchers treat, several sources* (when there's one), *such as* (before a list that is actually complete).
- Instead: name who said it, or own the claim, or cut it.

### 1.7 Formula conclusions about challenges and future prospects
- Shape: "Despite its [praise], X faces several challenges..." ending with "Despite these challenges, X continues to..." or speculation about the future.
- Headings: *Challenges and Legacy, Future Outlook, Future Prospects*.
- Instead: if a real problem exists, state it plainly where it belongs. Don't end on uplift.

### 1.8 "X and Y" section headings, especially "Awards and recognition"
- Instead: name sections for what's in them. One noun is usually enough.

---

## 2. Language and grammar

### 2.1 AI vocabulary
These words became far more frequent after 2022. One alone proves nothing. Several together read as machine-written.
- 2023 to mid-2024: *additionally (to open a sentence), boasts, bolstered, crucial, delve, emphasizing, enduring, garner, intricate/intricacies, interplay, key (adjective), landscape (abstract), meticulous/meticulously, pivotal, underscore (verb), tapestry (abstract), testament, valuable, vibrant*.
- Mid-2024 to mid-2025: *align with, bolstered, crucial, emphasizing, enhance, enduring, fostering, highlighting, pivotal, showcasing, underscore, vibrant*.
- Mid-2025 to mid-2026: *emphasizing, enhance, highlighting, showcasing*, plus the notability phrases in 1.2.
- Mid-2026 onward: *challenge, clearer, dependable, echoed, foster, leverage, matters, multifaceted, practical, prioritize, quietly, steady, universally*, with very even 8 to 20 word sentences and almost only commas and periods.
- Also flagged: *robust, deep dive, showcase, highlight (verb)*. Grok-style: *causal, empirical, correlate*.
- Instead: the plain word. *has, important, look at, shows, improve, use, detailed, area/field*. Often the best fix is deleting the word.

### 2.2 Avoiding "is" and "are"
Replacing a plain copula with something grander.
- Phrases: *serves as, stands as, marks, functions as, operates as, represents, boasts, features, maintains, offers, refers to* (when you mean "is").
- Example: "The library serves as a hub for..." → "The library is where..."
- Instead: use *is*, *are*, *has*. They are fine.

### 2.3 Negative parallelism
Framing as if correcting a misconception nobody had.
- "Not only X, but also Y" / "It's not just X, it's Y" / "doesn't just X; it Y".
- "Not X, but Y" / "It's not X, it's Y" / "No X, no Y, just Z" / "This isn't A, it's B".
- Reversed: "Y rather than X", "Rather than simply X, it Y".
- Instead: state Y. Mention X only if someone actually believes it.

### 2.4 Rule of three
Reflexive triplets: "adjective, adjective, adjective" or "phrase, phrase, and phrase", used to sound thorough.
- Example: "mythological image, magical weapons, and spirit of resistance".
- Instead: list the number of items that actually exist. Two is fine. One is often better.

### 2.5 Elegant variation (synonym cycling)
Avoiding repetition by rotating synonyms for the same thing: "the artists... these creators... the non-conformists... like-minded painters".
- This is a trap when you try to avoid repeating words. Readers get confused about whether you mean different things.
- Instead: pick one term for one thing and keep it, or use a pronoun, or restructure so the noun isn't needed twice. What you're avoiding is clumsy repetition (the same word twice in a sentence, or every sentence opening the same way). Repeating a term that names one thing is fine.

### 2.6 Lists or broad titles treated as proper nouns
"The List of X refers to a curated collection of..."
- Instead: talk about the thing itself, not the label.

---

## 3. Style and formatting

### 3.1 Title Case Headings
"Early Life And Career" instead of "Early life and career".
- Instead: sentence case, unless the house style says otherwise.

### 3.2 Boldface overuse
Bolding every key term, "key takeaways" style.
- Instead: no bold in prose. Bold at most one thing a reader must not miss.

### 3.3 Inline-header vertical lists
Bullets that each start with a bold label and a colon: "- **Performance:** The system..."
- Instead: prose when the items connect. A plain list when they don't. Labels only in genuine reference material.

### 3.4 Heading misuse
Headings on short pieces, skipped heading levels, top-level headings everywhere, headings that only contain other headings, a title heading repeated at the top.
- Instead: no headings for anything under ~300 words. For longer pieces, few and flat.

### 3.5 Emoji as formatting
Emoji in front of headings or bullets (✅ 🚀 📌 💡).
- Instead: none, unless the user's own writing uses them.

### 3.6 Unnecessary tables
Small tables holding what one sentence could say.
- Instead: a sentence. Tables only for real multi-column comparisons.

### 3.7 Thematic breaks between sections
`---` between every section.

### 3.8 Markdown where it doesn't belong
Asterisks and hashes in an email, chat message, form field, or anywhere that won't render them.
- Instead: match the destination's format.

### 3.9 Curly quotes (weak signal)
Some models output “curly” quotes. Weak tell on its own. Match what the user uses.

### 3.10 Em dashes (strong popular tell)
Models used em dashes far more than ordinary writers, often with spaces around them, to punch up a clause or a parallelism: "it's not a bug — it's a feature".
- Note: newer models that suppress em dashes swing to only commas and periods with sentences of even length. That flat rhythm is now its own tell.
- Instead: no em dashes (—) and no en dashes (–) used as dashes. Use a comma, colon, parentheses, semicolon, or a new sentence. Pick whichever fits, and use a mix across a piece.

---

## 4. Chat leakage

Text written *to the person asking* that ends up in text meant *for a reader*.

### 4.1 Collaborative communication
- Phrases: *Certainly!, Of course!, Great question!, You're absolutely right!, I hope this helps, Would you like me to..., Is there anything else, Let me know if..., Here is a..., Here's a more detailed breakdown, In this section, we will discuss...*
- Instead: deliver the text alone. No opener, no sign-off offer.

### 4.2 Hedging disclaimers about sources
- Phrases: *While specific details are limited/scarce, not widely documented/available/disclosed, in the provided/available sources, based on available information, should be treated as... rather than..., does not by itself establish...*
- Instead: if you don't know, say so once and plainly, or leave the claim out. Don't guess and then hedge the guess.

### 4.3 Placeholder templates
Unfilled blanks like *[Your Name], [Describe the specific section...], [Company]*. Also "I hope this message finds you well."
- Instead: fill them in, or ask for what you need. If a placeholder is unavoidable, flag it to the user outside the text.

### 4.4 Knowledge-cutoff and refusal text
*As of my last knowledge update, as an AI language model, I'm sorry but I cannot...*

---

## 5. Older tells that still give text away

### 5.1 Didactic disclaimers
*It's important to note, it's worth noting, it's crucial to remember, it's important to consider, may vary.*
- Instead: just say the thing.

### 5.2 Section summaries and conclusions
Paragraphs ending by restating their own point. Closing sections opening with *In summary, In conclusion, Overall, Ultimately*.
- Instead: stop when the content ends.

### 5.3 Signposting openers
*Additionally, Moreover, Furthermore, Notably, Consequently* opening sentence after sentence.
- One is fine. A chain of them is a tell.

---

## 5b. Other stock patterns (from review, not on the Wikipedia page)

The user flagged these in reviewed output. They read as chatbot habits even when every Wikipedia pattern is avoided.
- Openers that react to the question: *Good question, Good thing to ask, Great point, Fair question*.
- Signposts announcing the answer: *Here's the longer version, The short version:, Here's why, Let's break it down, In a nutshell*.
- Intensifiers that imply the reader was wrong or add nothing: *actually, really, basically, simply, just*.
- Clichés and idioms: *the hard way, bites you, works on my machine, low-hanging fruit, move the needle, under the hood, out of the box, game changer*.
- Slogan fragments for drama: "That's all it does. It only adds." Bullets that open with a punchline ("Failures are quiet.").
- Rhetorical questions as lead-ins: "Adopting Flyway on an existing database? Use a baseline."
- Instead: start with the first real sentence, state facts in full plain sentences, and make statements rather than questions.

## 6. What human writing tends to have

Wikipedia editors found these more common in human text than in AI text. Lean toward them.
- Plain *is/has* phrasing: "there is a", "it has a".
- Plain verbs over stiff ones: *wrote* not *authored*, *moved* not *relocated*, *used* not *utilized*, *tried* not *attempted*, *died* not *passed away*.
- Definite claims where true: *the first, the only, one of the best*.
- Normal qualifiers: *very, perhaps, tends to*, used sparingly.
- Specific, slightly unusual facts instead of generic praise.
- Varied sentence length and punctuation.

---

## 7. Wikipedia-only markup tells (for completeness)

These matter only when writing wikitext, but they're on the page:
- Markdown syntax in wikitext (`**bold**`, `#` headings, `[text](url)` links), broken wikitext, fenced code blocks around article text.
- Chatbot citation artifacts: `contentReference`, `oaicite`, `turn0search0`, `[cite: 1]`, `grok_card`, `【】` brackets, `attached_file`, `:::writing`, `utm_source=chatgpt.com`.
- Nonexistent categories or templates, fabricated or broken links, invalid DOIs/ISBNs, book citations without pages, unused named references.
- Pre-placed maintenance templates, canned user pages, AfC "submission statements".
- Edit summaries full of *ensured, refined, enhanced, streamlined, improved clarity and flow, preserved, retained, avoided, added sourced content, neutral/encyclopedic tone*.
- Abrupt cut-offs mid-sentence, outdated access-dates, a sudden shift in writing style or English variety.

The edit-summary list generalizes: commit messages, changelogs, and status updates written like *"Refined and enhanced X, ensuring clarity while preserving Y"* look AI-written. Say what changed.

---

## 8. Not reliable tells

The page warns against over-correcting. These don't mark text as AI, so there is no need to dumb writing down to avoid them:
- Perfect grammar.
- Mixing casual and formal registers.
- Formal or academic vocabulary in general (only the specific words above are tells).
- A single transition word.
- Correct formatting.
