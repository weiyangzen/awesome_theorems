# Exact-statement gate: blocked

Item: `S56-M-1427-STATEMENT`

Theorem: `THM-M-1427`

Base revision: `a4c7dbb600e52683335f2d2fdce53507a6a71422` (tree
`4e208cb1f379cd8fbfcca0c9860db5b5df0a3dd6`).

## Decision

The exact Lean 4 target cannot be truthfully selected or elaborated from the authoritative
repository record. Its complete mathematical wording is only the field label `复动力系统`
(`complex dynamical systems`) and the gloss `复解析映射的动力学` (`dynamics of complex analytic
maps`), attributed to many mathematicians in the twentieth century. It gives no bibliography,
definition, ordered binders, hypotheses, truth-valued conclusion, theorem locator, proof boundary,
or errata. The metadata label `已验证` is untrusted under rev-5.6.

The intake dependency deliberately freezes this as an unstable catalog target at `[H5, M4, R4]`
and leaves the canonical mathematical claim and formal target null. It also has provisional worker
state only, not master acceptance. The missing proposition-changing choices include:

- the phase space: `Complex`, a plane domain, the Riemann sphere, or a complex manifold;
- the map class: holomorphic, entire, meromorphic, polynomial, rational, or manifold-holomorphic,
  together with the self-map, degree, nonconstancy, pole, and infinity conventions;
- the iteration domain and whether zero iteration is included;
- the orbit, fixed-point, periodic-point, invariant-set, normality, stability, or other predicates;
- the exact theorem family and conclusion, including its topology or convergence notion; and
- the quantifier order and all constant, degree-zero/one, empty-domain, boundary, critical,
  exceptional-point, and undefined-iterate cases.

These choices yield inequivalent propositions. Choosing closure of analytic maps under iteration,
a fixed- or periodic-point result, a Julia/Fatou normal-family result, a local linearization
theorem, or a global dynamics theorem would invent or substitute missing mathematics. In
particular, the repository separately schedules Julia sets (`THM-M-1428`), Fatou sets
(`THM-M-1429`), the Mandelbrot set (`THM-M-1430`), the Douady-Hubbard theorem (`THM-M-1431`),
Yoccoz's theorem (`THM-M-1432`), the Brjuno condition (`THM-M-1433`), and Sullivan's
no-wandering-domain theorem (`THM-M-1434`). None can silently replace this field label.

The first failed gate is exact source-statement identity. With no canonical expression, there is no
truthful target declaration, minimal target import set, elaborated-expression fingerprint, checked
alternate transport, or meaningful removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutation suite. Those tests are undefined, not passed. No `Statement.lean`, assumed
predicate, axiom, placeholder, convenient special case, or statement receipt was created.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` imports three pinned modules and checks ten adjacent APIs for
analytic and meromorphic maps, composition, function iteration, fixed points, and periodic points.
It elaborates successfully and states no target theorem. These imports are discovery candidates
only; they cannot be certified minimal for an unidentified proposition.

A bounded pinned-mathlib source-name search found no named complex-dynamics, holomorphic-dynamics,
rational-dynamics, Julia-set, or Mandelbrot-set declaration under the searched terms. Its only
`Fatou` matches were measure-theoretic Fatou lemmas. A separate algebraic-geometry rational-map
module is not an analytic self-map dynamics target. This is narrow feasibility evidence, not an
anchor audit or proof of global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The `lean-toolchain`, `lake-manifest.json`, and probe
SHA-256 values are respectively `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`,
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`, and
`e9dadd0d7434c8d66684d0e38cb97472556a1b4bf4132091e5aa08709b808fde`.

The automation-provided `Formalizations/Lean/.lake` link existed before this phase and points to
the canonical checkout's pinned artifacts. It was used read-only. No `lake update`, `lake build`,
dependency clone or fetch, or other `.lake` mutation was run.

## Validation Evidence

Commands ran from this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1427` | 0 | rank 925, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all && git rev-parse HEAD && git rev-parse HEAD^{tree}` | 0 | before statement edits, only the pre-existing untracked `.lake` link was present; base revision and tree are recorded above |
| source-record and dossier `rg`/`nl` inspection | 0 | the catalog gives only a field label and activity gloss; the intake leaves the exact claim, formal target, imports, expression hash, and target environment fingerprint null |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, `x86_64-unknown-linux-gnu`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e`, Lean 4.29.0 |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1427/IntakeProbe.lean` | 0 | ten adjacent analytic, meromorphic, composition, iteration, fixed-point, and periodic-point APIs elaborated; no target theorem was stated |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | no output; pinned package worktree clean |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Stage1_Instances/THM-M-1427/IntakeProbe.lean` | 0 | hashes agree with the environment fingerprint above |
| bounded repository search for the theorem ID, Chinese/English labels, and gloss | 0 | found only underspecified metadata, generated projections, this intake dossier, and neighboring-target boundary references; no corrected proposition |
| bounded pinned-mathlib source search for complex-dynamics names | 0 | only three unrelated measure-theoretic Fatou-lemma lines matched; no target declaration found; discovery-only evidence |
| `python3 Stage1_Instances/THM-M-1427/check_intake.py` | 1 | known intake-only checker failure: it requires the intake worker's root self-test manifest, which the integration commit did not retain; this statement run does not recreate or rewrite intake evidence |
| prohibited Lean proof-escape scan over the owned path | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-1427/statement-blocker.json` and scoped Python assertions | 0 | blocker JSON parsed; identity, null target and imports, four undefined mutations, unchanged debt vector, false completion flags, changed paths, and no-self-test boundary agree |
| scoped tracked and added-file whitespace checks | 0 | no whitespace diagnostics; added-file checks normalized `git diff --no-index --check`'s expected difference status |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test manifest exists because the assigned statement deliverable is blocked |

## Retry Condition And Status Boundary

The integration lane must first accept the intake dependency. An accountable source owner must then
approve a corrected truth-valued root, preserve and hash an immutable primary or authoritative
source, select and transcribe one exact theorem and every incorporated definition, audit assumptions,
corrections and errata, and justify why that theorem represents `THM-M-1427` rather than a separately
scheduled neighbor. A second qualified reviewer must approve the source-to-statement mapping.

A later statement worker can then encode that same proposition with real Lean definitions, minimize
its pinned imports, serialize and hash the elaborated expression and environment, compile every
credited transport, and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; the root remains `[H5, M4, R4]`; `audit_complete` and
`theorem_complete` remain false; and no debt-vector change is proposed. Because the assigned phase
is not genuinely self-tested to its completion gate, no `.stage1-worker-selftest.json` is emitted
and no receipt or master acceptance is claimed.
