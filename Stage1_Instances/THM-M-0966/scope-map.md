# Scope map

## Preserved theorem family

The intended root must remain a finite-set Kruskal-Katona minimum-lower-shadow theorem. Intake does
not silently choose among these materially different formulations:

1. **Colex minimizer comparison.** For an `r`-uniform family `A` and a colex initial segment `C`
   with `|C| <= |A|`, the lower shadow of `C` has cardinality at most that of `A`. Pinned
   `Finset.kruskal_katona` has this shape.
2. **Exact-cardinality minimization.** For a family of `m` many `r`-sets, an initial colex segment
   of exactly `m` sets exists and minimizes the shadow. This incorporates an existence and
   cardinality-realization statement not present in the displayed basic Lean declaration.
3. **Binomial/cascade form.** Write `m` in its source-specified unique `r`-binomial representation
   and give the corresponding explicit lower bound for the shadow. The representation theorem,
   indices, strict inequalities, and zero conventions are part of this statement.
4. **Iterated-shadow form.** Bound the `i`-fold lower shadow. Pinned `Finset.iterated_kk` provides a
   colex comparison, while `Finset.kruskal_katona_lovasz_form` provides one binomial-threshold
   consequence.
5. **Equality characterization.** Classify every minimizer. Pinned mathlib explicitly lists this as
   future work, so it cannot be inferred from the inequality declaration.

## Decisions required at statement freeze

1. Admit an immutable primary edition and select the exact theorem, corollary, or reviewed modern
   formulation represented by the catalog gloss.
2. Freeze one-step versus iterated shadow, colex comparison versus numerical cascade bound, and
   inequality alone versus attainment or equality classification.
3. Define the lower shadow precisely: delete exactly one element, take all `(r - 1)`-subsets, or
   use an iterated/inclusive shadow. Pinned `Finset.shadow` removes one element and deduplicates the
   results in a `Finset`.
4. Freeze the ground set as `Fin n`, an abstract finite type, or a finite subset of an infinite
   type, and provide checked transports for every credited alternate encoding.
5. Freeze the family encoding and multiplicity semantics. `Finset (Finset (Fin n))` has no duplicate
   members; an indexed family or multiset would change cardinality and shadow behavior.
6. State uniformity exactly (`Set.Sized r`) and decide whether arbitrary complexes or nonuniform
   families are part of the root.
7. Define colex order and initial segment. Mathlib's `Finset.Colex.IsInitSeg C r` includes both
   `r`-uniformity and downward closure among `r`-sets.
8. Resolve `n = 0`, `r = 0`, `r = 1`, `r > n`, empty and singleton families, `C.card < A.card`
   versus equality, and every natural-subtraction boundary in iterated or numerical forms.
9. For a cascade statement, freeze existence/uniqueness, index termination, binomial conventions,
   and what happens when the family cardinality is zero.
10. Freeze the foundation, TCB, computation, freshness, alternate-encoding, and statement-mutation
    profiles only after the exact root is selected.

## Explicit exclusions

- The Lovasz threshold consequence substituted for the full Kruskal-Katona theorem without a
  checked relationship in the required direction.
- An iterated-shadow theorem substituted for a one-step root, or conversely.
- Sperner's theorem, Erdős-Ko-Rado, Hilton-Milner, Lovasz-Kneser, or another neighboring extremal
  set theorem used as the root.
- An upper-shadow theorem obtained by complementation without a checked transport and all domain
  and cardinality side conditions.
- A weakened asymptotic estimate, one numerical example, or a theorem that assumes the desired
  extremal family or shadow bound.
- A docstring, theorem name, Crossref record, `#check`, axiom printout, or the catalog's untrusted
  `已验证` label used as statement identity, source proof, or machine completion evidence.

No canonical expression, statement fingerprint, checked transport, obligation registry,
discovery protocol, accepted proof state, or completion claim is frozen at intake.
