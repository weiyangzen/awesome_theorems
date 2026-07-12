# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:128-133` supplies exactly the title `阿廷互反律`, Emil Artin,
1927, the gloss `类域论的核心定理`, importance "high," and status `已验证`. The same catalog
record is duplicated at lines 3054-3059. The original six-line record entered the repository at
commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. It contains no bibliography, formula,
definitions, hypotheses, conclusion, proof, errata record, or formal artifact.

`Docs/Stage0_Blueprint.md:528-553` repeats those fields and explicitly leaves precise definitions,
premises, proof route, dependencies, equivalent forms, axioms, machine status, and artifact links
open. Its generic tree and leaf-budget prose is planning metadata, not theorem evidence. The
rev-5.6 manifest preserves `已验证` only as `source_status_untrusted` and resets this target to
`L0 / rework_required`.

## Literal crosswalk

| Repository element | Candidate mathematical component | Required Lean component | Intake result |
|---|---|---|---|
| `阿廷互反律` | classical Artin reciprocity theorem family, conventionally read globally here | exact source-selected local/global domain, Artin map, and law | global form is the leading candidate; domain and encoding open |
| `类域论` | global or local class field theory; ideal or idelic language | explicit number/global field, places, ideles or ray groups, norms, topology, and Galois group | domain and representation open |
| `核心定理` | reciprocity alone or reciprocity plus class-field existence | exact clause bundle and conclusion type | no conjunction authorized by the catalog |
| Emil Artin, 1927 | historical proof provenance | immutable primary text and historical-to-modern premise mapping | bibliographic candidate located; full text and mapping open |
| `已验证` | untrusted inventory metadata | inspectable proof source and kernel receipt would be required | no H0 or M credit |

## Inspected modern source

J. S. Milne, *Class Field Theory*, version 4.03 (August 6, 2020), Chapter V, Section 5,
printed pages 177-179, was inspected from the author-hosted PDF. In that chapter's number-field
setup, Proposition 5.2 constructs the continuous global map from compatible local Artin maps.
Theorem 5.3, explicitly titled
"Reciprocity Law," says:

- the global Artin map `phi_K : I_K -> Gal(K^ab/K)` is trivial on `K^*`; and
- for every finite abelian extension `L/K`, it induces an isomorphism
  `I_K / (K^* Nm(I_L)) -> Gal(L/K)`, equivalently `C_K / Nm(C_L) -> Gal(L/K)`.

This source establishes a strong theorem-family candidate and supports provisional `H1`. It does
not yield H0: the catalog does not cite this formulation, and the incorporated definitions,
number-field/global-field scope, Frobenius normalization, historical equivalence, proof-node
mapping, corrections, errata, and independent review have not been accepted.

Milne's Theorem 5.5 on printed page 179 is separately titled "Existence Theorem." It classifies
finite-index open subgroups of the idele class group as norm groups. It is related class field
theory, but it is not silently included in this Artin reciprocity target.

## Historical source candidate

Emil Artin, *Beweis des allgemeinen Reziprozitaetsgesetzes*, *Abhandlungen aus dem Mathematischen
Seminar der Universitat Hamburg* 5(1) (1927), 353-363, DOI
`10.1007/BF02952531`, is the historical primary candidate. Crossref and the publisher page confirm
the author, title, journal, volume, issue, pages, DOI, and December 1927 date. The article body was
not accessible in this worker run. Therefore its exact statement, notation, premises, proof,
relationship to the modern idelic form, and errata remain uninspected and receive no H0 credit.

## Lean crosswalk

| Source component | Pinned Lean substrate | Intake boundary |
|---|---|---|
| number field `K` | `NumberField K`, ring of integers, number-field imports | available substrate only |
| adele ring | `NumberField.AdeleRing (O K) K` | additive ring exists; not by itself the restricted multiplicative ideles in the source |
| diagonal embedding | `NumberField.AdeleRing.algebraMap_injective` and additive `principalSubgroup` | checks an adjacent embedding, not principal ideles in the target quotient |
| finite abelian `L/K` | `IsAbelianGalois K L` plus a separate `FiniteDimensional K L` or equivalent finiteness hypothesis | Galois-plus-abelian predicate available; `IsAbelianGalois` alone does not assert finite dimension, and the full extension packaging remains to freeze |
| quotient group | `QuotientGroup.mk'`, `QuotientGroup.ker_mk'` | generic quotient infrastructure only |
| global Artin map, norms, Frobenius compatibility, quotient isomorphism | no exact declaration found in the bounded pinned-mathlib search | full statement/interface and formalization debt remain |

The repo-local legacy global-CFT file `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_077.lean`
is discovery input only. It defines candidate interfaces and explicitly records that no terminal
global Artin reciprocity theorem was found; it is owned by another historical target and transfers
no accepted statement or proof state here.

## Source gate

Before H0 or statement acceptance, accountable reviewers must select an immutable formulation,
transcribe every incorporated definition, ordered binder, hypothesis, conclusion, normalization,
and boundary case, reconcile Artin's ideal-theoretic statement with any modern idelic target, audit
errata and the proof boundary, and approve the source-to-Lean mapping. Until then the canonical
statement and expression remain null.
