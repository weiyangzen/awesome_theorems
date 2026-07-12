# Exact-statement gate: blocked

Item: `S56-M-1404-STATEMENT`

Theorem: `THM-M-1404`

Base revision: `61ce73b9038706a45488f5644ad0e0f3d98937a1`

Base tree: `c8e94ac73b6875f43c55ae766b0c4af4abc7ba3e`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The complete catalog wording is the title `测度熵` (measure-theoretic entropy), the attribution
Andrey Kolmogorov, the year 1958, and the phrase `保测动力系统的熵` (the entropy of a
measure-preserving dynamical system). This names an invariant or subject, not a truth-valued
proposition with ordered binders, hypotheses, and a conclusion. Stage0 explicitly leaves the exact
definitions and premises open, and the metadata label `已验证` is untrusted under rev-5.6.

The existing provisional intake consequently leaves both `canonical_statement` and the formal
declaration or expression null. Its worker receipt is not master-accepted. Several inequivalent
roots remain compatible with the catalog phrase:

- a definition of partition or system entropy, which by itself is not a theorem;
- existence of the normalized finite-partition entropy-rate limit;
- well-definedness of an extended-valued system invariant;
- invariance under measure-theoretic conjugacy;
- an iterate or inverse power law.

Those readings require different measure-space, transformation, partition, iteration, null-set,
limit, codomain, logarithm, and boundary conventions. The separately scheduled Sinai generator
theorem (`THM-M-1405`) and Kolmogorov-Sinai entropy (`THM-M-1406`) cannot be folded into this target.
Selecting a familiar formulation would therefore invent or substitute mathematics rather than
elaborate the exact received target.

The intake inspected a four-page 1958 Kolmogorov scan with a pinned digest and observed sections
1-4, numbered Theorems 1-4, and the symbols `h` and `h(T)`. It deliberately did not select or
translate one definition or theorem as this root. Without a pinpoint passage, incorporated
definitions, translation and errata review, and independent source approval, that discovery record
does not resolve statement identity.

Section 5.1 of the rev-5.6 blueprint therefore fails before proof evidence may be inspected. There
is no canonical target for which imports could be minimized or an elaborated expression could be
serialized. Checked alternate transports and the required removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations are likewise undefined rather than failed tests.
Machine state remains `M4`; statement and theorem completion are false.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` imports
`Mathlib.Analysis.SpecialFunctions.Log.NegMulLog`,
`Mathlib.Dynamics.Ergodic.Ergodic`, and
`Mathlib.MeasureTheory.Measure.PreVariation`. Under the pinned environment it elaborates
`MeasurePreserving`, its iterate theorem, `Ergodic`, `IsProbabilityMeasure`, a finite partition
type, and `Real.negMulLog`. These declarations only show that some candidate ingredients exist.
They neither define measure-theoretic entropy nor select a theorem, so the probe imports are not
claimed to be minimal imports for an unknown canonical target.

A bounded pinned-mathlib search found no literal source-text match for the recorded entropy-name
regex in `Mathlib/Dynamics` or `Mathlib/MeasureTheory`. This is narrow feasibility evidence, not a
saturated anchor audit or proof of global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The pre-existing `Formalizations/Lean/.lake` link
targets the canonical checkout's pinned artifacts and was used read-only. No update, build, clone,
fetch, or dependency mutation was run.

## Validation Evidence

Commands ran in this worker clone on `2026-07-12` (`Asia/Shanghai`).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1404` | 0 | rank 903; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short && git rev-parse HEAD && git rev-parse HEAD^{tree} && readlink Formalizations/Lean/.lake` | 0 | before statement edits, only the pre-existing untracked `.lake` link was present; base revision and tree are recorded above |
| `rg -n -C 4 '测度熵\|保测动力系统的熵' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md` | 0 | found only the topic phrase and Stage0 fields that leave exact definitions, premises, proof, axioms, and artifact open |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 and Lake 5.0.0 at the revisions above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json ../../Stage1_Instances/THM-M-1404/IntakeProbe.lean && git -C .lake/packages/mathlib rev-parse HEAD` | 0 | hashes and pinned mathlib revision match `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1404/IntakeProbe.lean` | 0 | all six adjacent APIs elaborated; no entropy definition or theorem target was asserted |
| `cd Formalizations/Lean && rg -n -i --glob '*.lean' 'measure.?theoretic entropy\|kolmogorov.?sinai\|kolmogorov entropy\|metric entropy\|partition entropy' .lake/packages/mathlib/Mathlib/Dynamics .lake/packages/mathlib/Mathlib/MeasureTheory` | 1 | expected no-match exit in the bounded pinned source search |
| `python3 Stage1_Instances/THM-M-1404/check_intake.py` | 1 | known phase-evolution failure: the historical intake checker requires the directory to contain exactly its nine intake artifacts and rejects the two new blocker artifacts; no intake receipt or hash was rewritten to manufacture agreement |
| `python3 -m json.tool Stage1_Instances/THM-M-1404/statement-blocker.json >/dev/null` | 0 | structured blocker parsed as JSON |
| `rg -n '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|opaque)[[:space:]]\|\bunsafe\b' Stage1_Instances/THM-M-1404 -g '*.lean'` | 1 | expected no-match exit; no prohibited proof construct or unsafe declaration was found |
| added-file whitespace checks plus `test ! -e .stage1-worker-selftest.json` | 0 | both blocker artifacts passed whitespace checks and the required no-self-test boundary is preserved |
| `git status --short --untracked-files=all` | 0 | only the automation-provided `.lake` link and the two owned blocker artifacts are untracked |

## Retry Condition And Status Boundary

An accountable source reviewer must preserve and hash an immutable primary edition or accepted
translation, select and transcribe one exact truth-valued result and every incorporated definition
with pinpoint locators, audit translation fidelity and errata, reconcile the selection with
`THM-M-1405` and `THM-M-1406`, and independently approve the mapping. That decision must freeze the
measure-space and transformation scope, partitions, iteration direction, equality modulo null sets,
entropy-rate construction, codomain, normalization, ordered binders, all hypotheses, conclusion,
and every boundary case.

A later statement worker can then encode that same claim with real Lean definitions, minimize its
pinned imports, serialize and hash the elaborated expression and environment, compile every
credited transport, and run all four required mutation classes.

This is the first failed gate, not completion of the statement node or any downstream node. The root
remains `[H5, M4, R4]`, with `audit_complete: false` and `theorem_complete: false`; no debt-vector
change is proposed. The assigned phase is not genuinely self-tested, so no
`.stage1-worker-selftest.json` is emitted.
