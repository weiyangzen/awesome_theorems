# Intake validation

Base revision: `c2e294becadae6ce784f27ee69f2e8dbf57e0b30` (tree
`3f567e7f76b189432b73444354070c0ff75925b9`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, scope and source crosswalk, open task DAG, structured
invariants, and pinned Lean candidate-interface probe. It does not validate a canonical dominated
convergence proposition or proof because source and variant selection remain open. The
automation-provided canonical `.lake` symlink was pre-existing and used read-only. No `lake
update`, build, clone, fetch, or other dependency mutation was performed. Dirty worker evidence is
nonrelease.

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

## Source boundary

Crossref DOI `10.1007/BF02420592` was inspected as bibliographic discovery. The observed response
had SHA-256 `14ecc7075ac6e618289d49db57b98661635a0609e7d509daefacd3a02d5400ac`
and identifies Lebesgue's *Intégrale, Longueur, Aire*, pages 231-359, in 1902. It does not supply an
exact proposition or primary proof crosswalk. It receives no H0 credit and was not added to the
repository.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0268` | exit 0; rank 1275, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before intake |
| `git rev-parse HEAD 'HEAD^{tree}'`; `git blame -L 1929,1934 -- Docs/researches/math_theorems.md` | exit 0; base revision/tree recorded above; all six source-record lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded Crossref API retrieval for DOI `10.1007/BF02420592` | exit 0; attribution, title, year, and page range confirmed; mutable bibliographic discovery only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package `status --short` | exit 0; pinned revision/tree recorded above; empty status output |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0268/IntakeProbe.lean)` | exit 0; seven exact-topic interfaces elaborated; representative declarations reported `[propext, Classical.choice, Quot.sound]`; complete output SHA-256 `834ccd18e768f3995086da58e3d02c89a3e51d12881731300802c066d4e73ebe` |
| bounded `rg` search in pinned mathlib and repo-local Lean | exit 0; Bochner, lintegral, filter, finite-integral, L1, and application interfaces located; no source identity or proof credit inferred |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | exit 0 after finalization; all structured artifacts parse |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0268-pycache python3 -m py_compile Stage1_Instances/THM-M-0268/check_intake.py` | exit 0; checker compiled without writing generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0268/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; target/DAG identity, source and dependency hashes, H1/M3/R4 boundary, null target, exact inventory, receipt/packet agreement, pinned Lean probe, and six open tasks agree |
| token-anchored prohibited Lean declaration scan over the owned path | exit 1 as expected; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration token; diagnostic `#print axioms` remains permitted |
| scoped per-file new-file whitespace checks and `git diff --check` | exit 0; no whitespace diagnostics |

## Known open gates

An exact immutable primary result, its incorporated definitions, ordered statement, assumption and
proof map, translation, corrections or errata, and independent review remain open. So do canonical
Lean expression and environment fingerprints, checked transports, statement mutations, exhaustive
anchor and provenance audit, discovery and obligation freezes, typed graphs, proof and composition,
accepted trust closure, readable reconstruction, hermetic replay, deterministic bundle, independent
verification, master acceptance, audit completion, and theorem completion. These open gates do not
invalidate a truthful self-tested `planned` intake.
