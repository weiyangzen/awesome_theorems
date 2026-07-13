# Exact-statement gate: blocked

Item: `S56-M-0202-STATEMENT`

Theorem: `THM-M-0202`

Base revision: `dc600635160cace0916df5234bf8808c39dc656d` (tree
`8ee34b31ec38be1ef067aaab38c9a4cb4935b75a`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0202-INTAKE` is provisional worker
state `[_]`, not master-accepted state `[x]`; its receipt is explicitly unaccepted and has no
accepted receipt ID. Rev-5.6 section 10.2 permits dependency-ordered preparation of a later node,
but master closure remains dependency ordered.

Independently, the exact-statement gate fails. The complete repository record supplies only the
title `婆罗摩笈多公式` (Brahmagupta's formula), attribution to Brahmagupta, year 628, and the gloss
`圆内接四边形面积公式` (area formula for a cyclic quadrilateral). It gives no formula,
bibliography, source locator, incorporated definitions, ordered binders, hypotheses, conclusion,
proof boundary, correction history, or reviewer. Its `已验证` label is untrusted metadata under
rev-5.6.

The conventional modern family is

```text
s = (a + b + c + d) / 2,
K = sqrt ((s - a) * (s - b) * (s - c) * (s - d)).
```

That recognizable formula does not determine the received proposition. The repository does not
select an ordered quadrilateral object, ambient dimension, positive-radius circle or cyclicity
predicate, convexity and simplicity assumptions, consecutive-side correspondence, area encoding,
nondegeneracy, square-root versus squared equality, equality orientation, or treatment of repeated,
collinear, self-crossing, zero-area, and higher-dimensional cases. MathWorld corroborates only the
modern formula family. MacTutor records a material historical ambiguity: the attributed source may
not explicitly restrict the rule to cyclic quadrilaterals. Both are mutable secondary discovery
leads, not independently admitted immutable propositions.

These choices change the theorem. Selecting the familiar strictly convex planar square-root form,
an abstract side-length identity, a determinant or triangulated-area formulation, or a squared
polynomial equality would invent or substitute mathematics. Heron's formula, Bretschneider's
formula, Ptolemy's theorem, and the supplementary-opposite-angle relation cannot replace this
target without source-approved, kernel-checked transports.

Rev-5.6 sections 5 and 5.1 make statement ambiguity and a missing expression fingerprint hard
blockers. There is therefore no canonical expression whose imports can honestly be certified
minimal, no credited alternate encoding for a checked transport, and no canonical target against
which the required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case
mutations can run. Those mutation results are undefined, not passed. No `Statement.lean`, target
declaration, proof body, weakened special case, or broadened interface was added. The root remains
`[H1, M4, R4]`.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` was re-elaborated with its two direct imports:

- `Mathlib.Geometry.Euclidean.Angle.Sphere`
- `Mathlib.Geometry.Euclidean.Triangle`

It checks seven adjacent cospherical, concyclic, angle, triangle, and real-square-root interfaces.
All checks pass, with 1,411 bytes of stdout and SHA-256
`27e6b44e21e3e173ce8d372b69029611a1ab8bd8fb2a6f71483e8dc82e5102ef`. The probe declares no
ordered quadrilateral area, Brahmagupta target, transport, or proof body, so its imports cannot be
certified minimal for an absent canonical target.

A bounded exact-topic search over repo-local Lean and pinned mathlib found only the intake
disclaimer and unrelated algebraic identities named after Brahmagupta. It found no target-specific
Brahmagupta, Bretschneider, cyclic-quadrilateral-area, quadrilateral-area, or semiperimeter
declaration. This is narrow statement-feasibility evidence, not the downstream anchor audit or a
global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided untracked
`Formalizations/Lean/.lake` symlink was used read-only, and the pinned mathlib worktree remained
clean. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation ran.

## Validation Record

Commands ran in this isolated automation clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0202` | 0 | rank 1534; planned; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `git blame -L 1457,1462 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| authority, source, intake, toolchain, lockfile, and relevant mathlib `sha256sum` checks | 0 | exact current hashes are preserved in `statement-blocker.json`; historical intake evidence was not rewritten |
| `python3 -B Stage1_Instances/THM-M-0202/check_intake.py` | 1 | historical intake replay rejects the current blueprint hash after integration changed authority projections; it was not modified or represented as statement validation |
| `python3 -B Stage1_Instances/THM-M-0202/check_json.py` | 0 | the three historical intake JSON files remain strict JSON |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned-mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0202/IntakeProbe.lean` | 0 | seven adjacent interfaces elaborated; stdout hash and size recorded above; no canonical target or proof body |
| bounded exact-topic `rg` over repo-local and pinned-mathlib Lean roots | 0 | only the intake disclaimer and unrelated Brahmagupta ring identities matched; no target declaration was identified |
| prohibited-declaration `rg` over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0202/statement-blocker.json` and scoped invariant assertions | 0 | valid JSON; identity, blocked state, null target/imports, unchanged vector, undefined mutations, false completion flags, exact two-file scope, and absent self-test agree |
| final standard, manifest, and target-show replays | 0 each | authority projections still pass; target remains planned, uniform L0/rework-required, and theorem-incomplete |
| scoped `git diff --check` plus per-new-file no-index checks | 0 aggregate | no whitespace diagnostics; raw no-index exit 1 is only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The historical intake checker is bound to its intake worker's earlier authority hashes and original
artifact inventory. Integration subsequently changed the generated blueprint/DAG projection while
recording intake `[_]`. Rewriting that historical evidence is outside this phase and would not cure
the missing proposition.

## Retry Condition And Status Boundary

The integration lane must master-accept fresh intake evidence before accepting a future statement
transition. Accountable reviewers must lawfully preserve and hash an immutable primary or approved
authoritative source, select and independently approve one exact proposition, and map every
incorporated definition, ordered binder, hypothesis, conclusion, proof boundary, correction, and
erratum. They must freeze the ambient plane and point structure; boundary order; cyclicity,
convexity, simplicity, and nondegeneracy predicates; area and side encodings; semiperimeter;
square-root or squared equality; orientation; checked alternate forms; and all degenerate cases.

A later statement worker can then encode precisely that reviewed claim, minimize pinned imports,
serialize and hash its elaborated expression and environment, compile every credited transport,
and run all four required mutation classes.

This records the first failed gate. It does not complete the statement node or any downstream node.
`audit_complete` and `theorem_complete` remain false, and no debt-vector change is proposed. Because
the exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`, node-specific
receipt, worker `[_]`, proof credit, or master acceptance is claimed.
