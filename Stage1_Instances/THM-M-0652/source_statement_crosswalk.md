# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| An interpolating formula exists | `Docs/researches/math_theorems.md`, entry "插值定理", attributes William Craig (1957) and says "插值公式的存在性" | `AwesomeTheorems.Stage1.S1_M_298.StatementShape` | Repository wording supports theorem identity but omits logic, consequence relation, and vocabulary condition; its `已验证` label is untrusted |
| Classical first-order semantic theorem | William Craig, "Three uses of the Herbrand-Gentzen theorem in relating model theory and proof theory", *Journal of Symbolic Logic* 22 (1957), 269-285 | explicit four-language semantic formulation in the historical module | Primary-source bibliographic anchor located, but edition/page-to-premise and errata audit remain open; no H0 claim |
| Consequence factorization | If left entails right, find theta with left entails theta and theta entails right | `SemanticConsequence` and `IsInterpolant` | Candidate direction matches the standard theorem; exact elaboration deferred |
| Common vocabulary | Theta contains only nonlogical symbols common to antecedent and consequent | `Lcommon` with maps to `Lleft` and `Lright` and a commuting joint-language square | A common sublanguage is represented, but equality with the full vocabulary intersection is not encoded or proved; this is the principal statement-risk item |
| Syntactic formulation | Derivability interpolation via a cut-free calculus | later proof-calculus bridge candidates in the historical module | Not part of the frozen root; equivalence requires checked soundness/completeness transports |

The root excludes Lyndon, uniform, propositional-only, infinitary, higher-order, and theory-relative
interpolation. It includes empty common vocabulary and identical side languages. The statement
phase must inspect the declaration type, serialize its normalized expression, decide and enforce
the exact common-symbol condition, check alternate transports, and mutation-test map commutation,
entailment directions, universes, and boundary languages.

Repository discovery candidate: `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_298.lean`.
No immutable primary-source URL or file hash is credited at intake. The bibliographic citation,
assumptions, page mapping, corrections, and independent review remain open. Current human status is
therefore `H2`, not `H0`.
