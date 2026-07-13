# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:677-682` supplies exactly the title `卡当-外尔定理`, attribution to
Elie Cartan and Hermann Weyl, the year 1913, the gloss `半单李代数的分类与表示`
(`classification and representations of semisimple Lie algebras`), importance "high," and status
`已验证`. Git history places all six uncited fields in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. It supplies no bibliography, standard-language
name, formula, definitions, ordered binders, assumptions, conclusion, proof boundary, corrections,
or formal declaration.

`Docs/Stage0_Blueprint.md:2632-2657` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof route, dependencies, alternate forms, axioms,
machine status, and artifact links open. The rev-5.6 manifest retains `已验证` only as untrusted
source metadata and resets this target to `L0 / rework_required`.

## Inspected source leads

No primary mathematical source was admitted during intake. Two immutable Encyclopedia of
Mathematics revisions were inspected as secondary leads. Revision 53489, `Lie algebra,
semi-simple`, states several equivalent characteristic-zero finite-dimensional conditions,
including decomposition into simple ideals and complete reducibility of every finite-dimensional
representation. It also states both directions of classification by reduced root systems over an
algebraically closed field. Revision 33105, `Cartan-Weyl basis`, instead defines a basis for a
finite-dimensional complex semisimple Lie algebra and cites Weyl's 1925 representation paper. The
raw observed SHA-256 digests were respectively
`2ddc65e191216d2e652e17f302bec8253bb4c5396c0133307a504efcace58cbd` and
`d0aabfaeccf32578ae3f38037fa0052f9e2d09c24b49b9ab9ba338fb0611e863`.

Crossref metadata for DOI `10.1007/BF01506234` identifies H. Weyl's *Theorie der Darstellung
kontinuierlicher halb-einfacher Gruppen durch lineare Transformationen. I*, *Mathematische
Zeitschrift* 23 (1925), pages 271-309; the response digest was
`b68eed7e55be3a3414bcff73d0a36143f0b0d4dfdf77996af494846b695c901b`. This is a
bibliographic lead only; the paper itself and an exact proposition were not inspected. The 1925
date makes the catalog's unexplained joint 1913 attribution a material source-audit problem.

The pinned mathlib sources expose further bibliographic leads but do not select the catalog root:

- `Mathlib/Data/Matrix/Cartan.lean` cites Bourbaki, *Lie Groups and Lie Algebras, Chapters 4--6*,
  plates I--IX, and J. Humphreys, *Introduction to Lie Algebras and Representation Theory*,
  Chapter 11, for the finite-type Cartan matrices.
- `Mathlib/Algebra/Lie/Semisimple/Defs.lean` cites G. B. Seligman, *Modular Lie Algebras*, page 15,
  while warning that the word "semisimple" has competing definitions outside the usual
  characteristic-zero setting.
- `Mathlib/Algebra/Lie/Semisimple/Basic.lean` itself calls the relevant classification the
  Cartan-Dynkin-Killing classification, not a uniquely identified Cartan-Weyl proposition.

The encyclopedia pages and formal-library references are E5 locator leads, not complete primary
proof editions or `H0` evidence. The statement phase must lawfully preserve and inspect an
authoritative edition, map every incorporated definition and assumption, audit corrections and
translations, and obtain independent review. Historical attribution and the 1913 date remain
unverified.

## Component crosswalk

| Catalog component | Source-family alternatives | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| "semisimple Lie algebra" | direct sum of simple ideals; trivial radical; nondegenerate Killing form in characteristic zero | `LieAlgebra.IsSemisimple`, `LieAlgebra.HasTrivialRadical`, `LieAlgebra.IsKilling` | multiple encodings; hypotheses and transports open |
| "classification" | simple types; semisimple products; root-system or Dynkin-diagram classification | `LieAlgebra.IsKilling.rootSystem`, `RootPairing.IsRootSystem`, `CartanMatrix.A` through `CartanMatrix.G2` | adjacent construction/data only; no root classification selected |
| algebra examples | classical matrix Lie algebras and exceptional types | `LieAlgebra.SpecialLinear.sl`, orthogonal/symplectic definitions, Cartan matrices | examples/data do not prove exhaustiveness or uniqueness |
| "representations" | complete reducibility; irreducibles by highest weights; character or dimension classification | `LieModule.IsIrreducible`, generic semisimple-module APIs, future highest-weight representation surface | conclusion and field/dimension assumptions absent |
| joint Cartan-Weyl label | one theorem, conjunction, or historical program | no canonical declaration or expression | nonstandard/ambiguous target name; exact source required |
| `已验证` | untrusted inventory label | no proposition or proof object | no H or M credit |

## Pinned Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`IntakeProbe.lean` elaborates nine adjacent declarations. The semisimple API decomposes a Lie algebra
into atomic ideals and derives trivial radical; the root-system API requires a characteristic-zero
field, finite dimension, a Killing condition, a Cartan subalgebra, and triangularizability; the
Cartan-matrix API supplies named matrices. Those are materially useful ingredients and partial
formal leads, but they do not provide a checked classification equivalence or a classification of
irreducible representations for an approved source statement.

Two further pinned boundaries make the incompleteness explicit. `Mathlib/Algebra/Lie/Basis.lean`
defines a partial Chevalley-Serre-style basis but lists existence for every semisimple Lie algebra
and definitions of Weyl/Chevalley bases as TODOs. The Geck-construction modules construct a
semisimple Lie algebra from suitable root data and identify the root system of that constructed
algebra, but do not supply the converse arbitrary-algebra isomorphism or representation
classification needed for the broad catalog wording.

A bounded exact-topic search found no repo-local or pinned-mathlib declaration named for a
Cartan-Weyl theorem. That observation is intake discovery only, not the required later immutable
external anchor audit and not evidence of global absence.

Before leaving `H1`, reviewers must select one exact source claim, settle whether the algebra and
representation clauses are conjunctive or alternative, record edition and pinpoint locators,
transcribe every definition/binder/hypothesis/conclusion, audit attribution/translation/errata, and
approve the mapping independently. Only then may the statement phase select minimal imports,
serialize an elaborated target, check transports, and run the four required mutation classes.
