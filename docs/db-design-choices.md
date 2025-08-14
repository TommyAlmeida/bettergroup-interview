# Database Design Choices

This db design is built on top of the YAGNI Principle, just because we dont want to build what the requirements dont ask for.

This design prioritizes security, simplicity, and data isolation.

I end up choosing a company-centric architecture due to data isolation, by making the company the root of all relationships and adding company_id to the join table, we ensure:

- Impossible for users to access projects from other companies
- All queries can be scoped by company first (efficient partitioning)
- Easier to implement data residency and privacy regulations

## UUID PKs

I used this instead of integeres due to the security and scalability of distributed systems:

- Because they dont expose business metricas (user count, project count)
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