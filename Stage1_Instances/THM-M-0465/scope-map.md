# Scope map

## Included claim

- An abelian variety `A` and a closed subvariety `X` of `A`.
- Torsion points of the group of geometric points of `A` lying in `X`.
- Finiteness of maximal torsion cosets in `X`, equivalently containment of all torsion points in a
  finite union of torsion translates of abelian subvarieties contained in `X`.
- The characteristic-zero/algebraically closed field conventions selected by the inspected source.

## Decisions deferred to the statement phase

Primary-source inspection must settle whether the paper states the result over `C`, over
`Qbar`, or after an embedding; whether `X` is irreducible; the exact meaning of torsion coset and
maximality; reducedness and closed-point conventions; and which direction of the equivalence is the
canonical target. It must also freeze universes, binder order, empty and zero-dimensional cases,
and whether the result is phrased via Zariski density or a finite union.

## Explicit exclusions

- The broader Mordell-Lang, Andre-Oort, or Zilber-Pink conjectures.
- Merely the Pila-Wilkie counting theorem or Ax-Lindemann input used by the proof method.
- A statement only for elliptic curves, algebraic tori, or curves as a substitute for abelian
  varieties and arbitrary closed subvarieties.
- A structure that assumes the desired finite decomposition as a field.

The statement phase must use concrete mathlib notions or record precise missing APIs; it may not
replace the geometric theorem with an abstract finite-set consequence.
