# THM-M-0973 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog entry named the Kim-Vu
inequality. The repository supplies the year 2000 and only the gloss `多项式集中不等式`
("polynomial concentration inequality"). Its attribution `Jeong Han Han/Van Vu` contains an
unresolved catalog error: bibliographic metadata for the likely paper gives Jeong Han Kim and Van
H. Vu. The adjacent `已验证` label is untrusted inventory metadata, not source or kernel evidence.

The metadata strongly points to Jeong Han Kim and Van H. Vu's 2000 paper *Concentration of
Multivariate Polynomials and Its Applications*. DOI and publisher metadata confirm the authors,
title, journal, date, and pages. The accessible abstract says the paper studies a multivariable
polynomial with positive coefficients evaluated at independent zero-one random variables and gives
a condition for strong concentration around its mean. The full primary theorem text and formulas
were not available for statement-level inspection, so intake does not promote a remembered or
secondary Kim-Vu formula into the canonical root.

Material choices remain open: which numbered result or variant the catalog owns; the variable
index and probability spaces; Bernoulli parameters; whether the polynomial is multilinear or is
first multilinearized; coefficient domain and positivity; degree convention; the exact family of
partial or directional derivatives; maximum versus average derivative expectations; normalization,
constants, auxiliary parameters, tail event, and lower/upper/two-sided conclusion; and all zero,
constant, degree-zero, or vanishing-parameter cases. These are proposition-changing choices that
must come from an admitted source and independent review.

`IntakeProbe.lean` authenticates only adjacent pinned mathlib interfaces for multivariate
polynomials, evaluation, partial derivatives, independent functions, and Bernoulli product
measures. A bounded search found no Kim-Vu or polynomial-concentration declaration in repo-local
Lean or pinned mathlib. The probe and search are feasibility observations, not an exhaustive anchor
audit, an exact target, or proof evidence.

The provisional vector is `[H1, M4, R4]`: a credible primary-paper lead and broad result family are
known, but the exact statement, incorporated definitions and assumptions, proof boundary, errata,
catalog correction, and independent review remain open; no usable exact formal artifact is located;
and no source-faithful reconstruction exists. All six downstream phases remain open. No H0, M0,
R0, accepted execution state, audit completion, theorem completion, or master acceptance is claimed.
