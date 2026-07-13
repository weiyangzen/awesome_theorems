# THM-M-0967 exact-statement gate: blocked

- Item: `S56-M-0967-STATEMENT`
- Base revision: `72e9e8092182121a6794921f61fcc9cae22f726d`
- Base tree: `0d6c1fdf06d1573c256af331c6b198e5a787af43`
- Attempt date: 2026-07-13 (`Asia/Shanghai`)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The complete catalog wording is only `Kneser图的色数` ("the chromatic number of the Kneser
graph"), attributed to Laszlo Lovasz in 1978. It does not define the graph, name its two parameters,
state their domain or range, give a chromatic-number formula, select a ground set or vertex
representation, fix ordered binders and typeclass assumptions, or resolve degenerate cases. The
catalog's verified-status label is untrusted inventory metadata under rev-5.6.

The likely primary publication is L. Lovasz, *Kneser's conjecture, chromatic number, and homotopy*,
Journal of Combinatorial Theory, Series A 25(3) (1978), 319-324, DOI
`10.1016/0097-3165(78)90022-5`. Intake admitted bibliographic metadata and a secondary abstract,
not the article body, its incorporated definitions, an exact result passage, parameter translation,
proof boundary, corrections, errata, durable immutable source copy, or independent review. The
secondary abstract states a disjoint-subset coloring form, but it cannot select the repository's
canonical clauses. This evidence supports the theorem family at `H1`, not an approved exact target.

The familiar modern equality `chi(KG(n,k)) = n - 2*k + 2`, normally restricted by `0 < k` and
`2 * k <= n`, is explicitly uncredited in the intake. Promoting it from mathematical familiarity
would invent the parameter range, graph definition, formula, and conventions missing from the
received record. It would also require substantive choices between `Fin n` and an arbitrary finite
ground type, finite-subset representations, `ENat` equality and colorability minimality, natural
subtraction and coercion conventions, and the cases `k = 0`, `n < k`, `n < 2 * k`, `n = 2 * k`, and
`k = 1`. These choices change the proposition or require checked transports; they are not notation.

The prerequisite `S56-M-0967-INTAKE` is only provisional worker state `[_]`, not master-accepted
state `[x]`. Its receipt declares `accepted: false`, is unsigned and not content-addressed, and has
no accepted receipt ID. Its historical checker also binds the former authoritative `[ ]`/attempt-0
cursor, while integration now records `[_]`/attempt 1, so replay correctly fails closed.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing expression
fingerprint hard blockers. The intake therefore correctly leaves the canonical claim, Lean module
and expression, imports, expression hash, environment fingerprint, binders, hypotheses, and
credited alternate forms null or empty at `[H1, M4, R4]`. Without a canonical target, imports
cannot be certified minimal, transports cannot be credited, and the required removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations are undefined, not passed.

No `Statement.lean`, axiom, placeholder, standard-but-unapproved encoding, weakened theorem, or
broadened substitute was added. Lifecycle remains `planned`, the item remains `[ ]`, and the root
remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates with two direct imports:

- `Mathlib.Combinatorics.SimpleGraph.Coloring`
- `Mathlib.Data.Fintype.Powerset`

It authenticates fixed-cardinality finite subsets, finite-set disjointness, relation-generated
simple graphs, colorings, and mathlib's `ENat`-valued chromatic number. It also checks the candidate
graph definition over `{s : Finset (Fin n) // s.card = k}`. The complete output has SHA-256
`28cd7a45b7dea7b13c9e0062a2990bb84f747256a854e83412d84d7b19752357`. A bounded exact-topic
search found no Kneser-graph or Lovasz-Kneser target in pinned mathlib or repository-local Lean;
the only external match was an unrelated additive Freiman-Kneser URL. This is bounded discovery
evidence, not an exhaustive anchor audit or proof of global absence.

The probe declares no theorem, source transport, or proof body, and its imports cannot be certified
minimal for an absent canonical target. Its fixed-subset and chromatic-minimality checks report
`propext`, `Classical.choice`, and `Quot.sound`; `SimpleGraph.fromRel_adj` reports no axioms. The
environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

The automation-provided `Formalizations/Lean/.lake` link was used read-only. No `lake update`,
`lake build`, dependency clone or fetch, or other `.lake` mutation was run.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (`Asia/Shanghai`). Lean commands ran from
`Formalizations/Lean`; all others ran from the repository root unless noted.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0967` | 0 | rank 1501; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree are recorded above |
| scoped reads and SHA-256 checks of authority, catalog, Stage0, intake, toolchain, lockfile, probe, and pinned mathlib inputs | 0 | confirmed the provisional dependency, null target, unresolved source clauses, and fingerprints recorded in `statement-blocker.json` |
| `git blame -L 7064,7069 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `python3 -B Stage1_Instances/THM-M-0967/check_intake.py` | 1 | historical intake replay stops because its checker expects authority state `[ ]`/attempt 0, while integration now records provisional `[_]`/attempt 1; the checker was preserved |
| `lake env lean --version`; `lake --version` | 0 | pinned Lean 4.29.0 and Lake 5.0.0 versions recorded above |
| pinned mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree agree; dependency worktree is clean |
| `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0967/IntakeProbe.lean` | 0 | fixed-subset, disjointness-graph, and coloring interfaces elaborated; complete output hash recorded above; no target or proof body |
| bounded exact-topic `rg` search over pinned mathlib and repository-local Lean | 0 with scoped matches | only the intake probe and an unrelated additive-theorem URL matched; no exact Kneser-graph target was found; discovery only |
| finalized JSON parse, scoped blocker assertions, prohibited-construct scan, and whitespace checks | 0 | blocker identity, null target/import/hash fields, unchanged vector, four undefined mutations, false completion fields, exact two-file scope, and absent self-test agree |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence. Accountable independent
reviewers must then lawfully preserve and hash an immutable primary edition, approve the exact
result and incorporated definitions, and freeze the parameter domains and range, graph and ground
set, vertex and adjacency encodings, chromatic-number codomain, arithmetic and coercions, ordered
binders, all hypotheses, conclusion, logical profiles, and every boundary case.

A fresh statement worker may then encode only that reviewed claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. `audit_complete: false` and `theorem_complete: false`; no debt-vector change is
proposed. Because the exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`,
statement receipt, worker `[_]`, master acceptance, statement fingerprint, or proof credit is
claimed.
