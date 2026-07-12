# THM-M-1397 statement-phase blocker

- Item: `S56-M-1397-STATEMENT`
- Base revision: `2cf42e232e732b5d915dc077d91524b386861821`
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt or theorem-completion claim

## First failed gate

The exact-statement gate in section 5.1 of `Docs/Stage1_Blueprint_rev-5.6.md` cannot be
truthfully entered from the authoritative repository record. That record supplies only the label
`Adams方法` (Adams method), an attribution to John Couch Adams, the year 1883, and the gloss
`多步数值方法` (multistep numerical methods). It contains no truth-valued proposition,
bibliography, theorem locator, recurrence, ordered binders, hypotheses, conclusion, proof boundary,
or exceptional cases. Stage0 explicitly leaves the exact definitions and premises open, and the
rev-5.6 manifest treats the historical `已验证` label as untrusted metadata.

This omission is proposition-changing. The label may denote an explicit Adams-Bashforth recurrence,
an implicit Adams-Moulton recurrence, a predictor-corrector procedure, coefficient derivation,
order or truncation-error formulas, consistency and convergence, zero- or absolute-stability
results, or a variable-step implementation theorem. These choices differ in their step count,
index and coefficient conventions, ODE and state domains, starting history, regularity, implicit
solve, error or stability notion, quantifier dependencies, and conclusion. Selecting one from
memory or conjoining several would invent, narrow, broaden, or substitute mathematics.

The inspected Encyclopedia of Mathematics entry is a stable source-family discriminator, not the
catalog's selected proposition or an admitted primary proof source. It distinguishes explicit,
implicit, predictor-corrector, error, and stability claims and dates the method to 1855, while the
catalog says 1883. No approved source correction, exact proposition, complete assumption and proof
crosswalk, historical reconciliation, errata audit, or independent review resolves that ambiguity.

The intake dependency is provisional `[_]` and has no master-accepted receipt. Independently of
that workflow boundary, exact source-statement identity is absent. Consequently there is no
canonical expression to elaborate, no honest minimal-import set, no normalized expression or
environment-expression fingerprint, and no credited alternate transport. Removed-hypothesis,
changed-domain, changed-binder-scope, and boundary mutations are not meaningful until the canonical
binders and premises exist. The statement node remains open at `M4`.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. Its three direct
imports expose five adjacent interfaces: `Lagrange.interpolate`,
`Lagrange.eval_interpolate_at_node`, `intervalIntegral`, `IsIntegralCurve`, and `Finset.sum`. These
generic interpolation, integration, ODE, and summation APIs may support a future source-selected
encoding, but none states an Adams-method theorem. The imports are therefore not claimed minimal
for the unidentified target, and the successful probe receives no statement, anchor, or proof
credit.

A bounded case-insensitive search of repo-local Lean and pinned mathlib found no numerical
Adams-Bashforth, Adams-Moulton, or multistep occurrence. Visible `Adams` occurrences concern the
separately owned Adams spectral sequence, an ordmap citation, or Adams operations in binomial-ring
documentation. This is narrow feasibility evidence, not the downstream formal-anchor audit and not
a global absence theorem.

The environment was Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided `.lake` symlink and pinned
artifacts were used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other
`.lake` mutation was run.

## Commands and exact results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1397` | 0 | rank 1007; `planned`; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` | 0 | before this phase, only the automation-provided untracked `Formalizations/Lean/.lake` symlink was present |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | revision above; tree `f37ffb23dda888fedd3da7b2d7a8bbceaee21d44` |
| `git blame -L 10174,10179 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned mathlib revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; the pinned package worktree was clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1397/IntakeProbe.lean` | 0 | all five adjacent APIs elaborated; complete output SHA-256 `515f47b8bf32b56d8834bd6111718b03a5df9d228ecb2107aafd7d81c12c9c46`; no target declaration |
| `rg -n -i '\\b(adams[-_ ]?(bashforth\|moulton\|method)\|multistep\|multi[-_ ]step)\\b' Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | expected no-match result for numerical Adams or multistep terms |
| `rg -n -i 'adams' Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | only unrelated namesakes described above; no numerical Adams target |
| `rg -n --glob '*.lean' '\\b(sorry\|admit)\\b\|\\bsorryAx\\b\|^[[:space:]]*(axiom\|constant\|opaque)\\b\|^[[:space:]]*unsafe\\b' Stage1_Instances/THM-M-1397` | 1 | expected no-match result; no prohibited Lean declaration in the owned probe |
| `python3 -B Stage1_Instances/THM-M-1397/check_intake.py` | 1 | the historical intake receipt fingerprints an older generated blueprint and execution DAG, and the checker freezes the original nine-file intake inventory; this statement phase does not rewrite historical intake evidence |
| `python3 -m json.tool Stage1_Instances/THM-M-1397/statement-blocker.json` | 0 | finalized blocker is valid JSON |
| scoped blocker invariant check | 0 | item and base identity, open state, null target/import/hash/fingerprint, unchanged `H5/M4/R4`, four unrunnable mutations, false completion fields, and absent worker self-test agree |
| scoped tracked and added-file whitespace checks | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest is absent because the statement deliverable did not pass |

## Unblocking condition

An accountable source owner must preserve and hash one immutable primary or authoritative edition,
select and transcribe one exact truth-valued Adams proposition with a pinpoint locator and every
incorporated definition and premise, reconcile the historical record, audit corrections, and
obtain independent approval of its identity with `THM-M-1397`. The selection must freeze the
scheme family, step/order and index conventions, coefficients, ODE and state domains, grid and
starting history, regularity and solvability assumptions, exact conclusion and constant
dependencies, asymptotic convention, and all boundary cases.

A later statement run can then encode that same claim, establish minimal pinned imports, serialize
and hash its elaborated expression and environment, check every credited transport, and run all
four mutation classes. Until then, no exact statement, proof, audit completion, theorem completion,
node-specific completion receipt, or master acceptance is claimed. Because this phase is not
genuinely self-tested to its completion gate, no `.stage1-worker-selftest.json` is emitted.
