# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md:491-496` supplies exactly:

- title: `舒尔引理`;
- attribution: Issai Schur;
- year: 1905;
- gloss: `不可约表示之间的同态要么为零要么为同构`;
- importance: high;
- untrusted formalization status: `已验证`.

All six catalog lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. `Docs/Stage0_Blueprint.md:1920-1945`
repeats the gloss while explicitly leaving exact definitions, premises, proof route, equivalent
forms, axioms, machine status, and artifact links open. Neither repository record cites a primary
work or a modern proof source. They establish catalog identity, not `H0`.

## Human-source boundary

The catalog's Issai Schur/1905 attribution is only a historical locator. This intake did not find
an identified work title, edition, theorem/page passage, quotation, incorporated definitions,
proof boundary, translation, errata record, or independent reviewer in the repository. No primary
source statement is therefore reconstructed or accepted. The first human-source gate remains a
pinpoint primary or authoritative source audit with a complete assumption and errata crosswalk.

## Clause crosswalk

| Repository phrase | Required mathematical meaning | Pinned Lean candidate | Intake status |
|---|---|---|---|
| "representation" | action of one fixed group or algebra by linear automorphisms on a vector space | `Representation k G V` | API located; exact acting object and scalar domain open |
| "irreducible" | nonzero representation with no proper nonzero invariant subspace | `Representation.IsIrreducible rho` | direct candidate definition located; source-definition identity open |
| "homomorphism" | equivariant linear map between the two representations | `IntertwiningMap rho sigma` | direct candidate type located; exact source convention open |
| "zero" | the zero intertwining map | `f = 0` | direct candidate conclusion branch |
| "isomorphism" | bijective equivariant map with equivariant inverse | `Function.Bijective f`, packaged by `IntertwiningMap.ofBijective` | candidate transport only; not frozen |
| "either ... or" | exact disjunction, including its orientation and exclusivity convention | `Function.Bijective f ∨ f = 0` | direct candidate orientation differs from the gloss order |
| `已验证` | untrusted inventory label | no expression, source receipt, or proof evidence | explicitly rejected as credit |

## Pinned formal leads

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`:

1. `Mathlib/RepresentationTheory/Irreducible.lean` defines irreducible monoid representations and
   proves `Representation.IsIrreducible.bijective_or_eq_zero`. The visible proof transports the
   intertwining map to a linear map over the monoid algebra and invokes the simple-module theorem.
2. `Mathlib/RingTheory/SimpleModule/Basic.lean` explicitly labels
   `LinearMap.bijective_or_eq_zero` as Schur's lemma for linear maps between possibly distinct
   simple modules.
3. `Mathlib/CategoryTheory/Preadditive/Schur.lean` proves
   `CategoryTheory.isIso_iff_nonzero` for morphisms between simple objects in a preadditive
   category with kernels and separately develops finite-dimensional algebraically closed variants.

The intake probe checks these declaration types and the representation-equivalence constructor in
the pinned environment. This is a bounded discovery result, not the exhaustive anchor audit.
Exact normalized types, terminal proof bodies, transitive declarations, axioms, placeholders,
unsafe/oracle boundaries, source identity, and checked transports remain downstream gates.

## First failed statement/source gate

No accepted source fixes the group or algebra, scalar field, dimensionality, irreducibility and
intertwiner conventions, or isomorphism witness. Therefore the direct monoid-representation
candidate, the module theorem, and the categorical theorem cannot yet be installed as the
canonical target without broadening or substituting the received claim.
