# Source-statement crosswalk

## Candidate primary sources

- Leopold Loewenheim, "Uber Moglichkeiten im Relativkalkul," *Mathematische Annalen* 76 (1915),
  447-470. This is a historical source candidate for the downward lineage, not yet a pinpoint
  source for the modern elementary-substructure formulation.
- Thoralf Skolem, "Logisch-kombinatorische Untersuchungen uber die Erfullbarkeit oder Beweisbarkeit
  mathematischer Satze nebst einem Theoreme uber dichte Mengen," *Videnskapsselskapets skrifter,
  I. Matematisk-naturvidenskabelig klasse* (1920), no. 4. This is a historical source candidate;
  its exact scope and relationship to the modern formulation still require inspection.
- Alfred Tarski and Robert L. Vaught, "Arithmetical extensions of relational systems,"
  *Compositio Mathematica* 13 (1956-1958), 81-102. This is a primary research source candidate for
  elementary extensions. An exact theorem/page, hypotheses, terminology, and errata have not yet
  been verified.

These entries are discovery anchors, not `H0`. The historical results need not use the modern
two-clause formulation frozen here. The anchor audit must select a stable source (or separate
primary sources for the two clauses), inspect the full statements and definitions, record exact
edition/theorem/page and errata, and obtain independent review.

## Crosswalk

| Frozen component | Human-source question | Required Lean component | Intake evidence/status |
|---|---|---|---|
| first-order language `L` | one-sorted finitary signature and its size convention | `FirstOrder.Language` and `L.card` | pinned API exists; source definition open |
| downward ambient model | nonempty `L`-structure `M` | `[L.Structure M] [Nonempty M]` | pinned API exists |
| distinguished set `A` | subset required to lie in the small model | `A : Set M`, `A subset N` | pinned API exists |
| downward cardinal bounds | infinite `kappa`, `|A|, |L| <= kappa <= |M|` | cardinal inequalities with universe lifts | exact transport open |
| downward conclusion | elementary substructure containing `A` of size `kappa` | `L.ElementarySubstructure M` and cardinal equality | candidate declaration probed |
| upward ambient model | infinite `L`-structure `M` | `[L.Structure M] [Infinite M]` | pinned API exists |
| upward cardinal bounds | `|L|, |M| <= kappa` | cardinal inequalities with universe lifts | exact transport open |
| upward conclusion | elementary extension of exact size `kappa` | bundled structure, `M` elementary-embeds into `N`, `#N = kappa` | candidate declaration probed |
| paired theorem identity | both directions belong to this target | conjunction/package plus checked projections | formal assembly open |

## Existing Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the local source comments
identify `FirstOrder.Language.exists_elementarySubstructure_card_eq` as the downward theorem and
`FirstOrder.Language.exists_elementaryEmbedding_card_eq_of_ge` as the upward theorem. The broader
`FirstOrder.Language.exists_elementaryEmbedding_card_eq` chooses an embedding direction from a
cardinal comparison and therefore does not by itself establish that the paired target has been
mapped exactly.

`IntakeProbe.lean` checks that these declarations and relevant types elaborate in the pinned worker
environment. It neither defines the canonical target nor audits terminal proof bodies, axioms,
transitive dependencies, source fidelity, or checked transports. Consequently the evidence remains
`M4` discovery input until the statement and anchor-audit gates are completed.
