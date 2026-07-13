# THM-M-1481 exact-statement gate: blocked

- Item: `S56-M-1481-STATEMENT`
- Base revision: `2b649e7f3c2c6e3617cfb58c680e29f34d2ca5d7` (tree
  `c9dfabc312a58c05c89917f6d7298a8e140356fc`)
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## First failed gate

The exact-statement gate in section 5.1 of `Docs/Stage1_Blueprint_rev-5.6.md` cannot be
truthfully entered from the authoritative record. The mathematics catalog supplies only the title
"simulated annealing," Scott Kirkpatrick, 1983, and the gloss "a randomized method for global
optimization." It gives no cited truth-valued proposition, definitions, ordered binders,
hypotheses, conclusion, or boundary cases. Stage0 explicitly leaves the precise definitions,
premises, proof route, equivalent forms, axioms, machine status, and artifacts open. The catalog's
`已验证` value is untrusted metadata under rev-5.6.

The wording identifies a method family, not one theorem. It does not choose between the 1983
heuristic framework, a later finite-state cooling-convergence theorem, a fixed-temperature Gibbs
invariance result, or correctness of a concrete implementation. These alternatives require
materially different state and cost spaces, proposal graphs or kernels, acceptance laws,
temperature and schedule conventions, energy-barrier definitions, process constructions,
convergence modes, quantifier orders, and conclusions. Selecting one from convention would invent,
narrow, broaden, or substitute mathematics rather than elaborate the received target.

The inspected Kirkpatrick-Gelatt-Vecchi 1983 article describes a Metropolis rule, staged cooling,
and numerical studies, but does not state one exact general convergence theorem matching the
catalog gloss. Hajek's 1988 cooling-schedule theorem family is a later, narrower lead and cannot be
silently substituted for a record attributed to Kirkpatrick in 1983. Neither source has been
admitted here as an immutable, pinpointed proposition with all incorporated definitions, proof and
errata crosswalk, and independent review.

Consequently there is no canonical expression to elaborate, no honest minimal-import claim, and no
canonical expression or environment fingerprint. Checked transports and the required removed-
hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are undefined until a
source-correct statement fixes the binders and premises. The intake vector remains
`[H5, M4, R4]`; no debt change is proposed. No `Statement.lean`, axiom, placeholder, stored
convergence hypothesis, or substituted theorem was introduced.

The intake prerequisite is only provisional `[_]`, and its worker receipt is unaccepted and not
content-addressed. This independently prevents statement-node acceptance. Its historical checker
also freezes the old authoritative intake state `[ ]` with zero attempts and therefore no longer
replays after integration recorded `[_]` with one attempt. This phase does not rewrite historical
intake evidence to manufacture freshness. The first statement-specific failure remains the absent
exact source proposition.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. Its three imports
expose generic finite-minimum, Markov-kernel, invariance, reversibility, and irreducibility APIs, and
all seven `#check` commands passed. The probe defines no annealing transition, cooling schedule,
process, or convergence proposition, and its imports cannot be certified minimal for an
unidentified target. This check receives no statement, anchor, or proof credit.

A bounded case-insensitive search of repo-local Lean and pinned mathlib located no source-identical
simulated-annealing, cooling-schedule, or Metropolis target declaration. This is narrow feasibility
evidence, not the downstream immutable anchor audit or a global absence claim.

The environment is Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided
`Formalizations/Lean/.lake` symlink points to the canonical pinned artifacts and was used read-only.
No `lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai), from the repository root unless a
different working directory is shown. Exact argument arrays and results are preserved in
`statement-blocker.json`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1481` | 0 | rank 1158, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree are recorded above |
| scoped reads and hash checks of the catalog, Stage0, target authorities, and intake artifacts | 0 | only a method-family gloss is authoritative; every proposition-changing choice remains open |
| `python3 -B Stage1_Instances/THM-M-1481/check_intake.py` | 1 | historical intake replay reached its frozen `[ ]`/zero-attempt assertion; current authority records provisional `[_]`/one attempt |
| `cd Formalizations/Lean && lake env lean --version` and `lake --version` | 0 | Lean and Lake agree with the pinned environment above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | revision and tree agree with the fingerprint; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1481/IntakeProbe.lean` | 0 | all seven adjacent APIs elaborated; output SHA-256 `dacfcbac...f6848f5`; no canonical target was stated |
| bounded exact-topic `rg` search recorded in `statement-blocker.json` | 1 | expected no-match result; no source-identical declaration was found in the bounded Lean roots |
| prohibited Lean construct scan over owned `*.lean` files | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, or unsafe declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-1481/statement-blocker.json` | 0 | structured blocker parses as JSON |
| scoped invariant and whitespace checks recorded in `statement-blocker.json` | 0 | identity, null target, undefined mutations, unchanged debt, false completion flags, exact path scope, absent self-test, and clean whitespace agree |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test manifest exists because the exact-statement deliverable is blocked |

## Retry condition

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers must
then preserve and hash one immutable primary or approved authoritative source, select and
transcribe one exact truth-valued claim and all incorporated definitions with pinpoint locators,
audit corrections and errata, reconcile neighboring-target ownership, and independently approve
the source-to-statement mapping. The decision must freeze the state and cost spaces, proposal
mechanism, acceptance law, schedule and energy depth, stochastic process and initial condition,
convergence mode and quantifier order, arithmetic model, ordered binders, hypotheses, conclusion,
alternate encodings, and every degenerate or boundary case.

A later statement worker can then encode precisely that claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and run all four required mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node.
`audit_complete` and `theorem_complete` remain false. Because the assigned phase is not genuinely
self-tested to its completion gate, no `.stage1-worker-selftest.json`, node receipt, worker `[_]`,
or master acceptance is claimed.
