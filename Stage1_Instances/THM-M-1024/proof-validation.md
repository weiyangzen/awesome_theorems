# THM-M-1024 proof-phase validation

Item: `S56-M-1024-PROOF`

Base revision: `c470319c4a07f669317557ea705f6546605ac4da`

## Implemented bodies

`Proof.lean` contains ten local, placeholder-free declarations. The exponent branch proves
measurability and an explicit Levy-weight bound for the compensated integrand, its Bochner
integrability, zero-frequency normalization, continuity of its jump integral by dominated
convergence, and continuity of the full frozen exponent.

These are genuine parts of `M1024-N-EXPONENT`, but its frozen interface is still a planned package
fingerprint and requires substantially more mathematics. This
receipt therefore claims zero complete frozen obligations, no package inhabitant, and no root
closure.

## Boundary

`ForwardExistencePackage`, `ConversePackage`, and `UniquenessPackage` remain uninhabited. Pinned
mathlib has no Levy-Khintchine or infinite-divisibility theorem family. The audited external
LeanLevy theorem is only over `Real`, uses scalar covariance and open-ball compensation, and has no
checked adapter to the exact all-dimensional closed-ball target. The root stays `[H1, M3, R3]`,
`audit_complete=false`, and `theorem_complete=false`.

The older progress report correctly recorded its then-current partial body and deliberately omitted
a self-test manifest. This packet supersedes only that handoff policy: repository proof-lane
precedent permits `[_]` for a self-tested partial proof contribution while recording zero closed
obligations and an open root. It does not turn partial progress into theorem completion.

## Commands and exact results

Validation reused the pre-existing canonical pinned `.lake` artifacts. No `lake update`, `lake
build`, dependency clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-1024` | 0 | rank 500; lifecycle `planned`; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1024/check_obligation_tree.py` | 0 | frozen 24-obligation/66-edge architecture passed; root open M3 |
| `bash Stage1_Instances/THM-M-1024/check_proof.sh` | 0 | exact statement and ten local declarations elaborated under pinned Lean `--trust=0`; five exported endpoints reported exactly the allowed axioms; source and packet checks passed |
| prohibited-device scan over `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` | 1 | expected no-match exit; no executable placeholder, bodyless declaration, unsafe/extern escape, implementation escape, or native oracle |
| `python3 -m json.tool` over the receipt, blocker, and self-test packet | 0 | all three structured artifacts parsed |
| `git diff --check -- Stage1_Instances/THM-M-1024 .stage1-worker-selftest.json` | 0 | no scoped whitespace errors |

The replay is warm nonrelease evidence. The proof item is proposed as `[_]` only for this
self-tested partial contribution; only the integration lane may accept it. The three terminal
packages, exact root, validation/release gates, and theorem completion remain open.
