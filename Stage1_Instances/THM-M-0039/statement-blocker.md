# Exact-statement gate: blocked

Item: `S56-M-0039-STATEMENT`

Theorem: `THM-M-0039`

Base revision: `a1c9974d7fb28cd680e6494b968544bf801a93a2` (tree
`1fa287bc821355aca2ca9e3ce107830a3eb58e64`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0039-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`; its receipt declares `accepted: false` and contains
no accepted receipt ID. Rev-5.6 allows dependency-ordered preparation from a provisional
predecessor, but only the integration lane may accept a later transition after its dependency is
accepted.

Independently, the exact-statement gate fails. The catalogue supplies only the title
`卡普兰斯基定理` (Kaplansky theorem), Irving Kaplansky attribution, year 1958, and the gloss
`关于PI环的结构` (the structure of PI rings). It gives no bibliography, truth-valued proposition,
incorporated definitions, ordered binders, hypotheses, conclusion, proof boundary, corrections,
errata, or independent source review. The catalogue's `已验证` label is explicitly untrusted under
rev-5.6.

The intake lawfully inspected Irving Kaplansky's 1948 paper *Rings with a polynomial identity* and
identified Theorem 1 as the strongest source lead:

> A primitive algebra satisfying a polynomial identity is finite-dimensional over its center.

That lead is not the frozen target. Its date conflicts with the catalogue by ten years, the
catalogue gloss is broader, the paper contains several materially different PI results, and
section 4(c) gives a distinct ring extension with coefficient conditions. No accountable reviewer
has approved Theorem 1, the ring extension, or another result as the intended catalogue root.

Even after choosing a source result, the following proposition-changing choices remain open:

- associative and unital algebra versus the qualified ring formulation;
- base field, coefficient embedding, and any required injectivity condition;
- left or right primitivity and its faithful simple-module encoding;
- a finite variable type, a nonzero element of `FreeAlgebra F X`, evaluation through
  `FreeAlgebra.lift`, and universal vanishing under all substitutions;
- the center carrier, its field structure, the scalar action, and the exact
  finite-dimensionality predicate;
- ordered binders, universes, typeclasses, foundation profile, and computation profile; and
- zero or subsingleton carriers, empty variable types, zero or constant polynomials, missing
  faithful simple modules, and every other boundary case.

Selecting a familiar encoding now would invent or substitute mathematics. Sections 5 and 5.1 of
the blueprint make statement ambiguity and a missing expression fingerprint hard blockers.
Therefore there is no canonical `Prop` whose imports can be certified minimal, no checked
alternate transport, and no meaningful removed-hypothesis, changed-domain, changed-binder-scope,
or boundary-case mutation. Those tests are undefined, not passed. No `Statement.lean`, theorem
declaration, statement receipt, or proof body was added. Lifecycle stays `planned`, and the
provisional family vector stays `[H1, M3, R4]`.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` was re-elaborated with the pinned environment. It
imports:

```lean
import Mathlib.RingTheory.SimpleModule.WedderburnArtin
import Mathlib.RingTheory.SimpleRing.Field
import Mathlib.Algebra.FreeAlgebra
```

It checks ten adjacent free-algebra, simple-module, Jacobson-density, center-field, module-finite,
and Artin-Wedderburn interfaces. Its complete stdout is 1,550 bytes with SHA-256
`9ff3923146af9e8919354e85f9e89e0d57258212a22c68ea401eb7b7c514d6d5`. The two printed candidate
axiom reports are `[propext, Classical.choice, Quot.sound]`.

The probe defines no primitive-algebra predicate, polynomial-identity predicate, canonical target,
transport, mutation fixture, or proof body. Its imports therefore cannot be certified minimal for
an absent target. A bounded exact-topic search of pinned mathlib, repository Lean, and other target
dossiers produced no match. This is narrow discovery evidence, not the downstream anchor audit or
a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided untracked
`Formalizations/Lean/.lake` symlink was used read-only, and the mathlib package worktree remained
clean. No Lake update or build, dependency clone or fetch, or other `.lake` mutation ran.

## Validation Record

Commands ran in this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0039` | 0 | rank 1517; planned; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| exact `sha256sum` over authority, source, toolchain, dependency-lock, and intake inputs | 0 | fingerprints recorded in `statement-blocker.json`; the intake target, claim, expression, and environment fingerprint remain null |
| `cd Formalizations/Lean && lake env lean --version`; `lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib status and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | package worktree clean; pinned revision and tree recorded above |
| `cd Formalizations/Lean && LC_ALL=C.UTF-8 TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0039/IntakeProbe.lean` | 0 | ten adjacent interfaces elaborated; output size and hash recorded above; no target or proof body |
| bounded exact-topic `rg` over pinned mathlib, repo Lean, and other dossiers | 1 (expected no match) | empty output, SHA-256 `e3b0c442...b855`; no exact Kaplansky primitive-PI target located |
| `python3 -B Stage1_Instances/THM-M-0039/check_intake.py` | 1 | historical intake replay stops at a stale input-manifest hash after integration changed authority state; it was not edited or represented as statement validation |
| prohibited-declaration scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool` plus scoped assertions on `statement-blocker.json` | 0 | structured identity, dependency, null target/imports, unchanged vector, undefined mutations, false completion fields, exact two-file change scope, and absent self-test agree |
| scoped and per-new-file whitespace checks | 0 diagnostics | no whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The historical intake checker binds intake-time authority hashes, recipes, and the original
nine-file inventory. Integration subsequently recorded intake `[_]` and changed the authoritative
blueprint and execution DAG. Adding this statement blocker also intentionally changes the dossier
inventory. Rewriting historical intake evidence is outside this phase and would not cure the
missing proposition.

## Retry Condition And Status Boundary

The integration lane must master-accept the intake before accepting a future statement transition.
Accountable source and scope reviewers must lawfully preserve and hash an immutable primary or
authoritative source, resolve the 1958/1948 chronology, select one exact proposition, and approve
every incorporated definition, ordered binder, hypothesis, conclusion, proof boundary, correction,
erratum, and boundary case. A later statement worker can then encode precisely that approved claim,
minimize pinned imports, serialize and hash its elaborated expression and environment, compile
every credited transport, and run all four mutation classes.

This records the first failed gate. It does not complete the statement node or any downstream node.
`audit_complete` and `theorem_complete` remain false, and no debt-vector change is proposed. Since
the exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`, node-specific
completion receipt, worker `[_]`, proof credit, or master acceptance is claimed.
