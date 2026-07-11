# THM-M-0133 anchor-audit validation

Item: `S56-M-0133-ANCHOR_AUDIT`  
Date: 2026-07-12  
Base revision: `16629827a8c07768fa69682fa6c8abee2a716543`

## Decision

The immutable mathlib and `flt-regular` candidates elaborate in the existing
pinned Lake environment. Mathlib supplies the exact root definition, a
conditional odd-prime recomposition theorem, exponents 3 and 4, and an adjacent
polynomial variant. The pinned external package supplies the regular-prime
family. None closes every odd prime exponent.

The exact-root candidate in `ImperialCollegeLondon/FLT` was audited at immutable
revision `8884a744090a0e7f5a6ba0fa7ba1019403f3ca78`. Its `FLT.Proof.flt` terminates
through `B1_proof`, `B2_proof`, and `B3_proof` at `B4_proof`, whose body contains
a proof gap. It uses Lean `v4.32.0-rc1` and mathlib revision
`0098dd94d810711e831b250902687d3edab9969b`, neither of which is in this worker's
pinned closure. It is classified `M5`; no dependency was fetched or mutated.

Thus the frozen root remains `M2`, not kernel closed. The remaining cut set is
the unconditional all-odd-prime exponent closure through the Wiles/Taylor-Wiles
and Frey/Ribet chain. This is an anchor-audit receipt pending master acceptance,
not proof, audit-completion, or theorem-completion evidence.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0133/AnchorAudit.lean` from `Formalizations/Lean` | 0 | all six candidate declarations elaborated; the five proof declarations reported only `propext`, `Classical.choice`, and `Quot.sound` |
| `python3 Stage1_Instances/THM-M-0133/check_anchor_audit.py` | 0 | local revisions and clean worktrees matched; local source declarations matched; immutable Imperial root chain and terminal proof gap matched; root remained `M2` |
| `python3 -m json.tool Stage1_Instances/THM-M-0133/anchor-audit.json` | 0 | structured audit ledger is valid JSON |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0133` | 0 | rank 22, planned, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0133` | 0 | no whitespace errors |

The external verifier deliberately searches the immutable source for the exact
gap token, so a generic forbidden-token scan would match that quoted evidence.
No Lean declaration or local proof body introduces a gap, assumption, or
substitute theorem.
