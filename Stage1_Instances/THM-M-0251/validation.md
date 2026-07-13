# THM-M-0251 intake validation

Base revision: `c6fd6dad8fcfe5fd464416cd452f50286b546978` (tree
`5a80b61d8fa09336779f8d1453dcfe4299c9472f`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, scope and non-substitution map, source-statement
crosswalk, six-node open downstream task DAG, receipt invariants, and a narrow pinned Lean API
probe. It does not validate a canonical inner-outer factorization statement or proof because the
catalog does not select one. The automation-provided canonical `.lake` symlink was present before
the intake, used read-only, and not changed. No update, build, clone, fetch, or other dependency
mutation was run. This dirty worker run is nonrelease evidence.

## Environment

- Linux `7.0.0-27-generic`, x86_64; timezone Asia/Shanghai.
- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands And Results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0251` | 0 | rank 1261; planned; L0/rework_required; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` | 0 | before editing, only the automation-provided untracked `Formalizations/Lean/.lake` symlink was present |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree recorded above |
| `git blame -L 1808,1813 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sed -n '1808,1813p' Docs/researches/math_theorems.md` | 0 | displayed the six-line catalog record: title, attribution, date, family gloss, importance, and untrusted status only; the scoped checker separately verifies its excerpt hash |
| `sed -n '6950,6975p' Docs/Stage0_Blueprint.md` | 0 | displayed the Stage0 projection: exact definitions, premises, proof, dependencies, alternatives, axioms, machine status, and artifacts remain open; the scoped checker separately verifies its excerpt hash |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree agreed; package worktree was clean |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0251/IntakeProbe.lean)` | 0 | eight adjacent APIs elaborated; output SHA-256 `0d8ce274...8bba`; representative axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`; no target declaration |
| bounded exact-topic `rg` over repo-local Lean and pinned mathlib | 1 | expected no-match for Hardy-space and inner-outer identifier/name families; discovery only, not an exhaustive audit |
| `python3 -m json.tool` over the three owned JSON files and root worker packet | 0 | all JSON parsed after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0251-pycache python3 -m py_compile Stage1_Instances/THM-M-0251/check_intake.py` | 0 | validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0251/check_intake.py` | 0 | public replay mode checked target/source identity, H5/M4/R4 planned boundary, pins, artifacts, receipt, and six open tasks without scheduler-only metadata |
| `python3 -B Stage1_Instances/THM-M-0251/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | worker mode additionally checked the root handoff packet and pre-integration authority state |
| prohibited-construct scan over the owned Lean probe | 1 | expected no-match; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped no-index whitespace checks and `git diff --check` | 0 | no whitespace diagnostics |

## Known Open Gates

The source edition and exact proposition remain unidentified. So do the Hardy class and exponent,
analytic domain, boundary model and measure, inner and outer predicates, factor list, zero premise,
product equality, normalization, uniqueness, ordered binders, assumptions, conclusion, and every
boundary case. The Beurling/1949 catalog identity has no accepted pinpoint crosswalk. The canonical
Lean expression and environment fingerprint, checked transports and mutations, precommitted
discovery protocol, exhaustive anchor audit, obligation registry, typed graphs, proof and
composition, provenance and trust closure, readable reconstruction, hermetic replay, deterministic
bundle, independent verification, and release all remain open.

These gates do not invalidate a truthful, self-tested `planned` intake. They do prevent exact
statement acceptance and all proof-completion claims. Master acceptance is also pending; the node
receipt is unsigned, provisional, non-content-addressed worker evidence with no accepted receipt ID.

## Status Boundary

Lifecycle remains `planned`. The worker proposes `[H5, M4, R4]`, `audit_complete=false`, and
`theorem_complete=false`. The intake creates no canonical obligation, statement fingerprint,
proof body, typed graph, composition certificate, or accepted execution state. Its only proposed
transition is worker `[_]` for the intake deliverable, subject to independent master validation.
