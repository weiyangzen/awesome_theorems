# Source-statement crosswalk

## Repository record

`Docs/Stage0_Blueprint.md:14766-14791` names cellular homology and supplies only "computation of the
homology of a CW complex" as its statement. `Docs/researches/math_theorems.md:3995-3999` repeats this
metadata and attributes the topic generically to many mathematicians. Neither record gives a
publication, theorem number, page, coefficients, assumptions, or proof. The manifest's `已验证`
value is explicitly untrusted under rev-5.6 and supplies no H or M credit.

## Source candidates

- Allen Hatcher, *Algebraic Topology* (2002), section 2.2, especially Theorem 2.35, is a stable
  modern candidate for the cellular-homology comparison and its skeletal-filtration construction.
  The exact edition text, hypotheses, coefficient conventions, surrounding lemmas, and corrections
  must be inspected before it can define the root.
- J. H. C. Whitehead, *Combinatorial Homotopy I*, *Bulletin of the American Mathematical Society*
  55 (1949), is a historical primary-source lead for CW complexes, but this intake has not verified
  that it contains the exact modern cellular-homology statement required here.

These are discovery leads, not `H0` records. The statement phase must choose an actual proposition
and a source reviewer must verify edition, locator, assumptions, definitions, and errata.

## Crosswalk

| Repository phrase | Standard mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "CW complex" | a space with cells and skeletal filtration | concrete `CWComplex`/`RelCWComplex` data and skeleta | included; encoding and hypotheses open |
| "homology" | singular homology with fixed coefficients | one pinned singular-homology functor and grading | included; coefficients and grading open |
| "cellular" | relative groups of consecutive skeleta | relative homology objects `H_n(X^n, X^(n-1))` | included; API availability open |
| "computation" | cellular differential and resulting homology | a concrete chain complex and boundary maps | included; construction open |
| comparison conclusion | cellular homology agrees with singular homology | exact degreewise or graded natural isomorphism | intended root; exact strength open |
| optional refinement | cellular chains are free on cells; incidence formula | basis and attaching-map degree declarations | source-dependent; not root-frozen |

## Pinned Lean discovery boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the repository contains
`Mathlib.Topology.CWComplex.Classical.Basic` with `CWComplex`/`RelCWComplex` and
`Mathlib.AlgebraicTopology.SingularHomology.Basic` with `singularHomologyFunctor`. A scoped search
found no declaration text named "cellular homology" or "cellular chain". This is intake discovery,
not an exhaustive anchor audit and not proof that no differently named implementation exists.
`IntakeProbe.lean` checks only that the two discovered interfaces elaborate in the pinned project.

The relative-homology-of-skeleta construction, comparison theorem, exact declaration provenance,
and transitive trust closure therefore remain open. Until an exact source assertion is selected and
elaborated, `H2` and `M4` are the truthful classifications.
