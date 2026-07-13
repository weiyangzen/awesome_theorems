# THM-M-0487 rev-5.6 dossier

This directory is the fail-closed `planned` dossier for `THM-M-0487`, the weak (ternary) Goldbach
theorem. The frozen human claim is: every odd integer greater than five is a sum of three primes,
with repetition permitted.

An immutable source lead was inspected: Harald A. Helfgott, *The ternary Goldbach conjecture is
true*, arXiv:1312.7748v2. Its unnumbered Main Theorem says exactly that every odd integer greater
than five is a sum of three primes. The proof combines an analytic result above `10^27` with a
separate finite verification. Source admission, the full dependency and computation crosswalk,
errata review, and independent review remain open, so this is `H1`, not `H0`.

`Statement.lean` now freezes the exact natural encoding: it quantifies `n : Nat`, requires `5 < n`
and `Odd n`, and asks for three natural prime witnesses whose sum is `n`. Restricting the source's
integer input to naturals is exact because `n > 5` makes every admissible integer positive. The
module checks integer-domain and equality-orientation transports, all four required mutation classes, and the boundary
`7 = 2 + 2 + 3`; repeated summands and the even prime remain possible. The merely eventual theorem
owned by `THM-M-0508` is weaker and cannot substitute for this target.

The two narrow direct imports are `Mathlib.Algebra.Ring.Int.Parity` and
`Mathlib.Data.Nat.Prime.Defs`; deleting either makes the statement module fail.
`check_statement.py` preserves the explicit-expression and environment fingerprints. Neither
the statement definition nor the boundary witnesses prove the unbounded theorem.

Status boundary: self-tested statement proposal pending integration-lane acceptance. The provisional
root vector is `[H1, M3, R3]`; no H0, proof body, M0, R0, accepted state, audit completion, or theorem
completion is claimed. The authoritative and local task states remain untouched and open.

Registry version 1 now freezes 54 obligations and 297 edges across seven typed graphs. The proof
architecture separates the analytic range `n >= 10^27` from the finite range below it and expands the common
Fourier/major/minor-arc route and the finite prime-ladder/certificate route, and checks only their
conditional range recomposition in `ObligationTree.lean`. The exact endpoint arithmetic is checked;
the historical computation is not. See `obligation-tree.md` for the frozen route and boundary.

Obligation-tree status: self-tested proposal pending dependency-ordered master acceptance. The
analytic and finite-upper substantive packages remain `M4`, accepted proof state is empty, and the
root stays `[H1, M3, R3]`.
