# THM-M-1522 obligation-tree validation

Item: `S56-M-1522-OBLIGATION_TREE`. Base revision:
`121922f67a878912b6465e89e536f16ae090bf8f`.

## Frozen result

Registry version 1 contains 16 unique semantic obligations and has denominator SHA-256
`8a9a7f243137efb0ac3ebafe2b5de3a292f41bcb0cc6bdc4a1a6adc364fb3242`.
The seven separate graph families contain 32 directed typed edges, including reciprocal
`proof_requires`/`composes` pairs. All machine-required nodes are reachable from the root through
proof or refinement edges, and every node carries the complete rev-5.6 schema and a substantive
ledger no larger than 100 steps or an explicit `split-required` marker.

The Lean check creates a temporary `Statement.olean` outside the repository with the pinned Lean
binary and Lake-derived `LEAN_PATH`, then elaborates `ObligationTree.lean` against it. The temporary
directory is automatically removed. No `.lake` dependency or repository build artifact is changed.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1522/build_obligation_artifacts.py` | 0 | deterministically wrote 16 obligations and both JSON artifacts; denominator hash above |
| `python3 Stage1_Instances/THM-M-1522/check_obligation_tree.py` | 0 | registry/schema/eligibility/hash, reciprocal typed edges, DAG reachability, cut set, and scoped Lean composition passed; 32 edges |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered rework-required targets passed |
| `python3 scripts/stage1_target.py show THM-M-1522` | 0 | rank 190, planned, L0/rework-required, theorem incomplete |
| `python3 -m json.tool` on both generated JSON files | 0 | both structured artifacts parsed |
| `git diff --check -- Stage1_Instances/THM-M-1522 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The first attempted scoped Lean run failed because importing sibling `Statement` requires an
`.olean` on `LEAN_PATH`; no repository file was created by that attempt. The final validator makes
that prerequisite explicit and ephemeral. `#print axioms` reports only `propext` for the conditional
composition lists `propext`, `Classical.choice`, and `Quot.sound`, with no `sorryAx`.

## Status boundary

This self-tests only the obligation-tree phase. The checked composition assumes the two open
substantive packages. The remaining root cut set is `M1522-L-POINTWISE` and
`M1522-T-IDENTIFY`; root debt stays `M3`. There is no pointwise proof, accepted master receipt,
H0 source claim, validation/release evidence, or theorem-completion claim.
