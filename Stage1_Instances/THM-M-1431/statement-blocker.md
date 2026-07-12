# Exact-statement gate: blocked

Item: `S56-M-1431-STATEMENT`

Theorem: `THM-M-1431`

Base revision: `dd8846dbc83818f6ba7124151d5d4b7b29bb5b0d` (tree
`1bf3680085cf7338ac4d405cf4ef2188fa14ccec`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1431-INTAKE` has provisional worker
state `[_]`, which the scheduler permits as the basis for this statement attempt. Master acceptance
is still required before an eventual accepted transition, but it did not block worker execution.
The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record. That record supplies
only the name `Douady-Hubbard定理`, Adrien Douady and John Hubbard, the year 1982, and the
gloss `Mandelbrot集的连通性` ("connectedness of the Mandelbrot set"). It supplies no
publication, exact source passage, incorporated definitions, ordered binders, hypotheses, proof
boundary, errata, or formal artifact. The catalog status `已验证` ("verified") is explicitly
untrusted under rev-5.6.

The intake identifies the 1982 C. R. note and the expanded Orsay notes, Chapter 8, Theorem 8.1 and
Corollary 8.3(a), as strong primary-source candidates. They have not been admitted as an immutable
edition with an independently approved definition chain, translation, corrections, and errata.
The repository also contains the exact metadata duplicate `THM-M-0261`; no authority has reconciled
the two target identities or assigned source and evidence ownership between them.

Several proposition-changing choices therefore remain open:

- whether the Mandelbrot locus is defined by boundedness of the range of the critical orbit,
  non-escape to infinity, membership of `0` in a filled Julia set, or connectedness of that filled
  Julia set, and which checked transports relate credited forms;
- whether the orbit is written from `0` or from its first value `c`, whether iterate zero is
  included, and whether boundedness uses `Bornology.IsBounded`, a uniform norm bound, an
  escape-radius condition, or a filter formulation;
- whether the root uses `IsConnected` or a separately composed nonemptiness plus
  `IsPreconnected` statement, and whether the ambient space is `Complex` or a compactification;
- how boundary parameters, the cusp `c = 1/4`, escape-radius equality, empty-set conventions, and
  the alternate filled-Julia and conformal-complement routes are treated.

Selecting the familiar bounded-critical-orbit formulation would be plausible mathematics, but it
would still make decisions that this target's integrated intake deliberately left open. A
conformal-isomorphism theorem, filled-Julia statement, compactness theorem, path-connectedness, or
local-connectedness claim would instead strengthen or substitute the requested root. Section 5 of
the rev-5.6 blueprint makes statement ambiguity and a missing expression fingerprint hard
blockers. There is consequently no canonical expression on which to certify minimal imports,
checked alternate transports, or removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations. Those four mutation classes are undefined, not passed. The first failed
substantive gate is exact source-statement identity, and the root remains `[H1, M4, R3]`.

This is a policy boundary, not a claim that Lean lacks the necessary vocabulary. A conventional
bounded-critical-orbit `IsConnected` target is technically expressible in the pinned environment,
and other dossiers sometimes freeze conventional forms while their H1 source audit remains open.
This attempt defers that choice because this target's integrated intake expressly freezes the
canonical claim and expression as null pending a source-exact definition-chain decision. Pending
intake acceptance and duplicate bookkeeping are separate acceptance and evidence-ownership issues;
neither is presented as the substantive elaboration failure.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` directly imports `Mathlib.Analysis.Complex.Basic`,
`Mathlib.Logic.Function.Iterate`, `Mathlib.Topology.MetricSpace.Bounded`, and
`Mathlib.Topology.Separation.Connected`. It re-elaborates representative complex-number,
iteration, range, boundedness, connectedness, preconnectedness, and compactness interfaces. The
probe states no proposition for `THM-M-1431`; its imports are discovery candidates only and cannot
be certified minimal for an unresolved target.

A bounded source-name search of pinned mathlib identified no Douady-Hubbard, Mandelbrot,
filled-Julia, Bottcher, or queried complex-dynamics declaration. The only output was an unrelated
bibliography line containing the surname Hubbard. This is narrow feasibility evidence, not the
downstream immutable anchor audit and not proof of global absence.

The adjacent intake for `THM-M-1430` records a credible future formal candidate:
`girving/ray` at immutable revision `0ca7b1e746b2911557ac76f56259068cfd1423ab`, whose
`Ray/Mandelbrot.lean` defines a non-escape locus and proves its connectedness under Lean
`v4.27.0-rc1` and mathlib `725c803ee924f55342e93f2c75976051ab902b54`. That source is not in
this repository's dependency closure, was not fetched or built in this phase, and has not passed
the source-statement mapping or downstream anchor audit for this target. It receives no statement
or proof credit here.

The local pinned environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The SHA-256 values of `lean-toolchain`,
`lake-manifest.json`, and `IntakeProbe.lean` are, respectively,
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`,
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`, and
`378ad3b2de17a898526ef4ce8a69da054d398f6b7461cfa1fa7991fea0194647`.

The worker clone's pre-existing `Formalizations/Lean/.lake` link points to the canonical pinned
artifacts and was used read-only. No `lake update`, `lake build`, dependency clone or fetch, or
other `.lake` mutation was run.

## Validation Evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1431` | 0 | rank 929, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all && git rev-parse HEAD && git rev-parse HEAD^{tree}` | 0 | before statement edits, only the pre-existing untracked `.lake` link was present; base revision and tree are recorded above |
| `rg -n -C 8 -e 'Douady-Hubbard定理' -e '曼德博集合连通性' -e 'Mandelbrot集的连通性' -e 'THM-M-1431' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md Docs/Stage1_Targets_rev-5.6.json Docs/Stage1_Execution_DAG_rev-5.6.json Stage1_Instances/THM-M-1431/{instance.json,source-statement-crosswalk.md,scope-map.md,task-dag.json}` | 0 | the catalog supplies only the connectedness gloss; Stage0 and intake leave the definition chain and exact target open; `THM-M-0261` is an unreconciled duplicate |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 and Lake 5.0.0 at the revisions above |
| `cd Formalizations/Lean && git -C .lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}' && git -C .lake/packages/mathlib status --short` | 0 | pinned mathlib revision and tree recorded above; empty status output confirms the package worktree is clean |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json ../../Docs/Stage1_Targets_rev-5.6.json ../../Docs/Stage1_Blueprint_rev-5.6.md ../../Docs/Stage1_Execution_DAG_rev-5.6.json ../../skills/execute-stage1-rev56/SKILL.md ../../Stage1_Instances/THM-M-1431/IntakeProbe.lean` | 0 | hashes agree with the structured environment fingerprint |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1431/IntakeProbe.lean` | 0 | nine adjacent pinned complex, iteration, range, boundedness, connectedness, preconnectedness, and compactness interfaces elaborated; no target theorem was stated |
| `cd Formalizations/Lean && rg -n -i --glob '*.lean' -e '\bdouady\b' -e '\bhubbard\b' -e '\bmandelbrot\b' -e 'filled[ -]?julia' -e 'b[öo]ttcher' -e 'complex[ -]dynam' -e 'quadratic[ -]family' -e 'quadratic[ -]dynam' .lake/packages/mathlib/Mathlib` | 0 | one unrelated Hubbard-and-West ODE bibliography line matched; no queried complex-dynamics target was identified; discovery-only evidence, not an anchor audit |
| `python3 Stage1_Instances/THM-M-1431/check_intake.py` | 1 | known intake-only checker failure: the integration base does not retain the intake worker's root self-test manifest; after these files are added its closed intake artifact inventory is also stale; intake evidence was not rewritten to manufacture agreement |
| `python3 -m json.tool Stage1_Instances/THM-M-1431/statement-blocker.json` and the recorded scoped `jq -e` assertion | 0 | blocker identity, null target, four undefined mutation classes, unchanged debt vector, false completion flags, exact changed paths, and no-self-test boundary agree |
| `rg -n --glob '*.lean' -e '\bsorry\b' -e '\badmit\b' -e '\bsorryAx\b' -e '^[[:space:]]*axiom\b' -e '^[[:space:]]*constant\b' -e '^[[:space:]]*opaque\b' -e '^[[:space:]]*unsafe\b' Stage1_Instances/THM-M-1431` | 1 | expected no-match exit; no prohibited proof escape or declaration was found |
| `git diff --check -- Stage1_Instances/THM-M-1431` plus the recorded per-file `git diff --no-index --check` loop | 0 | no tracked or added-file whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | no self-test manifest exists because the exact-statement deliverable is blocked |

The statement run does not rewrite the intake instance, receipt, checker, task DAG, historical
hashes, generated blueprint, or authoritative execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

Accountable reviewers must preserve and hash an immutable primary edition, identify and transcribe the exact
theorem or corollary and every incorporated definition with pinpoint locators, audit the French or
translated text, proof boundary, corrections and errata, reconcile `THM-M-1431` with duplicate
`THM-M-0261` without borrowing evidence by assumption, and obtain independent approval of the
source-statement mapping. The accepted statement must freeze the quadratic normalization, critical
orbit and indexing, boundedness or non-escape predicate, parameter set, topology and connectedness
convention, ordered binders, hypotheses, conclusion, boundary cases, and every credited alternate
form.

A later statement worker can then encode that same claim with real Lean definitions, minimize its
pinned imports, serialize and hash the elaborated expression and environment, compile every
credited transport, and run all four required mutation classes. Master acceptance of the intake
must also occur before an eventual accepted statement transition, but need not precede worker
retry.

The first failed gate is exact source-statement identity. Pending intake acceptance is a separate
acceptance boundary, not the cause of this blocked attempt. This blocker is the assigned phase's
truthful result, not completion of the statement node or any downstream node. Lifecycle remains
`planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the phase is not genuinely
self-tested to its completion gate, no `.stage1-worker-selftest.json` is emitted and no statement
receipt, worker `[_]`, or master acceptance is claimed.
