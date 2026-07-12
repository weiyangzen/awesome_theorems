# Exact-statement gate: blocked

Item: `S56-M-0797-STATEMENT`  
Theorem: `THM-M-0797`  
Base revision: `5278269d3ea693eba5c4c533ad3fe61693da0620`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. Its
entire mathematical wording is the title "diamond principle" and the gloss "combinatorial
set-theory principle", with an attribution to Ronald Jensen and the year 1972. Stage0 explicitly
leaves the exact definition, assumptions, equivalent formulations, axioms, proof route, and formal
artifact open. The `verified` label is untrusted metadata and does not identify a proposition.

The label is compatible with inequivalent formal roots, including `Diamond(omega_1)`, generalized
`Diamond(kappa)`, `Diamond(S)` for a selected stationary set, subset-guessing and function-guessing
variants, and a relative theorem about the constructible universe. In particular, the bare diamond
assertion is not interchangeable with a theorem that `L` satisfies diamond or with an implication
from `V = L`. These choices alter the domains, ordered binders, hypotheses, conclusion, and
foundation/model boundary.

Even after choosing a variant, the repository record does not specify the ordinal/cardinal
representation, regularity and uncountability assumptions, club and stationary conventions,
stagewise restriction operation, powerset universe levels, limit and zero stages, or whether
ordinals, subsets, and stationarity are internal or external to a model. Selecting these choices
would invent missing mathematics. Consequently there is no canonical expression to serialize or
hash, no defensible minimal import set, no checked alternate encoding, and no meaningful
removed-hypothesis, changed-domain, binder-scope, or boundary mutation tests. The rev-5.6 section
5.1 statement gate fails before proof evidence may be inspected.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated with pinned Lean 4.29.0. It imports ordinal aleph
and topology support plus order boundedness, then checks the first uncountable ordinal notation,
ordinal initial segments, closedness, ordinal closed-below, and unboundedness. These are nearby API
ingredients only; the probe is not a definition or statement of diamond and receives no statement
or proof credit. A bounded search of pinned mathlib's `Mathlib/SetTheory` tree found no diamond or
stationary-set declaration; its only matching `club` occurrence is an informal TODO comment.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The existing `.lake` artifacts were consumed read
only; no update, build, fetch, or clone was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0797` | 0 | rank 801, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | hashes `651c8a...1d2` and `321626...d81`, recorded in the JSON blocker |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision recorded above |
| repository `rg` search for the theorem ID, title, and gloss | 0 | found only underspecified metadata and open Stage0 fields; no exact proposition |
| pinned-mathlib `rg` search for `diamond`, `stationary`, and `club` | 0 | only an informal `club sets` TODO comment; no theorem-specific API located |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0797/IntakeProbe.lean` | 0 | seven nearby ordinal/order API expressions elaborated; no canonical target asserted |

## Retry condition and status boundary

An accountable source reviewer must preserve and hash an immutable primary or authoritative source,
select and transcribe one exact proposition with all incorporated definitions and assumptions,
dispose of errata, and independently approve the source mapping. The review must freeze the diamond
variant, cardinal or stationary-set parameter, ambient foundation/model, internal versus external
semantics, ordered binders, hypotheses, conclusion, and boundary cases. A later statement run can
then encode that exact claim, minimize imports, fingerprint the elaborated expression, check any
alternate transports, and execute all four required mutation classes.

This statement node remains `[ ]`, with the root unchanged at `[H3, M4, R4]` and
`audit_complete: false`, `theorem_complete: false`. The assigned phase did not pass its completion
gate, so no `.stage1-worker-selftest.json` is emitted.
