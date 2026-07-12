# THM-M-1289 release decision

Item `S56-M-1289-RELEASE` has the exact verdict **blocked**. The lifecycle remains `planned`, the
accepted root vector remains `[H2, M4, R3]`, and both `AUDIT-Z` and `THEOREM-Z` remain false. There
are no accepted receipt IDs. This is a tested negative release decision, not theorem completion or
master acceptance.

## Evidence reconciliation

The validation receipt provides provisional warm-cache kernel evidence for the exact statement,
conditional composition, positivity, and infinite smoothness. These local proof bodies do not close
the Aubin-Talenti theorem. `aubinTalentiTarget_of_remaining_components` still consumes the critical
PDE, function-norm finiteness, gradient-norm finiteness, and sharp-extremal components. Their frozen
IDs form the minimal mathematical root cut: `M1289-L-PDE`, `M1289-L-FUN-NORM`,
`M1289-L-GRAD-NORM`, and `M1289-T-EXTREMAL`.

The first failed gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`: the prerequisite validation receipt is
provisional, nonrelease, and not master accepted. The frozen typed graph also predates the positivity
and smoothness bodies, so release preserves the weaker authoritative state rather than promoting it.
The first release-specific failure is `S56-10.6-HERMETIC-COLD-BUILD`. H0/R0 review, complete trust
and supply-chain closure, offline restoration, independent clean runners, a minimal verifier,
mutation evidence, a deterministic bundle, and master reconciliation are absent.

## Validation

Commands ran from repository root on 2026-07-12. They reused the existing pinned `.lake` artifacts;
no update, build, clone, fetch, or intentional `.lake` mutation was performed.

```text
python3 Stage1_Instances/THM-M-1289/check_release.py
  exit 0; validation replay passed; blocked verdict and unchanged authority confirmed

python3 Docs/tools/check_stage1_standard.py
  exit 0; 15 assurance groups and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-1289
  exit 0; rank 460, planned lifecycle, theorem_complete=false

python3 -m json.tool Stage1_Instances/THM-M-1289/release-decision.json
  exit 0; release decision is valid JSON

git diff --check -- Stage1_Instances/THM-M-1289 .stage1-worker-selftest.json
  exit 0; no whitespace errors
```

Retry requires dependency-legal master acceptance and graph reconciliation, proof and composition
of the four open analytic components, then accepted audit, hermetic supply-chain, independent
verification, deterministic-bundle, and master release gates.
