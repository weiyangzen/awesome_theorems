# Exact-statement gate: blocked

Item: `S56-M-1411-STATEMENT`

Theorem: `THM-M-1411`

Base revision: `61ce73b9038706a45488f5644ad0e0f3d98937a1` (tree
`c8e94ac73b6875f43c55ae766b0c4af4abc7ba3e`)

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1411-INTAKE` is provisional `[_]`, not
master-accepted `[x]`, so the dependency/master-acceptance gate has not passed. Independently, the
exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record. The
entire claim is the label `双曲动力系统` ("hyperbolic dynamical systems") and the gloss
`双曲性的理论` ("the theory of hyperbolicity"). These words identify a field, not a truth-valued
proposition with ordered binders, hypotheses, and a conclusion. The catalog status `已验证` is
explicitly untrusted under rev-5.6.

The record does not choose any of the proposition-changing data needed for a statement:

- a discrete self-map or diffeomorphism versus a continuous flow, including time and invertibility;
- a topological, smooth finite-dimensional, Banach-manifold, vector-bundle, or cocycle setting;
- a fixed point, periodic orbit, invariant subset, nonwandering set, or whole-space scope;
- local linear, uniform, partial, or nonuniform/Pesin hyperbolicity;
- stable/unstable or stable/center/unstable directions, with continuity or measurability, invariance,
  direct-sum, norm, constant, iterate, and exponential-estimate conventions; or
- one exact conclusion, such as a definition equivalence, invariant splitting, stable manifold,
  shadowing, robustness, decomposition, or symbolic-coding result.

These alternatives are inequivalent. Several familiar consequences and variants also belong to
separate repository targets, including Anosov diffeomorphisms, Axiom A systems, spectral
decomposition, Markov partitions, stable manifolds, structural stability, Lyapunov exponents,
Oseledets' theorem, and Pesin theory. Selecting any one of them would invent, narrow, or substitute
the assigned mathematics.

Consequently there is no canonical human proposition to encode, no exact Lean expression to hash,
and no meaningful way to establish minimal imports, checked alternate transports, or the required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary mutations. No theorem
declaration, axiom, placeholder, broadened interface, or convenient special case was added.

## Pinned Lean boundary

The existing `IntakeProbe.lean` directly imports `Mathlib.Dynamics.Flow`,
`Mathlib.Dynamics.PeriodicPts.Defs`, and `Mathlib.Geometry.Manifold.MFDeriv.Basic`. It successfully
re-elaborates `IsInvariant`, `Flow`, `Flow.fromIter`, `Flow.isInvariant_orbit`,
`Function.IsFixedPt`, `Function.IsPeriodicPt`, `mfderiv`, and `tangentMap`. These are adjacent
substrate APIs only. The probe states no target theorem, and its three imports are not claimed to be
minimal for an unknown target. Its successful elaboration supplies no statement, anchor, or proof
credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The SHA-256 values of `lean-toolchain`,
`lake-manifest.json`, and `IntakeProbe.lean` are, respectively,
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`,
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`, and
`03c69d79d57eab7ee6c8c46ce8e0065cac06a542d4c175ac3068acdb46ec3822`.

The worker clone's pre-existing `Formalizations/Lean/.lake` link points to the canonical pinned
artifacts and was used read-only. No `lake update`, build, dependency clone, fetch, or other `.lake`
mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1411` | 0 | rank 910, planned, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | 0 | before this attempt, only the automation-provided untracked `Formalizations/Lean/.lake` link was present |
| `rg -n -C 6 '双曲动力系统\|双曲性的理论' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md` | 0 | found only the field label, theory gloss, and Stage0's open definitions and premises; no proposition or pinpoint source |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0 at the commit above |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake version above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Stage1_Instances/THM-M-1411/IntakeProbe.lean` | 0 | hashes agree with the pinned fingerprint above |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1411/IntakeProbe.lean)` | 0 | all eight adjacent APIs elaborated; no canonical target was stated |
| bounded exact-topic search under pinned `Mathlib/Dynamics` | 1 | expected no-match exit; no hyperbolic-dynamics, hyperbolicity, uniformly-hyperbolic, Anosov, or Axiom A name found; discovery only, not an anchor audit |
| prohibited Lean proof-escape scan over the owned path | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, or `constant` declaration in target Lean source |
| `python3 -m json.tool Stage1_Instances/THM-M-1411/instance.json` | 0 | intake JSON is valid; the canonical claim and formal target remain null |
| `python3 -m json.tool Stage1_Instances/THM-M-1411/task-dag.json` | 0 | task DAG JSON is valid; statement and every downstream task remain open |
| `python3 -m json.tool Stage1_Instances/THM-M-1411/statement-blocker.json` | 0 | structured blocker is valid JSON |
| statement-blocker invariant check | 0 | item identity, `[ ]` state, null target and fingerprint, H5/M4/R4 boundary, false completion flags, and absent worker self-test agree |
| `git diff --check -- Stage1_Instances/THM-M-1411` plus per-new-file `git diff --no-index --check` | 0 | no whitespace diagnostics; the expected add-file diff status was accepted for each untracked blocker artifact |

## Retry condition and status boundary

First obtain master acceptance of the intake. Then an accountable reviewer must preserve and hash
an immutable primary or authoritative source, identify and transcribe one exact proposition and
all incorporated definitions with a pinpoint locator, audit errata, freeze every semantic choice
and boundary case above, and obtain independent approval that the proposition represents this
target rather than a neighbor. A later statement worker can then encode that same claim, minimize
its pinned imports, serialize and hash the elaborated expression and environment, check alternate
transports, and run all four required mutation classes.

The first failed substantive gate is exact source-statement identity. The provisional, unaccepted
intake dependency independently prevents node acceptance. The root remains `[H5, M4, R4]`, with
`audit_complete: false` and `theorem_complete: false`; no debt-vector change is proposed. This is
blocked-attempt evidence, not completion of the statement node or any downstream node. Because the
assigned phase is not genuinely self-tested to its completion gate, no
`.stage1-worker-selftest.json` is emitted and no worker `[_]` or master-acceptance receipt is
claimed.
