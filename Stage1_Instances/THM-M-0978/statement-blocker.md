# Exact-statement gate: blocked

Item: `S56-M-0978-STATEMENT`

Theorem: `THM-M-0978`

Base revision: `48abbb2d2eeb89816c5ffc0ad8faafa4b9d24dd0` (tree
`0f26e2c78fb5fff9277cbbdfef5e145fd4ef06f1`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0978-INTAKE` has provisional state
`[_]`, not master-accepted state `[x]`. The intake receipt declares `accepted: false`, is not
content-addressed, has no accepted receipt ID, and deliberately leaves the canonical mathematical
claim and formal target null. Its historical checker also freezes the earlier open intake cursor
and therefore rejects the integrated `[_]` / one-attempt state. Dependency-ordered investigation
and this provisional statement attempt are permitted by rev-5.6 section 10.2. Any eventual master
closure of the statement remains dependency-ordered after intake acceptance or reconciliation.

Independently, the exact-statement gate cannot pass. The catalog supplies only the family name
"Hoeffding inequality," Wassily Hoeffding, the year 1963, and the gloss "concentration of sums of
bounded random variables." It gives no formula, source locator, definitions, ordered binders,
hypotheses, conclusion, proof boundary, corrections, reviewer, or boundary conventions. The
adjacent `verified` label is explicitly untrusted under rev-5.6.

The catalog also contains `THM-M-0994` under a Chinese transliteration of the same title, with the
same author, year, literal gloss, importance, and untrusted status. That target separately owns a
modern one-sided centered finite-family statement, proof artifacts, and historical wrappers.
Category placement and a legacy slot do not allocate the shared mathematics. No accepted identity,
distinct-root, merge, or evidence-sharing decision authorizes copying its proposition here.

The intake inspected Hoeffding's *Probability Inequalities for Sums of Bounded Random Variables*.
Theorem 2, printed page 6, equation (2.10), gives an upper-tail inequality for the average of
independent pointwise-bounded variables with `t > 0`; its proof is on printed pages 12-13. This is a
strong primary-source lead, not an approved canonical target. The inspected artifact is a May 1962
UNC mimeograph corresponding to the 1963 journal paper. Exact catalog theorem selection,
mimeograph/journal reconciliation, corrections and errata, lawful admission, complete source map,
duplicate allocation, modern transport, and independent review remain open.

The proposition-changing choices therefore remain open: Theorem 1, Theorem 2, or another source
result; initial-segment, nonempty, or arbitrary finite indexing; pointwise or almost-sure bounds;
average or centered-sum normalization; positive or nonnegative threshold; one-sided or two-sided
scope; strict or closed events; exponent algebra; and empty, zero-width, deterministic, endpoint,
and null-exception cases. Selecting a familiar formulation would invent, narrow, broaden, or
substitute mathematics rather than elaborate the exact received target.

Rev-5.6 sections 5 and 5.1 make statement ambiguity and a missing expression fingerprint hard
blockers. There is no honest canonical expression for which imports can be certified minimal, no
credited alternate encoding for a checked transport, and no canonical target against which the
required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations can
run. Those mutation results are undefined, not passed. The root vector remains `[H1, M3, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates with the direct import
`Mathlib.Probability.Moments.SubGaussian`. Eight exact-topic sub-Gaussian, independence,
Hoeffding-lemma, sum-tail, MGF, and CGF interfaces check successfully. The two representative axiom
reports contain `propext`, `Classical.choice`, and `Quot.sound`. The probe defines no canonical
target, source transport, mutation fixture, or proof body, so its import cannot be certified minimal
for an absent target.

A bounded search found the pinned exact-topic interfaces, the legacy Hoeffding wrappers, and the
separately owned `THM-M-0994` statement and proof artifacts. This is discovery-only evidence, not
the downstream immutable anchor audit or authority to transfer another target's statement.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, clone, fetch, or other
dependency mutation was run.

## Validation Record

Commands ran in this isolated worker clone on 2026-07-13 (`Asia/Shanghai`). Exact argv and result
summaries are retained in `statement-blocker.json`.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0978` | 0 | rank 1512; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| exact hashes and scoped inspection of authority, intake, source, lock, pinned source, and foreign-target inputs | 0 | all recorded hashes agree; the exact source proposition, duplicate allocation, formal target, imports, expression fingerprint, and mutations remain unresolved |
| `python3 -B Stage1_Instances/THM-M-0978/check_intake.py` | 1 expected | the historical checker stops because it requires intake `[ ]` / attempts 0 while integration records provisional `[_]` / attempts 1; static inspection shows it also freezes older authority inputs, and it was not rewritten or represented as current statement evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib revision/tree and package status | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0978/IntakeProbe.lean` | 0 | eight interfaces and two axiom reports elaborated; stdout SHA-256 `ea68b349a7c4befcf877dbbe1a6628dd9029af0ac9d3af8dd02106b9b5096790`; stderr empty |
| bounded sorted Hoeffding search | 0 | exact-topic candidates and foreign wrappers/statements located; output SHA-256 `0348f9e31a7bd86178adbd85af2282c6ec92bc32d47f1e383256e919bd64a645`; discovery only |
| scoped prohibited-construct search | 1 expected | no `sorry`, `admit`, `sorryAx`, `axiom`, bodyless `constant`, `opaque`, or `unsafe` declaration |
| JSON parse, scoped invariant and current-hash assertions, direct text checks, and the tracked/untracked diff-check wrapper | 0 each | the two blocker artifacts, current inputs, blocked boundary, and absent root self-test agree; each no-index check had its expected difference exit 1 and no whitespace diagnostic |

## Retry Condition And Status Boundary

The integration lane must resolve the `THM-M-0978` / `THM-M-0994` identity and ownership
allocation. Accountable reviewers must then lawfully preserve and hash one complete immutable
primary or approved authoritative source and
independently approve one exact proposition, every incorporated definition and premise, the proof
boundary and edition relationship, corrections and errata, transports, and all boundary cases.

A fresh statement worker can then encode only that reviewed claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and execute all four required mutation classes.

Eventual master closure of the statement remains dependency-ordered after intake acceptance or
reconciliation.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
