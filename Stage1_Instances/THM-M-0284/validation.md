# Intake validation

Base revision: `2eea98305d46266f078a50cf0e85853bf6a5e702`; base tree:
`02279a8caa5f31ed8e37e35c8584a336eed9b974`.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, statement and non-substitution boundaries, JSON and scoped invariants, a narrow pinned
Lean exact-topic probe, bounded discovery search, prohibited-construct hygiene, and whitespace. It
does not validate a canonical source statement, source-to-Lean transport, wrapper, or proof.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to the canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned files and root worker packet make the final tree dirty and
nonrelease.

All commands ran on 2026-07-13 in Asia/Shanghai. Commands without an explicit `cwd` ran at the
repository root.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0284` | 0 | rank 1290; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame -L 2041,2046 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sed -n '2041,2046p' Docs/researches/math_theorems.md \| sha256sum`, the duplicate at lines 7392-7397, and `sed -n '7846,7871p' Docs/Stage0_Blueprint.md \| sha256sum` | 0 | canonical and duplicate catalog excerpts agree; Stage0 retains all exact-statement fields as open |
| bounded network searches for a stable lawful copy of the probable 1933 primary source | non-evidence | search endpoints timed out or rejected access; no response, statement passage, or negative global claim was admitted |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean 4.29.0 at `98dc76e3...`; Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` and package status | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package status clean |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `651c8acc...85b1d2` and `321626c8...d81` as recorded in `instance.json` |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0284/IntakeProbe.lean)` | 0 | eight pinned zero-one, tail-independence, independence, measurability, and limsup APIs elaborated; stdout SHA-256 `0e974f6d...55e55`; no target or wrapper was declared |
| `(cd Formalizations/Lean && printf 'import Mathlib.Probability.Independence.ZeroOne\n#print axioms ProbabilityTheory.measure_zero_or_one_of_measurableSet_limsup_atTop\n' \| LC_ALL=C TZ=UTC lake env lean /dev/stdin)` | 0 | candidate reports `[propext, Classical.choice, Quot.sound]`; intake observation only, not full transitive trust closure |
| `rg -n -i 'Kolmogorov.{0,24}(zero\|0-1)\|measure_zero_or_one_of_measurableSet_limsup' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean --glob '*.lean' --glob '!Stage1_Instances/**'` | 0 | found the pinned terminal family and unrelated route mentions; the legacy `S1_M_284.lean` is optional stopping for THM-M-1004 |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured files are valid JSON after finalization |
| `python3 -c "import ast,pathlib; ast.parse(pathlib.Path('Stage1_Instances/THM-M-0284/check_intake.py').read_text())"` | 0 | scoped validator syntax is valid without generating files under the owned path |
| `python3 -B Stage1_Instances/THM-M-0284/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, source and dependency hashes, planned H1/M3/R4 boundary, null target, exact artifact inventory, provisional receipt/packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0284/check_intake.py` | 0 | public replay mode passes without the scheduler-only root packet |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque)\b\|^[[:space:]]*unsafe\b' Stage1_Instances/THM-M-0284` | 1 (expected no match) | no prohibited proof escape or declaration in the API-only probe |
| `git diff --check -- Stage1_Instances/THM-M-0284 .stage1-worker-selftest.json` plus `git diff --no-index --check /dev/null <each new changed file>` | 0/no diagnostics (no-index returns the expected new-file difference code 1) | no whitespace diagnostics |

## Known open gates

An accepted immutable source edition and theorem passage, complete definition/premise/conclusion/
proof-boundary/translation/errata crosswalk, independent review, independent-object choice,
generated-sigma-algebra transport, index and tail convention, ambient and measure assumptions,
event measurability, conclusion encoding, and boundary cases remain open. So do the canonical Lean
expression and environment fingerprint, checked transports, statement mutations, exhaustive anchor
audit, discovery protocol, obligation registry, typed graphs, proof and composition, full trust and
provenance closure, readable reconstruction, hermetic replay, deterministic bundle, independent
verification, master acceptance, audit completion, and theorem completion. These failures do not
invalidate a truthful self-tested `planned` intake.
