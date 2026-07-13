# Exact-statement gate: blocked

Item: `S56-M-0277-STATEMENT`

Theorem: `THM-M-0277`

Base revision: `0e5ae82e6d507ee607c3f011900571ffd8096800` (tree
`400e6edf1f69b971b60a367e3ea29be359b07907`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0277-INTAKE` has only provisional worker
state `[_]`, not master-accepted state `[x]`. The intake receipt declares `accepted: false`, is not
content-addressed, and has no accepted receipt ID. Rev-5.6 section 10.2 permits preparation of this
later-node blocker, but master closure remains dependency ordered.

Independently, the exact-source-statement gate fails. The repository supplies only the title
"closed graph theorem," the attribution Stefan Banach, the year 1932, and the gloss
`闭线性算子的连续性` ("continuity of closed linear operators"). The record has no source citation,
formula, incorporated definition, ordered binder, hypothesis, conclusion, proof boundary,
correction or erratum disposition, or reviewer. Stage0 explicitly leaves the precise definitions,
premises, equivalent formulations, formal system, and machine artifact open. The catalog's
`已验证` label is untrusted metadata under rev-5.6, not source or kernel evidence.

The gloss does not determine whether the operator is total or partially defined; whether both
spaces are Banach spaces or belong to a broader topological-vector-space category; whether the
scalars are real, complex, or an arbitrary nontrivially normed field; which product topology and
graph predicate are intended; or whether the conclusion is continuity, boundedness, or a bundled
continuous linear map. These choices change the proposition. In particular, a closed partially
defined unbounded operator cannot be silently replaced by the everywhere-defined Banach-space
theorem.

No immutable pinpoint primary or approved authoritative source, complete definition and premise
map, proof boundary, correction or erratum audit, source-to-target transport, or independent source
review has been accepted. Selecting the familiar total-map theorem from mathematical convention or
because pinned mathlib already proves it would supply proposition-changing assumptions that the
received source does not state. The intake therefore correctly leaves `canonical_statement`, the
Lean module and expression, elaborated-expression hash, target environment fingerprint, binders,
hypotheses, and alternate encodings null or empty.

Rev-5.6 sections 5 and 5.1 make statement ambiguity and a missing expression fingerprint hard
blockers. There is consequently no canonical expression whose imports can honestly be certified
minimal, no credited alternate encoding for a checked transport, and no target against which the
required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations can
run. Those mutations are undefined, not passed. The lifecycle remains `planned`, and the root
vector remains `[H1, M3, R4]`.

## Pinned Lean Boundary

The direct exact-topic candidate in pinned mathlib is
`LinearMap.continuous_of_isClosed_graph`. Its defining module is
`Mathlib.Analysis.Normed.Operator.Banach`, and its type has:

```text
{k} [NontriviallyNormedField k]
{E} [NormedAddCommGroup E] [NormedSpace k E] [CompleteSpace E]
{F} [NormedAddCommGroup F] [NormedSpace k F] [CompleteSpace F]
(g : E ->l[k] F)
(hg : IsClosed (g.graph : Set (E x F)))
|- Continuous g
```

The existing `IntakeProbe.lean` was re-elaborated with
`Mathlib.Analysis.Normed.Operator.Banach` and the separate partial-operator discriminator
`Mathlib.Topology.Algebra.Module.LinearPMap`. It authenticates the direct theorem, its sequential
variant, the two bundled constructors, and the total/partial graph APIs. The direct and sequential
theorems report `propext`, `Classical.choice`, and `Quot.sound`. A bounded search found the direct
candidate and adjacent mathlib uses but no accepted source-identical mapping in repository-local
Lean.

This is real candidate-interface evidence only. The probe defines no canonical target, checked
source transport, statement mutation, or proof body. `Mathlib.Analysis.Normed.Operator.Banach`
would be the minimal direct import for the candidate total-map expression, but it cannot be claimed
as the minimal import of the absent canonical source target. The partial-operator module is a scope
discriminator, not an import required by that direct candidate.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided canonical `.lake` symbolic
link was used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake`
mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0277` | 0 | rank 1283; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| initial `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree appear above |
| repository record, Stage0, blueprint, manifest, intake dossier, and pinned source inspection | 0 | confirmed the sparse family gloss, proposition-changing omissions, null canonical target, and direct candidate boundary |
| `sha256sum` over authority, intake, toolchain, lockfile, probe, and pinned candidate source inputs | 0 | exact current fingerprints are recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib `git rev-parse HEAD 'HEAD^{tree}'` and `git status --short` | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0277/IntakeProbe.lean` | 0 | seven total/partial closed-graph APIs elaborated; the two direct candidates reported the three axioms above; stdout SHA-256 `18ef25189f8f15a3f8418f4ce077a0f6d45185ea07001c00714f87a2e5484cf8`; empty stderr |
| bounded exact-topic `rg` over repository-local and pinned-mathlib Lean sources | 0 | located the direct theorem, sequential form, constructors, partial-operator interfaces, and adjacent uses; no accepted source-identical mapping was credited |
| `python3 -B Stage1_Instances/THM-M-0277/check_intake.py` | 1 | historical intake replay rejects the integrated `HEAD`, because it is frozen to intake base `bd81d485...e458`; intake evidence was not rewritten to manufacture later-phase agreement |
| finalized JSON parse and scoped blocker assertions | 0 | identity, dependency, null target/imports, four undefined mutations, unchanged vector, false completion flags, exact two-file scope, and absent self-test agree |
| prohibited-declaration scan over owned Lean files | 0 | inner `rg` returned expected no-match exit 1; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration token; diagnostic `#print axioms` is allowed |
| scoped `git diff --check` and per-new-file no-index whitespace checks | 0 for scoped check; 1 expected difference for each new file | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | worker self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The intake checker is historical intake evidence: it freezes the earlier repository base and its
closed intake-only artifact inventory. It is not edited or represented as passing for this
statement attempt.

## Retry Condition And Status Boundary

The integration lane must master-accept the intake before accepting a later statement transition.
Accountable reviewers must preserve and hash a lawful immutable primary or approved authoritative
source, select and independently approve one exact proposition, and map every incorporated
definition, ordered binder, hypothesis, conclusion, proof boundary, correction, erratum, and
boundary case. They must decide total versus partial domain, completeness and space category,
scalar field, product topology, graph encoding, conclusion form, and real/complex versus generalized
scalar transport.

A fresh statement worker can then encode precisely that approved claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute the removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof
credit, or master acceptance is claimed.
