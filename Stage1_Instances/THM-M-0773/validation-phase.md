# THM-M-0773 validation-phase result

Item: `S56-M-0773-VALIDATION`  
Base revision: `32404187d6cee70b44ae90adf8d0d765752e5149`  
Validation time: `2026-07-12T17:41:08+08:00`

The node-scoped validator replays the exact statement and proof in a fresh
temporary olean directory. It also checks `Validation.lean`, a separately
written direct reconstruction that imports only `Statement` and does not use
the proof-phase wrapper or obligation composition theorem. Both roots report
exactly `propext`, `Classical.choice`, and `Quot.sound`.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 python3 Stage1_Instances/THM-M-0773/check_validation.py` | 0 | Exact proof and differential root elaborated; axiom set and pinned clean mathlib source passed; stale graph, hermetic, and independent gates failed closed. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets with ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0773` | 0 | Rank 781, planned, L0/rework-required, theorem incomplete. |
| `git diff --check -- Stage1_Instances/THM-M-0773 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

During validator authoring, the first `check_validation.py` run exited 1 because
the direct Lean executable did not inherit Lake's printed `LEAN_PATH`, so it
could not resolve the `Mathlib` module prefix. The validator was corrected to
set that pinned path explicitly; the final recorded run above exits 0.

The validator invokes the existing pinned Lean 4.29.0 toolchain and mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. It performs no update,
build, clone, fetch, or dependency mutation.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | pass | Exact proof root and direct differential root elaborate. |
| Placeholder/unsafe scan | pass | Local checked modules and terminal mathlib source contain no prohibited mechanism. |
| Trust observation | provisional pass | Both roots print exactly the three disclosed classical axioms; full TCB closure is absent. |
| Local provenance | pass | Source hashes, frozen denominator, proof receipt, toolchain, manifest, and clean mathlib pin agree. |
| Structured-state freshness | fail closed | The immutable pre-proof graph still reports root `M3`; only the master may reconcile it. |
| Hermetic validation | fail closed | The worker reused shared warm `.lake`; there is no cold offline-restored cache, complete TCB/SBOM archive, or immutable clean snapshot. |
| Independent verification | fail closed | The differential implementation ran in this worker and cache, without a distinct identity, provisioned runner, signature, or minimal independent verifier. |

The first dependency gate failure is proof-node master acceptance. The first
release gate failure is `hermetic.cold_empty_cache`. This provisional receipt
grants no `E0/E1`, accepted `M0-*`, `AUDIT-Z`, `THEOREM-Z`, release, theorem
completion, or master-acceptance credit.
