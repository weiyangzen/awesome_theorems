# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md:214-219` records only:

- title: `韦德伯恩-阿廷定理`;
- attribution: Joseph Wedderburn / Emil Artin;
- year: 1907;
- gloss: `半单环的结构定理` ("the structure theorem for semisimple rings");
- importance: high;
- untrusted formalization label: `已验证`.

All six lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. `Docs/Stage0_Blueprint.md:857-882` repeats the
catalogue identity while explicitly leaving exact definitions and premises, proof route,
equivalent formulations, axioms, machine status, and artifact links open. These records establish
catalogue provenance only.

## Historical source leads

The attribution and date point toward J. H. M. Wedderburn's early structure work, "On Hypercomplex
Numbers," *Proceedings of the London Mathematical Society* (2) 6 (1908), pages 77-118, DOI
`10.1112/plms/s2-6.1.77`, and toward Emil Artin's later "Zur Theorie der hyperkomplexen Zahlen," *Abhandlungen aus
dem Mathematischen Seminar der Universitaet Hamburg* 5 (1927), pages 251-260, DOI
`10.1007/BF02952526`. Crossref metadata confirms both bibliographic records; the latter metadata
also includes a bibliographic reference naming Wedderburn's paper. These are discovery leads only:
this intake has not pinned full immutable
texts, located and translated an exact theorem passage, reconciled the catalogue's year with
publication chronology, mapped historical hypotheses and terminology to modern semisimplicity,
audited corrections or errata, or obtained independent review. They therefore provide no H0
source record and do not select a canonical formulation.

## Crosswalk

| Repository/source element | Theorem-family interpretation | Prospective Lean component | Intake status |
|---|---|---|---|
| semisimple ring | regular module decomposes as a sum of simple modules, with handedness fixed | `[Ring R]` and `IsSemisimpleRing R` | recognizable family; definition/source mapping open |
| structure theorem | finite decomposition into simple Artinian factors | an existential finite product and ring equivalence | conclusion shape not stated by catalogue |
| simple factor | a full matrix ring over a division ring | `Matrix (Fin (d i)) (Fin (d i)) (D i)` with `DivisionRing (D i)` | factor conventions and size positivity open |
| finite product | finitely many factors, perhaps including an empty product by convention | `Pi` over `Fin n` | `n = 0` and zero-ring boundary open |
| existence direction | semisimple implies a matrix-product decomposition | `IsSemisimpleRing.exists_ringEquiv_pi_matrix_divisionRing` | pinned formal candidate only |
| converse direction | such a product is semisimple | `isSemisimpleRing_iff_pi_matrix_divisionRing` | whether part of source target is open |
| canonical factors | endomorphism rings of simple ideals, with opposites | `exists_ringEquiv_pi_matrix_end_mulOpposite` | alternate candidate, not credited transport |
| Wedderburn / Artin / 1907 | historical catalogue metadata | no proposition or proof object | chronology and exact source passage unreviewed |
| `已验证` | untrusted inventory status | no source, statement, or kernel evidence | explicitly rejected as credit |

## Lean boundary

The repository separately assigns `THM-M-0036` to `阿廷-韦德尔本定理` with the gloss
`中心单代数的分类` ("classification of central simple algebras") at
`Docs/Stage0_Blueprint.md:1100-1125`. That sibling is not owned here. This intake restricts
`THM-M-0027` to the general semisimple-ring family signaled by its own gloss and leaves a formal
identity/overlap audit between the two records open. Neither target may inherit the other's proof
credit.

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe
elaborates the three candidates above and two adjacent simple-Artinian and finite-algebra variants.
It also records `#print axioms` output for the forward existence and biconditional candidates. The
mathlib source file labels the results "Wedderburn-Artin," but declaration names and docstrings do
not prove identity with the repository's underspecified source claim.

The repo-local file `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_078.lean` is owned by legacy
target `THM-M-0424` and wraps
`IsSimpleRing.exists_algEquiv_matrix_divisionRing_finite` only for finite-dimensional central
simple algebras. It is read-only discovery evidence for a special case, not an existing artifact
or proof body for `THM-M-0027`.

These observations are intake-only substrate discovery, not the comprehensive repo-local and
external candidate audit assigned to `S56-M-0027-ANCHOR_AUDIT`. Before statement credit, an
independently reviewed source passage must map every material domain, binder, premise, convention,
boundary case, and conclusion to one elaborated Lean expression, with checked transports for every
credited alternate form.
