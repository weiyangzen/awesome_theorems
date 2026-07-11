# THM-M-0106 release decision

Item: `S56-M-0106-RELEASE`

Base revision: `1ec654c416270f261b365f46f5f2409b65d3f839`

Decision time: `2026-07-11T20:20:50Z` (`2026-07-12` Asia/Shanghai)

## Exact verdict

Release is **blocked**. The lifecycle remains `planned`; `AUDIT-Z` and
`THEOREM-Z` are both blocked, and `theorem_complete` remains false. There are
no accepted receipt IDs. This is a self-tested negative release decision, not
theorem completion or master acceptance.

The first failed gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`. The validation
prerequisite is a provisional worker receipt, explicitly non-release-grade,
and has not been master accepted. The accepted root vector therefore remains
`H4/M2/R4`. The proof and validation receipts support a provisional `M0-W`
proposal for the exact root through pinned mathlib's
`exists_finite_inj_algHom_of_fg`, but worker evidence cannot promote the
accepted graph.

## Gate reconciliation

The warm-cache kernel replay and separately written same-workspace probe pass
for the frozen target. Both report only `propext`, `Classical.choice`, and
`Quot.sound`; the scoped placeholder scan also passes. These facts do not
satisfy the remaining source, readability, trust, reproducibility, or release
gates.

`AUDIT-Z` is not available because the discovery and source-boundary
inventory, evidence states, and debt projections have not been completely
reconciled and accepted. In particular, the primary source remains H4 and
lacks an edition/theorem/page/assumption/errata crosswalk with independent
review. The readable surface remains R4 and lacks structured entries and an
independent reader receipt.

The first missing release-specific gate is
`S56-10.6-HERMETIC-COLD-BUILD`. No immutable clean snapshot, empty-cache
network-denied build, offline archive replay, complete transitive TCB,
SBOM/license bundle, deterministic evidence bundle, protected CI result, two
independent signed attestations, or independently implemented minimal verifier
exists. The validation probe ran in this worker checkout with the shared warm
dependency cache and therefore is not section 10.7 independent verification.

## Self-test record

Commands ran from the worker clone. No `lake update`, `lake build`, fetch,
clone, or dependency mutation was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0106
  exit 0: rank 30; lifecycle planned; theorem_complete=false

python3 Stage1_Instances/THM-M-0106/check_validation.py
  exit 0: exact proof and same-workspace independent probe elaborated; axiom,
  provenance, pin, receipt-hash, registry, and scoped hygiene checks passed

python3 Stage1_Instances/THM-M-0106/check_release.py
  exit 0: blocked decision, unaccepted validation dependency, unchanged
  H4/M2/R4 vector, false terminal booleans, and release cut set agree

python3 -m json.tool Stage1_Instances/THM-M-0106/release-decision.json
  exit 0: valid JSON

git diff --check -- Stage1_Instances/THM-M-0106 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

The pre-existing untracked `Formalizations/Lean/.lake` symlink was reused by
the narrow validator and was not modified. This makes the input nonrelease
evidence. The integration lane may accept this release-node handoff as an
honest blocked verdict, but only a later qualifying release run and master
reconciliation can decide a successful terminal transition.
