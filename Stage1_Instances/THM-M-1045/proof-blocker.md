# THM-M-1045 proof-phase blocker

Item: `S56-M-1045-PROOF`  
Base revision: `3ec252ff03162db067bf77973c0a74a97d4bbe0a`  
Validation date: 2026-07-12

## First failed gate

The frozen statement is not currently a provable encoding of the Cameron-Martin theorem. Its
`WienerData.paleyWienerIntegral` field has only a measurability requirement, while the root target
quantifies over every `WienerData` and demands the RN density formula for that field.

`ProofBlocker.lean` changes only this unconstrained field to the measurable constant-one map. From
the frozen root it kernel-checks the resulting zero-direction consequence

```text
(translatedMeasure W.measure 0).rnDeriv W.measure =ae
  (fun _ => ENNReal.ofReal (Real.exp 1)).
```

The intended zero-direction density is the constant one function. This checked consequence shows
that the open density obligation cannot be truthfully implemented against statement version 1.
The statement phase must create a new registry version adding the required Paley-Wiener isometry,
Gaussian-law, and compatibility contract (or construct the integral rather than accepting it as
unconstrained data), then repeat statement and obligation-tree acceptance before proof execution.

No branch package or root proof was asserted. Machine status remains `M3`; the open cut set remains
`M1045-B-EQUIVALENCE`, `M1045-B-DENSITY`, and `M1045-B-SINGULARITY`. No worker self-test manifest is
written because the assigned proof phase is blocked rather than completed.

## Commands and results

All commands ran in this worker clone and reused the canonical pinned Lake environment. No Lake
update, build, dependency fetch, or dependency mutation ran.

| Command | Exit | Result |
|---|---:|---|
| `LEAN=$(lake env which lean); LP=$(lake env printenv LEAN_PATH); cd ../../Stage1_Instances/THM-M-1045 && LEAN_PATH="$LP" "$LEAN" Statement.lean -o /tmp/Statement.olean >/dev/null && LEAN_PATH="/tmp:$LP" "$LEAN" ProofBlocker.lean` (from `Formalizations/Lean`) | 0 | Frozen statement and the exact bad zero-density consequence elaborated with the pinned Lean kernel |
| `python3 scripts/stage1_target.py show THM-M-1045` | 0 | Rank 238, planned, uniform L0/rework-required, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1045` | 0 | No whitespace errors |
