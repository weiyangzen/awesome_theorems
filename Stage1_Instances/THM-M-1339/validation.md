# Intake validation

Base revision: `85da7777da7cc5104d4bc4eaa1d947b8137ca5f5` (tree
`ae4ad4de219b61476e1ed10c008e8139247b9d77`). Validation ran on 2026-07-13 in the isolated worker
clone.

Validation is limited to target-set consistency, dossier structure and scope invariants, source
family crosswalk, neighbor-target boundaries, pinned environment identity, a narrow Lean API probe,
a bounded local source search, proof-escape hygiene, JSON integrity, and whitespace. The catalog
does not select one proposition, so no canonical target, expression hash, mutation result, source
acceptance, or proof is claimed.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

Environment fingerprint:

- Platform: Linux x86_64.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1339` | 0 | rank 950, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink |
| `git blame -L 9768,9773 -- Docs/researches/math_theorems.md` | 0 | all six uncited target-record lines originate at commit `bcf3f9fa...b74f` |
| `curl -L --fail --silent --show-error https://www.mat.univie.ac.at/~gerald/ftp/book-ode/ode.pdf -o /tmp/teschl_ode.pdf` | 0 | downloaded the author-hosted complete preliminary edition; SHA-256 `166e267d...4af` |
| `pdftotext -layout /tmp/teschl_ode.pdf /tmp/teschl_ode.txt` and bounded `rg`/`sed` inspection of Section 2.4 | 0 | Theorems 2.8, 2.9, and 2.11 distinguish field/initial-state estimates, joint initial-time/state dependence, and explicit-parameter dependence |
| `curl -L --fail --silent --show-error https://www.mat.univie.ac.at/~gerald/ftp/book-ode/errata.pdf -o /tmp/teschl_errata.pdf` | 0 | downloaded official errata dated 2026-06-23; SHA-256 `3eacbac5...996e` |
| `pdftotext -layout /tmp/teschl_errata.pdf /tmp/teschl_errata.txt` and bounded page/theorem search | 0 | page-45 correction recorded; no listed correction to Theorem 2.8 or 2.11 found |
| `python3 -m json.tool Stage1_Instances/THM-M-1339/instance.json`, repeated for `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all four structured artifacts are valid JSON |
| `python3 -c 'import ast, pathlib; ast.parse(pathlib.Path("Stage1_Instances/THM-M-1339/check_intake.py").read_text())'` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-1339/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/DAG identity, planned H5/M4/R4 boundary, null target, exact inventory, source hashes, provisional packet, and six open tasks agree |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1339/IntakeProbe.lean)` | 0 | assumption package plus both initial-state local-flow candidates elaborated; axiom reports were `[propext, Classical.choice, Quot.sound]` |
| bounded `rg` for exact title/parameter-dependence topics over repo-local and pinned-mathlib Lean sources | 0 | located the two Picard-Lindelof candidates and no explicit external-parameter solution-dependence declaration; intake discovery only, not an exhaustive anchor audit |
| prohibited Lean proof-escape scan over the owned path | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-1339 .stage1-worker-selftest.json` plus scoped new-file checks | 0 | no whitespace diagnostics in changed files |

## Known downstream failures

- The title and gloss do not select one stable proposition. The inspected source presents multiple
  candidate roots and confirms rather than resolves the ambiguity.
- No approved canonical-root selection, independently reviewed exact theorem and complete
  definition/assumption/proof/errata crosswalk, or reconciliation with `THM-M-1340` and
  `THM-M-1341` exists.
- No canonical Lean expression, expression/environment hash, exact imports, checked alternate
  encoding, or statement mutation is frozen.
- The pinned candidates cover dependence on initial state and time for a fixed field, not the
  catalog's external-parameter clause; no exact source-to-Lean transport is established.
- Discovery protocol, obligation registry, typed graphs, proof, composition, readable
  reconstruction, hermetic replay, deterministic bundle, independent verification, release, and
  master acceptance remain open.

The worker self-test therefore proposes only the intake node as `[_]`. Both `audit_complete` and
`theorem_complete` remain false.
