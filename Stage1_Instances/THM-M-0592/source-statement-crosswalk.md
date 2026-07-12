# Source-statement crosswalk

## Repository source boundary

`Docs/researches/math_theorems.md` gives Alain Connes, 1985, the title "Connes cyclic cohomology,"
and the gloss "cohomology of noncommutative geometry." `Docs/Stage0_Blueprint.md` repeats those data
and explicitly leaves the precise definition and hypotheses open. Its `已验证` label is untrusted
metadata and supplies neither a proved proposition nor machine evidence.

The repository also contains `THM-M-0337` with the near-duplicate Chinese title "康内斯循环上同调"
in a different category. That is an intake-quality issue to be reviewed by the master, not authority
to broaden, merge, or transfer proof credit for `THM-M-0592`.

## Candidate sources

- Alain Connes, "Non-commutative differential geometry," *Publications Mathematiques de l'IHES*
  **62** (1985), 41-144, DOI `10.1007/BF02698807`. This is the historical primary-source candidate
  associated with the metadata date and the introduction of cyclic cohomology in noncommutative
  geometry. An immutable copy, exact proposition/theorem and pages, definitions incorporated by
  reference, assumptions, and corrections have not been accepted in this intake.
- Jean-Louis Loday, *Cyclic Homology*, second edition, Grundlehren der mathematischen
  Wissenschaften 301, Springer (1998). This is a secondary source candidate for comparing precise
  modern formulations and sign conventions. It cannot replace primary-source inspection for H0.

These are bibliographic discovery anchors only. No citation here is an evidence receipt or proof
credit.

## Crosswalk

| Metadata phrase | Candidate mathematical meaning | Required Lean component | Intake disposition |
|---|---|---|---|
| "cyclic cohomology" | a graded invariant built from cyclic cochains or an equivalent complex | algebra, cochains, cyclicity predicate/operator, differential, square-zero proof, cohomology | theory identified; no proposition selected |
| "Connes" | historical construction and associated comparison/periodicity results | no component follows from attribution alone | provenance clue only |
| "noncommutative geometry" | intended domain and applications | associative algebra plus any topology, bornology, or completion explicitly required by the selected theorem | domain family only |
| 1985 | likely historical source year | immutable source revision and exact theorem/page still required | discovery clue only |
| `已验证` | repository status label | none | rejected as source or machine evidence |

## Candidate proposition boundaries

| Candidate | Inputs that must be frozen | Conclusion that must be frozen | Noninterchangeability warning |
|---|---|---|---|
| complex construction | coefficient ring, algebra, cochains, operators and signs | differential squares to zero and defines graded cohomology | a definition alone is not this theorem |
| SBI sequence | Hochschild/cyclic theories and connecting maps | a precisely oriented long exact sequence | not equivalent to mere existence of cyclic cohomology |
| Morita invariance | algebra category and matrix/Morita context | specified induced map is an isomorphism | not a general comparison of cochain models |
| K-theory pairing | cyclic cocycle, K-class model, parity and coefficients | well-defined invariant/pairing with stated properties | requires additional K-theory infrastructure |

Before target correction, an independent reviewer must inspect a stable primary-source copy, select
one proposition, record exact labels/pages and incorporated definitions, map every binder,
hypothesis, and conclusion, check errata, and approve exclusions. Before H0, the source proof must
also be mapped node by node. Before any M0 status, a separate exact Lean expression and kernel proof
closure are required.
