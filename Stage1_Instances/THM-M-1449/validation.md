# Intake validation

Base revision: `be1f1d3c684eb883c819bcc968e0631d7f151bb0` (tree
`cff05d9f99014e6c54839589d4470f02df94a986`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source-statement, duplicate-collision and
non-substitution boundaries, open task DAG, structured intake invariants, and a narrow pinned Lean
API probe. It does not validate a canonical SVD proposition or proof because none is frozen. The
automation-provided canonical `.lake` symlink was pre-existing and used read-only; no dependency
update, build, clone, fetch, or other `.lake` mutation was performed. This dirty worker run is
nonrelease evidence.

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
| `python3 scripts/stage1_target.py show THM-M-1449` | exit 0; rank 1126, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree match this record |
| `git blame -L 10581,10586 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --silent --show-error https://linear.axler.net/LADR4e.pdf -o /tmp/thm-m-1449-LADR4e.pdf`; `sha256sum /tmp/thm-m-1449-LADR4e.pdf`; `pdftotext -f 283 -l 288 -layout /tmp/thm-m-1449-LADR4e.pdf -` | exit 0; Definition 7.65 and Theorem 7.70 on printed pages 271 and 273-274 located; observed PDF SHA-256 `45f821b6f51e1f6c42728db6254699d89c14c90fcdb2443c1341188672815d03`; H1 source lead only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `sha256sum Docs/Stage1_Targets_rev-5.6.json Docs/Stage1_Blueprint_rev-5.6.md Docs/Stage1_Execution_DAG_rev-5.6.json skills/execute-stage1-rev56/SKILL.md Docs/Blueprint_Guidelines.md Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; immutable input hashes recorded in `instance.json` and the provisional receipt |
| `sha256sum Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/SingularValues.lean Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Spectrum.lean Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/Matrix/Spectrum.lean Formalizations/Lean/.lake/packages/mathlib/Mathlib/LinearAlgebra/UnitaryGroup.lean` | exit 0; all four pinned source hashes match `instance.json` |
| `rg -n -i --glob '*.lean' 'singular.?value.?decomposition|\\bSVD\\b|U.?Sigma.?V|U.?Σ.?V' Stage1_Instances Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib` | exit 0; found the sibling `THM-M-0044` exact target, proof and differential-validation declarations plus adjacent or prose hits; complete output SHA-256 `5fc82317119d8826ed381f9960eff38a84c3e07db35f48af2fa9f3031e5ce247`; intake discovery only |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0044/Proof.lean)` | exit 1; expected direct-run limitation: sibling `Proof.lean` imports an isolated `ObligationTree.olean` produced by its recorded recipe, so the bare command reported unknown module prefix `ObligationTree`; output SHA-256 `4893d26db53773e3e5b21a47efbde5997f307edf49cc411726aeb97af5e1f7cc`; not treated as proof failure |
| `(cd Formalizations/Lean && bash ../../Stage1_Instances/THM-M-0044/check_proof.sh)` | exit 0; sibling full rectangular Real-and-Complex SVD root elaborated under its isolated prerequisite-olean recipe; root axioms `propext`, `Classical.choice`, and `Quot.sound`; stdout/stderr SHA-256 `91997651fca55341677e4ea5f25e30a7cb10bd0cd2164daa0d34edc066a63e80`; substantive M3 candidate only, with no duplicate/status transfer |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1449/IntakeProbe.lean)` | exit 0; twelve singular-value, spectral, diagonal, conjugate-transpose, and unitary APIs elaborated; two axiom reports named only `propext`, `Classical.choice`, and `Quot.sound`; stdout SHA-256 `fbfd5026c59f3de1e752c148cb239918dd0c1bd8b0966280c91b3c382b2c50bb`; no SVD target declared |
| `python3 -m json.tool Stage1_Instances/THM-M-1449/instance.json`; `python3 -m json.tool Stage1_Instances/THM-M-1449/task-dag.json`; `python3 -m json.tool Stage1_Instances/THM-M-1449/intake-receipt.json`; `python3 -m json.tool .stage1-worker-selftest.json` | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1449-pycache python3 -m py_compile Stage1_Instances/THM-M-1449/check_intake.py` | exit 0; scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-1449/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; target/item identity, planned H1/M3/R4 boundary, null target, duplicate and sibling-candidate boundaries, dependency pins, artifacts, provisional receipt, worker packet, and six open tasks agree |
| `rg -n -i --glob '*.lean' '\\b(sorry|admit|sorryAx|axiom|constant|opaque|unsafe)\\b' Stage1_Instances/THM-M-1449` | exit 1 as expected; no prohibited construct in `IntakeProbe.lean` |
| `git diff --check -- Stage1_Instances/THM-M-1449 .stage1-worker-selftest.json && while IFS= read -r -d '' f; do git diff --no-index --check /dev/null "$f" >/tmp/thm-m-1449-one.out 2>&1; rc=$?; test "$rc" -eq 1; test ! -s /tmp/thm-m-1449-one.out; done < <(find Stage1_Instances/THM-M-1449 -maxdepth 1 -type f -print0) && git diff --no-index --check /dev/null .stage1-worker-selftest.json >/tmp/thm-m-1449-one.out 2>&1; rc=$?; test "$rc" -eq 1; test ! -s /tmp/thm-m-1449-one.out` | exit 0; every no-index exit 1 was normalized only after its diagnostic stream was verified empty |

## Known open gates

An accepted immutable source edition and exact proposition, the `THM-M-0044` identity and
root-ownership decision, scalar field, rectangular dimensions and finite indices, full/thin/compact
factor shape, orthogonal/unitary and star orientation, rectangular diagonal encoding,
nonnegativity/order/multiplicity/zero-padding conventions, existence/uniqueness boundary, every
degenerate case, corrections and historical audit, and independent source review remain open. So
The sibling's full-SVD proof candidate is real but cannot clear this target's statement or machine
debt before duplicate identity, root ownership, exact transport, and receipt acceptance. So do the
canonical Lean expression and environment fingerprints, checked transports, statement
mutations, exhaustive formal anchor audit, discovery protocol, obligation registry, typed graphs,
proof and composition, trust and provenance closure, readable reconstruction, hermetic replay,
deterministic bundle, independent verification, master acceptance, audit completion, and theorem
completion. These open gates do not invalidate a truthful self-tested `planned` intake.
