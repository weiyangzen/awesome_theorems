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

Pinned mathlib has a very close formal anchor. Module `Mathlib.GroupTheory.Perm.Subgroup` explicitly
calls `Equiv.Perm.subgroupOfMulAction` Cayley's theorem and gives a multiplicative equivalence from
any group with a faithful action to the range of its permutation representation. Specializing the
action carrier to the group itself recovers the usual left-regular statement. The canonical
statement deliberately imports only `Mathlib.Algebra.Group.Action.End` and
`Mathlib.Algebra.Group.Subgroup.Ker`; deletion tests show both vocabulary imports are needed, while
the proof-bearing Cayley anchor is unavailable. `IntakeProbe.lean` remains discovery-only; exact
anchor provenance, proof-body inspection, and trust closure belong to later phases.

The provisional vector remains `[H1, M3, R4]`: the theorem is classical and a historical primary-paper
lead is known, but no pinpoint source proof is accepted; an exact formal anchor is locally checkable
but not yet audited or credited; and no independently reviewed readable reconstruction exists.
`statement.json` records the exact target and fingerprint, `statement-validation.md` records the
scoped self-test, and `statement-receipt.json` is the provisional node handoff. `instance.json`
remains the planned structured scope authority, while `task-dag.json` remains unchanged with all
six downstream tasks open pending master action. No H0, M0, R0, accepted execution state, audit
completion, theorem completion, or master acceptance is claimed.
