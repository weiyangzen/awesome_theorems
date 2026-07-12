# Exact-statement gate: blocked

Item: `S56-M-1412-STATEMENT`

Theorem: `THM-M-1412`

Base revision: `3d1d6d3eb018f17657cae1cfd7d25fc30492a12b` (tree
`3aa3dd324b35549da6cf2c5a54183a63ed1bfff9`)

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1412-INTAKE` is provisional `[_]`, not
master-accepted `[x]`, so the dependency/master-acceptance gate has not passed. Independently, the
exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record. The
entire mathematical record is the title `Anosov微分同胚` ("Anosov diffeomorphism"), the attribution
Dmitri Anosov, the year 1967, and the gloss `一致双曲系统` ("uniformly hyperbolic system"). These
words name a class of smooth dynamical systems; they do not select a truth-valued proposition with
ordered binders, hypotheses, and a conclusion. The catalog status `已验证` is explicitly untrusted
under rev-5.6.

The record does not choose any of the proposition-changing data needed for a statement:

- a definition or classification predicate versus an existence, equivalence, structural-stability,
  expansivity, stable-manifold, periodic-orbit, or other consequence theorem;
- the scalar field, model space, universe levels, dimension, differentiability class, compactness,
  connectedness, boundary, smooth structure, and metric or tangent norm of the manifold;
- the regularity and global invertibility of the map, the time or iterate domain, and whether
  hyperbolicity holds on the whole manifold or only on an invariant subset;
- stable and unstable subspaces or subbundles, their continuity, dimensions, directness, and
  invariance under the derivative cocycle;
- uniform constants, their side conditions, forward or inverse iterate conventions, norms, and the
  exact contraction or expansion inequalities; or
- empty, singleton, zero-dimensional, disconnected, noncompact, boundary-bearing, zero-subbundle,
  and `n = 0` cases.

These alternatives are inequivalent. Several familiar variants and consequences also belong to
separate repository targets, including generic hyperbolic dynamical systems, Axiom A, spectral
decomposition, Markov partitions, stable manifolds, structural stability, Lyapunov exponents,
Oseledets' theorem, and Pesin theory. Choosing a standard definition, a toral example, or any one
of those results would invent, narrow, or substitute the assigned mathematics.

The intake's historical Anosov and Smale references are discovery leads only. No immutable edition,
exact definition or theorem locator, incorporated assumptions, errata disposition, or independent
review selects either as this target. Consequently there is no canonical human proposition to
encode, no exact Lean expression to hash, and no meaningful way to establish minimal imports,
checked alternate transports, or the required removed-hypothesis, changed-domain,
changed-binder-scope, and boundary mutations. No theorem declaration, axiom, placeholder,
broadened interface, or convenient special case was added.

## Pinned Lean boundary

The existing `IntakeProbe.lean` directly imports `Mathlib.Geometry.Manifold.Diffeomorph` and
`Mathlib.Geometry.Manifold.MFDeriv.Defs`. It successfully re-elaborates `Diffeomorph`,
`Diffeomorph.refl`, `Diffeomorph.symm`, `Diffeomorph.trans`, `TangentSpace`, `TangentBundle`,
`mfderiv`, and `tangentMap`. These are adjacent substrate APIs only. The probe states no target
theorem, and its imports are not claimed to be minimal for an unknown target. Its successful
elaboration supplies no statement, anchor, or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The SHA-256 values of `lean-toolchain`,
`lake-manifest.json`, and `IntakeProbe.lean` are, respectively,
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`,
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`, and
`04b36a5c1f13e5ae43c4e7f89c26148db3c3a07a310d0d6d10288d0bb4a20029`.

The worker clone's pre-existing `Formalizations/Lean/.lake` link points to the canonical pinned
artifacts and was used read-only. No `lake update`, build, dependency clone, fetch, or other `.lake`
mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1412` | 0 | rank 911, planned, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | 0 | before this attempt, only the automation-provided untracked `Formalizations/Lean/.lake` link was present |
| `rg -n -C 5 'Anosov微分同胚|一致双曲系统|THM-M-1412' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md Docs/Stage1_Targets_rev-5.6.json` | 0 | found only the class label, descriptive gloss, and Stage0's open definitions and premises; no proposition or pinpoint source |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0 at the commit above |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake version above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Stage1_Instances/THM-M-1412/IntakeProbe.lean` | 0 | hashes agree with the pinned fingerprint above |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1412/IntakeProbe.lean)` | 0 | all eight adjacent APIs elaborated; no canonical target was stated |
| `rg -n -i 'Anosov|uniform(ly)?[ _-]+hyperbolic|hyperbolic[ _-]+(diffeomorphism|system)' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | expected no-match exit; bounded discovery-only name search, not an anchor audit |
| `rg -n '\b(sorry|admit|sorryAx)\b|^[[:space:]]*(axiom|opaque)[[:space:]]' Stage1_Instances/THM-M-1412 -g '*.lean'` | 1 | expected no-match exit; no prohibited proof construct or declaration in target Lean source |
| `python3 -m json.tool Stage1_Instances/THM-M-1412/instance.json`, `task-dag.json`, and `intake-receipt.json` | 0 | all three intake JSON artifacts are valid; the canonical claim and formal target remain null |
| `python3 Stage1_Instances/THM-M-1412/check_intake.py` | 1 | known phase-evolution failure: the historical intake checker requires exactly its nine intake artifacts and rejects the two new blocker artifacts; no intake receipt or hash was rewritten to manufacture agreement |
| `python3 -m json.tool Stage1_Instances/THM-M-1412/statement-blocker.json` | 0 | structured blocker is valid JSON |
| inline Python statement-blocker invariant check | 0 | item identity, `[ ]` state, null target and fingerprint, H5/M4/R4 boundary, false completion flags, and absent worker self-test agree |
| `git diff --check -- Stage1_Instances/THM-M-1412` plus `git diff --no-index --check -- /dev/null <file>` for each blocker | 0 | no whitespace diagnostics; expected add-file diff status 1 was accepted |

## Retry condition and status boundary

First obtain master acceptance of the intake. Then an accountable reviewer must preserve and hash
an immutable primary or authoritative source, identify and transcribe one exact proposition and
all incorporated definitions with a pinpoint locator, audit errata, freeze every manifold,
regularity, splitting, derivative, constant, iterate, norm, hypothesis, conclusion, and boundary
convention above, and obtain independent approval that the proposition represents this target
rather than a neighbor. A later statement worker can then encode that same claim, minimize pinned
imports, serialize and hash the elaborated expression and environment, check alternate transports,
and run all four required mutation classes.

The first failed substantive gate is exact source-statement identity. The provisional, unaccepted
intake dependency independently prevents node acceptance. The root remains `[H5, M4, R4]`, with
`audit_complete: false` and `theorem_complete: false`; no debt-vector change is proposed. This is
blocked-attempt evidence, not completion of the statement node or any downstream node. Because the
assigned phase is not genuinely self-tested to its completion gate, no
`.stage1-worker-selftest.json` is emitted and no worker `[_]` or master-acceptance receipt is
claimed.
