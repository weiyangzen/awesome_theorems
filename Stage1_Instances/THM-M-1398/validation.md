# Intake validation

- Item: `S56-M-1398-INTAKE`
- Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9`
- Validation date: 2026-07-13 (Asia/Shanghai)

Validation is limited to target membership, the truthful `planned` dossier, source-boundary and
neighbor checks, JSON and artifact invariants, a bounded exact-topic search, and a narrow pinned
Lean API probe. The repository wording is not a proposition, so no canonical expression,
statement mutation, human-source acceptance, proof, audit completion, or theorem completion is
claimed.

The automation-provided untracked `Formalizations/Lean/.lake` symlink points to canonical pinned
artifacts and was used read-only. No `lake update`, `lake build`, dependency clone/fetch, or `.lake`
mutation was performed. This inherited dirty worker is nonrelease evidence.

## Commands and exact results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1398` | 0 | rank 1008; planned; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` before edits | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink was untracked |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision `d502dd6f...d8c9`; tree `829a47c4...215e` |
| `git blame -L 10181,10186 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa...b74f` |
| Crossref API lookup for DOI `10.1073/pnas.38.3.235` | 0 | metadata confirmed Curtiss/Hirschfelder, title, PNAS 38(3), March 1952, pages 235-243, and DOI; discovery only |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned mathlib `8a178386...a95`; tree `bdc39a31...3d5c2b` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | `651c8acc...b1d2` and `321626c8...2d81` |
| bounded case-insensitive `rg` over repo-local and pinned analysis Lean sources for word-bounded stiff, A-stability, multistep, Runge-Kutta, BDF, and related exact-topic names, excluding `omega-stability` false positives | 1 | expected no-match result; no exact-topic Lean declaration located; intake discovery only |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1398/IntakeProbe.lean)` | 0 | nine generic ODE, Gronwall, trajectory-distance, uniqueness, and existence APIs elaborated; stdout SHA-256 `c31836a6...620a` |
| `python3 -B Stage1_Instances/THM-M-1398/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | `intake invariant check: ok (THM-M-1398 planned; H5/M4/R4; six open tasks)` |
| prohibited-construct scan of `IntakeProbe.lean` | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, axiom, constant, opaque, or unsafe declaration |
| scoped JSON, Python compilation, final-newline, LF, NUL, trailing-whitespace, no-index diff, and `git diff --check` checks | 0 | all owned artifacts and the worker packet passed |

## Known downstream failures

- No approved immutable source proposition or stiffness definition exists, and no independent
  source, scope, translation, proof-boundary, correction, or errata review has occurred.
- Equation class, numerical method, grid and arithmetic models, assumptions, binders, exact
  conclusion, constants, and degenerate cases are all open.
- Therefore no canonical Lean expression, minimal import set, expression/environment fingerprint,
  checked transport, or required mutation test exists.
- Anchor audit, discovery protocol, obligation registry, typed graphs, proof, composition, trust
  closure, readable reconstruction, hermetic replay, deterministic bundle, and independent release
  verification remain open.
- Master acceptance remains pending.

These failures prevent ordinary theorem execution and every theorem-completion claim. They do not
invalidate a self-tested planned intake whose purpose is to freeze the honest ambiguity boundary
and the dependent open task DAG.
