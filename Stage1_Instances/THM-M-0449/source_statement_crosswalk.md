# Source-statement crosswalk

| Claim component | Available source anchor | Lean discovery candidate | Intake assessment |
|---|---|---|---|
| Theorem identity | `Docs/researches/math_theorems.md`: Chinese label, Guy Henniart / Marie-France Vigneras, 2000 | none | Insufficient to identify a primary publication or named theorem; `H4` |
| Root claim | "p-adic群的局部朗兰兹对应" | `S1_M_063.FrozenTheoremVariant` | Broad research program, not an exact proposition; legacy candidate is expressly an abstract statement shape |
| p-adic group | no group family stated | `PadicReductiveGroupDatum K` | Candidate broadens to arbitrary abstract K-points and therefore cannot be accepted |
| Automorphic objects | not stated | abstract `AutomorphicParameter` plus predicate | Missing smoothness, admissibility, irreducibility, isomorphism classes, and coefficient conditions |
| Galois/L-parameters | not stated | abstract `LanglandsParameter` plus predicate | Missing Weil/Weil-Deligne/L-group definition, continuity, Frobenius convention, and enhancement |
| Correspondence properties | not stated | bijectivity plus central-character and local-factor predicates | Predicate meanings and normalization are abstract, so these fields do not establish fidelity |
| Boundary cases | not stated | none accepted | characteristic, rank, ramification, and coefficient restrictions remain open |

## Source identity blocker

The repository attribution is not enough to distinguish several materially different local
Langlands results. Intake therefore does not manufacture a title, DOI, theorem number, or scope.
Before statement work, a primary source must be identified and pinned, and its actual theorem must
be crosswalked by page/theorem number, hypotheses, conclusion, normalization, and errata. The
attributed authors and year must also be checked rather than treated as authority.

The historical file `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_063.lean` says itself that its
`FrozenTheoremVariant` is definitionally an abstract statement shape and "not a terminal local
Langlands proof." It is retained solely as discovery provenance. Substituting it for the unknown
human theorem would violate the rev-5.6 exact-statement gate.
