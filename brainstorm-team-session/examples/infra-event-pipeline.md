# Example: Event Pipeline Architecture

## User Input

> We're getting ~50k events/sec and they need to be processed in order per
> customer. I'm thinking Kafka with customer ID as partition key. What could
> go wrong?

## Phase 0: Assert P

**Restated problem:** You need ordered, per-customer event processing at 50k
events/sec with reliability guarantees.

Confirmed with user? Yes — they agreed the ordering is per-customer, not
global.

## Phase 1: Extract Constraints

| Type | Constraint |
|------|-----------|
| Hard | Per-customer ordering must be preserved |
| Hard | ~50k events/sec sustained throughput |
| Soft | Team already knows Kafka (implicit: low ramp-up cost) |
| Implicit | "Processed" implies at-least-once or exactly-once semantics needed |

## Phase 2: S(P) Loop

**S_0: Kafka, customer_id as partition key**

- Advocate: Kafka handles this natively. Partition ordering is guaranteed.
  Team knows it. Battle-tested at this scale.
- Skeptic: What happens when a hot customer generates 40% of traffic? Single
  partition becomes bottleneck. Also: what if customer_id changes (merges,
  migrations)?
- Pragmatist: Kafka ops overhead is real — ZooKeeper (or KRaft), broker
  tuning, partition rebalancing. Is the team staffed for this?
- User-proxy: Does "in order" mean strict total order, or causal order?
  Strict order with a hot partition = head-of-line blocking.

**Problems found** -> Phase 3.

## Phase 3: Account For Problems

1. **Hot partition / key skew** — blocker
   - If one customer generates disproportionate traffic, their partition
     becomes a bottleneck and can back-pressure the entire consumer group.
   - User chose: Resolve now -> sub-partitioning strategy with
     customer_id + session_id, merge at consumer.

2. **Ops overhead** — risk
   - Team is 3 people. Kafka cluster management is non-trivial.
   - User chose: Note and accept -> will use managed Kafka (Confluent/MSK).

3. **Exactly-once semantics** — risk
   - Kafka's exactly-once requires idempotent producers + transactional
     consumers. Adds complexity.
   - User chose: Note and accept -> at-least-once with idempotent consumers
     is sufficient.

## Phase 4: Present Candidate

**Recommended:** Managed Kafka (MSK) with composite partition key
(customer_id + session_id). Consumers merge ordering per-customer using
sequence numbers. At-least-once delivery with idempotent consumer writes.

- Satisfies: per-customer ordering, 50k/sec throughput, team familiarity
- Trade-offs: managed service cost (~$X/mo), slightly more complex consumer
  logic for sub-partition merging
- Accepted risks: ops dependency on cloud provider, at-least-once (not
  exactly-once)
- Discarded: Redis Streams (ordering guarantees weaker at scale), SQS FIFO
  (300 msg/sec per group — 170x short)
