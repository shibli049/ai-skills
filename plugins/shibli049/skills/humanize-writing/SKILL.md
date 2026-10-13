---
name: "humanize-writing"
description: "Write and rewrite everyday prose so it reads like a person wrote it, not a chatbot: concise, specific, plain words, varied rhythm, no invented details, and none of the tells catalogued on Wikipedia's 'Signs of AI writing' page (em dashes, puffery, 'delve/crucial/showcase' vocabulary, 'not just X but Y', rule of three, bold-label bullet lists, 'I hope this helps', etc.). Use this whenever you draft or edit text a person will send or post: emails, Slack/Teams messages and replies (including detailed technical explanations in chat), LinkedIn or blog posts, cover letters, bios, essays, reviews, announcements, or feedback. Also use it when the user asks to humanize, de-AI, rewrite, polish, tighten, or make text sound natural or less robotic, even if they don't name the skill. For documentation files and pages (README, Confluence, wiki, runbook, ADR, API docs, PR descriptions, commit messages, changelogs) use the tech-docs skill instead."
---

# Humanize writing

Readers now recognize chatbot prose on sight, and once they do they stop trusting it. The tells are not random: a model drifts toward the safest, most generic sentence, so specific facts get replaced by praise, plain verbs by grand ones, and every claim gets padded. Writing that sounds human does the opposite. It says the specific thing, in plain words, at the length the content needs, and stops.

## Length

Cut words, not substance. Remove what the reader wouldn't miss: preamble, restating the question, summaries of what you just said, closing offers, filler. Keep every fact, number, name, date, caveat, and step the reader needs to act.

Clarity beats brevity. Keep or add a detail when leaving it out could confuse the reader, let them draw the wrong conclusion, or send them back with a follow-up question. That includes edge cases, the reason behind a rule, the condition under which something stops being true, and the step a newcomer wouldn't know to take. A test: if the reader could act wrongly on the shorter version, it's too short.

For short messages (emails, chat replies, posts) that usually means a few sentences. When the user asks you to explain, elaborate, or go into detail, cover each point the reader needs, not a sample of them. Write in tight sentences, but don't trim the list of points to look concise. A long, complete answer with no padding is the goal.

Before writing a detailed explanation, list for yourself the points a senior colleague in that field would expect it to cover. Include the operational ones that are easy to skip: how it behaves during deploys and rollbacks (staged or zero-downtime changes, several instances running at once), what happens when it fails, and the security and performance consequences. Then make sure each point that applies is in the draft. A thorough answer that leaves out the thing that bites people in production is still incomplete.

When rewriting someone's draft, keep their meaning, facts, and voice. Remove the tells; don't impose a new personality.

## Don't invent anything

This applies to every kind of writing: drafts, rewrites, messages, and posts. Specific details make text feel human, so the temptation is to invent one: a project name, a start date, "I'll be back Monday", "the wedding is that weekend", what the new job involves, a command the repo probably has. Don't put guesses into the text, even plausible or harmless-looking ones, because the person may send or publish it without checking. Use only what the user told you, what's in the files you were given, and what follows directly from them. If a detail would help, mention it outside the text ("you could add when you're back") and let them supply it.

The same goes for the user's team, company, or setup. Don't write "what we do here", "our setup", or "we always..." unless they told you how they work. Present advice as advice ("Set `ddl-auto=validate`"), not as a description of their current practice.

## Hard rules

These are the user's explicit requirements. Treat them as non-negotiable.

1. **No em dashes (—), and no en dashes (–) or spaced hyphens ( - ) standing in for them.** Use a comma, colon, semicolon, parentheses, or a new sentence. Vary which one, because text that only uses commas and periods has become its own tell.
2. **No careless word repetition.** Don't reuse the same content word within a sentence or in back-to-back sentences, and don't open consecutive sentences the same way. Fix it by restructuring or using a pronoun. Do not fix it by cycling synonyms for one thing ("the artists... these creators... the painters"); that is a separate AI tell and it confuses readers. One thing keeps one name.
3. **No unnecessary emphasis.** No bold or italics scattered inside sentences, no ALL CAPS, no exclamation marks for energy, no intensifiers (*truly, incredibly, absolutely, extremely*) unless they carry real information. Emphasis that helps the reader navigate is necessary, not decoration: bold section headers in a long structured reply, and bold on the one warning a reader must not miss, are fine (see Format).
4. **No clichés and no stock AI phrases.** See the list below and the full catalog.

## The tells to avoid

The full list, with examples and fixes for every pattern on Wikipedia's page, is in `references/ai-writing-patterns.md`. Read it before writing anything longer than a few paragraphs, or when a draft feels off and you can't say why. The short version:

**Content**
- Inflating significance: *serves as a testament, plays a pivotal role, marks a turning point, reflects broader trends, leaves an indelible mark, evolving landscape*. State the fact; if it mattered, say what changed.
- Trailing *-ing* commentary: "..., highlighting its importance", "..., ensuring quality", "..., fostering collaboration". End the sentence at the fact.
- Brochure language: *vibrant, rich, nestled, in the heart of, boasts, groundbreaking, renowned, seamless, diverse array, commitment to*.
- Vague links (*associated with, in connection with*) where a direct verb (*taught, ran, built*) is true.
- Weasel attributions: *experts argue, observers note, industry reports, many believe*. Name the source or own the claim.
- Formula endings: "Despite these challenges...", "The future looks bright", "In conclusion", "Overall", a closing line restating the point.

**Language**
- AI vocabulary: *delve, crucial, pivotal, key (adj.), landscape, tapestry, testament, underscore, highlight (verb), showcase, foster, enhance, leverage, robust, intricate, meticulous, vibrant, valuable, multifaceted, align with, additionally, moreover, furthermore, notably*. Use the plain word or delete it.
- Dodging *is/are/has*: *serves as, stands as, functions as, boasts, features*. Plain copulas are fine.
- Negative parallelism: "not only X but also Y", "it's not X, it's Y", "X rather than Y", "no X, no Y, just Z". Say Y.
- Reflexive triplets ("fast, reliable, and scalable"). Use the number of items that exist.
- Stiff verbs: *utilize, facilitate, commence, endeavor, authored, relocated*. Use *use, help, start, try, wrote, moved*.
- Filler: *it's important to note, it's worth mentioning, in order to, the fact that, when it comes to, at the end of the day, in today's fast-paced world*.
- Intensifiers and softeners that add nothing: *actually, really, basically, simply, just, quite, truly*. "What `update` actually does" implies the reader was wrong; drop the word.
- Clichés and idioms: *the hard way, bites you, works on my machine, low-hanging fruit, move the needle, game changer, deep dive, the elephant in the room, double-edged sword, a perfect storm*. Say the plain thing ("before it causes an outage").
- Slogan fragments for drama: "That's all it does. It only adds." or bullets that open with a punchline ("Failures are quiet.", "Nobody reviews it."). State the fact in a normal sentence: "If an `ALTER` fails, Hibernate logs it and the app starts anyway."
- Rhetorical questions as lead-ins ("Adopting Flyway on an existing database?"). Write the statement: "On an existing database, use a baseline.

**Format**

Short pieces (emails, quick replies, posts, anything a reader takes in at a glance) stay plain:
- No headings, no bold, no emoji, no `---` dividers.
- No bullet lists with bold labels and colons ("**Speed:** ..."). Use prose when ideas connect; a plain list when they don't.
- No tables for what one sentence can say.

Long or technical explanations (roughly 250 words and up, or anything a reader will scan and come back to, such as a detailed Slack answer, a design explanation, or an incident write-up) need visible structure. A wall of paragraphs is hard to follow even when every sentence is clean:
- Split it into sections with short, specific headers that say what the section answers: "What `ddl-auto=update` can't do", "What we do instead". Not generic ones like "Key benefits" or "Overview". Use sentence case.
- Under each header, use prose for reasoning and a bullet or numbered list for parallel items such as failure cases, steps, or rules.
- Put code, config keys, commands, and file names in code formatting so they stand out from the prose.
- Bold is for the section headers and for at most one critical warning. Don't bold words inside sentences.
- End with the practical takeaway (what to do, the rule of thumb), not a summary of what you said.

Match the destination's formatting. Slack and Teams render bold, lists, and code, so use them there (Slack uses `*bold*`). Emails and plain-text fields get no Markdown; use short paragraphs and, if needed, plain numbered lines.

**Chat leakage**
- No *Certainly!, Great question!, You're absolutely right, I hope this helps, Let me know if you'd like, Would you like me to, Here's a...*. Hand over the text itself.
- No opener that reacts to the question (*Good question, Good thing to ask, Great point, Fair question*), and no signpost that announces the answer (*Here's the longer version, The short version:, Here's why, Let's break it down, In a nutshell*). Start with the first real sentence of the answer.
- No "I hope this message finds you well", no unfilled *[Your Name]* placeholders. If you need a detail, ask, or point out the gap outside the text.
- No hedges about sources (*based on available information, details are scarce*). If you don't know, say so once or leave it out.

## What to do instead

- Lead with the point. The first sentence should be one the reader would miss.
- Prefer concrete over abstract: a number, a name, a date, an example.
- Use plain verbs and *is/has*. Use contractions where the register allows.
- Vary sentence length. Some short. Some longer, with a clause that adds a reason or a condition.
- Mix punctuation naturally: a colon to introduce, parentheses for an aside, a semicolon now and then.
- Make definite claims when they're true (*the first, the only*); hedge only when you're actually unsure.
- Write like the person would talk to a smart colleague. Casual where the context is casual.

## Check before handing over

After writing, review the whole draft before handing it over. Do this as a separate pass once the draft exists, not in your head while writing: reread the actual text, and for anything longer than a short message, also check it against `references/ai-writing-patterns.md`. Tells slip in during drafting no matter how carefully you write, and you only catch them on a reread. Removing tells is only part of the job; the text also has to be correct and easy to follow. Read it through once for each of these:

1. **Grammar and spelling.** Fix typos, subject-verb agreement, tense shifts, wrong word forms, missing or doubled words, and punctuation errors. Keep the spelling variant (US or UK) consistent and matching the user's. Check names, product terms, and identifiers against the source, because a misspelled name or config key is a factual error, not a style issue.
2. **Clarity as a whole.** Read it as the intended reader, without the context in your head. For a long piece, can the reader find each part by scanning the headers? Does each sentence say one clear thing? Is it obvious what every "it", "this", and "they" refers to? Could anything be read two ways? Does the order make sense, with what the reader needs first? Are terms the reader may not know explained or avoidable? Rewrite any sentence you had to read twice.
3. **Accuracy and completeness.** Every fact, number, name, date, and command matches what the user gave you or what's in the files. Nothing was invented, and nothing important was dropped while tightening. For explanations, check the draft against the list of points you made before writing.
4. **AI tells.** Reread as a skeptical reader who has seen a lot of ChatGPT output. Edits made in steps 1 and 2 can bring tells back in (a "crucial" here, a dash there), so check after them, not before. Scan specifically for:
   - any em dash (—) or en dash (–), or a spaced hyphen standing in for one;
   - words from the AI vocabulary list above;
   - "not just X, it's Y" and its variants;
   - a comma followed by an *-ing* clause that comments on the sentence ("..., highlighting...");
   - lists of exactly three that exist only for rhythm;
   - the same content word twice in one sentence, or consecutive sentences opening the same way;
   - sentences that are all about the same length, or punctuation that is only commas and periods;
   - an opener or sign-off addressed to the user instead of the reader, including "Good question" style reactions and "Here's the longer version" signposts;
   - *actually, really, basically*, clichés and idioms, slogan fragments, and rhetorical questions.

   In a long technical reply, repeating the exact name of a config key, command, or component is correct, so don't "fix" it. A word like *key* in "API key" is fine.

Don't over-correct. Perfect grammar, formal vocabulary in general, and an occasional transition word are not AI tells. The goal is natural writing, not writing that dodges a list.

## Example

Before:
> Certainly! Our new caching layer isn't just a performance tweak — it's a fundamental shift in how we deliver value. By leveraging Redis, it seamlessly enhances response times (median down from 420 ms to 90 ms), reduces database load (reads down roughly 70%), and improves scalability, underscoring our commitment to a robust user experience. It's worth noting that entries expire after five minutes. I hope this helps!

After:
> The new Redis cache cut median response time from 420 ms to 90 ms and dropped database reads by about 70%. Cache entries expire after five minutes, so prices can lag by that much.

The rewrite is shorter, keeps every fact, adds the one caveat a reader needs, and has nothing to flag.
