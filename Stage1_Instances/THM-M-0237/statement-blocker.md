# Exact-statement gate: blocked

Item: `S56-M-0237-STATEMENT`

Theorem: `THM-M-0237`

Base revision: `9898aa12e1dd435f018a54a6266ec411ed09a26a` (tree
`c0abfcd8c20a1be4b894a7664746d02086072b9d`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0237-INTAKE` has provisional worker
state `[_]`, not a master-accepted receipt. Section 10.2 permits provisional preparation of a later
node under explicit concurrency, but master closure remains dependency ordered. Independently, no
exact Lean 4 target can be truthfully elaborated from the authoritative repository record.

That record supplies only the title Riemann-Roch theorem, the attribution Riemann/Roch, the year
1865, and the topic-level gloss "divisor theory of compact Riemann surfaces." It provides no
bibliography, formula, incorporated definitions, ordered binders, assumptions, conclusion, proof
boundary, correction history, or formal artifact. Stage0 explicitly leaves the precise definitions
and premises open. The catalog status `verified` is untrusted metadata under rev-5.6.

The intake identifies the familiar candidate formula

```text
ell(D) - ell(K - D) = deg(D) + 1 - g
```

but deliberately does not credit it as the canonical statement. The two human-source candidates
were identified from bibliographic metadata only; no lawful immutable text, exact theorem and
definition chain, proof boundary, corrections, errata, or independent review was accepted. The
following choices change the proposition rather than merely its notation:

- whether a compact Riemann surface is nonempty and connected by definition, and the exact
  one-dimensional complex-manifold model;
- the divisor representation, finite-support and sign conventions, order of a meromorphic
  function, effectivity, principal divisors, subtraction, and degree;
- whether `L(D)` and `ell(D)` use meromorphic functions or global sections of `O(D)`, including
  finite-dimensionality and the zero function;
- the genus convention and whether `K` is a chosen canonical divisor, divisor class, or canonical
  bundle, including existence and choice independence;
- integer versus natural dimensions, coercions, universes, typeclass context, binder order, and
  the precise equality or Euler-characteristic form; and
- genus zero and one, negative degree, `D = 0`, `D = K`, empty support, constant functions, zero
  differentials, and empty or disconnected surfaces.

Selecting conventional answers would manufacture a nearby textbook theorem. Reusing
`THM-M-0105` or `THM-M-0175` would substitute an algebraic-curve target without a checked
analytification or GAGA bridge. Their legacy `S1_M_027.lean` and `S1_M_124.lean` files quantify
abstract divisor packages whose operations and invariants do not concretely encode this compact
analytic surface. Hiding the missing mathematics in such a package would be a weakened substitute,
not an exact target.

Section 5 of the rev-5.6 blueprint makes statement ambiguity and a missing expression fingerprint
hard blockers. There is therefore no canonical expression for which minimal imports, checked
alternate transports, or removed-hypothesis, changed-domain, changed-binder-scope, and boundary
mutations can be certified. Those mutations are undefined, not passed. The first substantive failed
gate is exact source-statement identity and its definition chain. The root remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated using the pinned environment. Its two direct
imports are:

```lean
import Mathlib.Analysis.Meromorphic.Basic
import Mathlib.Geometry.Manifold.Complex
```

The probe checks ten adjacent interfaces: `ModelWithCorners`, `ChartedSpace`, `IsManifold`,
`CompactSpace`, `MDifferentiable`, two compact-manifold holomorphic constancy results, and the
plane-domain predicates `MeromorphicAt`, `MeromorphicOn`, and `Meromorphic`. It defines no
compact-surface divisor, canonical bundle or divisor, finite-dimensional section space, genus,
`ell`, or Riemann-Roch proposition. Its imports consequently cannot be certified minimal for an
absent canonical target.

Pinned `Mathlib/Geometry/Manifold/Complex.lean:28-32` itself lists holomorphic vector and line
bundles and finite-dimensionality of their section spaces as TODO work. A bounded pinned-mathlib
source search found no declaration matching the queried Riemann-Roch or compact-Riemann-surface
terms. Repository Lean matches belong to other algebraic, Grothendieck, Hirzebruch, or graph
Riemann-Roch targets. These results are narrow feasibility evidence only, not the downstream anchor
audit, a proof of global absence, or statement/proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided untracked
`Formalizations/Lean/.lake` symlink points to the canonical pinned artifacts and was used read-only.
The mathlib package worktree remained clean. No `lake update`, `lake build`, dependency clone or
fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran in the isolated automation checkout on 2026-07-13 (Asia/Shanghai).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0237` | 0 | rank 940; planned; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` (pre-edit); `git rev-parse HEAD 'HEAD^{tree}'` | 0 each | only the automation-provided `.lake` symlink was untracked; base revision and tree are recorded above |
| exact whole-file `sha256sum` command and catalog-block `sed ... \| sha256sum` pipeline listed in `statement-blocker.json` | 0 each | current authority, source, toolchain, dependency, intake, and catalog-block hashes matched the structured fingerprints |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 and Lake 5.0.0 at the revisions above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 each | pinned mathlib revision and tree above; package status output empty |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0237/IntakeProbe.lean` | 0 | all ten adjacent API checks elaborated; no target theorem was stated |
| exact pinned-mathlib `rg` command listed in `statement-blocker.json` | 1 | expected no-match result for the bounded query; discovery-only evidence, not an anchor audit or global absence claim |
| exact repository Lean `rg` command listed in `statement-blocker.json` | 0 | matches belong to other theorem IDs and abstract algebraic-curve packages; no exact analytic target was identified |
| `python3 Stage1_Instances/THM-M-0237/check_intake.py` | 1 | known historical-intake freshness failure at its hardcoded HEAD assertion: the checker is bound to `122f443c54e4e81d1bf325b07e18ba095823da6d`, not the current integrated HEAD; historical intake evidence was not rewritten |
| `python3 -m json.tool Stage1_Instances/THM-M-0237/statement-blocker.json`; exact scoped `jq -e` command listed in that JSON | 0 each | blocker JSON parsed; identity, null target/imports, undefined mutations, unchanged vector, false completion flags, and blocked state passed |
| prohibited-declaration `rg` scan over owned Lean files | 1 | expected no match: no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-0237`; separate exact `git diff --no-index --check` commands listed in the JSON | 0 / 1 each | no whitespace diagnostics; each no-index command has expected new-file difference status |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The historical intake checker is intentionally not represented as a current statement validator.
Its receipt and invariants are bound to the intake worker's earlier revision and authority hashes.
Rewriting that provisional history is outside this phase and would not cure the missing proposition.

## Retry Condition And Status Boundary

The integration lane must master-accept the intake before an eventual accepted statement
transition. Accountable reviewers must preserve and hash a lawful immutable primary or
authoritative source, transcribe its exact analytic theorem and every incorporated definition,
ordered binder, hypothesis, conclusion, proof boundary, correction, erratum, and exceptional case,
reconcile the duplicate-target and analytic-to-algebraic boundaries, and independently approve the
mapping. A later statement worker can then encode that same claim with concrete Lean definitions,
minimize pinned imports, serialize and hash the elaborated expression and environment, compile each
credited transport, and run all four required mutation classes.

This records the first failed gate. It does not complete the statement node or any downstream node.
The root remains `[H1, M4, R4]`; `audit_complete` and `theorem_complete` remain false, and no debt
change is proposed. The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json`, node-specific completion receipt, proof credit, or master-acceptance
claim is emitted.
