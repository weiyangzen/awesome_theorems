# THM-M-0877 exact-statement gate: blocked

- Item: `S56-M-0877-STATEMENT`
- Base revision: `fcabbf1e0ad9507eebe91663bccabfa87d22813e`
- Base tree: `873e589c594454b7f263c7ed2342089a4d15e842`
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The complete mathematical wording is the title `网络流` (network flow), attribution to many
mathematicians in the twentieth century, and the gloss `最大流与最小割理论` (max-flow and min-cut
theory). The catalog cites no work or theorem and contains no network definition, ordered binder,
hypothesis, conclusion, proof boundary, correction, erratum, reviewer, or formal declaration.
Stage0 explicitly leaves precise definitions and premises open, and the catalog's `已验证` label is
untrusted under rev-5.6.

That wording denotes a subject and theorem family, not one proposition. It does not choose weak
duality, max-flow/min-cut equality, existence or attainment of optima, integrality, an
augmenting-path characterization, or correctness, termination, and complexity of an algorithm.
These claims have different hypotheses, conclusions, and proof architectures. The repository also
fixes none of the graph or network representation; source and sink conventions; capacity and flow
carriers; path-flow versus edge-flow semantics; conservation and feasibility; partition-cut versus
disconnecting-edge-set semantics; extrema; ordered binders; or boundary cases.

The neighboring ownership boundary is decisive. `THM-M-0814` separately owns the explicit
max-flow/min-cut equality and Ford/Fulkerson attribution. Its statement selects Ford and Fulkerson's
1956 finite undirected, positive-capacity, weighted-chain-flow formulation with disconnecting arc
sets. That is not interchangeable with the familiar directed conservation-flow formulation, and it
cannot be copied here without an accountable duplicate or theorem-family decision. Selecting it or
another familiar branch would invent, narrow, broaden, duplicate, or substitute proposition-changing
mathematics rather than elaborate this exact received target.

The target remains sensitive to empty vertex or edge types, absent source-to-sink paths, isolated
vertices, equal terminals, loops and parallel arcs, zero capacities, empty flows and cuts, infeasible
networks, capacity overflow, integral versus fractional values, and maximum/minimum attainment
versus supremum/infimum. None can be silently decided by convention.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing expression
fingerprint hard blockers. The intake correctly leaves `canonical_statement`, `canonical_claim`,
the Lean module and expression, minimal target imports, elaborated-expression hash, and
canonical-target environment fingerprint null at `[H5, M4, R4]`. Consequently, checked alternate
transports and the required removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations are undefined, not passed. No `Statement.lean`, theorem declaration,
proof body, assumed optimizer interface, weakened special case, or broadened theorem was introduced.

The prerequisite `S56-M-0877-INTAKE` is only provisional worker state `[_]`. Its receipt declares
`accepted: false`, is not content-addressed, supplies no accepted receipt ID, and remains unaccepted
by the master. Rev-5.6 section 10.2 permits this provisional blocker preparation, but the unfinished
dependency independently prevents accepted statement closure.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates with the pinned environment. It checks
six adjacent undirected-graph, directed-graph, finite-sum, and finite-maximum APIs. The probe defines
no capacities, feasible flow, conservation law, cut, optimum, canonical target, checked source
transport, or proof body. Its four combined imports therefore cannot be certified as minimal imports
for an absent target and receive no statement or proof credit.

A bounded exact-topic search of the repository Lean library roots and pinned mathlib found no
declaration named for max flow, min cut, network flow, or Ford-Fulkerson. `Stage1_Instances` was
deliberately outside that query; the known `THM-M-0814` neighbor was inspected separately. This is
discovery-only feasibility evidence, not the downstream anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The probe's exact stdout SHA-256 is
`e4daeb1cace9ec6c576cbb8e2875df5dcaf956dd8a9f722e9d8a8431967741ff`.

The automation-provided `Formalizations/Lean/.lake` link points to canonical pinned artifacts and
was used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake`
mutation was run.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai). Lean commands ran from
`Formalizations/Lean`; all others ran from the repository root unless noted. Structured commands
preserve exact executable arguments; manual inspections and invariant assessments are explicitly
labeled as such. Exits, result summaries, and current input fingerprints are preserved in
`statement-blocker.json`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0877` | 0 | rank 1430; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree are recorded above |
| scoped reads of the standard, skill, guidelines, target entry, catalog, Stage0 projection, execution DAG, complete intake dossier, and neighboring `THM-M-0814` statement | 0 | confirmed the provisional dependency, null canonical target, distinct candidate roots, and duplicate-ownership boundary |
| current `sha256sum` over named authority, source, intake, toolchain, lockfile, and relevant pinned mathlib files | 0 | exact digests are recorded in the structured blocker |
| `git blame -L 6425,6430 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| pre-edit `python3 -B Stage1_Instances/THM-M-0877/check_intake.py` | 0 | intake invariants passed: planned, `[H5, M4, R4]`, six open tasks |
| post-edit replay of the same historical intake checker | 1 | expected historical-boundary failure: the checker freezes the original nine-file intake inventory and rejects the two later statement-blocker artifacts; it was not rewritten |
| pinned Lean, Lake, mathlib revision/tree, and package-status checks | 0 | Lean 4.29.0, Lake 5.0.0, and the expected clean pinned mathlib worktree passed |
| `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0877/IntakeProbe.lean` | 0 | six adjacent APIs elaborated; stdout hash recorded above; no canonical target or proof body |
| bounded exact-topic `rg` over the repository Lean library and pinned mathlib | 1 expected | no target declaration found under the searched terms; discovery-only evidence |
| prohibited-construct scan over owned Lean | 1 expected | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| JSON, scoped invariant, newline, and whitespace checks | 0 | the two blocker artifacts are well formed, internally consistent, and confined to the owned path |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

## Retry Condition And Status Boundary

The integration lane must first master-accept fresh intake evidence. Accountable reviewers must then
preserve and hash one lawful immutable primary or approved authoritative source, select and
independently approve one exact proposition or explicitly typed theorem-family ledger, reconcile
`THM-M-0814` ownership, and map every incorporated definition, ordered binder, hypothesis,
conclusion, proof locator and boundary, correction, erratum, and degenerate case. They must fix the
graph, terminals, capacities, flows, conservation, cuts, extrema, algorithm or nonalgorithm boundary,
transports, and foundation, TCB, and computation profiles.

A fresh statement run can then encode precisely that reviewed claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, master
acceptance, statement fingerprint, or proof credit is claimed.
