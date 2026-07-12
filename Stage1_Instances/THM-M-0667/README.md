# THM-M-0667 rev-5.6 intake

This directory is the `planned` rev-5.6 instance for "Ackermann function
non-definability" (`阿克曼函数不可定义性`). It starts from
`L0 / rework_required`; the repository's historical `已验证` label is discovery
metadata and supplies no source or proof credit. `Statement.lean` now freezes
and elaborates the exact target `not (Primrec2 Nat.ack)` using only
`Mathlib.Computability.Ackermann`. Checked transports connect it to the
uncurried and paired-unary encodings, while the three displayed equations are
kernel-checked boundary witnesses.

## Frozen claim

The canonical mathematical claim is that the standard two-variable
Ackermann-Peter function `A : Nat -> Nat -> Nat` is not primitive recursive.
Here `A` is determined by

```text
A(0, n) = n + 1
A(m + 1, 0) = A(m, 1)
A(m + 1, n + 1) = A(m, A(m + 1, n)).
```

"Not definable" is therefore read narrowly as non-representability in the
class generated from zero, successor, and projections by composition and
primitive recursion. It does not mean first-order undefinability in an
unspecified structure.

## Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Function | The displayed two-variable Ackermann-Peter normalization on natural numbers | Ackermann's original multi-variable normalization needs an explicit transport before it can receive credit |
| Function class | Primitive recursive functions `Nat^2 -> Nat` under a future pinned Lean encoding | General recursive, partial recursive, computable, and complexity classes are distinct boundaries |
| Root conclusion | No primitive-recursive binary function is extensionally equal to `A` | Fast growth alone is not the root statement unless connected by a checked domination argument |
| Expected route | Enumerate or structurally bound primitive-recursive functions and show that a suitable Ackermann level eventually dominates each one | The domination theorem, diagonal argument, and encoding transports remain open obligations |
| Natural-number boundary | Zero arguments and both recursive boundary equations are included | No positivity restriction or truncated domain may weaken the claim |
| Formal surface | Lean 4 plus the repository's pinned mathlib environment | No declaration, expression fingerprint, or machine closure is claimed at intake |

## Open phase DAG

1. `S56-M-0667-STATEMENT`: select the primitive-recursive-function encoding,
   define the displayed normalization, and elaborate the exact Lean target.
2. `S56-M-0667-ANCHOR_AUDIT`: audit pinpoint primary sources, pinned mathlib,
   and immutable external Lean 4 candidates.
3. `S56-M-0667-OBLIGATION_TREE`: freeze the domination, diagonal, transport,
   provenance, and trust obligations before assigning proof credit.
4. `S56-M-0667-PROOF`: implement or pin/import exact proof bodies without
   weakening the function, domain, or function class.
5. `S56-M-0667-VALIDATION`: run kernel, trust, provenance, and independent
   validation gates.
6. `S56-M-0667-RELEASE`: reconcile the evidence and obtain master acceptance.

## Status boundary

The provisional root vector remains `[H1, M3, R3]`: the historical result and
primary-source family are identified, but the edition/theorem/premise mapping
has not been independently audited; the exact Lean expression is now locally
elaborated, while candidate proof equivalence, terminal-body provenance, and
closure have not passed their later gates; and no reviewed readable proof
reconstruction exists. This statement phase does not claim `H0`, an `M0`
class, proof credit, audit completion, theorem completion, or master
acceptance.
