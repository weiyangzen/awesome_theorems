# Source-statement crosswalk

The authoritative repository record at intake says
`与标准球同伦等价但不微分同胚的流形` ("a manifold homotopy equivalent to
the standard sphere but not diffeomorphic to it"). Its `已验证` label is
explicitly untrusted under rev-5.6 and supplies no machine-proof credit.

| Claim component | Human source anchor | Lean target at intake | Assessment |
|---|---|---|---|
| Existence of a nonstandard differentiable structure on a sphere | John Milnor, *On manifolds homeomorphic to the 7-sphere*, Annals of Mathematics (2) 64 (1956), 399-405 | None selected | Primary historical proof source identified; direct edition, theorem/page-to-claim mapping, assumptions, and corrections remain unaudited |
| Dimension | Milnor's title and construction concern dimension seven | Unselected dimension parameter | The repository phrase omits `7`; selecting it is a source-resolution decision for the statement phase |
| Topological comparison with the standard sphere | The primary paper's advertised result is homeomorphism to the 7-sphere | No topology witness type selected | Homeomorphism implies homotopy equivalence, but the converse fails in general; the two formulations must not be treated as definitionally interchangeable |
| Smooth distinction | The historical result distinguishes the constructed smooth manifold from the standard sphere up to diffeomorphism | No `Diffeomorph`-based expression selected | Orientation conventions and the exact characteristic-class or cobordism obstruction must be mapped from the primary source |
| Concrete construction | The historical examples arise from certain 3-sphere bundles over the 4-sphere | Future construction node only | Bundle conventions, parameter restrictions, total-space smoothness, and the exact example require primary-text audit |
| Repository formalization status | The source metadata says `已验证` | No declaration or module located at intake | Metadata is discovery input only; it does not establish a public Lean artifact or repo-local closure |

The source phrase permits several inequivalent formal targets. For example, an
existential theorem over an unspecified dimension is not the same statement as
existence of an exotic smooth structure specifically on `S^7`. Likewise,
homotopy equivalence alone does not express the defining homeomorphism
condition normally used for an exotic sphere. The dependent statement phase
must choose and justify one exact claim without using a convenient weakening
or an unrecorded historical sharpening.

Source locators for discovery, not immutable evidence receipts:

- Milnor, Ann. of Math. (2), volume 64 (1956), pages 399-405,
  DOI `10.2307/1969983`.
- Repository source record: `Docs/researches/math_theorems.md`, entry headed
  `米尔诺怪球` whose statement is the translated phrase above.
- Generated Stage0 record: `Docs/Stage0_Blueprint.md`, `THM-M-0578`.

No `H0` claim is made. `H1` records a named primary proof source with an open
exact-statement, premise, edition/hash, errata, and independent-review audit.

## Statement-phase resolution

The exact statement phase selects dimension seven and homeomorphism to the standard smooth
seven-sphere. This is supported both by Milnor's cited title/result and by the repository's second
entry for the same named theorem, whose statement is `七维怪球的存在` ("existence of a
seven-dimensional exotic sphere"). It entails the first entry's homotopy-equivalence wording but
does not replace the named theorem with a weaker arbitrary homotopy-sphere claim.

The frozen Lean expression is
`Stage1Instances.THM_M_0578.MilnorExoticSphereTarget` in `Statement.lean`. Pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` contains the identically shaped declaration
`exists_homeomorph_isEmpty_diffeomorph_sphere_seven`, but marks it `proof_wanted`; consequently it
confirms the encoding surface only and supplies no theorem-proof credit.
