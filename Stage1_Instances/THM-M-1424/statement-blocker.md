# Exact-statement gate: blocked

Item: `S56-M-1424-STATEMENT`

Theorem: `THM-M-1424`

Base revision: `a4c7dbb600e52683335f2d2fdce53507a6a71422` (tree
`4e208cb1f379cd8fbfcca0c9860db5b5df0a3dd6`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record supplies only the subject label `随机动力系统` ("random dynamical systems"), Ludwig
Arnold, the year 1998, and the gloss `随机微分方程的动力学` ("dynamics of stochastic differential
equations"). It supplies no truth-valued proposition, primary-source theorem locator, incorporated
definitions, ordered binders, hypotheses, conclusion, proof boundary, or errata. Stage0 explicitly
leaves the exact definitions and premises, proof route, dependencies, alternate forms, axioms, and
machine artifact open. The catalog label `已验证` is untrusted under rev-5.6.

Arnold's 1998 monograph is a strong bibliographic match, but it contains multiple inequivalent
results. Chapter 1 includes definitions and cocycle-perfection results; Chapter 2 includes global
and local random-differential-equation generation theorems, semimartingale-driven generation
theorems, and converse representation theorems. The intake also records Arnold and Scheutzow's
1995 article as a primary-source candidate: its Theorems 28, 30, and 31 respectively give a global
semimartingale-RDS generation result, a converse, and a cocycle-perfection result. The catalog does
not select any of these propositions, and none has an accepted exact-statement crosswalk.

The following proposition-changing inputs therefore remain unresolved:

- the immutable source edition, exact theorem and definition chain, proof boundary, corrections,
  errata, and independent source-to-target approval;
- the probability/noise space and measure-preserving base action, including completion and
  exceptional-set conventions;
- the time monoid or group, one-sided or two-sided convention, and treatment of time zero and
  inverse shifts;
- the measurable, topological, metric, manifold, or Banach state space and its regularity,
  separability, completeness, compactness, and dimensional assumptions;
- the stochastic or random differential equation, driver, filtration, integration and solution
  notions, coefficient regularity, pathwise uniqueness, explosion, and version policy;
- the global or local, crude or perfected, measurable, continuous, or smooth cocycle convention;
  and
- whether the conclusion is generation, converse representation, perfection, invariant measure,
  stability, regularity, or another result, together with every binder and boundary case.

Selecting one familiar generation theorem, merely defining an RDS, using a deterministic flow,
or introducing a structure that assumes the desired cocycle or conclusion would invent, narrow,
or substitute mathematics. Rev-5.6 section 5 makes statement ambiguity and a missing expression
fingerprint hard blockers. There is therefore no canonical expression on which to certify minimal
imports, checked alternate transports, or removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations. Those four tests are undefined, not passed. The
first failed gate is exact source-statement identity, and the root remains `[H5, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` directly imports four pinned modules and checks eight adjacent APIs
for filtrations, adapted processes, Markov kernels, measure-preserving maps, and deterministic
flows. It elaborates successfully in the pinned environment but states no target theorem.
Mathlib's `Flow` is a deterministic continuous monoid action, not a random cocycle. The four probe
imports are discovery candidates only and cannot be certified minimal for a target that does not
exist.

A bounded pinned-mathlib source-name search found no occurrence matching the searched RDS, random
cocycle, metric dynamical system, SDE, or semimartingale phrases. This is narrow feasibility
evidence, not the downstream anchor audit and not proof of absence from every Lean project.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The `lean-toolchain`, `lake-manifest.json`, and probe
SHA-256 values are respectively
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`,
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`, and
`685944eb2f83811d4ad2df0270750b1626f1213f8d7070b206ad63c8eb476d5a`.

The automation-provided `Formalizations/Lean/.lake` link existed before this phase and points to
the canonical checkout's pinned artifacts. It was used read-only. No `lake update`, `lake build`,
dependency clone or fetch, or other `.lake` mutation was run.

## Validation Evidence

Commands ran from this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1424` | 0 | rank 922, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all && git rev-parse HEAD 'HEAD^{tree}'` | 0 | before statement edits, only the pre-existing untracked `.lake` link was present; the base revision and tree are recorded above |
| source-record and dossier `rg`/`nl` inspection | 0 | the catalog and Stage0 supply only a subject label and broad gloss; the intake leaves the canonical statement and formal target null |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 and Lake 5.0.0 at the revisions above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | the pinned mathlib revision and tree above; package status was clean |
| `sha256sum Docs/Stage1_Targets_rev-5.6.json Docs/Stage1_Blueprint_rev-5.6.md skills/execute-stage1-rev56/SKILL.md Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Stage1_Instances/THM-M-1424/IntakeProbe.lean` | 0 | manifest, blueprint, skill, toolchain, dependency-lock, and probe inputs were fingerprinted in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1424/IntakeProbe.lean` | 0 | eight adjacent pinned APIs elaborated; no target theorem was stated |
| bounded pinned-mathlib source search for RDS, random cocycle, metric dynamical system, SDE, and semimartingale phrases | 1 | expected no-match exit; discovery-only feasibility evidence, not an anchor audit |
| `python3 -B Stage1_Instances/THM-M-1424/check_intake.py` before statement artifacts were added | 0 | the integrated planned intake, H5/M4/R4 boundary, and six open tasks agreed |
| `python3 -B Stage1_Instances/THM-M-1424/check_intake.py` after statement artifacts were added | 1 | expected historical intake-only failure: its frozen nine-file inventory does not admit later-phase artifacts; no intake evidence was rewritten |
| `python3 -m json.tool Stage1_Instances/THM-M-1424/statement-blocker.json` and scoped `jq` assertions | 0 | blocker JSON parsed; identity, null target, failed gate, four undefined mutations, unchanged debt, false completion flags, and changed paths agreed |
| prohibited Lean proof-escape scan over the owned path | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped tracked and added-file whitespace checks | 0 | no whitespace diagnostics; added-file checks normalized `git diff --no-index --check`'s expected difference status |
| `test ! -e .stage1-worker-selftest.json` | 0 | the required no-self-test boundary is preserved because the statement deliverable is blocked |

After the blocker artifacts are added, the historical intake-only checker rejects their presence
because it freezes the intake phase's exact nine-file inventory. This statement run does not
rewrite intake evidence merely to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must first accept the provisional intake dependency. An accountable source
reviewer must then preserve and hash an immutable primary or authoritative edition, select and
transcribe one exact theorem and every incorporated definition with pinpoint locators, audit its
proof boundary and errata, freeze every base, time, state, equation, solution, cocycle,
measurability, locality, exceptional-set, binder, conclusion, and boundary convention above, and
justify why that proposition represents `THM-M-1424`. A second qualified reviewer must approve the
mapping.

A later statement worker can then encode that same claim using real Lean definitions, minimize its
pinned imports, serialize and hash the elaborated expression and environment, compile every
credited transport, and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the phase is not genuinely
self-tested to its completion gate, no `.stage1-worker-selftest.json` is emitted and no statement
receipt or master acceptance is claimed.
