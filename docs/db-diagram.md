# Database Schema

## Core Tables

**companies**: Organizations with domains
**users**: People belonging to companies
**projects**: Projects owned by companies
**project_memberships**: User-project relationships

## Key Design Decisions

**UUID Primary Keys**: Better for distributed systems
**Company-Centric**: All entities flow from companies
**Denormalized company_id**: In memberships for faster queries
**Cascade Delete**s: Maintain referential integrity
 
Few more in [Design Choices](./db-design-choices.md)

``` mermaid 
erDiagram
    companies {
        uuid id PK
        varchar name
        varchar domain UK
        timestamp created_at
    }
    
    users {
        uuid id PK
        varchar email UK
        uuid company_id FK
        timestamp created_at
    }
    
    projects {
        uuid id PK
        varchar name
        uuid company_id FK
        timestamp created_at
    }
    
    project_memberships {
        uuid id PK
        uuid project_id FK
        uuid user_id FK
        uuid company_id FK
        timestamp created_at
    }
    
    %% Relationships - Company-Centric
    companies ||--o{ users : "owns all users"
    companies ||--o{ projects : "owns all projects"
    companies ||--o{ project_memberships : "controls all access"
    users ||--o{ project_memberships : "can be members"
    projects ||--o{ project_memberships : "can have members"
```
