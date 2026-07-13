# THM-M-0933 exact-statement gate: blocked

Item: `S56-M-0933-STATEMENT`

Base revision: `b56df790fc94c5366cf919a6fe5411d06b427c59` (tree
`18ba629d4c00333f6e17018905f4fbd30558bb4c`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0933-INTAKE` has only provisional
worker state `[_]`: its receipt is unaccepted and non-content-addressed, lists no accepted receipt
IDs, and leaves the canonical claim and formal target null. There is no master-accepted dependency
receipt.

Independently and decisively, the exact-statement gate fails. The complete catalog record gives the
name Olson theorem, John Olson, 1969, and only the gloss "the Davenport constant of finite abelian
groups." It does not state a formula, define the Davenport invariant, select a finite-abelian-group
subclass, or identify a source proposition. Stage0 explicitly leaves the exact definitions and
premises open.

The inspected source record exposes several materially different candidate roots:

- Olson Part I's finite abelian p-group equality `D(G) = D*(G)`;
- the rank-at-most-two equality associated with Olson Part II;
- the specialization `D((Z/nZ)^2) = 2n - 1`;
- a direct least-length forcing statement for a nonempty zero-sum subsequence; and
- a maximum zero-sum-free sequence formulation.

These are not interchangeable without source approval and checked transports. The repository also
does not fix a list, multiset, or multiplicity-function sequence model; subsequence semantics;
nonemptiness; additive versus multiplicative notation; an abstract group versus explicit
decomposition; binders and hypotheses; or trivial-group and threshold boundary cases. Choosing a
familiar candidate would invent, narrow, broaden, or substitute proposition-changing mathematics.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing elaborated
expression fingerprint hard blockers. There is consequently no canonical Lean expression whose
imports can be certified minimal, no approved alternate encoding, and no meaningful
removed-hypothesis, changed-domain, changed-binder-scope, or boundary-case mutation. Those four
mutation classes are undefined, not passed. No `Statement.lean`, theorem declaration, proof body,
weakened special case, or broadened interface was added. The root remains `[H1, M4, R4]`.

## Source And Lean Boundary

The strongest inspected source lead is David J. Grynkiewicz,
*A Generalization of the Chevalley-Warning and Ax-Katz Theorems with a View Towards Combinatorial
Number Theory*, arXiv:2208.12895v1. PDF page 5 defines `D(G)` and `D*(G)` and states Theorem 1.5:

```text
If G is a finite abelian p-group, then D(G) = D*(G).
```

Pages 17-18 give a modern proof. The paper cites John E. Olson,
*A Combinatorial Problem on Finite Abelian Groups I*, *Journal of Number Theory* 1(1) (1969),
8-10, DOI `10.1016/0022-314X(69)90021-3`. Intake confirmed bibliographic and abstract metadata,
but did not retrieve or inspect the original article body. Published crosschecks distinguish the
p-group result from Olson's rank-two result, confirming rather than resolving the catalog
ambiguity. The source lead therefore supports `H1`, not an independently accepted root or `H0`.

The existing discovery-only `IntakeProbe.lean` imports:

- `Mathlib.Algebra.BigOperators.Group.Multiset.Basic`;
- `Mathlib.Combinatorics.Additive.ErdosGinzburgZiv`;
- `Mathlib.GroupTheory.FiniteAbelian.Basic`; and
- `Mathlib.GroupTheory.PGroup`.

It checks seven adjacent finite-abelian decomposition, p-group, multiset, and EGZ interfaces. A
fresh replay passed in the pinned environment. A bounded exact-topic search found no
source-identical Olson/Davenport declaration in pinned mathlib; the repo-local match was only the
probe's disclaimer. This is feasibility evidence, not the downstream anchor audit. Because the
target is unidentified, the probe imports cannot be called minimal for it and receive no statement
or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided canonical `.lake` link
was used read-only. No dependency update, build, clone, fetch, or other `.lake` mutation ran.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0933` | 0 | rank 1472; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree appear above |
| scoped authority and null-target assertions | 0 | rank, dependency, intake `[_]`, statement `[ ]`, null canonical claim and target, `H1/M4/R4`, and unaccepted intake receipt agree |
| `git blame -L 6819,6824 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `python3 -B Stage1_Instances/THM-M-0933/check_intake.py` | 1 | historical intake checker expects state `[ ]`, attempts 0; integration now records `[_]`, attempts 1; it was not edited or represented as statement evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib revision, tree, and package-status checks | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0933/IntakeProbe.lean` | 0 | seven adjacent APIs elaborated; 769 output bytes; SHA-256 `a82c5636faea3eda9c08ad0f36f5b9d3ee9d7fb4d973ac30569a7f645e9a4ce9`; no target or proof body |
| bounded exact-topic Lean search | 0 overall | repo-local result was only the probe disclaimer; pinned mathlib returned expected no-match exit 1; no source-identical declaration located |
| prohibited-declaration scan over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0933/statement-blocker.json` plus scoped blocker invariants | 0 | valid JSON; identity, dependency, null target/imports, unchanged vector, four undefined mutations, false completion fields, two-file change scope, and no-self-test boundary agree |
| scoped tracked and new-file whitespace checks | 0 for diagnostics | no whitespace error in either blocker artifact |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The historical intake checker freezes its pre-integration authority snapshot. Rewriting that
receipt or checker is outside this statement phase and would not resolve the missing proposition.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must
lawfully preserve and admit an immutable primary or authoritative source, independently select one
exact Olson proposition, and approve every incorporated definition, binder, hypothesis,
conclusion, proof boundary, correction, erratum, transport, and boundary case.

A fresh statement worker can then encode precisely that reviewed claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile each credited
transport, and execute all four mutation classes.

This is a truthful blocked statement attempt, not completion of this or any downstream node.
Lifecycle remains `planned`; `audit_complete: false` and `theorem_complete: false`; no debt
change is proposed. Because the assigned phase did not pass, no `.stage1-worker-selftest.json`,
statement receipt, worker `[_]`, proof credit, or master acceptance is claimed.
