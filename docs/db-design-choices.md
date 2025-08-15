# Database Design Choices

This db design is built on top of the YAGNI Principle, just because we don't want to build what the requirements don't ask for.

This design prioritizes security, simplicity, and data isolation.

I end up choosing a company-centric architecture due to data isolation, by making the company the root of all relationships and adding company_id to the join table, we ensure:

- Impossible for users to access projects from other companies
- All queries can be scoped by company first (efficient partitioning)
- Easier to implement data residency and privacy regulations

## UUID PKs

I used this instead of integers due to the security and scalability of distributed systems:

- Because they don't expose business metrics (user count, project count, company count)
- No conflicts when merging databases (if needed)
- Works across multiple database instances (aka no weird driver issues)

## Join table with company ref

Instead of just project_memberships(project_id, user_id), we add company_id:

- Enforces company boundaries at the data level
- Can filter by company first in complex membership queries
- Triple-check that user, project, and company all align
- Clear ownership chain for compliance

## Single FKs Constraints

- Database prevents orphaned records
- Migration order is obvious
- App crashes early if trying to create invalid relationships


We don't really use the `created_at` field, but it's there for completeness.

``` mermaid 
erDiagram
    Company {
        UUID id PK
        string name
        string domain UK
        datetime created_at
    }
    
    User {
        UUID id PK
        string email UK
        UUID company_id FK
        datetime created_at
    }
    
    Project {
        UUID id PK
        string name
        UUID company_id FK
        datetime created_at
    }
    
    ProjectMembership {
        UUID id PK
        UUID project_id FK
        UUID user_id FK
        UUID company_id FK
        datetime created_at
    }
    
    %% Relationships - Company-Centric
    Company ||--o{ User : "owns all users"
    Company ||--o{ Project : "owns all projects"
    Company ||--o{ ProjectMembership : "controls all access"
    User ||--o{ ProjectMembership : "can be members"
    Project ||--o{ ProjectMembership : "can have members"
    
    %% Constraints
    ProjectMembership }|--|| User : "unique(project_id, user_id)"
```
