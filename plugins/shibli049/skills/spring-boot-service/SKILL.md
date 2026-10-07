---
name: "spring-boot-service"
description: "Engineering standards for writing, extending, refactoring, testing, securing and reviewing Java Spring Boot microservices — TDD, DDD, clean code, meaningful test coverage, performance, security basics, and avoiding over-engineering. Use this for any Java or Spring Boot work: new features, bug fixes, refactors, code review, test writing, or service scaffolding — even when the user doesn't say \"best practices\" or \"standards\" explicitly, just describes a Java/Spring task."
---

# Spring Boot service engineering

The goal is code a senior engineer would approve without comment: behaviour proven by tests that were written first, a domain model that speaks the business language, and no more structure than the problem needs. Every rule below exists to serve that; when a rule and the goal disagree, follow the goal and say why.

## 1. Orient before writing

Read the project first, because fitting in matters more than any default here.

- Build file (`pom.xml`, `build.gradle[.kts]`): Java version, Spring Boot version, build tool, which starters and test libraries are present. Use only language features the configured Java version supports (records need 16+, sealed types and pattern matching for switch need 17/21, virtual threads need 21). Spring Boot 3+ means `jakarta.*`, not `javax.*`.
- Package layout, naming, how existing features are sliced, how errors are returned, how tests are named and set up, which database migration tool is used, whether Lombok / MapStruct / AssertJ / Testcontainers are in use.
- Quality gates already configured: JaCoCo thresholds, PIT, SonarQube, Checkstyle, SpotBugs, PMD, ArchUnit. The change has to pass them.
- Run the build with the project's wrapper (`./mvnw`, `./gradlew`) if present.

**Existing project:** match its architecture and conventions, even where you would have chosen differently. Consistency is worth more than a locally better pattern. If a convention is actively harmful (for example it causes a bug in the code you are touching), fix only what the task needs and mention the rest instead of refactoring unasked.

**New project or new service:** use the pragmatic hexagonal layout in section 3.

Do not add a dependency for something the project or the JDK already does.

## 2. Work test-first

TDD is the working method, not a coverage chore. Writing the test first forces the design question "how will this be used and what should it do?" before any structure exists, which is the cheapest guard against over-engineering.

1. **Red.** Write one small test for the next piece of behaviour. Run it and see it fail for the right reason (an assertion, not a compile error you did not expect).
2. **Green.** Write the simplest code that passes. Resist adding anything the test does not demand.
3. **Refactor.** With tests green, remove duplication and improve names. Run the tests again.

Start from the inside: domain behaviour first (plain unit tests, no Spring), then the use case, then adapters. For a bug, first write a test that reproduces it and fails, then fix it. For untested legacy code, pin current behaviour with a characterization test before changing it.

Actually run the tests when a build tool is available, and report the real result. If you cannot run them, say so plainly rather than implying they pass.

### What makes a test meaningful

A test earns its place if it would fail when the behaviour breaks and would keep passing through a refactor that preserves behaviour.

- Test behaviour through the public API of the unit, not its implementation. Assert on returned values, resulting state, published events and persisted data. Use `verify(...)` only when the interaction itself is the outcome (a message was sent, an email was requested).
- Name tests as sentences about behaviour: `rejectsOrderWithoutItems`, `marksInvoiceOverdue_whenPaymentIsLate`. Follow the project's existing naming style if it has one.
- Group related behaviour with `@Nested` classes and use `@Tag` (`fast`, `integration`) so slow suites (Testcontainers, `@SpringBootTest`) can be filtered out of the everyday run. Reach for `@DisplayName` only when the method name cannot say it cleanly.
- Arrange / act / assert, one behaviour per test, with the data that matters visible in the test. Hide irrelevant setup behind small builders or factory methods (`anOrder().withItems(3).build()`).
- Cover the edges where bugs live: boundaries (0, 1, max, exactly-at-threshold), empty and null inputs, duplicates, invalid state transitions, time zones and clock boundaries, concurrent updates where relevant. Use `@ParameterizedTest` when the same rule has many inputs.
- Test the unhappy paths: each domain rule that rejects something gets a test that proves the rejection and its reason.
- Inject `Clock` (and id / random sources) so tests are deterministic. No `Thread.sleep`; use Awaitility for asynchronous outcomes.
- Prefer AssertJ. Assert the specific thing (`assertThat(result.status()).isEqualTo(SHIPPED)`), not `isNotNull()`.
- When one behaviour genuinely produces several independent facts worth checking (several fields of a single result), group them with AssertJ's `assertSoftly` / `SoftAssertions` so every mismatch is reported in one run instead of stopping at the first failure. This is not a substitute for one-behaviour-per-test — reach for it only when a single behaviour's outcome has several parts, not to bundle unrelated assertions together.

Tests not worth writing: getters and setters, records' generated methods, framework behaviour (that `@Autowired` works), tests that mirror the implementation line by line with mocks, and tests whose only assertion is that no exception was thrown when there is real output to check.

### Meaningful coverage

Coverage is a tool for finding behaviour nobody has tested, not a number to hit. A line that was executed by a test with no real assertion is covered and unprotected, so judge coverage by what would be caught, not by what was run.

- Aim for every business rule, every branch of a decision, and every error path in domain and application code to be exercised by a test that asserts the outcome. Look at branch coverage rather than line coverage: an `if` with only its true side tested shows as a covered line.
- Apply the mutation question to each piece of logic you write: if this condition were flipped, this boundary moved by one, or this line deleted, would a test fail? If not, the test is missing or too weak. Where PIT is configured, run it on the changed classes and treat surviving mutants in business logic as gaps.
- When the coverage report (JaCoCo or the project's tool) shows uncovered code in domain or application classes, ask which it is: a missing test, or dead code to delete. Do not paper over it either way.
- Spend effort where the risk is. Rules, calculations, state transitions, mappings between models, queries with conditions, retry and failure handling deserve thorough tests. Configuration classes, plain DTOs and records, generated code and the `main` class do not need tests written for their own sake.
- Never raise the number artificially: no assertion-free tests, no tests that call methods only to execute them, no reflection tricks to reach private code, no new coverage exclusions or lowered thresholds to get a build through. If a project gate cannot be met honestly within the task, say so and explain what is uncovered.
- In the final summary, state what is deliberately not covered and why, so the gap is a decision rather than an accident.

### Choosing the test level

Use the cheapest test that can actually catch the bug.

| What is under test | Test type |
|---|---|
| Domain rules, value objects, aggregates, pure logic | Plain JUnit, no Spring context, no mocks |
| Use case orchestration | JUnit with hand-written fakes or Mockito for the ports |
| Controller: mapping, validation, status codes, error body | `@WebMvcTest` (or `@WebFluxTest`) with the use case mocked |
| Repository queries, mappings, constraints, migrations | `@DataJpaTest` against real PostgreSQL via Testcontainers |
| Redis, messaging, outbound HTTP adapters | Testcontainers; WireMock or `MockRestServiceServer` for HTTP |
| Wiring and one or two critical end-to-end flows | `@SpringBootTest`, kept few |

Mock only what you own at an architectural boundary (ports, other services). Do not mock value objects, entities, or types you do not own such as `RestClient` internals or `EntityManager`; test against the real thing or a fake. H2 is not PostgreSQL: it hides dialect, locking, JSONB and constraint differences, so use Testcontainers for persistence tests unless the project has deliberately chosen otherwise. Share one container across the suite (static container or `@ServiceConnection`) to keep the suite fast.

As of Spring Boot 3.4, stub or spy a bean in a test context with `@MockitoBean` / `@MockitoSpyBean`, not `@MockBean` / `@SpyBean` — the latter are deprecated and gone entirely in Spring Boot 4. Check the project's Boot version before reaching for either; an older project may still be on the deprecated pair deliberately.

## 3. Structure and domain model

### Layout for new services

When there is no project yet, generate the skeleton instead of hand-rolling boilerplate — `curl https://start.spring.io/starter.zip -d bootVersion=<version> -d javaVersion=<jdk> -d dependencies=<starters, comma-separated> -d packageName=<base package> -d type=<maven-project|gradle-project-kotlin> -o starter.zip && unzip starter.zip`. Keep it one module. The multi-module `api` / `service` / `persistence` / `common` split some scaffolding guides reach for by default is itself a premature abstraction for most services (section 8): it buys you nothing until separate deployability or reuse by another service is a real requirement, and until then it only adds POMs and inter-module wiring to maintain. Start flat with the package-by-feature layout below and split into modules only when that boundary actually appears.

Give the service a way to run its real dependencies locally: a `docker-compose.yml` with the database (and Redis, a broker, and so on, if the service needs them) is the standard shortcut. A hardcoded throwaway password in that file is fine — it is a local container nobody outside the machine can reach, not a production credential — but keep it out of `application.yml`'s defaults, which would also apply when the service runs for real. Wire it through a dev-only Spring profile instead (see the Configuration rule in section 4), so there is no path from the convenience password to a production environment.

Package by feature (bounded context or aggregate) first, then by role. This keeps a change in one place and makes the service's capabilities visible from the top-level packages.

```
com.acme.shop
  order/
    domain/        Order, OrderId, OrderPlaced, OrderRepository (port)
    application/   PlaceOrderUseCase, command and result types
    adapter/
      in/web/      OrderController, request/response DTOs
      in/messaging/
      out/persistence/  JPA entity or mapping, repository implementation
      out/client/
  shared/          genuinely cross-cutting types only
```

Dependencies point inward: adapters depend on application, application depends on domain, domain depends on nothing in Spring or the infrastructure. This is what lets domain rules be tested in milliseconds. Where ArchUnit is available — or worth adding to a new service — write one test that enforces this mechanically (the domain package must not depend on Spring, web, or persistence types), so the layering rule can't quietly rot as the codebase grows instead of just living in this description.

**Pragmatic** means the following shortcuts are intended, not lapses:

- Add a port (interface) only at a real boundary: persistence, messaging, another service, the clock. Do not create an interface for a class with one implementation and no boundary, and do not add `Impl` classes.
- A simple feature that is only CRUD may be a controller, a service and a Spring Data repository. Do not wrap it in use cases, mappers and ports it does not need.
- JPA annotations on the domain entity are acceptable while the persistence shape matches the domain shape. Split into a separate persistence model only when they genuinely diverge.
- Spring Data repository interfaces may serve directly as the port when no translation is needed.

### Domain-driven design, applied tactically

- **Ubiquitous language.** Name classes, methods and tests with the words the business uses. If the user says "credit note", the code says `CreditNote`, not `RefundData`. Ask when a term is ambiguous.
- **Value objects** for concepts with rules or units: `OrderId`, `Money`, `EmailAddress`, `Quantity`. Make them immutable (records where the Java version allows), validate in the constructor so an invalid one cannot exist, and give them behaviour. This removes primitive obsession and whole classes of argument-order bugs. Do not wrap a primitive that has no rules and no risk of confusion.
- **Entities and aggregates.** Put behaviour and invariants on the aggregate (`order.addItem(product, quantity)`), not in a service that manipulates setters. No public setters for invariant-bearing state. Keep aggregates small; reference other aggregates by id; one transaction modifies one aggregate, and other aggregates follow through domain events.
- **Domain services** only for logic that genuinely spans aggregates and belongs to none.
- **Application services / use cases** orchestrate: load, call the domain, save, publish. They own the transaction and contain no business rules.
- **Domain events** named in the past tense (`OrderPlaced`) when something else needs to react.
- **Anti-corruption.** Translate external payloads and other services' models at the adapter. Never let a third party's DTO, a JPA entity, or an HTTP request type travel into the domain or out through the API.

Do not apply the full tactical toolkit to a feature with no rules. A lookup table does not need an aggregate.

## 4. Clean code rules

- **Imports, not fully qualified names.** Import every type and reference it by its simple name: `List<Order>`, never `java.util.List<com.acme.Order>`. This applies to annotations, exceptions, generics, static nested types and test code too. The only exception is a real simple-name clash within one file (for example `java.util.Date` and `java.sql.Date`): import the one used most and fully qualify the other. No wildcard imports unless the project already uses them. Static imports are fine for assertions, Mockito, and well-known constants where they read better. Before finishing, scan what you wrote for package-qualified type names (`java.`, `javax.`, `jakarta.`, `org.`, `com.`, and the project's own base package) appearing outside `import` and `package` lines, including inside query strings and annotations. When you touch a file that already contains fully qualified names, convert them in that file.
- **Names** reveal intent and use domain terms. No abbreviations that need decoding, no `data`, `info`, `manager`, `helper`, `util` as a substitute for a real concept.
- **Small, single-purpose methods** at one level of abstraction. Guard clauses instead of nested conditionals. If a method needs a comment to explain a block, extract the block and name it.
- **Constructor injection** with `final` fields; no field injection. A constructor with many dependencies is a signal the class does too much.
- **Immutability by default**: `final` fields, records for DTOs, commands and value objects, unmodifiable collections returned from the domain (`List.copyOf`).
- **No nulls across boundaries.** Return `Optional` for a single value that may be absent and empty collections instead of `null`. Do not use `Optional` for fields or parameters.
- **Errors.** Throw specific domain exceptions with meaningful messages; translate them to HTTP once, in a `@RestControllerAdvice`, preferably as RFC 9457 `ProblemDetail`. Never swallow an exception, never catch `Exception` to hide a failure, and do not use exceptions for ordinary control flow.
- **Comments** explain why, never what. No commented-out code, no TODOs without an owner.
- **Javadoc** on public API: controllers' public methods, published ports, and domain types other modules depend on. State the contract in the summary line — what it does, what it rejects, what it returns for the empty or absent case — rather than restating the method name. Skip it on private and package-private members and on anything the signature already says in full (a getter, a record's generated accessor).
- **Configuration** through `@ConfigurationProperties` (validated, typed, immutable) rather than scattered `@Value`. Vary configuration per environment with Spring profiles (`application-{profile}.yml`), not conditional logic in code. No secrets or environment-specific values in code.
- **Logging** via SLF4J with parameterized messages (`log.info("Order accepted orderId={}", id)`), at the right level, without personal data or secrets. Log an exception once, where it is handled.
- **API contracts.** Request and response DTOs are separate from domain and persistence types. Validate input with Bean Validation at the edge; enforce invariants in the domain. Use correct status codes, and page any collection that can grow.

### Code smells

A smell is a sign that a change will be harder or riskier than it should be. Do not introduce any of these in code you write, and remove them from the code you are changing when doing so is small and covered by tests. Smells elsewhere in the codebase are reported in the summary, not fixed unasked, because an unrequested refactor makes the change harder to review. Refactor only with tests green before and after, and keep refactoring separate from behaviour change.

| Smell | What to do instead |
|---|---|
| Long method, deep nesting, a method doing several things | Extract well-named methods; guard clauses; one level of abstraction |
| Large class or "god" service with many dependencies | Split by responsibility or by use case |
| Long parameter list, the same group of values passed around together (data clump) | Introduce a value object or command record |
| Primitive obsession (`String`, `long`, `Map<String, Object>` standing in for domain concepts) | Value object, enum or typed record |
| Anemic domain model: entities with only getters/setters, rules in services | Move the rule onto the entity or aggregate |
| Feature envy: a method mostly reads another object's data | Move the behaviour to the object that owns the data |
| Message chains (`a.getB().getC().doX()`) | Ask the nearest object to do the work |
| Duplicated logic | Extract once the duplication is real (same reason to change), not merely similar-looking |
| Boolean flag parameter that switches behaviour | Two methods with names that say what they do |
| Repeated `switch` / `if` chain on a type or status | Enum with behaviour, sealed types with pattern matching, or polymorphism |
| Magic numbers and strings | Named constant, enum, or configuration property |
| Mutable shared or static state, static utility classes holding business logic | Immutable values; logic on a domain type or an injected bean |
| Shotgun surgery: one change requires edits in many places | Bring what changes together into one module |
| Dead code, unused parameters, speculative generality | Delete it |
| Temporal coupling: methods that must be called in a particular order | Make the invalid order impossible (constructor, builder, single method) |
| Comments explaining confusing code | Make the code clear, then remove the comment |

Spring-specific smells to avoid: business logic in controllers or in `@Query`/SQL; controllers calling repositories directly when there are rules to enforce; returning JPA entities from the API; `@Transactional` on controllers or wrapped around remote calls; field injection and circular bean dependencies; catching `Exception` and returning a generic result; `@Autowired` `ApplicationContext` lookups in place of injection; one giant `@Configuration` or a shared "common" module that every feature depends on.

Smells in tests count too: several behaviours in one test, logic (loops, conditionals) in a test, tests that depend on execution order or shared mutable state, excessive mocking, and copy-pasted setup that hides what matters.

When the project has static analysis configured (SonarQube, Checkstyle, SpotBugs, PMD, ArchUnit), run it if possible and leave no new findings. Do not silence a finding with a suppression unless it is a real false positive, and say why in the suppression.

## 5. Data structures

Choose the structure from how the data is accessed, because the wrong one silently turns into an O(n^2) path or a correctness bug.

- Lookup by key: `Map` (`HashMap`; `EnumMap` for enum keys; `LinkedHashMap` when insertion order matters; `TreeMap` when you need ordering or range queries).
- Membership tests and uniqueness: `Set`, not `List.contains` in a loop. `EnumSet` for enum flags.
- Ordered sequence with index access: `ArrayList`. `LinkedList` is almost never right; for queue or stack use `ArrayDeque`.
- Priority or "next due": `PriorityQueue`. Time- or range-indexed data: `NavigableMap` / `TreeMap` (`floorEntry`, `subMap`).
- Shared across threads: `ConcurrentHashMap` with atomic `compute` / `merge`, not a synchronized wrapper plus check-then-act.
- Fixed set of states or types: `enum` or a sealed hierarchy instead of strings and integer codes.
- Money and exact decimals: `BigDecimal` (compare with `compareTo`), never `double`. Time: `Instant` for points in time, `Duration` for amounts, zone-aware types only at the edges.
- Group or index a list once (`Collectors.toMap`, `groupingBy`) instead of searching it repeatedly inside another loop.
- Use streams where they make the transformation clearer, a plain loop where they do not. Presize collections when the size is known and large. Avoid boxing in hot paths.

## 6. Performance

Write the obviously efficient version by default, and measure before doing anything clever. Readability wins unless a measurement says otherwise.

Things that are always worth getting right, because they are cheap up front and expensive in production:

- **No N+1 queries.** Associations are `LAZY` by default (set `@ManyToOne(fetch = LAZY)` explicitly); load what a use case needs with a fetch join, `@EntityGraph`, or a projection. Verify query counts in a persistence test when the query is non-trivial.
- **Fetch only what is needed.** Use DTO or interface projections for read models; never load full aggregates to build a list view. Always page or stream unbounded result sets.
- **Transactions** are short, sit at the application-service level, and are `readOnly = true` for queries. Never hold one open across a remote call. Remember `@Transactional` and `@Cacheable` do not apply to self-invocation or private methods.
- **Batch writes** (`hibernate.jdbc.batch_size`, `saveAll`) and use bulk statements for mass updates. Disable `spring.jpa.open-in-view`.
- **Indexes** for every column used in a `WHERE`, `JOIN` or `ORDER BY` of a frequent query, added in a migration alongside the query.
- **Timeouts on every remote call** (connect and read) and bounded, tuned connection pools. A missing timeout is an outage waiting to happen.
- **No blocking in the wrong place**: no remote or database calls inside loops when a batch call exists, none inside `synchronized` blocks or stream pipelines.

Do not add caching, async execution, parallel streams or custom thread pools speculatively. Introduce them when there is evidence, and state the evidence.

## 7. Technology guidance

### JPA / Hibernate with PostgreSQL

- Schema changes go through a migration tool, never `ddl-auto` beyond `validate`. Which tool: if the user names one, use it; otherwise use whatever the project already has (Flyway, Liquibase, or other) and follow its existing file layout, naming and format; for a new project, or one with no migration tool yet, use Liquibase. Never introduce a second tool beside an existing one.
- With Liquibase: a master changelog (`db/changelog/db.changelog-master.yaml`) that only includes per-change files; match the changelog format the project uses (YAML by default for new projects). One logical change per changeSet with a stable, descriptive id and an author; never edit a changeSet that has been applied anywhere, add a new one. Provide a `rollback` where Liquibase cannot derive it, and use preconditions rather than hoping about existing state.
- Make migrations backward compatible so a rolling deployment works (expand, migrate, contract).
- Implement `equals` / `hashCode` on entities by business key or by id with a constant hash code; never Lombok `@Data` on an entity.
- Use optimistic locking (`@Version`) on aggregates that can be updated concurrently, and handle the conflict explicitly.
- Prefer sequence-based ids with pooled allocation or application-generated UUIDs, so inserts can batch. Map enums as `STRING`. Store timestamps as `timestamptz` / `Instant`.
- Enforce integrity in the database as well (`NOT NULL`, unique, foreign keys): the application is not the only writer over time.
- Derived query methods for simple cases, `@Query` JPQL when the name would become unreadable, native SQL when a PostgreSQL feature is needed.
- Pass enums and constants into `@Query` as parameters rather than writing them as fully qualified literals in the query string; the imports rule applies inside JPQL too.
- A query for the "latest" or "first" row needs a deterministic tie-breaker (for example the id) so two rows with the same timestamp cannot produce a result that depends on row order.

### Redis caching

- Cache when a read is frequent, comparatively expensive, and tolerant of staleness; decide the acceptable staleness first, since it sets the TTL. Every key has a TTL.
- Cache-aside via `@Cacheable` / `@CacheEvict` on a Spring bean's public method, or an explicit cache port when logic is needed. Evict or update on write, after the transaction commits.
- Cache immutable DTOs or projections with an explicit, versioned serialization format (JSON), not JPA entities and not JDK serialization. Namespace and version keys (`shop:order:v1:{orderId}`).
- The service must still work when Redis is down: treat cache errors as misses. Consider stampede protection (`sync = true`, jittered TTLs) for hot keys.

### Messaging and events

- Assume at-least-once delivery: consumers are idempotent (dedupe on a message or business id, or make the operation naturally idempotent) and tolerate out-of-order and duplicate messages.
- Never publish to the broker inside a database transaction and hope both succeed. Use a transactional outbox, or publish after commit when occasional loss is acceptable and stated.
- Event contracts are a public API: explicit, versioned schema, additive changes only, separate from domain classes. Carry a correlation id and event id.
- Bounded retries with backoff, then a dead-letter destination; never an infinite poison-message loop. Choose the partition or session key to preserve the ordering the domain needs.

### Security

Treat a security requirement the same way as any other domain rule: it gets a test, not just a comment. "Rejects login after 5 failed attempts" and "a user cannot fetch another user's order" are behaviours, and behaviours are proven the same way everything else in this skill is.

- **Authentication and authorization** through Spring Security. Prefer method-level checks (`@PreAuthorize`) on the application service or controller method over scattering ownership/role `if` checks through the code, so the rule for who may do this is visible in one place, next to the operation it guards.
- **Passwords and secrets.** Hash passwords with a strong adaptive algorithm through Spring Security's `PasswordEncoder` (BCrypt or Argon2); never a fast general-purpose hash, never your own. Never log a password, token, API key, or other secret, even at `DEBUG` — the "Logging" rule in section 4 applies here first. Secrets are injected from the environment or a secrets manager, never committed or hardcoded.
- **Input at the edge, invariants in the domain.** Bean Validation (`@Valid`, `@NotNull`, `@Size`, bounded strings) on every DTO that crosses the API boundary rejects malformed input before it is acted on. The domain still re-validates its own invariants regardless, because a request DTO is not the only path invalid data can take to reach it (a test, an internal caller, a future API, a message consumer).
- **Output and queries.** Parameterized queries and JPA/JPQL prevent SQL injection by construction; never concatenate request data into a query string, native SQL included. Let the serialization layer encode response output; do not hand-assemble HTML, scripts, or shell commands from request data.
- **Transport and sessions.** TLS at the edge, `HttpOnly` and `Secure` cookies for session-based auth, and CSRF protection left on for browser-facing session endpoints. A stateless, token-authenticated API can disable CSRF protection, but that is a stated decision, not Spring Security's default left untouched without anyone deciding.
- **Dependencies.** A vulnerable transitive dependency is still the service's problem; when the project runs a dependency scanner (OWASP Dependency-Check, Snyk, `./gradlew dependencyCheckAnalyze`), treat a new high-severity finding on a dependency you touched like a failing test, not a note for later.

### Resilience and observability

- Every outbound call has a timeout. Add retries only for idempotent operations, with backoff and jitter and a bound; add a circuit breaker or bulkhead (Resilience4j if present) where a failing dependency could exhaust threads. Define what the service does when the dependency is down.
- Expose Actuator liveness and readiness probes that reflect real state, for Kubernetes. Support graceful shutdown.
- Metrics through Micrometer for what matters to the business and to operations (rates, errors, latency, queue lag), with bounded-cardinality tags. Propagate trace context across HTTP and messaging; put the correlation id in the logging context.

## 8. Avoiding over-engineering

Build for the requirement in front of you. Unneeded abstraction costs every future reader, and it is easier to add structure when a second case appears than to remove structure that guessed wrong.

- No interface with a single implementation unless it is a port at a real boundary.
- No design pattern without the problem it solves being present: no factory for one type, no strategy for one algorithm, no builder for three fields.
- No generic "base" classes, frameworks, or configuration options for cases nobody asked for. Tolerate a little duplication until the third occurrence shows the right abstraction.
- No CQRS, event sourcing, saga framework, reactive stack, extra service, or multi-module build unless the requirement clearly calls for it.
- No mapper layer between two identical shapes; no MapStruct for two fields.
- Keep the change scoped to the task. Note worthwhile improvements you noticed rather than making them unasked.

Fixing a smell must not become over-engineering: do not answer a ten-line method with three new classes. When a simpler design and a more "architecturally pure" one both satisfy the requirement and its tests, choose the simpler and say in one line what would make you revisit it.

## 9. Before you finish

Check the work against this list and fix what fails:

- Tests were written first, they run, and they pass; each one would fail if its behaviour broke. Edge and failure cases are covered.
- Every rule, branch and error path in new or changed logic is asserted by a test; nothing was added only to raise a coverage number; project coverage and static-analysis gates pass without new exclusions or suppressions.
- No code smells from section 4 in new or changed code.
- No fully qualified type names outside `import` / `package` lines; no unused imports.
- Business rules live in the domain, not in controllers, application services, or SQL.
- No entity or third-party type leaks through the API; inputs validated; errors mapped consistently.
- No N+1, unbounded query, missing timeout or transaction spanning a remote call.
- Anything handling credentials, authorization, or user input was checked against section 7's security basics, not just the happy path.
- Data structures match access patterns.
- Nothing was added that the requirement does not need.
- New code follows the project's existing conventions and Java version.

Then summarise briefly: what changed, which tests prove it, how to run them, what is deliberately not covered, smells noticed but left alone, and any trade-off or assumption the user should know about. If something could not be verified, say so.
