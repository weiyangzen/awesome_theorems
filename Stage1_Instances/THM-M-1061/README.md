# THM-M-1061 rev-5.6 intake

This is the `planned` intake for Varadhan's integral lemma. The Stage0 phrase
"Laplace principle" is too short to determine a formal proposition by itself. This
intake freezes the standard bounded-continuous integral lemma, not an equivalence
between an LDP and a Laplace principle and not an unbounded-function extension.

## Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Ambient space | regular topological measurable space adequate for the LDP bounds and compactness argument | exact mathlib typeclasses are not selected |
| Probabilistic input | probability measures with a full LDP and good rate function at vanishing positive speed | weak-LDP and exponential-tightness transports are separate obligations |
| Test function | bounded continuous real-valued `F` | unbounded variants require an additional tail/moment hypothesis |
| Root result | logarithmic exponential-integral limit equals `sup_x (F x - I x)` | extended-real codomain and empty/infinite conventions remain statement work |
| Proof architecture | compact-sublevel upper bound, local LDP lower bound, tail control, passage to supremum | no leaf or terminal theorem is credited |
| Formal surface | future Lean 4 target using pinned mathlib measure, topology, and asymptotic APIs | no declaration has been found or elaborated in this phase |

The canonical binders, hypotheses, exclusions, conventions, and alternate encodings
are recorded in `intake.json`. Source-to-claim correspondence and its remaining
audit debt are recorded in `source_statement_crosswalk.md`.

## Statement artifact

The statement phase has now frozen and elaborated
`Stage1Instances.THM_M_1061.VaradhanIntegralLemmaTarget` in `Statement.lean`.
It selects a nonempty Polish ambient space, spells out the full LDP upper and
lower bounds, uses a good `ENNReal`-valued rate function, and places both sides
of the limit in `EReal`. Exact hashes, imports, mutations, and commands are in
`statement.json` and `statement-validation.md`. This is statement evidence only.

## Intake verdict

Lifecycle remains `planned`; the statement node is self-tested pending master
acceptance. The source anchors are discovery-quality rather than accepted H0
receipts, and no theorem proof is claimed. The next workflow gate is the anchor
audit. The theorem is not complete.

## Obligation architecture

Registry version 1 now freezes 15 canonical obligations and seven separate
typed graphs in `obligation-registry.json` and `typed-graphs.json`. The lower
localization, compact-core upper bound, bounded tail estimate, and EReal limit
merge remain open. `ObligationTree.lean` checks only the conditional identity
transport from the exact terminal proposition to the root; it supplies no
analytic proof or theorem-completion credit.

## Validation

The exact local checks and results are recorded in `validation.md`. They validate
manifest membership, repository-standard consistency, JSON syntax, and dossier
references only.
