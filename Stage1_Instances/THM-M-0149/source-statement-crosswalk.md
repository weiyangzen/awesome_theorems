# Source-statement crosswalk

## Available record and candidate source

The repository inventory supplies the Chinese title `博克松定理`, attribution to Caucher Birkar,
year 2016, and only the phrase "boundedness of Fano varieties". Its `已验证` label is untrusted under
rev-5.6. Attribution and subject strongly indicate Birkar's proof of the BAB conjecture; the title
itself is not a reliable mathematical identifier.

A primary-source candidate is Caucher Birkar, *Singularities of linear systems and boundedness of
Fano varieties*, Annals of Mathematics 193 (2021), 347-405, especially the boundedness theorem near
the start of the paper. This bibliographic locator is discovery evidence only. The article's exact
theorem number, wording, definitions, submission/preprint history, and errata have not been
independently inspected in this intake, so it supplies no `H0` credit.

## Crosswalk

| Repository/source phrase | Provisional mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "Fano varieties" | normal projective varieties with anti-canonical positivity | schemes/varieties, canonical divisor, positivity | family identified; conventions open |
| "boundedness" | parameterization by a finite-type family | family over finite-type base and fiber/isomorphism relation | exact definition open |
| Birkar / BAB | singular Fano boundedness at fixed dimension and singularity threshold | dimension and epsilon-lc predicates | essential omitted hypotheses restored provisionally |
| fixed `d` | uniform family for one dimension | dimension equality and outer quantification | binder order open |
| fixed `epsilon > 0` | uniform lower discrepancy bound | real/rational parameter and discrepancy inequalities | coefficient/domain open |
| log-pair variant | possible boundary `B` and `-(K_X+B)` positivity | divisor coefficients, log canonical divisor | source selection open |

## Source and machine boundary

No theorem-specific accepted Lean declaration is identified at intake. The manifest's
`hard_mathlib_anchor_and_wrapper` lane is scheduling metadata, not evidence that mathlib contains
the terminal theorem. The later anchor audit must search the pinned dependency and credible Lean 4
projects at immutable revisions and inspect exact declaration types, bodies, axioms, and licenses.

Before `H0`, an independent reviewer must inspect the chosen primary edition, theorem/page,
definitions, every hypothesis, proof boundary, and errata. Before statement credit, every approved
component must map row by row to an elaborated canonical Lean expression.
