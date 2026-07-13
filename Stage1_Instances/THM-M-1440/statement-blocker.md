# Exact-statement gate: blocked

Item: `S56-M-1440-STATEMENT`

Theorem: `THM-M-1440`

Base revision: `1944ddb6f503b699293e82f18d19efe0f32b4380` (tree
`e5004bc50d7e6fae75e8332fb00748a57e3bf622`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1440-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Rev-5.6 section 10.2 permits this assigned statement
attempt while concurrent preparation is enabled, but dependency-ordered master closure still
requires intake acceptance. The intake receipt is provisional, has `accepted: false`, and is stale
against the current blueprint and execution DAG. This run records that boundary instead of
rewriting historical intake evidence.

Independently and decisively, the repository does not identify an exact mathematical statement to
elaborate. Its entire claim is the method label `牛顿迭代法` and the gloss `方程求根的二次收敛方法`
("a quadratically convergent method for finding roots of equations"). It supplies no bibliography,
theorem locator, formula, ordered binders, assumptions, conclusion, proof boundary, corrections,
or independent review. The catalog status `已验证` is untrusted metadata under rev-5.6.

That wording is not one truth-valued proposition. It does not choose a real, complex,
finite-dimensional, or Banach-space carrier; scalar or Frechet derivative; function class; root
and simplicity or derivative-invertibility premise; Newton update and inverse convention; initial
neighborhood; invariant domain and well-defined iterates; convergence definition; one-step error
bound, Q-order-two, asymptotic-ratio, big-O, complexity, or solver-correctness conclusion; or exact
versus finite-precision arithmetic. These choices produce inequivalent theorems.

The ambiguity affects truth, not presentation. For `f(x) = x^2` at its multiple root zero, every
nonzero classical Newton iterate is divided by two, so its convergence is linear rather than
quadratic. The classical field update is also undefined when an iterate has zero derivative.
Silently choosing a simple-root local real theorem, a `C^2` error-bound theorem, a complex theorem,
a Newton-Kantorovich theorem, or a polynomial algebra theorem would invent or substitute the
missing mathematics. Newton optimization is separately owned by `THM-M-1500`; secant, bisection,
generic fixed-point iteration, and Banach fixed-point results are separately owned by
`THM-M-1441` through `THM-M-1444`.

Rev-5.6 sections 5 and 5.1 make statement ambiguity and a missing expression fingerprint hard
blockers. Without a source-selected proposition, there is no exact Lean expression whose imports
can be certified minimal, no canonical elaborated expression or environment-expression
fingerprint, no approved alternate encoding, and no meaningful removed-hypothesis,
changed-domain, changed-binder-scope, or boundary-case mutation suite. Those mutation results are
undefined, not passed. No surrogate theorem, broadened interface, special case, axiom,
placeholder, or proof body was added.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` was re-elaborated through the pinned environment
with the sole direct import `Mathlib.Dynamics.Newton`. Nine polynomial Newton-map,
root/fixed-point, and nilpotent interfaces elaborate. In particular, pinned mathlib defines a
polynomial `newtonMap` over commutative rings, uses a junk value at nonunit derivative values, and
proves fixed-point and nilpotent divisibility results. It does not state the absent analytic
quadratic-convergence target. A bounded repo-local and pinned-mathlib search found no Lean source
using the analytic quadratic-convergence or Q-order terminology.

The probe therefore authenticates adjacent substrate only. It states no canonical theorem,
contains no proof body, supplies no source transport, and cannot make its import minimal for an
unknown target. Its successful elaboration supplies no statement, anchor, or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, dependency clone, fetch,
or other `.lake` mutation was performed.

## Validation Evidence

Commands ran in this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1440` | 0 | rank 1119, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; the recorded base revision and tree were otherwise clean |
| source record, Stage0, manifest, blueprint, and intake dossier inspection | 0 | only the method label and gloss exist; intake leaves the canonical claim and formal target null and lists proposition-changing choices |
| `cd Formalizations/Lean && lake env lean --version`; `lake --version` | 0 | the pinned Lean and Lake versions above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short`; revision/tree inspection | 0 | the package worktree was clean and its pinned revision and tree matched |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1440/IntakeProbe.lean` | 0 | nine adjacent polynomial Newton APIs elaborated; complete stdout SHA-256 `79f36073ebd39e01c2c95fc5bf2d9e4d3f1ce23585587be71c1363deb4be3b57` |
| bounded analytic quadratic-convergence terminology search in repo-local and pinned-mathlib Lean | 1 | expected no-match exit; discovery only, not a downstream anchor audit or global absence claim |
| `python3 -B Stage1_Instances/THM-M-1440/check_intake.py` before blocker artifacts were added | 1 | historical intake replay stopped on a stale blueprint input hash; its closed intake inventory would also reject later-phase artifacts |
| structured JSON parsing and blocker invariant assertions | 0 | item identity, blocked state, null target and imports, four undefined mutations, unchanged debt, false completion flags, exact changed paths, and absent self-test agreed |
| prohibited Lean construct scan and tracked/added-file whitespace checks | 0 | expected no-match and expected new-file-difference statuses were handled; no prohibited declaration or whitespace diagnostic |
| `test ! -e .stage1-worker-selftest.json` | 0 | the self-test manifest is absent because the exact-statement deliverable did not pass |

The historical `check_intake.py` is intake-only evidence. This statement attempt does not mutate
its frozen hashes, expected artifact inventory, receipt, task DAG, or the authoritative checklist
to manufacture a pass.

## Retry Condition And Status Boundary

The integration lane must revalidate and master-accept the intake dependency before accepting a
later statement transition. Accountable reviewers must preserve and hash an immutable primary or
approved authoritative source edition, select one exact theorem and page locator, transcribe every
incorporated definition, ordered binder, hypothesis, conclusion, proof boundary, correction,
erratum, and boundary case, and independently approve the mapping. They must explicitly settle the
carrier, function and derivative class, root nondegeneracy, update convention, neighborhood and
iterate well-definedness, convergence and rate notions, constants and quantifier order,
arithmetic model, and separation from the neighboring targets.

A later statement worker can then encode precisely that approved claim, minimize pinned imports,
serialize and hash its elaborated expression and environment, compile each credited transport,
and run all four required mutation classes.

The first failed gate is exact source-statement identity. The root remains `[H5, M4, R4]`, with
`audit_complete: false` and `theorem_complete: false`; no debt-vector change is proposed. This is
blocked-attempt evidence, not completion of the statement node or any downstream node. Because the
assigned phase did not pass its completion gate, no `.stage1-worker-selftest.json`, statement
receipt, worker `[_]`, or master acceptance is claimed.
