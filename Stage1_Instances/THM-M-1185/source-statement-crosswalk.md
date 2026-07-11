# Source-statement crosswalk

## Available source record

`Docs/researches/math_theorems.md` gives the title "Brenier theorem", Yann Brenier, 1991, the
statement phrase `凸势的最优传输`, and the untrusted status `已验证`.
`Docs/Stage0_Blueprint.md` supplies only the target name. No bibliography, paper title, theorem
number, page, definitions, hypotheses, proof, or errata record is attached. Thus the intake does
not assert a primary-source candidate and does not assign `H0`.

## Crosswalk

| Source element | Information fixed | Information still required for Lean | Intake result |
|---|---|---|---|
| "Brenier theorem" | names a theorem family | exact theorem variant and proposition | unresolved |
| Yann Brenier / 1991 | attribution and approximate date | primary edition, theorem/page, errata | unresolved |
| "optimal transport" | optimization over transport is central | measures, couplings/maps, cost and minimizer predicate | unresolved |
| "convex potential" | convexity and a potential are central | domain, codomain, gradient notion, a.e. convention | unresolved |
| `已验证` | secondary metadata label | inspectable source proof and kernel receipt | no credit |

## Candidate boundary

The standard Euclidean quadratic-cost formulation commonly called Brenier's theorem is a discovery
hypothesis only. The repository also contains adjacent optimal-transport material, including
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_151.lean` for a McCann/existence target and
`S1_M_280.lean` for transport-cost infrastructure. Neither file is an exact candidate merely by
topic, and neither receives rev-5.6 proof credit at intake.

The next gate must first pin a primary source and approve a row-by-row mapping of every source
hypothesis and conclusion to an elaborated Lean expression. Only afterward may the anchor audit
test mathlib or external declarations for exact type, proof-body provenance, axioms, and imports.
