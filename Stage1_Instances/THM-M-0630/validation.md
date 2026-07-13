# Intake validation

Base revision: `d1b510bacab792f84a99231485cf4429fdb78978` (tree
`f77c4e4db196fc0ecc271815514a411d06ea6053`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, scope and source crosswalk, open task DAG, structured
invariants, and pinned Lean candidate probe. It does not validate a canonical Stone-Cech
proposition or proof because separation, compactification, greatestness, source mapping, and exact
statement freeze remain open. The automation-provided canonical `.lake` symlink was pre-existing
and used read-only; no update, build, clone, fetch, or other dependency mutation was performed.
Dirty worker evidence is nonrelease.

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
| `python3 scripts/stage1_target.py show THM-M-0630` | exit 0; rank 1323, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` | exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree recorded above |
| `git blame -L 4671,4676 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| exact `curl` commands for Crossref DOIs `10.1090/S0002-9947-1937-1501905-7`, `10.2307/1968839`, and the AMS Stone PDF URL; then `pdftotext -layout` | Stone metadata and 107-page publisher PDF obtained; Definition 21 and Theorems 78, 79, 88 inspected; Cech metadata obtained but body unavailable; exact argv and hashes are in `intake-receipt.json`; H1 family leads only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and status | exit 0; pinned revision/tree above and clean package worktree |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0630/IntakeProbe.lean)` | exit 0; 14 construction, compact/T2, dense, extension, uniqueness, and categorical interfaces elaborated; six candidate axiom reports were `[propext, Classical.choice, Quot.sound]`; output SHA-256 `5456f6851c254ebfb84245a1d66a91698b114b0344e94d467263a01bd18b8adf` |
| `rg -n -i 'stone.?cech\|stone.?čech\|compactification\|isDenseEmbedding_stoneCechUnit\|stoneCechEquivalence' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems` | exit 0; located the strong pinned candidates recorded in the crosswalk; no source-identical root transport credited and no exhaustive anchor audit claimed |
| `python3 -m json.tool` separately on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | exit 0 after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0630-pycache python3 -m py_compile Stage1_Instances/THM-M-0630/check_intake.py` | exit 0; checker compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0630/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; target/DAG identity, hashes, H1/M3/R4 boundary, null target, candidate/source boundaries, artifact inventory, receipt/packet, and six open tasks agree |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0630` | exit 1 as expected; no prohibited declaration token; diagnostic `#print axioms` commands are intentionally permitted |
| `git diff --check -- Stage1_Instances/THM-M-0630 .stage1-worker-selftest.json` plus the exact per-file no-index loop in `intake-receipt.json` | exit 0; no whitespace errors |

## Known open gates

Canonical root selection, complete source definitions and assumption reconstruction, exact
Stone/Cech relationship and modern translation, corrections/errata, and independent source review
remain open. So do complete-regularity separation, compactification and competitor packages,
greatestness order, factor existence/uniqueness/surjectivity, universe and degenerate-case choices,
the canonical Lean expression and environment fingerprints, checked transports, statement
mutations, exhaustive anchor/provenance audit, discovery protocol, obligation registry, typed
graphs, proof and composition, trust closure, readable reconstruction, hermetic replay,
deterministic bundle, independent verification, master acceptance, audit completion, and theorem
completion. These failures do not invalidate a truthful self-tested `planned` intake.
