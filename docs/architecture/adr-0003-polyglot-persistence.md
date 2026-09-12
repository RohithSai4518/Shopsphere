# ADR 0003: Polyglot Persistence Strategy

## Status
Accepted

## Decision
Use PostgreSQL as the source of truth with Redis Cluster for cache invalidation and distributed session tokens.