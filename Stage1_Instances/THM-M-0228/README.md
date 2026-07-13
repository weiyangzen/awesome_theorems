# THM-M-0228 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Little Picard theorem. The
repository attributes the theorem to Emile Picard in 1879 and supplies only the gloss "a
nonconstant entire function takes all complex values with at most one exception." Its `已验证`
("verified") label is untrusted metadata under rev-5.6 and supplies no source or Lean proof credit.

The gloss identifies the classical theorem family, but it does not fix the exact definition of
entire, the nonconstancy encoding, or the logical form of "at most one exception." Equivalent
candidate conclusions include saying that the complement of the range is a subsingleton, that any
two omitted values are equal, or that there is a possibly non-omitted value outside of which the
function is surjective. These require checked transports rather than textual identification.

This intake freezes that scope and the decisions required by the statement phase while leaving the
canonical mathematical and Lean targets null. The provisional root vector is `[H1, M4, R3]`: a
historically proved theorem family is recognizable, but no accepted pinpoint statement/proof
source or exact formal artifact is credited, and only an intake-level route explanation exists.

The structured authority is `instance.json`. The scope map and source-statement crosswalk record
the exact boundary; all six dependent phases remain open in `task-dag.json`. `IntakeProbe.lean`
checks only adjacent pinned APIs and states no target theorem. No H0, M0, R0, accepted execution
state, audit completion, theorem completion, or master acceptance is claimed.
