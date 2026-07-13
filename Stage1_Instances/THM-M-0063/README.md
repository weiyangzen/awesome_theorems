# THM-M-0063 rev-5.6 statement dossier

This directory is the fail-closed `planned` intake dossier for Cayley's theorem. The repository
gloss is "every group is isomorphic to some permutation group," attributed to Arthur Cayley in
1854 and labelled verified. Under rev-5.6 the label is untrusted inventory metadata, not a source
audit, exact Lean target, or proof receipt.

The intended theorem family is clear: an arbitrary group acts faithfully on its
underlying set by left multiplication and is therefore isomorphic to the image subgroup inside the
full permutation group. "A permutation group" means a subgroup of a symmetric group, not normally
the entire symmetric group. `Statement.lean` now freezes the conventional repository claim as
`CayleyTheoremTarget`: for every universe-polymorphic `G` with `[Group G]`,
`Nonempty (G ≃* (MulAction.toPermHom G G).range)`. This retains the trivial, finite, and infinite
cases without finiteness, decidable-equality, commutativity, or nontriviality premises.

Pinned mathlib has an exact formal anchor. Module `Mathlib.GroupTheory.Perm.Subgroup` explicitly
calls `Equiv.Perm.subgroupOfMulAction` Cayley's theorem and gives a multiplicative equivalence from
any group with a faithful action to the range of its permutation representation. Specializing the
action carrier to the group itself recovers the usual left-regular statement. The canonical
statement deliberately imports only `Mathlib.Algebra.Group.Action.End` and
`Mathlib.Algebra.Group.Subgroup.Ker`; deletion tests show both vocabulary imports are needed, while
the proof-bearing Cayley anchor is unavailable to that statement-only module. The bounded anchor
audit classifies `Equiv.Perm.subgroupOfMulAction G G` as an exact pinned `M0-W` candidate, but the
classification and wrapper check are provisional and grant no accepted proof credit.

The provisional vector remains `[H1, M3, R4]`: the theorem is classical and a historical primary-paper
lead is known, but no pinpoint source proof is accepted; an exact formal anchor is locally checkable
but not yet audited or credited; and no independently reviewed readable reconstruction exists.
`obligation-registry.json` now freezes 22 canonical obligations before proof-phase acceptance.
`typed-graphs.json` separates proof, refinement, provenance, evidence, trust, documentation, and
workflow edges; `obligation-tree.md` is the stable readable architecture surface.
`ObligationTree.lean` checks only conditional composition from explicit faithful-action,
injectivity, left-inverse, and range-equivalence interfaces to the exact root. It does not invoke or
install the pinned Cayley body. `instance.json` remains the planned structured scope authority, and
the master-owned `task-dag.json` is unchanged. No H0, accepted M0 root, R0, accepted execution state,
audit completion, theorem completion, or master acceptance is claimed.
