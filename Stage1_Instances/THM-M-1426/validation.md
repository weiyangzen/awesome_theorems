# Intake validation

Base revision: `ea6d9ac3942ade0c65c13eccb6bcec945e698e69` (tree
`16e4f4fa87955d7ae7392859a6713a56bcfe7b7e`). Validation date: 2026-07-12 in the
isolated worker clone.

Validation is limited to target-set consistency, dossier structure and scope invariants, primary-
candidate identity and ambiguity evidence, pinned environment identity, a narrow Lean API probe, a
bounded local target search, proof-escape hygiene, and whitespace. The repository gloss is not a
proposition, so no canonical target, expression hash, statement mutation, source acceptance, or
proof is claimed.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It is used read-only. No
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
- Inspected candidate PDF SHA-256:
  `3d708a8b27e6d889c5b6b929a1a3d9702383fc0f0be9ca41ccd4be38fbbf2269`.

## Commands and results

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1426` | 0 | rank 924, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink |
| `git blame -L 10418,10423 -- Docs/researches/math_theorems.md` | 0 | all six uncited record lines originate at commit `bcf3f9fa...b74f` |
| Crossref API query for DOI `10.1016/S0362-546X(00)00216-9` with a compact `jq` projection | 0 | Caraballo, Langa, and Valero; article title; journal 48(6); pp. 805-829; February 2002; DOI confirmed; source-selection evidence only |
| institutional repository PDF download followed by `sha256sum`, `wc -c`, `pdfinfo`, and bounded `pdftotext` inspection | 0 | 251443 bytes, 28 pages, digest above; Definition 1 and multiple inequivalent propositions/theorems located, confirming that source selection remains open |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, finalized `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON |
| Python `ast.parse` on `Stage1_Instances/THM-M-1426/check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-1426/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, planned H5/M4/R4 boundary, null target, exact artifact inventory, provisional packet, and six open tasks agree |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1426/IntakeProbe.lean)` | 0 | eight adjacent pinned relation, measurable-space, measure, and measure-preserving APIs elaborated; no MRDS theorem |
| bounded exact-topic `rg` over repo-local and pinned-mathlib Lean sources | 1 | expected no-match exit; no multivalued/set-valued random dynamics, flow/cocycle, or random differential-inclusion target name found; intake discovery only |
| prohibited Lean proof-escape scan over the owned path | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-1426 .stage1-worker-selftest.json` plus per-new-file no-index checks | 0 | no whitespace diagnostics in all changed files |

## Known downstream failures

- The catalog wording is not a stable proposition. The inspected 2002 paper is not an accepted
  catalog identity and offers several inequivalent target choices.
- No independently reviewed immutable primary theorem, complete definition/assumption/proof/errata
  crosswalk, or boundary decision against `THM-M-1424` and `THM-M-1425` is accepted.
- No canonical Lean expression, expression/environment hash, exact imports, checked alternate
  encoding, or statement mutation test exists.
- Discovery protocol, anchor audit, obligation registry and typed graphs, proof, composition and
  trust checks, readable reconstruction, hermetic replay, deterministic evidence bundle, and
  independent release verification are open.

These failures prevent statement, audit, and theorem-completion claims. They do not invalidate a
truthful, self-tested `planned` intake whose purpose is to freeze the honest ambiguity boundary and
open DAG. Only the integration lane may accept the provisional worker receipt.
