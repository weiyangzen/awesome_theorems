# THM-M-0400 validation-phase evidence

Item: `S56-M-0400-VALIDATION`

## Validated boundary

The proof-phase module and an independent Lean module that does not import it
both elaborate the three elementary height and rational-vector encoding facts.
All six declarations report only `propext`, `Classical.choice`, and
`Quot.sound`. The fail-closed validator binds the statement, proof, validation
probe, frozen obligation tree, proof receipt, toolchain, and Lake manifest by
SHA-256 and confirms the honest open-root state.

This is partial same-workspace validation, not validation of Schmidt's
Subspace Theorem. The proof receipt closes no frozen obligation. The deep
coefficient-field, transport, auxiliary construction, nonvanishing, gap,
subspace extraction, finite-cover, terminal composition, and exact root remain
open. The root vector stays `H1/M3/R3`; audit and theorem completion are false.

## Commands and exact results

Commands ran at base revision
`76065c6d4727c5f002398b7e5310e0e68c872b56` on 2026-07-12
(`2026-07-11T19:46:01Z` UTC).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets and ranks passed |
| `python3 scripts/stage1_target.py show THM-M-0400` | 0 | rank 13, planned, L0/rework-required, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0400/check_obligation_tree.py` | 0 | 13 obligations, 36 typed edges, frozen registry passed |
| `(cd Formalizations/Lean && bash ../../Stage1_Instances/THM-M-0400/check_proof.sh)` | 0 | statement and three proof declarations elaborated with the three recorded axioms |
| `(cd Formalizations/Lean && bash ../../Stage1_Instances/THM-M-0400/check_validation_lean.sh)` | 0 | independently implemented equivalents elaborated with the same axiom profile |
| `python3 Stage1_Instances/THM-M-0400/check_validation.py` | 0 | frozen inputs and open 13-node boundary verified; both Lean recipes replayed |
| prohibited-token scan of the three Lean sources | 1, expected | no `sorry`, `admit`, axiom declaration, or unsafe declaration |
| `git diff --check -- Stage1_Instances/THM-M-0400 .stage1-worker-selftest.json` | 0 | no whitespace errors |

No network access, Lake update/build, dependency clone/fetch, or `.lake`
mutation occurred. The pre-existing pinned `.lake` link supplied a warm cache.
This is not an empty-cache hermetic replay, offline archive replay, or distinct
runner attestation. Those gates and master acceptance remain open.
