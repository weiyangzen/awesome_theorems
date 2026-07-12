# Statement validation record

Item: `S56-M-0526-STATEMENT`  
Base revision: `9a468f5e9a1a136bac76eb92f1c16ea75bfbb5d5`

## Frozen target

`Stage1Instances.THM_M_0526.SeifertVanKampenTarget` elaborates the intake-selected classical based
two-open-set claim. Sets `U` and `V` are open, cover `X`, contain `x0`, and are path-connected along
with their intersection. The conclusion names the four inclusion-induced fundamental-group maps,
asserts square commutativity, and states the existence and uniqueness clause for every compatible
pair of homomorphisms into a same-universe group. This is the pushout universal property, rather
than a bare isomorphism or generation claim.

The sole direct import is
`Mathlib.AlgebraicTopology.FundamentalGroupoid.FundamentalGroup`. The formal source defines only
transparent inclusion maps and the target predicate; it contains no proof of van Kampen.

## Commands and results

Commands ran in this worker clone. Lean commands ran from `Formalizations/Lean` against the existing
pinned Lake environment; `.lake` was not changed or fetched.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0526/Statement.lean` | 0 | target, inclusion maps, four mutations, and common-basepoint boundary elaborated; explicit target printed |
| `python3 ../../Stage1_Instances/THM-M-0526/check_statement.py` | 0 | expression SHA-256 `a7550267adfd8bc8d37de8174319c6389cb1bbab62b740595a9c91d831567d45`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-0526/Statement.lean lean-toolchain lake-manifest.json` | 0 | `862db0...7d28`, `651c8a...1d2`, and `321626...d81` |

## Boundary and status

The mutation validator separately elaborates and rejects as expression-identical: removal of the
open-cover premises, removal of intersection path-connectedness, weakening to generation by the
two ambient images, and substitution of an arbitrary commutative square. The checked
`intersection_nonempty` lemma records that the chosen common basepoint excludes the empty
intersection boundary. Coincident cover members and members equal to the whole space remain in
scope, as the classical claim requires.

This is statement-only evidence pending master acceptance. Primary-source fidelity remains at the
intake classification, and no theorem proof or downstream-node evidence is claimed.
