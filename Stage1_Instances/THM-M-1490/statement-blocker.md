# THM-M-1490 exact-statement gate: blocked

- Item: `S56-M-1490-STATEMENT`
- Base revision: `d1b510bacab792f84a99231485cf4429fdb78978` (tree
  `f77c4e4db196fc0ecc271815514a411d06ea6053`)
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## First failed gate

The exact-statement gate in section 5.1 of `Docs/Stage1_Blueprint_rev-5.6.md` cannot be
truthfully entered from the authoritative record. The mathematics catalog supplies only the title
"optimization theory," the collective attribution "many mathematicians," the twentieth century,
and the gloss "the theory of mathematical optimization." It gives no citation or truth-valued
proposition, objective, domain, feasible-set or constraint model, ordered binders, hypotheses,
conclusion, or boundary cases. Stage0 explicitly leaves the precise definitions, premises, formal
target, equivalent forms, axioms, machine status, and artifacts open. The catalog's `已验证` value
is untrusted metadata under rev-5.6.

The wording identifies a field, not one theorem. It does not select minimizer existence or
attainment, uniqueness, a necessary or sufficient optimality condition, local-to-global
optimality, weak or strong duality, sensitivity, an algorithm, convergence, rate, or complexity.
Those alternatives require materially different spaces, objectives, feasible-set and constraint
encodings, assumptions, binders, conclusions, computation policies, and degenerate cases. Choosing
one from mathematical familiarity would invent, narrow, broaden, or substitute
proposition-changing mathematics rather than elaborate the received target. The neighboring
targets `THM-M-1491` through `THM-M-1509` also separately own convex, linear, conic and semidefinite
optimization, named algorithms, KKT, duality, saddle points, and minimax.

Consequently there is no canonical expression to elaborate, no honest minimal-import claim, and
no canonical expression or environment fingerprint. Checked transports and the required removed-
hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are undefined until
a source-correct proposition fixes the binders and premises. The intake vector remains
`[H5, M4, R4]`; no debt change is proposed. `H5` classifies the received field label, not correctly
stated optimization theorems. No `Statement.lean`, theorem declaration, axiom, placeholder, stored
desired property, or substituted theorem was introduced.

The intake prerequisite is only provisional `[_]`, and its worker receipt is unaccepted and not
content-addressed. Its recorded blueprint and execution-DAG hashes are older than the current
authority, and its historical checker expects intake `[ ]` with zero attempts rather than the
integrated `[_]` with one attempt. This independently prevents statement-node acceptance. This
phase records rather than rewrites stale intake evidence. The first statement-specific failure
remains the absent exact source proposition.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. Its two imports,
`Mathlib.Analysis.Convex.Extrema` and `Mathlib.Topology.Order.Compact`, expose compact-domain
minimizer existence, convex local-to-global optimality, and strict-convexity uniqueness. All six
`#check` commands and three axiom reports passed, but these are inequivalent candidate theorem
families. The probe defines no optimization model, catalog-selected theorem, checked transport, or
proof body. Its imports therefore cannot be certified minimal for an unidentified target and
receive no statement, anchor, or proof credit.

A bounded exact-topic search over the owned, repo-local, and pinned-mathlib Lean roots returned no
match and located no source-identical optimization-theory target declaration. This is narrow
statement-feasibility evidence, not the downstream immutable anchor audit or a global absence
claim.

The environment is Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided
`Formalizations/Lean/.lake` symlink points to the canonical pinned artifacts and was used read-only.
No `lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai), from the repository root unless a
different working directory is shown. Exact argument arrays and results are preserved in
`statement-blocker.json`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1490` | 0 | rank 1167, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `python3 -B Stage1_Instances/THM-M-1490/check_intake.py` | 1 | historical intake replay reached its frozen `[ ]`/zero-attempt assertion; current authority records provisional `[_]`/one attempt |
| `cd Formalizations/Lean && lake env lean --version` and `lake --version` | 0 | Lean and Lake agree with the pinned environment above |
| mathlib revision/tree and package-status checks | 0 | revision and tree agree with the fingerprint; package worktree is clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-1490/IntakeProbe.lean` | 0 | six adjacent APIs and three axiom reports elaborated; stdout SHA-256 `c2753a35cefe4d2af1f85ee062d1a98b3d1d1d60ead60ceec169cfbb698f2a3d`; no canonical target was stated |
| bounded exact-topic search recorded in `statement-blocker.json` | 1 | expected no-match: no source-identical target declaration was found |
| prohibited Lean construct scan over owned `*.lean` files | 1 | expected no-match: no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, or unsafe declaration |
| scoped `jq -e` invariant recorded in `statement-blocker.json` | 0 | identity, null target, undefined mutations, unchanged debt, false completion flags, exact two-file scope, and remaining workflow phases agree |
| `git diff --check` plus one `git diff --no-index --check` per added blocker file | 0 / 1 expected | no whitespace diagnostic; exit 1 from each no-index check records only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test manifest exists because the exact-statement deliverable is blocked |

## Retry condition

The integration lane must first revalidate and master-accept refreshed intake evidence.
Accountable reviewers must then preserve and hash one immutable primary or approved authoritative
source, select and transcribe one exact truth-valued optimization proposition with pinpoint
locators, audit corrections and errata, reconcile neighboring-target ownership, and independently
approve the source-to-statement mapping. The decision must freeze the optimization orientation and
claim family; spaces and typeclass assumptions; objective and constraint functions; feasible-set
and solution representation; ordered binders, hypotheses, and conclusion; algorithm and arithmetic
semantics if applicable; alternate encodings; and all empty, infeasible, unbounded, unattained,
nonunique, boundary, zero-dimensional, oracle, stopping, and computation cases that apply.

A later statement worker can then encode precisely that claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and run all four required mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node.
`audit_complete` and `theorem_complete` remain false. Because the assigned phase is not genuinely
self-tested to its completion gate, no `.stage1-worker-selftest.json`, node receipt, worker `[_]`,
or master acceptance is claimed.
