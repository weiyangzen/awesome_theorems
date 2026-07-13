# THM-M-1474 exact-statement gate: blocked

Item: `S56-M-1474-STATEMENT`

Base revision: `974415b7b5b44717c9e7aacd8c838c9489ce27f4` (tree
`d9e4d272bf64ef22b1ff43831862394b0135ada3`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1474-INTAKE` has only provisional worker
state `[_]`: `intake-receipt.json` is unaccepted and non-content-addressed, and it contains no
accepted receipt ID. Master closure therefore remains dependency ordered.

Independently and decisively, the exact-statement gate fails. The complete repository claim is the
method-family gloss "stability analysis of finite differences." It fixes no equation or PDE class,
domain and data, grid, stencil, recurrence, coefficients, boundary treatment, Fourier convention,
frequency set, scalar or matrix amplification object, spectral assumptions, stability norm and
quantifiers, logical direction, conclusion, constants, arithmetic model, ordered binders, or
boundary cases. Stage0 explicitly leaves exact definitions and premises open; intake accordingly
records a null human claim and null canonical Lean target at `[H5, M4, R4]`.

Materially inequivalent propositions fit the gloss: a necessary amplification condition, a
sufficient condition, a scalar periodic-grid equivalence with `|G(theta)| <= 1`, a matrix-symbol
criterion with normality or uniform diagonalizability, a multistep root condition, or a stability
calculation for one chosen scheme. The inspected LeVeque source-family lead itself separates
parabolic and hyperbolic von Neumann analyses and has a material nearby erratum; the catalog cites
and selects none of its results. Choosing any familiar version would invent, narrow, broaden, or
substitute proposition-changing mathematics.

Consequently there is no canonical expression to elaborate, no honest minimal-import claim, no
expression or environment fingerprint, and no credited alternate encoding. The required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are undefined,
not passed. No `Statement.lean`, theorem declaration, proof body, weakened special case, or
broadened interface was added.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740` and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). Its two imports expose continuous L2 Fourier and
abstract spectral-radius interfaces only. Four API checks passed, and the two representative axiom
reports list only `propext`, `Classical.choice`, and `Quot.sound`. The probe defines no finite-
difference grid, recurrence, symbol, amplification factor, stability predicate, or target theorem;
its imports therefore cannot be certified minimal for the absent target.

A bounded exact-topic search over repo-local Lean and pinned mathlib found no source-selected von
Neumann finite-difference stability declaration. This is narrow feasibility evidence, not the
downstream anchor audit or a global absence proof. The automation-provided canonical `.lake`
symlink and pinned artifacts were used read-only. No dependency update, build, clone, fetch, or
other `.lake` mutation was run.

## Validation Record

Commands ran from the isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1474` | 0 | rank 1151; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| authority and null-target assertions over the target manifest, execution DAG, `instance.json`, and intake receipt | 0 | rank, dependency, intake `[_]`, statement `[ ]`, null claim/target, unaccepted intake receipt, and H5/M4/R4 agree |
| `git blame -L 10756,10761 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `python3 -B Stage1_Instances/THM-M-1474/check_intake.py` | 1 | historical intake checker expects authoritative intake state `[ ]`, while integration now records provisional `[_]`; this statement phase records rather than rewrites stale intake evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib `git rev-parse HEAD 'HEAD^{tree}'` and `status --short` | 0 | revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1474/IntakeProbe.lean` | 0 | four adjacent APIs elaborated; stdout SHA-256 `85d5cdd84664ff053dd14e8f1afe7d72fd5e6f5694ea82ea5e194a07de423086`; no target declaration |
| bounded exact-topic `rg` over repo-local Lean and pinned mathlib | 1, expected no match | empty output; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`; no source-selected declaration located |
| prohibited-construct scan over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

Final JSON, invariant, whitespace, and absent-self-test checks are recorded in the structured
blocker beside this report.

## Retry Condition

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must then
admit an immutable pinpoint source and independently select one exact proposition, fixing every
equation, domain and data condition, grid, scheme and recurrence, boundary rule, Fourier convention,
frequency set, amplification object and spectral premise, stability definition and logical
direction, conclusion, constants, ordered binders, arithmetic boundary, and degenerate case.

A fresh statement worker can then encode precisely that reviewed claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport, and
execute all four required mutation classes.

This is a truthful blocked statement attempt, not completion of this node or any downstream node.
Lifecycle remains `planned`; `audit_complete: false` and `theorem_complete: false`; no debt-vector
change is proposed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or master acceptance
is claimed.
