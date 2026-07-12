# THM-M-0792 rev-5.6 intake

This is the `planned` dossier for the fundamental theorem of forcing. The repository source says
only "basic properties of forcing extensions". That phrase can denote the forcing theorem, the
truth lemma alone, or a broader generic-model theorem, which are not interchangeable propositions.
The intake therefore records the intended family without inventing an exact Lean target.

## Scope map

| Surface | Candidate scope | Boundary at intake |
|---|---|---|
| Ground model | a transitive set model of a specified fragment of ZF/ZFC, or an internally coded model | model notion, theory fragment, transitivity, countability, and external universe are unfrozen |
| Forcing notion | a preorder/partial order `P` belonging to the ground model, possibly with a top element | order convention, separativity, set/class status, and membership assumptions are unfrozen |
| Generic object | a filter `G` meeting every dense subset of `P` that belongs to the ground model | filter orientation and whether existence is assumed externally are unfrozen |
| Syntax and semantics | first-order formulas in the language of set theory, forcing names, valuation by `G`, and satisfaction in `M[G]` | coding, arity, assignments, and parameter restrictions are unfrozen |
| Definability lemma | the forcing relation is definable over the ground model by recursion on formulas/names | candidate component, not a frozen root |
| Truth lemma | truth in `M[G]` is witnessed by a condition in `G` that forces the corresponding formula | candidate component, not a frozen root |
| Combined forcing theorem | definability plus the equivalence between extension truth and forcing by some member of `G` | leading root candidate, but not selected by the source record |
| Generic model theorem | `M[G]` is a model of a base theory, has the expected ordinals, and contains `M` and `G` | related theorem family; not accepted as an equivalent substitute |
| Lean surface | a model-theoretic or set-theoretic encoding of the rows above | exact modules, expression, universes, and environment fingerprint remain open |

Set forcing is the candidate scope. Class forcing, Boolean-valued models, iterated forcing,
preservation theorems, and applications such as independence of CH are excluded unless a later
source-faithful scope decision explicitly selects them. Trivial forcing is a boundary fixture, not
a replacement target.

## Intake verdict

Lifecycle is `planned`; root vector is `[H3, M4, R3]`. The first failed gate is exact source scope:
the available record does not identify one proposition or its assumptions. No canonical Lean
expression can truthfully be elaborated yet. This is statement/formalization debt, not a claim that
the underlying mathematics is open. The theorem is not complete.

## Validation

The commands and results in `validation.md` establish manifest membership, repository-standard
consistency, JSON syntax, dossier reference integrity, and absence of proof-placeholder constructs.
No Lean declaration is introduced in this intake, so no kernel proof result is claimed. Master
acceptance and all dependent phases remain outstanding.
