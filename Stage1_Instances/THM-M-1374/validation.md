# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9` (tree
`829a47c47ae831cada4f8acc6c2c00ba5883215e`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source and scope boundary, open task DAG, JSON and
scoped invariants, and a narrow pinned Lean API probe. It does not validate a canonical Noether
statement or proof because neither has been frozen. The automation-provided canonical `.lake`
symlink was pre-existing and used read-only; no dependency update, build, clone, fetch, or other
`.lake` mutation was performed. The dirty worker evidence is nonrelease evidence.

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
| `python3 scripts/stage1_target.py show THM-M-1374` | exit 0; rank 984, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree recorded above |
| `git blame -L 10013,10018 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --silent --show-error --max-time 30 -o /tmp/noether-tavel-physics0503066.pdf https://arxiv.org/pdf/physics/0503066` | exit 0; fetched the 14-page v3 translation to temporary storage for source discovery only |
| `sha256sum /tmp/noether-tavel-physics0503066.pdf` | exit 0; SHA-256 `b9f73c19db726b7fd427a38fb786a4a0e7653472abd56d3a042e3b0255ac07d5` |
| `pdftotext -layout /tmp/noether-tavel-physics0503066.pdf /tmp/noether-tavel.txt` | exit 0; inspected Section 1 Theorems I/II and Section 3 page 7 on-shell consequences; no H0 acceptance |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1374/IntakeProbe.lean)` | exit 0; seven adjacent pinned derivative, Frechet derivative, continuous-linear-map, flow, and invariant-set interfaces elaborated; output SHA-256 `26302cdb022fddbd7f92db37c081f09d95a45d18df0dc1b49f10b1af3390f4d3`; no target theorem declared |
| exact regular-expression `rg` search for Noether near Lagrangian, variational-symmetry, current, charge, or conservation terms in pinned mathlib | exit 1; expected no match; bounded intake discovery rather than an exhaustive external audit |
| the same exact `rg` search in repo-local Lean and `Stage1_Instances/THM-M-1515` | exit 0; 16 hits under legacy `S1_M_184`, captured output SHA-256 `3e27c3a92d8e95fb61546ac3c2aeabc0315cd26caddefc8d7029965b6263637d`; no evidence transferred |
| four separate `python3 -m json.tool <path>` invocations for `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root packet | exit 0 for each after finalization |
| `python3 -c "import ast,pathlib; ast.parse(pathlib.Path('Stage1_Instances/THM-M-1374/check_intake.py').read_text(encoding='utf-8')); print('validator ast: ok')"` | exit 0; scoped validator parsed without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-1374/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; manifest and authoritative-DAG identity, null target, H5/M4/R4 boundary, source pins, exact artifact inventory, duplicate-target boundary, receipt/worker packet, and six open tasks agree |
| prohibited Lean construct scan over the owned path | exit 1; expected no match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, `unsafe`, `placeholder`, or `fake result` |
| scoped per-new-file whitespace checks plus `git diff --check` | exit 0; no whitespace errors |

## Known open gates

Canonical root selection, a duplicate-target ownership decision, an accepted immutable source
edition and proposition, complete incorporated definition/premise/conclusion/proof-boundary/
translation/correction crosswalk, and independent source review remain open. So do the canonical
Lean expression and environment fingerprints, checked transports, statement mutations, exhaustive
formal anchor audit, discovery protocol, obligation registry, typed graphs, proof and composition,
trust and provenance closure, readable reconstruction, hermetic replay, deterministic bundle,
independent verification, master acceptance, audit completion, and theorem completion. These
failures do not invalidate a truthful self-tested `planned` intake.
