# Exact-statement gate: blocked

Item: `S56-M-0212-STATEMENT`

Theorem: `THM-M-0212`

Base revision: `b243ebc0f9058ba5afafef8240b92c2dfb2edc6e` (tree
`b4b092069141ac54ea1ab5a6ea946192a30ec78c`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0212-INTAKE` is only provisional worker
state `[_]`, not master-accepted state `[x]`; its receipt says `accepted: false`, is not content
addressed, and has no accepted receipt ID. Rev-5.6 permits dependency-ordered preparation from this
provisional predecessor, but master closure remains dependency ordered.

The exact-statement gate also fails independently. The repository supplies only the name
`布里昂雄定理` (Brianchon's theorem), Charles Julien Brianchon, the year 1806, and the gloss
`圆锥曲线外切六边形的共点性质`, or "the concurrency property of a hexagon circumscribed about a
conic." It supplies no bibliography, projective model, scalar field, conic or tangency definition,
ordered binders, hypotheses, exact conclusion, proof boundary, correction history, or boundary
convention. The `已验证` label is untrusted inventory metadata.

The standard forward reading uses six cyclically ordered tangent lines, constructs the six
adjacent-line intersections, and concludes that the three lines through opposite vertices are
concurrent. That reading still does not select:

- a synthetic projective plane, `P(K^3)`, or another model, and its field and characteristic;
- a smooth irreducible conic, a possibly singular quadratic zero locus, or another conic model;
- tangency through contact points, polarity, or intersection multiplicity;
- side and contact-point distinctness, cyclic order, and general-position assumptions;
- the contracts for forming vertices and the three opposite-vertex diagonals;
- concurrency as a common projective point, coordinate dependence, or a determinant equation;
- forward Brianchon, a dual Mobius specialization, a checked duality transport from Pascal, a
  converse, or an equivalence; or
- ideal intersections, repeated tangents or vertices, coincident diagonals, characteristic two,
  singular conics, and every other degenerate case.

The inspected Valles source lead works in the complex projective plane with a smooth conic and
obtains the `n = 3` dual Mobius result by polarity. The other inspected publisher abstract describes
the classical six-tangent configuration but studies a wider family of relabelings and Brianchon
points. The catalog cites neither source, and no independent reviewer has accepted either as its
exact proposition. Selecting one familiar formulation would therefore invent, narrow, broaden, or
substitute unresolved mathematics.

Rev-5.6 sections 5 and 5.1 make statement ambiguity, a null canonical expression, and a missing
expression fingerprint hard blockers. There is consequently no honest canonical declaration whose
imports can be certified minimal. No `Statement.lean`, expression fingerprint, checked transport,
or mutation suite was created. The removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations are undefined, not passed. The provisional vector remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates with four pinned imports:

```lean
import Mathlib.LinearAlgebra.Projectivization.Constructions
import Mathlib.LinearAlgebra.Projectivization.Independence
import Mathlib.LinearAlgebra.Projectivization.Subspace
import Mathlib.LinearAlgebra.QuadraticForm.Basic
```

Twelve projective, incidence, dependence, quadratic-form, and polar-form APIs elaborate.
`Projectivization.cross` totalizes equal inputs, and `Projectivization.orthogonal` is coordinate
dot-product incidence rather than an arbitrary conic polarity. The probe defines no source-selected
conic, tangency or polarity relation, projective concurrency predicate, canonical target, checked
transport, or proof body. Its imports are adjacent-substrate imports only and cannot be certified
minimal for an absent target. Exact one-line deletion checks show all four imports are necessary for
the twelve API checks, but that probe-only minimality gives no target-import credit.

A bounded exact-topic search found no Brianchon, circumscribed-hexagon, or tangent-hexagon Lean
declaration in pinned mathlib or repository-local Lean. This is discovery-only evidence, not the
downstream immutable anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was reused read-only. No update, build, clone, fetch, or other
dependency mutation was run, and the pinned mathlib worktree remained clean.

## Validation Record

Commands ran on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0212` | 0 | rank 1541; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| catalog, Stage0, blueprint, skill, target manifest, execution DAG, and intake dossier inspection | 0 | confirmed the sparse gloss, proposition-changing choices, null canonical target, and provisional predecessor |
| `sha256sum` over authorities, intake artifacts, toolchain, lock, and imported mathlib sources | 0 | exact digests are recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision/tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0212/IntakeProbe.lean` | 0 | twelve adjacent APIs elaborated; stdout was 1,881 bytes with SHA-256 `49378727ad2a2a9561cddf8ec443dab52b1569d7c5e06a0e240c86751e631034`; no target or proof body |
| exact one-line deletion of each of the four probe imports, followed by `lake env lean` | aggregate 0 | all four deletion variants failed on their corresponding API checks; this establishes minimality only for the discovery probe and gives no target-import credit |
| bounded exact-topic `rg` search over pinned mathlib and repository-local Lean | 1 (expected no match) | no target-specific declaration matched |
| `python3 -B Stage1_Instances/THM-M-0212/check_intake.py` | 1 | the historical intake checker expects its original authoritative intake row `[ ]` with zero attempts; the integrated DAG now records provisional `[_]` with one attempt, and this worker did not rewrite intake evidence |
| prohibited-declaration scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, bodyless `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0212/statement-blocker.json` plus scoped blocker-invariant and recorded-hash checks | 0 | identity, current base, dependency, null target/imports, unchanged vector, undefined mutations, false completion fields, exact scope, hashes, and absent self-test agree |
| scoped `git diff --check` and per-new-file no-index checks | 0 aggregate | no whitespace diagnostics; each no-index exit 1 was only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest is absent because the exact-statement deliverable did not pass |

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must then
preserve and hash one lawful immutable primary or authoritative source, select and independently
approve one exact proposition and proof boundary, and transcribe every incorporated definition,
ordered binder, hypothesis, conclusion, correction, erratum, side ordering, tangency and vertex
contract, diagonal pairing, concurrency convention, duality or converse boundary, and degenerate
case.

A fresh statement attempt may then encode precisely that approved claim, minimize pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport, and
run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion. Lifecycle remains `planned`;
`audit_complete: false` and `theorem_complete: false`; no debt change is proposed. Because the
exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt,
worker `[_]`, proof credit, or master acceptance is claimed.
