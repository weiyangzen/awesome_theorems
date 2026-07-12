# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9` (tree
`829a47c47ae831cada4f8acc6c2c00ba5883215e`). Validation ran on 2026-07-13 in
the isolated worker clone.

Validation is limited to target-set consistency, dossier structure and scope invariants,
repository-source provenance, pinned environment identity, a narrow Lean API probe, a bounded
local search, proof-escape hygiene, JSON integrity, and whitespace. The source gloss is not a
truth-valued proposition. Elaborating a purported canonical target would prematurely choose a disk
representation, hyperbolic structure and scale, model relation, conformality convention, and
conclusion bundle. `IntakeProbe.lean` therefore checks adjacent APIs only and supplies no statement
or proof credit.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

## Environment fingerprint

- Platform: Linux x86_64; worker timezone `Asia/Shanghai`.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

All repository commands ran at the repository root unless a different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok`; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0218` | 0 | rank 1011, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only the pre-existing automation `Formalizations/Lean/.lake` symlink was untracked; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 1571,1576 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sed -n '1571,1576p' Docs/researches/math_theorems.md \| sha256sum` | 0 | exact catalog block SHA-256 `c577fc261ece5e2dd196e6a10bab8274345f16ae04dfa92608825b6b80f8c7d5` |
| repository crosswalk inspection | 0 | the catalog and Stage0 supply no primary source, exact definitions, quantifiers, hypotheses, conclusion, formula, proof, errata, reviewer, or formal artifact |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean 4.29.0 and Lake 5.0.0 at the recorded Lean revision |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0218/IntakeProbe.lean)` | 0 | nine pinned unit-disk, metric-ball, conformality, and upper-half-plane APIs elaborated; no target declaration |
| `rg -n -i --glob '*.lean' 'hyperbolic.{0,40}unit[ _-]*(disc\|disk)\|unit[ _-]*(disc\|disk).{0,40}hyperbolic\|poincareDisc\|poincareDisk' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems` | 1 | expected no-match result; bounded intake discovery only, not an exhaustive anchor audit or global absence proof |
| `python3 -m json.tool` separately on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured records are valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0218-pycache python3 -m py_compile Stage1_Instances/THM-M-0218/check_intake.py` | 0 | scoped validator compiles without adding generated files to the owned path |
| `python3 Stage1_Instances/THM-M-0218/check_intake.py` | 0 | manifest/item identity, pinned inputs, H5/M4/R4 planned boundary, null target, artifact inventory, worker packet, and six open tasks agree |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque)[[:space:]]\|^[[:space:]]*unsafe\b' Stage1_Instances/THM-M-0218` | 1 | expected no-match result; no proof escape declaration in the API-only probe |
| scoped `git diff --check` plus the intake checker's byte-level checks for every untracked owned file | 0 | no whitespace diagnostics, CR, NUL, missing final newline, or inventory mismatch |

## Known downstream failures

- The catalog wording is not a stable proposition. No approved source selects the disk
  representation, metric or line element and scale, model relation, conformality meaning,
  orientation policy, hypotheses, conclusion bundle, binder order, or boundary cases.
- No independently reviewed immutable primary or authoritative theorem, complete
  definition/assumption/proof/errata crosswalk, or exact source locator is accepted.
- No canonical Lean expression, minimal imports, expression/environment fingerprint, checked
  alternate encoding, or semantic mutation test exists.
- Discovery precommit, anchor audit, obligation registry and typed graphs, proof, composition and
  trust checks, readable reconstruction, hermetic replay, deterministic evidence bundle, and
  independent release verification remain open.

These failures prevent statement, audit, and theorem-completion claims. They do not invalidate a
truthful, self-tested `planned` intake whose deliverable is to freeze this ambiguity boundary and
open the downstream DAG. Only the integration lane may accept the provisional worker receipt.
