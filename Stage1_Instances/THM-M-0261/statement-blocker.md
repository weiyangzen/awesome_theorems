# Exact-statement gate: blocked

Item: `S56-M-0261-STATEMENT`

Theorem: `THM-M-0261`

Base revision: `c2e294becadae6ce784f27ee69f2e8dbf57e0b30` (tree
`3f567e7f76b189432b73444354070c0ff75925b9`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0261-INTAKE` has provisional worker
state `[_]`, which permits this statement attempt, but the exact Lean 4 target cannot be truthfully
frozen from the authoritative record. The catalog supplies only the title `曼德博集合连通性`,
Adrien Douady and John Hubbard, the year 1982, and the gloss `Mandelbrot集的连通性`
("connectedness of the Mandelbrot set"). It supplies no publication, exact passage, incorporated
definitions, ordered binders, hypotheses, proof boundary, corrections, errata, or formal artifact.
The catalog status `已验证` ("verified") is explicitly untrusted under rev-5.6.

The intake identifies the 1982 C. R. note and the expanded Orsay notes, Chapter 8, Theorem 8.1 and
Corollary 8.3(a), as strong primary-source candidates. They have not been admitted as an immutable
edition with an independently approved definition chain, translation, corrections, and errata.
The repository also schedules the exact metadata duplicate `THM-M-1431`; no authority has
reconciled the two target identities or assigned source and evidence ownership between them.

Several proposition-changing choices therefore remain open:

- whether the Mandelbrot locus is defined by boundedness of the critical orbit, non-escape to
  infinity, membership of `0` in a filled Julia set, or connectedness of that filled Julia set,
  and which checked transports relate credited forms;
- whether the orbit starts at `0` or its first value `c`, whether iterate zero is included, and
  whether boundedness uses `Bornology.IsBounded`, a uniform norm bound, an escape-radius condition,
  or a filter formulation;
- whether the root uses `IsConnected` or separately composes nonemptiness with `IsPreconnected`,
  and whether the ambient space is `Complex` or a compactification;
- how `c = 0`, the cusp `c = 1/4`, boundary parameters, escape-radius equality, empty-set
  conventions, and the filled-Julia and conformal-complement routes are treated.

Selecting the familiar bounded-critical-orbit formulation would be plausible mathematics, but it
would still resolve choices that this target's intake deliberately left open. A filled-Julia,
conformal-complement, compactness, path-connectedness, or local-connectedness claim would instead
substitute or strengthen the requested root. Section 5 of the rev-5.6 blueprint makes statement
ambiguity and a missing expression fingerprint hard blockers. There is consequently no canonical
expression on which to certify checked alternate transports or removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations. Those mutation classes are undefined, not
passed. The first failed substantive gate is exact source-statement identity, and the root remains
`[H1, M4, R3]`.

Master acceptance of the intake is still required before an accepted statement transition, but it
is separate from this substantive failure. The provisional predecessor allowed the attempt; it
did not supply the missing canonical claim.

## Pinned Lean Boundary

This is a policy blocker, not a claim that Lean lacks the necessary vocabulary. The existing
`IntakeProbe.lean` imports `Mathlib.Analysis.Complex.Basic`,
`Mathlib.Logic.Function.Iterate`, `Mathlib.Topology.MetricSpace.Bounded`, and
`Mathlib.Topology.Separation.Connected`. It re-elaborates representative complex-number,
iteration, range, boundedness, connectedness, preconnectedness, and compactness interfaces. It
states no proposition for `THM-M-0261`; its imports are discovery candidates only and cannot be
certified as the imports of an unresolved target.

A bounded source-name search of pinned mathlib and repo-local Lean identified no Douady-Hubbard,
Mandelbrot, filled-Julia, Bottcher, or queried complex-dynamics declaration. The only output was an
unrelated bibliography line containing the surname Hubbard. This is narrow feasibility evidence,
not the downstream immutable anchor audit and not a global absence claim.

The intake records `girving/ray` at immutable revision
`0ca7b1e746b2911557ac76f56259068cfd1423ab`, whose `Ray/Mandelbrot.lean` defines a non-escape
locus and declares its connectedness under Lean `v4.27.0-rc1` and mathlib
`725c803ee924f55342e93f2c75976051ab902b54`. That source is outside this repository's dependency
closure, was not fetched or built in this phase, and has not passed this target's source-statement
mapping or downstream anchor audit. It receives no statement or proof credit here.

The local pinned environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The SHA-256 values of `lean-toolchain`,
`lake-manifest.json`, and `IntakeProbe.lean` are, respectively,
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`,
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`, and
`58228ccd4c0d38da1ec36f62239a0558dc31f659147b2e7ad952e8eb7c869368`.

The worker clone's pre-existing `Formalizations/Lean/.lake` link points to canonical pinned
artifacts and was used read-only. No `lake update`, `lake build`, dependency clone or fetch, or
other `.lake` mutation was run.

## Validation Evidence

Commands ran in this isolated worker clone on 2026-07-13 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0261` | 0 | rank 1269, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all && git rev-parse HEAD && git rev-parse HEAD^{tree}` | 0 | before statement edits, only the pre-existing untracked `.lake` link was present; base revision and tree are recorded above |
| bounded catalog, Stage0, manifest, blueprint, intake, and duplicate-boundary inspection | 0 | the repository supplies only the connectedness gloss; exact definitions, canonical claim, and Lean target remain open; `THM-M-1431` is an unreconciled duplicate |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 and Lake 5.0.0 at the revisions above |
| `cd Formalizations/Lean && git -C .lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}' && git -C .lake/packages/mathlib status --short` | 0 | pinned mathlib revision and tree recorded above; empty status output confirms the package worktree is clean |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json ../../Docs/Stage1_Targets_rev-5.6.json ../../Docs/Stage1_Blueprint_rev-5.6.md ../../Docs/Stage1_Execution_DAG_rev-5.6.json ../../skills/execute-stage1-rev56/SKILL.md ../../Stage1_Instances/THM-M-0261/IntakeProbe.lean` | 0 | toolchain, dependency lock, target manifest, blueprint, execution DAG, skill, and probe hashes were recorded in the structured blocker |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0261/IntakeProbe.lean` | 0 | eleven adjacent pinned interfaces elaborated; no target theorem was stated |
| bounded exact-topic `rg` under pinned mathlib and repo-local Lean | 0 | one unrelated Hubbard-and-West bibliography line matched; no queried complex-dynamics declaration was identified; discovery only |
| `python3 -B Stage1_Instances/THM-M-0261/check_intake.py` | 1 | known intake-only replay failure: the integration base omits the intake worker's root self-test manifest; statement evidence was not rewritten to manufacture agreement |
| `python3 -m json.tool Stage1_Instances/THM-M-0261/statement-blocker.json` and the recorded scoped `jq -e` assertion | 0 | blocker identity, null target, four undefined mutation classes, unchanged debt vector, false completion flags, exact changed paths, and no-self-test boundary agree |
| prohibited Lean proof-escape scan over `Stage1_Instances/THM-M-0261` | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom, bodyless constant, opaque, or unsafe declaration was found |
| `git diff --check -- Stage1_Instances/THM-M-0261` plus per-added-file no-index checks | 0 | no tracked or added-file whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test manifest exists because the exact-statement deliverable is blocked |

The statement run does not rewrite the intake instance, receipt, checker, task DAG, historical
hashes, generated blueprint, or authoritative execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

Accountable reviewers must preserve and hash an immutable primary edition; identify and transcribe
the exact theorem or corollary and every incorporated definition with pinpoint locators; audit the
French or translated text, proof boundary, corrections, and errata; reconcile `THM-M-0261` with
duplicate `THM-M-1431` without borrowing evidence by assumption; and independently approve the
source-statement mapping. The accepted statement must freeze the quadratic normalization, critical
orbit and indexing, boundedness or non-escape predicate, parameter set, topology, connectedness
convention, ordered binders, hypotheses, conclusion, boundary cases, and every credited alternate
form.

A later statement worker can then encode that same claim with real Lean definitions, minimize its
pinned imports, serialize and hash the elaborated expression and environment, compile every
credited transport, and run all four required mutation classes. Master acceptance of the intake
must also occur before an eventual accepted statement transition, but need not precede worker
retry.

The first failed gate is exact source-statement identity. This blocker is the assigned phase's
truthful result, not completion of the statement node or any downstream node. Lifecycle remains
`planned`; `audit_complete: false` and `theorem_complete: false`; no debt-vector change is
proposed. Because the assigned phase is not genuinely self-tested to its completion gate, no
`.stage1-worker-selftest.json` is emitted and no statement receipt, worker `[_]`, or master
acceptance is claimed.
