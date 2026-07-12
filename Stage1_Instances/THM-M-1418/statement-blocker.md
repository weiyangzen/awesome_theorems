# Exact-statement gate: blocked

Item: `S56-M-1418-STATEMENT`

Theorem: `THM-M-1418`

Base revision: `3d1d6d3eb018f17657cae1cfd7d25fc30492a12b` (tree
`3aa3dd324b35549da6cf2c5a54183a63ed1bfff9`)

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1418-INTAKE` is provisional `[_]`, not
master-accepted `[x]`, so the dependency/master-acceptance gate has not passed. Independently, the
exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record. The
entire mathematical claim is the label `Lyapunov指数` ("Lyapunov exponent") and the gloss
`轨道分离的指数率` ("exponential rate of orbit separation"). These words identify a dynamical
quantity, not a truth-valued proposition with ordered binders, hypotheses, and a conclusion. The
catalog status `已验证` is explicitly untrusted under rev-5.6.

The record does not choose any of the proposition-changing data needed for a statement:

- a discrete self-map, a differentiable flow, or a deterministic or random linear cocycle;
- a phase space and its metric, normed-vector, smooth, bundle, measurable, probability,
  compactness, or finite-dimensional structure;
- a base point or orbit and a second-point perturbation procedure, or a nonzero tangent or cocycle
  direction, including all quantifiers and exceptional sets;
- metric separation versus derivative or cocycle norm growth, and a maximal, directional, indexed,
  or full-spectrum exponent;
- an ordinary limit, limsup, or liminf; real or extended-real codomain; logarithm base;
  normalization; norm or metric; and pointwise, uniform, or almost-everywhere scope; or
- one exact conclusion, such as existence, invariance, stability, constancy, a spectrum, a
  measurable splitting, or an entropy relation.

These alternatives are inequivalent. Boundary choices also change the claim: coincident points,
the zero tangent vector, a zero derivative or cocycle image, `log 0`, infinite exponents, failure of
an ordinary limit, fixed or periodic orbits, time zero, forward versus two-sided time, norm
dependence, and exceptional null sets all remain open.

Neighboring catalog entries rule out convenient substitutions. `THM-M-1419` owns Oseledets'
multiplicative ergodic theorem and its exponent-existence or splitting conclusion;
`THM-M-1420` owns Pesin theory; `THM-M-1421` owns the Pesin entropy formula; and `THM-M-1056`
separately names a random-matrix Oseledets theorem. Lyapunov stability and Lyapunov functions,
finite-time numerical estimates, toy examples, and structures that assume an exponent as a field
are likewise not this target.

Consequently there is no canonical human proposition to encode, no exact Lean expression to hash,
and no meaningful way to establish minimal imports, checked alternate transports, or the required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary mutations. No theorem
declaration, axiom, placeholder, broadened interface, weakened special case, or substituted result
was added.

## Pinned Lean boundary

The existing `IntakeProbe.lean` directly imports `Mathlib.Logic.Function.Iterate`,
`Mathlib.Topology.MetricSpace.Basic`, `Mathlib.Analysis.Calculus.FDeriv.Basic`,
`Mathlib.Analysis.SpecialFunctions.Log.Basic`, and `Mathlib.Order.LiminfLimsup`. It successfully
re-elaborates these nine adjacent interfaces:

- `Function.comp_def` and `Function.Semiconj.iterate_right`;
- `dist`;
- `fderiv` and `HasFDerivAt`;
- `norm_nonneg`;
- `Real.log`; and
- `Filter.limsup` and `Filter.liminf`.

These are substrate APIs only. The probe states no target theorem, and its five imports are not
claimed to be minimal for an unknown target. Its successful elaboration supplies no statement,
anchor, or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The SHA-256 values of `lean-toolchain`,
`lake-manifest.json`, and `IntakeProbe.lean` are, respectively,
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`,
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`, and
`bdd3ee8ac44e62ef0b1815227d9c6fd7e95a9021ecd5098179da0ab23a764e65`.

The worker clone's pre-existing `Formalizations/Lean/.lake` link points to the canonical pinned
artifacts and was used read-only. No `lake update`, `lake build`, dependency clone, fetch, or other
`.lake` mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1418` | 0 | rank 917, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | 0 | preflight showed only the automation-provided untracked `Formalizations/Lean/.lake` link; final status additionally shows the two owned blocker files |
| `rg -n -C 6 'Lyapunov指数\|轨道分离的指数率\|Oseledets乘法遍历定理\|Lyapunov指数的存在性' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md` | 0 | found only the topic/gloss records and Stage0's open definitions and premises; no proposition or pinpoint source |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0 at the commit above |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake version above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Stage1_Instances/THM-M-1418/IntakeProbe.lean` | 0 | hashes agree with the pinned fingerprint above |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1418/IntakeProbe.lean)` | 0 | all nine adjacent APIs elaborated; no canonical target was stated |
| `rg -n -i 'lyapunov\|liapunov\|oseledets\|multiplicative[ _-]ergodic\|linear[ _-]cocycle' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | expected no-match exit; discovery only, not an anchor audit |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)\b' Stage1_Instances/THM-M-1418` | 1 | expected no-match exit; no prohibited proof escape or declaration in target Lean source |
| `python3 -m json.tool Stage1_Instances/THM-M-1418/instance.json` and likewise for `task-dag.json`, `intake-receipt.json`, and `statement-blocker.json` | 0 each | all four structured artifacts are valid JSON; the target remains null and the statement task remains open |
| `jq -e '.item_id == "S56-M-1418-STATEMENT" and .state == "[ ]" and (.statement_gate_passed == false) and (.canonical_statement == null) and (.canonical_formal_target == null) and (.root_vector == {"H":"H5","M":"M4","R":"R4"}) and (.statement_elaborated == false) and (.theorem_complete == false) and (.gate_state == "blocked_no_worker_selftest")' Stage1_Instances/THM-M-1418/statement-blocker.json` | 0 | blocker identity, open state, null target, H5/M4/R4 boundary, and false completion flags agree |
| `git diff --check -- Stage1_Instances/THM-M-1418` plus per-new-file `git diff --no-index --check -- /dev/null <file>`, accepting exit 1 only as the normal added-file difference | 0 | no whitespace diagnostics in tracked or new owned artifacts |
| `test ! -e .stage1-worker-selftest.json` | 0 | worker self-test is absent because the statement completion gate did not pass |

The two owned artifacts added by this attempt are `statement-blocker.json` and
`statement-blocker.md`. They add no Lean declaration, obligation, statement fingerprint, typed
graph edge, composition certificate, proof body, or accepted receipt. The change-impact set is only
`S56-M-1418-STATEMENT`.

## Retry condition and status boundary

First obtain master acceptance of the intake. Then an accountable reviewer must preserve and hash
an immutable primary or authoritative source, identify and transcribe one exact truth-valued
proposition and all incorporated definitions with a pinpoint locator, audit errata, freeze every
semantic choice and boundary case above, and obtain independent approval that the proposition
represents this target rather than a neighbor. A later statement worker can then encode that same
claim, minimize its pinned imports, serialize and hash the elaborated expression and environment,
check alternate transports, and run all four required mutation classes.

The first failed substantive gate is exact source-statement identity. The provisional, unaccepted
intake dependency independently prevents node acceptance. The root remains `[H5, M4, R4]`, with
`audit_complete: false` and `theorem_complete: false`; no debt-vector change is proposed. This is
blocked-attempt evidence, not completion of the statement node or any downstream node. Because the
assigned phase is not genuinely self-tested to its completion gate, no
`.stage1-worker-selftest.json` is emitted and no worker `[_]` or master-acceptance receipt is
claimed.
