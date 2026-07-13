# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:684-689` supplies exactly the title `最高权定理`, attribution to
Elie Cartan, the year 1913, the gloss `半单李代数不可约表示由最高权分类` ("irreducible
representations of semisimple Lie algebras are classified by highest weight"), importance `high`,
and status `verified`. Git history places all six uncited fields in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:2659-2684` repeats the metadata while explicitly leaving the formal
system, foundation, exact definitions and premises, proof route, dependencies, equivalent forms,
axiom policy, machine status, and artifact links open. The rev-5.6 manifest retains `verified` only
as untrusted metadata and resets the target to `L0 / rework_required`.

The catalog has no bibliography, theorem/page locator, scalar field, finite-dimensionality clause,
Cartan/Borel or positive-root choice, dominant-integral definition, representation model,
irreducibility convention, ordered binders, exact conclusion, proof boundary, correction history,
or reviewer. Its gloss names a theorem family rather than one stable proposition.

## Inspected modern source lead

Pavel Etingof, *18.745: Lie Groups and Lie Algebras I*, full Fall 2020 lecture notes, author-issued
through MIT OpenCourseWare and observed on 2026-07-13, was inspected. Section 25 begins on printed
page 132 by fixing a complex semisimple Lie algebra and complex representations, mostly
finite-dimensional. Within that setup:

- Definition 25.4 and Proposition 25.5, printed page 133, define highest-weight vectors/modules and
  prove that every nonzero finite-dimensional representation contains a highest-weight vector, so
  every finite-dimensional irreducible representation is highest-weight.
- Proposition 25.12 and Corollary 25.13, printed pages 135-136, construct the unique irreducible
  quotient `L_lambda` of a Verma module and classify irreducible highest-weight modules by their
  highest weight.
- Proposition 25.14 through Lemma 25.16 identify necessity and the Weyl-invariance mechanism.
- Theorem 25.17, printed page 137, proves that `L_lambda` is finite-dimensional exactly for dominant
  integral `lambda`, and concludes that finite-dimensional irreducible representations are
  classified up to isomorphism by dominant integral highest weights.

The observed PDF SHA-256 is
`908b49bd938da6b28f2bceb01311028c8f453c721af6830ce0e32a1e52b6b929`. The catalog does not cite
this edition; no complete incorporated-definition and proof-node crosswalk, correction audit,
historical verification of Cartan/1913, repository preservation, or independent review is
credited. The notes are therefore an `H1` lead, not accepted `H0` evidence.

## Component crosswalk

| Catalog component | Source component | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| "semisimple Lie algebra" | complex semisimple `g`, with Cartan and root data from earlier sections | `LieAlgebra.IsSemisimple`, `LieAlgebra.IsCartanSubalgebra`, `LieAlgebra.IsKilling.rootSystem` | exact field, finite dimension, splitting, and choice data absent from catalog |
| "irreducible representations" | nonzero finite-dimensional complex `g`-modules, classified up to isomorphism | `LieModule`, `FiniteDimensional`, Lie submodules/equivalences, possible enveloping-algebra module encoding | representation and irreducibility encoding open |
| "highest weight" | a weight vector killed by positive simple-root operators and generating its module | `LieModule.weightSpace` or `genWeightSpace` plus future positive-root annihilation and generation predicates | positive system and ordinary/generalized weight boundary open |
| "classified" | `lambda ↦ L_lambda` is a bijection from dominant integral weights to isomorphism classes of finite-dimensional irreducibles | future Verma/simple construction and quotient or isomorphism-class encoding | existence, uniqueness, quotient, and bijection contract absent |
| finite-dimensional parameter test | `L_lambda` finite-dimensional iff `lambda` is dominant integral | future weight lattice, coroot pairing, and dominant chamber | no pinned terminal declaration located |
| `verified` | untrusted inventory label | source review plus kernel evidence would be required | no H or M credit |

## Variant boundary

The short gloss could mean only that every finite-dimensional irreducible has a unique highest
weight, or the stronger two-way parameterization including construction for every dominant integral
weight. Etingof's final theorem contains the latter, assembled from several prior results. The
catalog does not fix this proof boundary. Nor does it decide the common extension from `Complex` to
an algebraically closed characteristic-zero field, or the related compact simply-connected Lie
group formulation. None is adopted without a source-selected statement and checked transports.

## Pinned Lean boundary

Pinned mathlib exposes genuine Lie-module weight spaces, Cartan and root-space infrastructure,
semisimple/Killing-form interfaces, and a root-system construction. `IntakeProbe.lean` checks a
small adjacent subset. A bounded case-insensitive search of repo-local Lean and pinned mathlib found
no highest-weight module, dominant-integral highest-weight, Verma module, or terminal classification
declaration. The abstract affine highest-weight predicates in `S1_M_053.lean` are inputs to another
target and do not construct the requested objects or prove this theorem. These observations are
discovery evidence only, not the downstream exhaustive anchor audit.

The root-system construction requires `LieAlgebra.IsKilling`, while the received theorem says
semisimple. Pinned mathlib proves the former implies the latter, but the converse bridge in
characteristic zero is not available there. The stronger API is therefore adjacent infrastructure,
not permission to restrict the canonical theorem from semisimple to nondegenerate Killing form.

## Required source admission

Before leaving `H1`, accountable reviewers must preserve an immutable lawful source edition, select
one exact proposition and proof boundary, map every incorporated definition, ordered binder,
hypothesis, conclusion and boundary case, audit corrections and the historical attribution, and
independently approve fidelity to `THM-M-0093`. Only then may the statement phase freeze minimal
imports, the elaborated expression and environment hashes, checked alternate encodings, and all
required statement mutations.
