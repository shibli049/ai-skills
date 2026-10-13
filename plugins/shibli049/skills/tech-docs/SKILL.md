---
name: "tech-docs"
description: "Write or update technical documentation that reads like a senior engineer wrote it: accurate to the code, scannable, and free of AI-writing tells from Wikipedia's 'Signs of AI writing' page. Explores the project before writing and never invents commands, config, endpoints, or features. Use this for READMEs, Confluence pages, repo or GitHub/GitLab wikis, runbooks, ADRs, design docs, API references, how-to and onboarding guides, CLI docs, changelogs, release notes, PR descriptions, and commit messages, whether creating a new doc or updating an existing one, even if the user just says 'document this' or 'write up how X works'. For emails, chat messages, and posts use the humanize-writing skill instead."
---

# Technical docs

Readers come to docs to get something done: run the service, change a setting, decide whether to adopt a pattern, recover from an incident. They scan, they copy commands, and they trust what they read. That sets two priorities. First, every statement must be true of the code as it is today, because a wrong doc costs more time than a missing one. Second, the writing must be plain and specific, because chatbot prose (puffery, filler, vague claims) makes readers doubt the parts that are accurate.

This skill applies the same AI-writing rules as general writing, but with flexible formatting: headings, tables, lists, admonitions, and some bold are tools here, not tells.

## Procedure

### 1. Understand the request

Work out:
- **What** is being documented: a project, feature, API, decision, procedure, or change.
- **Who** reads it: new team members, users of an API, on-call engineers, reviewers.
- **Where** it goes: a file path in the repo (`README.md`, `docs/adr/0007-...md`), a wiki, a Confluence space, a PR description. The destination decides the format (see "Match the destination").

### 2. Read the source of truth before writing

A doc written without project context is worse than no doc. Before writing:
- Read the build files (`pom.xml`, `build.gradle`, `package.json`, `Makefile`) for the name, versions, runtime, dependencies, and the real build, test, and run commands.
- Read config (`application.yml`, `.env.example`, Helm values) for settings, environment variables, defaults, and ports.
- Read the entry points and the code the doc describes: controllers or routes for an API, the main class, scheduled jobs, CLI argument parsing.
- Check for CI workflows, Dockerfiles, compose files, migrations, OpenAPI specs, `CHANGELOG`, and ADR folders. Note what is absent as well as what is present.
- If a doc already exists at the target, read it fully before editing. Keep what is still true, fix what isn't, and match its structure and tone unless the user asked for a rewrite.
- Look at other docs in the repo to match established conventions: heading case, admonition style, how commands are shown.

For a PR description or commit message, read the actual diff. For a Confluence page written from a chat description with no repo access, the user's message is the only source of truth.

### 3. Table of contents

For a long doc (roughly five or more top-level sections), ask the user whether they want a ToC. If you can't ask, leave it out. Never add an empty ToC placeholder.

If yes, put it right below the intro as a nested bullet list: one entry per line, each a link to its heading's anchor, with each deeper heading level indented two more spaces under its parent. Match the heading text and order exactly, and stop at the levels a reader needs (usually `##` and `###`).

```markdown
## Contents

- [Run it locally](#run-it-locally)
  - [Prerequisites](#prerequisites)
  - [Steps](#steps)
- [Configuration](#configuration)
- [API](#api)
  - [Status codes](#status-codes)
- [Development](#development)
```

Anchors are the heading text lowercased, with spaces turned into hyphens and punctuation other than hyphens removed (`## Run it locally` becomes `#run-it-locally`). For Confluence, use the Table of Contents macro instead of a hand-written list.

### 4. Plan the structure

Pick sections for the doc type. Full scaffolds are in `references/templates.md` (README, ADR, guide/runbook, API reference, PR description, commit message, changelog entry). Omit any section with nothing real to say. A short, complete doc beats a long one with "TBD" sections.

### 5. Write

Follow the rules below, then create or replace the file (or hand over the page text for Confluence and wikis).

### 6. Review

See "Check before handing over" at the end.

## Accuracy: don't invent anything

Every command, file path, config key, environment variable, flag, default value, endpoint, port, version, dependency, and feature in the doc must exist in the repo or in what the user gave you. A made-up `npm run setup` or a plausible `APP_TIMEOUT` variable is worse than a gap, because readers trust docs and will lose an hour before suspecting the doc.

- Describe what is there, not what a typical project of this kind has. No Docker section without a Dockerfile, no test command you haven't found, no "supports X" unless the code does X.
- Badges only for things that exist: a CI badge needs a real workflow file, a version badge needs a real version. No license badge without a LICENSE file.
- Don't document planned or half-built features as working. If the code has a TODO, a stub, or returns "not implemented", say so plainly or leave it out.
- Copy commands, keys, and names exactly, including case. Don't "clean up" a name.
- Don't add helper commands or setup the repo doesn't have, even labelled as a suggestion or "untested": no `docker run` for a database when there's no compose file, no seed scripts, no `psql` one-liners, no curl calls to endpoints that don't exist. Name the prerequisite ("a PostgreSQL database reachable at `DB_URL`") and leave how to get it to the reader. If you think a helper would be useful, suggest it to the user in your notes, not in the doc.
- List only environment variables and properties that appear in the config files. Don't derive new ones (for example through Spring's relaxed binding) or document overrides the config doesn't define. If a setting can only be changed in a file, say that.
- Test the commands you include, which should all come from the repo, when you can. If you can't, don't present them as verified: mark the step (for example with a `[!WARNING]` that it needs credentials you didn't have), or leave a visible `TODO: confirm ...`. Marking a command as untested never makes an invented one acceptable.
- When you can't verify a fact (a staging URL, an owner, an SLA), don't guess. Ask, or leave `TODO: confirm the staging URL`, and list every TODO for the user when you hand the doc over.
- Examples (requests, responses, output) should come from the code, tests, or fixtures. If you have to construct one, keep it consistent with the real types and field names, and say it's illustrative if the values are made up.
- Don't describe the team's process or conventions ("we deploy on Fridays", "our on-call rota") unless the repo or the user says so.
- Behaviour you inferred from reading the code (for example "a missing id returns 500 because nothing handles the exception") should be stated with that basis, or flagged to the user, not presented as documented behaviour.

## Writing rules (strict, same as all writing)

These come from Wikipedia's "Signs of AI writing" and the user's own requirements. They apply to docs exactly as they apply to any prose. The full catalog with examples is in `references/ai-writing-patterns.md`; read it before writing a long doc.

- **No em dashes (—), and no en dashes (–) or spaced hyphens standing in for them.** Use a colon, comma, parentheses, or a new sentence. This includes list items: write "`--dry-run`: print the plan without applying it", not "`--dry-run` — print the plan".
- **No marketing or puffery.** *Powerful, seamless, robust, cutting-edge, comprehensive, blazing fast, state-of-the-art, game-changing, vibrant.* Say what it does. "The service exposes a REST API", not "this powerful service unleashes a cutting-edge REST API".
- **No AI vocabulary.** *Delve, crucial, pivotal, landscape, tapestry, testament, underscore, showcase, foster, enhance, leverage, streamline, intricate, meticulous, additionally, moreover, furthermore.* Use the plain word or cut it.
- **No filler words.** *Simply, just, easily, straightforward, obviously, actually, really, basically, it's important to note, in order to, the fact that.* "Simply run" is condescending when the step fails.
- **No clichés, idioms, or slogan fragments.** *The hard way, works on my machine, out of the box, under the hood, game changer.* No punchline-style fragments ("That's it. It just works."). Say the plain thing in a full sentence.
- **No significance padding or trailing *-ing* commentary.** "Caches responses for 5 minutes", not "caches responses, enhancing performance and ensuring a seamless experience".
- **No negative parallelisms** ("it's not just a library, it's a platform") and no reflexive lists of three.
- **No vague intros.** Not "This repository contains the source code for the payout service." Instead: "Stores merchant payouts in Postgres and moves pending ones to the bank every 15 minutes."
- **No formula sections**: no "Challenges and future outlook", no closing summary that restates the doc, no "Conclusion".
- **No chat leakage.** No "Here's the README", "I hope this helps", "Let me know if...", unfilled `[Your Name]` placeholders, or hedges like "based on available information".
- **No rhetorical questions**, and no first person ("I", "we") unless the doc type or repo convention uses it (ADRs and team runbooks often say "we").
- **No careless repetition, but keep one name per concept.** Don't repeat words for no reason, and never rotate synonyms for one thing ("the worker... the processor... the job runner"). In docs, readers assume different words mean different things.

## Formatting rules (flexible for docs)

General writing keeps short pieces plain. Docs are reference material that readers scan and return to, so structure helps. Use these tools when they make the doc easier to scan; don't add them for decoration.

- **Headings.** Use them to make sections findable. Sentence case by default ("Getting started", "Run it locally"); follow the repo's existing style if it uses title case. Keep levels in order (no jump from `##` to `####`), one `#` title per file, and no heading that only contains other headings.
- **Lists.** Numbered for steps done in order, bullets for parallel items. A label per item is fine when the label is a real identifier or name: "`retry.max-attempts`: retries before giving up. Default 3." Bold-label bullets that restate a sentence ("**Scalability:** The system scales well") are still a tell.
- **Tables.** For config options (name, type, default, meaning), endpoints, status codes, comparisons, and symptom/cause/fix troubleshooting. Not for a list a bullet list handles.
- **Code.** Fenced blocks with a language tag (`bash`, `java`, `json`, `yaml`, `sql`) for every command and sample. Inline code for identifiers, paths, keys, and values in prose. Never put multi-line samples in inline code. Code and log output are never edited for style.
- **Bold.** For UI labels (**Settings > Tokens**), and for a flag, setting, or key term the first time it's defined. Not for general emphasis: rewrite the sentence instead.
- **Admonitions.** GitHub syntax in Markdown, chosen by level:
  - `> [!NOTE]` extra context, not required reading;
  - `> [!TIP]` a shortcut or good practice;
  - `> [!IMPORTANT]` must read before proceeding;
  - `> [!WARNING]` causes problems if ignored;
  - `> [!CAUTION]` risk of data loss or an irreversible action.

  Use them for things that really matter. Don't restate the paragraph above in a callout, and never cut a warning or prerequisite for brevity.
- **Emoji.** None by default. If the repo's existing docs use them, follow that, but never one per bullet or heading.
- **Sections to omit from a README.** License, Contributing, Changelog, Code of conduct: these belong in their own files. If the user asks for one, write the standalone file (`CONTRIBUTING.md`) instead.
- **Lead with the task.** Open with what it is and does in one or two sentences, then how to run it, configure it, use it, and what goes wrong. Background and history go last, if at all.
- **Tone.** Present tense for facts ("Returns 404 if the payout doesn't exist"), imperative for steps ("Run `./mvnw test`"). Short, plain sentences, like a senior engineer explaining to a peer.

## Match the destination

- **README, GitHub/GitLab wiki, docs folder:** GitHub Flavored Markdown with admonitions as above.
- **Confluence:** structure that pastes cleanly into the editor (headings, lists, tables, code blocks). Map admonitions to Confluence panels: Info for NOTE, Tip for TIP, Note for IMPORTANT, Warning for WARNING and CAUTION. Produce Confluence wiki markup or storage format only if the user asks.
- **PR descriptions:** what changed and why, how it was tested, anything reviewers or deployers must know (migrations, flags, config). See the template.
- **Commit messages:** follow the repo's convention (check `git log`, e.g. Conventional Commits). Imperative subject under ~72 characters, body that explains why.
- **Changelogs and release notes:** user-visible changes grouped by kind, written from the reader's side ("Refunds now return 501 instead of 500").

Wikipedia flags a specific tell in change descriptions: *"Refined and enhanced X, ensuring clarity and consistency while preserving Y."* Words like *enhanced, refined, streamlined, ensured, improved clarity, preserved, robust* say nothing. Say what changed: "Rename `fullName` to `name` in the payout API and add a migration."

## Check before handing over

Do this as a separate pass after the doc is written: reread the actual file (and the source files you're checking it against), not your memory of what you meant to write. Read it through once for each of these:

1. **Accuracy against the source.** Every command, path, key, env var, endpoint, port, version, and default matches the repo or the user's input. Nothing invented, nothing stubbed shown as working. Every TODO is listed for the user.
2. **Completeness for the reader.** Could a new team member run, configure, and use it from this doc alone? Are prerequisites, required settings (like a password with no default), and known gaps stated? For an explanation or design doc, does it cover deploys and rollback, failure behaviour, security, and performance where they apply?
3. **Grammar and spelling.** Typos, agreement, tense, missing words, consistent US or UK spelling matching the repo. Identifiers spelled exactly as in the code.
4. **Clarity and structure.** Headings make sections findable; steps are in order; each sentence says one thing; every "it" and "this" has a clear referent. Rewrite anything you had to read twice.
5. **Format.** Code blocks have language tags; no broken links or leftover placeholders; admonitions mark real warnings only; no empty or filler sections.
6. **AI tells.** Scan last, because edits bring them back: em or en dashes, the vocabulary and filler words above, puffery, trailing *-ing* commentary, "not X but Y", lists of three that exist for rhythm, chat leakage, *actually/really/basically*, clichés, slogan fragments, rhetorical questions, and synonym cycling for one concept. Repeated technical terms, headings, tables, and labelled reference entries are expected in docs; don't "fix" those.

Don't over-correct. Formal vocabulary in general, correct formatting, and perfect grammar are not tells. The goal is a doc readers trust because it's accurate and easy to use.
