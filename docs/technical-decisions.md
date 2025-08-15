# Technical decisions

This document outlines the key architectural and implementation decisions I made for the project.
I went with some technical decisions like I would in a real-world project.

> For database design decisions, see [Database Design Choices](./db-design-choices.md).

## Architecture: Feature-Driven Structure

I chose a **feature-driven architecture** over traditional layered architecture for better maintainability and developer experience.

```
src/
├── core/                    # Cross-cutting concerns
│   ├── database.py         # Database connection & session management
│   ├── middleware.py       # API key authentication middleware
│   └── config.py          # Environment configuration (Pydantic settings)
├── features/               # Domain-specific features
│   ├── companies/
│   │   ├── models.py      # Company database models
│   │   ├── schemas.py     # Pydantic DTOs for API contracts
│   │   ├── service.py     # Business logic & data operations
│   │   └── router.py      # FastAPI route definitions
│   ├── projects/          # Same structure for projects
│   ├── users/             # Same structure for users
│   └── analytics/         # Same structure for analytics
└── scripts/
    └── docker stuff and data sync scripts
```

### Why Feature-Driven?

**Benefits over traditional layered architecture:**
- ✅ **Domain Isolation**: Each feature is self-contained with clear boundaries
- ✅ **Team Scaling**: Features can be owned by different team members
- ✅ **Testing**: Natural isolation makes unit testing cleaner (we didn't test it in here, but this would be a must)
- ✅ **Refactoring**: Changes to one feature rarely impact others

**Core vs Feature Distinction:**
- **Core**: Shared infrastructure that every feature needs (database, auth, config)
- **Feature**: Business domain logic specific to one area of the application

## Dependency Management

I prioritize **simplicity and explicitness** in dependency management:

### Principles
1. **If it shouldn't be there, it shouldn't be there** - No unnecessary dependencies
2. **Reusable components get getters** - Avoid passing dependencies through multiple layers
3. **Single source of truth** - One place to configure each dependency

## Authentication: Middleware vs Dependency Injection

I chose **middleware-based API key validation** over FastAPI's `Depends()` pattern.

### Why Middleware?

1. **Cleaner Routes**: Business logic isn't cluttered with authentication concerns
2. **Early Validation**: Authentication fails fast, before route processing
3. **Consistency**: Impossible to forget authentication on a route
4. **DRY Principle**: Authentication logic exists in exactly one place
5. **Security by Default**: All routes are protected unless explicitly excluded

## Data Synchronization: Script vs Function

I chose a **standalone script** approach for external API data synchronization.

### Why Standalone Script?

**Advantages:**
- ✅ **Operational Control**: Can be run independently of app lifecycle
- ✅ **Scheduling Flexibility**: Easy to integrate with cron jobs or task schedulers
- ✅ **Reusability**: Can be run for maintenance, testing, or data recovery
- ✅ **Clear Separation**: Data initialization is separate from runtime concerns

**Trade-offs:**
- ❌ **Manual Step**: Requires explicit execution

For a project management platform where data sync is a one-time or periodic operation (not real-time), the operational flexibility outweighs the convenience of automatic execution.

## Design Decisions

All decisions follow the **"You Aren't Gonna Need It"** principle aka **YAGNI**.

- **Security-first**: Company-centric data isolation and UUID primary keys
- **Maintainability**: Clear separation of concerns and explicit dependencies

## Decisions I end up choosing not to make (due to this ^), but I would do if in a "real-world" project:
- **Soft deletes (Pretty damn common in B2B for compliance/recovery)
- **Pagination (Not really needed for this project but good to have for large datasets)
- **RBAC (Casbin is top notch for this, project roles)
- **Auditing (Who did what, when - crucial for B2B)
- **Caching (Redis for company/user lookups)
- **Analytics infrastructure** (ClickHouse/Snowflake or even a TDBMS like Prometheus with Grafana dashboards instead of PostgreSQL aggregations)

I tried to maintain balance above all else, it's pretty easy to over-engineer something, so if we scope out first and execute later, everything comes together :)