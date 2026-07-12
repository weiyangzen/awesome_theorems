# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:121-126` supplies exactly the theorem title, the attribution
Leopold Kronecker/Heinrich Weber, the year 1887, the claim
`有理数域的有限阿贝尔扩张都包含于分圆域`, importance "high," and status `已验证`.
Git history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, stable source
identifier, formula, definition, ordered binder, hypothesis, proof boundary, errata, reviewer, or
formal artifact.

`Docs/Stage0_Blueprint.md:501-526` repeats the literal claim while explicitly leaving the target
formal system, foundations, exact definitions and premises, proof path, dependencies, alternate
forms, axioms, machine state, and artifact links open. Its generic statement that a closed result
is known is planning metadata, not proof evidence. The rev-5.6 manifest retains `已验证` only as
`source_status_untrusted` and resets this target to `L0 / rework_required`.

## Literal crosswalk

| Catalog component | Required mathematical content | Prospective Lean content | Intake result |
|---|---|---|---|
| rational field | an explicitly fixed base field `Q` | `ℚ` and a coherent `Algebra ℚ K` | base is identifiable; presentation open |
| finite extension | finite dimension over `Q` or an equivalent number-field condition | `FiniteDimensional ℚ K`, `NumberField K`, or a tower object | exact representation open |
| abelian extension | a finite Galois extension whose Galois group is abelian | likely `IsAbelianGalois ℚ K`, after declaration audit | incorporated hypotheses open |
| cyclotomic field | `Q(zeta_n)` for a source-fixed root-of-unity convention | `CyclotomicField n ℚ` with the intended algebra instance | model and index convention open |
| contained in | literal inclusion, embedding, or intermediate-field equivalence | `Nonempty (K ->ₐ[ℚ] CyclotomicField n ℚ)` or a checked alternate form | relationship not yet checked |
| universal claim | every finite abelian extension has some cyclotomic host | ordered type and instance binders followed by `exists n` | exact quantifiers not frozen |
| Kronecker/Weber, 1887 | historical attribution | provenance metadata only | no pinpoint proof-source credit |
| `已验证` | untrusted inventory field | accepted source reviews and kernel receipts would be required | no H0 or M credit |

The phrase "contained" is the main presentation boundary. A literal inclusion presupposes one
ambient algebraic closure, whereas an abstract number-field type generally supports an embedding
or an equivalence with an intermediate field. Those are standard related formulations, but
rev-5.6 requires their relationship to be source-reviewed and kernel-checked rather than assumed.

## Duplicate-record boundary

The manifest separately includes `THM-M-0419`, also named the Kronecker-Weber theorem, in the
number-theory/algebraic-number-theory category. Its shorter source gloss omits the containment
conclusion, and it owns a historical Stage1 slot. It is not an alias declared by the authoritative
target manifest, so its evidence and state cannot be transferred to `THM-M-0014`.

The sibling legacy module
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_074.lean` is useful discovery input. It proposes
a number-field/abelian-Galois/algebra-embedding statement shape, checks adjacent mathlib APIs, and
repeatedly records that the terminal containment theorem is absent. Under the uniform rev-5.6 L0
baseline it is unaccepted even for its owning target; for this target it receives zero statement,
source, and proof credit.

## Bibliographic discovery candidates

- Lawrence C. Washington, *Introduction to Cyclotomic Fields*, second edition, Graduate Texts in
  Mathematics 83, Springer, 1997, Chapter 14, "The Kronecker-Weber Theorem," pages 321-331, book
  DOI `10.1007/978-1-4612-1934-7`, is a standard modern source candidate. Official chapter
  metadata supports the broad containment wording but is not a proof-passage audit.
- Daniel A. Marcus, *Number Fields*, second edition, Springer Universitext, 2018, is a secondary
  comparison candidate for the cyclotomic-field treatment.

These leads are not admitted here as H0 evidence. No physical or immutable full edition, exact
theorem and proof passage within the cited chapter, incorporated assumptions, proof-node
crosswalk, errata decision, or independent review was completed for this intake.

## Source gate

Before `H0` or statement acceptance, accountable reviewers must preserve an immutable edition,
identify the exact theorem and proof passages, transcribe all incorporated definitions, ordered
binders, hypotheses, conclusion, and exceptional cases, audit errata, decide the containment
presentation, map every material premise and proof transition, reconcile the duplicate target,
and approve the human-to-Lean crosswalk. Until then the canonical statement and formal expression
remain null.

The provisional `H1` records a historically proved theorem with incomplete source fidelity. It
does not turn the catalog label into evidence and does not claim that the exact repository wording
has already passed source review.
