# THM-M-1078 obligation-tree validation

Item: `S56-M-1078-OBLIGATION_TREE`  
Base revision: `dfacb54b5f277adf642e7658a065015f486d4cf2`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

The registry freezes 15 canonical obligations: 13 semantic machine obligations and two
informational source/provenance overlays. The selected route integrates the audited immutable
Burkholder candidate only after explicit obligations for dependency pinning, transform indexing,
predictability, pointwise-to-a.e. bounds, finite-measure inference, norm codomain conversion, and
the candidate's stronger all-time `MemLp` premise. None of those differences is hidden in a
generic wrapper node.

All leaves have four substantive ledger steps, below the 100-step split threshold. The structural
validator recomputed denominator SHA-256
`f7a3b25e4d46cf0e67ad09199b7b4035216a1bc5acc4b2c6f7c21fd07e63c73e`, checked the one-to-one
registry/node map, all seven graph types, reciprocal edge indexes, root reachability, leaf budgets,
readable anchors, statement hash, and fail-closed closure record. There are 51 typed edges.

The Lean check concatenated the already elaborated `Statement.lean` text with the conditional
composition module in a temporary file. This both avoids creating an untracked olean in the owned
path and checks that the local composition target is definitionally identical to the exact frozen
target. `root_of_allTimeMemLpTransformBound` consumes two open propositions; it proves neither the
external body nor the earlier-time integrability bridge. Its reported axioms were `propext`,
`Classical.choice`, and `Quot.sound`, with no `sorryAx`.

No dependency update, fetch, clone, build, or `.lake` mutation was performed.

## Commands and exact outcomes

| Command | Exit | Outcome |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1078/build_obligation_artifacts.py` | 0 | wrote 15 obligations; denominator digest `f7a3b25e...63c73e` |
| `python3 Stage1_Instances/THM-M-1078/check_obligation_tree.py` | 0 | `PASS THM-M-1078 obligation tree: 15 obligations, 51 typed edges`; root open M2 |
| `python3 -m json.tool Stage1_Instances/THM-M-1078/obligation-registry.json >/dev/null` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1078/typed-graphs.json >/dev/null` | 0 | valid JSON |
| `bash Stage1_Instances/THM-M-1078/check_exact_composition.sh` | 0 | conditional composition and exact target equivalence elaborated; no `sorryAx` in printed axioms |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets and ranks passed |
| `python3 scripts/stage1_target.py show THM-M-1078` | 0 | rank 520, planned, L0/rework-required, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1078 .stage1-worker-selftest.json` | 0 | no whitespace errors |

Validated content hashes:

```text
2fec28e7bf3090e35ec0ab350e723a2eba7faacdd62db57d8536d7c7753263cd  obligation-registry.json
cf7e8839f6ef5c34f0f6ec7345fd823c29dad2d37b2ff48d4d64aedbb4ef55c1  typed-graphs.json
128d1eb0ff0387be4ffdd2c384a916eba14ab2855b414d610f71c6949b1d89fc  ObligationTree.lean
24aaa7ddc3b30e6db201f3c93bd72d9fb1edbfc6ce878d3007fef980bc849edf  check_exact_composition.sh
```

## Status boundary

This self-test establishes only the architecture freeze. All 13 semantic obligations remain open
and the root remains `M2`. The first critical cut is `M1078-C-EXTERNAL-PIN`,
`M1078-T-ALLTIME`, `M1078-B-PREDICTABLE`, and `M1078-B-NORM`. There is no integrated external
proof body, exact wrapper, accepted composition certificate, H0/R0 review, audit completion, or
theorem completion. Master acceptance remains required.
