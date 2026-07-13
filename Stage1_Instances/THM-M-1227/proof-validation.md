# THM-M-1227 proof-phase validation

Item: `S56-M-1227-PROOF`. Base revision:
`0712591ddaea6a40a0dc6482670e6129e727f5df`.

## Verdict

`partial_proof_self_tested_root_blocked`. `Proof.lean` now contains an independently elaborating,
placeholder-free implementation candidate for the zero-data branch. The first declaration verifies all
six frozen `IsLerayHopfSolution` conjuncts for the zero velocity and gradient. The second consumes
`u0 = 0` and supplies the existential witnesses required at that branch of the canonical target.

The frozen `M1227-B-ZERO` record has only a planned human-statement fingerprint. The checked
declarations are therefore a provisional implementation candidate pending master exact-statement
mapping, not an accepted `M0-L` or closed-obligation claim. They do not handle nonzero admissible
data and do not prove `lerayHopfExistenceTarget`. If the mapping is accepted, the root would improve
from `M4` to `M2`; the accepted instance and frozen pre-proof graph remain `M4` and unchanged.

## Validation

All commands ran in this worker clone on 2026-07-14. The Lean replay used only the existing pinned
toolchain and dependency artifacts, copied the two owned modules to a disposable `/tmp` directory,
and wrote the temporary `Statement.olean` there. No dependency update, build, clone, fetch, or
`.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1227` | 0 | rank 416; planned; L0/rework-required; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1227/check_obligation_tree.py` | 0 | frozen 21-obligation, 63-edge architecture passed; pre-proof graph remains root-open M4 |
| `bash Stage1_Instances/THM-M-1227/check_proof.sh` | 0 | trust-zero isolated statement/proof replay passed; both declarations were sorry-free and reported exactly `propext`, `Classical.choice`, and `Quot.sound` |
| `python3 Stage1_Instances/THM-M-1227/check_proof.py` | 0 | source hashes, frozen fingerprint and denominator, receipt/blocker boundary, cut set, and prohibited devices passed |
| prohibited-device scan over owned `*.lean` | 1 (expected) | no `sorry`, `admit`, `sorryAx`, bodyless axiom/constant, `opaque`, `unsafe`, `extern`, `implemented_by`, or `native_decide` token matched |
| `python3 -m json.tool` on proof receipt and blocker | 0 | both structured artifacts parsed |
| `git diff --check -- Stage1_Instances/THM-M-1227 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The checked proof-source hash is
`f6f03cbf4cc61927cea5a175c7afa1fbc314a27d423598a75f1b228a7f16cabb`. The frozen,
planned (not elaborated) `M1227-B-ZERO` fingerprint is
`planned:v1:sha256:9e7c319da66cfeb318b717f3c4c097c196e66bc9044fd03a4a0e7cf7c81f44db`.

## Remaining blocker

The first unavailable substantive leaf is `M1227-N-DATA`. The complete remaining root cut is
`M1227-N-DATA`, `M1227-N-GLOBAL`, `M1227-C-GALERKIN`, `M1227-C-BOUNDS`, and
`M1227-C-COMPACT`. These packages must construct smooth solenoidal data, global divergence-free
Galerkin solutions, uniform energy estimates, and enough compactness to pass the nonlinear term,
identify the gradient, obtain the strong initial trace, and retain the energy inequality for every
nonnegative time. Neither pinned mathlib nor the audited external statement project contains such
a terminal existence body.

Resume after implementing those packages and the dependent general-data lemmas without
placeholders, or after integrating an immutable compatible exact proof with checked type,
provenance, dependency, axiom, and trust closure. Until then `root_closed=false`,
`audit_complete=false`, and `theorem_complete=false`.
