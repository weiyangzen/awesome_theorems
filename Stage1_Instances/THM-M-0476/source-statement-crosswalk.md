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

| Catalog component | Conventional interpretation | Pinned Lean surface | Statement status |
|---|---|---|---|
| `p` | natural modulus | `p : Nat`; modular values in `ZMod p` | conventionally selected and elaborated; absent from literal catalog |
| hidden premise | `p` is prime | explicit `hp : p.Prime` | conventionally selected and elaborated; primary-source approval open |
| `p - 1` | natural predecessor under primality | `Nat` subtraction | frozen; truncation is harmless under the explicit prime premise |
| factorial | product `1 * ... * (p - 1)` | `Nat.factorial (p - 1)`, cast into `ZMod p` | frozen exact statement encoding |
| congruent modulo `p` | equality of residue classes | `((p - 1)! : ZMod p) = -1` | frozen exact statement encoding |
| `-1` | additive inverse of the unit residue | `(-1 : ZMod p)` | frozen; natural-residue and divisibility transports remain uncredited |
| displayed direction | prime implies factorial congruence | `Stage1Instances.THM_M_0476.WilsonTheoremTarget` | frozen forward target; converse/iff not substituted |
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

`Statement.lean` deliberately does not import this proof-bearing module. It uses only
`Mathlib.Data.Nat.Factorial.Basic`, `Mathlib.Data.Nat.Prime.Defs`, and
`Mathlib.Data.ZMod.Defs`, freezes the explicit-prime root, and checks an `Iff` transport to the
`[Fact p.Prime]` binder form. The successful elaboration establishes statement/interface evidence
at `M3`; it does not audit or invoke the Wilson proof body and confers no `M0-W` credit.

## Remaining source and downstream gates

The formal statement selection is now explicit and machine-tested, but no primary or authoritative
human source passage has been admitted. An independent source review must still approve the forward
prime-modulus claim and every material domain, hypothesis, notation, direction, and boundary row;
until then the source status remains `H1`. Formal candidate provenance/trust audit, obligation
freeze, proof, readable reconstruction, hermetic validation, and release remain downstream.
