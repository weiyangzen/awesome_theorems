# Statement phase blocker

Item: `S56-M-0726-STATEMENT`

Base revision: `d19d83e12b57432e75cbb1c35f4577d5b0645cf9`.

## First failed gate

The rev-5.6 exact-statement gate cannot be completed from the repository source. The complete
source wording for this target is `BPP, RP, ZPP等类` ("BPP, RP, ZPP, and other classes"). This is
a topic list, not a truth-valued mathematical statement: it has no ordered binders, hypotheses, or
conclusion. It also does not select a randomized computation model, input encoding and size
measure, random-bit distribution, time convention, error thresholds, or boundary cases.

Consequently there is no exact human claim to map to Lean and no legitimate canonical Lean target
to elaborate. Choosing a familiar inclusion, equality characterization, closure theorem, or a set
of definitions would broaden or substitute the recorded target. The intake correctly records
`canonical_claim: null`, `declaration_or_expression: null`, and root vector `[H5, M4, R4]`.

This phase therefore produces no `Statement.lean`, expression hash, alternate-form transport, or
mutation certificate. The API probe is retained only as evidence that potential deterministic
complexity and discrete-probability ingredients elaborate; it is not presented as the target.

## Validation evidence

Validation ran on 2026-07-12 (Asia/Shanghai) using the existing pinned artifacts. No `lake update`,
build, clone, fetch, or other `.lake` mutation was performed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0726` | exit 0; rank 763, `planned`, legacy artifacts unaccepted, `theorem_complete: false` |
| `rg -n '概率复杂性类\|BPP, RP, ZPP等类' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md` | exit 0; every target occurrence gives only the same topic label/list; Stage0 leaves exact definitions and proof route open |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0726/IntakeProbe.lean)` | exit 0; `Language`, `Turing.TM2OutputsInTime`, `Turing.TM2ComputableInPolyTime`, `PMF`, `PMF.pure`, and `PMF.bind` elaborated under Lean 4.29.0 |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0726 -g '*.lean'` | exit 1 as expected; no prohibited declaration or placeholder was found |

Pinned inputs observed were `leanprover/lean4:v4.29.0` and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`.

## Retry condition and status boundary

Retry only after an accountable source decision selects one immutable, pinpointed proposition and
independent inspection freezes its referenced definitions, randomized machine and randomness
semantics, encoding, time/cost convention, error convention, exact quantifier order, hypotheses,
conclusion, and boundary cases. Then the statement phase must elaborate that exact target with
minimal imports and perform all four rev-5.6 mutation classes before inspecting proof evidence.

Verdict: `blocked`. Lifecycle remains `planned`; root vector remains `[H5, M4, R4]`.
`audit_complete: false`; `theorem_complete: false`. No statement-phase receipt or acceptance is
claimed, and no `.stage1-worker-selftest.json` is emitted.
