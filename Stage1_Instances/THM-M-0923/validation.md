# Intake validation

Base revision: `fb0baac89ea0633612be3b47448464b4b8e4bef7` (tree
`018557070da18ea1733a82de81a238750c59aa84`).

Commands were run from the repository root on 2026-07-13 (Asia/Shanghai). The automation-provided
`Formalizations/Lean/.lake` symlink was present before the work and was used read-only. No `lake
update`, `lake build`, dependency fetch/clone, or `.lake` mutation was performed. This dirty worker
snapshot is nonrelease evidence.

## Source and environment inspection

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0923` | 0 | rank 1465; planned; L0; no legacy slot; theorem incomplete |
| `git status --short --untracked-files=all` | 0 | initially only the pre-existing automation `.lake` symlink was untracked |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree above |
| `git blame -L 6749,6754 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa...`; no later source refinement |
| `curl -L --fail --max-time 30 -sS https://dlmf.nist.gov/26.7 -o /tmp/dlmf-26.7.html` | 0 | observed DLMF 1.2.7 Bell-number section; 79724 bytes; SHA-256 `8941e6f1...d833c` |
| six analogous DLMF equation-TeX requests for `26.7.E1` through `26.7.E6` | 0 | captured zero case, Stirling sum, finite Dobinski form, Dobinski formula, generating function, and recurrence; exact hashes are in the instance |
| Crossref query for DOI `10.1080/00029890.1934.11987615` | 0 | confirmed E. T. Bell, *Exponential Numbers*, 1934, journal/volume/issue/pages; response SHA-256 `101f1591...a1376` |
| publisher and JSTOR PDF requests for the Bell article | 22 | expected access blockers (HTTP 403 and 420); no article body was inspected or credited |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3...`, x86_64 Linux |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned mathlib revision `8a178386...` and tree `bdc39a31...` |
| bounded exact-topic inspection of pinned `Bell.lean` and `Stirling.lean` | 0 | found recursive candidates and explicit Bell counting-correspondence TODOs; no cardinality theorem was credited |

The DLMF HTML digest is observation provenance, not an immutable source identity: the response
included dynamic delivery material. The equation TeX endpoints and Crossref response likewise are
discovery inputs, not accepted proof archives. Failed article access grants no evidence.

## Final scoped checks

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0923/IntakeProbe.lean` | 0 | Bell/Stirling definitions and recurrence candidates elaborated; trust reports printed; stdout SHA-256 `941402c6...457a` |
| `python3 -m json.tool Stage1_Instances/THM-M-0923/instance.json >/dev/null` | 0 | instance JSON parsed |
| `python3 -m json.tool Stage1_Instances/THM-M-0923/task-dag.json >/dev/null` | 0 | open DAG JSON parsed |
| `python3 -m json.tool Stage1_Instances/THM-M-0923/intake-receipt.json >/dev/null` | 0 | provisional receipt JSON parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0923-pycache python3 -m py_compile Stage1_Instances/THM-M-0923/check_intake.py` | 0 | scoped validator compiled without adding owned generated files |
| `python3 -B Stage1_Instances/THM-M-0923/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target identity, H5/M3/R4 boundary, null target, exact inventory, worker packet, mathlib TODO boundary, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0923/check_intake.py` | 0 | public replay mode passes without the root worker packet |
| scoped Lean scan for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declarations | 1 | expected no-match; the probe contains no prohibited declaration |
| no-index newline, CR, NUL-byte, and trailing-whitespace checks for all nine owned files and `.stage1-worker-selftest.json` | 0 | no diagnostics |
| `git diff --check -- Stage1_Instances/THM-M-0923 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics; the explicit newline/CR/NUL/trailing-whitespace loop covers untracked files |

The Lean probe proves only that the pinned candidate declarations elaborate. Its axiom report says
`Nat.bell_succ` and `Multiset.bell_mul_eq` use `propext`, `Classical.choice`, and `Quot.sound`, while
`Nat.stirlingSecond_succ_succ` reports no axioms. These are candidate trust observations, not an
axiom audit of an absent canonical target.

## Boundary

These checks self-test the `planned` intake node only. They do not select a truth-valued Bell-number
proposition, establish a partition-cardinality interpretation, create an exact target or expression
fingerprint, or validate a proof. Source selection, all six dependent tasks, master acceptance,
audit completion, and theorem completion remain open.
