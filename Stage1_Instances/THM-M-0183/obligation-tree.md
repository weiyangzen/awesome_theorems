# THM-M-0183 obligation tree

The frozen registry contains 14 root-relevant obligations. Proof edges point from a parent to the
children it requires and have reciprocal child-to-parent `composes` edges. Provenance, trust,
documentation, refinement, evidence, and workflow edges are separate typed graphs and confer no
proof credit.

The proof architecture follows the classical continuity method: native geometric realization;
reference metric and global potential; the Chern/ricci-form transport; complex Monge-Ampere
reduction; uniform estimates; openness and closedness; elliptic regularity; construction of a
compatible metric in the prescribed class; and exact final assembly. Boundary behavior and the
foundation policy own independent obligations.

`M0183-T-ASSEMBLE` is the only provisionally checked leaf. `ObligationTree.lean` verifies that the
complete analytic package implies the frozen root under identical binders and hypotheses. It does
not construct the package. The current remaining root cut set is therefore `M0183-T-METRIC`, and
the root remains M4. No audit-complete or theorem-complete claim is made.

The machine-readable node ledgers, eligibility denominators, validity records, and all seven typed
graphs are frozen in `obligation-registry.json` and `typed-graphs.json`. Any later split, merge, or
eligibility correction requires a versioned append-only delta rather than mutation of this v1
denominator.
