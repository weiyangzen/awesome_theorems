# THM-M-1023 validation-phase evidence

Item: `S56-M-1023-VALIDATION`. Base revision:
`a9274bb02f984e5c74d2c97339044c6db8eb14f9` (tree
`c72a5af07dd4ab3f7088c516c74235e794a6de09`).

## Verdict

`self_tested_pending_master_acceptance`. The structured recipe freshly source-compiles the exact
statement, frozen conditional composition, all 20 vendored LeanLevy modules, the proof root, and a
separately written exact-root reconstruction at Lean trust level zero. Lean runs with a read-only
host root, fresh temporary output directory, cleared environment, fixed locale/timezone/thread
count, and an unshared network namespace. The proof and differential roots are sorry-free, and all
six inspected declarations report exactly `propext`, `Classical.choice`, and `Quot.sound`.

This is nonrelease evidence. The canonical pinned mathlib cache is shared and warm, the proof node
is only worker-provisional, and the observed axiom set has no accepted foundation profile or full
transitive declaration/TCB inventory. `Validation.lean` imports neither `Proof` nor
`ObligationTree`, but it uses the same worker, checkout, cache, and vendored terminal body; it is
differential corroboration, not a distinct signed verifier or independent proof body.

Structured authority remains intentionally weaker. `typed-graphs.json` predates the external proof
route and keeps the root open at `H1/M3/R4`; `anchor-audit.json` still records the earlier bounded
search result that found no exact external theorem. Validation does not rewrite predecessor
authority. No obligation is accepted, `audit_complete=false`, and `theorem_complete=false`.

## Commands and exact results

Commands were run on 2026-07-15 (`Asia/Shanghai`). No `lake update`, `lake build`, dependency
clone/fetch, or `.lake` write was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and all 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1 through 1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-1023
  exit 0: rank 499, planned, legacy artifacts unaccepted, theorem_complete=false

python3 Stage1_Instances/THM-M-1023/check_obligation_tree.py
  exit 0: 17 frozen obligations and 46 typed edges passed; the intentionally pre-proof graph
  remains root-open with M1023-T-FORWARD and M1023-T-REVERSE in its cut set

bash Stage1_Instances/THM-M-1023/check_validation.sh
  exit 0: network-isolated trust-zero replay compiled all 20 vendored modules, the exact statement,
  frozen composition, proof root, and differential root; all inspected axiom and sorry reports passed

python3 -I -B Stage1_Instances/THM-M-1023/check_validation.py
  exit 0: kernel, hygiene, selected provenance, tool, receipt, state-boundary, and packet checks passed;
  authority, foundation/TCB, cold hermetic, independent, H0, R0, and release gates failed closed

git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}
git -C Formalizations/Lean/.lake/packages/mathlib status --porcelain=v1
  exit 0: pinned revision 8a178386...ea95, tree bdc39a31...c2b, and empty status

python3 -m json.tool on validation-spec.json, validation-receipt.json, and the worker packet
PYTHONPYCACHEPREFIX=/tmp/stage1-m1023-validation-pycache python3 -m py_compile check_validation.py
  exit 0: structured artifacts parsed and Python compiled outside the repository

git diff --check -- Stage1_Instances/THM-M-1023 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

The predecessor `check_proof.py` is not rerun after installing the validation worker packet because
it is deliberately bound to the proof-phase base revision and proof self-test item. This validator
hash-binds that proof receipt and independently replays the actual Lean sources instead.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact kernel replay | provisional pass | Exact statement, conditional composition, proof root, and differential root freshly elaborate from vendored sources at trust zero. |
| Placeholder and unsafe boundary | pass | Lean transitive sorry reports and nested-comment/string-aware local and vendor source scans pass. |
| Trust observation | provisional pass | Six declarations report the same three observed axioms. The foundation profile and complete transitive TCB closure remain open. |
| Selected provenance | provisional pass | Target/registry hashes, reversible two-edit vendor reconstruction, upstream revision/archive hash, license, clean mathlib pin/tree/selected source and olean, and tool digests agree. |
| Structured authority | fail closed | Proof is only `[_]`; the frozen graph and stale negative anchor audit need dependency-ordered master reconciliation. |
| Hermetic release | fail closed | Shared warm `.lake`; no immutable clean checkout, empty-cache bootstrap, offline restoration, complete SBOM/TCB inventory, or deterministic bundle. |
| Independent verification | fail closed | Same worker, checkout, cache, and vendored terminal; no distinct identity, signature, independently provisioned runner, or independent minimal verifier. |
| Human and readable review | fail closed | No pinpoint independently reviewed `H0` source crosswalk or independently accepted `R0` reconstruction exists. |

The first failed node gate is `dependency.S56-M-1023-PROOF.master_acceptance`; the first failed release
gate is `S56-10.6-HERMETIC-COLD-BUILD`. The implementation is genuinely self-tested and proposes
only `[_]`. It grants no accepted `E1/M0-P`, `AUDIT-Z`, `THEOREM-Z`, release, or theorem-completion
credit.
