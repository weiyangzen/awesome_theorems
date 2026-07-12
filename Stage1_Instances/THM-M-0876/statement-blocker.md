# THM-M-0876 exact-statement gate: blocked

- Item: `S56-M-0876-STATEMENT`
- Base revision: `35681bf154be61836528486ed7830f619fc03231`
- Base tree: `b45fc969fef64ad53ac30dc548894b08e8bef834`
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The complete mathematical wording is the topic `图同构的复杂性` (complexity of graph
isomorphism) and the gloss `图同构在NP与P之间的位置`, literally "the position of graph
isomorphism between NP and P." This is a classification question, not one truth-valued proposition
with fixed definitions, ordered binders, hypotheses, and conclusion.

The wording does not select any one of these inequivalent candidates:

- membership of a fixed graph-isomorphism decision language in NP;
- the open proposition that graph isomorphism belongs to P;
- membership in `NP \ P` or a conditional NP-intermediacy theorem;
- Babai's deterministic quasipolynomial-time upper bound; or
- a typed ledger separating known upper bounds, conditional consequences, and open branches.

In particular, "between" cannot be encoded as `GI ∈ NP \ P`: the repository supplies neither
nonmembership in P nor the assumptions and reductions needed for an intermediacy result. The record
also fixes no graph representation, input serialization, malformed-input policy, isomorphism
predicate, machine and cost model, complexity-class definition, reduction, asymptotic convention,
quantifier order, or boundary case. Choosing these would invent or substitute proposition-changing
mathematics rather than elaborate the received target.

The most obvious known upper-bound branch is not a silent fallback. The intake records László
Babai's *Graph Isomorphism in Quasipolynomial Time*, arXiv `1512.03547v2`, only as a discovery lead.
Its later flaw/repair history has not been audited there, and the generic quasipolynomial result and
Babai algorithm are separately scheduled as `THM-M-0873` and `THM-M-0874`. `THM-M-0875` owns the
Weisfeiler-Lehman topic, while `THM-M-1567` is a separate duplicate-domain catalog record. None can
transfer a statement or proof body to this target by topical proximity.

Rev-5.6 permits this provisional later-node attempt, but the prerequisite intake remains worker
state `[_]`: its receipt declares `accepted: false` and has no accepted receipt ID. That would
independently prevent accepted closure. The first gate failed by this attempt is exact source and
target identity: intake deliberately freezes `canonical_statement`,
`canonical_claim`, the Lean module and expression, the expression hash, and the canonical-target
environment fingerprint as null. Rev-5.6 sections 5 and 5.1 make that ambiguity and missing
fingerprint hard blockers. With no target, minimal imports and the removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations are undefined rather than failed
Lean tests. The vector remains `[H5, M4, R4]`.

## Pinned Lean Boundary

The discovery-only `IntakeProbe.lean` re-elaborates with these direct imports:

- `Mathlib.Combinatorics.SimpleGraph.Maps`
- `Mathlib.Computability.Language`
- `Mathlib.Computability.Reduce`

It checks `SimpleGraph.Iso` and its elementary identity, symmetry, and composition interfaces,
`Language`, `ManyOneReducible`, and `OneOneReducible`. All seven checks pass under the pinned
environment. They provide graph-isomorphism witnesses, unbounded formal languages, and computable
reductions only. The probe defines no finite graph encoding, decision language, resource-bounded P
or NP class, quasipolynomial-time predicate, complexity theorem, canonical target, checked source
transport, or proof body. These imports therefore cannot be certified as minimal target imports and
receive no statement or proof credit.

A bounded exact-topic search returned no graph-isomorphism complexity, polynomial-time,
quasipolynomial, or P/NP declaration in pinned mathlib or repository-local Lean under the recorded
patterns. This is narrow feasibility evidence, not the downstream anchor audit or a claim of global
formal absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No `lake update`, `lake build`, dependency
clone or fetch, or other dependency mutation was run.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai). Lean commands ran from
`Formalizations/Lean`; all others ran from the repository root unless noted. Exact argument and
result records for executable checks, current authority hashes, and pinned-source hashes are
preserved in `statement-blocker.json`. The JSON is an ad hoc worker blocker report using a
repository-local compatibility label, not a published strict schema or node receipt.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0876` | 0 | rank 1017; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree are recorded above |
| scoped reads of the blueprint, skill, manifest, catalog, Stage0 record, execution DAG, and complete intake dossier | 0 | confirmed provisional dependency, null target, inequivalent roots, and unresolved proposition-defining inputs |
| recorded `sha256sum` argv over named authority, source, complete intake, toolchain, lockfile, and directly imported mathlib sources | 0 | exact current digests for every listed file are recorded in the structured blocker |
| pinned Lean, Lake, and mathlib revision/tree/status checks | 0 | Lean 4.29.0, Lake 5.0.0, expected clean pinned mathlib revision and tree |
| `lake env lean ../../Stage1_Instances/THM-M-0876/IntakeProbe.lean` | 0 | seven adjacent APIs elaborated; output SHA-256 `f312f54d...acf8`; no target or proof body was declared |
| bounded exact-topic search in pinned mathlib and repo-local Lean | 1 expected | no match under the recorded patterns; discovery-only feasibility evidence |
| `python3 -B Stage1_Instances/THM-M-0876/check_intake.py` | 1 | historical intake replay stopped on a stale blueprint input hash after integration changed authority bytes; this phase did not rewrite it |
| JSON parse, scoped blocker invariants, and prohibited-construct scan | 0 aggregate | structured blocker is valid; identity, null target, unchanged vector, false completion fields, exact scope, and no proof escape agree |
| scoped whitespace checks | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement completion gate failed |

The intake checker is frozen to the authority inputs and nine-file inventory of the earlier intake
attempt. The integration lane later changed the generated blueprint and DAG, so replay already
fails its stored blueprint digest. Adding these statement blocker artifacts also makes its original
intake-only inventory historical. This phase records that boundary rather than rewriting the intake
checker, receipt, instance, task DAG, generated blueprint, or authoritative execution DAG to
manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must master-accept a fresh intake receipt bound to the current authority.
Accountable reviewers must then preserve and hash one immutable primary or approved authoritative
source, select and independently approve one exact theorem, open proposition, or typed branch
ledger, and transcribe every incorporated definition, ordered binder, hypothesis, conclusion,
proof boundary, correction, and boundary case. They must resolve root and evidence ownership
relative to `THM-M-0873`, `THM-M-0874`, `THM-M-0875`, and `THM-M-1567`.

A fresh statement attempt can then freeze the graph and input encodings, decision predicate,
machine and cost semantics, complexity classes, reductions, assumptions, constants, asymptotic
conventions, and degenerate cases; encode precisely the approved claim in Lean; prove its pinned
direct imports minimal; serialize and hash the elaborated expression and environment; compile every
credited transport; and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt change is proposed. Because the exact-statement deliverable did
not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or master acceptance
is claimed.
