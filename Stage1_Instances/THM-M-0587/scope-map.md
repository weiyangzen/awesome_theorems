# Scope map

## Repository claim

`Docs/researches/math_theorems.md` gives only the title, Stephen Smale, 1962, and the gloss
`h-配边与微分同胚`. `Docs/Stage0_Blueprint.md` repeats that record while leaving definitions,
hypotheses, equivalent forms, proof route, axioms, and formal artifacts open. The catalog's
`已验证` label is untrusted metadata under rev-5.6.

## Provisional included claim family

- A compact smooth cobordism `W` whose boundary is identified with two closed smooth manifolds
  `M₀` and `M₁`.
- The two boundary inclusions are homotopy equivalences, making `W` an h-cobordism.
- The simply connected case, expressed either for `W` or for a boundary component after proving
  the relevant equivalence.
- Smale's stable dimension range: provisionally `dim W >= 6`, equivalently boundary dimension at
  least five, subject to the selected source's convention.
- A diffeomorphism from `W` to `M₀ x [0,1]` with the exact relative-boundary compatibility taken
  from the selected source.

This list identifies a theorem family. It is not yet a canonical human or Lean statement.

## Decisions required at statement freeze

The statement phase must fix the source edition, theorem label, page, and wording; smooth category
and Hausdorff/second-countability conventions; whether manifolds are connected and oriented;
compactness and boundary/corner conventions; collars and the boundary decomposition; whether
simple-connectivity is required of `W`, `M₀`, or both; the exact definition of h-cobordism; the
dimension variable; and the product diffeomorphism's behavior on each boundary component.

Lean universes, manifold models, ordered binders, explicit versus typeclass hypotheses, minimal
imports, foundation/TCB profiles, and checked transports to alternate encodings also remain open.
The target must define or independently establish the h-cobordism hypotheses; it may not accept
the desired product diffeomorphism as opaque input.

## Explicit exclusions

- The s-cobordism theorem or a Whitehead-torsion criterion for arbitrary fundamental group.
- Low-dimensional analogues, the topological or PL category, or a bare homeomorphism conclusion.
- The generalized Poincare conjecture substituted for the h-cobordism theorem without checked
  implications and all required side conditions.
- Only the conclusion that `M₀` and `M₁` are diffeomorphic, which is weaker than triviality of the
  cobordism.
- A product structure assumed as a hypothesis, numerical evidence, or the metadata status as proof
  evidence.

The separate catalog target `THM-M-0602` (generic "h-cobordism theorem") supplies no proof credit
or permission to merge theorem identities.
