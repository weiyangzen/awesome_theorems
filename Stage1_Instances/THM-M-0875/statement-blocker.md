# THM-M-0875 exact-statement gate: blocked

- Item: `S56-M-0875-STATEMENT`
- Base revision: `db4b8793e70ce8af74c9c9490acfa50aa3684d5e`
- Base tree: `6434a20532ae7c523ad293e67a6228ab384bfb8a`
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The complete mathematical wording is the algorithm-family title `Weisfeiler-Lehman算法` and the
gloss `图同构的启发式算法`, literally "a heuristic algorithm for graph isomorphism." This is not a
truth-valued proposition with fixed definitions, ordered binders, hypotheses, and conclusion.

The wording does not select any one of these inequivalent candidates:

- the original finite-multigraph ordered-arc or coherent-closure procedure;
- modern one-dimensional vertex color refinement;
- a `k`-dimensional tuple refinement;
- isomorphism invariance or sound nonisomorphism rejection;
- stabilization or a complexity bound for a fixed implementation;
- completeness on a precisely identified graph class; or
- a limitation or counterexample theorem.

The intake's strongest historical lead is B. Yu. Weisfeiler and A. A. Leman's *The Reduction of a
Graph to Canonical Form and the Algebra Which Appears Therein*, in Grigory Ryabov's English
translation, together with the WL2018 historical preface. Those materials are discovery evidence,
not an accepted source selection. The original procedure is not interchangeable with modern
`1-WL` or `k-WL`, and the preface explicitly says that the original conjectures that the method
solves graph isomorphism were incorrect. Generic graph-isomorphism completeness is therefore not a
permitted fallback.

The record also fixes no graph representation, vertex or color carrier, finiteness and decidability
context, initialization, refinement update, color-renaming semantics, comparison and stopping
rules, output, dimension, cost or computation model, quantifier order, or boundary cases. Choosing
these would invent or substitute proposition-changing mathematics rather than elaborate the
received target. Nearby records `THM-M-0873`, `THM-M-0874`, `THM-M-0876`, and `THM-M-1567` do not
transfer their scope or evidence by topical proximity.

Rev-5.6 permits this provisional later-node attempt, but the prerequisite intake remains worker
state `[_]`: its receipt declares `accepted: false`, is not content-addressed, and has no accepted
receipt ID. That would independently prevent accepted closure. The first gate failed here is exact
source-statement and target identity. Intake deliberately freezes `canonical_statement`, the
canonical claim, Lean module and expression, elaborated-expression hash, and canonical-target
environment fingerprint as null. Sections 5 and 5.1 make that ambiguity and missing fingerprint
hard blockers. With no target, minimal imports and the removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations are undefined rather than failed Lean tests. The
vector remains `[H5, M4, R4]`.

## Pinned Lean Boundary

The discovery-only `IntakeProbe.lean` re-elaborates with the single direct import
`Mathlib.Combinatorics.SimpleGraph.Finite`. It checks finite simple graphs, graph isomorphisms,
neighborhoods, degrees, finite filtering, and cardinality. All eleven interfaces elaborate in the
pinned environment. The two printed library axiom reports contain only `propext` and `Quot.sound`.

This is real adjacent-substrate validation, but the probe defines no Weisfeiler-Leman refinement,
canonical target, checked source transport, or proof body. Its import therefore cannot be certified
as minimal for an absent target and receives no statement or proof credit. A bounded exact-topic
search found only the probe's disclaimer and no Weisfeiler-Leman or color-refinement declaration in
pinned mathlib or repository-local Lean. This is narrow feasibility evidence, not the downstream
anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No `lake update`, `lake build`, dependency
clone or fetch, or other dependency mutation was run.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai). Lean commands ran from
`Formalizations/Lean`; all others ran from the repository root unless noted. Exact argument and
result records and current input hashes are preserved in `statement-blocker.json`. That JSON is an
ad hoc worker blocker report using a repository-local compatibility label, not a published strict
schema or node receipt.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0875` | 0 | rank 1429; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree are recorded above |
| scoped reads of the blueprint, skill, manifest, catalog, Stage0 record, execution DAG, and complete intake dossier | 0 | confirmed the provisional dependency, null target, inequivalent roots, and unresolved proposition-defining inputs |
| recorded `sha256sum` over named authority, source, intake, toolchain, lockfile, and directly imported mathlib sources | 0 | current digests are recorded in the structured blocker |
| pinned Lean, Lake, and mathlib revision/tree/status checks | 0 | Lean 4.29.0, Lake 5.0.0, and the expected clean pinned mathlib revision and tree |
| `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0875/IntakeProbe.lean` | 0 | eleven adjacent APIs elaborated; output SHA-256 `22b76ee5...7ef9a`; no target or proof body was declared |
| bounded Weisfeiler-Leman/color-refinement search in pinned mathlib and repo-local Lean | 0 | the only match was the probe disclaimer; no exact-topic declaration matched; discovery evidence only |
| `python3 -B Stage1_Instances/THM-M-0875/check_intake.py` | 1 | historical intake replay stopped because the authoritative DAG intake row changed after integration; this phase did not rewrite historical evidence |
| JSON parse, scoped blocker invariants, and prohibited-construct scan | 0 aggregate | structured blocker is valid; identity, null target, unchanged vector, false completion fields, exact scope, and no proof escape agree |
| scoped whitespace checks | 0 / 1 expected differences | tracked check passed; each new-file no-index check exited 1 only because the file differs from `/dev/null`, with no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement completion gate failed |

The intake validator is frozen to the authority inputs and nine-file inventory of the earlier intake
attempt. Integration later changed the authoritative DAG intake state and attempt count, so replay
already fails its stored exact-row assertion. Adding these statement blocker artifacts also makes
its original intake-only inventory historical. This phase records that boundary rather than
rewriting the intake checker, receipt, instance, task DAG, generated blueprint, or authoritative
execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must master-accept a fresh intake receipt bound to the current authority.
Accountable reviewers must preserve and hash an immutable primary or approved authoritative source,
select and independently approve one exact Weisfeiler-Leman proposition, and transcribe every
incorporated definition, ordered binder, hypothesis, conclusion, proof boundary, correction,
erratum, and boundary case while preserving neighboring-target ownership. They must fix the
historical or modern algorithm variant, graph and color domains, dimension, initialization, update,
renaming, comparison, stopping rule, output, cost, computation model, exact conclusion, and all
degenerate cases.

A fresh statement attempt can then encode precisely that approved source claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and run the removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case
mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt change is proposed. Because the exact-statement deliverable did
not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or master acceptance
is claimed.
