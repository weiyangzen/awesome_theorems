# THM-M-0013 intake validation

Validation date: 2026-07-13, Asia/Shanghai. Base revision:
`c2467750f2cdb3960045c83e819d96687253303d`. The worktree initially contained only the
automation-provided untracked `Formalizations/Lean/.lake` symlink. It was reused read-only; no
`lake update`, build, clone, fetch, or dependency mutation was run. The run is nonrelease evidence.

## Scope and result

The intake self-test covers only the planned dossier, scope map, source-statement crosswalk, open
task DAG, input revision bindings, and a narrow pinned Lean discovery probe. The probe checks finite
and infinite Galois-correspondence API names, but the unresolved source variant prevents a canonical
Lean statement, expression fingerprint, alternate transports, or statement mutation certificate.
It neither states nor proves the target theorem.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0013` | 0 | rank 1063; planned; L0/rework_required; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short` | 0 | initial status contained only the automation-provided untracked `.lake` symlink; preserved and used read-only |
| `git blame -L 114,119 -- Docs/researches/math_theorems.md` | 0 | all six catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --silent --show-error https://www.jmilne.org/math/CourseNotes/FT.pdf -o /tmp/thm-m-0013-ft.pdf` plus `sha256sum`, `pdfinfo`, and `pdftotext` | 0 | author-hosted version 5.10 inspected from temporary storage; SHA-256 and finite/infinite locators recorded |
| `curl -L --fail --silent --show-error` on immutable Stacks `fields.tex` commit URL plus `sha256sum` and scoped `sed` | 0 | commit-pinned Tag `09DW` source and distinct infinite theorem inspected from temporary storage |
| `sha256sum` over normative, source, toolchain, lock, and probed mathlib inputs | 0 | hashes recorded in `instance.json` and `intake-receipt.json` |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0013/IntakeProbe.lean)` | 0 | eleven adjacent finite/infinite fixed-field correspondence API checks elaborated; no target theorem stated |
| `python3 -m json.tool` on the three owned JSON files and worker packet | 0 | all JSON is syntactically valid after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0013-pycache python3 -m py_compile Stage1_Instances/THM-M-0013/check_intake.py` | 0 | scoped validator compiles without writing repository bytecode |
| `python3 Stage1_Instances/THM-M-0013/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identities, planned/null-target boundary, source and pin hashes, artifact inventory, provisional packet, and six open tasks agree |
| `python3 Stage1_Instances/THM-M-0013/check_intake.py` | 0 | public replay mode passes without the scheduler-only worker packet |
| `rg -n '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0013 -g '*.lean'` | 1 | expected no-match exit; no prohibited Lean proof token or declaration |
| no-index whitespace check for all new files, then scoped `git diff --check` | 0 | no whitespace diagnostics |

Known downstream failures remain deliberately open: exact finite/infinite and clause selection;
historical primary-source and theorem-specific errata review; independent source review; canonical
Lean elaboration, transports, and mutations; exhaustive formal-candidate provenance and trust
audit; obligation and graph freezes; proof and composition; hermetic replay; deterministic release
bundle; independent verification; and master acceptance. They prevent theorem completion but do
not invalidate the truthful `planned` intake.
