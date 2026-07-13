# Intake validation

Base revision: `f3910e9d9c9dde383801913343b9244462e6173a` (tree
`28f0e995eac01d75999b013a02e02eb792c07754`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier, catalog and ambiguity freeze,
source-statement and non-substitution boundaries, the open task DAG, structured intake invariants,
and a narrow pinned Lean interface/axiom probe. It does not validate a canonical Gershgorin
proposition or proof because the exact source result, domain, encodings, and boundary conventions
are not frozen. The automation-provided canonical `.lake` symlink was pre-existing and used
read-only. No dependency update, build, clone, fetch, or other `.lake` mutation was performed.
This dirty worker run is nonrelease evidence.

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
- Pinned `Mathlib/LinearAlgebra/Matrix/Gershgorin.lean` SHA-256:
  `d55fd47dd6fc18289d04c9ac628c74b6f3813bbc569efcfd276e308fe170cb79`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0053` | exit 0; rank 1521, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree recorded above |
| `git blame -L 398,403 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| scoped inspection of Encyclopedia of Mathematics revision 56196 and zbMATH Open JFM record 2560682 | exit 0; located basic closed row-disc inclusion, standard proof, component-counting refinement, and the 1931 paper bibliography; primary-source/H0 admission remains open |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}' 'HEAD:Mathlib/LinearAlgebra/Matrix/Gershgorin.lean' 'HEAD:docs/1000.yaml'` | exit 0; pinned revision, tree, source blob, and title-map blob recorded in `instance.json` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| bounded exact-topic search and pinned history inspection | exit 0; found `eigenvalue_mem_ball`, its determinant applications, title map, and origin commit `a075669f9771fca06315e01c59a1c20a41a8408d`; discovery only |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0053/IntakeProbe.lean)` | exit 0; six pinned interfaces elaborated; direct axioms `[propext, Classical.choice, Quot.sound]`; stdout SHA-256 `0ea3f7d141ed4ecec7b0f0397d4e01677cb1f0c5465249e60b615631ea716e7b` |
| `python3 -m json.tool` on all owned JSON artifacts and the root packet | exit 0 after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0053-pycache python3 -m py_compile Stage1_Instances/THM-M-0053/check_intake.py` | exit 0; scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0053/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; authoritative identity, null target, H1/M3/R4 boundary, source/dependency pins, receipt/packet, exact inventory, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0053/check_intake.py` | exit 0; packet-independent structural replay passed |
| prohibited Lean construct scan over `IntakeProbe.lean` | exit 1 as expected; no match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` |
| scoped per-new-file whitespace checks plus `git diff --check` | exit 0; no whitespace errors |

## Known open gates

A lawful immutable primary source, exact basic-inclusion versus component-counting root, complete
definitions and premise/proof crosswalk, translation/correction audit, and independent source review
remain open. So do the scalar domain, finite-index and dimension conventions, row/column choice,
eigenvalue and disc encodings, multiplicity and boundary cases, canonical Lean expression and
environment fingerprints, minimal imports, checked transports, statement mutations, exhaustive
anchor and terminal-body audit, discovery protocol, obligation registry, typed graphs, proof and
composition, transitive trust and provenance closure, readable reconstruction, hermetic replay,
deterministic bundle, independent verification, master acceptance, audit completion, and theorem
completion. These open gates do not invalidate a truthful self-tested `planned` intake.
