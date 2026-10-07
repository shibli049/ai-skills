# ai-skills

Skills for AI coding assistants (Claude Code, GitHub Copilot, and similar tools).

A skill is a packaged instruction set — frontmatter with a `name` and `description` that tells the assistant when to use it, plus a body of detailed guidance that only loads into context when the skill actually triggers.

## Skills

### [spring-boot-service](spring-boot-service/SKILL.md)

Engineering standards for writing, extending, refactoring, testing, securing, and reviewing Java Spring Boot microservices: TDD, DDD, clean code, meaningful test coverage, performance, security basics, and avoiding over-engineering.

Use it for any Java or Spring Boot work — new features, bug fixes, refactors, code review, test writing, or service scaffolding — even when the request doesn't explicitly say "best practices" or "standards."

## Installing a skill

Copy the skill's directory into the assistant's user-level skills folder:

| Assistant | Skills folder |
|---|---|
| Claude Code | `~/.claude/skills/` |
| GitHub Copilot CLI | `~/.copilot/skills/` |

```sh
cp -r spring-boot-service ~/.claude/skills/
```

The assistant picks it up automatically on the next session — no further registration needed.

## License

MIT — see [LICENSE](LICENSE).
