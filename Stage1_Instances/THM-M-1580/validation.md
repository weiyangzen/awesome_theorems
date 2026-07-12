# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9` (tree
`829a47c47ae831cada4f8acc6c2c00ba5883215e`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source and neighboring-record boundary, open task
DAG, structured invariants, and a narrow pinned Lean API probe. It does not validate a canonical
noisy-channel coding statement or proof because the catalog does not identify one. The
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
| `python3 scripts/stage1_target.py show THM-M-1580` | exit 0; rank 1027, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink was present |
| `git blame -L 11644,11649 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --retry 2 --fail --silent --show-error --max-time 120 https://people.math.harvard.edu/~ctm/%68ome/text/others/shannon/entropy/entropy.pdf` | exit 0; retrieved a 55-page consolidated copy of Shannon's 1948 paper; PDF SHA-256 `6e4e3411984f3edf99dbfe8b941cb5e8a321379ff0cae6ae5c1f592ad8882ca8` |
| `pdftotext -layout <downloaded-PDF> <temporary-text>` and bounded inspection | exit 0; extracted-text SHA-256 `9a2aa6ad93890df38c11813c8ee89f36559a79f0e204a2a56e7f1f7721dba410`; Sections 5, 11, 12, and 13 Theorems 11 and 12 were inspected; no source bytes were added to the repository |
| Crossref requests for DOI `10.1002/j.1538-7305.1948.tb01338.x` and DOI `10.1002/j.1538-7305.1948.tb00917.x` | exit 0 each; identified the July pages 379-423 and October pages 623-656 parts; response hashes are recorded in `instance.json` and `intake-receipt.json` |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1580/IntakeProbe.lean)` | exit 0; ten adjacent pinned PMF, Markov-kernel, binary-entropy, KL-divergence, chain-rule, uniquely-decodable-code, and Hamming interfaces elaborated; no target theorem declared |
| `rg -n -i --glob '*.lean' 'channel[ _-]*(capacity\|coding)\|noisy[ _-]*channel\|mutual[ _-]*information\|Shannon[ _-]*(channel\|coding)' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | exit 1; expected no match; bounded pinned-mathlib discovery only, not an exhaustive external audit |
| the same exact `rg` pattern over `Formalizations/Lean/AwesomeTheorems` | exit 0; one unrelated metadata string names an external `channel-capacity` repository; it is not a declaration, theorem candidate, or proof credit |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, finalized `intake-receipt.json`, and `.stage1-worker-selftest.json` | exit 0; all structured artifacts are valid JSON |
| `python3 -c "import ast,pathlib; ast.parse(pathlib.Path('Stage1_Instances/THM-M-1580/check_intake.py').read_text())"` | exit 0; scoped validator parsed without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-1580/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; target and authoritative-DAG identity, source pins, H5/M4/R4 boundary, null target, exact artifact inventory, provisional receipt, worker packet, and six open tasks agree |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque)\b\|^[[:space:]]*unsafe\b' Stage1_Instances/THM-M-1580` | exit 1; expected no match; no prohibited declaration in the API-only probe |
| `git diff --check -- Stage1_Instances/THM-M-1580 .stage1-worker-selftest.json` plus `git diff --no-index --check /dev/null <each-new-file>` | exit 0; no whitespace diagnostics, including untracked files |

## Known open gates

The received title/gloss must first be corrected or resolved to one stable proposition. An
accepted immutable primary or authoritative source, exact incorporated definitions,
assumption/conclusion/proof-boundary and correction/errata crosswalk, decision among Shannon
Theorem 11, its direct clause, Theorem 12, and a modern finite-DMC theorem, resolution of the
printed equality boundary, neighboring-record decision, and independent review remain open.

So do the canonical Lean expression and environment fingerprints, checked transports and
mutations, exhaustive anchor audit, discovery protocol, obligation registry, typed graphs, proof
and composition, trust and provenance closure, readable reconstruction, hermetic replay,
deterministic bundle, independent verification, master acceptance, audit completion, and theorem
completion. These open gates do not invalidate a truthful, self-tested `planned` intake.
