# Intake validation

Base revision: `62fad55ced807fdc06921c45d6fcd1f9ad86a1c2` (tree
`9d7c8fe49a4c859d90f3069dc47973ffc5ced768`). Validation ran on 2026-07-13 in the isolated worker
clone.

Validation is limited to target-set consistency, dossier structure and scope invariants, source
provenance, an authoritative modern source lead, pinned environment identity, a narrow Lean
candidate probe, bounded local searches, proof-escape hygiene, JSON integrity, and whitespace. The
catalog gloss does not determine one exact formula variant, so no canonical Lean target was
invented. The candidate probe supplies statement/interface feasibility evidence only.

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
| `python3 scripts/stage1_target.py show THM-M-0222` | 0 | rank 1235, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` before edits | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree above |
| `git blame -L 1605,1610 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sed -n '1605,1610p' Docs/researches/math_theorems.md \| sha256sum` | 0 | exact catalog excerpt SHA-256 `1c31231598289cf3e34fbcd4fedda3e41f778c4e34c318713ebd2fc2a0f2cf92` |
| NIST DLMF requests for section `1.9` and equations `1.9.E30.tex`, `1.9.E31.tex` | 0 | inspected scalar simple-contour value and derivative formulas plus positive orientation; observed SHA-256 values recorded in `instance.json`; source lead only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0222/IntakeProbe.lean)` | 0 | six representative normalized, unnormalized, wrapper, and scalar candidates elaborated; two axiom reports each list `propext`, `Classical.choice`, `Quot.sound`; no target declaration |
| bounded Cauchy-integral-formula search over pinned mathlib and repo-local Lean | 0 | located the pinned candidate family and the foreign `THM-M-1559` wrapper; no ownership or source-match claim inferred |
| `python3 -m json.tool` separately on `instance.json`, `task-dag.json`, finalized `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON |
| path-free Python `compile(...)` syntax check on `Stage1_Instances/THM-M-0222/check_intake.py` | 0 | scoped validator syntax is valid without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-0222/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/DAG identity, source and dependency hashes, planned H1/M3/R4 boundary, null target, exact artifact inventory, packet, and six open downstream tasks agree |
| `python3 -B Stage1_Instances/THM-M-0222/check_intake.py` | 0 | public replay mode passes without requiring the scheduler-only worker packet |
| prohibited Lean proof-escape scan over `Stage1_Instances/THM-M-0222` | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in the API-only probe |
| scoped `git diff --check` plus no-index checks for every untracked changed file | 0 | no whitespace diagnostics |

## Known downstream failures

- The catalog does not select scalar or Banach-valued codomain, circle or general contour/domain,
  function domain, continuity and holomorphicity assumptions, exceptional-set policy, orientation
  and winding, normalization, evaluation point, derivative scope, ordered binders, conclusion, or
  boundary cases.
- DLMF gives an authoritative modern scalar formula but is not the catalog's cited edition. No
  immutable primary Cauchy source, historical 1831 passage, translation/genealogy audit, complete
  incorporated-definition and assumption crosswalk, correction/errata audit, or independent
  source review is accepted.
- No canonical Lean expression, expression/environment fingerprint, exact minimal import claim,
  checked alternate encoding, or statement mutation test exists. Strong pinned candidates support
  `M3` only; exact target match and proof credit are not claimed.
- Formal anchor and terminal-body audit, discovery protocol, obligation registry and typed graphs,
  proof, composition, full provenance and trust closure, source-faithful readable reconstruction,
  hermetic replay, deterministic evidence bundle, and independent release verification remain
  open.
- Master acceptance remains pending.

These failures prevent statement, audit, and theorem-completion claims. They do not invalidate a
truthful, self-tested `planned` intake whose purpose is to freeze the theorem-family boundary,
candidate crosswalk, and open task DAG. Only the integration lane may accept the provisional worker
receipt.
