# THM-M-0063 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for Cayley's theorem. The repository
gloss is "every group is isomorphic to some permutation group," attributed to Arthur Cayley in
1854 and labelled verified. Under rev-5.6 the label is untrusted inventory metadata, not a source
audit, exact Lean target, or proof receipt.

The intended theorem family is clear at intake: an arbitrary group acts faithfully on its
underlying set by left multiplication and is therefore isomorphic to the image subgroup inside the
full permutation group. "A permutation group" means a subgroup of a symmetric group, not normally
the entire symmetric group. The source record nevertheless omits an exact citation, its definitions,
ordered binders, the subgroup carrier, the regular-action convention, and all source-to-formal
mapping. Intake records those open choices rather than selecting the downstream canonical target.

Pinned mathlib has a very close formal anchor. Module `Mathlib.GroupTheory.Perm.Subgroup` explicitly
calls `Equiv.Perm.subgroupOfMulAction` Cayley's theorem and gives a multiplicative equivalence from
any group with a faithful action to the range of its permutation representation. Specializing the
action carrier to the group itself recovers the usual left-regular statement. `IntakeProbe.lean`
authenticates this API and its axiom report, but does not freeze an expression or confer proof credit;
exact specialization, target identity, provenance, and trust closure belong to later phases.

The provisional vector is `[H1, M3, R4]`: the theorem is classical and a historical primary-paper
lead is known, but no pinpoint source proof is accepted; an exact formal anchor is locally checkable
but not yet integrated as the canonical target; and no independently reviewed readable
reconstruction exists. `instance.json` is the structured scope authority and `task-dag.json` keeps
all six downstream phases open. No H0, M0, R0, accepted execution state, audit completion, theorem
completion, or master acceptance is claimed.
