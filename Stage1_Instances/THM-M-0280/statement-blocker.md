# Exact-statement gate: blocked

Item: `S56-M-0280-STATEMENT`

Theorem: `THM-M-0280`

Base revision: `a75b2f3ac5b8b7d34eb73435734edfeecc41bd40` (tree
`66a22e1dc2e1c14c27bd01396a99826ab2536bf1`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0280-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. The intake receipt declares `accepted: false`, is not
content-addressed, and has no accepted receipt ID. It deliberately leaves the canonical
mathematical statement, Lean module and expression, expression hash, and canonical-target
environment fingerprint null.

Independently, the exact source-statement gate fails. The entire repository record names
Minkowski's inequality, attributes it to Hermann Minkowski in 1896, and gives only the gloss
`L^p空间的三角不等式` (the triangle inequality in Lp space). It supplies no citation, formula,
incorporated definitions, ordered binders, hypotheses, conclusion, proof boundary, correction
history, or reviewer. Stage0 repeats the gloss while explicitly leaving precise definitions and
premises, alternate forms, axioms, and machine artifacts open. The catalog's `已验证` label is
untrusted metadata and gives neither source-identity nor kernel credit.

The gloss denotes a theorem family rather than one formal proposition. An exact root must decide
whether it is an integral formula for representative functions, an extended-valued `eLpNorm`
inequality, a real-valued `lpNorm` inequality, addition closure for `MemLp`, or the norm triangle
inequality on the almost-everywhere quotient `Lp`. It must also choose a real or `ENNReal`
exponent, the finite and infinity endpoints, the measure assumptions, scalar or vector codomain,
measurability or integrability premises, finite versus extended-infinite semantics, binder order,
and the treatment of representatives and null-set changes. These are proposition-changing choices,
not notation that Lean can infer.

No immutable primary or approved authoritative theorem passage, incorporated definition chain,
complete assumption and conclusion map, proof boundary, correction or errata disposition, or
independent review has been accepted. Selecting a familiar textbook formula or the most general
pinned declaration would therefore invent the missing source bridge. It could also silently replace
the requested general measure-space family with a finite-sum or sequence-space special case, or
confuse it with a different Minkowski namesake.

Rev-5.6 sections 5 and 5.1 make this ambiguity and the absent elaborated-expression fingerprint
hard blockers. There is consequently no honest canonical expression whose imports can be certified
minimal, no approved alternate encoding for a checked transport, and no canonical target against
which the required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case
mutations can run. Those mutations are undefined, not passed. The lifecycle remains `planned`, and
the root vector remains `[H1, M3, R4]`.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates with these three direct imports:

- `Mathlib.MeasureTheory.Function.LpSeminorm.LpNorm`
- `Mathlib.MeasureTheory.Function.LpSpace.Basic`
- `Mathlib.Analysis.MeanInequalities`

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, it authenticates five
nonidentical exact-topic interfaces:

- `MeasureTheory.eLpNorm_add_le`, for AE-strongly-measurable functions into an extended
  seminormed additive monoid, `p : ENNReal`, and `1 <= p`;
- `MeasureTheory.lpNorm_add_le`, for normed-group-valued functions, `MemLp f p mu`, and
  `1 <= p`;
- `MeasureTheory.Lp.instNormedAddCommGroup`, the quotient-`Lp` normed additive group under
  `Fact (1 <= p)`;
- `ENNReal.lintegral_Lp_add_le`, an explicit integral formula for a.e.-measurable
  `ENNReal`-valued functions and a real exponent `p >= 1`; and
- `Real.Lp_add_le`, a finite-sum real-valued specialization.

The four theorem declarations report exactly `propext`, `Classical.choice`, and `Quot.sound`.
This is real pinned elaboration of candidate interfaces, but the probe declares no canonical target,
checked source transport, statement mutation, or proof body. Its import set therefore cannot be
certified minimal for the absent target and supplies no statement, anchor-audit, or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symbolic link was used read-only. No `lake update`, `lake build`,
dependency clone or fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0280` | 0 | rank 1286; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree appear above |
| `git blame -L 2013,2018 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| exact `sha256sum` command recorded in `statement-blocker.json` | 0 | current authority, source, intake, toolchain, lockfile, probe, and five pinned candidate-source fingerprints were captured |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib `git rev-parse HEAD 'HEAD^{tree}'` and `git status --short` | 0 | pinned revision/tree recorded above; package source worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0280/IntakeProbe.lean` | 0 | five distinct candidate interfaces elaborated; four theorem reports showed the three axioms above; stdout SHA-256 `06295a3965083752673a8dc0ced2ed75c9919708deb3ff73b3c9f4f2d164d2cb` |
| exact bounded `rg` command recorded in `statement-blocker.json` | 0 | located the five candidate families and unrelated Minkowski namesakes; no source-identical root mapping was inferred |
| `python3 -B Stage1_Instances/THM-M-0280/check_intake.py` | 1 | historical intake checker rejected the integration-updated intake state; it is stale intake evidence, not statement evidence, and was not modified |
| exact scoped prohibited-declaration `rg` command recorded in `statement-blocker.json` | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration was found |
| `python3 -m json.tool Stage1_Instances/THM-M-0280/statement-blocker.json` and exact scoped Python assertion command recorded in `statement-blocker.json` | 0 / 0 | blocker identity, null target/imports, unchanged vector, four undefined mutations, false completion flags, two-file scope, and no-self-test boundary agree |
| `git diff --check -- Stage1_Instances/THM-M-0280` | 0 | no tracked whitespace diagnostics |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-0280/statement-blocker.json` | 1 (expected new-file difference) | empty diagnostic output; no whitespace error |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-0280/statement-blocker.md` | 1 (expected new-file difference) | empty diagnostic output; no whitespace error |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The intake checker freezes the intake-time authority hashes and original DAG state `[ ]`.
Integration has since recorded intake as `[_]`, so replay fails closed on that changed input. Adding
these statement artifacts also makes its original nine-file inventory historical. This run records
the limitation rather than rewriting intake evidence to manufacture agreement.

## Retry Condition And Status Boundary

Accountable reviewers must lawfully preserve and hash an immutable primary or approved
authoritative source, identify one exact theorem and every incorporated definition, map its ordered
binders, hypotheses, conclusion, proof boundary, correction, erratum, and boundary case, and
independently approve the mapping. They must select the representation, exponent and endpoint
regime, measure and codomain assumptions, measurability or integrability premises, finite or
extended semantics, quotient convention, and credited alternate forms. Refreshed intake evidence
must also receive master acceptance before an accepted statement transition.

A later statement worker can then encode only that reviewed claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and run all four mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. No `.stage1-worker-selftest.json`,
statement receipt, worker `[_]`, master acceptance, statement fingerprint, proof body, or proof
credit is claimed.
