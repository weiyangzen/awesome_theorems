# Source-statement crosswalk

## Candidate sources and attribution boundary

Christopher D. Sogge's monograph *Fourier Integrals in Classical Analysis* is a natural source for
the terminology and Fourier-integral-operator framework. The foundational local smoothing
estimates are also associated with Andreas Seeger, Christopher D. Sogge, and Elias M. Stein,
"Regularity properties of Fourier integral operators", *Annals of Mathematics* 134 (1991),
231-251, DOI `10.2307/2944346`, and later work of Mockenhaupt, Seeger, and Sogge. These are candidate
anchors, not a verified identification of the repository label.

An authoritative copy must be inspected before choosing an exact theorem, page, assumptions, and
edition. The label "Sogge local smoothing theorem" is too ambiguous to justify merging results or
attributing a later sharp exponent range to an earlier theorem. Bibliographic identification is
not H0.

## Crosswalk

| Repository phrase | Source component to freeze | Required Lean component | Intake status |
|---|---|---|---|
| "Sogge local smoothing theorem" | one numbered theorem at a stable edition/revision | one exact theorem expression | family scoped; exact anchor open |
| local smoothing | integrated-in-time improvement over fixed-time regularity | measurable time-parametrized output and space-time norm inequality | included; gain open |
| wave/FIO evolution | source operator, phase, amplitude, and curvature hypotheses | concrete operator or fully expanded analytic hypotheses | operator choice open |
| exponent range | dimension-dependent `p` and endpoint restrictions | explicit binders and inequalities for exponents | open; conjectural ranges excluded |
| derivative count | source Sobolev orders and epsilon/loss convention | exact fractional-regularity spaces and norm powers | open |
| uniform estimate | constant independent of the quantified input/frequency | quantified constant with dependencies exposed | included; dependencies open |

## Evidence boundary

No accepted source excerpt or Lean declaration was found in the target metadata. H0 requires an
independent, row-by-row check against the selected primary theorem, its referenced definitions, and
errata. M-credit requires an elaborated exact target and later inspection of actual declarations
and terminal proof bodies at immutable revisions.
