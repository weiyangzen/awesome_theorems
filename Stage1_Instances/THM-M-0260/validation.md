# Intake validation

Base revision: `c6fd6dad8fcfe5fd464416cd452f50286b546978` (tree
`5a80b61d8fa09336779f8d1453dcfe4299c9472f`). Validation date: 2026-07-13
(Asia/Shanghai).

Validation is limited to target-set consistency, dossier structure and scope invariants,
publisher-confirmed ambiguity evidence, pinned environment identity, a narrow Lean API probe, a
bounded local target search, proof-escape hygiene, and whitespace. The repository gloss is not a
proposition, so no canonical target, expression hash, statement mutation, source acceptance, or
proof is claimed.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

## Environment

- Linux `7.0.0-27-generic`, x86_64.
- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Source boundary

The Societe Mathematique de France publisher page for DOI `10.24033/ast.306` was inspected as a
source-selection discriminator. The 88,441-byte response had SHA-256
`6912bcfad3a5a3ce658ed2bc1ff3aed3181dfc698b3634f209b56b52f131c26b`. It confirms Yoccoz,
*Petits diviseurs en dimension 1*, Asterisque 231 (1995), and distinguishes the earlier
Bruno-condition sufficiency result from Yoccoz's non-Bruno quadratic converse. It neither selects
the catalog's 1988 root nor supplies a complete primary theorem crosswalk. It receives no H0 credit
and was not added to the repository.

The Numdam item page was also inspected to verify the article-level lead. Its 37,409-byte response
had SHA-256 `415e52492937bd1b926106b9d9c328b2140e904aba27f7cdfabe81db6f32b806` and identifies Yoccoz's
*Theoreme de Siegel, nombres de Bruno et polynomes quadratiques*, Asterisque 231 (1995), pages
1-88. This is bibliographic discovery evidence only; it does not identify the catalog's exact root.

## Commands and results

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0260` | 0 | rank 1268, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink |
| `git rev-parse HEAD 'HEAD^{tree}'`; `git blame -L 1871,1876 -- Docs/researches/math_theorems.md` | 0 | base revision/tree recorded above; all six target-record lines originate at `bcf3f9fa...b74f` |
| bounded `curl` retrieval and inspection of the SMF publisher page for DOI `10.24033/ast.306` | 0 | response size and digest recorded above; publisher confirms materially different sufficiency/converse variants; discovery only |
| bounded `curl` retrieval and inspection of Numdam item `AST_1995__231__1_0` | 0 | 37,409-byte response and digest recorded above; article title, author, volume, year, and pages 1-88 confirmed; discovery only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions recorded above; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package `status --short` | 0 | pinned revision/tree recorded above; empty status output |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0260/IntakeProbe.lean)` | 0 | eight adjacent pinned analytic, unit-disc, and semiconjugacy interfaces elaborated; stdout SHA-256 `67228c6c822c7ebdb31309c4ee54d1ddb86ad85c53646112f1f31570a598e9c9`; no target theorem |
| bounded exact-topic `rg` over repo-local and pinned-mathlib Lean sources | 1 | expected no-match exit; no Yoccoz, Brjuno/Bruno, Siegel-disk, Cremer, or holomorphic-dynamical linearization declaration found; intake discovery only |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, finalized `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 after finalization | all structured artifacts parse |
| Python `ast.parse` on `Stage1_Instances/THM-M-0260/check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0260/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 after finalization | target/DAG identity, source and dependency hashes, duplicate boundary, planned H5/M4/R4 state, null target, exact inventory, receipt/packet agreement, pinned probe, and six open tasks agree |
| token-anchored prohibited Lean declaration scan over the owned path | 1 as expected | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration token |
| scoped per-file new-file whitespace checks and `git diff --check` | 0 | no whitespace diagnostics |

## Known open gates

An approved target correction, exact immutable primary result, incorporated definitions, ordered
statement, assumption and proof map, historical attribution, translation, corrections or errata,
reconciliation with duplicate target `THM-M-1432`, and independent review remain open. So do the
canonical Lean expression and environment fingerprints, checked transports, statement mutations,
exhaustive anchor and provenance audit, discovery and obligation freezes, typed graphs, proof and
composition, accepted trust closure, readable reconstruction, hermetic replay, deterministic
bundle, independent verification, master acceptance, audit completion, and theorem completion.
These open gates do not invalidate a truthful self-tested `planned` intake.
