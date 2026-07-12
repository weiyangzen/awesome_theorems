# Intake validation

Base revision: `f88008269fd93059958bb45cbbbfb9a820b13534`.

This phase has no exact Lean statement to elaborate. Running a proof-shaped
surrogate would violate the source boundary, so the only Lean check is the
pinned executable fingerprint. The commands below validate repository
membership and the syntax and internal references of the blocker dossier; they
do not validate a theorem.

## Commands and results

- `python3 Docs/tools/check_stage1_standard.py` (exit 0):
  `ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)`.
- `python3 scripts/stage1_target.py check` (exit 0):
  `ok (1546 unique targets, ranks 1..1546, all L0/rework_required)`.
- `python3 scripts/stage1_target.py show THM-M-0675` (exit 0): confirmed
  rank 718, `L0`, `rework_required: true`, `lifecycle_mode: planned`, and
  `theorem_complete: false`.
- `python3 -m json.tool Stage1_Instances/THM-M-0675/intake.json >/dev/null`
  (exit 0): intake JSON parses.
- A dossier-local Python assertion check (exit 0) verified the assigned item
  and theorem IDs, planned lifecycle, explicit statement blocker, null human
  claim, false theorem-completion flag, and existence of all five owned
  artifacts and every declared public merge target. Output:
  `dossier_selfcheck: ok (planned blocker, 5 owned artifacts, references resolve)`.
- `(cd Formalizations/Lean && lake env lean --version)` (exit 0):
  `Lean (version 4.29.0, x86_64-unknown-linux-gnu, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740, Release)`.
- `git diff --check -- Stage1_Instances/THM-M-0675` (exit 0): no whitespace
  errors.

Preflight `git status --short` showed the canonical-cache symlink
`Formalizations/Lean/.lake` as pre-existing untracked worker setup and this
new owned directory as untracked. No command mutated `.lake`.

## Known failure

First failed gate: rev-5.6 section 5 canonical human statement. The repository
source is not a proposition and supplies no domains, quantifiers, hypotheses,
or conclusion. Consequently the Lean statement gate, expression fingerprint,
mutation suite, and all dependent phases remain blocked.

No workspace-root `.stage1-worker-selftest.json` is emitted: the structural
checks pass, but the assigned intake cannot be represented as genuinely
self-tested completion while this hard source-identity gate remains open.
