# Source-statement crosswalk

| Claim component | Available source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Theory identity | `Docs/researches/math_theorems.md` names Ljusternik and Schnirelmann, gives 1930, and says "topological index and critical points" | none | Repository metadata only; not a citable theorem statement |
| Topological invariant | The gloss suggests an LS category/index | none located or checked | Normalization is unspecified; changing it changes the numerical conclusion |
| Critical-point result | The gloss suggests a category-to-critical-point lower bound | none located or checked | Space, function, critical-point notion, compactness assumptions, and exact inequality are absent |
| PDE/variational specialization | Manifest category is differential equations / PDE | none | No functional, PDE, boundary condition, or Palais-Smale-type hypothesis is named |

The familiar modern slogan that the LS category bounds the number of critical points is only a
candidate theorem family. It cannot be promoted to the canonical statement from the present
metadata: sources use different category normalizations and prove finite-dimensional,
infinite-dimensional, critical-point, and critical-value variants under different hypotheses.

The statement phase therefore requires a primary-source or authoritative-edition pinpoint with the
exact theorem text, definitions, assumptions, page/theorem number, and errata status. It must then
map each premise and the conclusion to a Lean expression and mutation-test the convention and
boundary cases. A modern secondary reference suitable for discovery, but not accepted here as H0
evidence, is O. Cornea, G. Lupton, J. Oprea, and D. Tanre, *Lusternik-Schnirelmann Category*,
Mathematical Surveys and Monographs 103, AMS (2003), DOI `10.1090/surv/103`.

No source theorem, Lean anchor, checked transport, or proof-body credit is claimed by this
crosswalk. The historical spelling variants "Ljusternik" and "Lusternik" must both be searched in
the later source audit.
