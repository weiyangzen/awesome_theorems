# Full study: `K₆` and `K₁,₃,₃` in dimension five

<a id="F1"></a>
## F1 — Frozen statement and conventions

The frozen declaration is
`Erdos1007.erdos_1007.variants.dimension_five_extremal` from revision
`2270d31e8dd611521f979de6d86da364930b7669`.  Its two outputs say that the
complete graph on six vertices and the complete tripartite graph with parts of
sizes one, three, and three each have dimension five and exactly fifteen
edges.  “Dimension” is interpreted as faithful unit-distance dimension: the
vertex map is injective, graph edges have distance one, and pairs in the same
tripartite part do not accidentally become unit edges.  Translation preserves
all distances.

Trust boundary: the provider declaration contains an unresolved source proof
and is used only for statement provenance.  No provider proof body is used.
The canonical Master must elaborate the frozen type and the claim-owned target
and recompute their bidirectional transport.

<a id="F2"></a>
## F2 — Edge inventory

Every pair of the six vertices of `K₆` is an edge, so the count is
`6·5/2 = 15`.  In `K₁,₃,₃`, edges occur exactly between different parts.  The
three part-pairs contribute `1·3`, `1·3`, and `3·3`, hence
`3 + 3 + 9 = 15`.  There are no within-part edges.

Exceptional cases: unordered pairs are counted once; loops are excluded; and
the singleton contributes to both of its cross-part products but never to a
within-part term.

<a id="F3"></a>
## F3 — `K₆` upper bound

Take the six vertices of a regular five-simplex of side length one in a
five-dimensional Euclidean space.  Equivalently, start with the six standard
basis vectors in `ℝ⁶`, subtract their barycentre, and rescale by `1/√2` inside
the five-dimensional hyperplane whose coordinate sum is zero.  Every two
vertices are a unit distance apart.  This is an injective realization of the
complete graph, so its dimension is at most five.

Formal anchor: the finite certificate records the `6 - 1 = 5` hyperplane
dimension and the edge count.  The Master-owned elaboration trace is the
boundary that connects this calculation to the provider’s `HasDimension`.

<a id="F4"></a>
## F4 — `K₆` lower bound

Suppose `p₀,…,p₅` is any unit-distance realization in `ℝᵈ`.  Translate so
`p₀ = 0` and set `vᵢ = pᵢ - p₀` for `1 ≤ i ≤ 5`.  Then
`‖vᵢ‖² = 1`.  From `‖vᵢ-vⱼ‖² = 1`, polarization gives
`⟪vᵢ,vⱼ⟫ = 1/2` for `i ≠ j`.  Therefore, for real coefficients `xᵢ`,

`‖∑ xᵢvᵢ‖² = 1/2·∑ xᵢ² + 1/2·(∑ xᵢ)²`.

If the linear combination is zero, the left side and hence the displayed
nonnegative right side is zero.  Every `xᵢ` is zero.  Thus the five vectors are
linearly independent, forcing `d ≥ 5`.  Combined with F3, `K₆` has dimension
exactly five.

Exceptional case: the argument uses all five displacements; deleting one only
establishes a weaker bound.  No assumption about orientation or coordinates is
made.

<a id="F5"></a>
## F5 — `K₁,₃,₃` upper bound

Write a five-dimensional Euclidean space as an orthogonal sum
`C ⊕ U ⊕ W`, with dimensions one, two, and two.  Choose `c ∈ C` with
`‖c‖² = 1/2`.  In `U`, choose an equilateral triple `u₁,u₂,u₃` centred at zero
with `‖uᵢ‖² = 1/2` and `⟪uᵢ,uⱼ⟫ = -1/4` for `i ≠ j`.  Choose an analogous
triple `w₁,w₂,w₃` in `W`.

Map the singleton to `0`, the second part to `aᵢ = c+uᵢ`, and the third part
to `bⱼ = c+wⱼ`.  Each `aᵢ` and `bⱼ` has norm one, so every singleton edge has
length one.  Orthogonality gives `⟪aᵢ,bⱼ⟫ = ‖c‖² = 1/2`; hence every
cross-edge has squared length `1+1-2·(1/2)=1`.  Within either three-vertex
part, squared distance is `1/2+1/2-2·(-1/4)=3/2`, not one.  The seven images
are distinct.  This is a faithful realization in dimension five.

<a id="F6"></a>
## F6 — `K₁,₃,₃` lower bound

Consider any faithful realization and translate the singleton `z` to zero.
Call the other parts `A={a₁,a₂,a₃}` and `B={b₁,b₂,b₃}`.  Singleton edges give
`‖aᵢ‖=‖bⱼ‖=1`.  Cross edges give
`⟪aᵢ,bⱼ⟫=1/2` for every `i,j`.

Let `U = span{a₂-a₁,a₃-a₁}` and
`W = span{b₂-b₁,b₃-b₁}`.  Three distinct points on a sphere cannot be
collinear: a line meets a sphere in at most two points.  Injectivity therefore
makes both `U` and `W` two-dimensional.  Subtracting two cross-inner-product
equations shows every generator of `U` is orthogonal to every `bⱼ`, and every
generator of `W` is orthogonal to every `aᵢ`; in particular `U ⟂ W`.

The orthogonal sum `U ⊕ W` is four-dimensional.  It cannot contain both `a₁`
and `b₁`: since `a₁ ⟂ W` and `b₁ ⟂ U`, membership would force
`a₁ ∈ U` and `b₁ ∈ W`, which would give `⟪a₁,b₁⟫=0`, contradicting the
cross-edge value `1/2`.  Thus their span adds at least one direction beyond
`U ⊕ W`; the ambient dimension is at least five.  Together with F5, the
dimension is exactly five.

Exceptional cases: injectivity is essential to rule out a collapsed triple;
the cross-edge value is nonzero, so the common direction cannot disappear;
and no same-part distance is silently treated as an edge.

<a id="F7"></a>
## F7 — Composition and downstream use

F2 supplies both edge equalities.  F3–F4 supply the exact dimension of `K₆`.
F5–F6 supply the exact dimension of `K₁,₃,₃`.  Pairing those four conclusions
in provider order yields the frozen conjunction.  The result is used only as
the one mathematical completion for `S5-CLM-00003561` and its frozen Stage6
alias `S6-CLM-00005346` / `S6-VAR-00000050`; it creates no second claim.

The worker performs only the task-local no-Lean preflight.  Cold trust-zero
Lean replay, elaborated-expression equality, the complete transitive constant
census, and semantic-substitution mutations remain mandatory independent
Master recomputations over harvested bytes.
