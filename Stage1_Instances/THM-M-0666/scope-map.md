# Scope map

## Metadata boundary

The authoritative target manifest supplies the name "Pila-Zannier theorem" and Stage0 supplies only
the gloss "special points in o-minimal structures". This does not determine what ambient variety
or definable set is used, what "special" means, or what conclusion is asserted. A proof method is
not itself a proposition. Intake must not borrow the more specific Manin-Mumford statement from
`THM-M-0465`, despite the duplicated name.

## Candidate mathematical boundary

A source-faithful theorem in the Pila-Zannier strategy may require some or all of the following,
depending on the primary theorem selected:

- an algebraic or Shimura variety and a uniformizing/period map into an o-minimal definable domain;
- a precisely defined special-point or torsion-point locus;
- a height and complexity convention, with finite bounded-height sets;
- a Pila-Wilkie-type upper bound outside the algebraic part;
- lower bounds for Galois orbits and height/degree comparison;
- functional transcendence or Ax-Lindemann input identifying positive-dimensional algebraic parts;
- a conclusion such as finiteness, non-density, or containment in finitely many special
  subvarieties.

These are a candidate ingredient inventory, not hypotheses or conclusions of a frozen root.

## Variant decision required

The statement phase must use a pinpoint primary source to decide among inequivalent possibilities,
including:

1. the Manin-Mumford torsion-coset theorem proved by Pila and Zannier in 2008;
2. an Andre-Oort finiteness/density theorem for a specified Shimura variety;
3. a Zilber-Pink or other unlikely-intersection result for a specified family; or
4. a methodological reduction theorem combining o-minimal counting, Galois lower bounds, and
   functional transcendence.

The repository wording alone selects none of these. The selected source must fix the ambient
category, base field, definability structure, special locus, dimensions, irreducibility and
connectedness assumptions, height normalization, binder order, and all empty/zero-dimensional
boundary cases.

## Explicit exclusions

- Substituting `THM-M-0465` merely because its translated title is identical.
- Calling the Pila-Wilkie rational-point counting theorem alone the Pila-Zannier theorem.
- Replacing special points by an arbitrary predicate or assuming the desired finiteness as data.
- Restricting to an elliptic curve, a torus, or a zero-dimensional/empty locus only to obtain an
  easier Lean proposition.
- Treating the Stage0 `已验证` label or a bibliography entry as human or machine proof evidence.

Before proof-tree construction, the statement phase must freeze the complete intake-contract
record, elaborate its exact Lean expression, fingerprint its environment, and mutation-test the
domain, hypotheses, binder scope, and boundary cases.
