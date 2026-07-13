# Intake validation

Base revision: `62fad55ced807fdc06921c45d6fcd1f9ad86a1c2` (tree
`9d7c8fe49a4c859d90f3069dc47973ffc5ced768`). Validation ran on 2026-07-13 in the isolated worker
clone.

Validation is limited to target-set consistency, dossier structure and scope invariants, exact
repository-source provenance, pinned environment identity, a narrow Lean API probe, a bounded
local name search, proof-escape hygiene, JSON integrity, and whitespace. The catalog gloss omits
the geometry, line, parallel, and infinitude semantics needed for a canonical proposition, so
elaborating a purported target would invent missing mathematics. `IntakeProbe.lean` therefore
checks adjacent substrate only and supplies no statement or proof credit.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

## Environment fingerprint

- Platform: Linux `7.0.0-27-generic` x86_64; worker timezone `Asia/Shanghai`.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok`; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0213` | 0 | rank 1228, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` before edits | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree above |
| `git blame -L 1536,1541 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sed -n '1536,1541p' Docs/researches/math_theorems.md \| sha256sum` | 0 | exact catalog excerpt SHA-256 `c6f388f4...4cb21` |
| `sed -n '5919,5944p' Docs/Stage0_Blueprint.md \| sha256sum` | 0 | exact Stage0 projection SHA-256 `ad49bb6b...fe3e` |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0213/IntakeProbe.lean)` | 0 | eight adjacent upper-half-plane metric, affine-line, and set-infinitude interfaces elaborated; no target declaration |
| `rg -n -i --glob '*.lean' 'hyperbolic[ _-]+parallel\|parallel[ _-]+postulate\|parallel[ _-]+axiom\|lobachevsky\|bolyai\|limiting[ _-]+parallel\|ultraparallel' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems` | 1 expected no-match | no exact-topic source occurrence located; intake discovery only, not an exhaustive absence claim |
| `python3 -m json.tool` separately on `instance.json`, `task-dag.json`, finalized `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0213-pycache python3 -m py_compile Stage1_Instances/THM-M-0213/check_intake.py` | 0 | scoped validator compiles without adding generated files to the owned path |
| `python3 Stage1_Instances/THM-M-0213/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/DAG identity, source and dependency hashes, planned H5/M4/R4 boundary, null target, artifact inventory, packet, and six open downstream tasks agree |
| `python3 Stage1_Instances/THM-M-0213/check_intake.py` | 0 | public replay mode passes without requiring the scheduler-only worker packet |
| prohibited Lean proof-escape scan over `Stage1_Instances/THM-M-0213/IntakeProbe.lean` | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` token in the API-only probe |
| scoped `git diff --check` plus no-index checks for every untracked changed file | 0 | no whitespace diagnostics |

## Known downstream failures

- The catalog wording is not one stable proposition. No approved source selects a synthetic axiom
  system or analytic model, point/line/incidence definitions, external-point premise, parallel
  convention, line identity, infinitude encoding, logical role, binders, conclusion, or boundary
  cases.
- No immutable primary or authoritative source, exact theorem or postulate and incorporated
  definitions, page-level assumption/proof/translation/errata crosswalk, or independent source
  review is accepted.
- No canonical Lean expression, expression/environment fingerprint, exact minimal imports,
  checked alternate encoding, or statement mutation test exists. Adjacent pinned mathlib carrier,
  metric, affine-line, and infinitude APIs do not select the root.
- Formal anchor audit, discovery protocol, obligation registry and typed graphs, proof,
  composition, transitive provenance and trust closure, readable reconstruction, hermetic replay,
  deterministic evidence bundling, and independent release verification remain open.
- Ordinary theorem-proof execution is blocked by `H5` until the target becomes a stable
  proposition. Master acceptance of this intake remains pending.

These failures prevent statement, audit, and theorem-completion claims. They do not invalidate a
truthful, self-tested `planned` intake whose purpose is to freeze the ambiguity boundary and open
DAG. Only the integration lane may accept the provisional worker receipt.
