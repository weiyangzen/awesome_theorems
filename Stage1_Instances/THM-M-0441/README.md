# THM-M-0441 rev-5.6 intake

This directory now freezes the first version of the Pila-Wilkie rational-point counting theorem:
Theorem 1.8, with height from Definition 1.3 and algebraic part from Definition 1.5 of the 2006
paper. `Statement.lean` elaborates the exact quantitative target with explicit o-minimality,
definability, affine rational height, algebraic part, finiteness, constant, and threshold.

The legacy `S1_M_087.lean` file remains discovery input only. Its `StatementShape` quantifies over a
`subpolynomialBound` predicate supplied as structure data and therefore is not accepted as the
classical theorem. The provisional root vector is `[H1, M3, R4]`. Elaboration is statement evidence,
not a proof or completion claim.

The source crosswalk records the inspected source and exact encoding. Downstream work remains open
in `task-dag.json`; statement validation is recorded in `validation.md`.
