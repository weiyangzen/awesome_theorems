# Exact-statement gate: blocked

Item: `S56-M-0309-STATEMENT`

Theorem: `THM-M-0309`

Base revision: `a07fc18923e20fd2876d04809a15d5b31e55512f` (tree
`1268491c8f2677e1c8e38754fa93dd190892e69e`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record supplies only the name "Rellich-Kondrachov compact embedding theorem", the attribution
Franz Rellich / Vladimir Kondrachov, the year 1930, and the gloss "compact embedding of Sobolev
spaces". It supplies no source locator, definition chain, ordered binders, hypotheses,
conclusion, proof boundary, or errata. Stage0 explicitly leaves the formal system, exact definitions
and premises, proof route, dependencies, alternate statements, axioms, machine status, and artifact
links open. The catalog's "verified" label is untrusted under rev-5.6.

The provisional intake therefore leaves `canonical_statement`, `canonical_claim`, the Lean module
and expression, and the expression and target-environment fingerprints null. Its worker state is
`[_]`, not master acceptance. A Rellich-Kondrachov theorem may concern `W^{1,p}` to `L^q` on a
bounded regular Euclidean domain, `H_0^1` to `L^2`, higher Sobolev orders, or `H^1` to `L^2` on a
compact manifold. Those are materially different propositions. The catalog does not choose the
Sobolev model and order, ambient setting, domain and regularity, measure and scalars, dimension,
exponent range and endpoints, inclusion, or compactness formulation.

Choosing any familiar variant would invent or substitute mathematics. Section 5 of the rev-5.6
blueprint makes statement ambiguity and a missing expression fingerprint hard blockers. There is
therefore no canonical target on which to certify minimal imports, checked alternate transports, or
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations. Those four
tests are undefined, not passed. The first failed gate is exact source-statement identity, and the
root remains `[H5, M4, R4]`.

## Source And Duplicate Boundary

The repository also schedules `THM-M-1238`, named "Rellich-Kondrachov theorem", from an identical
broad gloss in the PDE category. No accepted decision says whether these IDs should share a
proposition, select different variants, or be deduplicated. This target cannot inherit that other
target's statement, source, state, or evidence.

The legacy `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_176.lean` belongs to `THM-M-1238`.
Its `RellichKondrachovData` stores the desired compact embedding as a field, and `StatementShape`
only asks for a nonempty instance of that structure. It consequently assumes rather than proves
compactness and cannot identify this target. Its external-project reference is also outside this
repository's pinned dependency closure and was not fetched or credited here.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` imports three pinned modules and checks six adjacent `L^p`, compact-
operator, bounded-image, and Sobolev-inequality APIs. It elaborates successfully in the pinned
environment but states no proposition for `THM-M-0309`. The Sobolev declarations are continuous
estimates for smooth compactly supported functions, not a compact embedding theorem. These imports
are discovery candidates only and cannot be certified minimal for an unknown target.

A bounded source-name search of pinned mathlib found no Lean source matching Rellich, Kondrachov,
RellichKondrachov, compact-embedding spellings, or compact-Sobolev spellings. This is narrow
feasibility evidence, not the later anchor audit or a claim of global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The `lean-toolchain`, `lake-manifest.json`, and
probe SHA-256 values are respectively
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`,
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`, and
`ec846e6da95380959260e64ca3acb5b42a8278b44d2ba5b8c0aaf3ba0f11197b`.

The automation-provided `Formalizations/Lean/.lake` link existed before this phase and points to
the canonical checkout's pinned artifacts. It was used without dependency mutation. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was run.

## Validation Evidence

Commands ran from this worker clone on 2026-07-13 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0309` | 0 | rank 1050, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all && git rev-parse HEAD && git rev-parse HEAD^{tree}` | 0 | before statement edits, only the automation-provided untracked `.lake` link was present; base revision and tree are recorded above |
| source-record, Stage0, intake, and DAG inspection | 0 | found only the underspecified theorem-family gloss; intake leaves the canonical statement and formal target null, and its dependency is provisional `[_]` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 and Lake 5.0.0 at the revisions above |
| mathlib revision/tree/status plus scoped SHA-256 checks | 0 | mathlib pin and clean package status, toolchain/manifest, target manifest, blueprint, skill, and probe hashes were recorded |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0309/IntakeProbe.lean` | 0 | six adjacent pinned APIs elaborated; no target theorem was stated |
| bounded pinned-mathlib source search for Rellich, Kondrachov, compact embedding, and compact Sobolev spellings | 1 | expected no-match exit; discovery-only feasibility evidence, not an anchor audit |
| `python3 -B Stage1_Instances/THM-M-0309/check_intake.py` | 1 | the historical intake receipt is stale against the integrated blueprint hash; this statement run did not rewrite prior evidence to manufacture agreement |
| `python3 -m json.tool Stage1_Instances/THM-M-0309/statement-blocker.json` | 0 | structured blocker parsed as JSON |
| scoped `jq` blocker invariants | 0 | identity, blocked verdict, null target, undefined mutations, unchanged debt vector, false completion flags, and no-self-test boundary agree |
| prohibited Lean declaration and proof-escape scan over the owned path | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, bodyless constant, `opaque`, or `unsafe` declaration was found |
| scoped tracked and added-file whitespace checks | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | required no-self-test boundary is preserved because the statement deliverable is blocked |

The statement run does not rewrite the intake manifest, receipt, checker, task DAG, generated
blueprint, or authoritative execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must accept the intake dependency and make an accountable scope decision for
`THM-M-0309` versus `THM-M-1238`. A source reviewer must then preserve and hash an immutable primary
or authoritative statement source, transcribe one exact theorem and every incorporated definition
with pinpoint locators, audit its proof boundary and errata, and freeze the Sobolev spaces and
orders, ambient setting, domain regularity and measure, scalars, dimension, complete exponent range
and endpoints, inclusion map, compactness encoding, ordered binders, hypotheses, conclusion, and
all degenerate cases. Independent review must approve that same proposition.

A later statement worker can then encode the approved claim, minimize its pinned imports, serialize
and hash the elaborated expression and environment, compile every credited transport, and run all
four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the phase is not genuinely
self-tested to its completion gate, no `.stage1-worker-selftest.json` is emitted and no statement
receipt or master acceptance is claimed.
