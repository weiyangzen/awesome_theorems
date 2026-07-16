# Source-statement crosswalk

| Claim component | Source or formal lead | Required Lean content | Current result |
|---|---|---|---|
| Canonical basis for a Coxeter Hecke algebra | D. Kazhdan and G. Lusztig, *Representations of Coxeter groups and Hecke algebras*, Invent. Math. 53 (1979), 165-184, Section 1 | one exact existence-and-uniqueness declaration | Blocked: the intake gives a section locator, not an immutable edition and exact result/page pinpoint |
| Coxeter system and length | opening definitions in the same section | `CoxeterMatrix`, `CoxeterSystem`, `CoxeterSystem.length` | Diagnostic match only; the pinned declarations elaborate from `Mathlib.GroupTheory.Coxeter.Length` |
| Hecke algebra and standard basis | the paper's generic Hecke algebra construction | concrete algebra, standard basis, multiplication, and parameter convention | No accepted general-Coxeter model exists in the pinned dependency closure |
| Bar involution | the involution used in the canonical characterization | coefficient involution and induced algebra involution | Absent; its formula depends on the unresolved parameter and quadratic convention |
| Triangular normalization | the canonical-basis characterization | Bruhat support, leading coefficient, and coefficient sublattice | Absent; neither the precise formula nor the `C_w`/`C'_w` convention is frozen |
| Existence and uniqueness | the intended Kazhdan-Lusztig basis theorem | unique existence of a basis family satisfying the preceding conditions | Cannot be serialized until all preceding rows are exact |

## Formal leads

The historical declaration `AwesomeTheorems.Stage1.S1_M_056.StatementShape` is not an alternate
encoding of the canonical theorem. Its `AbstractHeckeContext` stores the Hecke algebra, Bruhat
relation, bar-invariance predicate, triangularity predicate, and required hypotheses as
unconstrained fields. Treating it as the target would replace the named theorem by a weaker
interface whose desired mathematics can be assumed.

A non-credited lead was inspected in `facebookresearch/atlas-lean` at commit
`34ffed396f376454c1a9b297f3fd74c5c801fb50`, tree
`c12fe2315fe475d70a4fcee81d6b731f853373ab`. The source
`Atlas/LieGroups/code/HeckeKL.lean` has SHA-256
`71d5c6ea34f0156f41000e8a2babe87854c99954736b1d9ae46954544ca16766` and Git blob
`5d6f0adf28d87ee3c4763bf0abf046166cd7820f`. Its `targets.yaml` entry for Theorem 21.5 describes
vanishing/diagonal conditions, a degree bound, and self-duality of the resulting basis element.
This improves the search vocabulary, but it cannot identify the repository target because:

- `CoxeterGroupData` requires a finite `Fintype W`, while the target is for a general Coxeter system;
- the Coxeter laws and Bruhat order are bundled abstractly rather than transported to pinned mathlib;
- `RPoly_orthog`, `kl_coeff_self_dual_identity`, and `self_dual_implies_coeff_eq` have unclosed proof gaps;
- `kl_poly_unique` assumes a recursion in place of the canonical self-duality condition; and
- the repository is not a pinned dependency of this Lean project.

No bytes or declaration from that external checkout receive statement, proof, or dependency-reuse
credit. The original-paper DOI, <https://doi.org/10.1007/BF01390031>, likewise remains a discovery
locator rather than immutable source evidence.

## Retry boundary

Supply an immutable primary-source edition and pinpoint the exact existence-and-uniqueness result.
Then transcribe its ordered premises and formula, freeze the parameter, quadratic relation,
coefficient lattice, bar involution, standard-basis normalization, and `C_w`/`C'_w` convention.
Only after a concrete general-Coxeter Hecke/Bruhat encoding or checked import exists can the exact
Lean expression, transports, fingerprint, and four required mutations be produced.
