# THM-M-0926 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label `卡西尼恒等式`
(Cassini's identity). The catalog supplies the gloss `斐波那契数列的恒等式` ("an identity of the
Fibonacci sequence"), attributes it to Jean-Dominique Cassini in 1680, and labels it `已验证`.
The label is explicitly untrusted under rev-5.6.

The name strongly identifies the conventional identity family, but the received source does not
state a formula. It fixes no Fibonacci definition, index or value domain, lower bound, binder,
boundary convention, equation orientation, sign convention, source locator, or proof. Intake does
not silently replace those missing choices with a familiar formula.

MathWorld was inspected as a modern secondary statement lead. It gives
`F_(n-1) * F_(n+1) - F_n^2 = (-1)^n`, describes this as a special case of Catalan's identity, and
provides later printed references. It does not supply the catalog's claimed 1680 primary source,
an index domain, a complete proof crosswalk, corrections or errata, or independent review.

Pinned mathlib contains `Int.fib_succ_mul_fib_pred_sub_fib_sq` in
`Mathlib.Data.Int.Fib.Lemmas`, explicitly documented as Cassini's identity for every integer `n`.
That integer extension is a strong formal candidate, not source evidence selecting the root.
`IntakeProbe.lean` authenticates this and adjacent interfaces at the pinned revision without
declaring a wrapper or inspecting them as accepted proof evidence.

The provisional catalog-target vector is `[H5, M3, R4]`. `H5` classifies only the literal received
wording as not yet a stable proposition; it does not refute or question the standard Cassini
identity. `M3` records precise pinned statement and proof candidates while the source-approved
target and expression fingerprint remain absent. All six downstream phases remain open. No H0,
M0, R0, accepted state, audit completion, theorem completion, or master acceptance is claimed.
