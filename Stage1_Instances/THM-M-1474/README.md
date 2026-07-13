# THM-M-1474 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog label
`von Neumann稳定性分析` (von Neumann stability analysis). The repository supplies only the
gloss `有限差分的稳定性分析` (stability analysis of finite differences), attributes it to
John von Neumann in 1947, and labels it `已验证`. A method-family label and topic gloss do not
form a truth-valued proposition with ordered binders, hypotheses, and a conclusion. The verified
label is untrusted metadata and supplies neither source nor proof credit.

Von Neumann analysis has materially different theorem forms for scalar or system schemes,
one-step or multistep recurrences, parabolic or hyperbolic equations, and periodic, infinite-grid,
or boundary-value settings. A source must also decide whether an amplification-factor or symbol
condition is necessary, sufficient, or equivalent to a specified stability notion. The catalog
fixes none of the equation, grid, stencil, coefficients, boundary treatment, norm, time horizon,
frequency range, power bound, parameter restrictions, or conclusion. Selecting the familiar
scalar condition `|G(theta)| <= 1` would invent proposition-changing mathematics.

Randall J. LeVeque's 2007 SIAM book *Finite Difference Methods for Ordinary and Partial
Differential Equations* was inspected only as a modern source-family lead. Its contents place
distinct von Neumann analyses in the parabolic chapter (Section 9.6, page 197) and hyperbolic
chapter (Section 10.5, page 219), alongside scheme-specific stability and CFL sections. The
catalog neither cites this book nor selects a theorem or page. No immutable pinpoint proposition,
assumption/proof/errata crosswalk, or independent review has been admitted, so it supplies no
`H0` credit.

Pinned mathlib supplies an `L2` Fourier isometry/Plancherel identity and abstract Banach-algebra
spectral-radius infrastructure. `IntakeProbe.lean` authenticates those adjacent interfaces only.
It does not define a finite-difference scheme, its Fourier symbol, or any source-selected stability
criterion and supplies no canonical statement or proof credit.

The provisional vector is `[H5, M4, R4]`. `H5` classifies the received catalog target as not
yet a stable proposition; it does not refute correctly stated von Neumann stability results. All
six downstream phases remain open. No H0, M0, R0, exact mathematical or Lean statement, accepted
proof state, audit completion, theorem completion, accepted receipt, or master acceptance is
claimed.
