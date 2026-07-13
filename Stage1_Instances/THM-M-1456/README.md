# THM-M-1456 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
`预处理技术` (preconditioning techniques). The catalog supplies only the gloss
`加速迭代收敛的技术` ("techniques for accelerating iterative convergence"), attributes the
topic to many mathematicians in the twentieth century, and labels it `已验证`. A technique name
and purpose do not form a truth-valued proposition with ordered binders, hypotheses, and a
conclusion. The verified label is untrusted metadata and supplies neither source nor proof credit.

Numerical preconditioning can mean an invertible equivalent transformation of a linear system, a
stationary-iteration spectral-radius result, a condition-number bound for preconditioned conjugate
gradients, an algorithm-specific Jacobi/SSOR/incomplete-factorization/multigrid construction, or a
practical setup-cost versus iteration-count claim. The catalog selects none of these. It does not
fix the problem class, scalar field, matrix or operator domain, iterative method, preconditioner
side, invertibility or positivity assumptions, convergence metric, comparator, tolerance,
arithmetic model, or performance conclusion.

The Netlib electronic edition of *Templates for the Solution of Linear Systems*, second edition,
was inspected as an authoritative specification lead. Chapter 3 defines a preconditioner as a
matrix effecting an equivalent same-solution transformation intended to improve spectral
properties, illustrates left preconditioning by `M^-1 A x = M^-1 b`, distinguishes left, right,
and symmetric variants, and explicitly treats construction/application cost as a tradeoff. The
source uses conditional language: spectral properties may improve. It does not supply one
universal acceleration theorem matching the catalog slogan, and the catalog does not cite it.

The provisional vector is `[H5, M4, R4]`. `H5` classifies the received method gloss as not yet a
stable proposition; it does not refute standard preconditioning results. `M4` records that no exact
formal target or usable proof artifact has been identified for the unfrozen root. `R4` records that
no source-faithful proof reconstruction can attach to it. `IntakeProbe.lean` authenticates only
adjacent pinned matrix, positivity, norm, and fixed-point interfaces. All six downstream phases
remain open. No exact statement, proof body, accepted state, audit completion, theorem completion,
or master acceptance is claimed.
