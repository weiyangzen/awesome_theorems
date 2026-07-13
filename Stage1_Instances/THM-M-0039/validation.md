# Intake validation record

## Boundary

This record validates only the `planned` intake for `S56-M-0039-INTAKE`. The worker clone started
at revision `d66b6e80968b53d5b99774584721ae8976f303a5` with the scheduler-provided untracked
`Formalizations/Lean/.lake` symlink to the canonical pinned dependency artifacts. The symlink and
its dependency repositories were used read-only. No Lake update, build, fetch, or clone command
was run.

The primary-source inspection constrains the candidate family but does not select an exact target.
The Lean probe declares no theorem and authenticates adjacent APIs only. In particular, it does
not define polynomial identity, formalize primitive algebra, prove finite-dimensionality over the
center, or transfer proof credit from Jacobson density or Artin-Wedderburn.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0039` | 0 | rank 1517; planned; no legacy slot; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` | 0 | initial status contained only the scheduler-provided untracked `Formalizations/Lean/.lake` symlink |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base commit `d66b6e80968b53d5b99774584721ae8976f303a5`; tree `aaa82721074fccea81033a9a18d21652af89f8e4` |
| `git blame -L 298,303 -- Docs/researches/math_theorems.md` | 0 | all six catalogue lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| official AMS PDF GET, `sha256sum`, `pdfinfo`, `pdftotext`, bounded inspection, second GET, and `cmp` | 0 | six-page 1948 primary paper inspected; both GETs matched SHA-256 `5291a8b8...1f27`; Theorem 1 is a strong candidate but catalogue correction and H0 review remain open |
| Crossref DOI metadata GET and `jq` | 0 | author, title, 1948, volume 54, issue 6, pages 575-580, and DOI confirmed; observed response SHA-256 `6c1f7792...3bd5` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | mathlib commit `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | no output; pinned mathlib worktree clean |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `cd Formalizations/Lean && lake --version` | 0 | Lake 5.0.0-src+98dc76e |
| `cd Formalizations/Lean && LC_ALL=C.UTF-8 TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0039/IntakeProbe.lean` | 0 | ten adjacent pinned interfaces elaborated; two representative axiom reports were `[propext, Classical.choice, Quot.sound]`; output SHA-256 `9ff39231...d6d5` |
| exact target-phrase `rg` recipe recorded in `intake-receipt.json` | 1 | expected no-match exit and empty output SHA-256 `e3b0c442...b855`; no local or pinned exact PI-Kaplansky theorem located |
| `python3 -m json.tool` on the three dossier JSON files | 0 | instance, open task DAG, and receipt are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0039-pycache python3 -m py_compile Stage1_Instances/THM-M-0039/check_intake.py` | 0 | scoped checker compiles without writing cache files into the repository |
| `python3 -B Stage1_Instances/THM-M-0039/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | final planned-intake identity, source/pin hashes, artifacts, receipt, packet, three replay recipes, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0039/check_intake.py` | 0 | packetless replay validates the historical intake subset without requiring the scheduler-only packet or freezing later authority state |
| prohibited Lean construct scan | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in the probe |
| per-file `git diff --no-index --check /dev/null FILE` and scoped `git diff --check` | 0 | all new owned files and the worker packet have no whitespace diagnostics; expected new-file differences were not treated as errors |

## Result

The intake is self-tested and proposes worker state `[_]` for master review. It freezes a strong
primary-source candidate, the catalogue chronology discrepancy, proposition-changing choices,
formal discovery boundary, and an open six-node DAG. The first downstream failure is the statement
gate: no independent reviewer has approved the candidate identity or a complete source-to-Lean
encoding. The root remains provisionally `[H1, M3, R4]`; no accepted receipt or proof state exists,
and `audit_complete=false` and `theorem_complete=false`.
