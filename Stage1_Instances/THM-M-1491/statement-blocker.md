# THM-M-1491 exact-statement gate: blocked

- Item: `S56-M-1491-STATEMENT`
- Base revision: `e179b2be594419aa5fb33c3862f73491fdaf113e` (tree
  `8c1da8dad4712804811f550b583129e7b73effdc`)
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## First failed gate

The exact-statement gate in section 5.1 of `Docs/Stage1_Blueprint_rev-5.6.md` cannot be
truthfully entered from the authoritative record. The mathematics catalog supplies only the title
"convex optimization," the collective attribution "many mathematicians," the twentieth century,
and the gloss "optimization of convex functions." It gives no citation or truth-valued
proposition, domain, objective or constraint model, ordered binders, hypotheses, conclusion, or
boundary cases. Stage0 explicitly leaves the precise definitions, premises, formal target,
equivalent forms, axioms, machine status, and artifacts open. The catalog's `已验证` value is
untrusted metadata under rev-5.6.

The wording identifies a field and activity family, not one theorem. It does not select problem
structure, minimizer existence or uniqueness, local-to-global optimality, first- or second-order
conditions, KKT conditions, duality, sensitivity, an algorithm, convergence, rate, or complexity.
Those alternatives require materially different spaces, objective codomains, feasible-set and
constraint encodings, assumptions, binders, conclusions, and degenerate cases. Choosing one from
mathematical familiarity would invent, narrow, broaden, or substitute proposition-changing
mathematics rather than elaborate the received target.

Boyd and Vandenberghe's 2004 *Convex Optimization*, Chapter 4, is an inspected authoritative
modern source lead only. It separately defines a standard-form convex problem and proves a
local-to-global optimum result. The catalog does not cite the book or choose that result. No
immutable proposition and complete definition/assumption/proof/correction crosswalk has been
admitted, and no independent source and convex-optimization review has approved target identity.

Consequently there is no canonical expression to elaborate, no honest minimal-import claim, and
no canonical expression or environment fingerprint. Checked transports and the required removed-
hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are undefined until
a source-correct proposition fixes the binders and premises. The intake vector remains
`[H5, M4, R4]`; no debt change is proposed. No `Statement.lean`, theorem declaration, axiom,
placeholder, stored desired property, or substituted theorem was introduced.

The intake prerequisite is only provisional `[_]`, and its worker receipt is unaccepted and not
content-addressed. Its recorded blueprint and execution-DAG hashes are older than the current
authority, and its historical checker expects intake `[ ]` with zero attempts rather than the
integrated `[_]` with one attempt. This independently prevents statement-node acceptance. This
phase records rather than rewrites stale intake evidence. The first statement-specific failure
remains the absent exact source proposition.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. Its sole import,
`Mathlib.Analysis.Convex.Extrema`, exposes `ConvexOn`, `IsLocalMinOn`, `IsMinOn`, and two checked
local-to-global extrema theorems. All five `#check` commands and both axiom reports passed, but the
probe defines no convex-optimization problem, catalog-selected theorem, checked transport, or
proof body. The imported theorems are one possible narrowing only. The import therefore cannot be
certified minimal for an unidentified target and receives no statement, anchor, or proof credit.

A bounded exact-topic search over the owned, repo-local, and pinned-mathlib Lean roots found only a
Boyd-Vandenberghe bibliography reference in a convex-cone source file. It located no source-
identical convex-optimization target declaration. This is narrow statement-feasibility evidence,
not the downstream immutable anchor audit or a global absence claim.

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
| `python3 scripts/stage1_target.py show THM-M-1491` | 0 | rank 1168, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `python3 -B Stage1_Instances/THM-M-1491/check_intake.py` | 1 | historical intake replay reached its frozen `[ ]`/zero-attempt assertion; current authority records provisional `[_]`/one attempt |
| `cd Formalizations/Lean && lake env lean --version` and `lake --version` | 0 | Lean and Lake agree with the pinned environment above |
| mathlib revision/tree and package-status checks | 0 | revision and tree agree with the fingerprint; package worktree is clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-1491/IntakeProbe.lean` | 0 | five adjacent APIs and two axiom reports elaborated; stdout SHA-256 `589ef4ec6608e2a8dd844edc729b2a2b4884bbc4125827304367713c6024ffc6`; no canonical target was stated |
| bounded exact-topic search recorded in `statement-blocker.json` | 0 | only one bibliography reference matched; no source-identical target declaration was found |
| prohibited Lean construct scan over owned `*.lean` files | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, or unsafe declaration |
| scoped `jq -e` invariant recorded in `statement-blocker.json` | 0 | identity, null target, undefined mutations, unchanged debt, false completion flags, exact two-file scope, and remaining workflow phases agree |
| `git diff --check` plus one `git diff --no-index --check` per added blocker file | 0 / 1 expected | no whitespace diagnostic; exit 1 from each no-index check records only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test manifest exists because the exact-statement deliverable is blocked |

## Retry condition

The integration lane must first revalidate and master-accept refreshed intake evidence.
Accountable reviewers must then preserve and hash one immutable primary or approved authoritative
source, select and transcribe one exact truth-valued convex-optimization proposition with pinpoint
locators, audit corrections and errata, reconcile neighboring-target ownership, and independently
approve the source-to-statement mapping. The decision must freeze the optimization orientation and
model; spaces and typeclass assumptions; objective and constraint functions; feasible-set and
optimum representation; ordered binders, hypotheses, and conclusion; alternate encodings; and all
empty, infeasible, unbounded, unattained, nonunique, boundary, zero-dimensional, arithmetic, and
algorithmic cases that apply.

A later statement worker can then encode precisely that claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and run all four required mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node.
`audit_complete` and `theorem_complete` remain false. Because the assigned phase is not genuinely
self-tested to its completion gate, no `.stage1-worker-selftest.json`, node receipt, worker `[_]`,
or master acceptance is claimed.
