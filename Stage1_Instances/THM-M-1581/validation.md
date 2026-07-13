# Intake validation

Base revision: `62fad55ced807fdc06921c45d6fcd1f9ad86a1c2` (tree
`9d7c8fe49a4c859d90f3069dc47973ffc5ced768`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source and neighboring-record boundary, open task
DAG, structured invariants, and a narrow pinned Lean API probe. It does not validate a canonical
noiseless source-coding statement or proof because the catalog does not identify one. The
automation-provided canonical `.lake` symlink was pre-existing and used read-only. No `lake
update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed. This
dirty worker evidence is not release evidence.

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
| `python3 scripts/stage1_target.py show THM-M-1581` | exit 0; rank 1203, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink was present |
| `git blame -L 11651,11656 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --retry 2 --fail --silent --show-error --max-time 120 https://people.math.harvard.edu/~ctm/%68ome/text/others/shannon/entropy/entropy.pdf` | exit 0; retrieved a 55-page consolidated copy of Shannon's 1948 paper; PDF SHA-256 `6e4e3411984f3edf99dbfe8b941cb5e8a321379ff0cae6ae5c1f592ad8882ca8` |
| `pdftotext -layout <downloaded-PDF> <temporary-text>` and bounded inspection | exit 0; extracted-text SHA-256 `9a2aa6ad93890df38c11813c8ee89f36559a79f0e204a2a56e7f1f7721dba410`; Part I Sections 1-10 and especially Section 9 Theorem 9 were inspected; no source bytes were added to the repository |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-1581/IntakeProbe.lean)` | exit 0; eight adjacent pinned APIs elaborated; complete stdout SHA-256 `83e26cac5ff39f0a997aa57747b4742981d9dc7cae21286ea9f0cda504553b7f`; no canonical target or proof body was declared |
| `rg -n -i --glob '*.lean' 'source[ _-]*coding\|noiseless[ _-]*(coding\|channel)\|shannon[ _-]*(source\|noiseless)\|expected[ _-]*code[ _-]*length\|entropy.*code.*length' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems` | exit 1 as expected; no source-coding, noiseless-coding, source-entropy/expected-code-length, or Shannon-noiseless declaration matched; empty output SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `python3 -B Stage1_Instances/THM-M-1581/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; planned `H1/M4/R4` invariants, nine owned artifacts, open six-task DAG, source pins, provisional receipt, and worker packet agree |
| `rg -n --glob '*.lean' '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)\b' Stage1_Instances/THM-M-1581` | exit 1 as expected; no prohibited Lean declaration matched |
| JSON parsing of `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | exit 0 for every file |
| per-new-file `git diff --no-index --check` plus `git diff --check -- Stage1_Instances/THM-M-1581 .stage1-worker-selftest.json` | expected new-file difference statuses with no diagnostics; scoped check exit 0 |

## Result boundary

The intake is self-tested as a `planned` dossier and proposes worker state `[_]`; master acceptance
is pending. The source pinpoint, variant map, boundary record, and Lean interfaces are discovery
evidence only. Canonical statement selection and every statement, anchor, obligation, proof,
composition, source-review, readability, hermetic, independent-verification, and release gate
remain open. `audit_complete=false` and `theorem_complete=false`.
