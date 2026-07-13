# Source-statement crosswalk

## Repository source record

`Docs/researches/math_theorems.md:3497-3502` supplies the title `威尔逊定理`, the attribution John
Wilson, the year 1770, and the formula `(p-1)! congruent to -1 (mod p)`. Git blame attributes all
six uncited catalog lines to repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record gives no bibliography, edition,
theorem/page, quantified domain, prime premise, definition of congruence, proof passage, correction
history, errata, or reviewer.

`Docs/Stage0_Blueprint.md:13055-13080` repeats the formula while explicitly leaving exact
definitions and premises, proof history, equivalent statements, axiom use, machine status, and
artifact links open. The rev-5.6 manifest retains `已验证` only as `source_status_untrusted` and
resets the target to `L0 / rework_required`. These records locate the intended theorem family but
cannot establish `H0`.

No primary historical edition or independently reviewed modern authoritative statement was
admitted during intake. The John Wilson/1770 attribution is therefore retained exactly as untrusted
catalog metadata, not asserted as audited genealogy. A future source audit must pinpoint the
historical formulation and proof, reconcile attribution and date, map every incorporated
definition and assumption, inspect corrections or errata, and obtain independent review.

## Clause crosswalk

| Catalog component | Conventional interpretation | Pinned Lean surface | Intake status |
|---|---|---|---|
| `p` | natural modulus | `p : Nat`; modular values in `ZMod p` | domain absent from catalog; candidate only |
| hidden premise | `p` is prime | explicit `hp : p.Prime`; candidate uses `[Fact p.Prime]` | indispensable premise to be source-approved and wrapped |
| `p - 1` | natural predecessor under primality | `Nat` subtraction; primality gives `1 <= p` | truncation harmless under candidate premise; boundary audit open |
| factorial | product `1 * ... * (p - 1)` | `Nat.factorial (p - 1)`, cast into `ZMod p` | direct notation match; cast and product normalization open |
| congruent modulo `p` | equality of residue classes | `((p - 1)! : ZMod p) = -1` | direct candidate encoding, not yet canonical |
| `-1` | additive inverse of the unit residue | `(-1 : ZMod p)` | natural-residue and divisibility transports remain uncredited |
| displayed direction | prime implies factorial congruence | `ZMod.wilsons_lemma` after explicit-hypothesis wrapper | direct pinned formal lead only |
| classical iff | factorial congruence characterizes primes, excluding `1` | `Nat.prime_iff_fac_equiv_neg_one` | stronger related theorem; explicitly not substituted |
| `已验证` | untrusted inventory label | no expression, source review, or receipt | rejected as evidence |

## Pinned Lean leads

At manifest-pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.NumberTheory.Wilson` contains:

```text
ZMod.wilsons_lemma (p : Nat) [Fact p.Prime] :
  ((p - 1)! : ZMod p) = -1

Nat.prime_iff_fac_equiv_neg_one {n : Nat} (h : n != 1) :
  n.Prime <-> ((n - 1)! : ZMod n) = -1
```

The same module contains `ZMod.prod_Ico_one_prime` and
`Nat.prime_of_fac_equiv_neg_one`. Its source route rewrites the factorial as the product of the
nonzero residues, identifies those residues with the units of `ZMod p`, and applies the product of
all units. That architecture is a downstream proof-tree lead, not an intake obligation registry.

`IntakeProbe.lean` imports the proof-bearing module, checks the named declarations, installs
`Fact p.Prime` from an explicit hypothesis in a candidate wrapper, reports candidate axioms, and
checks representative boundary behavior. The successful probe establishes usable exact-topic
interfaces, so the provisional machine level is `M3`; it does not freeze the root, audit the
terminal body or transitive dependency closure, or confer `M0-W` proof credit.

## First downstream gate

Before statement acceptance, an independent source review must approve the forward prime-modulus
claim and every material domain, binder, hypothesis, notation, direction, and boundary row. The
statement phase must then elaborate and fingerprint one exact expression using declared minimal
imports, check the explicit-hypothesis/typeclass and alternate-encoding transports, and reject the
required removed-hypothesis, changed-domain, changed-scope, and boundary mutations.
