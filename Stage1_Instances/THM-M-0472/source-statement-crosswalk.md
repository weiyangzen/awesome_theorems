# Source-statement crosswalk

## Repository source record

`Docs/researches/math_theorems.md:3469-3474` supplies the title `欧几里得算法`, attributes it to
Euclid around 300 BCE, and states only `求最大公约数的算法`. Git blame attributes all six
uncited catalog lines to repository commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record
contains no bibliography, book/proposition, edition, translation, input domain, gcd definition,
algorithm steps, termination or correctness contract, boundary policy, proof, errata, or formal
artifact.

`Docs/Stage0_Blueprint.md:12947-12972` repeats the gloss while leaving exact definitions and
premises, proof history, dependencies, equivalent forms, axioms, and machine artifacts open. The
rev-5.6 manifest preserves `已验证` only as `source_status_untrusted` and resets the target to
`L0 / rework_required`. These records identify the family but cannot establish `H0` or an exact
Lean proposition.

## Historical source leads

David E. Joyce's online English presentation of *Euclid's Elements*, Book VII, Proposition 2 states
"To find the greatest common measure of two given numbers not relatively prime." Its construction
uses repeated subtraction/remainders, then proves that the terminal remainder is a common measure
and that no greater common measure exists. Proposition 1 handles the relatively-prime branch ending
at a unit. The inspected HTML bytes have SHA-256 values
`c1974e37cfcce18c27840cce2f8270ae9787d1360fe979496d6c25a4c8f3499a` (VII.2) and
`c7dc63ce4fb8244930f9343e9762800b1b88ad23eb4585b151ef3441063b76c7` (VII.1).

These are bounded discovery leads only. They are not preserved as an accepted primary edition;
their translation, incorporated definitions, exact relationship to the catalog's combined modern
name, zero/equal-input coverage, correction history, and mathematical fidelity have not received
independent review. They therefore do not support `H0`.

## Component crosswalk

| Catalog component | Mathematical decision | Prospective Lean component | Intake status |
|---|---|---|---|
| "algorithm" | executable recursion, trace relation, or extensional specification | `Nat.gcd`, an explicit trace/program, or a wrapper | exact root open |
| "find" | termination plus returned output | well-founded definition and `Nat.gcd.induction` | termination contract open |
| "greatest" | every common divisor divides the result | `Nat.dvd_gcd` and `Nat.gcd_eq_iff` | characterization candidate located |
| "common divisor" | result divides both inputs | `Nat.gcd_dvd_left`, `Nat.gcd_dvd_right` | correctness candidates located |
| repeated remainder | gcd invariant for one recursive step | `Nat.gcd_rec m n` | exact recurrence and orientation checked |
| inputs | naturals, positive integers, or signed integers | candidate `m n : Nat` | source/domain choice open |
| zero boundary | stopping rule and `gcd(0,n)` convention | `Nat.gcd_zero_left n` | pinned candidate includes zero |
| `已验证` | untrusted inventory label | no proof object | explicitly rejected as evidence |

## Pinned Lean discovery anchors

At the manifest-pinned Lean toolchain revision, importing only `Init.Data.Nat.Gcd` exposes:

```text
Nat.gcd (m n : Nat) : Nat
Nat.gcd_def (m n : Nat) : gcd m n = if m = 0 then n else gcd (n % m) m
Nat.gcd_rec (m n : Nat) : gcd m n = gcd (n % m) m
Nat.gcd.induction : a well-founded induction principle following the same remainder step
Nat.gcd_dvd_left / Nat.gcd_dvd_right : the result divides each input
Nat.dvd_gcd : every common divisor divides the result
Nat.gcd_eq_iff : gcd m n = g iff g divides both inputs and every common divisor divides g
```

Lean's logical-model source documents `Nat.gcd` as a reference implementation by the Euclidean
algorithm, with arbitrary-precision kernel and compiler overrides for evaluation. `IntakeProbe.lean`
checks the interfaces, prints immediate axiom reports, kernel-checks the recurrence and full
divisibility-characterization wrappers, and checks the zero and `(48,18)` boundaries. Both
`Nat.gcd_rec` and `Nat.gcd_eq_iff` report `propext` and `Quot.sound` in the current environment.

This is real pinned API elaboration evidence for an `M3` candidate, not an `M0` claim. The probe does
not freeze the canonical target, map an accepted source statement, separate logical model from
runtime override assurance, audit terminal provenance or transitive trust, precommit the discovery
inventory, or perform an independent anchor audit. Those tasks remain downstream and open.

## Fidelity boundary

The catalog gloss and historical leads make the Euclidean gcd-algorithm family recognizable, but
they omit proposition-changing scope and representation decisions. Intake therefore preserves
candidate components and their boundaries without pretending that recurrence, termination, full
correctness, or program refinement has already been selected and accepted.
