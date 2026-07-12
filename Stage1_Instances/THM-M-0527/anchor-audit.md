# THM-M-0527 anchor audit

Item: `S56-M-0527-ANCHOR_AUDIT`. Base revision:
`9c62e277cad936290d63af79d788d97dd17bf4cf`. Audit date: 2026-07-12.

The audited target is the elaborated pointed classification in `Statement.lean`, not the broader
phrase "covering spaces correspond to the fundamental group." Searches covered this repository,
every Lean source in the already-pinned dependency tree, and public Lean code indexed by
Sourcegraph. External source was read by immutable commit URL; no dependency update, clone, or
fetch was performed.

## Pinned mathlib findings

Mathlib at `8a178386ffc0f5fef0b77738bb5449d50efeea95` has substantial prerequisites but no exact
classification theorem. `IsCoveringMap.monodromyFunctor` associates an action-like functor to an
existing cover. `IsCoveringMap.injective_path_homotopic_map` proves the induced map is injective.
`IsCoveringMap.existsUnique_continuousMap_lifts_of_range_le` is the subgroup-range lifting
criterion and is the strongest likely uniqueness anchor. None constructs a connected cover from
an arbitrary subgroup. `Subgroup.isQuotientCoveringMap` constructs a cover only for quotients of a
topological group by a discrete subgroup, so it cannot replace the arbitrary-base root.

`AnchorAudit.lean` elaborates all four declaration names and asks Lean for their axiom reports.
Each report is exactly `[propext, Classical.choice, Quot.sound]`, with no `sorryAx`. This establishes
that these particular pinned ingredients have kernel-checkable bodies under the ordinary classical
and quotient axioms; it does not turn an ingredient into root closure or M0 proof credit.

## External Lean 4 finding

The sole close public candidate found was Facebook Research's `atlas-lean`, commit
`34ffed396f376454c1a9b297f3fd74c5c801fb50`, file
`Atlas/AlgebraicTopologyI/code/Section31.lean` (SHA-256
`089de5e4fe174cbe07aa9291dbeb4a8c885e77cc5e45db6434223db1706fb0d9`). It pins the same Lean
4.29.0 toolchain and mathlib revision and declares
`CoveringSpaces.coveringSpacesClassification : (fiberFunctor b).IsEquivalence`.

That candidate is rejected: its terminal body is literally `by sorry`. Moreover, it classifies
all covering spaces categorically by fundamental-group actions under a different semilocal
predicate; it is not the frozen quotient-free pointed connected-cover/subgroup proposition. It
cannot be imported, wrapped, or counted as an anchor proof.

## Commands and results

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique ordered targets, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0527` | 0 | rank 584; planned; theorem incomplete |
| `rg -n -i 'covering (space|map)|covering.*fundamental|fundamental.*covering|monodromyFunctor' --glob '*.lean' . Formalizations/Lean/.lake/packages` | 0 | local target plus mathlib lifting/covering ingredients; no exact root declaration |
| Sourcegraph global Lean queries for `monodromyFunctor`, lifting criterion, covering classification, `fiberFunctor`, and `CoveringSpaceOver` | 0 | mathlib plus one close external repository, `facebookresearch/atlas-lean` |
| immutable raw read of `atlas-lean@34ffed3.../Section31.lean` and `sha256sum` | 0 | classification declaration found with terminal body `by sorry`; digest recorded above |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0527/AnchorAudit.lean)` | 0 | all four pinned candidate names elaborated; each axiom report was `[propext, Classical.choice, Quot.sound]`, with no `sorryAx` |
| `(cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-0527/check_statement.py)` | 0 | canonical statement hash `4c7a7d4c...625f55d`; all three statement mutations distinguished |
| `python3 -m json.tool Stage1_Instances/THM-M-0527/anchor-audit.json >/dev/null` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0527` | 0 | no whitespace errors |

The phase audit is self-tested and pending master acceptance. The exact external closure flag is
false, machine status remains `M3`, and theorem completion remains false. The next phase must build
an obligation tree around cover construction, induced-subgroup realization, and uniqueness; it
must not treat any audited ingredient as root closure.
