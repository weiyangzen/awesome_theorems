# THM-M-1083 validation phase

Item: `S56-M-1083-VALIDATION`

Base revision: `a9274bb02f984e5c74d2c97339044c6db8eb14f9`

This phase rechecks the proof-phase artifacts without adding mathematical proof content. The
network-isolated runner elaborates every one of the 15 vendored BrownianMotion modules, the exact
statement, the frozen conditional composition, the exact root, and a Lean trust probe at
`--trust=0`. It writes compiled output only to a fresh temporary directory and leaves the canonical
pinned `.lake` closure unchanged.

## Results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1083` | exit 0; rank 525, planned, L0/rework_required, theorem_complete false |
| `bash Stage1_Instances/THM-M-1083/check_validation.sh` | exit 0; all 15 vendored modules and exact root replayed with network denied; transitive placeholder scan passed; observed axioms were exactly `propext`, `Classical.choice`, and `Quot.sound` for the external terminal and exact proof root |
| `python3 -B Stage1_Instances/THM-M-1083/check_statement.py` | exit 0; canonical expression and four structural mutations passed |
| `python3 -B Stage1_Instances/THM-M-1083/check_obligation_tree.py` | exit 0; frozen 20-node registry and seven typed graphs passed with the pre-proof root intentionally open |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --porcelain=v1` | exit 0; empty output, pinned dependency worktree clean |
| `python3 -B Stage1_Instances/THM-M-1083/check_validation.py --skip-kernel-replay` | exit 0 after the separately recorded runner; structured receipt, freshness, inverse source reconstruction, tool identities, trust observations, and fail-closed boundaries passed |
| `git diff --check -- Stage1_Instances/THM-M-1083 .stage1-worker-selftest.json` | exit 0; no whitespace errors |

## Gate boundary

This is nonrelease, provisional worker evidence. The exact canonical root is kernel-inhabited, but
the proof prerequisite is not master-accepted and the vendored terminal follows an alternate route
that has not been reconciled with the frozen Markov/Borel-Cantelli graph. Consequently no frozen
obligation closure, accepted root, or debt-vector change is proposed.

`M1083-S-FOUNDATION`, complete transitive declaration/TCB/SBOM provenance, primary-source H0,
independently reviewed R0, cold empty-cache offline replay, deterministic release bundling, and a
distinct signed verifier remain open. `Validation.lean` is a same-worker trust probe importing the
existing proof, not an independent implementation or independently provisioned runner.

Verdict boundary: worker self-test may be handed off as `[_]`; `audit_complete=false` and
`theorem_complete=false`.
