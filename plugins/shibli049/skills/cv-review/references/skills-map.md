# Skills coverage map for backend-leaning engineers

Use this to spot gaps relative to the **target role**, not as a checklist everyone must fill. A focused, honest skills section beats an exhaustive one. Classify each gap as:

- **Missing but likely has** — common for their stack/experience; ask or suggest adding if true.
- **Present but buried** — mentioned in a bullet only, or under an odd name; surface it.
- **Gap worth closing** — expected for the target level/market and absent; suggest learning or a small project, not adding to the CV.

## Grouping for the skills section

Group into 5–7 lines, most relevant first, e.g.:

- **Languages**: Java (17/21), Kotlin, SQL, TypeScript
- **Frameworks**: Spring Boot, Spring Data JPA/Hibernate, Spring Security, Angular/React
- **Data**: PostgreSQL, Redis, Kafka / Azure Service Bus, Elasticsearch
- **Cloud & infra**: Azure (AKS, App Service, Key Vault), Docker, Kubernetes, Terraform, Helm/Kustomize
- **Practices**: Microservices, DDD, event-driven architecture, TDD, CI/CD (GitHub Actions/Azure DevOps), observability (OpenTelemetry, Prometheus, Grafana, App Insights)
- **Frontend (working knowledge)**: Angular, React, HTML/CSS

Don't put skill levels as bars. "Working knowledge" or ordering by strength is enough; it also keeps frontend claims honest.

## Expected areas by target role

### Senior backend engineer
Core language depth (concurrency, JVM tuning or equivalent), framework (Spring Boot etc.), relational DB design and query tuning, caching, messaging/event-driven, API design (REST, OpenAPI; gRPC/GraphQL a plus), testing strategy (unit/integration/contract, Testcontainers), containers + Kubernetes, one cloud in depth, CI/CD, observability, security basics (OAuth2/OIDC, secrets), production on-call/incident experience.

### Staff / principal engineer
All of the above plus: cross-team technical direction, system design at scale, reliability engineering (SLOs, capacity planning), migration strategy, platform/paved-road work, technical writing (RFCs/ADRs), mentoring at scale, cost awareness.

### Software / solution architect
Architecture styles and trade-offs (modular monolith vs microservices, event sourcing, CQRS), integration patterns, cloud architecture (well-architected frameworks), non-functional requirements, security/compliance (GDPR, ISO 27001 awareness), stakeholder communication, documentation (C4, ADRs), governance, often a cloud architect certification (Azure Solutions Architect Expert AZ-305, AWS SA Pro).

### Full-stack
Backend core plus a modern SPA framework in real depth (state management, testing, accessibility, performance), TypeScript, build tooling, CSS. If the frontend is light, recommend positioning as "backend-focused with full-stack experience" rather than claiming full-stack equally.

## Currently in-demand signals (verify against the job ad; trends shift)

Kubernetes, Terraform/IaC, event-driven (Kafka), observability (OpenTelemetry), cloud cost awareness, security (OAuth2/OIDC, supply-chain), Java 21 / virtual threads, Spring Boot 3, Kotlin, Go, platform engineering, AI/LLM integration in backend services (RAG, calling LLM APIs) — the last is increasingly asked even for non-ML roles; worth mentioning if the user has any real exposure.
