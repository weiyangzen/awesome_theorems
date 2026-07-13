# Exact-statement gate: blocked

Item: `S56-M-0240-STATEMENT`

Theorem: `THM-M-0240`

Base revision: `bd81d4853a030765585ef6fed4310484ceb1e458` (tree
`fb92fc7476bff9a2ce8c20f1d7be34c6655ca6b4`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0240-INTAKE` has provisional worker
state `[_]`, not a master-accepted receipt. Rev-5.6 section 10.2 permits provisional preparation of
a later node under explicit concurrency, but master closure remains dependency ordered.
Independently, no exact Lean 4 target can be truthfully elaborated from the authoritative
repository record.

That record supplies only the title `阿贝尔-雅可比定理` (Abel-Jacobi theorem), the attribution to
Niels Abel and Carl Jacobi, the year 1834, and the noun phrase `代数曲线的雅可比簇` (the Jacobian
variety of an algebraic curve). It gives no bibliography, truth-valued proposition, incorporated
definitions, ordered binders, hypotheses, conclusion, proof boundary, correction history, or
formal artifact. Stage0 explicitly leaves precise definitions and premises open. The catalog
status `已验证` is untrusted metadata under rev-5.6.

The inspected source lead does not cure this ambiguity. Milne's *Jacobian Varieties* contains
materially different results compatible with parts of the catalog phrase: Theorem 1.1 is an
algebraic existence and representability result, Theorem 1.2 is a pointed universal property, and
Theorem 2.5 is a complex analytic-to-algebraic comparison invoking Abel's theorem and Jacobi
inversion. The catalog does not cite Milne, and no accountable reviewer selected one of these
results, mapped its full definition chain and proof boundary, disposed of corrections and errata,
or independently approved it as this target.

The following choices change the proposition rather than merely its notation:

- existence or representability of a Jacobian, `Pic^0` identification, a based Abel-Jacobi map
  property, an Albanese or Picard universal property, or analytic-algebraic comparison;
- the base field and whether it is arbitrary, perfect, algebraically closed, or `Complex`;
- the curve model, including completeness or projectivity, smoothness or nonsingularity,
  connectedness or integrality, and genus;
- whether a rational base point or degree-one divisor is assumed and how it normalizes the map;
- the divisor, line-bundle, Picard-functor, Jacobian, symmetric-power, degree, sign, covariance, and
  functor-of-points conventions;
- the exact conclusion, including existence, representability, equality, equivalence,
  isomorphism, injectivity, surjectivity, kernel characterization, or universality; and
- genus zero and one, trivial Jacobians, nonclosed or inseparable fields, base change and descent,
  singular or reducible curves, and all degree and rational-point boundary cases.

Selecting familiar answers would invent a nearby theorem. Abel's divisor criterion cannot be
silently substituted because `THM-M-0238` separately owns Abel's theorem; symmetric-power
surjectivity or Jacobi inversion cannot be substituted because `THM-M-0239` owns that target.
Likewise, a structure or hypothesis storing the requested Jacobian, equivalence, map, or universal
property would assume rather than state and establish the missing mathematics.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing elaborated
expression fingerprint hard blockers. There is therefore no canonical expression for which
minimal imports, checked alternate transports, or removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations can be certified. Those mutations are
undefined, not passed. The first failed gate is exact source-statement identity and its definition
chain. The root remains `[H5, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated using the pinned environment. Its direct imports
are:

```lean
import Mathlib.AlgebraicGeometry.EllipticCurve.Jacobian.Point
import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.AlgebraicGeometry.Morphisms.Smooth
```

The probe checks seven adjacent scheme, smoothness, properness, Weierstrass-curve, and Jacobian
coordinate interfaces. It defines no Jacobian variety or relative Picard functor of a general
curve, Abel-Jacobi map, canonical target, transport, or proof body. In particular,
`WeierstrassCurve.Jacobian` is a Weierstrass equation in weighted Jacobian coordinates, not a
general curve's Jacobian variety. The pinned `CommRing.Pic` interface concerns invertible modules
over a commutative ring, and its source leaves the connection to invertible sheaves on `Spec R` as
future work. Probe imports consequently cannot be certified minimal for an absent target.

A bounded exact-topic search found no matching general Abel-Jacobi, Jacobian-variety, Picard
scheme or functor, or degree-zero Picard declaration in pinned mathlib. Repository-local matches
are planning records that themselves describe curve-Jacobian or Picard formalization debt. These
are narrow discovery observations only, not the downstream immutable anchor audit or a proof of
global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided untracked
`Formalizations/Lean/.lake` symlink points to the canonical pinned artifacts and was used
read-only. The mathlib package worktree remained clean. No `lake update`, `lake build`, dependency
clone or fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran in this isolated automation checkout on 2026-07-13 (Asia/Shanghai).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0240` | 0 | rank 1251; planned; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` (pre-edit); `git rev-parse HEAD 'HEAD^{tree}'` | 0 each | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| exact whole-file `sha256sum` command listed in `statement-blocker.json` | 0 | current authority, source, toolchain, dependency, and intake hashes matched the structured fingerprints |
| `git blame -L 1731,1736 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package status | 0 each | pinned mathlib revision and tree recorded above; package status output empty |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0240/IntakeProbe.lean` | 0 | seven adjacent APIs elaborated; complete stdout SHA-256 `000f934cba853b17c2758921194deceeefd0a93fc88929bf8d910aba5d2eb859`; no target theorem was stated |
| bounded pinned-mathlib exact-topic `rg` command listed in `statement-blocker.json` | 1 | expected no-match result; discovery only, not an anchor audit or global absence claim |
| the corresponding repository Lean `rg` command | 0 | matches are planning prose recording formalization debt; no exact target declaration or proof body was identified |
| `python3 -B Stage1_Instances/THM-M-0240/check_intake.py` | 1 | known historical-intake freshness failure at its first stale authority hash (`Docs/Stage1_Blueprint_rev-5.6.md`); the checker also binds intake HEAD `c6fd6dad8fcfe5fd464416cd452f50286b546978` and the original nine-file inventory rather than the current integrated snapshot |
| `python3 -m json.tool Stage1_Instances/THM-M-0240/statement-blocker.json` plus the scoped `jq -e` invariant command listed there | 0 each | identity, null target and imports, four undefined mutations, unchanged vector, false completion flags, and blocked state passed |
| prohibited-declaration `rg` scan over owned Lean files | 1 | expected no match: no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-0240`; separate no-index checks listed in the JSON | 0 / 1 each | no whitespace diagnostics; each no-index command has expected new-file difference status |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The historical intake checker is not represented as a current statement validator. Its receipt and
invariants are bound to the intake worker's earlier revision, authority hashes, and exact nine-file
inventory. Rewriting that provisional history is outside this phase and would not cure the missing
proposition.

## Retry Condition And Status Boundary

The integration lane must master-accept the intake before an eventual accepted statement
transition. Accountable reviewers must preserve and hash a lawful immutable primary or
authoritative source, select one truth-valued proposition, transcribe every incorporated
definition, ordered binder, hypothesis, conclusion, construction and uniqueness convention,
proof boundary, correction, erratum, and exceptional case, reconcile the neighboring Abel and
Jacobi scopes, and independently approve the mapping. A later statement worker can then encode
that same claim using concrete Lean definitions, minimize pinned imports, serialize and hash the
elaborated expression and environment, compile every credited transport, and run all four required
mutation classes.

This records the first failed gate. It does not complete the statement node or any downstream node.
The root remains `[H5, M4, R4]`; `audit_complete` and `theorem_complete` remain false, and no debt
change is proposed. The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json`, node-specific completion receipt, proof credit, or master-acceptance
claim is emitted.
