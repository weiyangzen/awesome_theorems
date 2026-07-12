# THM-M-0030 scope map

## Human claim selected at intake

Let `R` be a commutative Noetherian local ring and `I` a proper ideal of `R`. Then
the intersection of the ideals `I ^ n` over every natural number `n` is the zero ideal.

The ordered mathematical binders are `R`, its commutative-ring structure, its Noetherian and local
ring hypotheses, `I`, and the properness hypothesis. The conclusion concerns the ideal lattice of
the same ring. This is a repository-scope selection from a short catalog gloss, not an H0 finding
or an accepted canonical Lean statement.

## Scope decisions

| Surface | Intake-selected meaning | Open verification |
|---|---|---|
| Ring | arbitrary commutative Noetherian local ring `R` | historical source convention and exact Lean universe/context |
| Ideal | arbitrary proper `I : Ideal R` | source definition and checked encoding of properness as `I != top` |
| Powers | ordinary ideal powers indexed by every `n : Nat`, starting at zero | notation, index, and expression fingerprint |
| Intersection | infimum of all `I ^ n` in the ideal lattice | membership/intersection alternate encoding and checked transport |
| Conclusion | the intersection equals the zero ideal | canonical elaboration and statement mutations |

## Boundary cases

- The properness hypothesis is material. `I = top` is excluded because all its powers remain `top`.
- `I = bot` is included; the first positive power already forces the intersection to `bot`.
- The index starts at zero. The zeroth power is `top` and does not alter the intersection.
- The maximal ideal, nilpotent ideals, and nonmaximal proper ideals are included as instances of
  the general ideal binder, not separate roots.
- No domain, reducedness, completeness, dimension, principal-ideal, or characteristic premise is
  added. Mathlib's `IsLocalRing` convention includes nontriviality; the statement phase must record
  and source-map that convention rather than hide it.

## Related forms not credited as the root

Stacks tag `00IP` states the stronger finite-module form: for a finite module `M`, the intersection
of `I ^ n M` is zero. Pinned mathlib exposes this as
`Ideal.iInf_pow_smul_eq_bot_of_isLocalRing`. A later statement phase may connect it to the ideal
root only by a checked specialization with `M = R`.

The Jacobson-radical form, the integral-domain form, an adic Hausdorffness or completion statement,
and a result only for the maximal ideal are related theorems, not substitutions.

## Non-substitution rules

- Do not replace the local-ring claim with the domain variant or add a domain hypothesis.
- Do not weaken it to nilpotent, principal, maximal, or finitely generated chosen ideals.
- Do not broaden it to arbitrary modules without a checked relationship back to the ideal root.
- Do not substitute Artin-Rees, Nakayama's lemma, adic separatedness, or completion injectivity.
- Do not assume the conclusion through a structure field, oracle, experiment, or unchecked
  certificate.
- Do not treat the catalog's verified label, a declaration name, `#check`, or `#print axioms` as
  source or proof credit.

## Downstream handoff

The statement phase must admit and review a pinpoint source, ratify the ideal specialization and
all conventions above, elaborate a minimal-import target, preserve its expression and environment
fingerprints, check the module specialization transport if credited, and distinguish removed-
hypothesis, changed-domain, binder-scope, and boundary mutations. The anchor audit alone owns the
later proof-body, provenance, dependency, axiom, and TCB classification.
