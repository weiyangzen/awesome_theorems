# THM-M-1450 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label `幂迭代`
(power iteration, or the power method). The entire catalog gloss is `最大特征值的迭代方法` ("an
iterative method for the largest eigenvalue"), attributed only to "many mathematicians" in the
20th century. A method name and a goal do not determine a proposition with ordered binders,
hypotheses, a recurrence, and a conclusion. The attribution, date, and `已验证` label are untrusted
catalog metadata, not source or proof evidence.

The conventional family concerns normalized powers of a matrix or linear operator whose starting
vector has a nonzero component in a strictly dominant eigendirection. Materially different
theorems fit the catalog phrase. "Largest" can mean largest algebraic value, largest modulus, or
spectral radius; matrices can be real or complex, self-adjoint, normal, diagonalizable, or more
general; and convergence may concern projective direction, a sign/phase-adjusted unit vector, a
Rayleigh quotient, a norm ratio, a residual, or an error rate. Supplying any one version from
memory would invent proposition-changing mathematics.

This intake freezes that ambiguity. The provisional root vector is `[H5, M4, R4]`. `H5` classifies
the catalog method gloss as not yet a stable truth-valued proposition; it does not say that
standard power-method convergence results are false or open. `M4` records that no source-identical
formal target is usable, while `R4` records that a proof reconstruction cannot attach to an
unidentified root. Ordinary statement and proof execution remain blocked until an approved source
correction selects one exact convergence theorem.

A bounded search of pinned mathlib found eigenvector powers, matrix actions, and finite-dimensional
self-adjoint spectral decomposition, but no named or documented power-method convergence theorem.
`IntakeProbe.lean` authenticates those adjacent interfaces only. A SIAM/Netlib book section was
inspected as a secondary scope lead: it describes convergence to a dominant eigenpair under a
nonorthogonal-start condition and identifies the eigenvalue-modulus ratio controlling the rate.
It is not cited by the catalog, is not a pinpoint complete proof accepted for this target, and does
not settle all source choices, so it supplies discovery context only.

All six dependent phases remain open in `task-dag.json`. No canonical mathematical or Lean
statement, H0, M0, R0, accepted proof state, audit completion, theorem completion, accepted
receipt, or master acceptance is claimed.
