# Caching Strategy & Implementation Details

## Objective

The objective of the caching strategy was to reduce unnecessary database operations and improve the response time of the Executive Briefing generation process. By storing frequently accessed data in memory, repeated requests can be served significantly faster without repeatedly querying the database.

---

# Current Caching Strategy

The Executive Briefing system uses an in-memory caching approach to minimize repeated database reads.

The following datasets are suitable for caching because they do not change frequently:

- Supplier Information
- Supplier Performance Data
- Inventory Information

These datasets are reused across multiple Executive Briefing requests whenever possible.

---

# Cache Design

The cache stores previously loaded data in memory.

Request Flow:

Client Request

↓

Check Cache

↓

Cache Available?

├── Yes → Return Cached Data

└── No → Read Database → Store in Cache → Return Response

This approach reduces repeated database access and improves overall system performance.

---

# Time-To-Live (TTL) Strategy

Different datasets require different cache durations depending on how frequently they change.

| Dataset | TTL |
|----------|-----|
| Supplier Information | 1 Hour |
| Supplier Performance | 24 Hours |
| Inventory Data | 4 Hours |

The TTL values ensure that cached data remains reasonably fresh while minimizing unnecessary database queries.

---

# Cache Hit

When valid cached data is available:

- Database queries are skipped.
- Data is returned directly from memory.
- Response time is significantly reduced.
- Local execution time is approximately 0.01 seconds after cache warm-up.

---

# Cache Miss

When cached data is unavailable or expired:

- The application queries the database.
- Latest data is retrieved.
- Cache is refreshed.
- Updated data is returned to the client.

The first request typically takes longer because it loads data from the database.

---

# Cache Invalidation

To prevent outdated information, cache invalidation is supported through:

## Time-Based Expiration

Cached data automatically expires after its configured TTL.

## Manual Invalidation

Whenever supplier or inventory information is updated, the cache can be cleared manually to ensure future requests use the latest data.

---

# Benefits

The implemented caching strategy provides several advantages:

- Reduced database load
- Faster repeated requests
- Lower network overhead
- Better scalability
- Improved API responsiveness
- Reduced unnecessary computation

---

# Future Improvements

Future optimization phases may include:

- Redis distributed caching
- Database query caching
- Connection pooling
- Automatic cache refresh
- Cache monitoring dashboards
- Configurable cache policies

---

# Conclusion

The in-memory caching strategy successfully improves Executive Briefing performance by minimizing repeated database operations. Combined with function refactoring and parallel execution, caching forms an important part of the overall optimization strategy. Future enhancements will focus on distributed caching solutions and database-level optimization.