# THM-M-1455 rev-5.6 intake

`THM-M-1455` is the numerical-analysis catalog item `共轭梯度法` (conjugate gradient
method). The repository supplies only the gloss `对称正定系统的迭代解法` ("iterative solution
method for symmetric positive-definite systems"), attribution to Magnus Hestenes and Eduard
Stiefel, the year 1952, and an untrusted `已验证` label. These fields identify a method and theorem
family, not a binder-complete mathematical proposition.

## Intake result

This directory records a fail-closed `planned` instance. The Hestenes-Stiefel primary paper was
inspected, but it contains several materially different claims: the exact-arithmetic recurrence,
finite termination, residual orthogonality, conjugacy of search directions, error-functional
minimization, and monotone error estimates. The catalog does not select one of these as its root.
Choosing a convenient result at intake would add source-absent mathematics.

The linear-system method is also distinct from the separately cataloged nonlinear optimization
item `THM-M-1503`. No statement or evidence crosses that boundary.

## Formal boundary

`IntakeProbe.lean` elaborates pinned positive-definite-matrix and matrix-vector APIs adjacent to a
future encoding. A bounded exact-topic search found no conjugate-gradient declaration in pinned
mathlib or the repo-local Lean sources. This is an intake observation, not the exhaustive formal
anchor audit and not proof evidence.

The canonical mathematical statement and Lean expression remain null. The provisional vector is
`[H5, M4, R4]`: the catalog method label is not yet a stable proposition, although standard
conjugate-gradient theorems are established in the literature; no source-identical usable formal
artifact is credited; and no readable proof reconstruction can attach to an unfrozen root. All six
downstream tasks remain open. Neither audit completion nor theorem completion is claimed.
