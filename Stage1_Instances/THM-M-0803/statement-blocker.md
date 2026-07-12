# Exact-statement gate: blocked

Item: `S56-M-0803-STATEMENT`  
Theorem: `THM-M-0803`  
Base revision: `8f8873f36acbc62e9b41b932a8bb65bf355c8ccf`

## Decision

The authoritative repository wording is only `内模型理论` ("inner model theory") with the gloss
`可构成宇宙的内模型` ("an inner model of the constructible universe"). This identifies a topic or
object, not a proposition. Stage0 explicitly leaves the exact definitions, assumptions, proof,
logical foundation, and target formal system open. No source edition, theorem number, page,
hypotheses, ordered binders, conclusion, or boundary cases are supplied.

Several inequivalent targets remain compatible with that metadata: that the constructible universe
`L` is an inner model of ZF or ZFC; a fine-structure or condensation theorem for levels of `L`; a
version of Jensen's covering lemma, with assumptions involving `0#`; or another existence/property
result about an inner model. Even the direction of the Chinese genitive is insufficient to decide
whether `L` is the proposed inner model or an inner model *of* `L`. Choosing any one of these would
silently substitute mathematics for the source record. The adjacent `V = L` and core-model entries
cannot resolve the ambiguity and are explicitly separate targets.

Consequently there is no canonical human proposition from which to derive an exact Lean expression,
minimal imports, a serialized expression hash, checked transports, or meaningful removed-hypothesis,
changed-domain, binder-scope, and boundary mutations. The exact-statement gate fails before proof or
anchor evidence may receive credit.

## Pinned Lean boundary

The existing `IntakeProbe.lean` imports `Mathlib.SetTheory.ZFC.Class` and
`Mathlib.SetTheory.ZFC.Ordinal`. It re-elaborates six type-level ZFC set/class, transitivity, ordinal,
and rank APIs. Those declarations are encoding ingredients only: they neither define the
constructible universe nor state that a selected class is an inner model of a selected object
theory. A bounded name search found no constructible-universe, inner-model, fine-structure, covering,
or `0#` declaration in pinned mathlib's set/model-theory sources. The probe is not a canonical target
and receives no statement or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. Existing canonical `.lake` artifacts were used read
only; no dependency update, build, clone, or fetch was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0803` | 0 | rank 806; planned; legacy artifacts unaccepted; theorem incomplete |
| `rg -n '内模型理论\|可构成宇宙的内模型' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md` | 0 | only the ambiguous label/gloss and explicitly open Stage0 fields were found |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | hashes `651c8a...1d2` and `321626...d81`, recorded in the JSON blocker |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision recorded above |
| bounded `rg` search in pinned mathlib set/model-theory Lean sources | 1 | expected no-match exit; no name-specific constructible-universe or inner-model API found |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0803/IntakeProbe.lean` | 0 | all six substrate API checks elaborated; no canonical theorem asserted |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0803 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom found |

## Retry condition and status boundary

An accountable reviewer must preserve and hash an immutable primary source, select and transcribe
one exact proposition with all incorporated definitions and assumptions, audit its attribution and
errata, resolve the translation direction, and independently approve the source crosswalk. A later
statement run can then encode that exact claim, minimize pinned imports, fingerprint the elaborated
expression, check transports, and execute all required mutation classes.

This node remains blocked at `M4`; the root remains `[H3, M4, R4]` with `audit_complete: false` and
`theorem_complete: false`. The assigned phase is not genuinely self-tested, so no
`.stage1-worker-selftest.json` is emitted.
