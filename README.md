# ai-skills

Skills for AI coding assistants (Claude Code, GitHub Copilot, and similar tools).

A skill is a packaged instruction set — frontmatter with a `name` and `description` that tells the assistant when to use it, plus a body of detailed guidance that only loads into context when the skill actually triggers.

This repo is also a **plugin marketplace** for both Claude Code and GitHub Copilot CLI, so the skills here can be installed with one command instead of a manual copy.

## Skills

### [spring-boot-service](plugins/shibli049/skills/spring-boot-service/SKILL.md)

Engineering standards for writing, extending, refactoring, testing, securing, and reviewing Java Spring Boot microservices: TDD, DDD, clean code, meaningful test coverage, performance, security basics, and avoiding over-engineering.

Use it for any Java or Spring Boot work — new features, bug fixes, refactors, code review, test writing, or service scaffolding — even when the request doesn't explicitly say "best practices" or "standards."

### [humanize-writing](plugins/shibli049/skills/humanize-writing/SKILL.md)

Writes and rewrites everyday prose so it reads like a person wrote it: emails, Slack and Teams messages (including detailed technical explanations), LinkedIn or blog posts, cover letters, and similar. It avoids every pattern on Wikipedia's [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) page, plus a few stock phrases found in review: em dashes, puffery, words like *delve* and *crucial*, "not just X but Y", "Good question" openers, and so on. It keeps text concise unless asked for detail, never adds details the user didn't give, and rereads each draft for grammar, clarity, accuracy, and AI tells before handing it over.

### [tech-docs](plugins/shibli049/skills/tech-docs/SKILL.md)

Writes and updates technical documentation: READMEs, Confluence pages, wikis, runbooks, ADRs, API references, PR descriptions, commit messages, and changelogs. It reads the project before writing and documents only what the code contains, with no invented commands, config, or features. It applies the same AI-writing rules as `humanize-writing`, but with flexible formatting (headings, tables, admonitions) for reference material. Templates for each doc type are in `references/templates.md`.

### [cv-review](plugins/shibli049/skills/cv-review/SKILL.md)

Reviews a software engineer's CV or resume the way a tech recruiter, a hiring manager, and an ATS would, then writes a scored report with concrete rewrites. It covers missing skills and keywords, weak bullets, seniority signals, market conventions (Sweden/EU, UK, US), fit against a pasted job ad, consistency with LinkedIn and GitHub, and comparisons between CV versions. It is tuned for backend engineers but also handles frontend, support, and lead roles, and consultancy profiles.

When the CV is a PDF or DOCX on disk, it runs `scripts/ats_check.py` to show what an ATS actually extracts. That script needs Python 3 with `pdfplumber` and `python-docx`, plus poppler (`pdftotext`, `pdffonts`) for the font checks. Without them the review still runs and notes that the parse test was skipped.

## Installing

### Option A: as a plugin marketplace (recommended)

**Claude Code:**

```
/plugin marketplace add shibli049/ai-skills
/plugin install shibli049@ai-skills
```

**GitHub Copilot CLI:**

```
/plugin marketplace add shibli049/ai-skills
/plugin install shibli049@ai-skills
```

Installing this way namespaces every skill under the plugin name (e.g. `shibli049:spring-boot-service`), so it won't collide with a same-named skill from another source, and future updates are a `git push` + a marketplace refresh instead of re-copying files by hand.

#### Updating an installed plugin

Refresh the marketplace catalog first, then update the plugin. Run these from your shell.

**Claude Code:**

```sh
claude plugin marketplace update ai-skills
claude plugin update shibli049@ai-skills
```

Restart Claude Code to load the new version.

**GitHub Copilot CLI:**

```sh
copilot plugin marketplace update ai-skills
copilot plugin update shibli049@ai-skills
```

Copilot can also update every installed plugin at once with `copilot plugin update --all`. Check which version is installed with `claude plugin list` or `copilot plugin list`.

### Option B: manual copy

Copy the skill's directory straight into the assistant's user-level skills folder:

| Assistant | Skills folder |
|---|---|
| Claude Code | `~/.claude/skills/` |
| GitHub Copilot CLI | `~/.copilot/skills/` |

```sh
cp -r plugins/shibli049/skills/spring-boot-service ~/.claude/skills/
```

The assistant picks it up automatically on the next session — no further registration needed. Don't combine this with Option A for the same skill; loading it both ways just duplicates it in the assistant's skill listing.

## Repo layout

```
.
├── .claude-plugin/marketplace.json      Claude Code marketplace manifest
├── .github/plugin/marketplace.json      GitHub Copilot CLI marketplace manifest
├── plugins/shibli049/
│   ├── .claude-plugin/plugin.json       Claude Code plugin manifest
│   ├── plugin.json                      Copilot CLI plugin manifest
│   └── skills/<skill-name>/             the actual skills (SKILL.md, references/, optional scripts/)
└── verification/scripts/                helper scripts for testing skill output (not part of any skill)
```

Skills contain instructions (`SKILL.md` plus optional `references/*.md`). A skill may bundle a script under its own `scripts/` folder only when the skill runs it as part of its job, like `cv-review/scripts/ats_check.py`. Tooling used to check a skill's output lives in `verification/scripts/`. For example, `check_ai_patterns.py` flags AI-writing tells in a draft:

```sh
python verification/scripts/check_ai_patterns.py draft.md
python verification/scripts/check_ai_patterns.py --doc README.md   # relaxed formatting checks for docs
```

Adding a new skill means dropping another `skills/<name>/SKILL.md` under `plugins/shibli049/` — no manifest changes needed.

## TODO

- Split the single `shibli049` plugin into individual plugins if the skills grow, so people can install only the ones they need. Installing a plugin currently installs every skill in it. A likely grouping: `spring-boot` (`spring-boot-service`), `writing` (`humanize-writing` and `tech-docs`, which share the AI-writing rules), and `cv-review`. Each plugin needs its own folder, manifests, and entries in both `marketplace.json` files. Skill names would lose the `shibli049:` namespace, and existing installs would need to reinstall.

## License

MIT — see [LICENSE](LICENSE).
