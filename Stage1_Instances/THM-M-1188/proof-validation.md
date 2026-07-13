# THM-M-1188 proof-phase validation

Item: `S56-M-1188-PROOF`  
Base revision: `309f58b7a54d36653b3483a543c6378eea53882c`

## Implemented proof

`Proof.lean` proves the exact classical weak maximum principle frozen in
`Statement.lean`. For each positive epsilon it maximizes `u(x,t) - epsilon*t`
on a compact truncated cylinder with terminal time strictly below `T`. At a
positive-time spatial-interior maximizer, a linewise second-derivative test
gives a nonpositive Laplacian and a tangent-cone argument gives a nonnegative
one-sided time derivative. These signs contradict the strict perturbed heat
inequality. The remaining maximizer lies on the exact initial-or-lateral
parabolic boundary. A fixed maximum of `u` on that boundary makes the witness
independent of epsilon, and continuity extends the resulting estimate to the
terminal face.

The module provides the exact canonical declaration
`Stage1Instances.THM_M_1188.Proof.heatEquationWeakMaximumPrinciple`, inhabits
the frozen `AnalyticMaximumEngine`, and replays `ObligationTree.root_compose`.
No terminal face was added to the boundary and no regularity at `t = T` was
assumed.

## Commands and results

All commands used the automation-provided pinned `.lake` artifacts read-only.
No update, build, clone, fetch, or dependency mutation was run.

```text
cd Formalizations/Lean &&
  bash ../../Stage1_Instances/THM-M-1188/check_proof.sh
  exit 0: isolated --trust=0 elaboration of Statement, ObligationTree, and
  Proof passed; all 17 audited declarations reported exactly propext,
  Classical.choice, and Quot.sound

python3 Stage1_Instances/THM-M-1188/check_proof.py
  exit 0: receipt identity, source/input hashes, provisional closure boundary,
  M0-L classification, and worker packet passed

python3 Docs/tools/check_stage1_standard.py
  exit 0: rev-5.6 structural standard passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique uniform-L0 targets passed

python3 scripts/stage1_target.py show THM-M-1188
  exit 0: rank 383, planned, theorem_complete=false

python3 Stage1_Instances/THM-M-1188/check_obligation_tree.py
  exit 0: frozen registry and typed obligation graphs passed

rg -n '\b(sorry|admit)\b|^[[:space:]]*(axiom|unsafe|opaque)[[:space:]]' \
  Stage1_Instances/THM-M-1188/Proof.lean
  exit 1 with empty output: no prohibited placeholder or declaration

git diff --check -- Stage1_Instances/THM-M-1188 \
  .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics
```

## Status boundary

This is provisional worker proof evidence proposing `M0-L` for the exact
kernel root after master acceptance. It provisionally closes the frozen proof
route except `M1188-S-FOUNDATION`, `M1188-X-SOURCE`, and
`M1188-X-PROVENANCE`, which remain validation/source/release work. The accepted
state remains `H2/M3/R3`; validation, release, H0, R0, complete transitive
provenance and TCB review, hermetic cold replay, and independent validation
remain open. Neither audit completion, theorem completion, release readiness,
nor master acceptance is claimed.
