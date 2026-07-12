# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9` (tree
`829a47c47ae831cada4f8acc6c2c00ba5883215e`). Validation ran on 2026-07-13 in
the isolated worker clone.

Validation is limited to target-set consistency, dossier structure and scope invariants, source
record provenance, pinned environment identity, a narrow Lean API probe, bounded local searches,
proof-escape hygiene, JSON integrity, and whitespace. The source record is not a proposition, so
elaborating a purported canonical Lean target would invent missing mathematics. `IntakeProbe.lean`
therefore checks only possible substrate; it introduces no theorem and supplies no statement or
proof credit.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1443` | 0 | rank 1051, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only pre-existing automation symlink `Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree match this record |
| `git blame -L 10539,10544 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sha256sum` over the manifest, blueprint, execution DAG, skill, guidelines, catalog, Stage0 projection, toolchain, and lockfile | 0 | immutable input hashes recorded in `instance.json` and the provisional receipt |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| initial `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1443/IntakeProbe.lean)` | 1 | rejected nonexistent public identifier `Function.iterate`; corrected to `Function.iterate_succ_apply` rather than masking the failure |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1443/IntakeProbe.lean)` | 0 | nine pinned iteration, fixed-point, contraction, convergence, and error-bound APIs elaborated; complete output SHA-256 `5c815bbbf09ac17a5cf76e4cb68696eeb222130c12d108154e62b8373b1778e9` |
| bounded repository and pinned-mathlib searches for the target ID, Chinese label, fixed-point iteration, successive approximations, Picard iteration, and root finding | 0/1 | no source-identical repo declaration; relevant contraction and limit-transfer candidates identified, with neighboring Banach collision recorded; intake discovery only |
| `python3 -m json.tool` on the three owned JSON files and `.stage1-worker-selftest.json` | 0 | instance, open task DAG, provisional receipt, and worker handoff are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1443-pycache python3 -m py_compile Stage1_Instances/THM-M-1443/check_intake.py` | 0 | scoped intake validator compiles without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-1443/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target and item identity, planned H5/M4/R4 boundary, null target, exact artifact inventory, hashes, handoff, and six open tasks agree |
| `rg -n -i --glob '*.lean' 'sorry\|admit\|sorryax\|axiom\|constant\|opaque\|unsafe' Stage1_Instances/THM-M-1443` | 1 | expected no-match; no prohibited proof escape in the API-only probe |
| `git diff --check -- Stage1_Instances/THM-M-1443 .stage1-worker-selftest.json`, then `git diff --no-index --check /dev/null <file>` for every untracked changed file | 0 | no whitespace diagnostics; expected no-index difference statuses contained no diagnostics |

## Known downstream failures

- The catalog method label and root-finding gloss do not select one stable truth-valued
  proposition or primary source. An approved correction and independent review are open.
- The equation, root/fixed-point bridge, space, map, invariant domain, initial point, assumptions,
  convergence mode and rate, error or stopping conclusion, and all boundary cases are open.
- The Banach contraction candidate overlaps separately cataloged `THM-M-1444`; no statement or
  proof credit can be transferred between the targets without a reviewed scope decision.
- No canonical Lean expression, expression/environment hash, exact imports, checked alternate
  encoding, or statement mutation test exists.
- Discovery protocol, source audit, obligation registry and typed graphs, proof, composition and
  trust checks, readable reconstruction, hermetic replay, deterministic evidence bundle,
  independent release verification, and master acceptance remain open.

These failures block ordinary theorem execution and completion. They do not invalidate a truthful,
self-tested `planned` intake whose deliverable is to preserve the ambiguity, scope boundary,
crosswalk, and open DAG. Only the integration lane may accept the provisional worker receipt.
