# Source-statement crosswalk

## Primary source

George Lusztig, "Canonical bases arising from quantized enveloping algebras", *Journal of the American Mathematical Society* **3** (1990), 447-498.

This paper is the primary construction anchor. Exact theorem/proposition numbers, page wording, the paper's Cartan-data conventions, stable identifier, and errata remain open to page-level inspection. Consequently the statement node still records `H1`, not `H0`, and cannot select a canonical Lean proposition.

## Crosswalk

| Intake component | Source-side role | Current disposition |
|---|---|---|
| symmetrizable Cartan data | input defining the quantized enveloping algebra | included; exact generality open |
| negative half | algebra carrying the canonical basis | included |
| integral form | lattice generated using divided powers | included; coefficient convention open |
| bar involution | structure used in canonical characterization | included; Lean model open |
| distinguished basis | canonical-basis construction and basis theorem | included; exact theorem nodes open |
| PBW/geometric presentation | construction or comparison route | no equivalence credited until source and Lean transports are checked |

## Exact premise and boundary mapping

| Formal statement component | Required source admission | Current result |
|---|---|---|
| Cartan datum binder | exact finite/general and symmetrizability convention | open; no ordered Lean binder frozen |
| quantum group object | exact negative, positive, or modified form and base coefficients | open; no concrete Lean object admitted |
| integral form | source definition and divided-power normalization | open; no hypothesis or structure credited |
| bar operation | coefficient action and involution law used by the selected result | open; no map type or side condition credited |
| PBW/geometric construction | selected order, indexing set, and comparison theorem | open; no alternate encoding credited |
| canonical basis conclusion | exact existence, basis, uniqueness, congruence, invariance, and positivity package | open; the repository slogan does not decide the conjunction |
| boundary data | zero rank, disconnected data, specializations, and sign/form conventions | open; no source-faithful boundary mutation is available |

Two broad readings remain uncredited: a bar-invariant integral-lattice characterization of the
basis of `U_q^-(g)`, and a geometric/PBW construction plus comparison theorem. The repository has
not selected source nodes that make either reading exact. Adopting the historical
`AwesomeTheorems.Stage1.S1_M_057.StatementShape` would not resolve this: its quantum-group and
canonical-basis properties are proposition-valued fields rather than source-defined structure.
It supplies no H0, exact-statement, transport, or proof credit.

## Provenance boundary

Repository metadata supplies a short Chinese name, category, and untrusted `已验证` label. It does not identify an exact source theorem or establish source fidelity. `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_057.lean` explicitly contains statement-shape scaffolding and audit records rather than a canonical-basis proof, and receives no rev-5.6 proof credit.

## Open H-gate work

Inspect a stable scan and bibliography; correct the identifier if necessary; record exact theorem labels/pages, hypotheses, definitions of the algebra and integral form, dependencies between construction and basis results, and published errata. An independent reviewer must attest the final source-to-Lean crosswalk before `H0` is possible. Until that source admission exists, the exact target, expression fingerprint, checked transports, and removed-hypothesis/changed-domain/changed-binder-scope/boundary-case mutations remain unavailable.
