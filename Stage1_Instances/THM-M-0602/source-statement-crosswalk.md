# Source-statement crosswalk

## Available record and candidate source

The repository inventory supplies the Chinese title, the gloss "simply connected h-cobordisms and
diffeomorphism", attribution to Stephen Smale, and the year 1962. Its `\u5df2\u9a8c\u8bc1` status is
explicitly untrusted under rev-5.6 and supplies no proof credit.

A primary-source candidate is Stephen Smale, *On the Structure of Manifolds*, American Journal of
Mathematics 84 (1962), 387-399. This bibliographic identification is a discovery anchor only. The
paper's exact theorem number/page, wording, definitions, proof boundary, corrections, and errata
have not been independently inspected in this intake, so it is not `H0` evidence. Smale's related
1961 work on the generalized Poincare conjecture must not be silently substituted for the selected
h-cobordism statement.

## Crosswalk

| Repository/source phrase | Provisional mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "h-cobordism" | cobordism whose two end inclusions are homotopy equivalences | smooth cobordism, boundary decomposition, inclusions, homotopy equivalences | included; exact encoding open |
| "simply connected" | fundamental-group condition on the relevant spaces | path connectedness and trivial fundamental group, or source-equivalent predicate | bearer and formulation open |
| high dimension | range in which Whitney/handle methods apply | manifold dimension and exact lower-bound hypothesis | bound convention open |
| "diffeomorphism" | product trivialization, implying diffeomorphic ends | relative smooth equivalence `W ~= M0 x I` and induced end diffeomorphism | exact relative condition open |
| compact smooth manifolds | classical differential-topology category | compactness, smooth structures, boundary/collar interfaces | included provisionally |
| Stephen Smale / 1962 | historical and bibliographic locator | no machine-proof component | candidate paper identified only |

## Source and machine boundary

The repository-wide search found no theorem-specific Lean declaration for this target. It did find
legacy text that identifies h-cobordism/s-cobordism and the required handle, surgery, and
transversality infrastructure as unavailable or open; those files belong to other targets and are
discovery input only. This is not a complete pinned-mathlib or external-project anchor audit.

Before `H0`, an independent reviewer must inspect the chosen edition and approve the exact theorem
locator, definitions, every assumption, dimension convention, conclusion strength, proof boundary,
and errata status. Before statement credit, those approved components must map row by row to an
elaborated Lean expression. The subsequent anchor audit must separately search pinned mathlib and
credible Lean 4 projects at immutable revisions and inspect terminal proof-body provenance.
