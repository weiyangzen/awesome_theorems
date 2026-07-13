# THM-M-0884 exact-statement gate: blocked

Item: `S56-M-0884-STATEMENT`

Base revision: `db4b8793e70ce8af74c9c9490acfa50aa3684d5e` (tree
`6434a20532ae7c523ad293e67a6228ab384bfb8a`).

## Decision

The statement item remains `[ ]`. Its prerequisite, `S56-M-0884-INTAKE`, has only provisional
worker state `[_]`. The intake receipt declares `accepted: false`; it has a provisional packet ID
but no accepted or content-addressed receipt ID. It
binds an older repository base and older authority snapshots. The current intake checker also
rejects replay because it expects the historical intake item shape (`[ ]`, attempt 0), while the
authoritative DAG now records `[_]`, attempt 1. There is no master-accepted dependency receipt.

Independently and decisively, the exact-statement gate cannot pass from the received source record.
The complete catalog statement is only `最优谱扩展图` ("optimal spectral expander graphs") under
the object label `Ramanujan图` ("Ramanujan graphs"). This names a graph class and gives an
optimality slogan; it is not one binder-complete truth-valued proposition. Stage0 explicitly leaves
the precise definitions, premises, formal system, proof route, equivalent forms, axiom use, and
machine artifact open. The catalog's `已验证` label is untrusted metadata under rev-5.6.

The intake records Alexander Lubotzky's *Ramanujan Graphs*, `arXiv:1711.06558v1`, as an immutable
exact-topic discovery lead. Its opening definition treats a finite connected `k`-regular graph,
`k >= 3`, as Ramanujan when every adjacency eigenvalue `lambda` satisfies
`|lambda| = k` or `|lambda| <= 2 * sqrt(k - 1)`. The exposition separately discusses
Alon-Boppana optimality, expansion consequences, existence, and explicit constructions. It does not
establish which of these inequivalent claims the catalog assigned to this target, and no source
reviewer has approved one as the canonical root.

Selecting the standard predicate definition, an Alon-Boppana asymptotic theorem, an expansion or
mixing implication, an existence theorem, a construction theorem, or a conjunction would therefore
invent, narrow, broaden, or substitute proposition-changing mathematics. It would also risk taking
scope owned by neighboring LPS, Morgenstern, MSS, spectral-graph-theory, and Cheeger targets.

Consequently there is no honest canonical Lean expression whose imports can be certified minimal,
no expression or environment fingerprint, no credited alternate encoding, and no meaningful
removed-hypothesis, changed-domain, changed-binder-scope, or boundary-case mutation suite. The
canonical human statement and formal target remain null, and the root vector remains
`[H5, M4, R4]` as a provisional, unaccepted intake classification. This blocker does not promote
or independently accept that vector.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` was re-elaborated with the pinned environment. It
checks finite-simple-graph, regularity, real adjacency-matrix, Hermitian-eigenvalue, spectrum, and
real-square-root APIs. It declares no Ramanujan predicate, target theorem, transport, axiom, or
proof body. A bounded source-name search found only unrelated analytic-number-theory uses of the
Ramanujan name and no graph-theoretic Ramanujan, Alon-Boppana, or spectral-expander declaration in
the repo-local `AwesomeTheorems` modules or pinned mathlib. These observations are discovery-only
evidence, not the later formal-anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided canonical `.lake` symlink was
used read-only. No `lake update`, `lake build`, dependency clone/fetch, or other `.lake` mutation was
run.

## Validation Record

Commands ran from this worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0884` | 0 | rank 1436; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all; git rev-parse HEAD; git rev-parse 'HEAD^{tree}'` | 0 | before statement edits only the automation-provided `Formalizations/Lean/.lake` link was untracked; base revision and tree are recorded above |
| `git blame -L 6474,6479 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'; git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | pinned revision and tree recorded above; mathlib worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0884/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; stdout 1,011 bytes with SHA-256 `338dc5b58bca6fa8b32a5e7bca7bc571b5f33033b8486a444857c78a05af24cd`; stderr empty; no target declaration |
| bounded `rg` search for `Ramanujan`, `Alon-Boppana`, and `spectral expander` in repo-local `AwesomeTheorems` modules and pinned-mathlib Lean | 0 | only unrelated analytic-number-theory matches; no graph-theoretic candidate found in that scope; discovery-only evidence |
| `python3 -B Stage1_Instances/THM-M-0884/check_intake.py` | 1 | historical intake replay stops at its exact old authority-item assertion: it expects intake `[ ]`, attempt 0, while current authority records `[_]`, attempt 1 |
| prohibited Lean declaration scan over the owned `*.lean` files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration matched |
| `python3 -m json.tool Stage1_Instances/THM-M-0884/statement-blocker.json` | 0 after finalization | structured blocker is valid JSON |
| inline Python JSON assertions recorded in `statement-blocker.json` | 0 after finalization | identity, null target/imports/fingerprints, unchanged vector, four undefined mutations, false completion flags, exact changed paths, and no-self-test boundary agree |
| scoped whitespace checks | expected added-file diff status after finalization | no whitespace diagnostics in either blocker artifact |
| `test ! -e .stage1-worker-selftest.json` | 0 after finalization | no self-test manifest was emitted because the exact-statement deliverable did not pass |

## Retry Condition

The integration lane must first revalidate and master-accept fresh intake evidence. Accountable
reviewers must lawfully preserve and independently approve one immutable pinpoint truth-valued root,
including all incorporated definitions, corrections, ordered binders, hypotheses, conclusion, graph
and spectrum conventions, meaning of optimality, family quantifiers, and boundary cases. A later
statement worker can then encode only that approved proposition, minimize its pinned imports,
serialize the elaborated expression and environment, compile every credited transport, and execute
all four required mutation classes.

This is a truthful blocked statement attempt, not completion of this node or any downstream node.
No statement receipt, worker self-test packet, worker `[_]`, proof credit, audit completion, theorem
completion, or master acceptance is claimed.
