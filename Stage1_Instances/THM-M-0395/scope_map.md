# Scope map

| Surface | Included meaning | Boundary |
|---|---|---|
| Base | arbitrary number field `K` | not arbitrary global fields |
| Object | smooth proper geometrically connected curve over `K` | no singular, open, or disconnected curves |
| Genus | genus at least two | genus 0 and 1 are excluded |
| Points | `K`-rational points, equivalently `K`-sections after a checked transport | transport is deferred to statement phase |
| Result | finiteness | no effective bound, enumeration, or uniformity claim |

The canonical claim is the Mordell-conjecture consequence/form of Faltings's
work, not the Tate conjecture, Shafarevich finiteness, or an isogeny theorem.
The existing `StatementShape` uses explicit predicate slots for several curve
properties. Those slots are a candidate encoding, not yet an accepted exact
formal target. No legacy declaration is credited until the statement gate
elaborates it, fingerprints it, checks transports, and runs mutations.
