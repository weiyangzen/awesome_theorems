# THM-M-0851 intake validation

Base revision: `1c0c5fc6f43e6ae5ecc3b50589b45c3628e0ead4` (tree
`61214aa2a03c032134ddc4958b1df63df3430a85`). Validation date: `2026-07-13`
(`Asia/Shanghai`). Exact per-command start/end times were not captured; the final replay completion
time is recorded in the provisional receipt, and master acceptance must recapture timestamped logs.

Validation is limited to target membership, repository-standard consistency, planned dossier
structure, JSON syntax, immutable input checks, source/scope boundaries, the pinned Lean API and
axiom probe, prohibited-construct hygiene, and whitespace. The catalog does not determine a
proposition, so an invented fixed-edge, independent-edge, or process threshold expression would be
substitution rather than validation. No canonical target, expression hash, mutation certificate,
theorem declaration, or proof is claimed.

The automation-provided `Formalizations/Lean/.lake` symlink existed before this work and exposes the
canonical pinned artifacts. It was used read-only. No update, build, dependency clone or fetch, or
other `.lake` mutation was run.

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0851` | 0 | rank 1406, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink was present |
| `git blame -L 6243,6248 -- Docs/researches/math_theorems.md` | 0 | all six catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `(cd Formalizations/Lean && LC_ALL=C.UTF-8 TZ=UTC lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && LC_ALL=C.UTF-8 TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0851/IntakeProbe.lean)` | 0 | seven adjacent random-graph/connectivity declarations elaborated; two boundary lemmas reported `[propext, Classical.choice, Quot.sound]`; output SHA-256 `a476e104e4ac2229f842934e26a7f910de85b937a5f46993b984344de4fd8de5` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`, clean source |
| bounded `rg` search for random-graph connectivity/threshold declarations in pinned mathlib | 1 | expected no-match: no declaration connecting the binomial random graph to a connectivity threshold; not an exhaustive anchor audit |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0851-pycache python3 -m py_compile Stage1_Instances/THM-M-0851/check_intake.py` | 0 | validator parses without writing in the owned path |
| `python3 -B Stage1_Instances/THM-M-0851/check_intake.py` | 0 | integration-portable public replay passed; worker packet is not required |
| `python3 -B Stage1_Instances/THM-M-0851/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, base inputs, H1/M4/R4 null-target boundary, exact artifact inventory, receipt/packet agreement, pinned probe, and six open tasks agree |
| scoped prohibited-construct scan over `Stage1_Instances/THM-M-0851/*.lean` | 1 | expected no-match: no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-0851 .stage1-worker-selftest.json` plus scoped byte check | 0 | no whitespace diagnostics; all ten new files have final newlines and no carriage return, NUL, or trailing whitespace |

The bounded discovery and prohibited-construct searches use no-match exit `1` deliberately. The
exact commands are recorded in `intake-receipt.json`; the two reusable validation recipes are
structured `cwd`/`argv` records rather than shell strings.

Known downstream failures remain open: immutable exact source selection and independent review;
canonical statement elaboration and required mutations; exhaustive formal anchor/provenance audit;
obligation registry and typed graphs; proof and composition; hermetic replay and deterministic
bundle; and independent release verification. These prevent statement, audit, and theorem
completion but do not invalidate a truthful, self-tested `planned` intake proposal.
