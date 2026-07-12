# Exact-statement blocker

Item: `S56-M-1416-STATEMENT`

Theorem: `THM-M-1416`

Base revision: `ea6d9ac3942ade0c65c13eccb6bcec945e698e69` (tree
`16e4f4fa87955d7ae7392859a6713a56bcfe7b7e`)

## Verdict

The rev-5.6 exact-statement gate is blocked. The authoritative catalog record supplies only the
title "Bowen-Margulis measure," the attribution Rufus Bowen / Grigory Margulis, the year 1970, and
the gloss "measure of/for hyperbolic systems." This identifies an object or theorem family, not a
truth-valued proposition with ordered binders, hypotheses, and a conclusion.

The existing intake therefore correctly leaves the canonical claim, human statement, Lean module,
expression, elaborated-expression hash, and exact-target environment fingerprint null. It also
leaves open the dynamical system, geometric and hyperbolicity setting, measure construction and
normalization, and the desired conclusion. Construction for a geodesic flow, existence or
uniqueness of a measure of maximal entropy, ergodicity, mixing, full support, and periodic-orbit
equidistribution are inequivalent targets. Selecting any one from memory would invent, narrow, or
substitute mathematics.

Sections 5 and 5.1 of the blueprint make statement ambiguity and a missing expression fingerprint
hard blockers. Minimal target imports, checked alternate transports, and mutations for a removed
hypothesis, changed domain, changed binder scope, and boundary case are undefined until a canonical
proposition exists. No `Statement.lean`, proof declaration, or completion receipt was added.

The intake dependency is also only provisional worker state `[_]`, not master-accepted `[x]`.
Dependency acceptance would not resolve the substantive first failure: exact source-statement
identity is still absent.

## Pinned Lean boundary

The existing `IntakeProbe.lean` imports `Mathlib.Dynamics.Ergodic.Ergodic`,
`Mathlib.Dynamics.Flow`, and `Mathlib.Dynamics.TopologicalEntropy.CoverEntropy`. Under the pinned
environment it re-elaborates generic measure, probability, measure-preserving, ergodic, flow, and
Bowen-Dinaburg cover-entropy interfaces. These are possible substrate only. The probe states no
Bowen-Margulis theorem, its imports cannot be certified minimal for an unknown target, and its
successful elaboration receives no statement, anchor, or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The `lean-toolchain`, `lake-manifest.json`, and probe
SHA-256 values are respectively `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`,
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`, and
`e1212a14eb0a0aae92ee1a157bfbf1413c46df31323566ea01955f4f123e05d7`.

The automation-provided `Formalizations/Lean/.lake` link existed before this phase and points to
the canonical checkout's pinned artifacts. It was used read-only. No update, build, clone, fetch,
or other dependency mutation was run.

## Validation evidence

Commands ran in this isolated worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1416` | 0 | rank 915, planned, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all && git rev-parse HEAD && git rev-parse HEAD^{tree}` | 0 | before statement edits, only the pre-existing `.lake` link was untracked; base revision and tree are recorded above |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 and Lake 5.0.0 at the revisions above |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1416/IntakeProbe.lean` | 0 | all six adjacent pinned APIs elaborated; no target theorem was stated |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision matched the environment record |
| bounded pinned-source search for Bowen-Margulis, maximal-entropy measure, Patterson-Sullivan, and geodesic-flow names | 1 | expected no-match exit; limited feasibility evidence only, not an anchor audit or global-absence claim |
| prohibited-construct search over owned Lean files | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, bodyless declaration, or `unsafe` code was found |

The historical `check_intake.py` treats the original nine intake files and its intake-phase root
self-test as a closed artifact set. It will reject the two statement blocker files and the required
absence of a statement-phase self-test. This phase does not rewrite the accepted intake files,
receipt hashes, or checker merely to manufacture agreement.

## Retry condition

First obtain master acceptance of the intake dependency. An accountable source reviewer must then
preserve and hash an immutable primary or authoritative edition, select and transcribe one exact
truth-valued proposition and every incorporated definition with pinpoint locators, audit source
assumptions, translation, corrections, and errata, and obtain independent approval that the claim
represents this target rather than a neighboring theorem. That decision must freeze the exact
system, domains, universes, ordered binders, hypotheses, construction, normalization, conclusion,
and all boundary cases.

A later statement worker can then encode that same claim, minimize the pinned imports, serialize
and hash the elaborated expression and environment, compile every credited transport, and run all
four required mutation classes.

Until then the root remains `[H5, M4, R4]`, with `audit_complete: false` and
`theorem_complete: false`. This blocker is the assigned phase's truthful result, not completion of
the statement node. Because the phase is not genuinely self-tested to its completion gate,
`.stage1-worker-selftest.json` is intentionally absent, and no statement receipt or master
acceptance is claimed.
