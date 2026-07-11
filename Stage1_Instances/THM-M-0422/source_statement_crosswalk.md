# Source-statement crosswalk

The manifest phrase "abelian extensions of number fields" names a theory rather than a single
proposition. To avoid silently substituting a weaker result, the intake root includes the two
standard global class field theory halves below. Pinpoint and errata verification is deliberately
left open, so these are discovery anchors and the human status remains `H3`.

| Root component | Human source discovery anchor | Candidate Lean surface | Intake assessment |
|---|---|---|---|
| Global reciprocity for finite abelian `L/K`: Artin map, norm kernel, and quotient isomorphism `C_K/N(C_L) \cong Gal(L/K)` | J. Neukirch, *Algebraic Number Theory*, Springer, 1999, Chapter VI, global class field theory sections; J. W. S. Cassels and A. Froehlich (eds.), *Algebraic Number Theory*, Academic Press, 1967, the class field theory chapters | A theorem over number fields, finite abelian extensions, ideles, idele classes, norm maps, and continuous Galois automorphisms | The mathematical component is identified, but edition-page/theorem pinpoints, assumptions, errata, and exact Lean object availability are not yet audited |
| Existence theorem: open finite-index subgroups of `C_K` are norm groups, yielding the abelian-extension correspondence | Same global class field theory sources; J. S. Milne, *Class Field Theory*, version 4.03 (2020), global class field theory chapters | A correspondence between suitable open subgroups and finite abelian intermediate fields in a fixed algebraic closure | Required root half; uniqueness and order-reversal conventions need normalization |
| Principal ideles lie in the reciprocity kernel and the global map is assembled from local symbols | The reciprocity construction in the cited global class field theory treatments | Compatibility diagram from local reciprocity maps through the idele quotient | Required proof/source boundary; local reciprocity by itself is not root closure |
| Profinite formulation `\widehat{C_K} \cong Gal(K^ab/K)` | Standard inverse-limit consequence/formulation in the cited treatments | Possible alternate target using profinite completion and maximal abelian extension | Candidate alternate only; equivalence to the finite-level compound root must be checked |
| Ray class fields and generalized ideal class groups | Finite-level existence presentations in standard global class field theory | Possible cofinal family of finite quotients | A route to the root, not an eligible replacement for it |

## Source boundary

The repository research note at `Docs/researches/math_theorems.md` and generated Stage0/Stage1 prose
are metadata, not mathematical sources. Their `已验证` label supplies no H or M credit. The cited
books/notes presently locate the conventional theorem family, but no immutable source receipt has
been created and no detailed premise-to-node crosswalk has been independently reviewed.

Discovery links, not accepted evidence receipts:

- Milne, *Class Field Theory*: <https://www.jmilne.org/math/CourseNotes/CFT.pdf>
- Neukirch bibliographic record: <https://doi.org/10.1007/978-3-662-03983-0>

The statement phase must select explicit Lean types for number fields, places, restricted products,
idele classes, norm subgroups, topological quotients, and Galois groups. It must then elaborate the
compound target, check any profinite or ray-class transport, and mutation-test abelianity,
finiteness, openness/index, norm direction, inclusion reversal, trivial extensions, and the `K = Q`
specialization before machine closure may be inspected or credited.
