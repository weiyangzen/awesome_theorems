# THM-M-0079 rev-5.6 statement dossier

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

Pinned mathlib contains the unusually close candidate `subgroupIsFreeOfIsFree` in
`Mathlib.GroupTheory.FreeGroup.NielsenSchreier`. `IntakeProbe.lean` checks its exact exposed type,
elaborates a candidate application, and prints its reported axioms. This makes a future `M0-W`
route credible. The intake probe itself supplies no statement identity or proof credit; the new
statement artifacts freeze the expression but do not authenticate the candidate's full provenance
and trust closure or install an accepted proof wrapper. The root remains `M3` and all downstream
phases remain open.

The provisional vector remains `[H1, M3, R4]`. `instance.json` is the structured scope authority;
`scope-map.md` and `source-statement-crosswalk.md` preserve the exact boundary; and `task-dag.json`
contains the six open dependent tasks. `statement.json`, `statement-validation.md`, and the
provisional statement receipt record the scoped handoff pending master review. No H0, M0, R0,
accepted statement state, accepted proof state, audit completion,
theorem completion, release, or master acceptance is claimed.
