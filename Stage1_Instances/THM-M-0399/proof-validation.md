# THM-M-0399 proof-phase validation

Item `S56-M-0399-PROOF`; base revision
`4dabab14860067cbb1220d76c5a1bd9abd87d624`.

The checked declaration `rothStatement_of_strongFinite` implements the frozen
`M0399-ROOT-COMPOSE` obligation: specializing the stronger constant-`C` interface at `C = 1`
produces the exact constant-one `RothStatement`. The proof uses `simpa` only to normalize
`one_mul`; it contains no placeholder or new assumption.

This is not a terminal proof of Roth's theorem. The premise `StrongFiniteStatement` is precisely
the central open Roth finiteness package. The immutable anchor audit found no proof body for that
premise in the pinned dependencies, and implementing Roth's 1955 auxiliary-polynomial, index,
height, and product-formula argument remains substantial `formalization_debt`. Consequently the
root stays `[H1, M4, R4]`, `M0399-ROOT` remains open, and `theorem_complete=false`.

## Validation record

| Command | Result |
|---|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0399/RothComposition.lean` | exit 0; printed `rothStatement_of_strongFinite : StrongFiniteStatement -> RothStatement` |
| `python3 Stage1_Instances/THM-M-0399/check_proof_phase.py` | exit 0; one composition body closed and exact root reported open |
| `python3 Stage1_Instances/THM-M-0399/check_obligation_tree.py` | exit 0; frozen 11-obligation denominator and typed graphs unchanged |
| `python3 -m json.tool Stage1_Instances/THM-M-0399/proof-phase.json` | exit 0 |
| `git diff --check -- Stage1_Instances/THM-M-0399 .stage1-worker-selftest.json` | exit 0; no output |

The narrow Lean replay uses the clone's pinned Lake project and its pre-existing canonical `.lake`
symlink. No update, build, fetch, or dependency mutation was performed. Master acceptance remains
outstanding.
