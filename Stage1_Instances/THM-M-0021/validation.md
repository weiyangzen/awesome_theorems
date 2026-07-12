# Intake validation

Base revision: `f608e06dccf2e158f1d2feeadb48f1b64d296cdd` (tree
`c0e4ab057a962cd2020342a692d39952f65d8bec`).

All commands ran from the isolated worker clone on 2026-07-13. Initial status contained unrelated
pre-existing edits in `Stage1_Instances/THM-M-1360/statement-blocker.json` and
`Stage1_Instances/THM-M-1360/statement-blocker.md`, plus the automation-provided untracked
`Formalizations/Lean/.lake` symlink. They were preserved. The shared canonical pinned `.lake`
artifacts were used read-only; no update, build, fetch, clone, or dependency mutation was run.

Validation covers manifest membership, planned-dossier structure, JSON integrity, a narrow pinned
Lean API probe, prohibited-token hygiene, and whitespace. Because the catalog does not identify a
truth-valued proposition, it establishes no canonical statement, expression fingerprint, mutation
certificate, source acceptance, or proof.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0021` | 0 | rank 1068; planned; L0/rework_required; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short` | 0 | recorded the two unrelated THM-M-1360 edits and automation `.lake` symlink before owned work |
| `git blame -L 170,175 -- Docs/researches/math_theorems.md` | 0 | all six catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `git blame -L 3103,3108 -- Docs/researches/math_theorems.md` | 0 | the identical duplicate record has the same origin |
| `sha256sum` over normative, source, toolchain, lock, and probed mathlib inputs | 0 | hashes recorded in `instance.json` and `intake-receipt.json` |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0021/IntakeProbe.lean)` | 0 | eight adjacent number-field invariant and generic-filter API checks elaborated; no target theorem stated |
| `rg -ni 'brauer.?siegel\|brauer_siegel' Formalizations/Lean/.lake/packages/mathlib/Mathlib -g '*.lean'` | 1 | expected no-match exit; bounded pinned-mathlib name search only, not a full anchor audit |
| `python3 -m json.tool Stage1_Instances/THM-M-0021/instance.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0021/task-dag.json` | 0 | valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0021-pycache python3 -m py_compile Stage1_Instances/THM-M-0021/check_intake.py` | 0 | scoped intake validator compiles without writing into the repository |
| `python3 Stage1_Instances/THM-M-0021/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identities, planned/null-target boundary, all recorded input hashes and revisions, exact artifact inventory, provisional packet, and six open tasks agree |
| `python3 Stage1_Instances/THM-M-0021/check_intake.py` | 0 | public replay mode passes without the scheduler-only root packet |
| `rg -n '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0021 -g '*.lean'` | 1 | expected no-match exit; no prohibited Lean declaration or proof token |

Final JSON, scoped invariants, provisional packet linkage, and whitespace checks are recorded after
receipt finalization in `intake-receipt.json`. Known downstream failures remain deliberately open:
pinpoint source inspection and independent review; exact family, hypotheses, normalization, and
conclusion selection; canonical Lean elaboration and mutation tests; discovery and obligation
freezes; candidate and provenance audit; proof and composition; hermetic replay; deterministic
release bundle; and independent master acceptance. They prevent theorem completion but do not
invalidate this truthful `planned` intake.
