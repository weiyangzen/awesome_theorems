# Scope map

## Included claim

- The collective result in Karp's 1972 chapter, not merely the existence of an NP-complete problem.
- Exactly the chapter's listed combinatorial decision problems, with source-faithful definitions.
- For every problem, membership in the relevant nondeterministic-polynomial class and the required
  polynomial reduction/completeness result.
- The reduction graph and composition needed to deliver completeness for every list member.
- Finite input encodings, size measures, reduction algorithms, correctness, and polynomial bounds.

The formal root should ultimately be a fixed 21-component conjunction or an indexed proposition
whose index type is proved to correspond bijectively to the source inventory. A theorem about an
unconstrained supplied list would weaken the historical claim.

## Decisions deferred to statement freeze

The statement phase must transcribe the source's displayed list and definitions from a stable copy,
including the distinction between source problem headings and later conventional counting. It must
fix exact encodings for Boolean formulas, graphs/digraphs, integer arrays, set families, routing,
packing, covering, assignment, and sequencing instances; the input length measure; the notion of
polynomial time; and the direction and strength of reduction.

All constraints that make a problem a decision problem belong in the target. Examples include
graph finiteness, directedness, integer sign/range, capacity and threshold parameters, and whether
a route or cover must be exact. Empty and malformed inputs must be accepted or excluded explicitly,
not left to an implementation accident.

## Explicit exclusions

- Cook-Levin/SAT completeness alone, or any one of the 21 results alone.
- The claim that an unspecified collection of 21 predicates is complete.
- Modern variants bearing similar names without checked transports to Karp's definitions.
- Pairwise equivalence without separately establishing class membership and the source's notion of
  completeness.
- Computable many-one reducibility (`ManyOneReducible`) as a silent substitute for polynomial-time
  reducibility.
- Optimization versions, heuristic performance, or empirical solver success.
- The manifest label `已验证` as human-source or kernel evidence.

No canonical Lean target is frozen at intake. The next node must resolve the exact inventory and
encoding boundary before it observes or credits proof candidates.

