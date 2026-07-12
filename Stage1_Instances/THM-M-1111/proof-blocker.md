# Proof-phase blocker

Item: `S56-M-1111-PROOF`  
Base revision: `270e3fb34fda8c9a44c27d55bd2b9ac69b3c4945`  
Date: 2026-07-12

## First failed gate

The frozen root is not provable from its binders. `TaoVuFourMomentTarget` accepts an arbitrary
`FourMomentSemantics`, but that structure imposes no laws on `powerBound` (or on any other semantic
operation). `ProofBlocker.lean` constructs a lawful value whose statistic is always zero and whose
`powerBound` is always `-1`. All hypotheses of the target can then be met at `k = 1` and at a bulk
index, while the conclusion reduces to `0 <= -1`.

The kernel-checked declaration
`Stage1Instances.THM_M_1111.not_taoVuFourMomentTarget_counterSemantics` therefore proves the
negation of the exact frozen target at this instance. This is not evidence against the mathematical
Tao--Vu theorem. It shows that the semantic interface omitted the laws needed to connect its fields
to the paper. No proof body for the current root can be supplied without inconsistency, adding an
axiom, or changing the target.

## Commands and exact results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1111` | 0 | rank 551; planned; L0/rework-required; theorem incomplete |
| `LEAN=$(cd Formalizations/Lean && lake env which lean); LP="$(cd Formalizations/Lean && lake env printenv LEAN_PATH):Stage1_Instances/THM-M-1111"; LEAN_PATH="$LP" "$LEAN" -R Stage1_Instances/THM-M-1111 Stage1_Instances/THM-M-1111/Statement.lean -o Stage1_Instances/THM-M-1111/Statement.olean; LEAN_PATH="$LP" "$LEAN" -R Stage1_Instances/THM-M-1111 Stage1_Instances/THM-M-1111/ProofBlocker.lean; rm -f Stage1_Instances/THM-M-1111/Statement.olean Stage1_Instances/THM-M-1111/Statement.ilean` | 0 | pinned Lean 4.29.0 checked the countermodel; `#print axioms` reported only `[propext, Classical.choice, Quot.sound]` |
| `rg -n '(^\|[[:space:]])(sorry\|admit)([[:space:]]\|$)\|^[[:space:]]*axiom[[:space:]]' Stage1_Instances/THM-M-1111/ProofBlocker.lean` followed by `test $? -eq 1` | 0 | no forbidden proof devices or axiom declarations |
| `git diff --check -- Stage1_Instances/THM-M-1111` | 0 | no scoped whitespace errors |

The Lean recipe reused only the pinned environment exposed by `lake env`; it performed no update,
build, fetch, or dependency mutation. The pre-existing untracked `Formalizations/Lean/.lake` link
was not modified.

## Unblock condition

The statement phase must replace the unconstrained interface with an implemented model of random
Hermitian matrices, or add source-justified laws strong enough to derive the comparison estimate,
and then repeat statement mutation testing and freeze a new obligation denominator. That is a
statement/obligation-tree revision, not a permissible proof-phase weakening.

The proof node remains blocked at `M4`; theorem completion, validation, and release are not claimed.
Because the assigned proof phase did not close, no `.stage1-worker-selftest.json` is emitted.
