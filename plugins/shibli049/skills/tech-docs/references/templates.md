# Doc-type templates

Scaffolds for common doc types. They are starting points: delete any section with nothing real to say, and fill every remaining section from the repo or the user's input, never from what a typical project would have.

## Contents

1. README
2. ADR (architecture decision record)
3. Guide or runbook
4. API reference
5. PR description
6. Commit message
7. Changelog or release notes entry

---

## 1. README

````markdown
# Project name

One or two sentences: what it does and who uses it. Specific, no tagline puffery.

<!-- Badges only for things that exist: a CI badge needs a real workflow file, a license badge needs a LICENSE file. Use flat-square style. Omit the line entirely if none apply. -->
[![Build](https://img.shields.io/github/actions/workflow/status/<org>/<repo>/<workflow>.yml?style=flat-square)](https://github.com/<org>/<repo>/actions)

<!-- ToC only for long READMEs, and only if the user wants one: one link per line, inner levels indented -->
## Contents

- [Overview](#overview)
- [Run it locally](#run-it-locally)
  - [Prerequisites](#prerequisites)
  - [Steps](#steps)
- [Configuration](#configuration)
- [Usage or API](#usage-or-api)
- [Development](#development)
- [Known gaps](#known-gaps)

> [!NOTE]
> Context the reader needs before anything else (for example, "Refunds are not implemented yet"). Omit if there's nothing.

## Overview

What the system does at a high level and how the main parts fit together. Add a diagram only if one exists or the structure is non-obvious.

## Run it locally

### Prerequisites

- Runtime and version from the build file (for example, Java 21)
- Services it needs (for example, PostgreSQL)

### Steps

1. Set the required settings.

   ```bash
   export DB_PASSWORD=<password>
   ```

2. Start it.

   ```bash
   ./mvnw spring-boot:run
   ```

Say what success looks like (the port it listens on, a health URL that exists).

## Configuration

| Setting | Env var | Default | Meaning |
|---|---|---|---|
| `server.port` | none | `8085` | HTTP port |

## Usage or API

Real, runnable examples. Link to the API reference if there is one.

## Development

```bash
./mvnw test        # only if tests exist
```

> [!TIP]
> A real gotcha from the code or config, if there is one.

## Known gaps

What's stubbed, missing, or not implemented yet. Omit if nothing.
````

Do not add License, Contributing, Changelog, or Code of conduct sections; those are separate files.

---

## 2. ADR (architecture decision record)

```markdown
# ADR-NNN: Decision in a few words

| | |
|---|---|
| **Status** | Proposed / Accepted / Deprecated / Superseded by ADR-NNN |
| **Date** | YYYY-MM-DD |
| **Deciders** | Names, only if the user gave them |

## Context

The situation and constraints that forced a decision. Facts, numbers, and links to incidents or tickets if they exist.

## Options considered

Each option in a sentence or two, with its real trade-off. Only options that were actually considered.

## Decision

What was decided, specifically enough that someone could check whether the code follows it.

## Consequences

What gets easier, what gets harder, and what the team now has to do (migrations, monitoring, follow-up work). Include the downsides.
```

---

## 3. Guide or runbook

````markdown
# Task in a few words (for example, "Restart a stuck payout worker")

One sentence on what this covers and when to use it.

## When to use this

The symptom or trigger, concretely (for example, "payouts stuck in PENDING for more than 30 minutes").

## Before you start

- Access or tools needed
- Approvals needed

> [!CAUTION]
> Any irreversible or approval-gated action, stated plainly.

## Steps

1. What to do.

   ```bash
   command exactly as given
   ```

2. How to check it worked.

## If it doesn't work

| Symptom | Likely cause | What to do |
|---|---|---|
| ... | ... | ... |

Who to escalate to and how, if the user gave it.

## Open items

- TODO: anything the user still needs to confirm. Remove this section once filled.
````

---

## 4. API reference

````markdown
# Payout API

Base path: `/api/v1/payouts`
Authentication: state what the code does, including "none" if there is none.

## GET /api/v1/payouts/{id}

Returns one payout.

**Path parameters**

| Name | Type | Description |
|---|---|---|
| `id` | long | Payout id |

**Response**

```json
{ "id": 1, "merchantId": "m_123", "amountMinor": 2500, "currency": "USD", "status": "PENDING" }
```

**Status codes**

| Code | Meaning |
|---|---|
| `200` | Found |
````

Field names and types come from the entity or DTO. Only list status codes the code actually returns; mark inferred ones as inferred.

---

## 5. PR description

```markdown
## What

One or two sentences on the change, in terms a reviewer can check against the diff.

## Why

The problem or ticket. Link it if the user gave one.

## How

Only the non-obvious parts of the approach. Skip if the diff speaks for itself.

## Testing

What was actually run (tests added, manual checks). Don't claim tests that weren't run.

## Deploy notes

Migrations, feature flags, config or env changes, ordering constraints. Omit if none.
```

No "This PR enhances/streamlines/improves..." openers, and no list of every file touched.

---

## 6. Commit message

Follow the repo's convention first (check `git log`). Default shape:

```text
Short imperative subject, under ~72 characters

Why the change was needed and anything a future reader of `git blame`
would want to know. Wrap at ~72 characters. Skip the body for trivial
changes.
```

Examples: "Return 501 from refund endpoint until ledger API is ready", not "Enhanced refund handling for improved robustness".

---

## 7. Changelog or release notes entry

```markdown
## [0.4.0] - YYYY-MM-DD

### Added
- `GET /api/v1/payouts?merchantId=` lists payouts for a merchant.

### Changed
- `PAYOUT_BATCH_SIZE` now defaults to 200.

### Fixed
- A missing payout id returns 404 instead of 500.
```

Write each line from the user's side: what they can now do or what behaves differently. Use the version and date from the repo or the user; leave `TODO` if unknown.
