# Intake validation

Base revision: `62fad55ced807fdc06921c45d6fcd1f9ad86a1c2` (tree
`9d7c8fe49a4c859d90f3069dc47973ffc5ced768`).

Commands were run from the worker-clone root on 2026-07-13 (Asia/Shanghai). The
automation-provided `Formalizations/Lean/.lake` symlink existed before this work and was used read
only. No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was performed.
This dirty worker snapshot is nonrelease evidence.

## Source and environment inspection

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1600` | 0 | rank 1220; planned; L0; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` | 0 | preflight contained only the automation-provided untracked `.lake` symlink |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree above |
| `git blame -L 11784,11789 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at `bcf3f9fa...`; no citation or proposition was added later |
| author-hosted GMR journal scan retrieval and visual inspection | 0 | 23 scanned pages, 18965960 bytes, SHA-256 `17b24f25...10222`; Sections 2.2 and 3.1-3.3 plus Theorems 1 and 2 distinguish several candidate roots |
| Crossref queries for `10.1137/0218012` and `10.1145/22145.22178` | 0 | confirmed journal and STOC bibliographic metadata; response hashes are recorded in `instance.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 commit `98dc76e3...`; Lake 5.0.0-src+98dc76e |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned mathlib revision `8a178386...`, tree `bdc39a31...` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned package source clean |
| `rg -n -i 'zero[- ]knowledge\|knowledge complexity\|interactive protocol\|computational indistinguish' Formalizations/Lean Stage1_Instances --glob '*.lean' --glob '!Formalizations/Lean/.lake/**' --glob '!Stage1_Instances/THM-M-1600/**'` and the same pattern under pinned `Mathlib` | 1 | expected no-match for both bounded searches; discovery-only lexical result, not an exhaustive anchor audit |

## Final scoped checks

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-1600/IntakeProbe.lean` | 0 | six generic language, polynomial-time, PMF, and superpolynomial-decay interfaces elaborated; stdout SHA-256 `bd87c72a...dba5` |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all four JSON artifacts parsed after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1600-pycache python3 -m py_compile Stage1_Instances/THM-M-1600/check_intake.py` | 0 | scoped validator compiled without creating files in the owned path |
| `python3 -B Stage1_Instances/THM-M-1600/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, planned H5/M4/R4 boundary, null target, source/dependency pins, artifact hashes, worker packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-1600/check_intake.py` | 0 | public replay mode passed without the root worker packet |
| scoped Lean scan for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declarations | 1 | expected no-match; the discovery-only probe contains no prohibited declaration |
| no-index whitespace checks for all nine owned files and `.stage1-worker-selftest.json` | 0 | every expected new-file difference had empty whitespace diagnostics |
| `git diff --check -- Stage1_Instances/THM-M-1600 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics |

## Boundary

These checks self-test only a `planned` intake. They do not select an exact zero-knowledge
proposition, establish a canonical Lean target or expression fingerprint, run statement mutations,
or validate a proof. Source selection and independent review, all six dependent phases, master
acceptance, audit completion, and theorem completion remain open.
