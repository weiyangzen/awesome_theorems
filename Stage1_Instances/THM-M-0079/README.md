# THM-M-0079 rev-5.6 statement and anchor-audit dossier

This directory is the fail-closed `planned` intake dossier for `THM-M-0079`, the
Nielsen-Schreier theorem. The repository claim is exactly "every subgroup of a free group is
free." Its `1921` date, joint Jakob Nielsen/Otto Schreier attribution, and `已验证` status are
untrusted catalog metadata rather than source or proof evidence.

The unrestricted claim is mathematically recognizable, but its historical source boundary needs
care. Crossref identifies the bibliographic record for Otto Schreier's 1927 paper *Die Untergruppen
der freien Gruppen*. An unpreserved secondary lead associates that paper with the general result
and the repository's 1921 date with Nielsen's earlier finitely generated case, so those historical
claims are questions for source audit rather than admitted facts. No primary theorem text,
incorporated definitions, proof boundary, corrections, or errata were available and reviewed in
this intake. The provisional human status is therefore `H1`, not `H0`.

`Statement.lean` now freezes the exact universe-polymorphic target: for every `G : Type u` with
`[Group G]` and `[IsFreeGroup G]`, every `H : Subgroup G` satisfies `IsFreeGroup H`. Its sole
direct import is `Mathlib.GroupTheory.FreeGroup.IsFreeGroup`. Checked equivalences cover both a
literal ambient `FreeGroup X` formulation and the definition-level existence of a
`FreeGroupBasis` for `H`. Four structural mutations and bottom, top, and infinite-rank boundary
specializations are validated. The proof-bearing Nielsen-Schreier module is deliberately absent.

Pinned mathlib contains the exact candidate `subgroupIsFreeOfIsFree` in
`Mathlib.GroupTheory.FreeGroup.NielsenSchreier`. `AnchorAudit.lean` checks a direct wrapper for a
literal copy of the frozen target, prints the terminal and major substrate bodies, and asks Lean for
their axiom and placeholder reports. The terminal body transports freeness along
`endMulEquivSubgroup H`; its deeper route makes the relevant action groupoid free and uses a
geodesic spanning tree to prove its vertex group free. At immutable mathlib revision
`8a178386...ea95`, Lean reports only `propext`, `Classical.choice`, and `Quot.sound` and reports all
five inspected declarations sorry-free. This is a kernel-checked `M0-W` candidate route, not
accepted proof state.

The frozen external inventory also records `dwarn/nielsen-schreier-lean@99fb30c...2ea1` and
`dwarn/nielsen-schreier-2@e51a8c65...7dbe`. They have mathematically relevant theorems but use
Lean 3.7.1 and Lean 3.27.0 with Lean 3 mathlib, have no recorded licenses, and were not replayed.
They receive no Lean 4 proof credit. Bounded repository, Sourcegraph, GitHub code, and grep.app
searches located no additional admissible Lean 4 body, but access limits mean no search-saturation
claim is made.

The provisional vector remains `[H1, M3, R4]`. `instance.json` is the structured scope authority;
`scope-map.md` and `source-statement-crosswalk.md` preserve the exact boundary; and `task-dag.json`
contains the six open dependent tasks. `statement.json`, `statement-validation.md`, and the
provisional statement and anchor receipts record scoped handoffs pending master review. The audit
candidate vector is `[H1, M0-W, R4]`, while the accepted root deliberately remains
`[H1, M3, R4]`. No H0, accepted M0, R0, accepted proof state, audit completion, theorem completion,
release, or master acceptance is claimed.
