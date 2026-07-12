# Exact-statement gate: blocked

Item: `S56-M-1406-STATEMENT`

Theorem: `THM-M-1406`

Base revision: `5ac2d33ee4b1a16fd90dca63313cd900ffc4bb50`

Base tree: `59b19df4105f58fc10c3e924c32320a284145b7c`

## Decision

The exact Lean 4 target cannot be truthfully frozen or elaborated from the authoritative repository
record. Its complete mathematical wording is the title `Kolmogorov-Sinai entropy`, the attribution
Kolmogorov/Sinai, the year 1958, and the phrase `entropy of a dynamical system`
(`动力系统的熵`). This names an invariant or topic, not a truth-valued proposition with ordered
binders, hypotheses, and a conclusion. Stage0 explicitly leaves the exact definitions, premises,
proof path, axioms, and formal artifact open, and rev-5.6 treats the catalog status `已验证` as
untrusted metadata.

The existing intake consequently leaves `canonical_statement`, the Lean module and expression,
the elaborated-expression hash, and the environment-expression fingerprint null. Its provisional
worker intake receipt has `accepted: false`, and the blueprint still renders that dependency `[_]`.
Its immutable 1958 Kolmogorov scan and fixed Scholarpedia revision are discovery records, not an
independently accepted selection and crosswalk of one exact root. Several inequivalent readings
remain compatible with the catalog phrase:

- a modern definition of system entropy as a supremum over partition entropy rates;
- existence of the normalized finite-partition entropy-rate limit;
- well-definedness or measure-theoretic isomorphism invariance of the invariant;
- an iterate or flow-time scaling law;
- agreement between a selected historical formulation and a modern one; or
- a computation theorem, including one that could overlap the separately scheduled Sinai generator
  theorem.

These readings require different measure-space, transformation, partition, iteration, null-set,
limit, codomain, logarithm, normalization, and boundary conventions. The catalog separately
schedules measure-theoretic entropy (`THM-M-1404`) and the Sinai generator theorem (`THM-M-1405`).
Selecting a familiar definition or theorem here would therefore invent, broaden, duplicate, or
substitute mathematics rather than elaborate the exact received target.

Section 5.1 of the rev-5.6 blueprint fails at exact source-statement identity. There is no canonical
target for which direct imports can be minimized or an elaborated expression can be serialized.
Checked alternate transports and the required removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations are undefined rather than failed tests. Machine
state remains `M4`; no statement or theorem completion is claimed.

## Pinned Lean boundary

The existing discovery-only `IntakeProbe.lean` imports
`Mathlib.Analysis.SpecialFunctions.Log.NegMulLog`,
`Mathlib.Dynamics.Ergodic.Ergodic`,
`Mathlib.MeasureTheory.MeasurableSpace.MeasurablyGenerated`, and
`Mathlib.MeasureTheory.Measure.PreVariation`. Under the pinned environment it elaborates
`MeasurePreserving`, its natural-number iterate theorem, `Ergodic`, `IsProbabilityMeasure`, an
order-theoretic finite partition of the measurable-set subtype, generated and pulled-back
measurable spaces, and `Real.negMulLog`. These are nearby candidate ingredients only. They define no
Kolmogorov-Sinai entropy and select no target theorem, so the probe imports are not claimed to be
minimal imports for the unknown root.

A bounded search of pinned mathlib source found no target-name occurrence matching
Kolmogorov-Sinai, measure-theoretic, Kolmogorov, metric, or partition entropy in the inspected
dynamics and measure-theory trees. This is narrow feasibility evidence, not a saturated anchor
audit or proof of global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The pre-existing `Formalizations/Lean/.lake` link
targets the canonical checkout's pinned artifacts and was used read-only. No update, build, clone,
fetch, or dependency mutation was run.

## Validation evidence

Commands ran in this worker clone on `2026-07-12` (`Asia/Shanghai`).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1406` | 0 | rank 905, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` before statement edits, then `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; the base revision and tree are recorded above |
| `rg -n -C 5 'Kolmogorov-Sinai熵\|动力系统的熵' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md` | 0 | found only the topic phrase and Stage0 fields that leave the exact definitions, premises, proof, axioms, and artifact open |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 and Lake 5.0.0 at the revisions above |
| `sha256sum Docs/Stage1_Targets_rev-5.6.json Docs/Stage1_Blueprint_rev-5.6.md skills/execute-stage1-rev56/SKILL.md Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Stage1_Instances/THM-M-1406/IntakeProbe.lean` | 0 | hashes match `statement-blocker.json` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}' && git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | pinned mathlib revision and tree match the structured blocker; source tree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1406/IntakeProbe.lean` | 0 | all eight adjacent APIs elaborated; no entropy target was asserted |
| `cd Formalizations/Lean && rg -n -i --glob '*.lean' 'kolmogorov.?sinai\|measure.?theoretic entropy\|kolmogorov entropy\|metric entropy\|partition entropy\|entropy of.*partition' .lake/packages/mathlib/Mathlib/Dynamics .lake/packages/mathlib/Mathlib/MeasureTheory` | 1 | expected no-match exit in the bounded pinned source search |
| `python3 Stage1_Instances/THM-M-1406/check_intake.py` | 1 | known phase-evolution failure: the intake-only checker rejects the two later statement artifacts because its original artifact list and hashes are closed; no intake evidence was rewritten |
| `python3 -m json.tool Stage1_Instances/THM-M-1406/statement-blocker.json >/dev/null` | 0 | structured blocker parsed as JSON |
| `rg -n '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|opaque)[[:space:]]\|\bunsafe\b' Stage1_Instances/THM-M-1406 -g '*.lean'` | 1 | expected no-match exit; no prohibited proof construct or unsafe declaration was found |
| added-file whitespace checks plus `test ! -e .stage1-worker-selftest.json` | 0 | both blocker artifacts passed whitespace checks and the required no-self-test boundary is preserved |
| `git status --short --untracked-files=all` | 0 | only the pre-existing `.lake` link and the two owned blocker artifacts are untracked |

## Retry condition and status boundary

An accountable source reviewer must preserve and hash an immutable primary edition or accepted
translation, select and transcribe one exact truth-valued result and every incorporated definition
with pinpoint locators, audit translation fidelity and errata, reconcile the selection with
`THM-M-1404` and `THM-M-1405`, and independently approve the mapping. That decision must freeze the
historical formulation, measure space, dynamics, partitions, iteration direction, equality modulo
null sets, entropy-rate construction, codomain, logarithm, normalization, ordered binders, all
hypotheses, conclusion, and every boundary case.

A later statement worker can then encode that same claim with real Lean definitions, minimize its
pinned imports, serialize and hash the elaborated expression and environment, compile every
credited transport, and run all four required mutation classes.

This is the first failed mathematical gate, not completion of the statement node or any downstream
node. The upstream intake also lacks master acceptance, so this worker cannot claim dependency-legal
completion. The root remains `[H5, M4, R4]`, with `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. The assigned phase is not genuinely
self-tested, so no `.stage1-worker-selftest.json` is emitted.
