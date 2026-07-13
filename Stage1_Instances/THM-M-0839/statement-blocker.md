# THM-M-0839 exact-statement gate: blocked

- Item: `S56-M-0839-STATEMENT`
- Base revision: `a3b18eec39bf04be025b1641cae02f4d44fdf11a`
- Base tree: `fdfff18dea4c6798c5b322b6088dfe556109c134`
- Attempt date: 2026-07-13 (`Asia/Shanghai`)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The complete mathematical wording says only that graph perfectness is equivalent to complement
perfectness, attributed to Laszlo Lovasz in 1972. It does not define a perfect graph, select finite
simple undirected loopless graphs, state the all-induced-subgraphs quantifier, choose a subset or
subgraph encoding, fix chromatic and clique number codomains and coercions, state ordered binders or
typeclass hypotheses, approve same-carrier complement transport, or settle degenerate cases. The
catalog's verified-status label is untrusted inventory metadata under rev-5.6.

The two direct 1972 source leads do not resolve those choices. The intake admitted bibliographic
metadata and published abstracts for Lovasz's *Normal hypergraphs and the perfect graph conjecture*
and *A characterization of perfect graphs*. It did not admit either full text, incorporated
definitions, an exact numbered result, proof passage, corrections, errata, durable lawful source
copy, or independent review. The abstracts support the weak perfect graph theorem family at `H1`;
they do not supply an approved binder-complete proposition.

Singh and Natarajan's 2019/2020 Coq formalization paper is a precise secondary discriminator. It
uses finite simple graphs and defines perfectness through equality of chromatic and clique numbers
for every induced subgraph, then states the complement equivalence. Promoting that conventional
reading would still invent clauses not approved from the primary source. In pinned mathlib,
chromatic number is `ENat` while clique number is `Nat`, so even the equality requires a substantive
coercion decision. Choosing `Set V` induction, a subgraph family, explicit finiteness, a `Finite`
typeclass, or any particular empty-case convention would likewise change the Lean proposition.

The prerequisite `S56-M-0839-INTAKE` is only provisional worker state `[_]`, not master-accepted
state `[x]`. Its receipt declares `accepted: false`, is not content-addressed, and contains no
accepted receipt ID. This independently prevents an accepted statement transition.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing elaborated
expression fingerprint hard blockers. The intake therefore correctly leaves the canonical human
claim, Lean module and expression, target imports, expression hash, environment fingerprint,
binders, hypotheses, and credited alternate forms null or empty at `[H1, M4, R4]`. Without a
canonical target, imports cannot be certified minimal, transports cannot be credited, and the
required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are
undefined, not passed.

No `Statement.lean`, axiom, placeholder, assumed perfectness predicate, standard-but-unapproved
encoding, weakened theorem, or broadened substitute was added. Lifecycle remains `planned`, the
item remains `[ ]`, and the root remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates with its sole direct import,
`Mathlib.Combinatorics.SimpleGraph.Coloring`. It authenticates:

- `SimpleGraph.compl_adj` and `SimpleGraph.induce`;
- `SimpleGraph.chromaticNumber : SimpleGraph V -> ENat`;
- `SimpleGraph.cliqueNum : SimpleGraph V -> Nat`;
- the coercing lower bound `SimpleGraph.cliqueNum_le_chromaticNumber`; and
- `SimpleGraph.cliqueNum_compl`.

The complete probe output has SHA-256
`305109dcab2f4d12882f073a3b7f72027f6ac511b3e86364066f763ec86f815d`. A bounded exact-topic
search over repository-local and pinned-mathlib Lean returned no graph-perfectness predicate or weak
perfect graph theorem; its empty stdout has SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. That is narrow discovery
evidence, not an exhaustive anchor audit or proof of global absence. The probe defines no
perfectness predicate, canonical target, source transport, or proof body, and its import cannot be
certified minimal for an absent target.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` link was used read-only. No `lake update`, `lake build`, dependency clone
or fetch, or other `.lake` mutation was run.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (`Asia/Shanghai`). Lean commands ran from
`Formalizations/Lean`; all others ran from the repository root unless noted.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0839` | 0 | rank 1396; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree are recorded above |
| scoped reads and SHA-256 checks of the authority, source, intake, toolchain, lockfile, probe, and relevant pinned mathlib inputs | 0 | confirmed the provisional dependency, null target, unresolved source clauses, and exact fingerprints recorded in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-0839/check_intake.py` | 1 | the historical intake checker expects authority state `[ ]`, while integration now records provisional `[_]`; historical evidence was preserved rather than weakened |
| `lake env lean --version`; `lake --version` | 0 | pinned Lean 4.29.0 and Lake 5.0.0 versions recorded above |
| pinned mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree agree; dependency worktree clean |
| `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0839/IntakeProbe.lean` | 0 | six adjacent graph APIs elaborated; complete stdout hash recorded above; no target or proof body |
| bounded exact-topic `rg` search over pinned mathlib and repository-local Lean | 1, expected no match | empty output hash recorded above; discovery only |
| prohibited-construct scan over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| finalized JSON parse, scoped blocker assertions, and whitespace checks | 0 | blocker identity, null target/import/hash fields, unchanged vector, four undefined mutations, false completion fields, exact two-file scope, and absent self-test agree |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The intake checker is bound to its intake-time authority state. Integration has since promoted only
the provisional intake cursor to `[_]`, so the checker fails closed on that changed input. It was
not edited or represented as passing for this statement attempt.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence. Accountable independent
reviewers must then lawfully preserve and hash an immutable primary edition, approve the exact
theorem and incorporated definitions, and freeze the graph domain, perfectness quantification,
invariant codomains and coercions, complement transport, ordered binders, all hypotheses,
conclusion, logical profiles, and every boundary case.

A fresh statement worker may then encode only that reviewed claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. `audit_complete: false` and `theorem_complete: false`; no debt-vector change is
proposed. Because the exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`,
statement receipt, worker `[_]`, master acceptance, statement fingerprint, or proof credit is
claimed.
