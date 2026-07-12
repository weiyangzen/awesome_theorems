# Exact-statement gate: blocked

Assigned item: `S56-M-0727-STATEMENT`  
Base revision: `f12b1ccbda307337d488a2993eddbf883b722be6`  
Validation date: 2026-07-12 (Asia/Shanghai)

## First failed gate

The rev-5.6 exact-statement gate cannot be passed truthfully. The complete repository wording for
this target is `交互证明系统` ("interactive proof systems"). This is the name of a model or subject,
not a truth-valued claim. It does not select a definition or theorem and supplies no ordered
binders, hypotheses, or conclusion. In particular, it does not determine the party and message
model, transcript and randomness semantics, input encoding, resource or round bounds, probability
thresholds, or quantified language.

Consequently, there is no exact source proposition to elaborate. The intake authority correctly
keeps `canonical_claim`, `declaration_or_expression`, and `elaborated_expression_hash` null. Creating
a convenient protocol structure, proving a projection from assumed completeness/soundness fields,
or substituting the adjacent `THM-M-0728` theorem `IP = PSPACE` would broaden or replace the target
and is prohibited. Generic mathlib API elaboration is only a capability probe and is not statement
elaboration for `THM-M-0727`.

Retry requires an accountable scope decision backed by independent inspection of an immutable
source edition and a pinpoint proposition (with all referenced definitions, assumptions, and
errata). That decision must fix the protocol, parties, messages, coins, transcript, encodings,
complexity and round bounds, error convention, ordered quantifiers, hypotheses, conclusion, and
boundary cases. Only then can the canonical Lean expression, minimal imports, transports,
environment fingerprint, and mutation tests be produced.

No statement receipt, accepted state, proof credit, audit completion, or theorem completion is
claimed. The root remains `[H5, M4, R4]`. Per the worker contract, no
`.stage1-worker-selftest.json` is emitted because the assigned statement phase is blocked rather
than self-tested to completion.

## Scoped validation evidence

The pinned worker environment was used without `lake update`, `lake build`, dependency network
operations, or mutation of `.lake`. `git status --short` reported only the worker's untracked
`Formalizations/Lean/.lake` reuse surface before this artifact was added; this is nonrelease
evidence.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard structure passed: 15 assurance groups and 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Manifest passed: 1546 unique targets, ranks 1 through 1546, all `L0/rework_required`. |
| `python3 scripts/stage1_target.py show THM-M-0727` | 0 | Confirmed rank 764, planned lifecycle, unaccepted legacy artifacts, and `theorem_complete: false`. |
| repository-source phrase count assertion over `Docs/researches/math_theorems.md` and `Docs/Stage0_Blueprint.md` | 0 | Found exactly the available gloss occurrences: two `陈述: 交互证明系统` records and one `定理内容: 交互证明系统` record; none states a proposition. |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0727/IntakeProbe.lean)` | 0 | Pinned Lean 4.29.0 elaborated the six generic `Language`, deterministic time/polytime, and `PMF` API checks; it did not elaborate a target theorem. |
| scoped JSON assertion for the canonical claim, Lean expression, expression hash, and root vector | 0 | Confirmed all three statement-identity fields are null and the recorded vector is `[H5, M4, R4]`; therefore statement-freeze preconditions are blocked. |
| `! rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0727 -g '*.lean'` | 0 | No prohibited placeholder or axiom occurs in the owned Lean probe. |

