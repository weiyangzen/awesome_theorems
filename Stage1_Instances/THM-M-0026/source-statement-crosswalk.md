# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:207-212` supplies the Chinese title `希尔伯特零点定理`, the
attribution David Hilbert, the year 1893, and the gloss
`代数闭域上多项式环的极大理想与代数集点的对应` ("correspondence between maximal ideals of a
polynomial ring over an algebraically closed field and points of the algebraic set"). Git history
places all six uncited lines in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record
contains no edition, theorem locator, definitions, finite-variable condition, ordered binders,
hypotheses, conclusion, proof boundary, correction history, or formal declaration.

`Docs/Stage0_Blueprint.md:830-856` repeats the gloss while leaving the exact definitions and
premises, proof route, dependencies, alternate forms, axioms, machine status, and artifact links
open. The rev-5.6 target manifest retains `已验证` only as untrusted source metadata and resets the
target to `L0 / rework_required`.

## Inspected mathematical source lead

The Stacks Project, Section 10.34, Theorem 10.34.1, stable tag `00FV`, was inspected on 2026-07-13.
It states for a field `k` that every maximal ideal of `k[x_1, ..., x_n]` has residue field finite
over `k`, and that every radical ideal is the intersection of the maximal ideals containing it;
the same assertions hold for finite-type `k`-algebras. The observed HTML SHA-256 was
`6cd63b63c40ce5998c105e5c5ce5b3e78aa099ff5dea75c17280eb1d66030bde`.

Over an algebraically closed `k`, the residue-field clause is an important route to the catalog's
maximal-ideal/point formulation. The inspected theorem does not itself spell out the exact
singleton-vanishing-ideal `Iff`, a bundled point/maximal-ideal bijection, or the repository's phrase
"point of the algebraic set." The repository also does not cite the Stacks Project or identify this
route as canonical. The source is therefore an authoritative lead, not accepted H0 evidence: a
lawfully preserved immutable edition, exact corollary/definition mapping, correction audit, and
independent mathematical review remain open. The catalog's historical attribution and date have
not been independently verified by this intake.

## Pinned Lean candidates

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.RingTheory.Nullstellensatz` contains several materially different candidates:

| Declaration | Pinned type/scope summary | Intake assessment |
|---|---|---|
| `MvPolynomial.eq_vanishingIdeal_singleton_of_isMaximal` | for fields `k`, `K`, an algebra `k -> K`, algebraically closed `K`, finite `sigma`: every maximal ideal of `MvPolynomial sigma k` is `vanishingIdeal k {x}` for some `x : sigma -> K` | close weak direction; coefficient/point fields may differ |
| `MvPolynomial.isMaximal_iff_eq_vanishingIdeal_singleton` | for algebraically closed field `K` and finite `sigma`: `I.IsMaximal` iff `I = vanishingIdeal K {x}` for some `x : sigma -> K` | closest candidate to the catalog gloss; exact source transport still open |
| `MvPolynomial.vanishingIdeal_zeroLocus_eq_radical` | for `I : Ideal (MvPolynomial sigma k)`: the polynomials vanishing on its `K`-zero locus form `I.radical` | strong Nullstellensatz; not interchangeable with the stated maximal-ideal correspondence |
| `MvPolynomial.IsPrime.vanishingIdeal_zeroLocus` | specializes the strong identity to prime ideals | adjacent specialization, not the catalog root |

The module file SHA-256 is
`cc19eaf5462c113cef15fdce99f41799b616333cdc33cc0ffaac2086e1bdf2c4`. The first two close
classification declarations in their present generalized form originate in mathlib commit
`632d3ae291feaf46fa8ea64babc65e4068a4ce99`; the strong theorem has older provenance and a current
terminal body in the same pinned module. `IntakeProbe.lean` checks their types, but this intake does
not inspect the full transitive declaration closure, axioms, terminal-body provenance, or exact
source equivalence required by the later anchor audit.

## Component crosswalk

| Catalog component | Mathematical choice still required | Prospective Lean surface | Intake status |
|---|---|---|---|
| algebraically closed field | coefficient field equals point field, or extension-valued points | `[Field K] [IsAlgClosed K]`, possibly `[Algebra k K]` | open |
| polynomial ring | finite list of variables or finite index type | `MvPolynomial sigma K` with `[Finite sigma]` | representation open |
| maximal ideals | predicate, subtype, or maximal spectrum | `Ideal.IsMaximal` | adjacent API checked |
| algebraic-set point | affine point, zero-locus member, or spectrum point | `sigma -> K`, `zeroLocus`, `vanishingIdeal K {x}` | meaning open |
| correspondence | existence, `Iff`, bijection, or strong ideal identity | the three candidate declarations above | root not selected |
| `已验证` | untrusted inventory label | no proposition or proof object | no H or M credit |

Before leaving `H1`, reviewers must select an immutable proposition, map every incorporated
definition, binder, premise, conclusion, and boundary case, audit corrections and the historical
claim, and independently approve the mapping. Only then may the statement phase freeze minimal
imports, an elaborated expression, checked transports, and the required four mutation classes.
