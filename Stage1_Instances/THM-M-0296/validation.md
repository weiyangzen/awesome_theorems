# Intake validation

Base revision: `940588d30669014430d5a1beb187f2bca118e816` (tree
`42d80725ccbabcdd826ed2bc8b3622ac31ac7695`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source/scope and non-substitution boundaries, open
task DAG, structured intake invariants, and a narrow pinned Lean API probe. It does not validate a
canonical Riesz-Thorin proposition or proof because neither has been frozen. The scheduler-provided
canonical `.lake` symlink was pre-existing and used read-only; no dependency update, build, clone,
fetch, or other `.lake` mutation was performed. This dirty worker run is nonrelease evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0296` | exit 0; rank 1300, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the scheduler-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree recorded above |
| `git blame -L 2125,2130 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| exact zbMATH Open API title query for Thorin's extension, saved to `/tmp/thm-m-0296-zbmath.json` | exit 0; records `2510273`, `3034022`, and `2518255` located G. O. Thorin's five-page Lund publication and a 1938/1939 ambiguity; stable bibliographic projection SHA-256 `060b85f5...1b8`; no primary full text or exact operator proposition admitted |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; hashes recorded above |
| exact-name `rg` search for Riesz-Thorin in pinned mathlib and repository-local Lean | exit 1 as expected; no named declaration found; bounded intake discovery only |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0296/IntakeProbe.lean)` | exit 0; seven adjacent `Lp`, induced-map, and Hadamard three-lines APIs elaborated; stdout SHA-256 `438e7f6975d99b873d569ed44a04e52828bdb29f6e21d4a8080bc03032d63aff`; no target declared |
| `python3 -m json.tool Stage1_Instances/THM-M-0296/instance.json`, repeated for `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | exit 0 for each after finalization |
| `python3 -c` with `ast.parse` on `check_intake.py` | exit 0; scoped validator parsed without writing generated files |
| `python3 -B Stage1_Instances/THM-M-0296/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; manifest/DAG identity, null target, H1/M4/R4 boundary, pins, hashes, provisional receipt and packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0296/check_intake.py` | exit 0; public replay mode passes without the scheduler-only packet |
| prohibited Lean construct scan over `IntakeProbe.lean` | exit 1 as expected; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `for f in Stage1_Instances/THM-M-0296/* .stage1-worker-selftest.json; do git diff --no-index --check /dev/null "$f" ...; done`, then scoped `git diff --check` | exit 0 under the recorded no-index new-file convention; no whitespace diagnostics |

## Known open gates

An immutable approved source edition and exact proposition; historical-date reconciliation;
measure spaces, scalars, operator domain and extension semantics; endpoint/intermediate exponent and
constant conventions; ordered binders and boundary cases; source corrections and independent
review remain open. So do canonical elaboration and fingerprints, checked transports and statement
mutations, exhaustive anchor audit, discovery protocol, obligation registry and typed graphs,
proof/composition/trust/provenance closure, readable reconstruction, hermetic replay, deterministic
bundle, independent verification, master acceptance, audit completion, and theorem completion.
These open gates do not invalidate a truthful self-tested `planned` intake.
