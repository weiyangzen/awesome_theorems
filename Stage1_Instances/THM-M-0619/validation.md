# Intake validation

Base revision: `5bc32428da3d17f138ceca67f30fbc2d149da1ba` (tree
`7d2433c3e014a9cc8c4d061bcc1b7d5c637ce33f`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source-statement and duplicate-target boundaries, open
task DAG, structured intake invariants, and a narrow pinned Lean API probe. It does not validate a
canonical compact-metric proposition or proof because neither has been frozen. The
automation-provided canonical `.lake` symlink was pre-existing and used read-only; no dependency
update, build, clone, fetch, or other `.lake` mutation was performed. This dirty worker run is
nonrelease evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0619` | exit 0; rank 1313, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree recorded above |
| `git blame -L 4594,4599 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `set -o pipefail; rg -n 'CompactSpace\.tendsto_subseq\|IsCompact\.tendsto_subseq\|SeqCompactSpace\.tendsto_subseq\|isCompact_iff_isSeqCompact\|compactSpace_iff_seqCompactSpace' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Topology/Sequences.lean Formalizations/Lean/.lake/packages/mathlib/Mathlib/Topology/Defs/Sequences.lean Stage1_Instances/THM-M-0264/IntakeProbe.lean \| sha256sum` | exit 0; bounded output SHA-256 `8353370c55f0ef9923cd6adc6a196485b2fbf91e248cd616202627be4f31954d`; five interfaces and duplicate target located; no source-identical root or proof credit inferred |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0619/IntakeProbe.lean)` | exit 0; five compactness/extraction interfaces elaborated; axiom reports recorded; stdout SHA-256 `d93c9a2c064586f9f08ce2b41e4388ceef9271a818a8b0eddd2483bb777fe38f` |
| `python3 -m json.tool Stage1_Instances/THM-M-0619/instance.json`; repeated for `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0619-pycache python3 -m py_compile Stage1_Instances/THM-M-0619/check_intake.py` | exit 0; scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0619/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; authorities, pins, null target, H-unclassified/M3/R4 boundary, artifacts, provisional receipt, packet, Lean probe, and six open tasks agree |
| `rg -n --glob '*.lean' '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0619` | exit 1 as expected; no prohibited declaration token; diagnostic `#print axioms` is permitted |
| `git diff --check -- Stage1_Instances/THM-M-0619 .stage1-worker-selftest.json`; then `git diff --no-index --check /dev/null "$f"` for each new file, accepting exit 1 as the expected new-file difference | exit 0 aggregate; no whitespace errors |

## Known open gates

An immutable primary edition and exact proposition; carrier versus compact-subset form; universes,
metric structures, ordered binders, selector and convergence encodings, limit membership, boundary
cases, proof passage, translation, errata audit, and independent source review remain open. So do
the canonical Lean expression and environment fingerprints, checked transports, statement
mutations, exhaustive formal anchor and provenance audit, discovery protocol, obligation registry,
typed graphs, proof and composition, trust closure, readable reconstruction, hermetic replay,
deterministic bundle, independent verification, master acceptance, audit completion, and theorem
completion. These open gates do not invalidate a truthful self-tested `planned` intake.
