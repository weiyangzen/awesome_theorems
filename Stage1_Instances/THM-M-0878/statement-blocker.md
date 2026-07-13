# THM-M-0878 exact-statement gate: blocked

- Item: `S56-M-0878-STATEMENT`
- Base revision: `46a0f2a3ea74765a0467c489264b838ffbb70675`
- Base tree: `7b1b5269d7da840fd086da731d6f92903c209c35`
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The complete mathematical wording is the title `最小费用流` (minimum-cost flow), attribution to
many mathematicians in the twentieth century, and the gloss `带费用的网络流` (a costed network
flow). The catalog cites no work or theorem and contains no network definition, ordered binder,
hypothesis, conclusion, proof boundary, correction, erratum, reviewer, or formal declaration.
Stage0 explicitly leaves precise definitions and premises open, and the catalog's `已验证` label is
untrusted under rev-5.6.

The gloss denotes a problem family, not one proposition. It does not choose among minimum-cost
circulation, prescribed-value minimum-cost flow, minimum-cost maximum flow, or transshipment. Nor
does it identify existence or attainment, integrality, primal-dual equality, residual-cycle or
price optimality, or correctness, termination, and complexity of a particular algorithm. These
choices have different hypotheses, conclusions, and proof architecture.

The inspected source lead does not resolve that ambiguity. Goldberg and Tarjan's 1987 technical
report *Finding Minimum-Cost Circulations by Canceling Negative Cycles* gives a precise circulation
model in Section 2 and states in Theorem 2.1 that a circulation is minimum-cost if and only if its
residual graph has no negative cycle. The report also states distinct price, epsilon-optimality,
algorithm, termination, iteration-count, and complexity theorems. The catalog does not cite or
select the report or Theorem 2.1. The incorporated-definition and premise map, report-to-journal
delta, corrections and errata, durable source admission, target ownership, and independent review
also remain open. Selecting Theorem 2.1 because it is a strong candidate would invent or substitute
proposition-changing mathematics rather than elaborate the exact received target.

The repository additionally fixes none of the directed-graph or multigraph representation; edge
identities, loops, and parallel arcs; terminals or balances; capacity and lower-bound convention;
numeric carriers and coercions; conservation and feasibility; attainment and boundedness; cost
objective; residual network; optimizer or dual witness; algorithm semantics and cost model; ordered
binders; or boundary cases. Empty, singleton, disconnected, infeasible, zero-flow, negative-cost,
and unbounded instances cannot be decided by convention.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing expression
fingerprint hard blockers. The intake correctly leaves `canonical_statement`, `canonical_claim`,
the Lean module and expression, target imports, elaborated-expression hash, and canonical-target
environment fingerprint null at `[H1, M4, R4]`. Consequently, minimal target imports, checked
alternate transports, and the required removed-hypothesis, changed-domain, changed-binder-scope,
and boundary-case mutations are undefined, not passed. No `Statement.lean`, declaration, proof
body, assumed optimizer interface, weakened special case, or broadened theorem was introduced.

The prerequisite `S56-M-0878-INTAKE` is only provisional worker state `[_]`. Its receipt declares
`accepted: false`, supplies no accepted receipt ID, and remains unaccepted by the master. Rev-5.6
section 10.2 permits this provisional blocker preparation, but the unfinished dependency
independently prevents accepted statement closure.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates with the pinned environment. It checks
nine adjacent directed-graph, path-weight, finite-sum, and finite-list argmin APIs. The probe defines
no capacity, feasible flow, conservation law, total-cost objective, residual network, optimizer,
algorithm, canonical target, checked source transport, or proof body. Its four combined imports
therefore cannot be certified as minimal imports for an absent target and receive no statement or
proof credit.

A bounded exact-topic search of repository-local and pinned-mathlib Lean sources found no
declaration named for minimum-cost flow, minimum-cost circulation, cycle canceling, or a negative
residual cycle. This is discovery-only feasibility evidence, not the downstream anchor audit or a
global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The probe's exact output SHA-256 is
`edfce5af6c2bfa77b75c654ccb56b5b6993f1839ea7afbb8cba4ee7fddb8152d`.

The automation-provided `Formalizations/Lean/.lake` link points to canonical pinned artifacts and
was used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake`
mutation was run.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai). Lean commands ran from
`Formalizations/Lean`; all others ran from the repository root unless noted. Exact executable
arguments, exits, result summaries, and current input fingerprints are preserved in
`statement-blocker.json`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0878` | 0 | rank 1431; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree are recorded above |
| scoped reads of the standard, skill, target manifest and entry, catalog, Stage0 projection, execution DAG, and complete intake dossier | 0 | confirmed the provisional dependency, null canonical target, distinct candidate roots, and unresolved proposition-defining inputs |
| current `sha256sum` over named authority, source, intake, probe, toolchain, lockfile, and relevant pinned mathlib files | 0 | exact digests are recorded in the structured blocker |
| `python3 -B Stage1_Instances/THM-M-0878/check_intake.py` | 1 | historical intake checker freezes intake state `[ ]` and attempts 0 while current integration records `[_]` and attempts 1; stored blueprint and DAG hashes are stale, so this phase records rather than rewrites historical evidence |
| pinned Lean, Lake, mathlib revision/tree, and package-status checks | 0 | Lean 4.29.0, Lake 5.0.0, and the expected clean pinned mathlib worktree passed |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0878/IntakeProbe.lean` | 0 | nine adjacent APIs elaborated; output SHA-256 `edfce5af...8152d`; no target or proof body was declared |
| bounded exact-topic search in pinned mathlib and repository-local Lean | 1 expected | no named target was found; no absence or anchor-audit claim is inferred |
| prohibited-construct scan over owned Lean | 1 expected | no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, or unsafe declaration |
| JSON parse, scoped blocker invariants, and whitespace checks | 0 | blocker identity, null target/imports, unchanged vector, false completion fields, exact two-file scope, absent self-test, valid JSON, and clean whitespace agree |

## Retry Condition And Status Boundary

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers must
then preserve and hash one immutable exact source proposition and independently approve every
incorporated definition and its proof boundary. That selection must fix the network representation;
terminals or balances; capacity and lower-bound conventions; numeric carriers; feasibility and
boundedness; cost objective; exact optimality, existence, integrality, duality, algorithm,
termination, or complexity conclusion; ordered binders; and every degenerate case.

A fresh statement attempt can then encode precisely that approved claim in Lean, prove its pinned
direct imports minimal, serialize and hash the elaborated expression and environment, compile every
credited transport, and execute all four mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; the root stays `[H1, M4, R4]`;
`audit_complete: false` and `theorem_complete: false`; no debt change is proposed. Because the
exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt,
worker `[_]`, or master acceptance is claimed.
