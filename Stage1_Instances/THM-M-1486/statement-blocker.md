# THM-M-1486 exact-statement gate: blocked

- Item: `S56-M-1486-STATEMENT`
- Base revision: `fd0fab2ab7f4f514a5cc625bbce92879e718ba13` (tree
  `4116d53bcf2573069e4b67205353fe3469dbe7bd`)
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## First failed gate

The exact-source-statement gate in section 5.1 of `Docs/Stage1_Blueprint_rev-5.6.md` cannot be
truthfully entered. The repository record supplies only the field label `深度学习` (deep learning),
the attribution "many mathematicians," the date "twenty-first century," and the noun phrase
`深层神经网络` (deep neural networks). It contains no cited truth-valued proposition, architecture,
domains, ordered binders, hypotheses, conclusion, proof boundary, or boundary cases. Stage0
explicitly leaves the precise definitions and premises, proof route, dependencies, alternate forms,
axioms, formal system, machine status, and artifacts open. The catalog's `已验证` value is untrusted
metadata under rev-5.6.

The wording names a research field and model family, not one theorem. It does not select whether the
root concerns a definition, universal approximation, deep-versus-shallow expressiveness, tensor
rank, optimization, training convergence, generalization, robustness, verification, or complexity.
It also leaves the network representation, depth and widths, activation and operations, input and
output domains, parameters, data and probability semantics, loss and optimizer, constants,
quantifier order, arithmetic model, and exceptional cases unresolved. Those choices yield
materially inequivalent propositions. Selecting one from familiarity would invent, narrow,
broaden, or substitute proposition-changing mathematics rather than elaborate the received target.

The inspected Goodfellow-Bengio-Courville book chapter and LeCun-Bengio-Hinton review are field
definition or survey leads, not catalog-selected theorem sources. Cohen-Sharir-Shashua Theorem 1
and Corollary 2, and Bentkamp's Isabelle/HOL
`fundamental_theorem_network_capacity_v3`, are specific expressiveness leads. The catalog cites none
of them. The Isabelle theorem is outside the pinned Lean dependency closure, and neither its exact
source mapping nor a target correction has received independent review. Choosing it because its
title matches "deep learning" would be an unauthorized substitution.

Consequently there is no canonical Lean expression to elaborate, no honest minimal-import claim,
and no canonical expression or environment fingerprint. Credited transports and the required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are undefined
until an accepted source-correct proposition fixes the binders and premises. No `Statement.lean`,
theorem declaration, proof body, weakened special case, or broadened interface was added. The root
remains `[H5, M4, R4]`; this classification does not deny correctly stated deep-learning results.

The prerequisite intake is only provisional worker state `[_]`. Its receipt is unaccepted,
non-content-addressed, has no accepted receipt ID, and binds repository base
`e552e0758e29de307cf357a703e6ecd16e40fb69` plus older blueprint and execution-DAG hashes. Current
authority records one provisional intake attempt, so the historical intake checker fails at its
frozen `[ ]`/zero-attempt assertion. This statement phase records rather than rewrites that
historical evidence. The absent exact source proposition independently and decisively blocks the
statement deliverable.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. Its two direct
imports expose holors, CP-rank infrastructure, and general polynomial density. All seven `#check`
commands and three representative axiom reports passed; the reports contain only `propext`,
`Classical.choice`, and `Quot.sound`. The probe defines no neural network, activation, training
semantics, deep-versus-shallow comparison, source-selected target, transport, or proof body. Its
imports therefore cannot be certified minimal for an unidentified target and receive no statement
or proof credit.

A bounded exact-topic search over the owned, repo-local, and pinned-mathlib Lean roots matched only
the probe disclaimer and the `Mathlib.Data.Holor` comment citing the AFP tensor library. It located
no source-identical deep-learning target declaration. This is narrow statement-feasibility evidence,
not the downstream immutable anchor audit or a global absence claim.

The environment is Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No `lake update`, `lake build`, dependency
clone or fetch, or other `.lake` mutation was run.

## Validation evidence

Commands ran in this isolated worker clone on 2026-07-13 (Asia/Shanghai), from the repository root
unless another working directory is shown. Exact argument arrays and results are preserved in
`statement-blocker.json`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1486` | 0 | rank 1163, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `python3 -B Stage1_Instances/THM-M-1486/check_intake.py` | 1 | historical intake replay reached its frozen `[ ]`/zero-attempt assertion; current authority records provisional `[_]`/one attempt |
| `cd Formalizations/Lean && lake env lean --version` and `lake --version` | 0 | Lean and Lake agree with the pinned environment above |
| mathlib revision/tree and package-status checks | 0 | revision and tree agree with the fingerprint; package worktree is clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-1486/IntakeProbe.lean` | 0 | seven adjacent APIs and three axiom reports elaborated; combined-output SHA-256 `ddffe5aa8b59fc112c713e5e44ddd3f3c435043c4941bc4d61e8918a4c597ded`; no canonical target was stated |
| bounded exact-topic search recorded in `statement-blocker.json` | 0 | only the probe disclaimer and one mathlib provenance comment matched; no source-identical target declaration was found |
| prohibited Lean construct scan over owned `*.lean` files | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, or unsafe declaration |
| JSON, scoped invariant, final-newline, and whitespace checks recorded in `statement-blocker.json` | 0 | identity, null target, undefined mutations, unchanged debt, false completion flags, exact path scope, absent self-test, and clean formatting agree |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test manifest exists because the exact-statement deliverable is blocked |

## Retry condition

The integration lane must first revalidate and master-accept refreshed intake evidence. Accountable
reviewers must then lawfully preserve and hash one immutable primary or approved authoritative
source, select and transcribe one exact truth-valued proposition with pinpoint locators, audit its
proof boundary, corrections, and errata, reconcile neighboring-target ownership, and independently
approve the source-to-statement mapping. The decision must freeze the architecture, data and
function domains, network semantics, parameters, activations and operations, training or
probability semantics when relevant, ordered binders, hypotheses, conclusion, constants,
quantifier order, arithmetic boundary, alternate encodings, and every degenerate case.

A later statement worker can then encode precisely that claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and run all four required mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node.
`audit_complete` and `theorem_complete` remain false. Because the assigned phase is not genuinely
self-tested to its completion gate, no `.stage1-worker-selftest.json`, node receipt, worker `[_]`,
or master acceptance is claimed.
