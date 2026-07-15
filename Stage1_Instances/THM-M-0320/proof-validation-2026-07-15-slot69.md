# S56-M-0320-PROOF worker validation

Item: `S56-M-0320-PROOF`

Base revision: `443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b`

## Proof result

`Proof.lean` now proves the frozen `ClosedGraphKakutaniCore` and the exact canonical
`KakutaniFixedPointTarget`. The construction uses a continuous convex selection of epsilon-enlarged
values, a Brouwer-derived compact-convex Schauder theorem, fixed-size Caratheodory packages, a
compact subsequence, and the frozen closed-graph bridge. `root_of_closedGraph_packages` checks the
final child-to-parent composition.

The Brouwer terminal is not the unlicensed Harfe source recorded by the old blocker. It is the
repository's existing MIT-licensed `math-xmum/Brouwer@c02205edf347ad45f0d62db85497598ba2c4291e`
source closure. `brouwer-source.json` pins all three source hashes, upstream revision/tree/archive,
license, and the read-only cross-target dependency boundary. No file under `THM-M-0318` was changed.

## Commands and results

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0320` | 0 | Rank 686; planned; theorem incomplete. |
| `bash Stage1_Instances/THM-M-0320/check_proof.sh` | 3 | Fail-closed before compilation: `lake env` found the shared canonical `.lake/packages/flt-regular` artifact with `HEAD` at `refs/heads/.invalid`. The checker did not fetch, update, build, remove, or modify `.lake`. |
| Raw pinned-Lean isolated replay described below | 0 | Fresh temporary source copies of the exact statement, obligation tree, graph bridge, three MIT vendor modules, source wrapper, and proof compiled with `--trust=0 -t0`; `kakutaniFixedPoint` reported exactly `[propext, choice, Quot.sound]`; three declarations passed `assert_no_sorry`. |
| Isolated temporary-project `lake env lean --trust=0 -t0 -R <tmp> <tmp>/Proof.lean` recheck | 0 | Lake selected `leanprover/lean4:v4.29.0`; the exact proof reported `[propext, choice, Quot.sound]` and three sorry-free declarations; output SHA-256 `fa7258c8ee3a47b979606ade83d089781605a6ec5ae3eae1d07aee56e1d8544f`. |
| `python3 Stage1_Instances/THM-M-0320/check_obligation_tree.py` | 0 | 10 frozen obligations and 22 typed edges passed; the unchanged pre-proof graph still reports the root open. |
| `python3 Stage1_Instances/THM-M-0320/check_proof.py` | 0 | Item, exact declarations, source hashes, license, prohibited constructs, receipt, and worker packet passed. |
| `python3 -m json.tool` on the three new JSON artifacts | 0 | All structured artifacts parsed. |
| `git diff --check -- Stage1_Instances/THM-M-0320 .stage1-worker-selftest.json` | 0 | No whitespace diagnostics. |

The successful raw replay used the already installed pinned Lean binary
`~/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean` and the pinned `LEAN_PATH` captured by a
prior successful `lake env printenv LEAN_PATH` in this same canonical dependency closure. It staged
only temporary copies and wrote no olean under the owned target or `.lake`. This is real kernel
evidence. A second temporary Lake project independently selected the same installed toolchain and
ran `lake env lean` against those fresh outputs. The integration lane must still repeat the
repository-owned `check_proof.sh` after restoring the missing pinned `flt-regular` artifact.

## Status boundary

This is proof-node evidence proposing only `[_]`. The exact root is kernel inhabited without
placeholders, but no authoritative obligation or debt-vector state changes here. Predecessor/master
acceptance, graph reconciliation, full foundation and trust review, H0, R0, cold hermetic replay,
independent validation, release, `AUDIT-Z`, and `THEOREM-Z` remain open. Therefore
`theorem_complete=false`.
