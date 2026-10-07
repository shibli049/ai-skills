# ai-skills

Skills for AI coding assistants (Claude Code, GitHub Copilot, and similar tools).

A skill is a packaged instruction set — frontmatter with a `name` and `description` that tells the assistant when to use it, plus a body of detailed guidance that only loads into context when the skill actually triggers.

This repo is also a **plugin marketplace** for both Claude Code and GitHub Copilot CLI, so the skills here can be installed with one command instead of a manual copy.

## Skills

### [spring-boot-service](plugins/shibli049/skills/spring-boot-service/SKILL.md)

Engineering standards for writing, extending, refactoring, testing, securing, and reviewing Java Spring Boot microservices: TDD, DDD, clean code, meaningful test coverage, performance, security basics, and avoiding over-engineering.

Use it for any Java or Spring Boot work — new features, bug fixes, refactors, code review, test writing, or service scaffolding — even when the request doesn't explicitly say "best practices" or "standards."

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
.claude-plugin/marketplace.json   Claude Code marketplace manifest
.github/plugin/marketplace.json   GitHub Copilot CLI marketplace manifest
plugins/shibli049/
  .claude-plugin/plugin.json      Claude Code plugin manifest
  plugin.json                     Copilot CLI plugin manifest
  skills/<skill-name>/SKILL.md    the actual skills
```

Adding a new skill means dropping another `skills/<name>/SKILL.md` under `plugins/shibli049/` — no manifest changes needed.

## License

MIT — see [LICENSE](LICENSE).
