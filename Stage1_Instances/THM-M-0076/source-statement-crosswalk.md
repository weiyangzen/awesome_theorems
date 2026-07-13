# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md:561-566` supplies exactly the title `布劳尔特征标定理`, Richard
Brauer attribution, year 1956, gloss `模表示论中特征标的性质` ("properties of characters in modular
representation theory"), importance high, and formalization status `已验证`. All six uncited fields
originate in repository commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:2190-2215` repeats the gloss while explicitly leaving the formal system,
exact definitions and premises, proof route, dependencies, equivalent forms, axioms, machine
status, and artifact links open. The rev-5.6 manifest retains `已验证` only as untrusted metadata and
resets the target to `L0 / rework_required`.

Neither record gives a bibliography, edition, theorem/page, formula, definition chain, ordered
binders, hypotheses, conclusion, proof boundary, translation/correction history, or reviewer. The
repository description is consequently `H5` at intake because it is not a stable proposition. It
is neither `H0` source evidence nor a statement that can be elaborated without inventing
mathematics. Source identification and a corrected exact statement must precede reclassification.

## Bibliographic leads, not accepted sources

A bounded Crossref query on 2026-07-13 returned related records:

- R. Brauer and C. Nesbitt, "On the Modular Characters of Groups," *Annals of Mathematics* 42(2)
  (1941), starting page 556, DOI `10.2307/1968918`;
- Richard Brauer, "On the Connection Between the Ordinary and The Modular Characters of Groups of
  Finite Order," *Annals of Mathematics* 42(4) (1941), starting page 926, DOI
  `10.2307/1968774`;
- Richard Brauer and John Tate, "On the Characters of Finite Groups," *Annals of Mathematics* 62
  (1955), starting page 1, DOI `10.2307/2007097`.

The records are bibliographic metadata, not inspected primary text. The first two are relevant
source-family candidates but conflict with the catalog's 1956 date; the third is a likely
ordinary-character/Brauer-induction boundary and must not be substituted. No exact theorem
passage, definitions, assumptions, proof, errata, edition digest, or independent review was
admitted at intake.

## Clause crosswalk

| Repository phrase | Material interpretations requiring a source decision | Pinned Lean surface | Intake status |
|---|---|---|---|
| "modular representation theory" | finite-group representations in positive characteristic; a `p`-modular system; modules over a residue field | general `Representation k G V` exists, but no selected modular-system or Brauer-character API was located | domain, coefficient data, and splitting assumptions absent |
| "character" | ordinary trace character; Brauer character on prime-regular elements; a class in a character/Grothendieck group | `Representation.character` is an ordinary trace on every group element | ordinary character is adjacent only and cannot define the requested root |
| "Brauer character" in the title | construction via eigenvalue/root lifts; irreducible Brauer characters; relations with ordinary characters; decomposition maps | no exact pinned declaration located | title identifies a family, not a conclusion |
| "properties" | well-definedness, class-function behavior, additivity, irreducibility, basis/completeness, decomposition numbers, blocks, lifting, or another theorem | no exact proposition can be matched before this choice | canonical conclusion and binders remain null |
| "Richard Brauer / 1956" | historical attribution or publication date | no formal analogue | Crossref leads are 1941/1955; identity and date require primary-source review |
| "verified" | historical catalog metadata | no receipt or declaration | untrusted; supplies no `H0`, `M0`, accepted state, or completion credit |

## Pinned formal boundary

The read-only pinned mathlib tree is revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. `IntakeProbe.lean` elaborates ordinary
representation-character interfaces and the unrelated Haar modular-character interface to make the
name collision explicit. Bounded mathlib and repository searches found no exact finite-group
Brauer-character theorem or usable target artifact. This supports provisional `M4`; it is not an
exhaustive anchor audit and does not establish nonexistence outside the bounded search.

## Neighbor and non-substitution boundary

- `THM-M-0037` is the Brauer group theorem for central simple algebras, not Brauer characters.
- `THM-M-0067` is Maschke's semisimplicity theorem in nonmodular characteristic, not this target.
- `THM-M-0068` is ordinary group-character orthogonality, not modular Brauer-character theory.
- `THM-M-0429` is Brauer's meromorphic-continuation theorem for Artin L-functions, not this target.

The first source-statement gate fails closed: preserve and independently review an authoritative
source passage, reconcile its identity and date with the repository record, select one exact
proposition, and map every definition, domain, binder, hypothesis, conclusion, and boundary case
before a canonical Lean target may be frozen.
