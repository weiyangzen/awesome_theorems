# Full study: Erdős 1095 lower solved variant

## Mathematical object

The target is the source theorem
`∃ c > 0, (fun k : ℕ ↦ exp (c * log k ^ 2)) =O[atTop] fun k ↦ (g k : ℝ)`,
where `g` is the source-defined Erdős–Selfridge function.  Its formal anchor
is `FormalConjectures/ErdosProblems/1095.lean:49-52` at the pinned revision.

## Formal transport

The target-local Lean files import the exact provider module and use the
qualified source declaration directly.  No hypothesis is dropped, and no
local symbol can shadow a source symbol.  The crosswalk records the source
file, declaration/type digests, elaborated-root placeholders for Master
recomputation, transitive constant census, bidirectional transport, and cold
replay evidence.

## Trust and review

Machine and readability ledgers are content-addressed.  Readable reconstruction
retains hypotheses, inference, output, formal anchor, downstream use,
exceptional cases, and trust boundary.  Two independent review identities are
recorded; all human, machine, and readability cut sets are empty pending the
canonical-Master replay.
