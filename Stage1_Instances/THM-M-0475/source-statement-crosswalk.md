# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:3490-3495` supplies only the title `Euler theorem`, Leonhard Euler,
1763, the formula `a^phi(n) congruent to 1 (mod n)`, importance `high`, and status `verified`. All
six lines originate at repository commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has
no bibliography, domains, binders, coprimality premise, definitions, proof, correction history, or
formal artifact.

`Docs/Stage0_Blueprint.md:13028-13053` repeats those fields while explicitly leaving the precise
definitions and premises, proof history, dependencies, equivalent forms, axioms, and machine
artifacts open. Its generic theorem-tree language is planning metadata. The rev-5.6 manifest keeps
`verified` only as `source_status_untrusted` and resets the target to `L0 / rework_required`.

## Component crosswalk

| Catalog component | Conventional mathematical completion | Pinned Lean candidate | Intake disposition |
|---|---|---|---|
| `a` | integer or natural representative of a residue class | implicit `{x : Nat}` | domain and binder are absent from the catalog |
| `n` | modulus, often positive or greater than one | implicit `{n : Nat}` | domain and degenerate conventions are absent |
| missing premise | `gcd(a,n)=1`, equivalently that the residue is a unit | `h : Nat.Coprime x n` | indispensable; the unconditional reading is false |
| `phi(n)` | number of residue classes modulo `n` coprime to `n` | `Nat.totient n`, naturals below `n` coprime to `n` | direct candidate convention; source confirmation open |
| congruence | equality modulo `n` | `Nat.ModEq n (x ^ Nat.totient n) 1` | closest syntactic candidate; source/domain mapping open |
| `verified` | untrusted catalog metadata | kernel and source receipts would be required | supplies no H or M credit |

The omitted coprimality premise changes truth, rather than merely presentation. The checked
counterexample `a = 2`, `n = 4` prevents the candidate theorem from being mistaken for the literal
catalog formula.

## Historical source lead

The University of the Pacific Euler Archive landing page for Euler Archive item E271 identifies
Leonhard Euler, *Theoremata arithmetica nova methodo demonstrata*, *Novi Commentarii academiae
scientiarum Petropolitanae*, pages 74-104, publication year 1763, and exposes a scan link. The
landing-page bytes inspected during intake have SHA-256
`eb19d2ada21b7d7fb890cf4d7adab0e74e401a922e4cd7132fa0881dc8e267a7`.

This is a bibliographic lead only. The scan could not be retrieved within the bounded intake run,
so no theorem text, page-specific premise, proof boundary, translation, later correction, or erratum
was inspected. The landing page corroborates the catalog attribution and year but does not establish
the exact proposition and cannot support H0.

## Pinned Lean discovery anchor

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.FieldTheory.Finite.Basic` contains:

```text
Nat.ModEq.pow_totient {x n : Nat} (h : Nat.Coprime x n) :
  x ^ Nat.totient n congruent to 1 modulo n
```

The same module contains `ZMod.pow_totient`, whose base is a unit of `ZMod n`. The library comments
call both declarations the Fermat-Euler totient theorem and describe them as alternate statements.
`Mathlib.NumberTheory.PowModTotient` contains remainder and exponent-reduction consequences, some
with an explicit `1 < n` premise.

`IntakeProbe.lean` imports only the direct declaring module, checks both declarations and the
relevant definitions, elaborates the conventional natural candidate and both degenerate cases, and
prints the candidate's immediate axiom report. That authenticates usable pinned statement
infrastructure and supports only an `M3` intake classification. It does not freeze the canonical
target, inspect terminal proof provenance or transitive trust, perform an external search, or grant
`M0-W` credit.

## Statement-phase retry condition

An accountable source review must preserve an immutable source edition, locate the exact theorem
and proof, map the base/modulus domains and coprimality premise, decide the `n = 0`, `n = 1`, and
positive-modulus conventions, record translations and errata, and obtain independent approval.
Only then may the statement phase freeze the canonical mathematical claim and Lean expression,
minimal imports, checked alternate transports, expression/environment fingerprints, and required
mutations.
