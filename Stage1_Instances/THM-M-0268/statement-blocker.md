# Exact-statement gate: blocked

Item: `S56-M-0268-STATEMENT`

Theorem: `THM-M-0268`

Base revision: `2226f559136f12fde46b1bf73cdf629043b8a648` (tree
`33cb254ed06b1391379b8e7f88c5e23188957b62`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0268-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Dependency-ordered preparation is possible, but its
unsigned non-content-addressed receipt has `accepted: false` and deliberately leaves the canonical
mathematical statement and formal target null.

More decisively, the exact source-statement gate fails. The complete repository record names the
Lebesgue dominated convergence theorem, attributes it to Henri Lebesgue in 1902, and says only
"conditions for exchanging an integral and a limit." It supplies no citation, formula,
incorporated definitions, ordered binders, premises, conclusion, proof boundary, correction
history, or reviewer. Stage0 repeats that gloss while explicitly leaving precise definitions and
assumptions open. The catalog label `verified` is untrusted metadata and supplies neither source
identity nor kernel credit.

The bibliographic lead recorded at intake, Lebesgue's 1902 *Integrale, Longueur, Aire*, was checked
only through mutable Crossref metadata. No lawful immutable exact proposition, definition chain,
proof passage, translation, correction or erratum disposition, or independent review has been
admitted. Thus the source does not decide between a Bochner integral and a nonnegative `lintegral`,
a scalar or general normed-space codomain, a natural-number sequence or countably generated filter,
ordinary or almost-everywhere measurability, the convergence and domination conventions, the
dominator encoding, or a conclusion bundle that also asserts integrability or L1 convergence.

These choices change the proposition. Selecting a convenient pinned mathlib declaration would
invent or substitute missing mathematics, not elaborate the exact received target. Consequently no
canonical target, minimal target import, elaborated-expression fingerprint, checked transport, or
meaningful removed-hypothesis, changed-domain, changed-binder-scope, or boundary-case mutation
exists. The vector remains `[H1, M3, R4]`.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` imports
`Mathlib.MeasureTheory.Integral.DominatedConvergence`. In the pinned environment it exposes and
successfully checks seven adjacent interfaces: Nat- and filter-indexed Bochner convergence,
measurable and a.e.-measurable nonnegative `lintegral` convergence, filter-indexed `lintegral`
convergence, finite integrability of the limit, and L1-norm convergence. The representative axiom
reports are `[propext, Classical.choice, Quot.sound]`.

This authenticates exact-topic interfaces only. Those declarations differ in domains, binders,
assumptions, and conclusions; the probe contains no canonical target, source transport, mutation,
or proof body. Its import therefore cannot be certified minimal for an absent target and receives
no statement or proof credit. A bounded repo-local and pinned-mathlib search found 34 files with
exact-topic declarations or downstream uses, but no source-identical mapping was accepted.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). Existing canonical `.lake` artifacts were used read
only; no update, build, clone, fetch, or dependency mutation was run.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0268` | 0 | rank 1275; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `git blame -L 1929,1934 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sha256sum` over current authority, intake, toolchain, lockfile, and three candidate mathlib source inputs | 0 | exact fingerprints are recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package `status --short` | 0 | pinned revision/tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0268/IntakeProbe.lean` | 0 | seven adjacent exact-topic interfaces elaborated; representative declarations reported the three axioms above; stdout SHA-256 `834ccd18e768f3995086da58e3d02c89a3e51d12881731300802c066d4e73ebe` |
| bounded `rg` search for dominated-convergence names and candidate declarations over repo-local Lean and pinned mathlib | 0 | 34 files with candidate declarations or downstream uses located; no source-identical root mapping or proof credit inferred |
| `python3 -B Stage1_Instances/THM-M-0268/check_intake.py` | 1 | historical intake checker freezes base `c2e294be...`, not this later worker base; it is not statement evidence and was not modified |

| `python3 -m json.tool` plus scoped semantic assertions over `statement-blocker.json` | 0 | valid JSON; blocked identity, null target/imports, unchanged vector, undefined mutations, and false completion/self-test flags agree |
| wrapped prohibited-declaration scan over `Stage1_Instances/THM-M-0268/*.lean` | 0 | inner `rg` returned expected no-match exit 1; no prohibited Lean declaration was found |
| `git diff --check` on the owned path plus new-file whitespace checks | 0 | no tracked or new-file whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

## Retry Condition And Status Boundary

Accountable reviewers must lawfully preserve and hash an immutable primary or approved
authoritative source, identify the exact proposition and all incorporated definitions, map every
ordered binder, premise, conclusion, proof boundary, correction, erratum, translation, and boundary
case, and independently approve the mapping. They must select the integral model, codomain, index,
measurability, convergence, domination, conclusion bundle, and null-set conventions. Master
acceptance of intake remains required before an accepted statement transition.

A later statement worker can then encode only that reviewed claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and run all four mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. No `.stage1-worker-selftest.json`,
statement receipt, worker `[_]`, master acceptance, statement fingerprint, proof body, or proof
credit is claimed.
