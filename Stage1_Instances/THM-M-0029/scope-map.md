# THM-M-0029 scope map

## Preserved theorem family

The catalog preserves only these facts: the item is called Nakayama's lemma, concerns generators
of modules, and belongs to ring theory. It does not select an exact formulation. A later statement
freeze must use an immutable, independently reviewed source passage to choose one root.

## Candidate forms, not credited

1. Determinant-trick form: for a finitely generated submodule `N`, if `N <= I N`, then some scalar
   congruent to one modulo `I` annihilates `N`.
2. Jacobson-radical vanishing form: if finitely generated `N <= I N` and `I` lies in the Jacobson
   radical, then `N = 0`.
3. Local-ring specialization: for a finitely generated module over a local ring, equality with the
   maximal-ideal multiple forces the module to vanish.
4. Generator-lifting form: for finitely generated `N`, a set spanning the quotient image of `N`
   modulo `I N` has selected representatives spanning `N`, under a Jacobson-radical hypothesis.
5. Relative submodule form: generators modulo a submodule suffice after a Jacobson-radical
   correction.

These forms are related, but relationship proofs and extra assumptions are material. No row is the
canonical root at intake.

## Decisions required at statement freeze

- Select the exact source formulation, edition, theorem or lemma number, page, definition chain,
  proof boundary, corrections, and errata.
- Fix commutative versus noncommutative rings, unital conventions, and left/right module actions.
- Fix the whole module versus an ambient submodule `N`, finite generation convention, and any
  nontriviality premise.
- Fix the ideal: arbitrary `I`, containment in the ring Jacobson radical, containment in the
  Jacobson radical of another ideal, or the maximal ideal of a local ring.
- Fix whether the premise is `N <= I N`, `N = I N`, or a relative containment modulo another
  submodule.
- Fix whether the conclusion is an annihilating scalar, `N = 0`, a properness result, a spanning
  lift, a bijection on generators, or a minimal-generator statement.
- Fix ordered binders, universe and coercion choices, quotient and span encodings, and all checked
  implication or equivalence directions.

## Boundary and degenerate cases

The exact source must decide the zero ring, zero module, zero submodule, `I = 0`, `I = top`, empty
generating sets, trivial quotients, and whether `Nontrivial R` or `Nontrivial M` is required. Intake
does not exclude any case or infer it from a candidate Lean theorem.

## Non-substitution rules

- Do not replace a generator-lifting statement with the vanishing form, or conversely, without a
  checked source relationship covering every premise and conclusion.
- Do not weaken the target to fields, finite modules, cyclic modules, or one example.
- Do not broaden a commutative source to a noncommutative theorem or a local source to all ideals.
- Do not treat a theorem name, `#check`, source-status label, axiom report, or nearby use in mathlib
  as exact statement identity or proof credit.
- Do not assume the desired conclusion through a structure instance, axiom, oracle, or unchecked
  certificate.

## Downstream handoff

`S56-M-0029-STATEMENT` must admit and review an exact source passage, select one formulation,
elaborate it with minimal pinned imports, record expression and environment fingerprints, and run
the required mutation classes. Only the later anchor audit may classify candidate proof bodies,
dependencies, provenance, axioms, and trust closure.
