# THM-M-1491 intake validation

Validation date: 2026-07-13 (Asia/Shanghai).
Base revision: `04d551db74b7e1d7d9d261bba4727b3daf8a70d5`.
Base tree: `ee8a3d7a6c48598ca61028d71e21e0802ed968e1`.

The worker reused the automation-provided canonical `Formalizations/Lean/.lake` symlink read-only.
No `lake update`, `lake build`, dependency clone/fetch, package mutation, theorem declaration, or
proof was run. The source PDF inspection used a temporary file outside the repository and did not
enter the dependency or release closure.

## Commands And Results

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1491` | 0 | rank 1168, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` (preflight) | 0 | only the pre-existing automation symlink `Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree recorded above |
| `git blame -L 10896,10901 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| literal record and Stage0 excerpt SHA-256 checks | 0 | catalog `1087a010...ce3e6`; Stage0 `17bd78ba...d586f` |
| `curl`/`pdfinfo`/`pdftotext` bounded inspection of the author-hosted Boyd-Vandenberghe PDF | 0 | 714-page PDF SHA-256 `40d976c8...d76e`; printed pages 136-139 distinguish a convex-problem definition from the local-to-global theorem |
| bounded repo-local and pinned-mathlib search for convex optimization/extrema declarations | 0 | exact adjacent local-to-global declarations found; no catalog-selected proposition exists |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean 4.29.0 at commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake `5.0.0-src+98dc76e` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` and package status | 0 | mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`, clean package worktree |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1491/IntakeProbe.lean)` | 0 | five adjacent definitions/declarations elaborated; both theorem axiom reports are `[propext, Classical.choice, Quot.sound]`; output SHA-256 `589ef4ec...ffc6`; no canonical target or local proof declared |
| `python3 -m json.tool` on the three owned JSON files and `.stage1-worker-selftest.json` | 0 | all four JSON documents parse |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1491-pycache python3 -m py_compile Stage1_Instances/THM-M-1491/check_intake.py` | 0 | scoped validator compiles without generated files under the owned path |
| `python3 -B Stage1_Instances/THM-M-1491/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | authority identity, null target, H5/M4/R4 boundary, source and pin hashes, exact inventory, handoff, and six open tasks agree |
| prohibited-construct `rg` over `Stage1_Instances/THM-M-1491/IntakeProbe.lean` | 1 expected | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-1491 .stage1-worker-selftest.json` plus per-new-file `git diff --no-index --check` | 0 | no whitespace, final-newline, CR, NUL, or trailing-space defect |

The JSON/worker-packet, scoped invariant, and final whitespace commands are recorded here before
their final rerun. Their exit codes above are valid only after that rerun completes; the provisional
receipt and root packet are emitted only on a passing final run.

## Known Failures And Boundary

- The catalog names a field rather than one truth-valued proposition. Exact immutable theorem
  selection, complete definitions and assumptions, conclusion, proof and corrections mapping, and
  independent source and convex-optimization review remain open.
- The inspected book and pinned theorem are source/formal leads only. The catalog does not identify
  the book or choose local-to-global optimality over existence, uniqueness, KKT, duality, or an
  algorithmic result.
- No canonical Lean target, minimal imports, elaborated expression or environment fingerprint,
  checked alternate encoding, or four-class mutation certificate exists.
- Complete anchor/provenance audit, obligation registry, typed graphs, proof, composition, trust
  closure, readable reconstruction, hermetic replay, deterministic bundle, and independent release
  verification remain open.
- Master acceptance is pending.

These failures block statement and theorem execution but do not invalidate a truthful, self-tested
`planned` intake. Verdict: `no_state_change`; proposed worker state: `[_]`; `audit_complete=false`;
`theorem_complete=false`.
