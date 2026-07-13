# THM-M-0846 exact-statement gate: blocked

- Item: `S56-M-0846-STATEMENT`
- Base revision: `748243faadc15828fb087059337fd05b7be9fdeb`
- Base tree: `e46d642646f80980838b6f016f5d69b817bd464d`
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The complete mathematical wording is the title `图极限理论` (graph limit theory), attribution to
Laszlo Lovasz and Balazs Szegedy in 2006, and the gloss `图序列的极限` (limits of graph
sequences). The catalog cites no work or theorem and contains no definition, ordered binder,
hypothesis, conclusion, proof boundary, correction, erratum, reviewer, or formal declaration.
Stage0 explicitly leaves precise definitions and premises open, and the catalog's `已验证` label is
untrusted under rev-5.6.

The intake's immutable source lead does not select a unique root. Lovasz and Szegedy's *Limits of
dense graph sequences*, arXiv `math/0408173v2`, includes materially different claims:

- the implication from a convergent dense simple-graph sequence to a symmetric measurable
  `[0,1]^2 -> [0,1]` limit object reproducing all homomorphism-density limits;
- the converse realization of such a limit object by a simple-graph sequence;
- the full five-way Theorem 2.2 characterization using graph-sequence limits, measurable limit
  objects, reflection positivity, positive-semidefinite connection matrices, and a nonnegative
  transform; and
- the almost-sure random realization `G(n,W)` in Corollary 2.6.

These are not interchangeable. Nor does the repository fix finite simple versus weighted graphs,
the vertex carriers, normalized density, convergence filter, graphon representation or quotient,
equality convention, uniqueness, algebraic definitions, measurability context, ordered binders, or
degenerate cases. Choosing any familiar candidate would invent, broaden, strengthen, or substitute
proposition-changing mathematics rather than elaborate the received target.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing expression
fingerprint hard blockers. The intake correctly leaves `canonical_statement`, `canonical_claim`,
the Lean module and expression, target imports, elaborated-expression hash, and canonical-target
environment fingerprint null at `[H1, M4, R4]`. Consequently, minimal target imports, alternate
transports, and the required removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations are undefined, not passed. No `Statement.lean`, axiom, placeholder,
assumed limit-object interface, weakened example, or broadened theorem was introduced.

The prerequisite `S56-M-0846-INTAKE` is only provisional worker state `[_]`. Its historical receipt
declares `accepted: false`, supplies no accepted receipt ID, and remains unaccepted by the master.
That independently prevents accepted statement closure.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates with the pinned environment. It checks
nine adjacent simple-graph, homomorphism, finite density, regularity, measure, and Fubini APIs. The
three axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`. The probe defines
no graphon, homomorphism-density integral, graph-sequence convergence predicate, canonical target,
checked source transport, or proof body. Its imports therefore cannot be certified as minimal
imports for an absent target and receive no statement or proof credit.

A bounded exact-topic search of repository-local and pinned-mathlib Lean sources found only the
unrelated `Set.graphOn` function-graph API, not a graphon or dense-graph-limit declaration. This is
discovery-only feasibility evidence, not the downstream anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The probe's exact combined output SHA-256 is
`92621eb3bf4eecd56561137090f301abfc498dd335afeb91128c0c4e9513ef91`.

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
| `python3 scripts/stage1_target.py show THM-M-0846` | 0 | rank 1401, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree are recorded above |
| scoped reads of the standard, skill, target manifest and entry, catalog, Stage0 projection, execution DAG, and complete intake dossier | 0 | confirmed the provisional dependency, null canonical target, distinct source roots, and unresolved proposition-defining inputs |
| current `sha256sum` over named authority, source, intake, probe, toolchain, lockfile, and directly relevant pinned mathlib files | 0 | exact digests are recorded in the structured blocker |
| pinned Lean, Lake, mathlib revision/tree, and package-status checks | 0 | Lean 4.29.0, Lake 5.0.0, and the expected clean pinned mathlib worktree passed |
| `lake env lean ../../Stage1_Instances/THM-M-0846/IntakeProbe.lean` | 0 | nine adjacent APIs elaborated; complete output SHA-256 `92621eb3...ef91`; no target or proof body was declared |
| bounded exact-topic search in pinned mathlib and repository-local Lean | 0 with unrelated matches | only `Set.graphOn` function-graph identifiers matched; no graphon or graph-limit target was credited |
| `python3 -B Stage1_Instances/THM-M-0846/check_intake.py` | 1 | the historical intake checker freezes the pre-integration DAG state; integration changed intake from `[ ]` to `[_]`, so this phase records rather than rewrites historical evidence |
| prohibited-construct scan over owned Lean | 1 expected | no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, or unsafe declaration |
| JSON parse, scoped blocker invariants, and whitespace checks | 0 | blocker identity, null target/imports, unchanged vector, false completion fields, exact two-file scope, absent self-test, valid JSON, and clean whitespace agree |

## Retry Condition And Status Boundary

The integration lane must master-accept fresh intake evidence bound to current authority. Accountable
reviewers must then preserve and hash one immutable primary or approved authoritative source, select
and independently approve one exact theorem or typed branch ledger, and transcribe every
incorporated definition, ordered binder, hypothesis, conclusion, proof boundary, correction,
erratum, and boundary case. They must resolve ownership relative to `THM-M-0845` and
`THM-M-0847`.

A fresh statement attempt can then freeze the graph and density domains, convergence and graphon
encodings, equality or quotient, measures, algebraic definitions, foundation/TCB/computation
profiles, and degenerate cases; encode precisely the approved claim in Lean; prove its pinned
direct imports minimal; serialize and hash the elaborated expression and environment; compile every
credited transport; and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; the root stays `[H1, M4, R4]`;
`audit_complete: false` and `theorem_complete: false`; no debt change is proposed. Because the
exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt,
worker `[_]`, or master acceptance is claimed.
