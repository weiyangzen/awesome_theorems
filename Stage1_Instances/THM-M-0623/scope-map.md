# Scope map

## Received claim

The repository supplies the title "Urysohn metrization theorem" and the gloss "a second-countable
regular space is metrizable." It supplies no definition of regularity or metrizability, no
separation convention, no binders, and no pinpoint source. Intake therefore freezes a recognized
theorem-family boundary, not an invented canonical proposition.

## Convention-sensitive boundary

There are two materially different readings that must not be conflated:

1. Under a convention where "regular" already includes a separation axiom such as T1 or T0, the
   familiar metric conclusion is plausible. Pinned mathlib represents the relevant full hypothesis
   by `T3Space X`, defined as `T0Space X` plus `RegularSpace X`, and concludes
   `MetrizableSpace X`.
2. Under mathlib's weaker `RegularSpace X`, no point-separation property is included. Together with
   `SecondCountableTopology X`, mathlib concludes only `PseudoMetrizableSpace X`.

The unrestricted Lean reading

```text
[TopologicalSpace X] [RegularSpace X] [SecondCountableTopology X] -> MetrizableSpace X
```

is false. A non-singleton finite type with the indiscrete topology is regular and second-countable
but not T0, whereas `MetrizableSpace` extends `T0Space`. This boundary rules out silently treating
bare mathlib regularity as sufficient for a metric conclusion.

## Candidate formal boundaries

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Topology.Metrizable.Urysohn` provides:

- `PseudoMetrizableSpace.of_regularSpace_secondCountableTopology`: bare `RegularSpace` plus
  `SecondCountableTopology` gives a compatible pseudometric structure;
- `metrizableSpace_of_t3_secondCountable`: `T3Space` plus `SecondCountableTopology` gives a
  compatible metric structure;
- `exists_isInducing_l_infty` and `exists_embedding_l_infty`: inducing-map and embedding forms
  used in the corresponding constructions.

These are strong exact-topic formal candidates. They remain uncredited at intake because the
catalog-to-source regularity convention, pseudometric-versus-metric conclusion, exact structure
encoding, and checked transports have not been accepted.

## Decisions required at statement freeze

1. Preserve and independently inspect an immutable primary or authoritative source edition,
   recording the exact theorem/page, all incorporated definitions and assumptions, proof boundary,
   translation, corrections, and errata.
2. Fix whether "regular" includes T0, T1, or Hausdorff separation, or whether a separate separation
   hypothesis must be added.
3. Fix whether "metrizable" means a genuine metric or allows a pseudometric, and whether the result
   is encoded as a compatible structure, equality of induced topology, an inducing map, or an
   embedding.
4. Fix the ambient type, universe, topology, typeclass order, all explicit and implicit hypotheses,
   and the exact conclusion.
5. Decide empty, singleton, non-T0 indiscrete, finite, discrete, already metrizable, and other
   boundary cases without silently excluding them.
6. Classify the Urysohn-versus-Tychonoff attribution and theorem version rather than transferring a
   library comment into source authority.
7. Compile checked relationships for every credited alternate encoding and mutation-test removed
   hypotheses, changed domains, binder scope, and boundary cases.

## Explicit exclusions

- Do not replace metric metrizability by pseudometrizability merely to fit bare `RegularSpace`.
- Do not silently add T0, T1, Hausdorff, or T3 assumptions merely to fit the pinned metric instance.
- Do not substitute Urysohn's lemma (`THM-M-0621`), Tietze extension (`THM-M-0622`), the
  Nagata-Smirnov theorem (`THM-M-0624`), or Bing's metrization theorem (`THM-M-0625`).
- Do not substitute only the l-infinity inducing-map or embedding result without an accepted
  relationship to the source claim.
- Do not use first countability, separability, a converse implication, or a finite/singleton special
  case as the general root.
- Do not encode the missing conclusion in an axiom, assumed certificate, structure field, or
  hypothesis, and do not treat the catalog label, theorem name, or API probe as proof evidence.

No canonical Lean expression, ordered binder list, hypothesis list, alternate encoding, or
degenerate-case exclusion is frozen in this intake.
