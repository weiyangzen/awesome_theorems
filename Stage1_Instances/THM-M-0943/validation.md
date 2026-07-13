# Intake validation

Base revision: `a3b18eec39bf04be025b1641cae02f4d44fdf11a`; base tree:
`fdfff18dea4c6798c5b322b6088dfe556109c134`. Validation date: 2026-07-13
(Asia/Shanghai); exact start and end timestamps are recorded in the provisional receipt.

This validation covers target membership, the planned dossier and open task DAG, catalog
provenance, theorem-family and result-variant discrimination, JSON and scoped invariants, a narrow
pinned Lean candidate-interface probe, bounded repository/mathlib discovery, prohibited-construct
hygiene, and whitespace. It does not validate a canonical statement or proof because the catalog's
"growth of sumsets" slogan does not choose one binder-complete proposition.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; its package source was clean before and after the
  probe.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Source discovery boundary

The repository record and Stage0 projection were inspected at the recorded base. They identify a
broad Plunnecke-Ruzsa family but no exact statement. Petridis arXiv:1101.3507v3, Theorems 1.1-1.2
on pages 1-2, was inspected temporarily and distinguishes Plunnecke subset growth from Ruzsa's
sum-and-difference extension. The observed PDF SHA-256 was
`f1f886a3780f2722ce9ba2e45589d32dd7374047f2136caae6978672ed0aa872`.

Crossref and the pinned mathlib bibliography identify its journal version and a 2014 overview. No
external source was added to the repository. No catalog adoption, immutable source admission,
complete definition/premise/conclusion/proof/correction map, or independent review was accepted.
These source leads support H1 only.

Pinned mathlib contains a real, proved declaration with an unusually close name. The probe checks
its exact current type, nearby variants, and reported axioms. M3 describes the unidentified root's
formal-interface state; it does not downgrade or deny the candidate theorem's upstream kernel body,
nor does it promote that candidate to M0 before exact source identity and integration gates pass.

## Commands and results

All repository commands ran at the repository root unless a different `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0943` | 0 | rank 1482; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 6889,6894 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| temporary inspection of `https://arxiv.org/pdf/1101.3507v3` plus Crossref metadata | 0 | exact published candidate statements and bibliography recorded; no H0 source admitted |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above; package status clean |
| `sha256sum` on authoritative manifests, catalog records, toolchain, lock, candidate module, and pinned bibliography | 0 | hashes recorded in `instance.json` and the provisional receipt |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0943/IntakeProbe.lean)` | 0 | five exact pinned declarations elaborated; two axiom reports were `[propext, Classical.choice, Quot.sound]`; output SHA-256 `9876c9208b5e0bf30a36237968ba3f227145c67aac7cb44e9e07787c57268a52` |
| bounded exact-topic `rg` search in repo-local Lean and pinned mathlib | 0 | no repo-local target declaration; pinned module, two importers, and exact candidate family located; intake discovery only, not a complete external anchor audit |
| `python3 -m json.tool` on all JSON artifacts and `ast.parse` on `check_intake.py` | 0 | every structured artifact and the checker parse after finalization |
| `python3 -B Stage1_Instances/THM-M-0943/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, source and dependency hashes, H1/M3/R4 null root, exact inventory, packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0943/check_intake.py` | 0 | public replay mode passes without the scheduler-only worker packet |
| prohibited Lean declaration scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in the discovery-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet | 0 aggregate | no whitespace diagnostics; each no-index exit 1 was only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0943 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics; per-file no-index checks cover all untracked artifacts |

## Known open gates

Catalog source adoption, exact Plunnecke-versus-Ruzsa result selection, incorporated definitions,
complete premises and conclusion, historical/correction audit, immutable source admission, and
independent review remain open. So do the canonical Lean target and minimal imports,
expression/environment fingerprints, checked transports, four statement mutation classes,
exhaustive candidate/provenance audit, discovery protocol, obligation registry, typed graphs, proof
composition, source/trust closure, readable reconstruction, hermetic replay, deterministic bundle,
independent verification, master acceptance, audit completion, and theorem completion.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0943-INTAKE` only. It supports a truthful
`planned` dossier, not an accepted node receipt. The strong pinned formal candidate is recorded
without being substituted for the unidentified root. No canonical statement, H0, M0, R0, proof,
audit completion, theorem completion, or master acceptance is claimed.
