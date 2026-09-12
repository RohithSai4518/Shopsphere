# ADR 0012: Tiered Rate Limiting

## Status
Accepted

## Decision
Enforce tiered rate limits by API key and client IP using sliding window counters in Redis.