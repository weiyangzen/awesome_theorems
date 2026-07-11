# THM-M-0405 statement receipt

## Frozen target

The normalized target is Bilu-Hanrot-Voutier's primitive-divisor theorem:
every Lucas number and every Lehmer number with index `n > 30` has a primitive
prime divisor. `Statement.lean` freezes both branches as one conjunction.

The carrier uses complex roots `alpha` and `beta`, together with integer
invariants and equations that enforce the source Lucas/Lehmer pair conditions.
The stored integer sequences are constrained by the source quotient identities.
A primitive Lucas divisor is required not to divide the discriminant or any
earlier positive term. A primitive Lehmer divisor is required not to divide
`(alpha^2 - beta^2)^2` or any earlier positive term. The ratio is explicitly
required not to be a root of unity.

This is a statement artifact only. It contains no theorem declaration, proof,
`sorry`, axiom, or claimed proof closure. Primary-source theorem numbering and
the later H-status audit remain outside this phase.

## Minimal import check

`Mathlib.Data.Complex.Basic` supplies the carrier, coercions, and elementary
power operations. `Mathlib.Data.Nat.Prime.Basic` is separately necessary for
`Nat.Prime`; a probe with only the complex import failed with `Unknown constant
Nat.Prime`. No broad `Mathlib` import or legacy Stage1 module is used.

## Validation

Base revision: `900ed1fb51c92dde0f0024262cddfa5fc7ae64b7`.

Commands were run in this worker clone on 2026-07-12. The Lean command was run
from `Formalizations/Lean`, using the existing pinned Lake environment.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0405/Statement.lean` | 0 | Printed `Stage1.THM_M_0405.Statement : Prop`; exact file elaborated. |
| `lake env lean /tmp/min.lean` with only `import Mathlib.Data.Complex.Basic` and `#check Nat.Prime` | 1 | Expected minimality probe: `Unknown constant Nat.Prime`. |
| `python3 -m json.tool Stage1_Instances/THM-M-0405/statement.json` | 0 | Structured statement record parses. |
| `git diff --check -- Stage1_Instances/THM-M-0405` | 0 | No whitespace errors. |

Status boundary: `S56-M-0405-STATEMENT` is self-tested worker evidence pending
master acceptance. Anchor audit, proof construction, theorem validation, and
theorem completion are not claimed.
