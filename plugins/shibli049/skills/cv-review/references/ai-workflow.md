# AI-assisted development on the CV

By 2026 most engineering job ads, and most hiring managers, assume engineers work with AI coding assistants. A CV that says nothing about it reads as either out of date or silent on something the reader wants to ask about. A CV that only lists tool names reads as hype. What the reader wants is evidence that the person uses these tools well: they ship faster without lowering quality, and they know where the tools fail.

Keep two things apart, because job ads and CVs often blur them:

- **AI-assisted development**: using assistants and agents to build software (Claude Code, OpenAI Codex, GitHub Copilot, Cursor, etc.). This is about the person's workflow. It is relevant to almost every engineering role now.
- **Building AI features**: calling LLM APIs from a service, RAG, tool/function calling, building MCP servers or agents as part of the product, evals, guardrails. This is product work and belongs in experience bullets and the skills map (see `skills-map.md`). It is not ML engineering; don't let the CV imply model training if the person only integrated APIs.

A person can have either, both or neither. Review each separately.

## What to look for

| Signal | Weak (tool list / hype) | Strong (evidence) |
|---|---|---|
| Tools | "ChatGPT, Copilot, AI tools" | "GitHub Copilot and Claude Code in daily work; Codex for background tasks on PRs" |
| Team workflow | "Used AI to speed up development" | "Set up Claude Code for the team: CLAUDE.md/AGENTS.md with our Spring Boot conventions, custom skills for test and migration patterns, hooks that run the linter and tests" |
| Context engineering | "Prompt engineering" | "Wrote repo instructions (copilot-instructions.md, AGENTS.md) and reusable skills/prompts so agents follow our architecture and testing rules" |
| Tool integration | — | "Built an internal MCP server exposing our service catalogue and runbooks to Claude Code and Copilot" |
| Quality and safety | — | "Defined review rules for AI-generated code (tests required, no secrets in prompts, licence checks); added AI code review on PRs as a first pass, humans approve" |
| Outcomes | "10x productivity with AI" | "Migrated [N] services from Java 11 to 21 in [X] weeks using agent-driven refactoring with test gates; previous estimate was [Y]" |
| Adoption / governance | — | "Led Copilot rollout to [N] engineers: pilot, guidelines, measured PR cycle time before/after" |
| Public work | — | "Author of open-source agent skills / Claude Code plugin / MCP server (link), [N] stars or users" |

Strong bullets name the tool, say what the person set up or changed (not just "used"), and give an outcome or a guardrail. Unverifiable productivity multipliers ("5x faster") hurt more than they help; ask for a real before/after or drop the number.

## Terms worth knowing

So you can recognise what the person did and suggest accurate wording. The landscape changes fast, so prefer the job ad's exact terms when they differ.

- **Assistants and agents**: GitHub Copilot (IDE completions, chat, coding agent, code review, CLI), Claude Code (terminal/IDE agent), OpenAI Codex (CLI and cloud agent), Cursor, Windsurf, JetBrains AI Assistant / Junie, Gemini CLI, Amazon Q Developer.
- **Configuration and context**: `CLAUDE.md`, `AGENTS.md`, `.github/copilot-instructions.md`, Cursor rules; agent skills (packaged instructions plus scripts that load on demand); custom slash commands, subagents, hooks; plugins and plugin marketplaces.
- **Integration**: Model Context Protocol (MCP) servers and clients; tool calling; agents running in CI (e.g. Copilot coding agent or Claude Code in GitHub Actions).
- **Practices**: plan/spec-first agentic work, test-driven guardrails for agents, parallel agents with git worktrees, AI-assisted code review, evals for prompts and skills, keeping secrets and customer data out of prompts.

ATS and recruiters match literal strings. Write "GitHub Copilot", not "Copilot" alone (it is easily confused with Microsoft 365 Copilot). Write "Model Context Protocol (MCP)" once in full. "AI-assisted development" or "agentic coding" works as a group label.

## Where it goes on the CV

- **Skills section**: one line, e.g. `AI-assisted development: Claude Code (skills, MCP, hooks), GitHub Copilot, OpenAI Codex`. Don't scatter AI tool names across every role.
- **Experience bullets**: the evidence. One strong bullet in the current role is worth more than a line in every role.
- **Selected projects / open source**: published skills, plugins, MCP servers, or prompt/eval tooling, with links. These are checkable and stand out.
- **Summary**: only if it is central to the target role (developer productivity, platform, AI tooling, or the ad stresses it). Otherwise keep the summary on level, domain and stack.

## Calibrate by level

- **Mid**: uses assistants effectively and critically in their own work; can say what they verify.
- **Senior**: shapes the team's workflow: repo instructions, shared skills/prompts, review rules, CI checks for agent output; mentors others on safe use.
- **Staff / architect / lead**: adoption and governance across teams: tool selection, policy (data handling, IP/licensing, security), measurement of real impact, platform work such as shared MCP servers or paved-road agent setups, cost.

## When the CV has nothing on it

Don't add anything on your own. Ask the user, in one line, whether and how they use AI assistants at work (which tools, anything they set up for the team, anything published). Most engineers do, and the bullet is usually easy to write once you know. If they don't use them and the target role or ad expects it, list it as a "gap worth closing" with a small, concrete way to get evidence (e.g. set up an agent workflow for a side project and publish the skills or config on GitHub).

Some employers restrict AI tools (regulated finance, defence, public sector, some consultancy clients). If the user's background or target is like that, frame experience around governance and safe use, and don't push it into the summary.

## Red flags to call out

- AI buzzword stuffing: "AI-driven", "leveraging cutting-edge AI", "prompt engineering expert" with no evidence behind them.
- Claims of AI or ML expertise based only on using ChatGPT.
- Productivity multipliers with no baseline.
- Wording that implies the AI did the work and the person didn't own the result.
- The CV text itself reading as AI-generated (stock phrases, puffery, uniform bullet rhythm). Recruiters notice, and it undercuts any claim of using AI well. Point out the specific phrases in the rewrites.
