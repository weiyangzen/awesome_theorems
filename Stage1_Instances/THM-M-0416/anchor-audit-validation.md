# THM-M-0416 Anchor Audit Validation

## Result

The frozen target has an exact candidate route in mathlib at immutable revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tag `v4.29.0`):
`NumberField.Units.rank_modTorsion`, the finite/free quotient instances, and
`NumberField.Units.exist_unique_eq_mul_prod` in
`Mathlib.NumberTheory.NumberField.Units.DirichletTheorem` jointly provide every conjunct.
`AnchorAudit.lean` restates the frozen target literally and checks the composed candidate in the
existing pinned Lake environment. The observed axiom report for both named terminal declarations
and the adapter is exactly `propext`, `Classical.choice`, and `Quot.sound`.

The terminal mathlib file, dependency tree, toolchain tag, license, source digest, declarations,
wrapper relationship, exclusions, and bounded external search are recorded in
`anchor-audit.json`. The historical `S1_M_071.statementShape_mathlib` is a duplicate wrapper over
the same bodies and is not independent proof credit. GitHub repository metadata found no other
project; authenticated code search was unavailable and grep.app rate-limited the query, so no
exhaustive negative claim is made.

This phase establishes an eligible `M0-W` route, but the root remains `M3` after this node. The
obligation tree, proof-integration receipt, transitive declaration and finite/free-instance
provenance, accepted foundation/TCB profile, hermetic validation, independent review, and release
bundle are later gates. Thus this is a self-tested anchor audit pending master acceptance, not
machine-proof promotion or theorem completion.

## Commands and results

Commands ran on 2026-07-12 inside this worker clone at base revision
`d76396d014ed07f02b5e64944c3eafca7d453d40`. Lean used only the existing pinned `.lake`
artifacts; no update, build, fetch, or clone was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0416` | 0 | rank 71; planned; legacy artifacts unaccepted; theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0416/Statement.lean` | 0 | frozen target, statement transport, and mutation surfaces re-elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0416/AnchorAudit.lean` | 0 | exact candidate elaborated; named declarations and adapter reported only `propext`, `Classical.choice`, and `Quot.sound` |
| `python3 Stage1_Instances/THM-M-0416/check_anchor_audit.py` | 0 | manifest/installed revision, tree, source/license hashes, declarations, adapter probes, and conservative status boundary agreed |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | commit `8a178386...ea95`; tree `bdc39a31...5c2b` |
| `sha256sum Formalizations/Lean/.lake/packages/mathlib/Mathlib/NumberTheory/NumberField/Units/DirichletTheorem.lean Formalizations/Lean/.lake/packages/mathlib/LICENSE` | 0 | source `c4eb26b3...5500`; license `b40930bb...33e1` |
| `curl ... api.github.com/search/repositories?q=...` | 0 | HTTP 200, zero complete results; response SHA-256 `08c082fd...2600b2` |
| `curl ... api.github.com/search/code?q=...` | 0 | HTTP 401 authentication blocker; response SHA-256 `b7dbd173...e29e` |
| `curl ... grep.app/api/search?q=...` | 0 | HTTP 429 rate-limit blocker; response SHA-256 `08f455ee...b166` |
| `rg -n 'sorry\\|axiom\\|native_decide\\|unsafe\\|external ' Stage1_Instances/THM-M-0416/AnchorAudit.lean Formalizations/Lean/.lake/packages/mathlib/Mathlib/NumberTheory/NumberField/Units/DirichletTheorem.lean` | 1 | no forbidden textual match; exit 1 is ripgrep's expected no-match status |
| `git diff --check -- Stage1_Instances/THM-M-0416 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Next gate

The obligation-tree phase must separate finite, free, rank, and unique-decomposition leaves and
record their typed composition. Only later proof and validation phases may bind the exact adapter
to transitive provenance, placeholder/trust checks, reproducibility receipts, and an `M0-W`
decision. Until those receipts receive master acceptance, theorem completion remains false.
