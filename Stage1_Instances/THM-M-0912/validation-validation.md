# THM-M-0912 validation handoff

Item: `S56-M-0912-VALIDATION`. Base revision:
`4a10a7a4ddff88e302d5a303b16dd687d9468f63` (tree
`730de242597680b39a7087d3204dfd1e6c41c60e`).

## Verdict boundary

The exact proof root and frozen composition kernel-replay with pinned Lean 4.29.0. A separately
written `Validation.lean` imports `Statement` but neither `Proof` nor `ObligationTree`, then closes
the unchanged `PascalIdentityTarget` directly through the pinned predecessor recurrence. The two
proof roots, the differential root, and their terminal recurrence declarations are sorry-free and
report exactly `propext`.

This is a truthful narrow validation result, not full rev-5.6 validation acceptance. The proof
prerequisite has only a provisional worker receipt, and the frozen typed graph still records the
pre-proof `[H1, M3, R4]` root. Direct terminal source/import/olean provenance passed, but complete
transitive declaration, compiled-object, foundation, bootstrap, and supply-chain trust closure did
not. The worker also reused the shared warm `.lake` closure, while the differential probe ran in
the same clone and cache. Thus the node verdict is `blocked`, and both `audit_complete=false` and
`theorem_complete=false` remain mandatory.

## Gate decisions

| Gate | Decision | Evidence or first boundary |
|---|---|---|
| Exact target and kernel replay | provisional pass | Statement, frozen composition, both proof roots, and the separately written exact root elaborated in a fresh temporary module directory. |
| Placeholder and unsafe paths | pass for inspected closure | Lean reported 12 covered declaration checks sorry-free; comment-aware scans found no prohibited local or terminal-source mechanism. |
| Axiom observation | provisional pass | All proof and differential declarations reported exactly `[propext]`, consistent with the provisional phase profile. |
| Direct provenance | pass | Pinned mathlib revision/tree/blob, `Basic.lean`, `Basic.olean`, direct imports, and local input hashes agree. |
| Complete trust/provenance | fail closed | No complete transitive declaration/body, olean, compiler/bootstrap, accepted foundation/TCB, or supply-chain closure. |
| Structured state and dependency | fail closed | `S56-M-0912-PROOF` lacks master acceptance; `typed-graphs.json` remains open M3 with no accepted nodes. |
| Hermetic reproduction | fail closed | Shared warm `.lake`; no immutable clean checkout, empty caches, outbound-network-denied cold replay, or offline restoration archive. |
| Independent verification | fail closed | Separate Lean implementation, but no distinct verifier identity, independently provisioned runner, signature, or independent receipt/graph verifier. |

## Commands and results

Commands ran in this isolated worker clone on 2026-07-13 (`Asia/Shanghai`). No `lake update`,
`lake build`, dependency clone/fetch, network operation, source edit, or `.lake` mutation ran.

```text
bash Stage1_Instances/THM-M-0912/check_proof.sh
  exit 0
  exact stdout SHA-256 c992e4e246af412dc7a18bf35e90239c8c91607c7905916109f87a42e27f2726
  isolated statement, obligation tree, and proof replay passed; ten declarations
  were sorry-free and every axiom report was exactly [propext]

python3 -B Stage1_Instances/THM-M-0912/check_validation.py
  exit 0
  exact temporary-module replay, separately written root, structured recipes,
  immutable local hashes, direct trust/provenance, pinned clean mathlib, receipt,
  worker handoff, and fail-closed release boundaries passed

python3 Docs/tools/check_stage1_standard.py
  exit 0: rev-5.6 standard, 15 assurance groups, and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique ordered targets at ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-0912
  exit 0: rank 1454, planned, L0/rework_required, theorem_complete false

python3 -m json.tool Stage1_Instances/THM-M-0912/validation-phase-spec.json
python3 -m json.tool Stage1_Instances/THM-M-0912/validation-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0: all three structured handoff artifacts parsed

PYTHONPYCACHEPREFIX=/tmp/stage1-m0912-validation-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-0912/check_validation.py
  exit 0: validator compiled outside the repository tree

git diff --check -- Stage1_Instances/THM-M-0912 .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics; the validator also checked final newlines and bytes
```

## Status boundary

The first node gate failure is
`dependency.S56-M-0912-PROOF.master_acceptance`; the first release gate failure is
`hermetic.cold_empty_cache_offline_replay`. The accepted root remains `[H1, M3, R4]`.
`M0912-S-FOUNDATION`, complete transitive provenance and trust, H0 source mapping, independently
reviewed R0, cold hermetic replay, distinct signed independent verification, deterministic release
bundling, `AUDIT-Z`, `THEOREM-Z`, release, and master acceptance remain open.
