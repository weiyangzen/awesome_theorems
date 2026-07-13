# Intake validation

Base revision: `67d32ab26aba14b674ae8a1b919e6935812190c3`; base tree:
`8a1d264cf3331992fbbc3a4fffca285af0b88929`.

This validation covers target membership, the planned dossier and open task DAG, repository and
source provenance, exact owned-artifact structure, and one narrow pinned Lean discovery probe. The
probe authenticates the direct mathlib candidate, units form, relevant definitions, `n = 0` and
`n = 1` behavior under coprimality, and a concrete counterexample to the unconditional catalog
formula. It does not freeze a canonical statement, perform the statement mutation suite, audit a
terminal proof body or transitive trust closure, or claim proof credit.

The automation-provided canonical `.lake` symlink was used read-only. No `lake update`, build,
dependency clone/fetch, or `.lake` mutation was performed. Because that symlink and the owned
artifacts are untracked worker inputs, this is nonrelease evidence.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0475` | exit 0; rank 1356, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | exit 0; revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0475/IntakeProbe.lean)` | exit 0; seven pinned declarations printed, three candidate/boundary examples elaborated, unconditional `a=2,n=4` case refuted; stdout SHA-256 `00846585...93fed` |

The final JSON parses, validator compilation, scoped invariant and action-replay check, prohibited
construct scan, and whitespace checks are recorded in `intake-receipt.json`. The candidate's
immediate axiom report is `[propext, Classical.choice, Quot.sound]`; this is a discovery observation,
not an accepted foundation or transitive trust result.

Known downstream failures remain open: preserved pinpoint source theorem/proof and independent
review; the coprimality repair, domains, ordered binders, totient/congruence conventions, degenerate
cases, translations, and errata; canonical Lean expression, minimal imports, fingerprints, checked
transports, and required mutations; discovery and obligation freezes; anchor/proof-body provenance,
composition, readability, hermetic replay, deterministic evidence bundle, independent verification,
and master acceptance. These prevent audit and theorem completion but do not invalidate a truthful
`planned` intake.
