# Proof-phase blocker

Item: `S56-M-1067-PROOF`  
Theorem: `THM-M-1067`  
Attempt date: `2026-07-12`  
Base revision: `7947d9e5d8986f9781776dbcebf381a3c9c000c5`

## Result

The proof phase is blocked and is not self-tested as complete. No proof body, receipt, machine-debt
promotion, or theorem-completion claim is made. In particular, no
`.stage1-worker-selftest.json` is emitted.

The exact target remains
`Stage1Instances.THM_M_1067.BrownianLocalTimeTarget` in `Statement.lean`. It asks for a
jointly continuous, pointwise measurable Brownian local-time field satisfying the occupation
density formula for every nonnegative measurable `ENNReal` test function and every nonnegative
time on one common probability-one event. The target elaborates, but elaboration is not a proof.

## First unresolved cut

The frozen registry has 15 machine-required obligations, and every one still has
`terminal_proof_body_id: null`. The first substantive cut is `M1067-N-WIENER`: the pinned
environment has no Brownian-motion or Wiener-measure construction API from which to derive the
registered increment, covariance, and Gaussian-density interface. Even granting such an
interface, the following independent proof bodies are absent:

- `M1067-C-APPROX`: measurable nonnegative mollified occupation densities;
- `M1067-L-MOMENTS` and `M1067-L-CAUCHY`: uniform moment and Cauchy estimates;
- `M1067-C-LIMIT`: construction of one limiting field;
- the continuity and occupation-identity branches, including extension to the simultaneous
  quantifier scope of the exact target.

The pinned mathlib commit contains neither a Brownian-motion module nor a local-time theorem. The
immutable external project recorded in `anchor-audit.md` supplies Brownian prerequisites only, is
on Lean 4.31 rather than the pinned Lean 4.29 toolchain, contains admitted dependencies, and has no
local-time or occupation-density declaration. It therefore cannot be pinned/imported as an exact
proof body. Filling the registered hypotheses of `ObligationTree.lean` would merely assume these
missing results and is explicitly not proof closure.

## Commands and results

All commands used the existing pinned artifacts. No dependency update, build, clone, fetch, or
`.lake` mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1,546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546 |
| `python3 scripts/stage1_target.py show THM-M-1067` | 0 | rank 509; planned; theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1067/Statement.lean` | 0 | exact target elaborates and prints |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1067/ObligationTree.lean` | 0 | assumption-parametric composition interfaces elaborate; no existence body |
| `test -e Formalizations/Lean/.lake/packages/mathlib/Mathlib/Probability/BrownianMotion/Basic.lean` | 1 | Brownian module is absent |
| `rg -n -i --glob '*.lean' 'local[ _-]?time\|occupation[ _-]?(density\|time)\|Tanaka' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 0 | one unrelated Wiener-Ikehara comment; no stochastic local-time candidate |
| `python3 Stage1_Instances/THM-M-1067/check_obligation_tree.py` | 0 | registry structurally valid; 17 obligations and open M4 root |
| registry terminal-body null assertion | 0 | all 15 machine-required obligations have null terminal bodies |
| `git diff --check -- Stage1_Instances/THM-M-1067` | 0 | no whitespace errors |

## Unblocking condition

Proof execution requires either (1) a placeholder-free Lean 4.29-compatible formalization of the
registered Brownian estimates, local-time construction, convergence, continuity, and simultaneous
occupation identity, with each body attached to its frozen obligation, or (2) an immutable exact
external theorem with a fully audited placeholder-free dependency closure that can be integrated
into the pinned environment. Neither exists in the audited source closure. Root debt therefore
remains `M4`, and `S56-M-1067-PROOF` must remain open.
