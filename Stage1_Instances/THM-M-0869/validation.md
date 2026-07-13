# Intake validation

## Environment and boundary

- Validation date: `2026-07-13`, timezone `Asia/Shanghai`.
- Base revision/tree: `748243faadc15828fb087059337fd05b7be9fdeb` /
  `e46d642646f80980838b6f016f5d69b817bd464d`.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`.
- Platform: Linux `7.0.0-27-generic`, `x86_64`.
- The automation-provided `Formalizations/Lean/.lake` symlink was the only pre-existing untracked
  path. It and the pinned dependency worktree were used read-only. No `lake update`, `lake build`,
  dependency clone/fetch, or `.lake` mutation ran.
- This is nonrelease evidence from an inherited worker environment. It makes no cold-cache,
  hermetic, independent-runner, signed-attestation, or release claim.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard structure passed: 15 assurance groups and 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required. |
| `python3 scripts/stage1_target.py show THM-M-0869` | 0 | Rank 1423; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false. |
| `git status --short --untracked-files=all` before edits | 0 | Only the pre-existing `Formalizations/Lean/.lake` link appeared. |
| `git rev-parse HEAD HEAD^{tree}` | 0 | Base revision and tree matched the environment record above. |
| `git blame -L 6369,6374 -- Docs/researches/math_theorems.md` | 0 | All six catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. |
| `lake env lean --version` in `Formalizations/Lean` | 0 | Lean 4.29.0 at the recorded commit and target. |
| `lake --version` in `Formalizations/Lean` | 0 | Lake 5.0.0 at the recorded Lean version. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | Pinned revision and tree matched the environment record. |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short --untracked-files=all` | 0 | No output; the pinned mathlib worktree remained clean. |
| `lake env lean ../../Stage1_Instances/THM-M-0869/IntakeProbe.lean` in `Formalizations/Lean` | 0 | Seven adjacent ordinary/induced containment interfaces elaborated. Complete stdout was 1153 bytes with SHA-256 `61d62ae40b39e2759ffafd0922c1129200e982a1aabca4e47143c5575ef674d5`; stderr was empty. No target theorem or proof body was declared. |
| bounded exact-topic search over pinned mathlib, repo-local Lean, and this dossier | 1 (expected no match) | No generic forbidden graph-class characterization declaration matched; intake discovery only, not a complete anchor audit. |
| bounded minor/contraction search in pinned `Mathlib/Combinatorics/SimpleGraph` | 1 (expected no match) | No simple-graph minor/contraction interface matched; not a global absence claim. |
| `python3 -m json.tool` over all structured dossier files and the worker packet | 0 | All JSON serialized and parsed successfully. |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0869-pycache python3 -m py_compile Stage1_Instances/THM-M-0869/check_intake.py` | 0 | The scoped checker compiled without writing generated files under the owned path. |
| `python3 -B Stage1_Instances/THM-M-0869/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | Manifest/DAG identity, H5/M4/R4 planned boundary, null target, source and artifact hashes, packet agreement, blocker, and six open tasks passed. |
| `python3 -B Stage1_Instances/THM-M-0869/check_intake.py` | 0 | Public replay mode passed without the scheduler-only packet. |
| prohibited-construct scan over owned Lean files | 1 (expected no match) | No `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration. |
| per-file `git diff --no-index --check /dev/null` plus `git diff --check` | 0 aggregate | No whitespace diagnostics; no-index checks cover the untracked files. |

## Validated scope

The checks validate only a `planned` theorem dossier, scope map, source-statement crosswalk,
explicit statement blocker, open downstream task DAG, repository/source fingerprints, and a
discovery-only pinned Lean API probe. The API signatures establish that adjacent containment
interfaces elaborate; they do not select or prove the catalog target.

The canonical human statement and Lean expression remain null. Primary-source selection and
independent review, exact statement elaboration and mutations, formal anchor audit, discovery and
obligation registries, typed graphs, proof, composition, axiom/provenance trust closure, readable
reconstruction, hermetic replay, deterministic evidence bundle, and independent verification all
remain open.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0869-INTAKE` only. It supports a truthful
`planned` intake proposal, not an accepted receipt. The intake awaits integration-lane master
acceptance, while the first theorem gate remains the unresolved exact statement. `audit_complete`
and `theorem_complete` are false; no H0, M0, R0, proof, accepted state, or downstream completion is
claimed.
