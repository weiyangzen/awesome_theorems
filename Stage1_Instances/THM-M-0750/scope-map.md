# THM-M-0750 scope map

## Preserved repository scope

The intake preserves target `THM-M-0750`, the title `图灵度`, the gloss `不可解度的结构`, the Emil
Post attribution, and the year 1944. This identifies the Turing-degree subject area, but it supplies
no formula, source theorem locator, ordered binders, hypotheses, or conclusion.

The mathematical family in scope starts from an explicitly chosen notion of oracle computability
and reducibility, forms equivalence classes under mutual reducibility, and studies the induced order.
This is a boundary around possible source-faithful statements, not a conjunction or substitute
theorem.

## Proposition-changing decisions

Before statement work can close, an immutable source and independent review must fix:

1. Whether reducibility is between subsets of natural numbers, characteristic functions, partial
   functions, decision problems, reals, or another explicitly encoded oracle object.
2. The computation model and oracle convention, including total versus partial functions, the
   treatment of undefined oracle answers, coding of tuples and queries, and the exact definition of
   `A <=_T B`.
3. Whether the intended root is a definition, equivalence-relation theorem, quotient/order theorem,
   least-degree theorem, join-semilattice theorem, density or incomparability theorem, or another
   named structural result.
4. If a quotient is used, the representative carrier, equivalence relation, quotient versus
   antisymmetrization construction, equality convention, induced order, and checked transports
   between set and partial-function presentations.
5. Every ordered binder, universe, side condition, classical or choice principle, and exact
   conclusion, including whether multiple structural properties form one conjunction.
6. The primary edition, theorem/definition and page locator, incorporated definitions, proof
   boundary, corrections or errata, historical attribution, and source-to-statement review.

## Boundary and degenerate cases

The statement phase must explicitly decide empty and universal sets, nowhere-defined and constant
partial functions, computable oracles, equality versus extensional equality, the least computable
degree, quotient representatives, empty oracle sets, and malformed or nondecidable encodings. No
case is silently excluded at intake.

## Neighbor and substitution exclusions

- `THM-M-0748` and `THM-M-0749` separately own Post's problem and the Friedberg-Muchnik theorem;
  existence of intermediate or incomparable computably enumerable degrees cannot be substituted.
- `THM-M-0751` separately owns the supremum or lattice-structure topic. A join construction or
  upper-bound theorem cannot be silently selected here.
- `THM-M-0752` separately owns the jump operator, and `THM-M-0758` owns computably enumerable
  degrees. Their statements and proof evidence do not transfer to this root.
- The outside-Stage1 computer-science record `THM-C-0011` names Turing reducibility. It is evidence
  of a definition boundary only and receives no Stage1 slot or proof credit here.
- Many-one, truth-table, enumeration, polynomial-time, and other degree structures are excluded
  unless an approved source explicitly selects and relates them to this target.
- Merely defining an equivalence class, projecting `PartialOrder` from an assumed structure, or
  citing the catalog label `已验证` cannot establish an unspecified structural theorem.

## Primary-source boundary

An observed publisher version-of-record PDF of Post's 1944 paper was inspected and bound by
SHA-256. On printed pages 289-290, Post explains that mutual reducibility gives the same degree of
unsolvability, one-way reducibility a lower degree, and non-reducibility both ways incomparable
degrees. He frames determination of degrees for unsolvable decision problems of recursively
enumerable sets as a primary problem. Section 11, printed pages 311-312, gives an explicitly
informal account of general or Turing reducibility for decision problems of recursively enumerable
sets via a terminating yes/no procedure with adaptive oracle questions. On page 312 he writes that
the discussion is informal and proceeds "as if" formalized. The paper ends on printed page 314 with
the lower-degree question unresolved.

Thus the primary paper strengthens the topic and model boundary but does not select one theorem for
the catalog row. It also exposes a required transport: Post's set/decision-problem and total yes/no
oracle discussion is not definitionally the same as mathlib's arbitrary partial-function
`RecursiveIn` presentation.

## Pinned formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Computability.TuringDegree` defines `TuringReducible` using `RecursiveIn`, defines
`TuringEquivalent` as the antisymmetric relation, proves the relevant equivalence properties,
defines `TuringDegree` by antisymmetrization, and supplies a `PartialOrder` instance. The bounded
`IntakeProbe.lean` checks those interfaces and reports `propext` for two representative proofs.

These are discovery-only candidates. The module's partial-function presentation, its 1989
secondary reference, and its particular structural declarations are not automatically identical to
the catalog's 1944 gloss. Because no canonical proposition exists, no declaration is credited as a
usable root artifact, and the machine status remains `M4` pending statement selection.
