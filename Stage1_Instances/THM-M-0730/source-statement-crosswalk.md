# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the title `PCP定理的更强形式`, attributes it to Irit
Dinur, dates it to 2007, and supplies only `PCP的组合证明` ("a combinatorial proof of PCP"). Stage0
repeats that metadata while leaving definitions, assumptions, proof path, equivalences, axioms,
and formal artifacts open. The rev-5.6 manifest deliberately preserves `已验证` only as
`source_status_untrusted`.

The duplicated research-catalog entry does not add an independent source. It gives neither a
quantified proposition nor PCP parameters, so the adjective "stronger" cannot determine a target.

## Probable primary source candidate

The metadata strongly suggests Irit Dinur, "The PCP Theorem by Gap Amplification," *Journal of the
ACM* 54(3), 2007, Article 12. This bibliographic identification is a discovery anchor, not `H0`:
no immutable copy, exact numbered theorem/page, assumption list, statement-to-Lean mapping, errata
check, or independent review has been accepted in this intake.

The article title also exposes the central ambiguity. "Gap amplification" names the proof engine,
whereas "the PCP theorem" names a complexity-theoretic consequence. They require different Lean
roots and cannot share proof credit without checked implications.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "PCP" | probabilistically checkable proof verifier/class | encoded languages, verifiers, randomness/query bounds, completeness and soundness | candidate only; exact convention absent |
| "combinatorial proof" | reduction through finite constraint graphs | finite CSP/constraint graph, assignment, satisfied-edge fraction, effective transformations | intended route only, not a proposition |
| "stronger form" | gap-amplification theorem | quantified input/output gap, size, degree, alphabet, and constructivity bounds | possible root; parameters absent |
| Dinur / 2007 | probable JACM article | immutable source revision and pinpoint theorem crosswalk | bibliographic candidate only |
| `已验证` | untrusted inventory label | no Lean proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports finite simple-graph, finite-cardinality, and rational-number support and checks seven
general API types. These are only possible encoding ingredients. A simple graph may itself be too
weak because a constraint graph can attach predicates to edges and may require parallel or directed
constraints. The probe neither selects that representation nor locates a PCP theorem.

