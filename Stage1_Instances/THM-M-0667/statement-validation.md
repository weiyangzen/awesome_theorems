# Statement validation record

Item: `S56-M-0667-STATEMENT`  
Base revision: `3bbec7282e62d6123372fda54f8eb18cd839d643`

## Frozen target

`Stage1Instances.THM_M_0667.AckermannNondefinabilityTarget` is exactly
`not (Primrec2 Nat.ack)`. The sole direct import is
`Mathlib.Computability.Ackermann`, which supplies both the selected function
normalization and mathlib's binary primitive-recursive predicate. Checked iff
theorems connect the root to the uncurried `Primrec` representation and the
paired unary `Nat.Primrec (Nat.unpaired ack)` representation.

The three defining equations are kernel-checked as boundary witnesses. The
statement checker distinguishes mutations that retain only the diagonal,
change the function class to general computability, swap the ordered
arguments, or remove negation.

## Commands and results

Commands ran inside this worker clone on 2026-07-12. Lean commands ran from
`Formalizations/Lean` with the existing pinned artifacts. No update, build,
fetch, clone, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0667/Statement.lean` | 0 | exact target, two transports, four mutations, and three defining equations elaborated; explicit target printed |
| `python3 ../../Stage1_Instances/THM-M-0667/check_statement.py` | 0 | expression SHA-256 `5e34e0af...15e7ab`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-0667/Statement.lean lean-toolchain lake-manifest.json` | 0 | `b0860262...3652`, `651c8acc...b1d2`, and `321626c8...2d81` |

This is statement-only evidence pending master acceptance. Although the pinned
import visibly contains a theorem with the same mathematical conclusion, its
candidate equivalence, proof body, dependency closure, trust, and provenance
belong to later nodes and receive no proof credit from this statement phase.
