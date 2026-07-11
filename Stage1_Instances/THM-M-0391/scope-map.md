# Scope map

## Included root

- Variables `x a y b : Nat`, in that order.
- Strict nontriviality hypotheses `1 < x`, `1 < a`, `1 < y`, and `1 < b`.
- Oriented equation `x ^ a = y ^ b + 1`, avoiding truncated natural subtraction.
- Conclusion fixing the unique tuple `(x,a,y,b) = (3,2,2,3)`.
- Boundary probes for bases or exponents at zero/one and for reversing the consecutive values.

## Candidate equivalent surfaces

- Consecutive nontrivial perfect-power values are exactly `8` and `9`.
- The positive-integer equation `x^a - y^b = 1` has the unique nontrivial solution.

These are not credited as equivalent until later Lean transports are checked. Negative integer
bases, rational powers, arbitrary rings, and uniqueness of exponent representations are excluded.

## Execution boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_005.lean` is a legacy discovery artifact. Its
`StatementShape` is a candidate formal target; its conditional wrappers and finite arithmetic
lemmas do not prove the universal theorem. This intake neither audits external formal candidates
nor freezes a proof-obligation tree, both of which belong to dependent DAG nodes.
