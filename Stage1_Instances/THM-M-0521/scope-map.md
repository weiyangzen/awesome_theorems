# Scope map

## Included topic boundary

- Elliptic curves over the exact number field selected by the source, presumptively `Q`.
- The source's precise analytic-rank/nonvanishing hypothesis for the Hasse-Weil L-function.
- The Mordell-Weil rank and Tate-Shafarevich-group conclusions actually proved.
- Every modularity, conductor, Heegner-point, reduction, and finiteness hypothesis needed by the
  selected theorem and by any Gross-Zagier input.

## Ambiguities to resolve at statement freeze

1. **Rank:** the gloss may mean algebraic rank or analytic rank. These cannot be exchanged.
2. **Direction:** a standard consequence starts from analytic rank at most one; the literal Chinese
   gloss can be read as starting from algebraic rank zero or one.
3. **BSD strength:** rank equality and finiteness of the Tate-Shafarevich group are not the entire
   leading-coefficient formula, and integral, rational, and prime-primary forms differ.
4. **The named result:** Kolyvagin's Euler-system theorem, its Gross-Zagier corollary, and separate
   analytic-rank-zero and analytic-rank-one statements have different inputs.
5. **Curve class:** the field, modularity assumptions, conductor restrictions, and Heegner
   hypotheses must be explicit rather than inferred from a modern retrospective formulation.

The statement phase must select an immutable source passage, record its exact hypotheses and
conclusion, and independently review a normalized human statement before defining Lean binders.

## Explicit exclusions

- BSD for every elliptic curve of algebraic rank zero or one without additional hypotheses.
- The full Birch and Swinnerton-Dyer leading-coefficient formula unless the selected source proves it.
- `THM-M-0522` or the separate repository entry for Kolyvagin Euler systems as substitutes.
- A generic `LSeries` or Dedekind-domain `selmerGroup` theorem presented as the elliptic-curve result.
- An abstract structure containing the desired conclusion as a field followed by its projection.
- The repository label `已验证` as evidence of a source proof or machine proof.

No canonical Lean target is frozen at intake.
