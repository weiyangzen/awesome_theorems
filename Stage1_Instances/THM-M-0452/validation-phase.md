# THM-M-0452 validation-phase result

Item: `S56-M-0452-VALIDATION`. Base revision:
`2029732601188918961647a1d1565c7d55a46f04`. Validation time:
`2026-07-12T02:21:12Z`.

The node-scoped validator re-elaborated the frozen statement, conditional
composition, quotient proof, and an exact-type probe in a fresh temporary
directory. The checked quotient declarations report exactly `propext`,
`Classical.choice`, and `Quot.sound`, with no `sorryAx` or forbidden source
token. The pinned mathlib source tree is clean at revision `8a178386ffc0`.

This validates only the real proof-phase deliverable: torsion quotient descent
and positive definiteness on the quotient, conditional on a supplied
`PolarizationCore`. `CanonicalHeightCore` and `PolarizationCore` remain open,
so the exact `NeronTatePairingTarget` is not proved.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets pass |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0452` | 0 | rank 301, planned, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0452/check_statement.py` | 0 | exact statement and four mutations pass |
| `python3 Stage1_Instances/THM-M-0452/check_anchor_audit.py` | 0 | four candidates classified; root remains M3 |
| `python3 Stage1_Instances/THM-M-0452/check_obligation_tree.py` | 0 | 23 obligations, 51 typed edges, root open |
| `python3 Stage1_Instances/THM-M-0452/check_validation.py` | 0 | temporary kernel replay, axiom observation, source hygiene, and pin checks pass |

The validator used existing `lake env lean` resolution only. It created and
removed temporary oleans under `Formalizations/Lean`; it did not update,
build, clone, fetch, or mutate dependencies.

## Gate decisions

| Gate | Decision | Boundary |
|---|---|---|
| Narrow kernel replay | pass | Frozen statement, composition, quotient proof, and exact-type probe elaborate. |
| Trust observation | provisional pass | Observed axioms are the expected three principles; no complete release TCB inventory is inferred. |
| Provenance | partial pass | Local proof hashes and the clean pinned mathlib revision are bound in the receipt; root provenance remains open. |
| Authoritative root state | open | Height and polarization bodies are absent; the frozen graph also awaits master reconciliation of the partial quotient proof. |
| Hermetic release | fail closed | The run reused a shared warm cache; no clean empty-cache offline replay, SBOM/license closure, or deterministic bundle exists. |
| Independent verification | fail closed | The exact-type probe imports the proof and ran in the same checkout/cache; there is no independent implementation, identity, runner, or signature. |

`audit_complete=false` and `theorem_complete=false`. This is provisional worker
validation of the available partial proof, not `E0/E1`, release, or master
acceptance.
