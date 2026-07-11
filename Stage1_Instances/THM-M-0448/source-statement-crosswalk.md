# Source-statement crosswalk

## Primary source anchor

Michael Harris and Richard Taylor, *The Geometry and Cohomology of Some Simple Shimura Varieties*,
Annals of Mathematics Studies 151, Princeton University Press, 2001, is the primary monograph
associated with this theorem. Its front matter, introduction, and terminal local-correspondence
results must be inspected in a stable edition before an exact theorem number and page span are
asserted. The bibliographic anchor alone is not immutable evidence and earns no `H0` credit.

The statement phase must record the exact labelled result, all definitions it incorporates, the
edition/page span, and any published errata. It must also distinguish what Harris--Taylor prove from
uniqueness characterizations or extensions credited to other authors.

## Metadata-to-source crosswalk

| Repository component | Source interpretation | Lean-side consequence | Intake disposition |
|---|---|---|---|
| "Harris--Taylor theorem" | theorem family arising from their Shimura-variety proof | a labelled root must be selected; the book as a whole is not a proposition | unresolved exact label |
| "local Langlands correspondence" | correspondence for `GL_n` over a nonarchimedean local field | concrete smooth-representation and Weil/Weil--Deligne objects are required | included subject |
| no rank or field qualifiers | likely quantified family, but coverage depends on the selected result | explicit binders and boundary cases are mandatory | blocking exact target |
| untrusted `已验证` | mathematical/source metadata only | supplies no Lean kernel or repository proof credit | rejected as evidence |

## Existing Lean discovery boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_062.lean` imports useful local-field, Galois-group,
general-linear-group, representation, and algebraic-geometry APIs. It also states that concrete
Weil--Deligne, smooth admissible representation, Shimura-variety, and cohomological infrastructure
is missing. Its abstract endpoint and correspondence records can be instantiated by assumptions and
therefore are not a formal statement or proof of local Langlands.

Before `H0`, an independent reviewer must compare every source hypothesis and conclusion with the
canonical claim, including normalization conventions and errata. Before machine credit, a later
anchor audit must identify exact Lean declarations and immutable revisions; this intake makes no
claim that a public Lean 4 closure exists.
