# THM-M-0721 proof-phase blocker

Item: `S56-M-0721-PROOF`  
Base revision: `2fdf663d8ec0210ce6ee8ba8c84221603b58d1dd`  
Assessment date: `2026-07-12` (`Asia/Shanghai`)

## Verdict

The proof phase is blocked and is not self-tested as complete. No proof body for
`Stage1Instances.THM_M_0721.ExistsNPCompleteLanguage` is available in the pinned dependency closure,
and the frozen obligation tree leaves both root children open:

- `M0721-T-SAT-IN-NP`: construct a concrete encoded SAT language, its verifier, correctness proof,
  certificate bound, and `TM2ComputableInPolyTime` witness;
- `M0721-T-UNIVERSAL-HARDNESS`: construct the Cook-Levin reduction for every frozen `InNP` source,
  prove both membership directions, and supply a `TM2ComputableInPolyTime` witness.

`ObligationTree.lean` proves only the exact child-to-root composition theorem. Its membership and
hardness arguments are hypotheses, so using it as root closure would substitute a conditional
theorem for the assigned existential theorem. The only local mathlib implementation of the frozen
TM2 polynomial-time interface supplies identity. Its composition declaration is `proof_wanted`, so
even the basic polynomial-time composition infrastructure cannot receive proof credit.

The immutable anchor audit also rejects all three external Cook-Levin candidates: one has no NP
endpoint, and the two headline endpoints contain root-relevant proof gaps and lack a checked
transport to this binary-word TM2 formulation. Fetching a moving dependency is forbidden and would
not resolve those mathematical and contract gaps.

Accordingly, no Lean source or structured proof state was changed, no
`.stage1-worker-selftest.json` was written, and this item must remain open. The first failed gate is
exact root kernel closure without placeholders. The remaining root cut set is
`M0721-T-SAT-IN-NP` and `M0721-T-UNIVERSAL-HARDNESS`.

## Narrow validation

No dependency operation or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0721` | 0 | rank 578, planned, L0/rework-required, theorem incomplete |
| concatenate `Statement.lean` and `ObligationTree.lean` into a temporary file, then run `cd Formalizations/Lean && lake env lean <temporary-file>` | 0 | the exact statement and conditional composition elaborated; `#print axioms` reported `[propext, Quot.sound]` |
| `rg -n 'proof_wanted\|sorryAx\|sorry\|admit\|axiom\|unsafe' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Computability/TuringMachine/Computable.lean` | 0 | the sole hit was line 284, `proof_wanted TM2ComputableInPolyTime.comp` |
| `sha256sum Stage1_Instances/THM-M-0721/Statement.lean Stage1_Instances/THM-M-0721/ObligationTree.lean Stage1_Instances/THM-M-0721/obligation-registry.json` | 0 | `6761ca31...2374bd`, `59484c43...6a10a`, `4d4243a5...a8f2` |

The successful Lean command validates only the already frozen conditional composition interface.
It is evidence for the blocker boundary, not evidence that the proof phase or theorem is complete.
