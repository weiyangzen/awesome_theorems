# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10097-10102` supplies exactly the title `Sturm分离定理`, Jacques
Sturm, 1836, the gloss `线性无关解的零点交错`, importance `高`, and status `已验证`. Git history
places all six uncited fields in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:37695-37720` repeats that metadata but explicitly leaves the exact
definitions and premises, proof route, dependencies, equivalent forms, axiom policy, machine-checked
status, and artifact links open. The rev-5.6 target manifest preserves `已验证` only as untrusted
metadata and resets the target to `L0 / rework_required`.

The catalog has no bibliography, theorem or page locator, equation, interval, ordered binders,
hypotheses, formal conclusion, proof boundary, errata review, or reviewer. Its gloss therefore does
not select one stable formal proposition.

## Historical primary-source lead

An immutable Numdam record identifies C. Sturm, "Mémoire sur les Équations différentielles
linéaires du second ordre", *Journal de Mathématiques Pures et Appliquées*, series 1, volume 1
(1836), pp. 106-186. Its image-only scan was observed with SHA-256
`c9bd6111d00e70a2214931f4633898314bbea0b009716aa9604f03aa906cf26e`
(3,056,791 bytes, 82 PDF pages).

The Numdam metadata explicitly links a separate `Errata`, pp. 459-460, whose image-only scan was
observed with SHA-256
`ed7f4db1783207a385546e47c43f8c952352ebedda823e62e0e611918a962cd7`
(294,296 bytes, three PDF pages). The article record labels this link `corrigé par`; the errata
record reciprocally links the article as the work it corrects. This is a plausible
primary source for the catalog's author and date, but no exact theorem passage, terminology,
assumptions, or correction impact has been transcribed, translated, mapped, or independently
reviewed. Visual intake inspection confirms that the errata includes corrections keyed to pages
inside the memoir, including printed pages 148, 156, 185, and 186; exact formula transcription and
its effect on the target still require source review. Neither scan is admitted as H0 evidence.

## Authoritative source-family lead

Paul R. Beesack, "On Sturm's Separation Theorem", *Canadian Mathematical Bulletin* 15(4) (1972),
pp. 481-487, DOI `10.4153/CMB-1972-086-7`, was inspected from the publisher PDF. The observed
730,959-byte, seven-page PDF has SHA-256
`5a7480ce6690550fe5fa545166943b33f7faddf9dbccb6eddb9918aea71e1ce9`.

On page 481, Beesack describes the classical theorem for the second-order linear self-adjoint
equation `(r y')' + s y = 0`: `r` and `s` are continuous, `r` is positive on a compact interval
`I`, and between each pair of zeros of one nontrivial solution lies precisely one zero of any other
linearly independent solution. This is a strong match for the repository gloss.

The same article's Theorem 1 is broader. It assumes continuous `r,s`, strictly positive `r` on an
open interval `(a,b)`, and linearly independent solutions `y1,y2`. It states Abel's identity
`r(x) * (y1(x) * y2'(x) - y2(x) * y1'(x)) = k != 0`; for consecutive zeros `x1 < x1bar` of `y1`,
part (a) makes `y2/y1` strictly monotone between them and part (b) gives precisely one zero of `y2`
when both endpoints are nonsingular. Parts (c)-(e) give different singular-endpoint conclusions.

The publisher page exposes no article-specific correction, retraction, or corrigendum marker. A
bounded Crossref relation/update check was empty. This records only that no postpublication
correction was located by those checks; the PDF's received/revised dates are prepublication history,
and its later digitization metadata is not mathematical revision evidence.

Beesack is not the catalog's cited source because the catalog supplies no citation. Its classical
summary and generalized Theorem 1 are discovery leads, not an accepted canonical-root choice or H0
crosswalk. Complete transcription, reference-chain and historical-source review, lawful immutable
source admission, correction audit, and independent review remain open.

Gerald Teschl's *Ordinary Differential Equations and Dynamical Systems*, Section 5.5, was also
inspected as a variant discriminator. Its Lemma 5.21 interlaces consecutive eigenfunctions of a
regular Sturm-Liouville problem, while Theorem 5.20 is a comparison theorem. Those solutions carry
different eigenvalues and therefore do not silently instantiate the same-equation independent-
solution separation root named by the catalog gloss.

Gholizadeh and Mingarelli, *The Converse of Sturm's Separation Theorem*, arXiv
`2109.06953v1`, was inspected as a specialist discriminator (observed PDF SHA-256
`99afcf6af3b0ff117040d50e38fbf318774e678aae22e365391d62b5d3e76287`). Its introduction
describes the classic exact-one-zero statement for `-(p y')' + q y = 0`, while its wider
Caratheodory framework and counterexamples highlight that coefficient sign, solution regularity,
turning points, and endpoint conventions are material hypotheses. It is not a catalog-selected
source or an H0 proof crosswalk.

## Component crosswalk

| Catalog component | Beesack/source-family readings | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| solutions | nontrivial or linearly independent real solutions of one second-order equation | functions plus a source-faithful solution predicate | carrier, scalar field, regularity, and equation semantics absent |
| linear independence | no constant linear relation between `y1,y2`; source proof relates this to nonzero Wronskian | `LinearIndependent ℝ ![y1,y2]` or checked equivalent | encoding and domain absent |
| zeros | zeros on a compact interval or consecutive zeros on an open/extended interval | `y x = 0`, membership, endpoint and consecutiveness predicates | endpoint and isolation conventions absent |
| interlace | precisely one zero of the other solution between consecutive zeros; possibly reciprocal | `∃! x ∈ Set.Ioo x1 x2, y2 x = 0` plus optional symmetric clause | exact strength and binder scope absent |
| equation | `(r y')' + s y = 0`, or another equivalent second-order form | nested derivative/HasDeriv predicate or checked transport | equation form and coefficient assumptions absent |
| 1836/Jacques Sturm | historical catalog attribution | provenance only | no historical edition or theorem locator supplied |
| `已验证` | untrusted inventory label | no declaration or proof body | explicitly rejected as evidence |

## Required source admission

The statement phase must preserve and hash a lawful complete source edition, select an exact result
and proof boundary, transcribe every incorporated definition, ordered binder, hypothesis, conclusion,
and boundary case, and obtain independent source review. It must explain whether the catalog root is
the classical compact theorem, Beesack Theorem 1(b), the full singular-endpoint extension, or another
pinpointed version, then freeze and mutation-test the same exact Lean expression.

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks
generic derivative algebra, monotonicity, Rolle, intermediate-value, and pairwise linear-independence
APIs. A bounded case-insensitive search found no Sturm separation or functional Wronskian terminal
declaration in repo-local Lean or pinned mathlib; the Wronskian hits were polynomial-only. This is
discovery evidence, not the downstream exhaustive anchor audit or a global absence claim.
