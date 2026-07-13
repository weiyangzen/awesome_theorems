# THM-M-0484 proof-phase validation

Item: `S56-M-0484-PROOF`. Base revision:
`a1c9974d7fb28cd680e6494b968544bf801a93a2`.

## Implemented proof

`Proof.lean` adopts the two exact correctness bodies from `Mathlib.NumberTheory.LucasLehmer` at
the manifest-pinned mathlib revision. `pinnedSufficiency` discharges the upstream `1 < p` premise
from the frozen `3 <= p` premise; `pinnedNecessity` has the exact reverse interface. `assembledRoot`
consumes both terminals through the frozen `root_of_directions` certificate, and
`lucasLehmerCriterion` consumes that result through `root_of_terminal` to prove the exact canonical
target.

Lean checks the two pinned terminals and all four local declarations without placeholders. Their
axiom closures are exactly `propext`, `Classical.choice`, and `Quot.sound`. The two upstream proof
bodies are content-identified separately and receive no duplicate credit through local wrappers.

This is a provisional proof-phase `M0-W` root proposal. Exact declaration evidence covers only
`M0484-T-SUFFICIENCY`, `M0484-T-NECESSITY`, `M0484-T-ASSEMBLE`, and `M0484-ROOT`. The full
18-node proof graph is mapped for impact analysis, but `closed_obligation_ids` remains empty. In
particular, the 17 source-body decomposition plans lack abstract-child certificates and receive no
individual or accepted closure credit. This proof phase does not claim theorem completion.

## Commands and exact results

Validation ran on 2026-07-13 (`Asia/Shanghai`). It reused the existing automation-provided pinned
`.lake` symlink without modifying it. No `lake update`, `lake build`, dependency clone/fetch,
network access, or dependency mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0484` | 0 | rank 1365, planned lifecycle, L0/rework-required, `theorem_complete=false` |
| `git status --short --untracked-files=all` before editing | 0 | only the automation-provided untracked `Formalizations/Lean/.lake` symlink |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `a1c9974d...93a2`, tree `1fa287bc...e64` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3...fb04` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `8a178386...ea95`, tree `bdc39a...5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --porcelain=v1` | 0 | empty; pinned dependency source tree clean |
| `bash Stage1_Instances/THM-M-0484/check_proof.sh` | 0 | isolated trust-zero statement/tree/proof elaboration passed; one sorry-free report and six axiom reports, all exactly the selected classical trio; output SHA-256 `65c8a07d...5f1e` |
| `python3 -B Stage1_Instances/THM-M-0484/check_proof.py` | 0 | exact target, receipt hashes, current dependency state, source/olean pins, graph boundary, placeholder policy, and worker packet passed |
| `python3 -m json.tool Stage1_Instances/THM-M-0484/proof-receipt.json` | 0 | valid JSON |
| `python3 -m json.tool .stage1-worker-selftest.json` | 0 | valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0484-proof-pycache python3 -m py_compile Stage1_Instances/THM-M-0484/check_proof.py` | 0 | checker syntax compiled outside the repository tree |
| scoped prohibited-construct scan over `Proof.lean` | 1, expected no match | no proof placeholder, custom/bodyless declaration, unsafe/opaque declaration, external implementation, or native oracle |
| `git diff --check -- Stage1_Instances/THM-M-0484 .stage1-worker-selftest.json` plus no-index checks for new files | 0 | no whitespace diagnostics |

The historical obligation-tree checker is snapshot-strict about its own former authoritative DAG
row. The integration lane has since promoted that predecessor row from `[ ]` attempt 0 to `[_]`
attempt 1, so rerunning the old checker would fail on expected successor-state drift rather than on
the frozen registry. The proof checker instead verifies the current dependency-legal predecessor
state, all current input hashes, the frozen graph boundary, and the narrow Lean proof replay. The
global standard and target validators passed independently.

## Status boundary

The local exact root is kernel-closed in a warm worker replay, but the packet is unsigned,
nonrelease, and not master-accepted. The accepted dossier remains `[H1, M3, R4]` with no accepted
closed obligations. Primary-source review, 17 internal composition certificates, complete
provenance and executable/imported-artifact TCB closure, readable reconstruction, hermetic cold
offline replay, independent verification, validation, release, `AUDIT-Z`, and `THEOREM-Z` remain
open.
