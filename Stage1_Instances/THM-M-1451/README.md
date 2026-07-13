# THM-M-1451 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `QR算法` (the QR algorithm). The
catalog gives the gloss `特征值的QR迭代` (QR iteration for eigenvalues), attributes it to John
Francis and Vera Kublanovskaya in 1961, and labels it `已验证`. These uncited inventory fields name
a numerical-algorithm family; they do not select one binder-complete theorem or supply proof
evidence.

## Intake result

The basic unshifted iteration factors `A_(k-1) = Q_k R_k` and sets `A_k = R_k Q_k`. This supports
several different claims: the per-step unitary-similarity or characteristic-polynomial invariant,
conditional convergence to triangular form, convergence rates, Hessenberg preservation, and
correctness of shifted or implicit Francis variants. The catalog does not choose among them or fix
the scalar field, matrix class, QR convention, shift/deflation policy, convergence hypotheses,
topology, endpoint, rate, initial-flag/eigenvector genericity assumptions, or finite-precision
semantics. Selecting any one now would narrow or substitute the source.

Peter Arbenz's Chapter 4, *The QR Algorithm*, was inspected as an authoritative modern lead. Its
printed pages 63-64 state the basic recurrence, the identity
`A_k = Q_k^* A_(k-1) Q_k`, and a conditional distinct-eigenvalue-modulus convergence description.
The repository does not cite these notes, and the inspected passage itself sends the convergence
proof to a later chapter and Wilkinson. Francis's 1961/1962 articles and Kublanovskaya's publication
are historical bibliographic leads whose primary theorem text was not inspected. None is admitted
as an exact root or `H0` evidence.

Pinned mathlib contains QR-factor ingredients and a precise one-step invariant:
`Matrix.charpoly_mul_comm` shows that `Q * R` and `R * Q` have the same characteristic polynomial.
It also contains spectrum/characteristic-polynomial and triangular-matrix interfaces. A bounded
intake search found no QR-iteration or QR-convergence declaration. `IntakeProbe.lean` authenticates
these adjacent APIs only; it defines no target and supplies no proof credit.

The provisional vector is `[H1, M3, R3]`: published QR-algorithm sources and the modern statement
lead make a complete proof source plausible, but no complete source proof or exact mapping was
inspected or accepted; only interfaces and an invariant ingredient are identified for an unfrozen
root; and this dossier maps scope without reconstructing a selected proof. All six downstream
phases remain open. No exact Lean statement, accepted state, audit completion, theorem completion,
or master acceptance is claimed.
