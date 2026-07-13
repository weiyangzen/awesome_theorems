# Exact-statement gate: blocked

Item: `S56-M-0976-STATEMENT`

Theorem: `THM-M-0976`

Base revision: `72e9e8092182121a6794921f61fcc9cae22f726d` (tree
`0d6c1fdf06d1573c256af331c6b198e5a787af43`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0976-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. The intake receipt declares `accepted: false`, has no
accepted receipt ID, and deliberately leaves the canonical mathematical statement, formal module,
Lean expression, expression hash, and canonical-target environment fingerprint null. Master
acceptance remains necessary before any eventual statement transition can be accepted.

Independently, the exact-statement gate cannot pass. The repository corpus repeats only the title
"McDiarmid inequality," the attribution Colin McDiarmid, the year 1989, and the gloss
`有界差函数的集中` ("concentration of bounded-difference functions"). It gives no bibliography,
formula, definition, theorem locator, ordered binders, hypotheses, constants, conclusion, proof
boundary, correction record, or reviewer. The catalog's `已验证` label is untrusted metadata under
rev-5.6 and supplies no statement or proof credit.

The intake identifies Colin McDiarmid's chapter "On the method of bounded differences," *Surveys
in Combinatorics, 1989*, pages 148-188, DOI `10.1017/CBO9781107359949.008`, as a credible source
lead. No lawful immutable full chapter, exact theorem passage, incorporated definition chain,
proof boundary, corrections or errata disposition, or independent review was admitted. The lead
therefore supports the provisional `H1` classification but does not select one proposition.

The proposition-changing choices remain open: the coordinate carriers and probability laws;
product-space versus common-space independence; the function's domain, codomain, measurability,
and integrability; pointwise versus almost-sure coordinate-replacement bounds; the sign and width
convention for each `c_i`; expectation, median, or other centering; upper, lower, or two-sided tail;
strict versus weak event inequalities; exponent normalization; ordered binders and coercions; and
empty-index, zero-sensitivity, zero-denominator, negative-threshold, and other boundary cases.
Selecting the familiar upper-tail formula
`P(f(X) - E[f(X)] >= t) <= exp(-2*t^2 / sum c_i^2)` would add mathematics absent from the admitted
record. An Azuma-Hoeffding, Hoeffding-sum, or Chernoff statement would instead substitute a
neighboring theorem.

Rev-5.6 sections 5 and 5.1 make statement ambiguity and a missing elaborated-expression fingerprint
hard blockers. There is no truthful canonical expression whose imports can be certified minimal,
no credited alternate encoding for a checked transport, and no canonical target against which the
required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations can
run. Those mutation results are undefined, not passed. The root vector remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates with these direct imports:

- `Mathlib.Probability.Independence.Basic`
- `Mathlib.Probability.Moments.SubGaussian`
- `Mathlib.Logic.Function.Basic`

It checks eight adjacent probability, independence, coordinate-update, integration, finite-sum,
and exponential APIs. The adjacent theorem
`ProbabilityTheory.HasSubgaussianMGF.measure_sum_ge_le_of_iIndepFun` is a centered finite-sum
Hoeffding interface, not a function-level McDiarmid statement. The probe declares no canonical
target, checked source transport, or proof body, so its imports cannot be certified minimal for the
absent target.

A bounded exact-topic search over repository-local Lean and pinned mathlib found no usable exact
McDiarmid declaration. It found the intake probe, the historical Hoeffding wrapper's explicit
McDiarmid exclusion, unrelated Neron-Tate and ring-theory uses of "bounded difference," and
martingale convergence results with bounded increments. This is discovery-only evidence, not the
later immutable anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, clone, fetch, or other
dependency mutation was run.

## Validation Record

Commands ran in this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0976` | 0 | rank 1510; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD`; `git rev-parse 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped catalog, Stage0, manifest, blueprint, skill, and intake inspection plus SHA-256 capture | 0 | confirmed the sparse catalog claim, unadmitted exact source, null canonical target, and open proposition-changing choices |
| `git blame` on all three catalog records | 0 | all 18 uncited lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib revision/tree queries and package status | 0 | revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0976/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; the adjacent sum theorem reported `[propext, Classical.choice, Quot.sound]`; stdout SHA-256 `bb6bde64a3e5db9190f8d848ba06ea051dc5161cca547de88a9d06e5f3136874`; empty stderr; no target or proof body |
| bounded `rg` search for McDiarmid and bounded-difference declarations | 0 | only unrelated or explicit non-target matches; no usable exact declaration located |
| `python3 -B Stage1_Instances/THM-M-0976/check_intake.py` | 1 | historical intake checker rejects its frozen `authoritative_blueprint_sha256` after integration updated shared authority; it is stale intake evidence and was not rewritten |
| scoped prohibited-construct scan over owned Lean files | 0 | inner search returned expected no-match; no prohibited proof declaration was found |

Final JSON, structured invariant, whitespace, and absent-self-test checks are recorded in the
structured blocker beside this report.

## Retry Condition And Status Boundary

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers must
lawfully preserve and hash a complete immutable primary or approved authoritative source, select
one exact proposition, and independently approve its incorporated definitions, ordered binders,
hypotheses, conclusion, proof boundary, corrections, errata, and every boundary case. They must
freeze the coordinate spaces and laws, independence encoding, function and regularity assumptions,
replacement relation, sensitivity constants, centering, event, exponent, coercions, and degenerate
cases.

A fresh statement worker can then encode precisely that reviewed claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
