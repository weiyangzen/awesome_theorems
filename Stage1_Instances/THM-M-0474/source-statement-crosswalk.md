# Source-statement crosswalk

## Repository source record

The target originates in `Docs/researches/math_theorems.md` lines 3483-3488 at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. It names Fermat's little theorem, attributes it to
Pierre de Fermat in 1640, and gives the complete mathematical text only as
`a^(p-1) congruent to 1 (mod p)`. `Docs/Stage0_Blueprint.md` lines 13001-13026 repeat that gloss
while explicitly leaving precise definitions and premises, proof history, axioms, equivalent
forms, and machine artifacts open. The manifest's `source_status_untrusted` value is metadata, not
source or proof evidence.

No primary-source edition, theorem/page or letter locator, immutable source artifact, translation,
assumption audit, errata check, or independent source review is present in the repository. The
catalog is therefore a discovery source only and cannot establish `H0`.

## Component crosswalk

| Catalog component | Conventional mathematical completion | Pinned Lean candidate | Intake disposition |
|---|---|---|---|
| `p` | prime natural modulus | `p : Nat`, `hp : p.Prime` | missing catalog premise; source confirmation required |
| `a` | residue represented by a natural or integer | implicit `{n : Nat}` in the closest natural declaration | domain not specified by catalog |
| nonzero residue | `gcd(a,p)=1`, equivalently `p` does not divide `a` when `p` is prime | `hpn : n.Coprime p` | missing catalog premise; unconditional reading refuted by `a=p` |
| exponent | `p - 1` | natural exponent `p - 1` | direct syntactic match under the prime premise |
| congruence | modulo `p` | `Nat.ModEq p (n ^ (p - 1)) 1` | closest candidate encoding |

## Lean discovery anchor

At the manifest-pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.FieldTheory.Finite.Basic` contains:

```text
Nat.ModEq.pow_card_sub_one_eq_one
  {p : Nat} (hp : p.Prime) {n : Nat} (hpn : n.Coprime p) :
  n ^ (p - 1) congruent to 1 [MOD p]
```

The same module contains the `ZMod` nonzero and units forms, the integer congruence form,
`Int.ModEq.pow_prime_eq_self`, and the natural remainder form. `IntakeProbe.lean` imports this one
module and checks those names in the pinned environment. That is real API and kernel elaboration
evidence for an `M3` candidate only. Intake does not freeze a canonical expression, conduct the
formal-candidate/provenance audit, inspect terminal proof bodies, or credit `M0-W`.

## Required statement/source follow-up

Before statement acceptance, a source reviewer must select a stable authoritative edition, give a
pinpoint theorem or historical text and translation, enumerate the prime and nondivisibility
assumptions, decide natural versus integer base, record equivalent-form boundaries and errata, and
obtain independent approval. The statement phase must then elaborate the exact selected target,
fingerprint it, and check transports and all mandated mutations.
