# Scope map

## Included topic boundary

- A source-selected definition of a Ramsey cardinal, normally expressed through a strong partition
  property for colorings of finite subsets of a set of cardinality `kappa`.
- The exact cardinal/type representation, arities, color set, homogeneous-set predicate, and
  cardinality requirement in that definition.
- The concrete property or characterization asserted by the selected source.
- Any hypotheses about infinitude, uncountability, regularity, foundations, or ambient models that
  the selected proposition actually uses.

## Ambiguities to resolve at statement freeze

The repository record does not decide among these materially different targets:

1. A definition using a coloring of all finite subsets simultaneously, with a size-`kappa` set
   whose subsets of each fixed finite arity are monochromatic (with the color allowed to depend on
   the arity).
2. A family of partition relations stated separately for every finite arity and a specified number
   of colors, with potentially different homogeneous sets.
3. Variants using two, finitely many, or countably many colors, or stronger regressive partition
   properties.
4. A measure, elementary-embedding, indiscernibility, or model-theoretic characterization.
5. A theorem about regularity, inaccessibility, indescribability, consistency strength, or another
   consequence, rather than the defining partition property.

The statement phase must inspect an immutable statement-bearing source and freeze ordered binders,
the exact arrow/partition convention, simultaneous versus arity-by-arity homogeneity, the
cardinality equality for the homogeneous subset, and the conclusion. It must also settle zero
arity, finite and countable boundary cases, lifted universe levels, and whether the claim is about a
cardinal, an initial ordinal, or a carrier type.

## Explicit exclusions

- Weakly compact, measurable, ineffable, Rowbottom, Erdos, or indescribable cardinals as substitutes.
- Finite Ramsey's theorem or the infinite Ramsey theorem on `Nat` as the requested large-cardinal
  target.
- Replacing the requested result with a freshly defined predicate followed by a tautological
  projection.
- Treating partition-relation formulations, measure formulations, and embedding formulations as
  equivalent without source-faithful statements and checked Lean transports.
- Treating the repository label `已验证` as evidence of a human proof or kernel closure.

No canonical Lean target is frozen at intake because the repository source does not identify a
unique proposition.
