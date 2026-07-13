# Intake validation

Base revision: `c2e294becadae6ce784f27ee69f2e8dbf57e0b30` (tree
`3f567e7f76b189432b73444354070c0ff75925b9`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, scope and source crosswalk, open task DAG, structured
invariants, and pinned Lean candidate probe. It does not validate a canonical Stone-Weierstrass
proposition or proof because exact source admission and the proposition-changing choices in the
scope map remain open. The automation-provided canonical `.lake` symlink was pre-existing and used
read-only. No update, build, dependency clone or fetch, or other `.lake` mutation was performed.
Dirty worker evidence is nonrelease.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean after the probe.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0266` | exit 0; rank 1274, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before intake |
| `git rev-parse HEAD 'HEAD^{tree}'`; `git blame -L 1915,1920 -- Docs/researches/math_theorems.md` | exit 0; base revision/tree recorded above; all six source-record lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref metadata requests for DOI `10.1090/S0002-9947-1937-1501905-7`, DOI `10.2307/3029750`, and DOI `10.2307/3029337` | exit 0; observed response SHA-256 values `b361149e...150c`, `1ae00b84...47d`, and `bad66fe6...f7e`; bibliographic leads only, no H0 credit |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package `status --short` | exit 0; pinned revision/tree recorded above; empty status output |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0266/IntakeProbe.lean)` | exit 0; six real, epsilon, compact-set, and RCLike Stone-Weierstrass interfaces elaborated; both representative declarations reported `propext`, `Classical.choice`, and `Quot.sound`; complete output SHA-256 `0aae7fba94eb9a61012a6a5bc541de1cd0337ae61992ab0301b335b366fe9380` |
| bounded `rg` searches in pinned mathlib and repo-local Lean | exit 0; direct real/RCLike candidate family, mathlib `1000` index, and adjacent uses located; no source-identical mapping or root proof credit inferred |
| `python3 -m json.tool` on the three owned JSON artifacts and `.stage1-worker-selftest.json` | exit 0 after finalization; all structured artifacts parse |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0266-pycache python3 -m py_compile Stage1_Instances/THM-M-0266/check_intake.py` | exit 0; checker compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0266/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; authority identity, source/dependency hashes, H1/M3/R4 boundary, null target, exact inventory, receipt/packet agreement, pinned Lean probe, and six open tasks agree |
| token-anchored prohibited Lean declaration scan over the owned path | exit 1 as expected; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration token; diagnostic `#print axioms` remains permitted |
| scoped no-index new-file whitespace checks and `git diff --check` | exit 0; no whitespace diagnostics |

## Known open gates

An immutable exact primary source, its incorporated definitions, theorem/page, ordered statement,
assumption and proof map, translation, corrections or errata, 1937-versus-1948 role decision, and
independent review remain open. So do the real/RCLike and global/local scope decisions; exact
algebra, compactness, separation, density, topology, binder, and boundary encodings; canonical Lean
expression and environment fingerprints; checked transports; statement mutations; exhaustive
anchor and provenance audit; discovery and obligation freezes; typed graphs; proof and composition;
accepted trust closure; readable reconstruction; hermetic replay; deterministic bundle; independent
verification; master acceptance; audit completion; and theorem completion. These open gates do not
invalidate a truthful self-tested `planned` intake.
