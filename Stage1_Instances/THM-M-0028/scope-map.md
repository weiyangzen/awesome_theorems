# THM-M-0028 scope map

## Human claim selected at intake

For every commutative ring `R`, if every ideal of `R` is finitely generated, then every ascending
sequence `I_0 <= I_1 <= ...` of ideals of `R` eventually stabilizes.

"Eventually stabilizes" means that there is an index `n` such that `I_m = I_n` for every
`m >= n`. The ordered mathematical binders are the carrier `R`, its commutative-ring structure,
the finite-generation premise, and the monotone ideal chain. The conclusion supplies a
stabilization index and the tail equality. The exact Lean target freezes a modern unital
specialization; the historical source explicitly did not require a unit, so fidelity to the wider
historical domain remains open rather than hidden.

This is a repository-scope selection from a short catalog gloss, not an `H0` source finding. The
statement phase has elaborated and fingerprinted that explicitly bounded modern target. A complete
historical-domain translation and independent source review remain open on the H axis.

## Scope decisions

| Surface | Selected meaning | Open verification |
|---|---|---|
| Base object | arbitrary unital commutative ring `R` | historical nonunital-domain fidelity remains open |
| Chain | natural-number-indexed monotone sequence of ideals under inclusion | exact `OrderHom` encoding frozen; source equivalence to unrestricted ACC remains open |
| Stabilization | some `n` satisfies `I_m = I_n` for all `m >= n` | binder order, equality, and order-direction fingerprint frozen |
| Premise | every ideal of `R` is finitely generated | exact explicit premise frozen; predicate reformulation remains an adjacent uncredited candidate |
| Root relation | finite generation implies chain stabilization | exact source-to-Lean ratification; converse remains a related form |
| Logic | ordinary proposition with no computational output | foundation and transitive trust audit |

## Domain and boundary cases

- The zero ring is included. Lean's `CommRing` does not require `Nontrivial`; a subsingleton witness,
  concrete `PUnit` probe, and boundary mutation freeze this choice.
- The sequence may be constant from the start; `n = 0` is allowed. Repeated equal ideals do not
  violate monotonicity.
- The condition quantifies over all natural-number-indexed monotone chains, including chains with
  long finite strict prefixes. It is not a bounded-chain or finite-ring statement.
- Fields, principal ideal rings, finite rings, and integral domains are instances of the general
  domain, never replacements for it.
- The chosen commutative convention avoids silently choosing a side for noncommutative ideals.
  Mathlib's generic regular-module definition can express a left-Noetherian convention; any use of
  it needs a checked relationship to the selected commutative ideal formulation.
- The converse implication, full biconditional, strict-chain nonexistence, well-foundedness of
  strict inclusion, and maximal-element formulation are related formulations. They receive no
  credit until the statement phase supplies directionally checked transports.

## Non-substitution rules

- Do not substitute Hilbert's basis theorem, Noether normalization, the Lasker-Noether theorem, or
  a theorem about spectra merely because each uses the word "Noetherian."
- Do not replace ascending chains by descending chains or Noetherianity by Artinianity.
- Do not weaken the claim to a field, PID, finite ring, fixed ring, or fixed chain.
- Do not broaden it to noncommutative left/right Noetherian rings without a source decision and a
  checked transport back to the commutative root.
- Do not assume either side through a typeclass premise, structure field, oracle, experiment, or
  unchecked certificate.
- Do not treat the catalog's verified label, a declaration name, or successful `#check` output as
  source or proof credit.

## Downstream handoff

The statement phase has frozen the commutative, one-way, natural-chain, ideal, modern-unital, and
zero-ring choices; used the sole minimal `Finiteness.Defs` import; elaborated and fingerprinted the
canonical target; checked its carrier and monotone-function encodings; and exercised all four
mutation classes. Complete
historical-domain fidelity and independent source review remain open. The anchor audit has now
authenticated the exact pinned mathlib composition, checked its bodies, placeholder and axiom
reports, provenance boundary, and literal adapter, and classified it as an unaccepted
`M0-W / E2` candidate. It also classifies the exact immutable Atlas wrapper as `M1 / E2` outside
the dependency and license boundary. Obligation-tree expansion, proof-phase integration, complete
transitive trust, release-grade evidence, and independent review remain open.
