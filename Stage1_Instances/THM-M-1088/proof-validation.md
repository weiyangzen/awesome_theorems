# THM-M-1088 proof-phase validation

Item: `S56-M-1088-PROOF`

Base revision: `a1a7e939e58f103f5ff5d23af51437fa8658aa04`

Base tree: `d881fd9641fa3e5f3ebe5082b35672981e90adcf`

## Implemented bodies

`Proof.lean` now contains four local, placeholder-free theorem bodies. The new coordinate lemma
derives the exact variance-parametrized sub-Gaussian MGF of each centered coordinate from its
Gaussian law. The new zero-tail lemma proves the frozen strict-event `u = 0` conclusion directly
from the probability normalization supplied by a nonempty Gaussian process. The existing generic
Chernoff conversion proves the strict `ENNReal` tail bound from a centered-supremum MGF estimate,
and the process-level wrapper composes both branches with the exact positive real `sigma2`
normalization.

These are genuine ingredients of `M1088-B-POSITIVE-TAIL`, `M1088-B-ZERO-TAIL`, and
`M1088-B-MERGE`. Their frozen signatures remain planned prose rather than exact Lean expressions,
so this receipt conservatively claims zero frozen obligations closed.

## Boundary

The coordinate MGF lemma does not imply an MGF bound for a pointwise maximum. The first failed
gate remains `M1088-L-FINITE-CONCENTRATION`: neither this repository nor pinned mathlib contains a
sharp Gaussian isoperimetry or finite Gaussian maximum theorem. The covariance normalization,
finite exhaustion, mean convergence, probability limit, exact upper-tail engine, source/trust
overlays, and root all remain open. The root vector stays `[H2, M3, R4]`, and
`theorem_complete=false`.

## Commands and exact results

All Lean checks reused the existing canonical pinned `.lake` artifacts. No `lake update`, `lake
build`, dependency clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-1088` | 0 | Rank 530; lifecycle `planned`; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1088/check_obligation_tree.py` | 0 | Frozen registry passed with 19 obligations and 43 typed edges; exact root open M3. |
| `bash Stage1_Instances/THM-M-1088/check_proof.sh` | 0 | Four local declarations elaborated under `--trust=0`; each reported exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| `python3 Stage1_Instances/THM-M-1088/check_proof.py` | 0 | Scope, source hashes, pins, receipt, blocker, self-test packet, and open-root boundary passed. |
| prohibited-device scan over `Proof.lean` | 1 | Expected no-match exit; no executable placeholder, bodyless axiom, unsafe/opaque/extern declaration, implementation escape, or native oracle. |
| `git diff --check -- Stage1_Instances/THM-M-1088 .stage1-worker-selftest.json` | 0 | No scoped whitespace errors. |

The pre-existing untracked `Formalizations/Lean/.lake` symlink was reused read-only and is not part
of this change. This worker packet proposes `[_]` only for the self-tested proof contribution. It
is not master acceptance or theorem completion.
