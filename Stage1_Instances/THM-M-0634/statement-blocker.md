# Exact-statement gate: blocked

Item: `S56-M-0634-STATEMENT`

Theorem: `THM-M-0634`

Base revision: `fd0fab2ab7f4f514a5cc625bbce92879e718ba13` (tree
`4116d53bcf2573069e4b67205353fe3469dbe7bd`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the received repository record. The
catalog gives only the title `介值定理`, Bernard Bolzano, the year 1817, and the fragment
`连通空间上连续函数的值域` ("the range of a continuous function on a connected space").
It supplies no bibliography, truth-valued predicate, ordered codomain, carrier convention,
ordered binders, hypotheses, conclusion, proof boundary, correction history, or independently
reviewed source crosswalk. Stage0 explicitly leaves precise definitions and premises open. The
catalog's `已验证` label is untrusted under rev-5.6.

The fragment admits materially different propositions. Read literally as a claim about the image,
it points to connectedness of a continuous image, but `THM-M-0626` separately owns the explicit
catalog claim `连通集的连续像连通`. Read in light of the title and Bolzano attribution, it points
to an ordered intermediate-value theorem, but it still does not choose a connected or preconnected
space or set, a general ordered topological codomain or `Real`, global or on-set continuity,
endpoint orientation, interval inclusion versus one existential preimage, or the sign-changing
root corollary. Equality, empty/singleton carrier, constant-function, reversed-endpoint, and
endpoint-witness cases are also unresolved. These choices change the proposition.

The prerequisite intake deliberately records this ambiguity. Its `canonical_statement`,
`canonical_claim`, Lean module, declaration/expression, expression hash, and canonical-target
environment fingerprint are null, and its first failed gate is exact source-statement identity.
Selecting `IsConnected.image`, `IsPreconnected.intermediate_value`, `intermediate_value_univ`, an
interval specialization, or a zero theorem in this phase would therefore invent or substitute
mathematics rather than elaborate a source-frozen target.

Sections 5 and 5.1 of the rev-5.6 blueprint make the missing canonical proposition and expression
fingerprint hard blockers. Without a canonical expression, no direct import can be certified
minimal, no alternate encoding can receive a checked transport, and the required removed-
hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are undefined rather
than passed. No `Statement.lean`, assumed theorem interface, axiom, placeholder, weakened special
case, or broadened theorem was introduced. Lifecycle remains `planned`, and the root remains
`[H1, M4, R4]`.

The prerequisite `S56-M-0634-INTAKE` has provisional worker state `[_]`, not master-accepted state
`[x]`. Its receipt declares `accepted: false`, is not content-addressed, and has no accepted receipt
ID. Rev-5.6 permits this dependency-ordered blocker inspection, but master acceptance remains an
independent prerequisite for any future accepted statement transition.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates against pinned mathlib. The direct
import `Mathlib.Topology.Order.IntermediateValue` exposes seven candidate interfaces, including:

```text
IsConnected.image :
  IsConnected s -> ContinuousOn f s -> IsConnected (f '' s)

IsPreconnected.intermediate_value :
  IsPreconnected s -> a in s -> b in s -> ContinuousOn f s ->
  Icc (f a) (f b) subset f '' s

intermediate_value_univ :
  [PreconnectedSpace X] -> Continuous f -> Icc (f a) (f b) subset range f
```

The probe also checks oriented and unordered closed-interval variants. All seven candidates
elaborate, and the diagnostic axiom reports for `IsConnected.image` and
`intermediate_value_univ` are `[propext, Classical.choice, Quot.sound]`. Its complete stdout has
SHA-256 `326ce5623e9287d05b5c1130e71cfe726f61e53335212232c762604d03ff302e`.

This is real interface-feasibility evidence, but it defines no canonical target, source transport,
mutation, or proof body. It also does not establish a minimal target import: the ordered candidates
are defined in `Mathlib.Topology.Order.IntermediateValue`, while the literal continuous-image
candidate is defined in `Mathlib.Topology.Connected.Basic`. Choosing between them is precisely the
unresolved proposition decision.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink targeted the canonical dependency cache. No `lake update` or
`lake build` was run. The target-relevant mathlib package remained at the pinned clean revision,
but a later concurrent audit command unexpectedly caused Lake to re-clone the unrelated pinned
`flt-regular` package in that shared cache. This violates the intended read-only cache discipline,
so the entire run is nonrelease evidence and the cache incident is an explicit known failure.

## Validation Evidence

Commands ran in this isolated worker clone on 2026-07-13 (`Asia/Shanghai`), from the repository
root unless another working directory is shown.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0634` | 0 | rank 1327, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision/tree appear above |
| scoped manifest, blueprint, skill, catalog, Stage0, intake, scope, crosswalk, task-DAG, and neighboring-target inspection | 0 | the received record is not binder-complete; intake deliberately leaves the target null pending source and `THM-M-0626` scope decisions |
| `python3 -B Stage1_Instances/THM-M-0634/check_intake.py` before this phase wrote artifacts | 1 | historical intake replay stops at its frozen authoritative-DAG intake-object hash: integration changed intake state/attempts from `[ ]`/0 to `[_]`/1; the prior checker was not rewritten |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib revision/tree and package-status checks | 0 | revision/tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0634/IntakeProbe.lean` | 0 | seven inequivalent candidate interfaces elaborated; two diagnostic axiom reports were `[propext, Classical.choice, Quot.sound]`; stdout hash recorded above |
| bounded source and declaration inspection in repo-local records and pinned mathlib | 0 | the literal continuous-image candidate overlaps `THM-M-0626`; ordered set, space, and interval candidates have different scopes; no source-approved canonical root was found or credited |
| post-validation shared-cache incident inspection | 0 | mathlib remained clean at its pinned revision/tree; concurrently invoked Lake re-cloned the unrelated pinned `flt-regular` dependency at `56161b6e...`; no further Lake command was run, and this run is explicitly nonrelease |
| prohibited Lean construct scan over the owned path | 1 | expected no-match result: no `sorry`, `admit`, `sorryAx`, axiom, constant, opaque, or unsafe declaration token; diagnostic `#print axioms` is permitted |
| JSON parse and scoped invariant validation for `statement-blocker.json` | 0 | identity, base/input hashes, open state, null target/imports, unchanged vector, four undefined mutations, false completion flags, two-file scope, and absent self-test agree |
| `git diff --check -- Stage1_Instances/THM-M-0634` plus direct checks of both added files | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The intake checker is historical evidence scoped to its earlier authoritative DAG snapshot and
original nine-file intake inventory. The current failure precedes the new files and is caused by
the integration lane's provisional intake-state update. Rewriting `check_intake.py`, the intake
instance or receipt, the target-local task DAG, or shared execution authorities would alter prior
evidence or exceed this worker's assignment; this phase records the mismatch instead.

## Retry Condition And Status Boundary

The integration lane must revalidate and master-accept refreshed intake evidence before accepting
a later statement transition. Accountable reviewers must lawfully preserve and hash one immutable
primary or authoritative source; transcribe and independently approve one exact proposition with
every incorporated definition, ordered binder, hypothesis, conclusion, proof boundary,
translation, correction, erratum, and boundary case; and explicitly reconcile the root with
`THM-M-0626`.

A fresh statement worker can then encode precisely that approved claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node. The
node remains `[ ]`; lifecycle remains `planned`; the root remains `[H1, M4, R4]`, with
`audit_complete: false` and `theorem_complete: false`; no debt-vector change is proposed. Because
the assigned phase is not genuinely self-tested to its completion gate, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or master acceptance is claimed.
