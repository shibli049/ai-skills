# Writing experience bullets that work for all three readers

## The shape

**Strong verb + what you built/changed + with what (tech) + scale/scope + result (number or concrete outcome).**

Variations: XYZ ("Accomplished X as measured by Y by doing Z"), CAR (Challenge–Action–Result). Don't force a formula on every line; aim for most bullets to carry *scope* and *outcome*.

## Weak → strong patterns

| Weak pattern | Problem | Better |
|---|---|---|
| "Responsible for developing microservices" | Duty, not achievement | "Built 6 Spring Boot services for order processing on AKS, handling ~[N] orders/day" |
| "Worked with Kafka, Redis, PostgreSQL" | Tech list, no story | "Cut checkout p95 latency from [X] to [Y] ms by adding a Redis read-through cache in front of PostgreSQL" |
| "Helped migrate to the cloud" | Vague role | "Led migration of [N] services from on-prem to Azure using Terraform; zero-downtime cutover" |
| "Improved performance" | No number | "Reduced batch run from 4 h to 25 min by replacing N+1 JPA queries with projections and batch fetching" |
| "Participated in code reviews" | Expected, low signal | "Introduced review guidelines and ArchUnit checks; reduced production incidents from [X]/quarter to [Y]" |
| "Used Angular to build UI" | Frontend undersold or oversold | "Built internal admin UI in Angular for [who], replacing manual SQL support tasks (~[N] h/week saved)" |

## Backend signal words that hiring managers look for

Throughput, latency (p95/p99), availability/SLO, incidents/MTTR, cost (cloud spend), data volume, number of services/teams/consumers, migration without downtime, idempotency/consistency, observability, security/compliance, release frequency, test coverage only if tied to outcome (e.g. fewer regressions).

## Verbs by level

- Mid: built, implemented, optimised, automated, integrated, fixed.
- Senior: designed, led, owned, drove, migrated, introduced, mentored, reduced, scaled.
- Staff/architect: defined, set direction, standardised (across N teams), influenced, de-risked, aligned stakeholders, authored ADRs/RFCs, established platform/paved road.

## Other rules

- 3–6 bullets for recent roles, 1–3 for older ones. Most recent and most relevant gets the most space.
- Past tense for past roles, present tense for current role (be consistent).
- One "Tech:" line per role is fine for ATS; it doesn't replace in-context mentions.
- Avoid "I", buzzwords ("synergy", "rockstar", "passionate"), and unexplained internal names (project code names, internal tool names) — translate to what it is.
- Metrics: real or approximate ("~", "over") is fine; invented is not. If the user doesn't track numbers, suggest proxies: users served, services owned, team size, time saved, frequency (daily deploys), before/after states.
