# THM-M-0030 scope map

## Human claim selected at intake

Let `R` be a commutative Noetherian local ring and `I` a proper ideal of `R`. Then
the intersection of the ideals `I ^ n` over every natural number `n` is the zero ideal.

The ordered mathematical binders are `R`, its commutative-ring structure, its Noetherian and local
ring hypotheses, `I`, and the properness hypothesis. The conclusion concerns the ideal lattice of
the same ring. This is a repository-scope selection from a short catalog gloss, not an H0 finding.
Its exact Lean encoding is now self-tested pending master acceptance.

## Scope decisions

| Surface | Intake-selected meaning | Open verification |
|---|---|---|
| Ring | arbitrary commutative Noetherian local ring `R` | exact `Type u` and typeclass context frozen; historical fidelity open |
| Ideal | arbitrary proper `I : Ideal R` | checked encoding as the proposition `I ≠ ⊤` |
| Powers | ordinary ideal powers indexed by every `n : Nat`, starting at zero | exact notation, index, and expression frozen |
| Intersection | infimum of all `I ^ n` in the ideal lattice | membership alternate encoding connected by checked iff |
| Conclusion | the intersection equals the zero ideal | canonical elaboration and four mutation classes self-tested |

## Boundary cases

- The properness hypothesis is material. `I = top` is excluded because all its powers remain `top`.
- `I = bot` is included; the first positive power already forces the intersection to `bot`.
- The index starts at zero. The zeroth power is `top` and does not alter the intersection.
- The maximal ideal, nilpotent ideals, and nonmaximal proper ideals are included as instances of
  the general ideal binder, not separate roots.
- No domain, reducedness, completeness, dimension, principal-ideal, or characteristic premise is
  added. Mathlib's `IsLocalRing` convention includes nontriviality, which the frozen context records.

## Related forms not credited as the root

Stacks tag `00IP` states the stronger finite-module form: for a finite module `M`, the intersection
of `I ^ n M` is zero. Pinned mathlib exposes this as
`Ideal.iInf_pow_smul_eq_bot_of_isLocalRing`. It remains uncredited because this statement packet
does not select the stronger module form as its root. The anchor audit now authenticates the pinned
ideal theorem that specializes this bridge to `M = R`; both remain one deduplicated proof path.

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

## Statement evidence and downstream handoff

`Statement.lean` elaborates the exact ideal target using only `Ideal.Operations`, `LocalRing.Defs`,
and `Noetherian.Defs`; deleting any one direct import fails. The membership iff, top and bottom
boundary witnesses, expression/environment fingerprints, and four required mutation classes are
recorded in `statement.json` and the provisional statement receipt. The anchor audit alone owns the
later proof-body, provenance, dependency, axiom, and TCB classification. Historical source
admission and independent review remain open on H. `AnchorAudit.lean` separately copies this exact
target and checks the pinned mathlib candidate; its candidate classification is provisional
`M0-W / E2`, while the accepted root stays `M3` pending later gates and master acceptance.
