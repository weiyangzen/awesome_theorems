# Intake validation

Base revision: `62fad55ced807fdc06921c45d6fcd1f9ad86a1c2` (tree
`9d7c8fe49a4c859d90f3069dc47973ffc5ced768`).

Commands were run from the repository root on 2026-07-13 (Asia/Shanghai). The automation-provided
`Formalizations/Lean/.lake` symlink was present before the work and was used read-only. No `lake
update`, `lake build`, dependency fetch/clone, or `.lake` mutation was performed. This dirty worker
snapshot is nonrelease evidence.

## Source and environment inspection

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1601` | 0 | rank 1221; planned; L0; no legacy slot; theorem incomplete |
| `git status --short --untracked-files=all` | 0 | initially only the pre-existing automation `.lake` symlink was untracked |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree above |
| `git blame -L 11791,11796 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa...`; no later source refinement |
| `curl -L --retry 8 --retry-all-errors --fail --silent --show-error --max-time 600 https://www.cs.cmu.edu/~odonnell/hits09/gentry-homomorphic-encryption.pdf -o /tmp/thm-m-1601-intake/gentry-stoc09.pdf` | 0 | retrieved a publicly hosted copy of the STOC 2009 primary paper from a CMU course page for discovery only; 612271 bytes, 10 pages, SHA-256 `ac2bf30d...b78a8` |
| `pdftotext -layout /tmp/thm-m-1601-intake/gentry-stoc09.pdf /tmp/thm-m-1601-intake/gentry-stoc09.txt` | 0 | extracted text SHA-256 `c58d3528...0497`; inspected pp.169-172 and 177 |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3...`, x86_64 Linux |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned mathlib revision `8a178386...` and tree `bdc39a31...` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | no output; pinned mathlib source was clean |
| bounded case-insensitive `rg` for homomorphic encryption, FHE, ciphertext, cryptosystem, encrypt, and decrypt in pinned mathlib and repo-local Lean | 0 | only an unrelated prose occurrence of "decrypting"; discovery-only lexical search, not an exhaustive anchor audit |

## Final scoped checks

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1601/IntakeProbe.lean` | 0 | seven generic operation-preservation and commuting-diagram APIs elaborated; stdout SHA-256 `b7a18d02...c4dd` |
| `python3 -m json.tool Stage1_Instances/THM-M-1601/instance.json >/dev/null` | 0 | instance JSON parsed |
| `python3 -m json.tool Stage1_Instances/THM-M-1601/task-dag.json >/dev/null` | 0 | open DAG JSON parsed |
| `python3 -m json.tool Stage1_Instances/THM-M-1601/intake-receipt.json >/dev/null` | 0 | provisional receipt JSON parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1601-pycache python3 -m py_compile Stage1_Instances/THM-M-1601/check_intake.py` | 0 | scoped validator compiled without adding owned generated files |
| `python3 -B Stage1_Instances/THM-M-1601/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target identity, planned H5/M4/R4 boundary, null target, exact file inventory, worker packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-1601/check_intake.py` | 0 | public replay mode passes without the root worker packet |
| scoped Lean scan for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declarations | 1 | expected no-match; the probe contains no prohibited declaration |
| no-index whitespace check for all nine owned files and `.stage1-worker-selftest.json` | 0 | no whitespace diagnostics |
| `git diff --check -- Stage1_Instances/THM-M-1601 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics |

An exploratory probe referenced the nonexistent name `Function.Semiconj₂.comp_right` and exited 1.
Inspection of the pinned source showed that the actual composition theorem is
`Function.Semiconj₂.comp`; the probe was corrected without broadening imports, and the final command
above passed. The exploratory failure grants no evidence.

## Boundary

These checks self-test the `planned` intake node only. They do not select an exact homomorphic-
encryption proposition, establish minimal imports for a canonical target, create an expression
fingerprint, or validate any proof. The source-selection blocker, all six dependent tasks, master
acceptance, audit completion, and theorem completion remain open.
