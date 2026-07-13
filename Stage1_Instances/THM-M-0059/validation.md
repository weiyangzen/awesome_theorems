# Intake validation

Base revision: `5fe11f4b5e32a06ffb4432460319fc8ae906fe7b` (tree
`64c5aacf7cf3eb79008f5a1970151e3e53cb9966`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier, catalog and ambiguity freeze,
source-statement and non-substitution boundaries, the open task DAG, structured intake invariants,
and a narrow pinned Lean interface/axiom probe. It does not validate a canonical Hadamard matrix
proposition or proof because the exact source formula, domain, row/column choice, equality scope,
and matrix transport have not been frozen as the target. The automation-provided canonical
`.lake` symlink was pre-existing and used read-only. No dependency update, build, clone, fetch, or
other `.lake` mutation was performed. This dirty worker run is nonrelease evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Pinned `Mathlib/Analysis/InnerProductSpace/Orientation.lean` SHA-256:
  `d3a27e4111ddcf0e84e1b0672d830323279c044cc4fee21516268ea13f6f3375`.

## Commands and results

All repository commands ran from the repository root unless a different working directory is
shown.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0059` | exit 0; rank 1526, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree recorded above |
| `git blame -L 440,445 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog fields originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded historical bibliography search | completed; the commonly cited Hadamard 1893 paper and pages 240-246 were identified as a lead, but no lawful immutable scan, pinpoint source crosswalk, correction audit, or independent H0 review was admitted |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded in `instance.json` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| bounded exact-topic search of repo-local Lean and pinned mathlib | completed; found the coordinate-free volume-form inequality, determinant bridges, orthogonal equality, weaker factorial entry bound, and unrelated entrywise Hadamard product; intake discovery only |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0059/IntakeProbe.lean)` | exit 0; seven pinned interfaces elaborated; direct axioms `[propext, Classical.choice, Quot.sound]`; stdout SHA-256 `6abe3a526a275542f689b99a45c2d0b0663be12f939cdc204d833ab12cd4756b` |
| `python3 -m json.tool` on all owned JSON artifacts and the root packet | exit 0 after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0059-pycache python3 -m py_compile Stage1_Instances/THM-M-0059/check_intake.py` | exit 0; scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0059/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; authoritative identity, null target, H1/M3/R4 boundary, source/dependency pins, receipt/packet, exact inventory, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0059/check_intake.py` | exit 0; packet-independent structural replay passed |
| prohibited Lean construct scan over `IntakeProbe.lean` | exit 1 as expected; no match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` |
| scoped per-new-file whitespace checks plus `git diff --check` | exit 0; no whitespace errors |

## Known open gates

A lawful immutable primary source, exact formula and equality scope, complete definitions and
premise/proof crosswalk, translation/correction audit, and independent source review remain open.
So do the real/complex scalar decision, finite-index and dimension conventions, row/column choice,
Euclidean norm, determinant and orientation encodings, matrix/volume-form and squared/unsquared
transports, all boundary cases, canonical Lean expression and environment fingerprints, minimal
imports, checked alternate transports, statement mutations, exhaustive anchor and terminal-body
audit, discovery protocol, obligation registry, typed graphs, proof and composition, transitive
trust and provenance closure, readable reconstruction, hermetic replay, deterministic bundle,
independent verification, master acceptance, audit completion, and theorem completion. These open
gates do not invalidate a truthful self-tested `planned` intake.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0059-INTAKE` only. It supports a planned
dossier, not an accepted node receipt. No canonical statement, source closure, root proof, audit
completion, theorem completion, or master acceptance is claimed.
