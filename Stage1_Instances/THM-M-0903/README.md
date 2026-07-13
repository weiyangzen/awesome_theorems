# THM-M-0903 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
`Bose-Shrikhande-Parker定理` (Bose-Shrikhande-Parker theorem). The catalog gives the three
authors, the year 1960, and only the gloss `Euler猜想的否定` (the negation of Euler's
conjecture). It supplies no definition of Euler's conjecture, quantifiers, order range, Latin-square
or orthogonality convention, theorem locator, or proof boundary.

The official 1960 paper by R. C. Bose, S. S. Shrikhande, and E. T. Parker was inspected as a
primary-source lead. Printed page 190 defines Latin squares and orthogonality. Printed page 202,
Theorem 10 states that there exist at least two orthogonal Latin squares of every order `v > 6`;
page 203 concludes that, among positive integers greater than two, 6 is the only order for which a
pair does not exist. This does not by itself select the repository root. The literal logical
negation of Euler's universal nonexistence conjecture needs only one counterexample, while the
paper's Theorem 10 is a stronger universal result. The source-exact final phrasing is restricted to
positive `v > 2`: a pair exists exactly when `v != 6`. Extending this to all positive orders would
add convention-sensitive orders one and two and require separate evidence.

The canonical human statement and Lean expression therefore remain null pending an independently
reviewed source-selection decision. `IntakeProbe.lean` checks only pinned finite-matrix and
bijectivity interfaces adjacent to a possible future encoding. A bounded repo-local and pinned-
mathlib search found no declaration named for Latin squares, orthogonal Latin squares, or the three
authors. Neither observation is a downstream formal-anchor audit or proof.

The provisional root vector is `[H1, M4, R4]`: a complete proof is published in an inspected named
primary source, but the exact repository claim, assumptions, errata, and source-to-node map are not
accepted; no usable formal artifact for the unselected root is credited; and no readable proof
reconstruction can attach before the root is fixed. All six downstream tasks remain open. No H0,
M0, R0, accepted state, audit completion, theorem completion, or master acceptance is claimed.
