# GUARA Constitution
## Core Principles

### [PRINCIPLE_1_NAME]
<!-- Example: I. Library-First -->
[PRINCIPLE_1_DESCRIPTION]
<!-- Example: Every feature starts as a standalone library; Libraries must be self-contained, independently testable, documented; Clear purpose required - no organizational-only libraries -->

### [PRINCIPLE_2_NAME]
<!-- Example: II. CLI Interface -->
[PRINCIPLE_2_DESCRIPTION]
<!-- Example: Every library exposes functionality via CLI; Text in/out protocol: stdin/args → stdout, errors → stderr; Support JSON + human-readable formats -->

### [PRINCIPLE_3_NAME]
<!-- Example: III. Test-First (NON-NEGOTIABLE) -->
[PRINCIPLE_3_DESCRIPTION]
<!-- Example: TDD mandatory: Tests written → User approved → Tests fail → Then implement; Red-Green-Refactor cycle strictly enforced -->

### [PRINCIPLE_4_NAME]
<!-- Example: IV. Integration Testing -->
[PRINCIPLE_4_DESCRIPTION]
<!-- Example: Focus areas requiring integration tests: New library contract tests, Contract changes, Inter-service communication, Shared schemas -->

### [PRINCIPLE_5_NAME]
<!-- Example: V. Observability, VI. Versioning & Breaking Changes, VII. Simplicity -->
[PRINCIPLE_5_DESCRIPTION]
<!-- Example: Text I/O ensures debuggability; Structured logging required; Or: MAJOR.MINOR.BUILD format; Or: Start simple, YAGNI principles -->

## [SECTION_2_NAME]
<!-- Example: Additional Constraints, Security Requirements, Performance Standards, etc. -->

[SECTION_2_CONTENT]
<!-- Example: Technology stack requirements, compliance standards, deployment policies, etc. -->

## [SECTION_3_NAME]
<!-- Example: Development Workflow, Review Process, Quality Gates, etc. -->

[SECTION_3_CONTENT]
<!-- Example: Code review requirements, testing gates, deployment approval process, etc. -->

## Governance
<!-- Example: Constitution supersedes all other practices; Amendments require documentation, approval, migration plan -->

[GOVERNANCE_RULES]
<!-- Example: All PRs/reviews must verify compliance; Complexity must be justified; Use [GUIDANCE_FILE] for runtime development guidance -->

**Version**: [CONSTITUTION_VERSION] | **Ratified**: [RATIFICATION_DATE] | **Last Amended**: [LAST_AMENDED_DATE]
<!-- Example: Version: 2.1.1 | Ratified: 2025-06-13 | Last Amended: 2025-07-16 -->

# GUARA Constitution

## Article I - Zero-Trust Architecture (ZTA)

### Section 1.1 - Network Security Posture
All system components must operate under a Zero-Trust Architecture model, where no implicit trust is granted to any network segment or service.

### Section 1.2 - Public Interface Restrictions
Public interfaces must not be exposed without middleware authentication. Binding to 0.0.0.0 without authentication is strictly prohibited.

### Section 1.3 - Transport Security
All production endpoints must use HTTPS/TLS 1.3 exclusively for secure communication.

## Article II - ORCID API Integration & OAuth 2.0 Compliance

### Section 2.1 - Redirect URI Validation
Redirect URIs must be validated using pinned matching with strict validation, prohibiting wildcarding or open redirects.

### Section 2.2 - PKCE Implementation
PKCE (Proof Key for Code Exchange) must be implemented with cryptographic secure state parameter verification against CSRF attacks.

### Section 2.3 - Rate Limiting and Exception Handling
Rate limiting and exception handling must be implemented to prevent ORCID API quota exhaustion or IP bans through exponential backoff and circuit breaker patterns.

### Section 2.4 - At-Rest Encryption
Client Secrets and Refresh Tokens must be encrypted using AES-256 (GCM) for data at rest.

## Article III - Data Persistence & Database Layer

### Section 3.1 - SQL Injection Prevention
Prevention of SQL Injection attacks through the use of Prepared Statements or Parameterized Queries via ORM (SQLAlchemy/SQLModel).

### Section 3.2 - Principle of Least Privilege
Database connections must follow the Principle of Least Privilege, with database roles lacking DDL privileges such as DROP or ALTER at runtime.

### Section 3.3 - Schema Validation
Schema validation must include Type Enforcement, Check Constraints, Foreign Key Cascades, and Unique Indexes.

### Section 3.4 - Input Sanitization and Validation
All API payloads must be validated and sanitized using Pydantic Schemas before processing.

## Article IV - AI Agent Code Generation Rules

### Section 4.1 - Prohibition of Mocks and Placeholders
No mocks, pseudocodes, MOPs, or placeholders (TODOs) are allowed in critical authentication, validation, or encryption routes.

### Section 2.2 - Static Application Security Testing
All generated code must pass Static Application Security Testing using Bandit and Ruff before approval.

### Section 4.3 - Fail-Secure Default
In case of unhandled failures, the system must terminate connections/transactions without exposing stack traces or infrastructure metadata in HTTP responses.

