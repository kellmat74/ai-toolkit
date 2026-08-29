---
name: perf-optimize
description: Performance optimization loop - establish baselines, profile to find real bottlenecks, fix highest-impact first, measure after each change, load test at the end. Use when something is slow, resource-hungry, or missing a performance target, or when the user asks to optimize or profile a component.
---

# Perf Optimize: Performance Optimization

## Trigger
`/perf-optimize <component or requirement>`

Identifies and executes performance optimization with profiling, analysis, and
validation. Core loop: baseline, measure, fix, validate.

## Purpose
- Performance profiling and analysis
- Bottleneck identification
- Optimization strategy development
- Implementation and validation
- Baseline comparison
- Load testing

## Workflow

### Phase 1: Define Performance Requirements

1. Find the targets. Check the repo's CLAUDE.md, docs, SLAs, or the project's
   vault note for documented performance requirements. If none exist, agree on
   targets with the user before optimizing - "faster" is not a target.
2. Identify current metrics
   - Response time
   - Throughput/requests per second
   - Memory usage
   - CPU utilization
   - Database query time
3. Determine optimization scope
   - Specific endpoints or functions
   - Overall system
   - Database queries
   - Frontend performance
   - Infrastructure

### Phase 2: Establish Baselines

Measure BEFORE changing anything. For a large or unfamiliar system, the
`performance-engineer` subagent (Task tool) can run the profiling pass
independently and report findings.

1. Response time
   ```
   Endpoint: GET /api/users
   p50: 245ms
   p95: 380ms
   p99: 520ms
   Target: p95 < 200ms
   Status: EXCEEDS TARGET by 90%
   ```
2. Throughput
   ```
   Current: 120 req/s
   Target: 500 req/s
   Gap: 76% under target
   ```
3. Resource usage
   ```
   Memory (peak): 340MB
   CPU (average): 65%
   Database connections: 12/20 (60%)
   ```
4. Database metrics
   ```
   Query time (avg): 180ms
   Query count per request: 15 (N+1 problem detected)
   Slow queries: 5 taking > 100ms each
   ```

### Phase 3: Analyze and Identify Bottlenecks

1. Profiling report
   ```
   Call Graph Analysis:
   - API handler: 10ms (8%)
   - Database queries: 180ms (72%) <- BOTTLENECK
   - Response marshaling: 30ms (12%)
   - Network latency: 20ms (8%)

   Time Distribution:
   - Query 1 (get user): 5ms
   - Query 2-15 (get posts): 170ms <- PROBLEM
   - Loop inefficiency: 5ms
   ```
2. Bottleneck identification, ranked by impact
   ```
   Bottleneck 1: N+1 Database Queries (CRITICAL)
   - Issue: Fetching user, then loop-fetching each post's comments
   - Impact: 170ms out of 250ms (68% of total time)
   - Root cause: No eager loading in ORM
   - Fix: Use JOINs or eager load() syntax

   Bottleneck 2: Memory Usage (MEDIUM)
   - Issue: Large result set loaded into memory
   - Impact: 340MB peak memory
   - Root cause: Fetching all data at once
   - Fix: Implement pagination or streaming

   Bottleneck 3: Unoptimized Query (MEDIUM)
   - Issue: Missing database index
   - Impact: 45ms per filtered query
   - Root cause: No index on user.status column
   - Fix: Add database index
   ```

### Phase 4: Design Optimization Strategy

1. Optimization plan, highest impact first, with expected improvement and risk
   per item:
   ```
   Optimization 1: Fix N+1 Queries (Impact: -68%)
   - Current: 15 separate queries
   - Optimized: 1 query with JOINs
   - Expected improvement: 170ms -> 15ms
   - Implementation: Modify ORM query, add tests
   - Risk: Low (no behavior change)

   Optimization 2: Add Database Index (Impact: -12%)
   - Current: Sequential scan on users table
   - Optimized: B-tree index on status column
   - Expected improvement: 45ms -> 5ms
   - Implementation: Migration to add index
   - Risk: Low (index-only change)

   Optimization 3: Implement Pagination (Impact: -10%)
   - Current: Load all results in memory
   - Optimized: Page-based loading
   - Expected improvement: 340MB -> 45MB (peak)
   - Implementation: API endpoint changes
   - Risk: Medium (behavior change for clients)

   Total expected improvement:
   - Response time: 245ms -> 48ms (80%)
   - Memory: 340MB -> 45MB (87%)
   - Meets target: p95 < 200ms
   ```
2. Risk assessment per optimization
   ```
   Risk 1: ORM query changes
   - Likelihood: Low (well-tested ORM)
   - Impact: Regression in other queries
   - Mitigation: Comprehensive test suite

   Risk 2: Index creation
   - Likelihood: Very low
   - Impact: Query performance regression
   - Mitigation: Test on staging first

   Risk 3: API pagination
   - Likelihood: Medium (client impact)
   - Impact: Client code breaks
   - Mitigation: Backward-compatible pagination
   ```

### Phase 5: Implement Optimizations

Implement sequentially, one at a time.

```python
# BEFORE: N+1 Query Problem
def get_users_with_posts():
    users = db.query(User).all()  # Query 1
    for user in users:
        user.posts = db.query(Post).filter(Post.user_id == user.id).all()  # Query 2-N
    return users

# AFTER: Optimized with eager loading
def get_users_with_posts():
    users = db.query(User).options(
        joinedload(User.posts)  # Load all posts in single query
    ).all()
    return users
```

After EACH optimization:
```bash
# Run tests to ensure behavior unchanged
pytest tests/ -v

# Re-profile to measure improvement
python -m cProfile -s cumulative main.py
```

Never stack unmeasured changes; if an optimization doesn't move the metric,
revert it rather than keep the complexity.

### Phase 6: Measure Improvement

Validate against the baseline after each optimization:

```
BEFORE OPTIMIZATION:
- p50: 245ms
- p95: 380ms <- TARGET: 200ms
- p99: 520ms
- Memory peak: 340MB
- Throughput: 120 req/s

AFTER OPTIMIZATION 1 (Fix N+1):
- p50: 95ms (61% improvement)
- p95: 145ms (62% improvement) <- MEETS TARGET
- p99: 210ms (60% improvement)
- Memory peak: 280MB (18% improvement)
- Throughput: 320 req/s (167% improvement)

AFTER OPTIMIZATION 2 (Add Index):
- p50: 82ms, p95: 125ms, p99: 195ms
- Throughput: 380 req/s

AFTER OPTIMIZATION 3 (Pagination):
- p50: 45ms, p95: 48ms, p99: 85ms
- Memory peak: 45MB (84% improvement)
- Throughput: 500 req/s

FINAL RESULT:
- Response time: 245ms -> 48ms (80% improvement)
- Memory: 340MB -> 45MB (87% improvement)
- Throughput: 120 -> 500 req/s (317% improvement)
- Meets all targets
```

### Phase 7: Load Testing

Test performance under load:

```javascript
// k6 load test
import http from 'k6/http';
import { check } from 'k6';

export let options = {
  stages: [
    { duration: '2m', target: 100 },   // Ramp up
    { duration: '5m', target: 500 },   // Stay at 500
    { duration: '2m', target: 0 },     // Ramp down
  ],
};

export default function() {
  let res = http.get('http://localhost:8000/api/users');
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 100ms': (r) => r.timings.duration < 100,
  });
}
```

Results to verify:
```
Load Test Results (500 concurrent users):
- Avg response: 52ms
- Max response: 145ms
- Error rate: 0%
- P95: 75ms
- P99: 120ms
- Throughput: 485 req/s

System Resources:
- CPU: 42% utilization
- Memory: 68MB (peak)
- Database connections: 8/20 (40%)
- All under capacity
```

### Phase 8: Document Results

Summarize before/after metrics, the optimizations applied with per-item
improvements, and confirmation that regression tests and load tests passed.
If this surfaces something durable (a recurring pattern, a convention, a
lesson), propose saving it to the Obsidian vault via the vault skill - ask
before writing.

## Optimization Techniques

### Database
- **Eager loading**: JOINs instead of N+1 queries
- **Indexing**: B-tree indexes on filter columns
- **Query optimization**: analyze query plans
- **Connection pooling**: reuse database connections
- **Caching**: Redis for frequently accessed data

### Code
- **Algorithmic**: reduce complexity (O(n^2) -> O(n log n))
- **Memoization**: cache expensive calculations
- **Lazy loading**: load data only when needed
- **Batch processing**: process in batches
- **Concurrency**: parallel execution where applicable

### Infrastructure
- **Caching layers**: CDN, Redis, HTTP caching
- **Load balancing**: distribute across servers
- **Horizontal scaling**: more servers
- **Vertical scaling**: more powerful server
- **Compression**: gzip for responses

### Frontend
- **Code splitting**: smaller bundles
- **Minification**: remove unnecessary bytes
- **Lazy loading**: load images/scripts on demand
- **Asset optimization**: image compression
- **Caching**: service workers, HTTP caching

## Metrics to Track

| Metric | Target | Tool |
|--------|--------|------|
| Response Time (p95) | < 200ms | APM, load test |
| Throughput | 500+ req/s | Load test |
| Error Rate | < 0.1% | APM, monitoring |
| Memory (peak) | < 100MB | Profiling |
| CPU Utilization | < 70% | Monitoring |
| Database Query Time | < 50ms | Database monitoring |

(Adjust targets per project; these are sane defaults for a typical API.)

## Best Practices

1. **Measure first** - know the baseline
2. **Profile accurately** - identify real bottlenecks
3. **Optimize strategically** - high impact first
4. **Test thoroughly** - no regressions
5. **Validate improvements** - measure after each change
6. **Load test** - ensure performance under stress
7. **Document findings** - share with the team
8. **Monitor in production** - catch regressions early
9. **Iterate** - optimization is ongoing
10. **Trade-offs** - understand complexity vs performance

## Output Format

Report with:
- Baseline performance metrics
- Bottleneck analysis with root causes
- Optimization strategy and plan
- Implementation details for each optimization
- Before/after measurements
- Load testing results
- Risk assessment
