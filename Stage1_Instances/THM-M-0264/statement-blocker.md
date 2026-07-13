# Exact-statement gate: blocked

Item: `S56-M-0264-STATEMENT`

Theorem: `THM-M-0264`

Base revision: `c2e294becadae6ce784f27ee69f2e8dbf57e0b30` (tree
`3f567e7f76b189432b73444354070c0ff75925b9`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0264-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. The intake receipt declares `accepted: false`, is not
content-addressed, and has no accepted receipt ID. It deliberately leaves the canonical
mathematical statement, Lean module and expression, expression hash, and target environment
fingerprint null.

Independently, the received source record is not binder-complete. It gives the title
Bolzano-Weierstrass theorem, the catalog category real analysis, and only the Chinese gloss
`有界数列必有收敛子列` (every bounded sequence has a convergent subsequence). It does not cite a
source or fix the sequence carrier, boundedness convention, topology, subsequence object, ordered
binders, exact conclusion, or limit-location clause. Stage0 explicitly leaves the precise
definitions, premises, equivalent forms, axioms, and machine artifact open.

The real-analysis category makes a natural-number-indexed real sequence the conventional reading,
but that is still a proposition-changing choice rather than information contained in the gloss.
The intake records the following as a resolution target only:

```text
for every x : Nat -> Real, if Set.range x is bornologically bounded, then there exist
a : Real and phi : Nat -> Nat such that StrictMono phi and x composed with phi tends to a.
```

An approved statement must still choose that real carrier rather than a finite-dimensional or
proper metric carrier; bornological range boundedness rather than an order or absolute-value
formula; a `StrictMono` natural selector rather than another subsequence encoding; ordinary real
topological convergence; and whether closure membership of the limit is part of the conclusion.
It must also settle whether every term is bounded or only frequently many terms are bounded.

These choices cannot be imported from the separate `THM-M-0619` target, which owns the compact
metric-space sequence formulation. A proper-metric theorem, compactness theorem, monotone
convergence theorem, or premise that already contains a convergent subsequence would broaden,
substitute, or trivialize the received target.

No immutable primary theorem passage, incorporated definitions, complete assumption and
conclusion map, proof boundary, translation, corrections or errata disposition, or independent
review has been accepted. Selecting the conventional formula solely from familiarity or a nearby
API would therefore invent the missing source bridge. Rev-5.6 sections 5 and 5.1 make this
ambiguity and the absent elaborated-expression fingerprint hard blockers.

There is consequently no honest canonical expression whose imports can be certified minimal.
Checked alternate transports and the required removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutation suites are undefined, not passed. The lifecycle
remains `planned`, and the root vector remains `[H1, M3, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates the direct pinned import
`Mathlib.Topology.MetricSpace.Sequences`. At mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, it authenticates these candidate interfaces:

```text
tendsto_subseq_of_bounded :
  IsBounded s -> (forall n, x n in s) ->
  exists a in closure s, exists phi, StrictMono phi and Tendsto (x composed with phi) atTop (nhds a)

tendsto_subseq_of_frequently_bounded :
  IsBounded s -> (frequently n in atTop, x n in s) ->
  exists a in closure s, exists phi, StrictMono phi and Tendsto (x composed with phi) atTop (nhds a)
```

Both declarations are universe-polymorphic over a proper pseudometric space, and both report
exactly `propext`, `Classical.choice`, and `Quot.sound`. The probe also checks the compact-closure,
compact-set subsequence, and sequentially compact space interfaces. This is real elaboration and
candidate-interface evidence, but it defines no canonical source target, checked source transport,
statement mutation, or new proof body. Its topical import cannot be certified as the minimal import
of an absent canonical target.

A bounded exact-topic search found the two named declarations and their source comments in pinned
mathlib, plus the target-local intake probe. It found no separately accepted source-identical root
mapping in repo-local Lean. This observation is not the downstream exhaustive anchor or terminal
proof-body audit and makes no global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symbolic link was used read-only. No update, build, dependency clone or
fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0264` | 0 | rank 1272; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` link was untracked; base revision and tree appear above |
| source record, Stage0, manifest, blueprint, intake dossier, task dependency, and source-boundary inspection | 0 | the bounded-sequence family is identified, but proposition-changing choices and the canonical target remain null |
| `sha256sum` over authority, intake, toolchain, probe, and pinned candidate sources | 0 | exact fingerprints are recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree recorded above; package source worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0264/IntakeProbe.lean` | 0 | five candidate or supporting APIs elaborated; both direct declarations reported the three axioms above; stdout SHA-256 `6b48207f7b1a9555239c71c399c62cc69f5d7c06548087fd0043192566b39d4b` |
| bounded exact-topic `rg` search in pinned mathlib and repo-local Lean | 0 | named candidate declarations and comments found; no source-identical mapping credited |
| `python3 -B Stage1_Instances/THM-M-0264/check_intake.py` | 1 | historical intake replay stops when its frozen expected authoritative intake row `[ ]`, attempt 0 differs from the integration-updated row `[_]`, attempt 1; intake evidence was not rewritten |
| `python3 -m json.tool Stage1_Instances/THM-M-0264/statement-blocker.json` plus scoped blocker invariants | 0 | structured blocker parses; identity, dependency, null target/imports, undefined mutations, unchanged vector, false completion flags, and no-self-test boundary agree |
| prohibited-declaration scan over owned Lean files | 0 | the inner search returned expected no-match exit 1; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration token; diagnostic `#print axioms` commands are permitted |
| scoped `git diff --check` plus per-new-file no-index whitespace checks | 0 for the scoped check; 1 expected difference for each new file | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | the worker self-test manifest is intentionally absent because the exact-statement deliverable did not pass |

The intake checker freezes the intake run's original authority row and closed nine-file owned
inventory. Integration has since made the intake provisional `[_]`. The checker is historical
intake evidence, not a later-phase validator. This run records its fail-closed result instead of
rewriting the intake instance, receipt, checker, task DAG, generated blueprint, or authoritative
execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must master-accept the intake dependency before accepting a later statement
transition. Accountable reviewers must preserve and hash an immutable source edition, transcribe
and independently approve one exact proposition with every incorporated definition, ordered
binder, hypothesis, conclusion, proof boundary, correction, erratum, translation, attribution,
and boundary case. In particular, they must approve the carrier, boundedness encoding, index and
subsequence representation, convergence topology, limit-location clause, binder order, and the
relationship to `THM-M-0619`.

A fresh statement worker can then encode precisely that approved claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute the removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
