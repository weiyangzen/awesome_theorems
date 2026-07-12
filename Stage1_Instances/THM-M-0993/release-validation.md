# THM-M-0993 release decision handoff

## Exact verdict

`S56-M-0993-RELEASE` is **blocked**. The lifecycle remains `planned`, the accepted root vector
remains `[H1, M3, R3]`, and both `audit_complete` and `theorem_complete` remain false. No receipt is
accepted and neither `AUDIT-Z` nor `THEOREM-Z` is claimed.

The first node gate failure is `S56-10.2-DEPENDENCY-ACCEPTANCE`: validation is provisional worker
evidence, explicitly `release_grade=false`, and has no master acceptance. The first intrinsic
release failure is `S56-10.6-HERMETIC-COLD-BUILD`.

## Evidence reconciliation

The frozen exact root, local composition, and a separately implemented reconstruction all
kernel-elaborate against pinned mathlib. The observed axiom profile is exactly `propext`,
`Classical.choice`, and `Quot.sound`, and the placeholder scan passes. This is meaningful provisional
machine evidence, but it ran in one mutable worker checkout using the shared warm canonical `.lake`
cache. The frozen typed graph predates proof closure and still records an open `M1` root. The weaker
accepted structured state therefore wins; release does not promote the intake vector.

`H0` remains open because the primary-source theorem/premise/errata crosswalk lacks independent
acceptance. `R0` remains open because there is no structured node-by-node reconstruction with an
independent reader receipt. Complete transitive body provenance and TCB evidence, cold offline
reproduction, SBOM/licenses, two independently provisioned signed attestations, a distinct minimal
verifier, protected CI mutation gates, and a deterministic release bundle are absent.

## Self-test

Commands were run from base revision `f3a78c922f6edd8503e644c9b0b350f72940ac0b` on 2026-07-12:

```text
python3 Stage1_Instances/THM-M-0993/check_release.py
  exit 0: reconciled hashes and authority passed; narrow validation replay passed;
  blocked verdict, unchanged H1/M3/R3, and false terminal decisions agreed

cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0993/Proof.lean
  exit 0: exact root and all local proof declarations elaborated; reported propext,
  Classical.choice, and Quot.sound

cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0993/Validation.lean
  exit 0: independently reconstructed exact root elaborated; reported the same axioms

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0993
  exit 0: rank 273, lifecycle planned, theorem_complete=false

python3 -m json.tool Stage1_Instances/THM-M-0993/release-decision.json
  exit 0

git diff --check -- Stage1_Instances/THM-M-0993 .stage1-worker-selftest.json
  exit 0
```

No `lake update`, `lake build`, dependency clone/fetch, network operation, or `.lake` mutation was
performed. The pre-existing untracked `.lake` symlink is excluded from changed paths and is not
release evidence.

## Retry boundary

The integration lane must accept the prerequisite chain and reconcile fresh authoritative root
state. A separately provisioned release lane must then close H0/R0 review, complete provenance and
trust, hermetic and independent reproduction, supply-chain and CI gates, and deterministic bundle
verification. Only the master may accept the release item.
