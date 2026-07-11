# Source-statement crosswalk

## Candidate sources

- Jonathan M. Beck, *Triples, Algebras and Cohomology* (1967 thesis; Reprints in Theory and
  Applications of Categories 2, 2003). This is the historical primary candidate. The precise
  theorem/page, relation between the original and reprint, and errata have not yet been inspected.
- Saunders Mac Lane, *Categories for the Working Mathematician*, second edition, Springer GTM 5
  (1998), the monads and algebras material. This is a secondary normalization candidate; an exact
  theorem/page and wording still require inspection.

These are discovery anchors, not `H0` evidence. The statement phase must inspect stable copies and
record the exact variant, assumptions, terminology, and errata.

## Crosswalk

| Repository phrase | Mathematical component | Expected Lean component | Intake status |
|---|---|---|---|
| "monads and adjunctions" | monad induced by `F ⊣ G` | `Adjunction.toMonad` | included; exact binders open |
| comparison functor | `D` to algebras for the induced monad | `Monad.comparison` | legacy candidate only |
| monadic | comparison functor is an equivalence | `MonadicRightAdjoint G` | encoding candidate only |
| `G`-split pair | pair whose image has specified split coequalizer data | `G.IsSplitPair f g` and related classes | terminology cross-check open |
| Beck criterion | creates, or has/preserves/reflects, relevant coequalizers | `monadicOf...GSplitCoequalizers` family | exact source variant open |

## Existing Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_140.lean` imports
`Mathlib.CategoryTheory.Monad.Monadicity` and wraps several declarations, including the creates and
has/preserves/reflects variants. It is valuable candidate evidence but predates the rev-5.6 freeze.
Its declarations must be re-elaborated at the pinned revision, their exact types and axioms checked,
and each terminal proof body's provenance audited. The intake makes no claim that the legacy
`StatementShape` matches a selected source theorem.
