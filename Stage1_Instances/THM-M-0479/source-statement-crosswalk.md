# Source-statement crosswalk

## Repository source record

The complete repository record is `Docs/researches/math_theorems.md:3518-3523`. Git history traces
all six uncited lines to commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

| Catalog field | Received value | Intake consequence |
|---|---|---|
| title | `狄利克雷定理` | Identifies Dirichlet's theorem, but the name alone is not a binder-complete proposition. |
| attribution | Peter Dirichlet | Historical metadata only until checked against an immutable source. |
| time | 1837 | Consistent with the classical theorem family; not a theorem locator. |
| statement | `等差数列中存在无穷多素数` | Identifies primes in arithmetic progressions but omits universal quantifiers, admissibility, domains, and definitions. |
| importance | high | Scheduling metadata only. |
| formalization status | `已验证` | Explicitly untrusted; supplies no human-source or kernel credit. |

The generated record at `Docs/Stage0_Blueprint.md:13136-13161` repeats the gloss and explicitly
leaves precise definitions and premises, proof route, equivalent forms, axioms, machine status,
and artifact links pending. It adds no exact source statement.

No immutable primary or authoritative edition, theorem/page locator, incorporated definitions,
assumption map, proof boundary, translation, correction or errata disposition, or independent
review is present in the repository. Accordingly, the provisional human status is `H1`: a famous
proved theorem family is recognizable, but exact source fidelity is not audited. This is not H0.

## Phrase-to-statement map

| Repository phrase | Candidate mathematical component | Prospective Lean component | Intake assessment |
|---|---|---|---|
| `等差数列` / arithmetic progressions | every reduced residue class `a` modulo a positive `q` | `q : Nat`, `[NeZero q]`, `a : ZMod q`, `IsUnit a` | standard modern reading, but the universal binders and reduced-class condition are absent from the gloss |
| implicit admissibility | `gcd(a, q) = 1` | `Nat.Coprime a q`, integer `IsCoprime a q`, or `IsUnit (a : ZMod q)` | mathematically essential for a universal infinitude result; exact encoding remains open |
| `素数` / primes | positive natural prime values in the class | `p : Nat` and `p.Prime` | direct candidate; the source's carrier convention is not documented |
| progression membership | `p` is congruent to `a` modulo `q` | `(p : ZMod q) = a`, `p ≡ a [MOD q]`, or integer modular equality | alternate encodings require checked transport before credit |
| `存在无穷多` / infinitely many exist | the set is infinite, equivalently members exist above every bound | `Set.Infinite {p | ...}` or `forall n, exists p > n, ...` | direct candidate family; canonical form and boundary conventions remain open |
| `已验证` | inherited catalog status | no Lean component | no proof, source, or receipt credit |

The Chinese gloss is compatible with the standard theorem only after adding proposition-changing
material that it leaves implicit. Intake records that interpretation as a candidate family, not an
exact transcription.

## Pinned formal candidate crosswalk

| Module and declaration | Exact candidate role | Intake credit and boundary |
|---|---|---|
| `Mathlib.NumberTheory.LSeries.PrimesInAP` / `Nat.infinite_setOf_prime_and_eq_mod` | For nonzero natural `q` and unit `a : ZMod q`, the set of natural primes reducing to `a` is infinite. | Closest set-infinitude candidate; supports M3 discovery only. No canonical root, source transport, proof-body audit, or M0 credit. |
| same module / `Nat.forall_exists_prime_gt_and_eq_mod` | Above every natural bound there is a prime reducing to a unit `ZMod q` class. | Candidate alternate encoding; no checked target-specific transport at intake. |
| same module / `Nat.forall_exists_prime_gt_and_zmodEq` | Integer representative, nonzero natural modulus, integer coprimality, and integer modular equality. | Candidate integer form; sign and coercion conventions are not source-approved. |
| same module / `Nat.forall_exists_prime_gt_and_modEq` | Natural representative and `Nat.Coprime`, with a prime above every bound satisfying `Nat.ModEq`. | Candidate natural congruence form; no canonical selection at intake. |
| same module / `Nat.infinite_setOf_prime_and_modEq` | Natural modulus and representative, coprimality, and an infinite set defined by `Nat.ModEq`. | Direct set-infinitude alternate; supports discovery only. |

The same mathematical family also appears in the repository's separate `THM-M-0500` dossier.
That is useful discovery evidence but cannot establish source identity for `THM-M-0479`, transfer
accepted state, or substitute for this target's own phase receipts.

## Human-source and machine boundary

Before H0, an independent reviewer must approve one immutable primary or authoritative edition and
pinpoint statement, every incorporated definition and material assumption, the proof boundary, any
translation, correction and errata findings, and the mapping to every formal binder and alternate
encoding. Before any M0 classification, downstream phases must freeze and elaborate the exact Lean
target, audit candidate identity and terminal bodies, freeze obligations and typed graphs, and run
the required composition, placeholder, axiom, provenance, trust, hermetic, and independent gates.

The successful intake probe proves only that the recorded declarations elaborate in the pinned
environment. It neither performs the scheduled exhaustive anchor audit nor claims that the root
theorem is accepted or theorem-complete.
