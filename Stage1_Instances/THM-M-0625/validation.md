# Intake validation

Base revision: `d1b510bacab792f84a99231485cf4429fdb78978` (tree
`f77c4e4db196fc0ecc271815514a411d06ea6053`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source-statement mismatch and non-substitution
boundaries, open task DAG, scoped intake invariants, and a narrow pinned Lean API probe. It does not
validate a canonical Bing proposition or proof because source identity and the missing
Moore/developability hypothesis have not been approved. The automation-provided `.lake` symlink was
pre-existing and used read-only; no update, build, clone, fetch, or dependency mutation was run.
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

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0625` | exit 0; rank 1319, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git blame -L 4636,4641 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| publisher PDF inspection with `pdftotext` and `pdfinfo` | exit 0; definitions on page 176, Theorem 10 on pages 182-183, and Theorem 14 on page 184 located; PDF SHA-256 `cbd17aac867cd231618bdc8661d37e87a22205fb20897329cce33e05a432d7e6`; H1 source lead only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| bounded exact-topic `rg` search over repo-local Lean and pinned mathlib | completed with no match for Bing, collectionwise normality, development/Moore-space, or screenability declarations; bounded discovery only |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0625/IntakeProbe.lean)` | exit 0; six adjacent regularity, normality, disjoint-family, and metrizability APIs elaborated; stdout SHA-256 `5d13b384c5703a7356c7f1efa814adc0f742f68e35aec2f0cf4639f020d6c327`; no target theorem declared |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root worker packet | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0625-pycache python3 -m py_compile Stage1_Instances/THM-M-0625/check_intake.py` | exit 0; validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0625/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; manifest/DAG identity, null target, H1/M4/R4 boundary, source and dependency pins, exact artifact hashes, provisional receipt/packet, and six open tasks agree |
| prohibited construct scan over `IntakeProbe.lean` | exit 1 as expected; no match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` |
| scoped per-new-file whitespace checks plus `git diff --check` | exit 0; no whitespace errors |

## Known open gates

Integration-lane review must decide whether Bing Theorem 10 is the catalog target and must preserve
its Moore/developability hypothesis. Exact modern definitions and checked transports for discrete
families, collectionwise normality, development, Moore space, separation conventions, and
metrizability remain open, as do errata review and independent source approval. The canonical Lean
expression/import/environment fingerprints, statement mutations, exhaustive anchor audit,
discovery protocol, obligation registry, typed graphs, proof/composition, trust/provenance closure,
readable reconstruction, hermetic replay, deterministic bundle, independent verification, master
acceptance, audit completion, and theorem completion are also open. These downstream gates do not
invalidate a truthful self-tested `planned` intake.
