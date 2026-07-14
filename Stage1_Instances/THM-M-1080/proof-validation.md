# THM-M-1080 proof-phase validation

Item: `S56-M-1080-PROOF`

Base revision: `fb0fd5be494d0813177dbdc959ec911d69a72015` (tree
`f6d39faae5fb024a71ee786e7a6b017d335841cd`). Validation date: 2026-07-15
(Asia/Shanghai).

## Result

The proof phase is self-tested as a provisional `[_]` proposal. It does not alter the authoritative
accepted state and does not claim theorem completion.

`Proof.lean` implements the arbitrary-measurable-space bounded-increment argument directly: the
symmetric exponential secant bound, centered one-step conditional Hoeffding estimate, finite MGF
iteration, exponential Markov bound and parameter optimization, and separate zero total
squared-bound and zero-threshold cases. `ExactRoot.lean` checks each implemented threshold branch
against its frozen `ObligationTree` package, composes them through the frozen
`azumaUpperTail_of_threshold_packages` theorem, and binds the result to the exact canonical
`Stage1Instances.THM_M_1080.Statement` type as `ExactRoot.azumaUpperTail_exact`.

The isolated replay copied the four Lean sources to a fresh temporary directory. It compiled fresh
`Statement.olean`, `ObligationTree.olean`, `Proof.olean`, and `ExactRoot.olean` outputs with the
direct pinned Lean executable, `--trust=0 -t0`, one Lean thread, and a temporary-first `LEAN_PATH`
only where sibling imports required it. The frozen composition declaration, eight proof
declarations, two package bridges, and exact root each reported exactly `propext`,
`Classical.choice`, and `Quot.sound`; none reported `sorryAx`.

## Commands

| Command | Exit | Result |
|---|---:|---|
| `bash Stage1_Instances/THM-M-1080/check_proof.sh` | 0 | Fresh four-module trust-zero replay passed; 12 axiom reports matched the exact allowed set; prohibited-construct scan passed. |
| `python3 -B Stage1_Instances/THM-M-1080/check_proof.py` | 0 | Source, exact-root, frozen-input, receipt, dependency-pin, and worker-packet invariants passed. |
| `python3 Stage1_Instances/THM-M-1080/check_obligation_tree.py` | 0 | The frozen 18-node, 42-edge denominator and its intentional pre-proof M3 snapshot remain valid. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Rev-5.6 structural standard passed for 15 assurance groups and 1546 targets. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 ordered uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py show THM-M-1080` | 0 | Rank 522; accepted lifecycle remains planned; theorem-complete remains false. |
| `git diff --check -- Stage1_Instances/THM-M-1080 .stage1-worker-selftest.json` | 0 | No scoped whitespace diagnostics. |

The replay reused only the canonical pinned `.lake` artifacts through the automation-provided
worker symlink and wrote all new Lean objects under the temporary directory. No `lake update`,
`lake build`, dependency clone/fetch, or other `.lake` mutation was performed. This is warm
pinned-cache, fresh-output, dirty-worker, nonrelease evidence.

## Status Boundary

The receipt provisionally proposes closure of the 15 machine-required obligations and an `M0-L`
candidate. The integration lane alone may accept that proposal. The frozen registry and typed
graphs remain unchanged and truthfully retain their pre-proof `M3` snapshot; accepted closure is
still empty and the accepted vector remains `H2/M3/R3`. Later validation and release items,
master acceptance, H0, R0, provenance review, hermetic/offline replay, and independent verification
remain open. `audit_complete` and `theorem_complete` are false.
