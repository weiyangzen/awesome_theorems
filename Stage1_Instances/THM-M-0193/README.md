# THM-M-0193 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0193`, the catalog item
`勾股定理` (Pythagorean theorem). The repository supplies the gloss "in a right triangle, the sum
of the squares of the two legs equals the square of the hypotenuse," attributes it to the
Pythagorean school around 500 BCE, and labels it `已验证`. Those are untrusted catalog fields, not
an exact source crosswalk or machine-proof evidence.

An inspected public-domain Euclid edition states Book I, Proposition XLVII: in a right-angled
triangle, the square on the hypotenuse equals the sum of the squares on the other two sides. This
strongly identifies the intended theorem family. It does not by itself resolve the catalog's
historical attribution, the source edition to admit, the exact point ordering, nondegeneracy, or a
transport from Euclid's areas of constructed squares to squared real distances. No independent
source review is recorded, so this is an `H1` source lead rather than `H0` evidence.

Pinned mathlib has a direct affine-distance candidate,
`EuclideanGeometry.dist_sq_eq_dist_sq_add_dist_sq_iff_angle_eq_pi_div_two`, plus vector variants.
`IntakeProbe.lean` authenticates those interfaces and their reported axioms. The candidate is an
iff over possibly degenerate real Euclidean affine spaces, whereas the received claim is a forward
triangle theorem. Selecting its stronger scope or silently projecting one direction belongs to the
statement and anchor-audit phases, not intake.

The provisional vector is `[H1, M3, R4]`: an exact human-source admission and crosswalk remain
open; a direct pinned formal interface exists but is not yet the frozen root or credited proof; and
there is no accepted source-faithful reconstruction. `instance.json` is the structured scope
authority, and `task-dag.json` leaves all six downstream phases open. No canonical Lean statement,
accepted proof state, audit completion, theorem completion, or master acceptance is claimed.
