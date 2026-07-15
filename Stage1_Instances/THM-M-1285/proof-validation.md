# THM-M-1285 proof-phase validation

Item: `S56-M-1285-PROOF`. Base revision:
`bbe7a5bd1c72a12f3f43b79b6a4cac3f62d2085a`.

## Implemented proof

`Proof.lean` gives the exact local declaration
`Stage1Instances.THM_M_1285.schwarzRearrangementTarget_proof :
SchwarzRearrangementTarget`.

The construction assigns a centered open ball to every finite distribution
value and defines a radial profile as the supremum of nonnegative rational
levels whose balls contain the point. The file proves ball-volume realization,
radius nesting, profile measurability and radial antitonicity, the rational
strict-superlevel union identities, and exact volume at every positive
`ENNReal` threshold. It permits infinite function values and uses the given
finiteness hypothesis only at positive rational levels above the requested
threshold. No boundary-nullity premise is introduced.

## Commands and results

Validation reused the automation-provided canonical pinned `.lake` artifacts
read-only. No `lake update`, `lake build`, dependency clone/fetch, network
operation, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-1285` | 0 | Rank 456; lifecycle `planned`; theorem incomplete in authoritative state. |
| `python3 Stage1_Instances/THM-M-1285/check_obligation_tree.py` | 0 | The frozen 16-obligation, 83-edge pre-proof architecture passed; denominator `6e441bf6a37b0bb83ae0a752e94b30ebf47c8eb567a9284969e869f68b032e9c`. |
| `bash Stage1_Instances/THM-M-1285/check_proof.sh` | 0 | Fresh temporary `Statement.olean`, `ObligationTree.olean`, and `Proof.olean` compiled with `--trust=0`; the exact root and every printed helper reported exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| `python3 -B Stage1_Instances/THM-M-1285/check_proof.py` | 0 | Exact target, frozen hashes and denominator, proof surfaces, receipt, pinned dependency identity, prohibited constructs, and worker packet passed. |
| `rg -n -i --glob '*.lean' '\b(sorry|admit|sorryAx)\b|^[[:space:]]*(axiom|constant|opaque|unsafe)[[:space:]]|implemented_by|native_decide|extern[[:space:]]' Stage1_Instances/THM-M-1285/Proof.lean` | 1 | Expected empty-output pass: no prohibited construct was found. |
| `python3 -m json.tool Stage1_Instances/THM-M-1285/proof-receipt.json` and `python3 -m json.tool .stage1-worker-selftest.json` | 0 | Both structured artifacts parsed. |
| `git diff --check -- Stage1_Instances/THM-M-1285 .stage1-worker-selftest.json` | 0 | No scoped whitespace errors. |

The final source and temporary olean hashes are recorded in
`proof-receipt.json`, after the complete command set above was rerun.

## Boundary

This is a provisional worker proof receipt. It proposes local kernel closure
for the exact root and the twelve implemented proof-route obligations, pending
dependency-ordered master acceptance. The frozen registry and typed graphs
retain their pre-proof snapshot. Accepted state remains `[H2, M3, R3]`.
Foundation/TCB acceptance, source and provenance closure, independently
accepted readability, cold hermetic replay, independent verification,
validation, release, audit completion, and theorem completion are not claimed.
