# Scope map

## Provisional included claim

- A compact smooth cobordism `W` whose boundary is identified with two closed smooth manifolds
  `M0` and `M1`.
- Both boundary inclusions are homotopy equivalences, making `W` an h-cobordism.
- The simple-connectivity and high-dimensional hypotheses required by the selected classical
  theorem.
- Triviality of the cobordism by a diffeomorphism from `W` to `M0 x [0,1]` relative to `M0`, with
  diffeomorphism of `M0` and `M1` as a consequence.

## Decisions required at statement freeze

The statement phase must select and inspect an immutable primary-source edition, then freeze
whether simple connectivity is assumed of `W`, both ends, or one end; whether connectedness and
nonempty boundary are explicit; whether the dimension bound is stated as `dim W >= 6` or
`dim M0 >= 5`; the category (smooth, PL, or topological); boundary collars and corner conventions;
the precise meaning of a diffeomorphism relative to an end; and whether orientation or ordered
boundary identifications are required. It must cover the threshold and low-dimensional cases,
disconnected inputs, empty ends, and the effect of swapping the ends.

## Explicit exclusions

- The s-cobordism theorem with vanishing Whitehead torsion as a substituted root statement.
- The Poincare conjecture, surgery classification, or handle cancellation alone.
- A claim merely that homotopy-equivalent manifolds are diffeomorphic.
- A low-dimensional or topological-category analogue not asserted by the selected source.
- A structure that contains the required product diffeomorphism as assumed data.
- The repository label `\u5df2\u9a8c\u8bc1` as human-proof or kernel evidence.

No Lean target is frozen at intake. A later target must expose concrete smooth manifolds with
boundary, cobordism boundary identifications, inclusion homotopy equivalences, dimension and
connectivity hypotheses, and the relative product diffeomorphism rather than assume the conclusion.
