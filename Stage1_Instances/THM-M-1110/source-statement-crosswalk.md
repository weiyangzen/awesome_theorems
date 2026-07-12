# Source-statement crosswalk

## Repository record and candidate sources

The repository inventory supplies the title "Erdos-Schlein-Yau theorem", the authors
Erdos/Schlein/Yau, the year 2010, and the gloss "universality of Wigner matrices". Its `已验证`
field is explicitly untrusted under rev-5.6. It gives no theorem number, ensemble, observable,
hypotheses, or convergence mode, so it cannot by itself identify an exact proposition.

A primary candidate matching the three named authors is Laszlo Erdos, Benjamin Schlein, and
Horng-Tzer Yau, *Universality of Random Matrices and Local Relaxation Flow*, **Inventiones
Mathematicae** 185 (2011), 75-119, DOI `10.1007/s00222-010-0302-7`, preprint arXiv:0907.5605.
The 2010 DOI/publication history may explain the inventory year, but this intake has not inspected
a pinned copy theorem by theorem. Exact locators, hypotheses, corrections, and which result the
repository intended remain open.

Another closely matching primary candidate is Laszlo Erdos, Jose Ramirez, Benjamin Schlein,
Terence Tao, Van Vu, and Horng-Tzer Yau, *Bulk Universality for Wigner Hermitian Matrices with
Subexponential Decay*, **Mathematical Research Letters** 17 (2010), 667-674. It is not an
Erdos-Schlein-Yau-only source and must not be substituted merely because its date and topic fit.
Related local-law and level-repulsion papers are supporting genealogy, not automatically the root
statement. All entries here are discovery anchors rather than `H0` evidence.

## Crosswalk

| Repository/source phrase | Mathematical component to freeze | Required Lean component | Intake status |
|---|---|---|---|
| "Wigner matrices" | symmetry class, entry laws, centering, variance, and tails | probability space, measurable random matrix, independence and distribution predicates | family identified; exact ensemble open |
| "universality" | equality of the limiting local statistic with GOE/GUE | exact convergence predicate and Gaussian reference observable | intended conclusion identified; formulation open |
| local/bulk statistics | bulk energy and mean-spacing rescaling | ordered eigenvalues or correlation measures, semicircle density, scale map | included; encoding and normalization open |
| correlation functions | source's `k`-point observable and test class | finite point/correlation measure and integral against a test function | candidate observable; exact one open |
| energy averaging | averaged or fixed-energy theorem strength | averaging interval, integral, limit, and quantifier order | unresolved and proposition-critical |
| 2010 / named authors | bibliographic disambiguation | no machine-proof credit | ambiguous between publication history and related papers |

## Human and machine boundary

The repository-wide theorem-name search found no existing artifact for `THM-M-1110`. This intake
does not perform the later exhaustive formal-anchor audit and makes no claim about external Lean
projects or about mathlib support for the full random-matrix statement.

Before `H0`, an independent reviewer must inspect an immutable edition, select the exact theorem
and pinpoint locator, map every definition and assumption, check errata and later corrections, and
approve the row-by-row source mapping. Before statement credit, the selected claim must be mapped
to an elaborated Lean target without deleting energy averaging, strengthening tail assumptions,
changing the symmetry class, or replacing local statistics by the global spectral law.
