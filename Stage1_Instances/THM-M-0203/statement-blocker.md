# THM-M-0203 exact-statement gate: blocked

Item: `S56-M-0203-STATEMENT`

Base revision: `48abbb2d2eeb89816c5ffc0ad8faafa4b9d24dd0` (tree
`0f26e2c78fb5fff9277cbbdfef5e145fd4ef06f1`). Attempt date: 2026-07-13
(`Asia/Shanghai`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0203-INTAKE` is provisional worker state
`[_]`, not master-accepted state `[x]`. The intake receipt is unaccepted and non-content-addressed,
has no accepted receipt ID, and binds an earlier repository revision and authority hashes. Rev-5.6
permits this dependency-ordered provisional attempt, but master closure remains dependency ordered.

Independently and decisively, the exact-source-statement gate fails. The complete repository record
supplies the title `海伦公式` (Heron's formula), attributes it to Heron of Alexandria around 60 CE,
and glosses it only as `三角形面积与三边关系` (the relationship between a triangle's area and its
three sides). It supplies no formula, bibliography, exact source locator, area definition, triangle
or ambient-space model, ordered binders, side correspondence, nondegeneracy, proof boundary,
correction history, errata, or reviewer. Stage0 explicitly leaves the exact definitions and
premises, formal system, proof route, alternate forms, axioms, machine status, and artifacts open.
The catalog's `已验证` label is untrusted inventory metadata.

The intake deliberately leaves the canonical human claim and Lean target null. Its records identify
proposition-changing decisions that no admitted source has resolved:

- three Euclidean points versus abstract side lengths, and the ambient dimension and structures;
- nonnegative geometric area versus signed, absolute, determinant, measure, trigonometric, or
  squared-area encodings;
- ordered vertices, side names `a`, `b`, and `c`, the selected angle, and permutation transports;
- distinctness, noncollinearity, strict or weak triangle inequalities, and degenerate triangles;
- semiperimeter syntax, radicand nonnegativity, `Real.sqrt`, squared-versus-square-root form, and
  equality orientation; and
- repeated or collinear vertices, low-dimensional spaces, degenerate or nongeometric side triples,
  orientation reversal, higher-dimensional embeddings, and negative radicands.

Choosing the familiar square-root formula over abstract side lengths, a squared polynomial
identity, or a geometric-area formulation would supply clauses absent from the source. Choosing the
pinned `Theorems100.heron` interface would instead select its affine generality, trigonometric area
expression, two side-distinctness hypotheses, point order, and boundary behavior. Any choice would
invent, narrow, broaden, or substitute mathematics rather than elaborate the exact received target.

Rev-5.6 sections 5 and 5.1 make statement ambiguity and a missing expression fingerprint hard
blockers. There is no honest canonical Lean expression whose imports can be certified minimal. The
expression and environment fingerprints, checked alternate transports, and required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are undefined,
not passed. No `Statement.lean`, theorem declaration, proof body, weakened special case, broadened
interface, axiom, or placeholder was added. The vector remains `[H1, M3, R4]`.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates with the single direct import
`Mathlib.Geometry.Euclidean.Triangle`. It checks seven Euclidean triangle, angle, trigonometric, and
square-root APIs. The checks pass, but the probe defines no area, canonical target, source transport,
or proof body. Its import therefore cannot be certified minimal for an absent target and receives no
statement or proof credit.

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains
`Archive/Wiedijk100Theorems/HeronsFormula.lean`, whose sole direct import is the triangle module and
whose declaration `Theorems100.heron` states, for affine points `p1`, `p2`, and `p3` with
`p1 != p2` and `p3 != p2`, that

```text
1 / 2 * a * b * sin (angle p1 p2 p3)
  = Real.sqrt (s * (s - a) * (s - b) * (s - c)).
```

Here `a`, `b`, and `c` are the three ordered distances and `s = (a + b + c) / 2`. Direct
read-only elaboration of that exact pinned source succeeds. This proves candidate feasibility only.
The declaration is not an approved source-identical repository root, and the pinned build tree has
no Archive object or `HeronsFormula.olean`. No build was attempted.

A bounded exact-topic search found only that Archive source. This is discovery evidence, not the
downstream immutable anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided canonical `.lake` symlink was
used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation
was run. The pinned mathlib worktree remained clean.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0203` | 0 | rank 1535; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `git blame -L 1464,1469 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| authority, source, intake, toolchain, lockfile, and pinned Heron `sha256sum` checks | 0 | exact current hashes are preserved in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-0203/check_intake.py` | 1 | historical intake replay stops because it expects authoritative intake state `[ ]`, while integration now records provisional `[_]`; this phase records rather than rewrites that evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib `git rev-parse HEAD 'HEAD^{tree}' 'HEAD:Archive/Wiedijk100Theorems/HeronsFormula.lean'` and package status | 0 | pinned revision/tree and candidate blob match the structured record; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0203/IntakeProbe.lean` | 0 | seven adjacent APIs elaborated; stdout was 1,382 bytes with SHA-256 `a218873f6cd2dea54177d0dd19b472466406081626feecd7d4d8ba9213c2411a`; no canonical target or proof body |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean .lake/packages/mathlib/Archive/Wiedijk100Theorems/HeronsFormula.lean` | 0 | exact pinned candidate source elaborated; stdout was empty with SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`; candidate replay only |
| bounded exact-topic search over repository-local Lean, pinned `Mathlib`, and pinned `Archive` | 0 | only the Archive Heron source matched; no source-identical root was credited |
| pinned Archive build-object inspection | 0 | zero Archive build files and no prebuilt `HeronsFormula.olean`; no build attempted |
| prohibited-construct scan over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

The final JSON, invariant, input-hash, whitespace, scoped-change, and absent-self-test checks passed
after these two blocker artifacts were written. The historical intake checker is frozen to
intake-time state and authority inputs. This run records that limitation instead of rewriting the
intake checker, receipt, instance, task DAG, generated blueprint, or authoritative execution DAG to
manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must eventually master-accept refreshed intake evidence before accepting a
statement transition. Accountable reviewers must lawfully preserve and hash one immutable primary
or approved authoritative source, select and independently approve one exact proposition and proof
boundary, and map every incorporated definition, ordered binder, hypothesis, conclusion,
translation, correction, erratum, and attribution claim. They must freeze the area encoding,
triangle and ambient domain, universes and typeclasses, point order and side correspondence,
nondegeneracy, semiperimeter and square-root conventions, equality form, orientation, and every
boundary case.

A fresh statement worker can then encode precisely that reviewed claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport, and
execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof
credit, or master acceptance is claimed.
