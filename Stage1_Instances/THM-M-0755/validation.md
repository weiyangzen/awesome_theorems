# Intake validation

Base revision: `d05520867fab3367a9b61b9544c3e12241204f54`.
Base tree: `fb2cfc62077d5b53e9938632cd6361dd60872067`.
Validation date: `2026-07-13` (`Asia/Shanghai`).

This validation covers target membership, source provenance, planned-dossier structure, JSON
integrity, open downstream task identity, and a narrow pinned Lean API probe. Because the catalog
supplies a topic rather than a proposition, no canonical target, expression fingerprint, mutation
result, source acceptance, or proof is claimed. Network retrieval was used only to preserve
secondary and bibliographic discovery metadata; it is not a hermetic source or release gate.

The automation-provided canonical `.lake` symlink and pinned artifacts were used read-only. No
dependency update, build, clone, fetch, or `.lake` mutation was performed. The symlink is a
scheduler-provided, out-of-scope untracked input, so this is nonrelease worker evidence.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0755` | exit 0; rank 1341, planned, L0/rework_required, legacy artifacts unaccepted, theorem_complete false |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree above |
| `git status --short --untracked-files=all` before edits | exit 0; only scheduler-provided `Formalizations/Lean/.lake` symlink was untracked |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; Lean 4.29.0 commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake 5.0.0-src+98dc76e; x86_64 Linux |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output; pinned mathlib worktree clean |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; `651c8acc...b1d2` and `321626c8...2d81`, respectively |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0755/IntakeProbe.lean)` | exit 0; all 12 computability, first-order prenex, powerset, tree, and boldface analytic-set API checks elaborated |
| `rg -n -i --glob '*.lean' 'analytical hierarchy\|analytic hierarchy\|projective hierarchy\|lightface\|boldface\|hyperarithmetical\|second[- ]order arithmetic\|Sigma.?1.?[0-9]\|Pi.?1.?[0-9]' Formalizations/Lean/.lake/packages/mathlib/Mathlib/{Computability,Logic,ModelTheory,SetTheory/Descriptive,MeasureTheory/Constructions/Polish}` | exit 1 (expected no-match); bounded pinned-source search found no exact-topic analytical-hierarchy API; not an external absence claim |
| `python3 -m json.tool Stage1_Instances/THM-M-0755/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0755/task-dag.json` | exit 0; valid JSON |
| `python3 -c "import ast, pathlib; ast.parse(pathlib.Path('Stage1_Instances/THM-M-0755/check_intake.py').read_text(encoding='utf-8'))"` | exit 0; checker syntax valid without writing generated files |

The final JSON validation, target-specific invariant checker, receipt hash check, worker-packet
check, prohibited-construct scan, and whitespace checks are recorded in `intake-receipt.json` after
receipt finalization. The checker independently verifies every untracked owned file's final newline,
line endings, trailing whitespace, inventory, and SHA-256 digest.

## Boundary and open gates

The intake self-test does not clear the node's master-acceptance gate. The first downstream failure
is statement selection: independently inspect an immutable primary Kleene source and justify one
exact source proposition without changing the lightface/boldface, syntax, semantics, pointclass,
parameter, indexing, conclusion, or boundary conventions. Canonical elaboration and mutation tests,
discovery and obligation freezes, complete anchor audit, proof, composition, trust closure,
readable reconstruction, hermetic replay, independent verification, and release remain open.

These failures prevent audit and theorem completion but do not invalidate a truthful `planned`
intake. The proposed vector is `[H5, M4, R4]`; H5 refers only to the received non-propositional
catalog wording, not to the mathematical truth of the classical hierarchy results.
