# Intake validation

Base revision: `ee8c1843ef3ce74178a990f4e64554c1558c51fa` (tree
`3a34df1cc2089854dc563ab4909cc0586713ad20`). Validation ran on 2026-07-13 in
the isolated worker clone.

Validation is limited to target-set consistency, dossier structure and scope invariants, source
record provenance, pinned environment identity, a narrow Lean API probe, bounded local searches,
proof-escape hygiene, JSON integrity, and whitespace. The source record is not an exact
proposition, so elaborating a purported canonical Lean target would invent missing mathematics.
`IntakeProbe.lean` therefore checks only possible substrate; it introduces no theorem and supplies
no statement or proof credit.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1440` | 0 | rank 1119, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only pre-existing automation symlink `Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree match this record |
| `git blame -L 10518,10523 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sha256sum` over manifest, blueprint, execution DAG, skill, guidelines, catalog, Stage0, toolchain, lockfile, and Newton module | 0 | immutable input hashes recorded in `instance.json` and the provisional receipt |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1440/IntakeProbe.lean)` | 0 | nine pinned polynomial Newton-map and root/fixed-point/nilpotent APIs elaborated; output SHA-256 `79f36073ebd39e01c2c95fc5bf2d9e4d3f1ce23585587be71c1363deb4be3b57` |
| `rg -n -i --glob '*.lean' 'Newton-Raphson\|newtonMap\|quadratic convergence\|quadratically converg\|Q-order' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems` | 0 | matches were confined to pinned `Mathlib/Dynamics/Newton.lean` and its polynomial `newtonMap` declarations; no repo-local target declaration or analytic rate theorem appeared |
| `rg -n -i --glob '*.lean' 'quadratic convergence\|quadratically converg\|Q-order' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems` | 1 | expected no-match in the bounded roots; intake discovery only, not a global absence claim |
| `python3 -m json.tool` on the three owned JSON files and `.stage1-worker-selftest.json` | 0 | instance, open task DAG, provisional receipt, and worker handoff are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1440-pycache python3 -m py_compile Stage1_Instances/THM-M-1440/check_intake.py` | 0 | scoped intake validator compiles without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-1440/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target and item identity, planned H5/M4/R4 boundary, null target, exact artifact inventory, hashes, handoff, and six open tasks agree |
| `rg -n -i --glob '*.lean' 'sorry\|admit\|sorryax\|axiom\|constant\|opaque\|unsafe' Stage1_Instances/THM-M-1440` | 1 | expected no-match; no prohibited proof escape in the API-only probe |
| `git diff --check -- Stage1_Instances/THM-M-1440 .stage1-worker-selftest.json`, plus `git diff --no-index --check /dev/null <file>` for untracked files | 0 | no whitespace diagnostics |

## Known downstream failures

- The catalog method label and convergence gloss do not select one exact truth-valued proposition
  or an approved primary source.
- The carrier, function class, derivative notion, root nondegeneracy, Newton update, initial
  neighborhood, iterate well-definedness, convergence and quadratic-rate definitions, constants,
  and boundary cases remain open.
- Pinned mathlib's polynomial Newton APIs are adjacent algebraic results, not the missing analytic
  quadratic-convergence theorem.
- No canonical Lean expression, expression/environment hash, exact imports, checked alternate
  encoding, or statement mutation test exists.
- Source and formal anchor audit, obligation registry and typed graphs, proof, composition and
  trust checks, readable reconstruction, hermetic replay, deterministic evidence bundle,
  independent release verification, and master acceptance remain open.

These failures block ordinary theorem execution and completion. They do not invalidate a truthful,
self-tested `planned` intake whose deliverable is to preserve the ambiguity, scope boundary,
crosswalk, discovery evidence, and open DAG. Only the integration lane may accept the provisional
worker receipt.
