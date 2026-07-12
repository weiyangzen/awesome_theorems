# Source-statement crosswalk

## Repository sources

`Docs/researches/math_theorems.md` records `单调电路下界`, Alexander Razborov, 1985, and only the
gloss `单调电路的下界` ("lower bounds for monotone circuits"). Stage0 repeats this record. It
contains no circuit definition, function family, lower-bound expression, parameter regime,
theorem locator, or proof citation. The rev-5.6 manifest therefore preserves `已验证` only as
`source_status_untrusted`.

`Docs/researches/cs_theorems.md` independently contains a nearby secondary row named `Razborov下界`
with the more specific gloss `CLIQUE的单调电路下界`. This supports CLIQUE as the leading source
candidate, but it is a separate inventory row and still lacks a quantified statement. It cannot by
itself resolve the target.

## Primary-source candidate

The bibliographic candidate matching the repository's author and year is A. A. Razborov, "Lower
bounds on the monotone complexity of some Boolean functions", *Doklady Akademii Nauk SSSR* 281
(1985), with the English translation in *Soviet Mathematics Doklady* 31 (1985), 354-357. This
intake records it as a locator, not an accepted `H0` source: the statement phase must inspect an
immutable scan or authoritative edition, identify the exact numbered result and pages, transcribe
its parameter choices and bound, check translation and errata, and obtain source review.

Later stronger CLIQUE lower bounds must be recorded separately rather than folded into Razborov's
1985 statement.

## Crosswalk

| Source phrase | Mathematical component to freeze | Lean component | Intake status |
|---|---|---|---|
| "monotone circuit" | positive Boolean gate basis, fan-in, constants, DAG/formula convention | a new audited circuit datatype/evaluator unless a pinned candidate is found | absent in pinned mathlib search |
| "CLIQUE" (secondary clue) | graph encoding and predicate for a clique of exactly/at least `k` vertices | `SimpleGraph`, `SimpleGraph.IsClique` / `IsNClique`, finite edge-indexed Boolean input | graph/clique API probed; encoding open |
| "lower bound" | circuit size measure and exact inequality/asymptotic notation | size function plus explicit quantified inequality | missing from repository statement |
| 1985 / Razborov | original approximation-method result | source nodes and formal obligations for every imported combinatorial lemma | candidate citation only |
| `已验证` | untrusted inventory metadata | no proposition or proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe imports
`Mathlib.Combinatorics.SimpleGraph.Clique` and checks finite simple graphs, `IsClique`, `IsNClique`,
the edge finset, and generic function monotonicity. A bounded case-insensitive search over
`Mathlib/**/*.lean` for circuit declarations and monotone circuit terminology found no relevant
Boolean-circuit complexity interface. This is scoped negative evidence only; the anchor-audit phase
must run the frozen discovery protocol over repo-local and external candidates.
