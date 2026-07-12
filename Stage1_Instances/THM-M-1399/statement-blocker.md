# THM-M-1399 statement-phase blocker

- Item: `S56-M-1399-STATEMENT`
- Base revision: `f23ca64267b6746e12a641dcc66cc4dbaf1e2191`
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt or theorem-completion claim

## First failed gate

The exact-statement gate in section 5.1 of `Docs/Stage1_Blueprint_rev-5.6.md` cannot be
truthfully entered from the repository record. That record supplies only the label
`向后微分公式` (backward differentiation formula), a collective twentieth-century attribution,
and the gloss `刚性方程的数值方法` (a numerical method for stiff equations). It supplies no exact,
mathematically determinate proposition that can be elaborated, bibliography, theorem or equation
locator, formula, ordered binders, hypotheses, conclusion, proof boundary, or exceptional cases.
Stage0 explicitly leaves the exact definitions and premises open, and rev-5.6 treats the historical
`已验证` label as untrusted metadata.

This omission changes the proposition. Even a formula-level reading could mean a constant-step
alpha-coefficient recurrence, an equivalent backward-difference form, the derivative-at-the-newest
node construction from an interpolating polynomial, or a variable-step or variable-order scheme;
the order could be fixed or quantified over a source-defined admissible range. Consistency, order,
zero-stability, convergence, stability, and implicit-update solvability are associated theorem
families rather than interchangeable definitions of the formula. These candidates can differ in
coefficient normalization, indexing, time grid, state and equation domain, starting history,
quantifier dependencies, and conclusion, so source selection must fix those dimensions. Selecting
BDF1, BDF2, a constant-step convention, or an associated correctness or stability theorem from
memory would narrow or substitute mathematics rather than elaborate the received target.

Curtiss and Hirschfelder's 1952 article *Integration of Stiff Equations* and Gear's 1971 article
*The automatic integration of ordinary differential equations* are historical discovery leads
recorded by intake. The catalog cites neither and selects no formula or theorem passage from them.
No immutable accepted edition, exact locator, incorporated-definition crosswalk, proof boundary,
correction and errata disposition, or independent approval has been admitted.

The intake dependency is only provisional `[_]`; its receipt says `accepted: false` and contains no
accepted receipt ID. Rev-5.6 section 10.2 permits this dependency-ordered statement attempt from a
provisional predecessor, but intake master acceptance remains necessary before any eventual
accepted statement transition. The first substantive failure in this attempt is exact
source-statement identity. Consequently there is no canonical expression to elaborate, no honest
minimal import set, no expression or environment-expression fingerprint, and no alternate encoding
to credit.
Removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are undefined
until canonical binders and premises exist. The statement item therefore remains `[ ]`, and the
root remains `[H5, M4, R4]`.

No `Statement.lean`, theorem declaration, axiom, placeholder, weakened special case, broadened
interface, or circular assumed package was added.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated using the pinned environment. Its four direct
imports expose five checked adjacent declarations: `HasDerivAt`, `IsIntegralCurve`,
`IsPicardLindelof`, `Lagrange.interpolate`, and
`Lagrange.iterate_derivative_interpolate`. These generic derivative, ODE, existence, and
polynomial-interpolation declarations may support a future source-selected encoding, but none of
the five defines a BDF method or states the missing proposition. The imports therefore cannot be
certified minimal for the unidentified target, and the passing probe receives no statement,
anchor, or proof credit.

A bounded case-insensitive search of only `Formalizations/Lean/AwesomeTheorems` and pinned
`Mathlib` found no match for the recorded backward-differentiation, backward-difference-formula,
linear-multistep, multistep-method, stiff-equation/ODE, and BDF-method regex. This is narrow
feasibility evidence, not a search of every repository-local Lean file, the downstream immutable
anchor audit, or a global absence claim.

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
| `python3 scripts/stage1_target.py show THM-M-1399` | 0 | rank 1009; `planned`; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` | 0 | before this phase, only the automation-provided untracked `Formalizations/Lean/.lake` symlink was present |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | revision above; tree `d1872d3251ef6a9c395116467608691849d80496` |
| `git blame -L 10188,10193 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned mathlib revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; the pinned package worktree was clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1399/IntakeProbe.lean` | 0 | all five adjacent APIs elaborated; complete output SHA-256 `40bb9f8bcde1d64cb5bc47087a569940b60c19efc6336ce83dc6814f2ab580c2`; no target declaration |
| `rg -n -i --glob '*.lean' 'backward.?differentiation\|backward.?difference formula\|linear.?multistep\|multistep method\|stiff (equation\|ode)\|bdf method' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems` | 1 | expected no-match result in the bounded search |
| `rg -n --glob '*.lean' '\\b(sorry\|admit)\\b\|\\bsorryAx\\b\|^[[:space:]]*(axiom\|constant\|opaque)\\b\|^[[:space:]]*unsafe\\b' Stage1_Instances/THM-M-1399` | 1 | expected no-match result; no prohibited Lean declaration in the owned probe |
| `python3 -B Stage1_Instances/THM-M-1399/check_intake.py` | 1 | historical intake evidence is stale after integration changed the generated blueprint and DAG; the first failure is `stale receipt input hash: Docs/Stage1_Blueprint_rev-5.6.md`; this phase did not rewrite it |
| `python3 -m json.tool Stage1_Instances/THM-M-1399/statement-blocker.json` | 0 | finalized blocker is valid JSON |
| `python3 -c "import json; from pathlib import Path; b=json.loads(Path('Stage1_Instances/THM-M-1399/statement-blocker.json').read_text()); assert b['item_id']=='S56-M-1399-STATEMENT' and b['theorem_id']=='THM-M-1399' and b['state']=='[ ]'; assert all(b[k] is None for k in ('canonical_statement','canonical_formal_target','minimal_imports','elaborated_expression_hash','environment_expression_fingerprint')); assert b['root_vector_before']==b['root_vector_after']=={'H':'H5','M':'M4','R':'R4'}; assert set(b['statement_gate']['mutation_tests'].values())=={'not_meaningful_without_a_canonical_statement'}; assert not Path('.stage1-worker-selftest.json').exists()"` | 0 | identity, open state, null target/import/hash/fingerprint, unchanged `H5/M4/R4`, four undefined mutations, and absent self-test agree |
| `git diff --check -- Stage1_Instances/THM-M-1399 .stage1-worker-selftest.json` plus `git diff --no-index --check /dev/null <each-new-blocker-file>` | 0; 1 for each new-file comparison | no whitespace diagnostics; the two no-index exits are the expected new-file difference status |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest is absent because the exact-statement deliverable did not pass |

## Unblocking condition

An accountable source owner must preserve and hash one immutable primary or authoritative edition,
select and transcribe one exact truth-valued formula proposition or explicitly approved corrected
root with a pinpoint locator and every incorporated definition and premise, audit corrections and
errata, and obtain independent approval of its identity with `THM-M-1399`. The selection must freeze
whether order is fixed or quantified, the admissible range if any, coefficient representation and
normalization, indices, constant or variable grid and step policy, state and equation domains,
starting history, exact conclusion, constant dependencies, and all source-relevant boundary cases
of the selected claim. Regularity, implicit-solve, arithmetic, and solver semantics must be frozen
when the chosen proposition uses them and explicitly excluded otherwise. The integration lane must
also master-accept the intake dependency before it can accept a later statement transition.

A later statement run can then encode that same claim, establish minimal pinned imports, serialize
and hash its elaborated expression and environment, check every credited transport, and run all
four mutation classes. Until then, no exact statement, proof, audit completion, theorem completion,
node-specific completion receipt, worker `[_]`, or master acceptance is claimed. Because this phase
did not pass its deliverable, no `.stage1-worker-selftest.json` is emitted.
