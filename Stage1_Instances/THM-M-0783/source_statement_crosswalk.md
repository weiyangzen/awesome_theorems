# Source-statement crosswalk

| Claim component | Source anchor | Formal candidate | Intake assessment |
|---|---|---|---|
| Received repository claim | `Docs/researches/math_theorems.md`, entry "Martin's axiom": "axiomatization of forcing," Donald Martin/Robert Solovay, 1970 | None | Too broad to determine a proposition; the adjacent "verified" label is explicitly untrusted by the rev-5.6 manifest |
| Standard defining family | For each `kappa < 2^aleph_0`, every ccc partial order and family of at most `kappa` dense subsets admits a filter meeting each member | Candidate `MartinsAxiomAt kappa`, then `forall kappa < continuum, MartinsAxiomAt kappa` | Mathematical scope identified, but order, filter, ccc, cardinal, and set-theory representations are not frozen |
| Historical primary-source family | D. A. Martin and R. M. Solovay, "Internal Cohen extensions," *Annals of Mathematical Logic* 2 (1970), 143-178 | No repository-local Lean declaration found at intake | Bibliographic discovery anchor only. Exact definition/theorem/page mapping, edition hash, corrections, and independent review remain open |
| Object-level logical status | MA is adopted as an additional axiom; it is not a theorem of ZFC merely because its defining formula can be encoded | A proposition may be defined in Lean without assuming or proving it | This blocks an ordinary `H0` theorem claim. An `axiom`/assumption in Lean would extend the foundation and supplies no proof credit |
| Relative consistency | Consistency results obtained by forcing, under explicit consistency assumptions on the background theory | A future model-theoretic implication between encoded consistency/satisfaction statements | Distinct metatheorem; it cannot silently replace the object-level MA target |
| Relationship with CH | MA is commonly studied with `not-CH`; CH fixes the continuum at `aleph_1`, while MA constrains families below the continuum | Separate propositions and checked implications would be required | `MA + not-CH` is not an alternate spelling of MA and remains excluded |
| Stronger forcing axioms | Proper forcing axiom and Martin's maximum strengthen/change the permitted forcing class and conclusions | None | Explicitly outside scope |

## Exactness risks

The forcing order is written in opposite orientations in different sources. A filter can therefore
appear upward closed or downward closed depending on whether stronger conditions are smaller or
larger. Density and directedness must use the same convention. Textual similarity cannot establish
the required transport.

The ccc hypothesis must quantify over antichains with the intended incompatibility relation. Its
formal equivalence to "every antichain is countable" depends on the chosen cardinal/countability
API. Likewise, "at most `kappa` dense sets" may be encoded by an index type with a cardinal bound or
by a set of subsets; these are candidates until kernel-checked transports exist.

The bound is strict: `kappa < 2^aleph_0`. Empty families and trivial orders are legitimate boundary
probes, whereas allowing a family of continuum size materially strengthens the assertion. The
statement phase must mutation-test these distinctions before looking for proof evidence.

## Source status

No network source or mutable web page is treated as evidence in this intake. The Martin-Solovay
citation is a discovery lead, not `E4`: no immutable copy, page-level statement/premise crosswalk,
errata search, or independent reviewer receipt is present. Consequently no `H0` or relative-
consistency claim is made.
