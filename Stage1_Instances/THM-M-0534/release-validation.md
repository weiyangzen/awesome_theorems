# THM-M-0534 release decision handoff

## Exact verdict

`S56-M-0534-RELEASE` is **blocked**. The lifecycle remains `planned`; the accepted intake vector
remains `[H2, M3, R4]`; `audit_complete=false`; and `theorem_complete=false`. There are no accepted
receipt IDs and no theorem-completion promotion.

The first node gate to fail is dependency acceptance. `S56-M-0534-VALIDATION` is `[_]` worker
evidence with `support_state=provisional_worker_selftest`, not a master-accepted prerequisite. The
first specifically release-grade failure is section 10.6 cold hermetic replay: validation reused
the shared warm `.lake` artifacts rather than a new empty-cache, network-denied environment.

## Evidence reconciliation

The exact root and the frozen child-to-parent composition route elaborate. An independently written
Lean module reconstructs that root without importing `Proof.lean` or `ObligationTree.lean`. All
three routes terminate at pinned mathlib's `ShortExact.homology_exact1`, `homology_exact2`, and
`homology_exact3` family, and Lean observes only `propext`, `Classical.choice`, and `Quot.sound`.
This is strong provisional evidence of exact kernel closure through pinned bodies, but it is not an
accepted `E1` receipt or release evidence.

The structured graph is stale by design: its frozen pre-proof snapshot still records
`root_closed=false` and `M1`. Only the integration lane may reconcile authoritative state. Human
source status remains `H2` because pinpoint primary-source, assumptions, errata, node crosswalk,
and independent review are absent. Readability remains `R4` because there is no independently
reviewed complete node-anchored reconstruction. Consequently `AUDIT-Z` also remains blocked.

Further release evidence is absent for complete transitive provenance/TCB closure, an immutable
clean snapshot, cold and offline reproduction, SBOM/licenses, two separately provisioned signed
attestations, an independent minimal verifier, protected CI and adversarial gates, and a
deterministic content-addressed bundle.

## Validation

Commands were run from base revision `eef00eab3acabcc58485ecd6cbe0a15a23e9bbf7` on 2026-07-12:

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0534
  exit 0: rank 591; lifecycle planned; theorem_complete=false

python3 Stage1_Instances/THM-M-0534/check_validation.py
  exit 0: exact proof and independent root reconstruction kernel-replayed;
  release-grade graph, hermetic, provenance, and independent-runner gates fail closed

python3 Stage1_Instances/THM-M-0534/check_release.py
  exit 0: blocked decision, provisional dependency, stale graph, false terminal
  booleans, and release cut set agree

python3 -m json.tool Stage1_Instances/THM-M-0534/release-decision.json
  exit 0: valid JSON

git diff --check -- Stage1_Instances/THM-M-0534 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

No update, build, dependency fetch, clone, or `.lake` mutation was performed. The pre-existing
untracked `.lake` symlink is excluded from changed paths and is not release evidence.

## Retry boundary

The integration lane must accept the dependency chain and reconcile the root graph. A separately
provisioned release lane must close H0/R0 reviews, full trust and provenance, hermetic and
independent reproduction, supply-chain and CI gates, and deterministic bundle verification. Only
the master may accept the terminal decision.
