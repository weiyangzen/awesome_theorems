# Source-statement crosswalk

## Primary-source discovery anchor

Jean-Pierre Serre, "Homologie singuliere des espaces fibres. Applications", *Annals of
Mathematics*, second series, **54** (1951), 425-505, is the primary publication associated with the
homology spectral sequence of a fiber space. The statement phase must inspect a stable scan and
record the exact theorem/page range and definitions; this bibliographic anchor alone is not `H0`.
The 1951 French original and later reformulations need not use modern `E^2_{p,q}` language or the
same fibration and convergence conventions.

## Source-to-target crosswalk

| Repository component | Source question | Lean-side consequence | Intake disposition |
|---|---|---|---|
| "Serre spectral sequence" | which numbered result and formulation? | determines the canonical root, not merely a namespace | unresolved |
| "homology" | coefficients and local system? | fixes coefficient ring/module and monodromy binders | unresolved |
| "of a fibration" | exact fiber-space hypotheses? | fixes the topology/fibration object model | unresolved |
| spectral-sequence conclusion | page, differential, and convergence convention? | fixes indices, page objects, filtration, and abutment equality | unresolved |
| source label `已验证` | no artifact or theorem name supplied | provides no kernel or source-fidelity credit | excluded from evidence |

## Modern normalization candidate, not yet the claim

A common modern formulation has a first-quadrant homological spectral sequence with
`E^2_{p,q}` identified with `H_p(B; H_q(F; R))`, converging to `H_{p+q}(E; R)`, with the fiber
homology interpreted as a local coefficient system. This sentence is only a search template. It
must not become the canonical claim until every hypothesis and the meaning of convergence have
been crosswalked to the selected source.

Before `H0`, an independent reviewer must verify the edition, numbered statement/pages, invoked
definitions, assumptions, coefficient conventions, and errata. Before machine credit, the later
anchor audit must identify exact Lean declarations and immutable revisions; this intake makes no
claim that mathlib already contains the theorem.
