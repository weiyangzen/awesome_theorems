# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9` (tree
`829a47c47ae831cada4f8acc6c2c00ba5883215e`).

Commands were run from the repository root on 2026-07-13 (Asia/Shanghai). The automation-provided
`Formalizations/Lean/.lake` symlink was present before the work and was used read-only. No `lake
update`, `lake build`, dependency fetch/clone, or `.lake` mutation was performed. This dirty worker
snapshot is nonrelease evidence.

## Source and environment inspection

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1593` | 0 | rank 1019; planned; L0; no legacy slot; theorem incomplete |
| `git status --short` | 0 | initially only the pre-existing automation `.lake` symlink was untracked |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree above |
| `git blame -L 11735,11740 -- Docs/researches/math_theorems.md` | 0 | all six catalog lines originate at `bcf3f9fa...`; no citation or later source refinement |
| `curl -L --fail --max-time 30 -A Mozilla/5.0 -sS https://web.stanford.edu/class/ee388/papers/ldpc.pdf -o /tmp/ldpc-research/ldpc.pdf` | 0 | retrieved an external Gallager monograph scan for discovery only; 647387 bytes, 90 pages, SHA-256 `3ce9a28b...c7e0` |
| Crossref queries for `10.7551/mitpress/4347.001.0001` and `10.1109/TIT.1962.1057683` | 0 | confirmed the 1963 MIT Press monograph and 1962 IRE article metadata; response hashes are in the receipt |
| Semantic Scholar metadata query for the 1962 DOI | 0 | abstract distinguishes several different distance, ML-decoding, iterative-decoding, complexity, and experimental claims |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3...`, x86_64 Linux |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned mathlib revision `8a178386...` and tree `bdc39a31...` |
| bounded `rg` for `LDPC`, `low-density parity-check`, and `parity-check code` in pinned mathlib and repo-local Lean | 1 | expected no-match; discovery-only lexical search, not an exhaustive anchor audit |

## Final scoped checks

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1593/IntakeProbe.lean` | 0 | seven generic Hamming and matrix APIs elaborated; stdout SHA-256 `4ca1b5ba...d50f` |
| `python3 -m json.tool Stage1_Instances/THM-M-1593/instance.json >/dev/null` | 0 | instance JSON parsed |
| `python3 -m json.tool Stage1_Instances/THM-M-1593/task-dag.json >/dev/null` | 0 | open DAG JSON parsed |
| `python3 -m json.tool Stage1_Instances/THM-M-1593/intake-receipt.json >/dev/null` | 0 | provisional receipt JSON parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1593-pycache python3 -m py_compile Stage1_Instances/THM-M-1593/check_intake.py` | 0 | scoped validator compiled without adding owned generated files |
| `python3 Stage1_Instances/THM-M-1593/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target identity, planned H1/M4/R4 boundary, null target, exact file inventory, worker packet, and six open tasks agree |
| `python3 Stage1_Instances/THM-M-1593/check_intake.py` | 0 | public replay mode passes without the root worker packet |
| scoped Lean scan for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declarations | 1 | expected no-match; the probe contains no prohibited declaration |
| no-index whitespace check for all nine owned files and `.stage1-worker-selftest.json` | 0 | no whitespace diagnostics |
| `git diff --check -- Stage1_Instances/THM-M-1593 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics |

The first Lean probe attempt included `#check ZMod 2` under the two declared imports and failed with
`Unknown identifier ZMod`. That line was removed rather than adding an unnecessary import to this
discovery-only probe; the corrected final command above passed. The failure grants no evidence.

## Boundary

These checks self-test the `planned` intake node only. They do not select an exact LDPC proposition,
establish minimal imports for a canonical target, create an expression fingerprint, or validate any
proof. The source-selection blocker, all six dependent tasks, master acceptance, audit completion,
and theorem completion remain open.
