# Intake validation

Base revision: `27400857bccc93638c97e9c65859ddf5d5b5f4da` (tree
`3762537e0e5ae46cd70b086da49a69e2fd7b275c`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier, source and non-substitution
boundaries, the open task DAG, scoped intake invariants, a bounded exact-topic search, and a narrow
pinned Lean API probe. It does not validate a canonical Brahmagupta proposition or credit a proof
because no source-selected statement is frozen and no target-specific formal artifact was located.
The automation-provided canonical `.lake` symlink was pre-existing and used read-only; no
dependency update, build, clone, fetch, or other `.lake` mutation was performed. This dirty worker
run is nonrelease evidence.

Two secondary web pages were downloaded to `/tmp` for bounded source discovery and were not added
to the repository or admitted as primary/H0 evidence. An attempted request for a primary-source
archive copy timed out after 20 seconds and yielded no artifact. The structured replay recipes
below use only repository and already pinned Lean inputs with network denied.
The recorded web hashes describe this run's responses only; mutable responses may differ and are
not validation-recipe inputs.

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

## Commands and results

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0202` | 0 | rank 1534; planned; L0/rework_required; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` before edits | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree recorded above |
| `git blame -L 1457,1462 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| repository source crosswalk inspection | 0 | catalog and Stage0 provide no formula, area/cyclicity/order definitions, binders, hypotheses, proof/source locator, corrections, errata, reviewer, or formal artifact |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | versions recorded above; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision/tree recorded above; empty package status |
| bounded exact-topic `rg` search for Brahmagupta, Bretschneider, cyclic-quadrilateral area, quadrilateral area, and semiperimeter in repo-local Lean and pinned mathlib | 0 | no target-specific geometry declaration, module, or reduction; unrelated ring identities, a title-only documentation row, Heron's triangle formula, and generic cyclicity/angle APIs were separated from the root |
| retrieve MathWorld `BrahmaguptasFormula.html` for secondary discovery | 0 | 59,682-byte HTML, SHA-256 `fdc7bed6...a270`; modern formula and cyclic specialization located; E5 lead only |
| retrieve MacTutor `Biographies/Brahmagupta/` for secondary discovery | 0 | 70,173-byte HTML, SHA-256 `a0dd298a...17e`; 628 work attribution and explicit historical cyclic-premise dispute located; E5 lead only |
| public-archive primary-source request | 28 | timed out after 20 seconds with no bytes or artifact; no source claim or dependency resulted |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0202/IntakeProbe.lean)` | 0 | seven adjacent cyclicity, angle, triangle, and square-root APIs elaborated; stdout SHA-256 `27e6b44e21e3e173ce8d372b69029611a1ab8bd8fb2a6f71483e8dc82e5102ef`; no target theorem declared |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, finalized `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 for each | all structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0202-pycache python3 -m py_compile Stage1_Instances/THM-M-0202/check_intake.py` | 0 | scoped validator compiled without generating files in the owned directory |
| `python3 -B Stage1_Instances/THM-M-0202/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/DAG identity, null target, H1/M4/R4 boundary, source and pin hashes, exact artifact inventory, provisional receipt/packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0202/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited Lean construct scan over `IntakeProbe.lean` | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -B Stage1_Instances/THM-M-0202/check_json.py --worker-packet` | 0 | strict parse found no duplicate keys in owned JSON and `.stage1-worker-selftest.json` |
| per-new-file no-index whitespace checks plus scoped `git diff --check` | 0 | no whitespace diagnostics |

## Known open gates

- No independently accepted immutable source edition fixes the formula, exact ordered cyclic
  quadrilateral, area, side correspondence, convexity/simplicity/distinctness, semiperimeter,
  square-root or squared equality, proof boundary, translation, attribution, corrections, errata,
  or degenerate cases.
- No canonical Lean expression, expression/environment fingerprint, checked alternate encoding,
  or statement mutation suite exists. Adjacent pinned APIs neither select nor prove the root.
- No target-specific formal declaration, reduction, or proof body was located; the provisional
  machine status is therefore M4. Comprehensive immutable anchor discovery remains downstream.
- Obligation and discovery freezes, typed graphs, proof and composition, source-faithful readable
  reconstruction, transitive provenance and trust closure, hermetic replay, deterministic evidence
  bundle, independent verification, master acceptance, audit completion, and theorem completion
  remain open.

These failures block the statement and every completion claim. They do not invalidate a truthful,
self-tested `planned` intake whose purpose is to freeze the source and ambiguity boundary and open
the downstream task DAG.
