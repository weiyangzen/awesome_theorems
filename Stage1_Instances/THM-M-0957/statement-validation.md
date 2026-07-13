# THM-M-0957 statement validation

Item: `S56-M-0957-STATEMENT`

Base revision: `b56df790fc94c5366cf919a6fe5411d06b427c59`

Base tree: `18ba629d4c00333f6e17018905f4fbd30558bb4c`

## Frozen target

`Stage1Instances.THM_M_0957.BehrendConstructionTarget` formalizes the displayed lower bound in
Behrend's 1946 note. For every positive real `epsilon`, there is a natural threshold `N0` such that
every `N >= N0` satisfies

`N ^ (1 - (2 * sqrt (2 * log 2) + epsilon) / sqrt (log N)) < rothNumberNat (N + 1)`.

The addition of one is deliberate: the source's extremal function ranges over the inclusive
interval of nonnegative integers at most `N`, while mathlib's `rothNumberNat n` ranges over
`Finset.range n`. The target retains positive epsilon, an epsilon-dependent threshold, strict
inequality, and the historical constant. `Real.log` selects natural logarithm, and the real base
and exponent select `Real.rpow`. The transcription and log-convention mapping still await H0
source review; this statement phase does not claim that review.

`SourceThreeAPFree` literally excludes pairwise-distinct natural `a`, `b`, and `c` satisfying
`a + c = b + b`. The checked `sourceThreeAPFree_iff_threeAPFree` proves exact agreement with
mathlib's predicate over `Nat`. The second checked iff converts the Roth-extremum root into a
direct `Finset Nat` existence claim with the same inclusive interval, source predicate, and strict
cardinality bound.

The direct imports are exactly `Mathlib.Analysis.SpecialFunctions.Pow.Real` and
`Mathlib.Combinatorics.Additive.AP.Three.Defs`. Deleting either makes the complete statement and
transport module fail, and separately makes an isolated canonical-target fixture fail. These are
substantive missing-vocabulary failures, not merely loss of the `Mathlib` module root. The proof-bearing
`Mathlib.Combinatorics.Additive.AP.Three.Behrend` module is deliberately absent, so this phase does
not inspect or credit the known formal proof candidate.

## Commands and results

All commands ran in this worker clone on 2026-07-13 (`Asia/Shanghai`). Lean reused the
automation-provided canonical pinned `.lake` artifacts read-only. No update, build, clone, fetch,
or dependency mutation was run.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0957` | 0 | rank 1491; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake `5.0.0-src+98dc76e` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package status | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`, clean package worktree |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0957/Statement.lean` | 0 | canonical root, two alternate forms and checked iff transports, four expected equality rejections, axiom reports, and fully explicit target elaborated; stdout SHA-256 `9c4ff578770208d5ab77deb4fb75aec7273c396ec590d4fa151c43dc4f7c8e7e` |
| `cd Formalizations/Lean && python3 -B ../../Stage1_Instances/THM-M-0957/check_statement.py` | 0 | root expression SHA-256 `e611db43ce6f3419553e3ebe0fe85a3ce89e4d3930b3842f5a09be8a7683d2ed`; bundle `dd54684a60e69f61c8feaf6588eae6a1c9aa5931b5f68297badf39e72aed6671`; source `b4bda6c926b0568d8b244623c12b4784651d55a9eb7df9d9ba3f512ed2cd9e46`; both import deletions failed in isolated-target and complete-module fixtures, and all four mutation expressions differed |
| `python3 -B Stage1_Instances/THM-M-0957/check_statement_artifacts.py` | 0 | fresh elaboration, metadata, global authority and target-local intake hashes, direct-import hashes, provisional receipt, pinned mathlib cleanliness, and worker handoff agree |
| `python3 -m json.tool` on `statement.json`, `statement-receipt.json`, and `.stage1-worker-selftest.json`; Python syntax checks | 0 | all structured statement artifacts parse; the checker compiles without adding cache files to the owned path |
| prohibited-construct scan over `Statement.lean` | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-file `git diff --no-index --check /dev/null` for each new statement artifact and worker packet | 0 aggregate | no whitespace diagnostic; no-index exit 1 per new file is only the expected file difference |

The historical intake-only checker is not statement evidence: it freezes the older null-target
artifact inventory and pre-integration authority hashes. It was neither modified nor used to
validate this phase.

## Mutation and trust boundary

The four mutations remove `0 < epsilon`, change epsilon from `Real` to `Rat`, move the threshold
outside the epsilon binder, or replace the inclusive interval by `rothNumberNat N`. Lean rejects
definitional equality with the canonical target, and the checker separately compares normalized,
fully explicit right-hand-side expressions. These are statement-identity tests, not assertions
that each changed proposition is mathematically false.

The predicate iff reports only `propext`; the extremal/direct-set iff reports only `propext`,
`Classical.choice`, and `Quot.sound`. No custom axiom, placeholder, unsafe declaration, oracle,
target proof, or imported Behrend proof is present.

This is a provisional statement-node self-test. The intake dependency and this phase require
dependency-ordered master acceptance. Immutable source admission, H0 review, anchor and proof-body
audit, obligation registry, typed graphs, proof, composition, readable reconstruction, hermetic
replay, independent verification, release, audit completion, and theorem completion remain open.
