# THM-M-0205 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label `莫利定理`
(Morley's trisector theorem). The catalog attributes it to Frank Morley in 1899, supplies only the
gloss `三角形角三等分线交点构成等边三角形` (the intersections of a triangle's angle
trisectors form an equilateral triangle), and labels it `已验证`. That label is untrusted metadata,
not a source audit, an exact Lean proposition, or proof evidence.

The gloss identifies the classical theorem family but does not determine one proposition. A
triangle has six interior trisector rays, while their supporting lines also participate in external
and directed variants. The catalog does not select the three pairs adjacent to the three sides,
define their intersections, fix internal rays versus full lines, state triangle nondegeneracy and
orientation, or choose equal side lengths versus equal angles as the equilateral conclusion.
Intake does not silently supply those clauses.

Taylor and Marr's paper *The six trisectors of each of the angles of a triangle* was inspected at
the immutable Cambridge DOI record. Section 2, printed page 119, states the familiar internal case:
the intersections of pairs of trisectors adjacent to the same side form an equilateral triangle.
It also records that Morley's broader unpublished result involved internal and external trisectors.
The paper is a strong proof-source lead, but the catalog does not cite it and no independent
source/edition/errata review is recorded. It supports provisional `H1`, not `H0`.

Pinned mathlib provides Euclidean affine angles, triangle noncollinearity, angle-sum, sine-law,
isosceles-converse, and distance interfaces. `IntakeProbe.lean` authenticates those APIs. A bounded
search found no Morley, angle-trisection, or equilateral-triangle root declaration. The checked APIs
are substrate, not a formal candidate or proof.

The provisional root vector is `[H1, M4, R4]`: a complete published human proof lead is known but
the exact catalog-to-source statement and assumptions are not accepted; no usable exact Lean
artifact is credited; and no source-faithful readable reconstruction exists. `instance.json` is
the structured scope authority, while `task-dag.json` keeps all six downstream phases open. No
canonical statement, H0, M0, R0, accepted execution state, audit completion, theorem completion,
or master acceptance is claimed.
