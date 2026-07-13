# THM-M-1184 release reconciliation

Item: `S56-M-1184-RELEASE`. Base revision:
`a7c34044268bf5745e40c011134b447dd1e7cd0f`.

## Exact decision

The release verdict is `blocked`. Lifecycle remains `planned`; the accepted
root vector remains `[H3, M2, R4]`; `audit_complete=false` and
`theorem_complete=false`; no receipt or obligation is accepted.

The local proof closes weak duality only. Its final theorem
`kantorovichDuality_of_reverse` still consumes `ReverseDualityPackage`, so it
cannot close the premise-free canonical root. The minimal mathematical cut is
`M1184-S-SEPARATION`, `M1184-C-POTENTIALS`, `M1184-L-GAP`,
`M1184-W-REVERSE`, and `M1184-T-STRONG`.

The first workflow failure is dependency acceptance: validation is provisional
`[_]`, `accepted=false`, `release_grade=false`, and not master accepted. The
first theorem failure is exact-root kernel closure. The first release-assurance
failure is the cold empty-cache hermetic gate. H0, R0, full provenance and TCB,
AUDIT-Z, offline restoration, SBOM/license closure, distinct signed runners,
an independent minimal verifier, protected adversarial CI, a deterministic
release bundle, and THEOREM-Z all remain open.

## Validation surface

The release checker binds the manifest, task DAG, frozen statement and
obligation hashes, graph state, proof and validation receipts, pinned toolchain,
and clean mathlib source tree. It records that the historical validation recipe
is snapshot-bound to `3bb4cb3ae15dff8b48c93242019edec3bf858e48`
and now correctly fails its freshness assertion at the integrated release base;
that historical receipt is not rewritten or promoted.

The checker then performs a current narrow replay in a fresh temporary output
directory. Every Lean subprocess runs at `--trust=0` inside a bubblewrap
network namespace. It re-elaborates `Statement.lean`, `ObligationTree.lean`,
`Proof.lean`, `Validation.lean`, and the release-only probe
`ReleaseCheck.lean`. The conditional composition, local weak proof,
independently written same-worker weak proof, and three release probes are
sorry-free and report exactly `propext`, `Classical.choice`, and `Quot.sound`.
This is warm-cache nonrelease evidence and supplies no strong-duality or root
credit.

## Commands and results

Commands run from the repository root on 2026-07-14 (Asia/Shanghai):

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1184` | 0 | rank 169, lane `hard_mathlib_anchor_and_wrapper`, planned, theorem incomplete |
| `python3 Stage1_Instances/THM-M-1184/check_statement.py` | 0 | target expression `edb496...1cc29`; four mutations distinguished |
| `python3 Stage1_Instances/THM-M-1184/check_obligation_tree.py` | 0 | 16 obligations and 43 typed edges pass; root remains M2/open |
| `python3 Stage1_Instances/THM-M-1184/check_proof.py` | 0 | local weak package passes; reverse package and root remain open |
| `python3 -I -B Stage1_Instances/THM-M-1184/check_validation.py` | 1 | expected freshness failure: historical checker asserts base `3bb4cb3a...`, current base is `a7c34044...` |
| `python3 -I -B Stage1_Instances/THM-M-1184/check_release.py` | 0 | hashes and negative terminal decisions agree; current trust-zero network-isolated weak/conditional replay passes; release stays blocked |
| `git diff --check -- Stage1_Instances/THM-M-1184 .stage1-worker-selftest.json` | 0 | no whitespace errors |

No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was
performed. The pre-existing canonical `.lake` symlink was reused read-only.

## Status boundary

This artifact is a provisional worker receipt for an exact negative release
decision. It does not claim an accepted dependency, premise-free root proof,
E0/E1, M0, H0, R0, AUDIT-Z, THEOREM-Z, theorem completion, release, or master
acceptance.
