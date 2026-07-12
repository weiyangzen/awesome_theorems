# THM-M-0158 proof-phase validation

Item: `S56-M-0158-PROOF`  
Base revision: `c8fac337977b232bee6815b02e84cf13ef3d0d85`

`Proof.lean` supplies a direct inhabitant of the exact frozen
`WeingartenEquationsTarget`. It differentiates the squared unit-normal identity and the
normal/tangent orthogonality identities within the open parameter domain. The determinant
hypothesis makes the Gram matrix invertible, which both solves the coefficient system and proves
that the two coordinate tangents are independent. Adding the nonzero orthogonal normal gives an
ambient basis; equality of inner products against that basis finishes vector reconstruction.

The proof contains no `sorry`, `admit`, `axiom`, unsafe declaration, or oracle. The kernel axiom
report is exactly `[propext, Classical.choice, Quot.sound]`; in particular it contains no
`sorryAx`. This proof-phase receipt does not claim validation, release, H0, R0, hermetic replay, or
theorem completion, all of which remain later master-gated nodes.

## Exact commands and results

Commands ran from the repository root unless noted.

| Command | Exit | Result |
|---|---:|---|
| `LEAN_PATH=$(cd Formalizations/Lean && lake env printenv LEAN_PATH) $(cd Formalizations/Lean && lake env which lean) -o Stage1_Instances/THM-M-0158/Statement.olean Stage1_Instances/THM-M-0158/Statement.lean` | 0 | exact frozen statement compiled with the pinned Lake environment |
| `LEAN_PATH=Stage1_Instances/THM-M-0158:$(cd Formalizations/Lean && lake env printenv LEAN_PATH) $(cd Formalizations/Lean && lake env which lean) Stage1_Instances/THM-M-0158/Proof.lean` | 0 | direct proof elaborated; axiom report `[propext, Classical.choice, Quot.sound]` |
| `lake env lean ../../Stage1_Instances/THM-M-0158/Statement.lean` (cwd `Formalizations/Lean`) | 0 | canonical statement still elaborates |
| `python3 ../../Stage1_Instances/THM-M-0158/check_statement.py` (cwd `Formalizations/Lean`) | 0 | exact expression fingerprint unchanged; all four mutations distinguished |
| `rg -n '\\bsorry\\b|\\badmit\\b|^\\s*axiom\\b|unsafe|implemented_by' Stage1_Instances/THM-M-0158/Proof.lean` | 1 | no forbidden proof boundary found (expected no-match exit) |
| `git diff --check -- Stage1_Instances/THM-M-0158` | 0 | no whitespace errors |

Temporary `Statement.olean` is removed after validation and is not a delivered artifact.
