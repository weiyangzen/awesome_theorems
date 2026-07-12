# Intake validation

Base revision: `d750776142c633e42858cebfc67c5c2664d419d7` (tree
`7e62c62f1939b5cb668e56590b709f71f6e676b5`). Validation date: 2026-07-13
(Asia/Shanghai).

Initial status contained only the automation-provided untracked `Formalizations/Lean/.lake`
symlink. It points to canonical pinned artifacts and was used read-only. No `lake update`, `lake
build`, dependency clone/fetch, or other `.lake` mutation was run. This dirty worker evidence is
nonrelease evidence.

Validation covers target membership, the planned/null-target dossier boundary, source and scope
crosswalk, JSON integrity, open downstream task chain, a narrow pinned Lean API probe, candidate
axiom observation, prohibited-token hygiene, and whitespace. It does not validate a canonical
Nullstellensatz statement or proof because the exact source proposition has not been frozen.
The required `Docs/Blueprint_Guidelines.md` policy input was read and bound at SHA-256
`a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535`.

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

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0026` | 0 | rank 1071; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` | 0 | before owned work, only the pre-existing automation `.lake` symlink appeared |
| `git blame -L 207,212 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --silent --show-error --max-time 30 https://stacks.math.columbia.edu/tag/00FV -o /tmp/stacks-00FV.html` | 0 | downloaded the inspected Theorem 10.34.1 HTML; source lead only, no H0 acceptance |
| `sha256sum /tmp/stacks-00FV.html` | 0 | `6cd63b63c40ce5998c105e5c5ce5b3e78aa099ff5dea75c17280eb1d66030bde` |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0026/IntakeProbe.lean)` | 0 | ten adjacent multivariable-polynomial and Nullstellensatz API checks elaborated; no target theorem was declared |
| `(cd Formalizations/Lean && lake env lean /dev/stdin)` with stdin `import Mathlib.RingTheory.Nullstellensatz`, then `#print axioms` for `MvPolynomial.eq_vanishingIdeal_singleton_of_isMaximal`, `MvPolynomial.isMaximal_iff_eq_vanishingIdeal_singleton`, and `MvPolynomial.vanishingIdeal_zeroLocus_eq_radical` | 0 | each candidate reported `[propext, Classical.choice, Quot.sound]`; intake observation only, not terminal trust acceptance |
| `rg -n -i --glob '*.lean' 'nullstellensatz\|vanishingIdeal_zeroLocus_eq_radical\|isMaximal_iff_eq_vanishingIdeal_singleton' Formalizations/Lean/AwesomeTheorems` | 1 | expected no match; no repo-local target wrapper located; not an exhaustive anchor audit |
| `python3 -m json.tool Stage1_Instances/THM-M-0026/instance.json` (repeated exactly for `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json`) | 0 | each structured artifact is valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0026-pycache python3 -m py_compile Stage1_Instances/THM-M-0026/check_intake.py` | 0 | scoped validator compiled without writing generated files into the owned path |
| `python3 -B Stage1_Instances/THM-M-0026/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target and authoritative-DAG identity, planned H1/M3/R4 boundary, null target, input pins, artifact inventory, packet agreement, and six open tasks passed |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0026` | 1 | expected no match; no prohibited Lean construct |
| `git diff --check -- Stage1_Instances/THM-M-0026 .stage1-worker-selftest.json` plus `git diff --no-index --check /dev/null <file>` for every new owned file and packet | 0 | no whitespace diagnostics, treating no-index exit 1 with empty diagnostic output as the expected new-file difference |

## Known open gates

An accepted exact source proposition, incorporated definitions and premises, historical/correction
audit, and independent review remain open. So do the exact Lean target and minimal imports,
expression/environment fingerprints, checked transports, four statement mutation classes,
exhaustive candidate and terminal-body provenance audit, discovery and obligation freezes, typed
graphs, proof/composition, readable reconstruction, hermetic replay, deterministic evidence bundle,
independent validation, and master acceptance. The close pinned declarations justify `M3` discovery
only; they do not establish M0 for an unidentified canonical root.

The `schema_version` values in the owned JSON files identify this dossier's provisional local record
shapes. No published strict repository schema exists for them in this checkout, so JSON parsing and
the explicit invariants in `check_intake.py` are the validated structural boundary; schema-level
conformance is not claimed.
