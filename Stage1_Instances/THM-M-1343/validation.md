# Intake validation

Base revision: `8bbb7ffdbb5e6e8e3e1ffaba9955137f6b68c76c` (tree
`ade61913e5912b1160e25afe096df7f5b3b0cfed`). Validation ran on 2026-07-13 in the isolated worker
clone.

Validation is limited to target-set consistency, dossier structure and scope invariants, repository
source provenance, neighbor-target boundaries, pinned environment identity, a narrow Lean API
probe, a bounded local source search, proof-escape hygiene, JSON integrity, and whitespace. The
catalog does not select one proposition, so no canonical target, expression hash, mutation result,
source acceptance, or proof is claimed.

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
| `python3 scripts/stage1_target.py show THM-M-1343` | 0 | rank 954, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink |
| `git blame -L 9796,9801 -- Docs/researches/math_theorems.md` | 0 | all six uncited target-record lines originate at commit `bcf3f9fa...b74f` |
| `git blame -L 6801,6807 -- Docs/researches/physics_theorems.md` | 0 | the related but distinct physics record originates at the same repository corpus commit |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1343/IntakeProbe.lean)` | 0 | six adjacent integral-curve, derivative, continuity, and convergence API checks elaborated |
| bounded `rg` for Lyapunov direct-method/stability-criterion terms over repo-local and pinned ODE/dynamics Lean sources | 1 | expected no-match exit; no obvious named direct-method criterion under the searched terms; discovery only, not an exhaustive anchor audit |
| `python3 -m json.tool Stage1_Instances/THM-M-1343/instance.json`, repeated for `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all four structured artifacts are valid JSON |
| `python3 -c 'import ast, pathlib; ast.parse(pathlib.Path("Stage1_Instances/THM-M-1343/check_intake.py").read_text())'` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-1343/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/DAG identity, planned H5/M4/R4 boundary, null target, exact inventory, source hashes, provisional packet, and six open tasks agree |
| prohibited Lean proof-escape scan over the owned path | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-1343 .stage1-worker-selftest.json` plus scoped new-file checks | 0 | no whitespace diagnostics in changed files |

## Known downstream failures

- The title and gloss do not select one stable proposition. No primary source, exact theorem,
  edition, page, assumptions, proof boundary, errata record, or independent source review exists.
- The system class, spaces, equilibrium or invariant set, solution and existence assumptions,
  Lyapunov-function regularity and positivity, orbital derivative, stability mode, locality, and
  boundary cases remain open.
- No canonical Lean expression, expression/environment hash, exact imports, checked alternate
  encoding, or statement mutation is frozen.
- The pinned declarations are only adjacent solution and calculus substrate; no exact source
  transport or exhaustive anchor audit exists.
- Discovery and obligation freezes, typed graphs, proof, composition, readable reconstruction,
  hermetic replay, deterministic bundle, independent verification, release, and master acceptance
  remain open.

The worker self-test therefore proposes only the intake node as `[_]`. Both `audit_complete` and
`theorem_complete` remain false.
