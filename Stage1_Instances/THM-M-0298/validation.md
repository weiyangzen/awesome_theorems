# Intake validation

Base revision: `940588d30669014430d5a1beb187f2bca118e816` (tree
`42d80725ccbabcdd826ed2bc8b3622ac31ac7695`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source and scope crosswalk, open task DAG, structured
invariants, and a pinned Lean feasibility probe. It does not validate a canonical Calderon-Zygmund
decomposition proposition or proof because the source formulation and target remain open. The
automation-provided canonical `.lake` symlink was pre-existing and used read-only; no update,
build, clone, fetch, or dependency mutation was performed. Dirty worker evidence is nonrelease.

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
| `python3 scripts/stage1_target.py show THM-M-0298` | exit 0; rank 1302, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before intake |
| `git status --short --untracked-files=all` | preflight exit 0; expanded the same automation symlink observation; used only to make later worker artifact coverage explicit |
| `git blame -L 2139,2144 -- Docs/researches/math_theorems.md` | exit 0; all six catalogue lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded Crossref/publisher inspection for DOI `10.1007/BF02392130` | exit 0; matching 1952 primary-publication metadata located; the publisher returned an article shell rather than immutable full text, so no pinpoint statement or H0 mapping was admitted |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0298/IntakeProbe.lean)` | exit 0; seven average, box-volume, and covering APIs elaborated; all three diagnostic axiom reports were `[propext, Classical.choice, Quot.sound]`; complete output SHA-256 `6e1748f92f79c84526b911cbad30c603f230ba967a0a5c9c24442ca3b83f60f1` |
| bounded case-insensitive search for `Calderon`, `Calderón`, `Zygmund`, and the exact decomposition phrase in pinned mathlib Lean sources | exit 1 as expected; no exact-name match; this is intake discovery only, not an exhaustive anchor audit |
| `python3 -m json.tool` on the structured intake artifacts | exit 0 after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0298-pycache python3 -m py_compile Stage1_Instances/THM-M-0298/check_intake.py` | exit 0; checker compiled without generated files in the owned path |
| bounded `curl`/`rg` immutable external-source inspection | exit 0; `fpvandoorn/carleson@fdcce451.../WeakCalderonZygmund.lean` and its blueprint hashes reproduced, its declaration bundle enumerated, and Lean `v4.30.0-rc2` / mathlib `1a4917...` pins confirmed; source-inspected only, not cloned, fetched, or locally elaborated |
| `python3 -B Stage1_Instances/THM-M-0298/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; manifest/DAG identity, null target, H1/M1/R4 boundary, source and dependency pins, external-candidate boundary, artifact hashes, worker packet, and six open tasks agree |
| token-anchored prohibited Lean declaration scan over the owned path | exit 1 as expected; no declaration-token match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` in the API-only probe; this intentionally permits the diagnostic command `#print axioms` |
| scoped new-file whitespace checks and `git diff --check` | exit 0; no whitespace errors |

## Known open gates

Canonical root selection, immutable primary full text, exact theorem and incorporated definitions,
complete source-to-modern translation, constants, correction or errata audit, and independent
source review remain open. So do the canonical Lean expression and environment fingerprint,
alternate transports and statement mutations, exhaustive anchor and provenance audit, discovery
protocol, obligation registry, typed graphs, proof and composition, trust closure, readable
reconstruction, hermetic replay, deterministic bundle, independent verification, master
acceptance, audit completion, and theorem completion. These failures do not invalidate a truthful
self-tested `planned` intake.
