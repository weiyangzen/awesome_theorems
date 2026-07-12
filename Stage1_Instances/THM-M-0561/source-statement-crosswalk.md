# Source-statement crosswalk

## Source status

No primary source is accepted at intake. The underlying repository record in
`Docs/researches/math_theorems.md` contains only the name, generic attribution, century, and short
gloss; it gives no authorial source, title, edition, theorem number, page, assumptions, or errata.
It therefore supports neither `H0` nor an exact formal target.

Edgar H. Brown Jr., *Cohomology theories*, Annals of Mathematics 75 (1962), 467-484, is a candidate
primary anchor for representability. It has not been inspected here at a stable page/theorem anchor,
and intake does not assert that its exact conclusion is the Omega-spectrum formulation intended by
the metadata. A later audit must distinguish Brown representability in each degree from the extra
suspension compatibility used to assemble representing spaces into an Omega-spectrum. A modern
stable-homotopy text may explain that assembly but cannot silently replace the selected source.

## Crosswalk

| Repository phrase | Source-level ambiguity | Required Lean component | Intake disposition |
|---|---|---|---|
| "generalized cohomology theory" | reduced/unreduced, domain category, grading, exactness and wedge axioms omitted | concrete theory structure and universe/category constraints | blocking |
| "representation" | existence for each functor, compatible family, natural equivalence, or categorical classification | quantified representing objects plus exact naturality data | blocking |
| "Omega-spectrum" | loop equivalence may mean pointed homotopy, weak equivalence, or a model-category fibrancy condition | pointed spaces/spectra, loop functor, structure maps, equivalence predicate | blocking |
| all degrees | indexing and suspension signs are absent | integer grading and checked suspension compatibility | unresolved |
| "many mathematicians", "20th century" | no bibliographic or theorem anchor | edition, theorem/page, assumptions, attribution, and errata absent | unresolved |
| "verified" | formal system, artifact, and provenance absent | no kernel declaration or evidence packet | rejected as proof credit |

## Required source decision

The statement phase must choose exactly one source proposition and transcribe its hypotheses and
conclusion. If the desired result is obtained by combining a representability theorem with a
separate suspension/loop assembly theorem, the root and its source boundaries must say so rather
than citing only Brown representability. Every normalization of categories, grading, equivalence,
and naturality must be explicit.

Lean and external-project candidates belong to the later anchor-audit phase. Before `H0`, an
independent reviewer must verify the selected edition and exact theorem/page locations, definitions,
assumptions, attribution, and errata, and approve the row-by-row source-to-Lean crosswalk.
