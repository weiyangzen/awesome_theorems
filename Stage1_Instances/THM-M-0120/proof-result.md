# THM-M-0120 proof-phase result

Item: `S56-M-0120-PROOF`  
Date: 2026-07-12  
Base revision: `1371ca5a74c6cbc303b18e97c518ffe32b24e9ef`

## Verdict

Blocked. The frozen `MoriConeTheoremTarget` is false as stated, so this phase
cannot truthfully provide its requested proof body.

`Proof.lean` constructs `emptyData`, a `ConeTheoremData` instance over the
algebraic closure of the rationals. Its scheme morphism is the identity and all
six explicit input propositions hold. Its numerical space is `Real`, its
canonical pairing is the identity, and its declared Mori cone is the closed
singleton `{-1}`. This is permitted by the frozen structure because no field
relates `moriCone` or `canonicalPairing` to the scheme or to the asserted input
propositions.

The conclusion would force `-1` into `NonnegativePart` via the forward
direction of the decomposition equivalence. That entails `0 <= -1`, a
contradiction. Lean therefore checks:

```text
Stage1Instances.THMM0120.Proof.not_moriConeTheoremTarget :
  not MoriConeTheoremTarget.{0, 0, 0, 0}
```

The declaration's axiom report is exactly `[propext, Classical.choice,
Quot.sound]`; it contains no added axiom and no placeholder. This is blocker
evidence, not proof closure. The proof item remains open, the machine boundary
remains at most `M3`, and no audit-complete, theorem-complete, release, or
master-acceptance claim is made.

## Repair condition

The statement phase must be reopened. In particular, the input structure must
replace the unconstrained proposition fields and arbitrary numerical data with
definitions or hypotheses strong enough to connect the projective klt pair to
its actual numerical curve space, effective cone, and canonical pairing. The
exact repaired target and obligation registry must then be frozen and accepted
before proof execution resumes. Merely assuming `Conclusion` or any of its
branches would be circular and is not an acceptable repair.

## Validation

All commands ran in this worker clone and used the existing pinned Lake closure.
No update, fetch, clone, build, or dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0120` | 0 | rank 39, planned, theorem incomplete |
| `tmp=$(mktemp -d ./.m0120-proof.XXXXXX); trap 'rm -rf "$tmp"' EXIT; cp ../../Stage1_Instances/THM-M-0120/Statement.lean ../../Stage1_Instances/THM-M-0120/Proof.lean "$tmp/"; lake env lean -o "$tmp/Statement.olean" "$tmp/Statement.lean" && LEAN_PATH="$tmp:$(lake env printenv LEAN_PATH)" lake env lean "$tmp/Proof.lean"` from `Formalizations/Lean` | 0 | statement elaborated; countermodel theorem checked; axiom report printed without `sorryAx` |
| `git diff --check -- Stage1_Instances/THM-M-0120` | 0 | no whitespace errors |

No `.stage1-worker-selftest.json` is emitted because the assigned proof phase
is genuinely blocked rather than self-tested as complete.
