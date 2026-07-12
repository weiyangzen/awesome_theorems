# Exact-statement gate: blocked

Item: `S56-M-0785-STATEMENT`  
Theorem: `THM-M-0785`  
Base revision: `5314165df54baa70993fddf08cc142a9739a74e0`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the available authoritative material.
The repository gives only the title `决定性公理` (axiom of determinacy), the attribution Jan
Mycielski/Stanisław Świerczkowski, the year 1964, and the gloss `实数集上某些博弈的决定性`
("determinacy of certain games on sets of reals"). It supplies no bibliographic work, immutable
source passage, theorem or definition locator, assumptions, errata, or independently reviewed
transcription.

The missing words are root-defining rather than notational. At least these inequivalent claims fit
the record:

1. full AD, quantifying over every payoff subset of Baire space;
2. determinacy restricted to a named Borel, analytic, projective, or other pointclass;
3. a theorem deriving some consequence from a determinacy hypothesis.

The repository does not fix the move alphabet, play length, information pattern, coding of reals,
player order, strategy convention, payoff owner, or ambient foundation. In particular, full AD is
not interchangeable with Borel determinacy, which is separately represented by `THM-M-0786`, nor
with unrestricted choice. Selecting conventional answers would manufacture or substitute a
theorem. Encoding an opaque `Determined` predicate or assuming the desired determinacy would be a
placeholder. Both are forbidden.

Consequently there is no canonical expression to hash, no meaningful import-minimality claim, no
source-equivalent alternate encoding to transport, and no sound removed-hypothesis, changed-domain,
changed-binder-scope, or boundary mutation test. The exact-source statement gate fails before
proof or anchor evidence may receive credit.

## Lean boundary

The pinned Lean environment is available. `IntakeProbe.lean` elaborates using the single direct
import `Mathlib.Data.Set.Basic`; it defines plays as `Nat -> Nat`, finite-history strategies, and one
full-payoff determinacy candidate. This checks only that one possible schema is expressible. The
intake explicitly did not select that candidate, so re-elaboration is not canonical statement
evidence and provides no theorem or proof credit. The target's Lean source contains no `sorry`,
`admit`, or declared `axiom`.

## Validation record

Commands ran from this worker clone on 2026-07-12 (Asia/Shanghai). The existing canonical `.lake`
artifacts were used read-only. No update, build, clone, fetch, or dependency mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets; ranks 1..1546; all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0785` | 0 | rank 790; planned; legacy artifacts unaccepted; theorem_complete false |
| repository `rg` search for the theorem ID, title, attribution, and gloss | 0 | only the underspecified catalogue/Stage0 wording and a distinct later AD/descriptive-set-theory entry were found |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `651c8a...1d2` and `321626...d81`, recorded in the JSON blocker |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0785/IntakeProbe.lean)` | 0 | all seven candidate-schema checks elaborated; no canonical target asserted |
| `rg -n '\\b(sorry|admit)\\b|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0785 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom found |
| `python3 -m json.tool Stage1_Instances/THM-M-0785/instance.json` | 0 | valid intake JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0785/task-dag.json` | 0 | valid task DAG JSON |

## Retry condition

An accountable reviewer must preserve an immutable authoritative source, record exact locators and
errata, transcribe and independently approve one proposition, and freeze the game, pointclass,
foundation, ordered binders, hypotheses, conclusion, and boundary cases. The statement phase can
then implement the real Lean substrate, minimize imports, serialize and hash the elaborated
expression, check transports, and run all four mutation classes.

This records the first failed gate. The statement node remains `[ ]` at `M4`; the root remains
`[H3, M4, R4]`, with `audit_complete: false` and `theorem_complete: false`. The assigned phase is
not genuinely self-tested, so no `.stage1-worker-selftest.json` is emitted.
