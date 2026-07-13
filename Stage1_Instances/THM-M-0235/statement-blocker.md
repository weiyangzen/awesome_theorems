# Exact-statement gate: blocked

Item: `S56-M-0235-STATEMENT`

Theorem: `THM-M-0235`

Base revision: `bd81d4853a030765585ef6fed4310484ceb1e458` (tree
`fb92fc7476bff9a2ce8c20f1d7be34c6655ca6b4`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0235-INTAKE` has provisional state
`[_]`, not a master-accepted receipt. Independently, the exact source claim cannot yet be mapped to
one Lean proposition without making proposition-changing choices that the repository leaves open.

The repository supplies only the gloss "nonconstant holomorphic functions are open maps." It does
not fix the domain, its nonemptiness/openness/connectedness convention, how a function on that
domain is represented, the meanings of holomorphic and nonconstant, or whether the conclusion is
relative openness, a subtype open-map predicate, or total `IsOpenMap`. In particular:

- `IsConnected U` includes nonemptiness, while `IsPreconnected U` permits the empty set;
- Lebl's inspected source lead uses `f : U -> Complex`, while the pinned mathlib candidate uses an
  ambient function `g : Complex -> Complex` (and in fact generalizes the domain carrier);
- subtype-open subsets of `U` and ambient-open sets contained in `U` require a checked transport;
- `DifferentiableOn Complex f U` and `AnalyticOnNhd Complex f U` require an open-set bridge; and
- the whole-plane entire-function corollary is a specialization, not a neutral reading of the
  received claim.

Jiri Lebl's *Guide to Cultivating Complex Analysis*, version 1.9, Definition 1.1 and Theorem
5.5.1, is a strong immutable source lead. It defines a domain as open and connected and states the
domain-relative open mapping theorem. Its footnote says sets are generally considered nonempty but
empty-domain statements are often vacuous. The catalog does not cite this source, its exact
subtype-to-ambient transport has not been checked, and no independent source approval is recorded.
The intake therefore correctly classifies it as H1 rather than selecting it as the canonical root.

Section 5.1 of the rev-5.6 blueprint makes statement ambiguity and a missing expression fingerprint
hard blockers. There is no canonical target for which imports can be certified minimal, and the
required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are
undefined rather than passed. No statement declaration, expression hash, checked transport,
statement receipt, or proof evidence is created.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` was re-elaborated with its one direct import,
`Mathlib.Analysis.Complex.OpenMapping`. It checks the local, connected-set, and whole-domain
interfaces plus the differentiability bridge. The closest connected-set candidate has type

```text
AnalyticOnNhd Complex g U -> IsPreconnected U ->
  (exists w, forall z in U, g z = w) or
  forall s subset U, IsOpen s -> IsOpen (g '' s).
```

The probe passed in pinned Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740` and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. Its exact stdout SHA-256 is
`50d100d55ec43fbcff16f201176c08f27c4a5eaefd3e9a0748e293335fd26596`; the three
representative declarations report `[propext, Classical.choice, Quot.sound]`.

This authenticates adjacent pinned interfaces only. It does not select a source-faithful root,
certify import minimality, check the subtype/ambient transport, perform the downstream anchor
audit, or credit a proof body. The automation-provided `.lake` symlink was used read-only; the
mathlib package remained clean, and no update, build, clone, fetch, or dependency mutation ran.

## Validation Record

Commands ran in this isolated worker checkout on 2026-07-13 (Asia/Shanghai).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0235` | 0 | rank 1247; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 each | pre-edit status contained only the automation-provided untracked `.lake` symlink; base revision/tree recorded above |
| `git blame -L 1696,1701 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 and Lake 5.0.0 at the pinned revision |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package `status --short` | 0 each | mathlib revision above, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package status empty |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0235/IntakeProbe.lean` | 0 | six interfaces elaborated; three axiom reports as above; stdout hash as above |
| bounded exact-topic `rg` search recorded in `statement-blocker.json` | 0 | exact-topic interfaces were confined to the pinned complex open-mapping module and intake probe; discovery only |
| `python3 -B Stage1_Instances/THM-M-0235/check_intake.py` | 1 | known historical-intake freshness failure: checker is bound to intake base `c6fd6dad...`, not current integrated HEAD; historical evidence was not rewritten |

## Retry Condition And Status Boundary

The integration lane must first master-accept the intake for an accepted dependent transition.
Accountable source and Lean reviewers must then select, preserve, hash, and independently approve an
immutable exact source proposition, including its definition of domain and nonemptiness convention,
function-domain presentation, holomorphicity and nonconstancy predicates, relative-open conclusion,
ordered binders, degenerate cases, correction and errata disposition, and required transports.

A later statement run can encode only that approved claim, minimize its pinned imports, serialize
the elaborated expression and environment, compile every credited transport, and execute all four
mutation classes. Until then the root remains `[H1, M3, R4]`; `audit_complete` and
`theorem_complete` remain false. Because this phase did not pass, no `.stage1-worker-selftest.json`,
node receipt, worker `[_]`, proof credit, or master-acceptance claim is emitted.
