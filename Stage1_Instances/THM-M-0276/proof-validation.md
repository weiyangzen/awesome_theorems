# THM-M-0276 proof-phase validation

Item: `S56-M-0276-PROOF`. Base revision:
`5931467f7eefac7a6e57777cc3082e4a2edc03d4`.

Validation date: `2026-07-13` (`Asia/Shanghai`).

## Implemented proof

`Proof.lean` installs the pinned Baire approximation, residual-series exact-preimage, and final
open-map bodies at their exact generic interfaces. It specializes the terminal theorem to the
frozen Real and Complex branches, assembles the canonical conjunction directly, and independently
closes that same target through the frozen `compose_root terminal_adapter pinnedMathlibTerminal`
certificate. The statement phase's definitional transport then closes the exact expanded
open-image target.

The mathematical bodies remain transparent in pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; wrappers do not receive duplicate body credit. Lean
reports all three upstream declarations and nine local declarations sorry-free, with axiom closure
exactly `propext`, `Classical.choice`, and `Quot.sound`. The proof source contains no placeholder,
custom axiom or constant, unsafe/opaque declaration, external implementation, or native oracle.

This is provisional proof-phase evidence for an exact-root `M0-W` proposal, not acceptance or
theorem completion. All 20 proof-reachable graph IDs are mapped for impact analysis, but
`closed_obligation_ids` remains empty. Fourteen internal source-body decompositions still lack
checked abstract-child composition certificates and receive no individual closure credit. The
accepted dossier remains `[H2, M3, R4]`.

## Commands and exact results

All commands ran in this worker clone. The existing automation-provided pinned `.lake` symlink was
reused without mutation. No `lake update`, `lake build`, dependency clone/fetch, network access, or
dependency mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0276` | 0 | rank 1282, planned lifecycle, L0/rework-required, `theorem_complete=false` |
| `git status --short` before editing | 0 | only the automation-provided untracked `Formalizations/Lean/.lake` symlink |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `5931467f...3d4`, tree `45a10c95...775` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3...fb04` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `8a178386...ea95`, tree `bdc39a...5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --porcelain=v1` | 0 | empty; pinned dependency source tree clean |
| `bash Stage1_Instances/THM-M-0276/check_proof.sh` | 0 | isolated trust-zero statement/tree/proof elaboration passed; 12 sorry-free reports; every axiom report was exactly the selected classical trio; direct, frozen-composition, and expanded roots elaborated |
| independent subagent replay of `bash Stage1_Instances/THM-M-0276/check_proof.sh` | 0 | independently confirmed exact signatures, 12 sorry-free reports, permitted axiom closure, clean prohibited scan, and no whitespace issue |
| `python3 -B Stage1_Instances/THM-M-0276/check_proof.py` | 0 | task identity, input hashes, exact wrappers, frozen graph boundary, source/olean pins, receipt, worker packet, placeholder policy, and isolated Lean replay agreed |
| `python3 -m json.tool Stage1_Instances/THM-M-0276/proof-receipt.json` | 0 | valid JSON |
| `python3 -m json.tool .stage1-worker-selftest.json` | 0 | valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0276-proof-pycache python3 -m py_compile Stage1_Instances/THM-M-0276/check_proof.py` | 0 | checker syntax compiled outside the repository tree |
| scoped prohibited-construct scan over `Proof.lean` | 1, expected no match | no proof gap, bodyless declaration, unsafe/opaque declaration, external implementation, or native oracle |
| `git diff --check -- Stage1_Instances/THM-M-0276 .stage1-worker-selftest.json` plus no-index checks for new files | 0 | no whitespace diagnostics |

## Status boundary

The exact root is kernel-closed in a warm worker replay, but the packet is unsigned, nonrelease,
and not master-accepted. The accepted dossier remains `[H2, M3, R4]` with no accepted obligations.
The H2 source's printed Baire-cover gap, 14 internal composition certificates, H0/R0, complete
provenance and executable/imported-artifact TCB closure, hermetic cold offline replay, independent
verification, validation, release, `AUDIT-Z`, and `THEOREM-Z` remain open.
