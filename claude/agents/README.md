# Agent roster

Subagent definitions symlinked into `~/.claude/agents/` by setup.sh. Most are adapted
from [visiquate/cco](https://github.com/visiquate/cco) (curated from its 117-agent set,
deduplicated, stripped of its daemon/knowledge-base dependencies). Conventions:

- `model:` uses bare tiers (haiku/sonnet/opus) so defs survive model releases.
- Tool grants are least-privilege: review/audit agents are read-only (Glob, Grep, Read);
  builders get Edit/Write/Bash only when the role requires it.
- No persistent store: agents check the project CLAUDE.md / vault note for context and
  return durable findings in their final response for the main session to persist.

## Architecture and design

| Agent | Model | Description |
|---|---|---|
| chief-architect | opus | High-level architecture and design-decision agent. |
| backend-architect | sonnet | Backend system architecture and API design specialist. |
| cloud-architect | sonnet | Cloud infrastructure design and optimization specialist for AWS/Azure/GCP. |
| database-architect | sonnet | Database architecture and design specialist. |
| architect-review | sonnet | Use this agent to review code for architectural consistency and patterns. |
| terraform-specialist | sonnet | Terraform and Infrastructure as Code specialist. |
| legacy-modernizer | haiku | Refactor legacy codebases, migrate outdated frameworks, and implement gradual modernization. |

## Security and compliance

| Agent | Model | Description |
|---|---|---|
| security-auditor | sonnet | Reviews code for security vulnerabilities - OWASP Top 10, auth/authz flaws, secrets, injection. Read-only. |
| security-engineer | sonnet | Security infrastructure and compliance specialist. |
| penetration-tester | sonnet | Penetration testing and ethical hacking specialist. |
| compliance-specialist | sonnet | Security compliance and regulatory framework specialist. |

## Review and quality

| Agent | Model | Description |
|---|---|---|
| code-reviewer | sonnet | Reviews code for quality, readability, and maintainability. Read-only - flags issues, does not fix them. |
| test-engineer | haiku | Test automation and quality assurance specialist. |
| debugger | haiku | Debugging specialist for errors, test failures, and unexpected behavior. |
| unused-code-cleaner | haiku | Detects and removes unused code (imports, functions, classes) across multiple languages. |

## AI and agentic

| Agent | Model | Description |
|---|---|---|
| ai-engineer | sonnet | LLM application and RAG system specialist. |
| prompt-engineer | haiku | Expert prompt optimization for LLMs and AI systems. |
| model-evaluator | haiku | AI model evaluation and benchmarking specialist. |
| mcp-server-architect | sonnet | MCP server architecture and implementation specialist. |
| mcp-testing-engineer | haiku | MCP server testing and quality assurance specialist. |

## Research

| Agent | Model | Description |
|---|---|---|
| technical-researcher | sonnet | Use this agent when you need to analyze code repositories, technical documentation, implementation details, or evaluate technical solutions. |
| academic-researcher | haiku | Academic research specialist for scholarly sources, peer-reviewed papers, and academic literature. |
| fact-checker | haiku | Fact verification and source validation specialist. |
| search-specialist | haiku | Expert web researcher using advanced search techniques and synthesis. |

## Data

| Agent | Model | Description |
|---|---|---|
| data-engineer | haiku | Data pipeline and analytics infrastructure specialist. |
| data-scientist | haiku | Data analysis and statistical modeling specialist. |
| database-admin | haiku | Database administration specialist for operations, backups, replication, and monitoring. |
| database-optimizer | haiku | SQL query optimization and database schema design specialist. |
| sql-pro | haiku | Write complex SQL queries, optimize execution plans, and design normalized schemas. |
| nosql-specialist | haiku | NoSQL database specialist for MongoDB, Redis, Cassandra, and document/key-value stores. |

## DevOps and operations

| Agent | Model | Description |
|---|---|---|
| devops-engineer | haiku | DevOps and infrastructure specialist for CI/CD, deployment automation, and cloud operations. |
| devops-troubleshooter | haiku | Production troubleshooting and incident response specialist. |
| incident-responder | haiku | Handles production incidents with urgency and precision. |
| monitoring-specialist | haiku | Monitoring and observability infrastructure specialist. |
| error-detective | haiku | Log analysis and error pattern detection specialist. |
| dependency-manager | haiku | Use this agent to manage project dependencies. |
| load-testing-specialist | haiku | Load testing and stress testing specialist. |
| git-flow-manager | haiku | Git Flow workflow manager. |
| changelog-generator | haiku | Changelog and release notes specialist. |
| network-engineer | haiku | Network connectivity and infrastructure specialist. |
| performance-engineer | sonnet | Profile applications, optimize bottlenecks, and implement caching strategies. |

## Languages

| Agent | Model | Description |
|---|---|---|
| python-pro | haiku | Write idiomatic Python code with advanced features like decorators, generators, and async/await. |
| typescript-pro | haiku | Write idiomatic TypeScript with advanced type system features, strict typing, and modern patterns. |
| javascript-pro | haiku | Master modern JavaScript with ES6+, async patterns, and Node. |
| golang-pro | haiku | Write idiomatic Go code with goroutines, channels, and interfaces. |
| rust-pro | haiku | Write idiomatic Rust with ownership patterns, lifetimes, and trait implementations. |
| shell-scripting-pro | haiku | Write robust shell scripts with proper error handling, POSIX compliance, and automation patterns. |

## Frontend and mobile

| Agent | Model | Description |
|---|---|---|
| frontend-developer | haiku | Frontend development specialist for React applications and responsive design. |
| fullstack-developer | haiku | Full-stack development specialist covering frontend, backend, and database technologies. |
| ui-ux-designer | haiku | UI/UX design specialist for user-centered design and interface systems. |
| web-accessibility-checker | haiku | Web accessibility compliance specialist. |
| web-vitals-optimizer | haiku | Core Web Vitals optimization specialist. |
| react-performance-optimizer | sonnet | Specialist in React performance patterns, bundle optimization, and Core Web Vitals. |
| nextjs-architecture-expert | sonnet | Master of Next. |
| cli-ui-designer | haiku | CLI interface design specialist. |
| mobile-developer | haiku | Cross-platform mobile development specialist for React Native and Flutter. |
| flutter-specialist | haiku | Flutter development specialist for cross-platform mobile, state management, native integrations, UI/UX implementation, and performance optimization. |
| ios-developer | haiku | Native iOS development specialist with Swift and SwiftUI. |

## Platforms and integration

| Agent | Model | Description |
|---|---|---|
| graphql-architect | sonnet | GraphQL schema design and API architecture specialist. |
| supabase-schema-architect | sonnet | Supabase database schema design specialist. |
| salesforce-api-specialist | sonnet | Salesforce platform integration expert covering REST/SOAP/Bulk/Streaming APIs, SOQL optimization, OAuth flows, and sync strategies. |
| api-explorer | sonnet | Explores, tests, and documents third-party APIs and builds integration POCs and client code. |
| ml-engineer | sonnet | ML production systems and model deployment specialist. |

## Docs and writing

| Agent | Model | Description |
|---|---|---|
| technical-writer | haiku | Technical writing and content creation specialist. |
| api-documenter | haiku | Create OpenAPI/Swagger specs, generate SDKs, and write developer documentation. |
| markdown-syntax-formatter | haiku | Markdown formatting specialist. |
| content-marketer | haiku | Content marketing and SEO optimization specialist. |
| business-analyst | haiku | Business metrics analysis and reporting specialist. |

## Obsidian vault maintenance

| Agent | Model | Description |
|---|---|---|
| vault-linker | haiku | Obsidian vault connection specialist. Analyzes the vault for missing links, orphaned notes, and connection opportunities, and reports proposed changes without editing anything. |
| vault-metadata | haiku | Obsidian frontmatter and metadata specialist. Audits the vault's frontmatter for gaps and inconsistencies against the vault's own observed conventions, and reports proposed changes without editing anything. |
| vault-tagger | haiku | Obsidian tag taxonomy specialist. Audits tag usage across the vault for duplicates, drift, and structure against the vault's own observed patterns, and reports proposed changes without editing anything. |
| vault-reviewer | haiku | Obsidian vault quality assurance specialist. Reviews proposed or applied vault maintenance changes (links, metadata, tags) for consistency with the vault's own conventions, and reports findings without editing anything. |
