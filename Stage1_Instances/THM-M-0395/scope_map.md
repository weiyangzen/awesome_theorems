# Scope map

| Surface | Included meaning | Boundary |
|---|---|---|
| Base | arbitrary number field `K` | not arbitrary global fields |
| Object | smooth proper geometrically connected curve over `K` | no singular, open, or disconnected curves |
| Genus | genus at least two | genus 0 and 1 are excluded |
| Points | `K`-rational points represented as `K`-sections | `RationalPoint` is the subtype of sections whose composite is the identity |
| Result | finiteness | no effective bound, enumeration, or uniformity claim |

The canonical claim is the Mordell-conjecture consequence/form of Faltings's
work, not the Tate conjecture, Shafarevich finiteness, or an isogeny theorem.
`Stage1Rev56.THMM0395.Statement` is the selected exact formal target. Its
`CurveOver` datum carries smoothness, properness, geometric connectedness,
dimension one, and genus at least two as named predicates because the pinned
mathlib snapshot has no complete curve-genus object API. The statement does
not quantify over arbitrary predicate functions: each predicate belongs to
the curve datum, and `IsFaltingsCurve` requires all five. This makes the
formalization boundary explicit without replacing or weakening an assumption.

The checked theorem `finite_points_iff_finite_univ` transports typeclass
finiteness of rational sections to finiteness of their universal set. The
legacy Stage1 module remains discovery input only and receives no proof credit.
