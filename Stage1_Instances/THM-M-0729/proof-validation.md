# THM-M-0729 proof-phase blocker

Item: `S56-M-0729-PROOF`  
Date: `2026-07-12`  
Base revision: `c72bad9e8827ffb1ba1a585dbe346c88393b4a3f`

## Verdict

`blocked`: no eligible proof body for the exact binary PCP target exists in the
repository or pinned mathlib closure. The checked theorem
`root_of_directionalPackage` is conditional composition: its premise already
contains both `InNP -> InPCPLogConst` and `InPCPLogConst -> InNP` for every
binary language. No declaration constructs that package.

The first failed proof gate is terminal proof-body availability for
`M0729-D-NP-PCP`; the root cut also contains `M0729-D-PCP-NP`. The forward
direction requires formalizing the frozen constraint normalization, robust gap
theorem, PCP composition, logarithmic randomness and constant-query accounting,
perfect completeness, and exact soundness-half transport. The reverse direction
requires finite proof-bit certificates, exhaustive random-string verification
with a polynomial cost proof, and the finite below-threshold branch.

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`
contains supporting deterministic Turing-machine, finite-cardinality,
polynomial, and logarithm APIs, but no NP/PCP class or PCP-theorem body. The
prerequisite immutable anchor audit found no eligible external Lean 4 terminal
proof to pin. No premise, axiom, placeholder, weaker inclusion, adaptive model,
or altered resource/soundness statement was added.

Because the assigned proof phase is not self-tested complete, this attempt
deliberately does not create `.stage1-worker-selftest.json`.

## Narrow validation evidence

All commands ran in the worker clone. `Formalizations/Lean/.lake` is a symlink
to the canonical pinned artifacts and was not modified. No update, build,
clone, fetch, or other dependency mutation was run.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard passes: 15 assurance groups and 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0729` | 0 | Rank 766, lifecycle `planned`, L0/rework-required, theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0729/check_statement.py` | 0 | Exact expression hash `2a3d6c...7bbc5`; four weakened mutations were distinguished against pinned mathlib. |
| `python3 Stage1_Instances/THM-M-0729/check_obligation_tree.py` | 0 | 19 obligations and 76 typed edges pass; denominator `66be2951...a2e854`; both directional packages remain open M3. |
| pinned `LEAN_BIN`/`LEAN_PATH`; compile a temporary owned `Statement.olean`, elaborate `ObligationTree.lean`, then remove the olean | 0 | Exact statement and conditional composition elaborate; `#print axioms` reports only `propext`, `Classical.choice`, and `Quot.sound`. |
| `rg -n -i 'PCPTheorem\|probabilistically checkable\|InPCP\|proof oracle\|PCP theorem' --glob '*.lean' Stage1_Instances/THM-M-0729 Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 0 | Hits are confined to this dossier; no terminal PCP proof body was found. |
| `python3 -m json.tool Stage1_Instances/THM-M-0729/proof-blocker.json` | 0 | Blocker record is valid JSON. |
| `rg -n '^\\s*(sorry\|admit\|axiom)(\\s\|$)\|sorryAx' Stage1_Instances/THM-M-0729 --glob '*.lean'` | 1 | No prohibited Lean token; exit 1 means no match. |
| `git diff --check -- Stage1_Instances/THM-M-0729` | 0 | No whitespace errors. |

Machine status remains M3, theorem completion remains false, and the proof node
must remain open pending a real implementation or eligible pinned proof body.
