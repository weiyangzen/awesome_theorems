# Intake validation

Base revision: `62fad55ced807fdc06921c45d6fcd1f9ad86a1c2` (tree
`9d7c8fe49a4c859d90f3069dc47973ffc5ced768`). Validation ran on 2026-07-13 in
the isolated worker clone.

Validation is limited to target-set consistency, dossier structure and scope invariants,
repository-source provenance, pinned environment identity, a narrow Lean API probe, a bounded local
search, proof-escape hygiene, JSON integrity, and whitespace. The source gloss is not a truth-valued
proposition. Elaborating a purported canonical target would prematurely choose the projective
carrier, dimension, quadratic form, affine chart, metric or cross-ratio normalization, model
relation, conclusion bundle, and boundary cases. `IntakeProbe.lean` therefore checks adjacent APIs
only and supplies no statement or proof credit.

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

All repository commands ran at the repository root unless another working directory is stated.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok`; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0217` | 0 | rank 1232, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only the pre-existing automation `Formalizations/Lean/.lake` symlink was untracked; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 1564,1569 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sed -n '1564,1569p' Docs/researches/math_theorems.md \| sha256sum` | 0 | exact catalog block SHA-256 `ce79068ccb6491debe29aa0fc70e6f55004a41e17a9066512dc3970f5e2f0960` |
| repository crosswalk inspection | 0 | catalog and Stage0 supply no primary source, exact definitions, formula, quantifiers, hypotheses, conclusion, proof, errata, reviewer, or formal artifact |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean 4.29.0 and Lake 5.0.0 at the recorded Lean revision |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0217/IntakeProbe.lean)` | 0 | eleven adjacent disk, convex-segment, projectivization, action, and projective-group APIs elaborated; no target declaration |
| `rg -n -i --glob '*.lean' 'beltrami[ _-]?klein\|klein[ _-]?(model\|disk\|disc\|metric)\|hyperbolic.{0,40}(projective\|cross.?ratio)\|projective.{0,40}hyperbolic\|cross.?ratio' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems` | 1 | expected no-match result; bounded intake discovery only, not an exhaustive anchor audit or global absence proof |
| `python3 -m json.tool` separately on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured records are valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0217-pycache python3 -m py_compile Stage1_Instances/THM-M-0217/check_intake.py` | 0 | scoped validator compiles without adding generated files to the owned path |
| `python3 Stage1_Instances/THM-M-0217/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/item identity, pinned inputs, H5/M4/R4 planned boundary, null target, exact artifact inventory, worker packet, and six open tasks agree |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque)[[:space:]]\|^[[:space:]]*unsafe\b' Stage1_Instances/THM-M-0217` | 1 | expected no-match result; no proof escape declaration in the API-only probe |
| scoped `git diff --check` plus the intake checker's byte-level checks for every untracked owned file | 0 | no whitespace diagnostics, CR, NUL, missing final newline, or inventory mismatch |

One initial probe run exited 1 because three generic declarations were incorrectly namespace-
qualified. The probe was corrected to the actual pinned names `convex_ball`, `segment`, and
`openSegment`; the recorded final recipe then exited 0. The failed run supplied no theorem evidence
and is retained here rather than hidden.

## Known downstream failures

- The catalog wording is not a stable proposition. No approved source selects the projective
  carrier, dimension, field, quadratic form, affine chart, distance/structure and normalization,
  model relation, root conclusions, ordered binders, hypotheses, or boundary cases.
- No independently reviewed immutable primary or authoritative theorem, complete definition,
  premise, proof-boundary, and errata crosswalk, or exact source locator is accepted.
- No canonical Lean expression, minimal imports, expression/environment fingerprint, checked
  alternate encoding, or semantic mutation test exists.
- Discovery precommit, anchor audit, obligation registry and typed graphs, proof, composition and
  trust checks, readable reconstruction, hermetic replay, deterministic evidence bundle, and
  independent release verification remain open.

These failures prevent statement, audit, and theorem-completion claims. They do not invalidate a
truthful, self-tested `planned` intake whose deliverable is to freeze this ambiguity boundary and
open the downstream DAG. Only the integration lane may accept the provisional worker receipt.
