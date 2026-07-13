# THM-M-0972 rev-5.6 intake

`THM-M-0972` is the enumerative-combinatorics catalog item "Janson inequality." The repository
attributes it to Svante Janson, dates it to 1990, and supplies only the gloss "probability of the
union of rare events" plus an untrusted `verified` label.

## Intake result

This dossier records a fail-closed `planned` instance. The received gloss does not determine one
truth-valued proposition. Standard references use "Janson inequality" for several bounds: two
nonoccurrence estimates for a dependent indicator count, a product refinement, and a 1990 lower-tail
estimate. These choices have different conclusions and sometimes different hypotheses. Moreover,
the event `X = 0` is the complement of the union of occurrence events, not the probability of their
union as the catalog wording suggests.

An immutable secondary reference and two matching 1990 primary-source leads are recorded in the
crosswalk. Their exact source definitions, theorem statements, proof boundaries, page-range
discrepancy, corrections, and independent review have not been admitted. No source is credited as
`H0`, and no one variant is silently chosen as the target.

## Formal boundary

`IntakeProbe.lean` elaborates adjacent pinned independent-random-set, independence, finite-union,
lower-tail Chernoff, and binomial-random-graph APIs. A bounded topic search found no declaration
named for Janson in repo-local Lean or pinned mathlib. An immutable external Atlas Lean snapshot
does contain exact-topic declarations, but their root-relevant chains use explicit `sorry` and earn
no proof credit; its restrictive license is also unresolved. These are intake observations only,
not the downstream exhaustive anchor audit and not proof evidence.

The canonical mathematical statement and Lean expression remain null. The provisional vector is
`[H1, M4, R4]`: complete published theorem families and source leads are known, but the exact root
and source map are open; no usable exact formal artifact is credited; and no source-faithful proof
reconstruction can attach to an unfrozen root. All six downstream tasks remain open. No accepted
execution state, audit completion, theorem completion, or master acceptance is claimed.
