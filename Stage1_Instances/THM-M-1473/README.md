# THM-M-1473 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `CFL条件` (the
Courant-Friedrichs-Lewy condition). The repository provides the authors, the year 1928, and the
gloss `双曲型方程的稳定性条件` ("a stability condition for hyperbolic equations"). It supplies no
equation, scheme, mesh, definition of stability, quantifier order, hypotheses, or conclusion. The
catalog's `已验证` label is untrusted metadata and gives no source or proof credit.

The matching historical primary-source family was inspected: R. Courant, K. Friedrichs, and H.
Lewy, *Über die partiellen Differenzengleichungen der mathematischen Physik*, *Mathematische
Annalen* 100 (1928), 32-74, DOI `10.1007/BF01448839`. The Göttingen scan is identified by PURL
`GDZPPN002272636` and range `LOG_0005`. Printed page 33 states that convergence for hyperbolic
initial-value problems generally requires inequalities between mesh ratios determined by the
characteristics. Section II.2, printed pages 61-62, compares numerical and differential domains of
dependence and gives a nonconvergence regime for a wave-equation stencil; Section II.3 then proves
convergence under additional source-specific data and mesh hypotheses.

That source is much richer than the catalog gloss and contains several materially different
claims. The modern CFL theorem is normally a necessary numerical-domain-of-dependence condition
for convergence, not a generic sufficient "stability condition." The catalog does not select the
historical wave-equation case, a general domain-of-dependence necessity theorem, a scalar-advection
Courant-number bound, or any specific stability result. Picking one would substitute missing
mathematics.

`IntakeProbe.lean` checks pinned forward-difference and abstract coercivity interfaces. Neither API
defines the missing PDE, scheme, convergence/stability predicate, or domain-of-dependence bridge.
The bounded repository and pinned-mathlib search located no source-identical CFL declaration.

The provisional vector is `[H1, M4, R4]`: an exact primary source family and relevant passages are
identified, but the canonical claim, full assumption crosswalk, errata review, translation review,
and independent source approval remain open. All six downstream phases remain open in
`task-dag.json`. No exact statement, proof, accepted execution state, audit completion, theorem
completion, accepted receipt, or master acceptance is claimed.
