# THM-M-0665 proof-phase validation

Item: `S56-M-0665-PROOF`

Intent: `prove`

Base revision: `72a35d5f64e32233c0bc77a57e47bd078475ad74`

Base tree: `a80eb91ed5629dee62d031e78bc87b509cf8e6eb`

Date: `2026-07-15` (`Asia/Shanghai`)

## Implemented proof bodies

`Proof.lean` contains fourteen unconditional, placeholder-free theorem bodies. They prove the
elementary algebraic-part containment and monotonicity laws, injectivity of the normalized rational
numerator-denominator pair, finiteness of bounded integers and rationals, finiteness of the affine
bounded-height grid and every canonical transcendental slice, and the corresponding cardinal
monotonicity. They also prove the exact affine-ambient-dimension-zero specialization with `c = 1`,
as well as the empty-transcendental-part, connected semialgebraic, and empty-set branches.

These declarations make partial progress toward `M0665-N-ALGEBRAIC`, `M0665-N-HEIGHT`,
`M0665-S-BOUNDARY`, `M0665-B-DIMENSION`, and `M0665-L-COUNT`. They close no entire frozen
obligation: the planned nodes require source-fidelity bridges, arbitrary-ambient dimension
induction, and the general subpolynomial estimate. In particular, the `n = 0` result is not a
substitute for zero-dimensional definable sets in arbitrary ambient dimension.

The exact general root remains `[H1, M3, R4]`. No terminal Pila-Wilkie proof was found by the
prerequisite anchor audit, and this phase does not invent the missing controlled parametrization,
determinant, arithmetic-vanishing, dimension-drop, or exponent-bookkeeping packages.

## Commands and exact results

All commands ran from this worker clone. The automation-provided canonical `.lake` symlink was
reused read-only. No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was
performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Rev-5.6 standard, 15 assurance groups, and all 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0665` | 0 | Rank 709; planned hard-statement-first lane; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0665/check_obligation_tree.py` | 0 | Frozen 20-obligation registry and 48 typed edges passed; root open at M3. |
| `bash Stage1_Instances/THM-M-0665/check_proof.sh` | 0 | Isolated `Statement.lean` and `Proof.lean` elaborated with `--trust=0`; all fourteen declarations passed `assert_no_sorry`. |
| `python3 Stage1_Instances/THM-M-0665/check_proof.py` | 0 | Identity, frozen inputs, source policy, receipt, blocker, pin, exact dirty-path set, and worker packet agreed. |
| Comment-stripped prohibited-device scan over `Proof.lean` | 1 | Expected no-match result: no executable `sorry`, `admit`, `sorryAx`, axiom/constant, unsafe/opaque/extern, `implemented_by`, or `native_decide`. |
| `python3 -m json.tool` on `proof-receipt.json`, `proof-blocker.json`, and `.stage1-worker-selftest.json` | 0 | All three structured artifacts parsed. |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m0665-proof-pycache python3 -m py_compile Stage1_Instances/THM-M-0665/check_proof.py` | 0 | Proof checker compiled without writing into the repository. |
| `git diff --check -- Stage1_Instances/THM-M-0665 .stage1-worker-selftest.json` plus no-index checks for new files | 0 | No whitespace diagnostics. |

The narrow Lean recipe concatenates the exact statement and proof after removing only the proof's
target-local import, then sends the combined source to `lake env lean` on standard input. The call
uses Lean `--trust=0`, one thread, heartbeat checking disabled, and a 180-second timeout.

Lean is `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib is pinned at
`8a178386ffc0f5fef0b77738bb5449d50efeea95`.

## Status boundary

This is a self-tested partial proof-phase delta proposed as `[_]`, not accepted state. The first
failed general gate is `M0665-C-PARAM`; the frozen remaining root cut set is `M0665-C-PARAM`,
`M0665-L-DERIVATIVE`, `M0665-L-ARITHMETIC`, `M0665-L-DROP`, and `M0665-L-COUNT`.
No frozen obligation, root proof, validation, release, `AUDIT-Z`, `THEOREM-Z`, or theorem completion
is claimed.
