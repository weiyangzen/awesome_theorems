# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:705-710` supplies exactly the title `谢瓦莱基定理`, attribution to
Claude Chevalley, year 1948, gloss `半单李代数的整基` ("an integral basis of a semisimple Lie
algebra"), importance `high`, and status `verified`. Git history places all six uncited fields in
commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:2740-2765` repeats the metadata while explicitly leaving the target formal
system, logical foundation, exact definitions and premises, proof route, dependencies, equivalent
forms, axiom policy, machine status, and artifact links open. The rev-5.6 manifest retains
`verified` only as untrusted metadata and resets this target to `L0 / rework_required`.

The catalog has no bibliography, theorem or page locator, definition of "integral basis," scalar
field, characteristic, finite-dimensionality clause, Cartan/root choices, ordered binders,
hypotheses, exact conclusion, proof boundary, correction history, or reviewer. It names a theorem
family rather than one stable proposition.

## Published-source leads

The pinned mathlib module `Mathlib.Algebra.Lie.Basis` cites Jean-Pierre Serre, *Complex Semisimple
Lie Algebras*, translated by G. A. Jones, Springer-Verlag, 1987, Chapter V, Sections 4 and 6, for
the Weyl/Chevalley-basis concept. The pinned bibliography records ISBN `0-387-96569-6` and DOI
`10.1007/978-1-4757-3910-7`. This intake inspected only mathlib's module documentation and pinned
bibliographic record, not the book itself. It did not verify the exact theorem, incorporated
definitions, proof pages, assumptions, corrections, or relationship to the catalog's 1948 label.

The Geck-construction modules cite Meinolf Geck, "On the construction of semisimple Lie algebras
and Chevalley groups," *Proceedings of the American Mathematical Society* 145 (2017), 3233-3247,
DOI `10.1090/proc/13600`. Mathlib says its construction follows this paper closely. That result
starts from based crystallographic root data and constructs a Lie algebra; it is a useful later
candidate for construction obligations, not a source-identity witness for the catalog root.

Both records are bibliographic leads only. Serre supports the provisional `H1` belief that a
complete standard proof is published, but no lead is accepted `H0` evidence and neither was used to
invent a canonical statement.

## Conventional component map, not source admission

| Catalog phrase | Conventional expansion to audit | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| "semisimple Lie algebra" | finite-dimensional complex or algebraically closed characteristic-zero Lie algebra | `LieAlgebra.IsSemisimple`, radical/Killing interfaces | exact field, dimension, splitting, and semisimplicity encoding absent |
| "basis" | Cartan elements and one normalized vector for each root, spanning the whole algebra | module basis plus Cartan/root-space data | index, choice, normalization, spanning, and independence contract absent |
| "integral" | all bracket structure constants lie in `Z` | integer coefficient predicate or scalar-cast equation | catalog does not say which coefficients/relations or how integers enter the field |
| opposite roots | commonly `[X_alpha, X_-alpha]` is a corresponding coroot element | root involution, coroot and bracket relation | normalization and sign conventions open |
| root sums | commonly `[X_alpha, X_beta]` is an integer multiple of `X_(alpha+beta)` when that is a root | root-string coefficient and bracket relations | magnitudes, signs and zero cases open |
| `Z`-form variant | integer span is bracket-closed and scalar extension recovers the Lie algebra | Lie ring/lattice plus base-change equivalence | equivalence to basis wording needs a checked transport |
| `verified` | untrusted inventory label | source review and kernel evidence would be required | no H0 or M credit |

## Variant boundary

A common theorem over `Complex` can be generalized to algebraically closed characteristic-zero
fields, but the catalog does not select either domain. Likewise, existence of some basis with
integer structure constants, existence of a normalized Chevalley basis, and existence of a
bracket-closed `Z`-form can differ in their data and conclusions. Uniqueness or independence of
Cartan, positive-root, sign, and ordering choices is another proposition. None is adopted without
an admitted source statement and checked transports.

## Pinned Lean boundary

`IntakeProbe.lean` checks nine adjacent declarations in three pinned modules. The most suggestive
name, `LieAlgebra.Basis`, is deliberately weaker than a Weyl/Chevalley basis: its module says more
axioms are needed to constrain brackets among positive or negative generators and lists the stronger
definition and general existence theorem as TODOs. `RootPairing.GeckConstruction.basis` closes that
weaker structure only for the construction's own Lie algebra. `Matrix.ToLieAlgebra` builds a
Serre-relation quotient from a Cartan matrix. No checked declaration inspected at intake states that
an arbitrary semisimple Lie algebra admits the catalog's unspecified integral basis.

These observations are scoped discovery evidence only. They do not replace the later immutable
repo-local, mathlib, and external candidate audit, and a TODO or bounded no-match is not proof of
global absence.

## Required source admission

Before leaving `H1`, accountable reviewers must lawfully preserve an immutable complete source
edition, identify the exact theorem and every incorporated definition, map ordered binders,
hypotheses, conclusion, normalization and boundary cases, crosswalk the complete proof and its
dependencies, audit corrections and the Chevalley/1948 attribution, and independently approve
fidelity to `THM-M-0096`. Only then may the statement phase freeze minimal imports, expression and
environment hashes, checked alternate encodings, and all required statement mutations.
