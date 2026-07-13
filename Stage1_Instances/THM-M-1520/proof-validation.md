# THM-M-1520 proof-phase validation

Item: `S56-M-1520-PROOF`. Base revision:
`f510617dd7a5509521db0a7ee0e5080a341b0a49`.

## Implemented bodies

`VectorFieldRegularity.lean` proves that the exact `C2` Hamiltonian hypothesis makes the canonical
Hamiltonian vector field `C1`. The proof differentiates `H`, transports its derivative through the
Riesz isometry defining `gradient`, projects the canonical `(q,p)` coordinates, applies the fixed
symplectic rotation, and transports back through `WithLp`.

`ChangeOfVariables.lean` composes two earlier checked subbranches. The exact two-sided flow laws
give bijectivity of `Phi t` with inverse `Phi (-t)`, and the nonlinear Jacobian bridge then yields
`MeasurePreserving (Phi t) volume volume` once spatial differentiability and determinant one are
supplied. A second declaration performs this composition uniformly for all times.

These are genuine placeholder-free proof bodies, but no whole frozen obligation is claimed closed.
In particular, the uniform result still has explicit hypotheses
`forall t, Differentiable Real (Phi t)` and
`forall t z, (fderiv Real (Phi t) z).det = 1`. It does not construct either fact from the canonical
Hamilton ODE assumptions.

## Open boundary

The exact target `Stage1.THM_M_1520.LiouvilleStatement` remains open. Pinned mathlib's
Picard-Lindelof development establishes local existence, uniqueness, and Lipschitz dependence on
the initial point, but not spatial `C1` dependence, the spatial variational equation, Jacobi
determinant evolution, or Hamiltonian-flow volume preservation. The first failed gate is therefore
`M1520-C-VARIATION`; the graph-derived minimal root cut remains `M1520-T-ALL-TIMES`.

The new vector-field lemma is an input toward `M1520-B-DIVERGENCE` and `M1520-N-FLOW`, not a proof
of mixed-Hessian cancellation. The change-of-variables lemmas support `M1520-L-CHANGE` and
`M1520-T-ALL-TIMES`, but because their decisive analytic facts are premises, neither those nodes nor
the root receives closure credit.

## Commands and results

All commands ran in this worker clone on 2026-07-14 (`Asia/Shanghai`). No `lake update`,
`lake build`, dependency clone/fetch, or `.lake` mutation was run.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-1520` | 0 | Rank 189; lifecycle `planned`; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1520/check_obligation_tree.py` | 0 | Frozen registry passed with 16 obligations and 32 typed edges; root open M3 and analytic package open M4. |
| `cd Formalizations/Lean && lake env which lean` | 1 | Shared canonical dependency error: `flt-regular: could not resolve 'HEAD' to a commit`; this failed environment query carries no proof credit and no dependency repair or fetch was attempted. |
| `bash Stage1_Instances/THM-M-1520/check_proof.sh` | 0 | Seven copied modules elaborated from disposable `--trust=0` oleans; all six substantive proof declarations and the conditional root composer reported only `propext`, `Classical.choice`, and `Quot.sound`; every declaration carrying `#print sorries` was sorry-free. |
| `python3 Stage1_Instances/THM-M-1520/check_proof.py` | 0 | Exact sources, hashes, receipt boundary, worker packet, clean dependency status, and changed-path coverage passed. |
| `python3 -m json.tool Stage1_Instances/THM-M-1520/proof-receipt.json` | 0 | Provisional node receipt is valid JSON. |
| `python3 -m json.tool .stage1-worker-selftest.json` | 0 | Worker handoff packet is valid JSON. |
| token-anchored prohibited-device scan over owned `*.lean` files | 1 | Expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom-like declaration, unsafe/opaque body, external declaration, implementation escape, or native oracle. |
| `git diff --check -- Stage1_Instances/THM-M-1520 .stage1-worker-selftest.json` | 0 | No scoped whitespace errors. |

The final validator initially requested the executable and import path through `lake env`, as
required. During replay, the shared canonical `flt-regular` checkout had no resolvable `HEAD`, so
Lake could no longer compute the environment. `check_proof.sh` therefore failed closed to the exact
pinned Lean 4.29.0 binary named by `lean-toolchain` and constructed `LEAN_PATH` only from existing
compiled dependency directories in the canonical `.lake`. This fallback neither downloads nor
builds anything and remains warm-cache, nonrelease evidence. The replay used this recipe:

```text
copy Statement, Proof, FlowAlgebra, JacobianBridge, VectorFieldRegularity,
  ChangeOfVariables, and ObligationTree to /tmp
compile Statement and JacobianBridge against the pinned dependency path
compile the five local-import modules with the disposable directory prepended
use LEAN_NUM_THREADS=1, --trust=0, -t0, and a 300-second timeout for every module
remove the disposable directory on exit
```

## Status boundary

This self-test proposes `[_]` only for the proof-phase worker contribution. Accepted state remains
unchanged until integration-lane review. The receipt is not a premise-free proof of the exact root,
does not support theorem completion, and is not validation, independent verification, or release.
