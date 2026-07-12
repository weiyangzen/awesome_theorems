# Exact-statement gate: blocked

Item: `S56-M-0892-STATEMENT`

Theorem: `THM-M-0892`

Base revision: `5c38e670073bc890a78e61556f36d2c6b35d257d` (tree
`95a189ecdfe548d9cff4faaebc111079babceb92`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record gives only the family label "Hoffman-Singleton theorem," attributes it to Alan Hoffman
and Robert Singleton in 1960, and supplies the gloss "existence of Moore graphs." It cites no
theorem and fixes no degree, diameter, girth, order, regularity, connectedness, quantifier,
uniqueness clause, proof boundary, correction, or erratum. Stage0 explicitly leaves the precise
definitions and premises open, and the catalog label `verified` is untrusted under rev-5.6.

The exact bibliographic match is A. J. Hoffman and R. R. Singleton, *On Moore Graphs with
Diameters 2 and 3*, IBM Journal of Research and Development 4(5), 497-504 (1960), DOI
`10.1147/rd.45.0497`. The intake records a temporary inspection of its result family: the paper
defines connected regular Moore graphs attaining the Moore bound; for diameter two, degrees `2`,
`3`, and `7` exist uniquely, `57` is the only other possible degree, and its existence is
undecided; it also contains a separate diameter-three result. The inspected scan was not suitable
for a lawful public source packet, and no complete transcription, correction audit, source
admission, proof-node mapping, or independent review was accepted.

The received gloss therefore does not choose among materially different propositions:

- existence or an explicit construction of the 50-vertex degree-7 graph;
- uniqueness of that graph up to graph isomorphism;
- classification of diameter-2 Moore-graph degrees as `2`, `3`, `7`, or `57`;
- one of the paper's diameter-3 results; or
- a precisely delimited conjunction of construction, uniqueness, and classification claims.

It also does not choose the source's diameter-and-Moore-bound encoding, a girth-5 encoding, or the
strongly regular parameters `(50, 7, 0, 1)`. Those representations require checked transports and
different boundary guards. In particular, asserting degree-57 existence would turn an unresolved
case into a false completion claim. Selecting any familiar candidate from the title, later
literature, or formal convenience would invent, narrow, broaden, or substitute mathematics rather
than elaborate the exact received target.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing elaborated
expression fingerprint hard blockers. The intake correctly leaves the canonical human claim, Lean
module and expression, minimal imports, ordered binders, and expression/environment fingerprints
null at `[H1, M4, R4]`. Without a canonical target, credited transports and the required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are undefined,
not passed. No `Statement.lean`, axiom, placeholder, assumed graph certificate, weakened example,
or broadened theorem was introduced.

The prerequisite `S56-M-0892-INTAKE` is only provisional worker state `[_]`, not master-accepted
state `[x]`. Rev-5.6 section 10.2 permits this dependency-ordered attempt, so pending acceptance did
not prevent truthful blocker work, but master acceptance remains independently required before a
future statement transition can be accepted. Its receipt declares `accepted: false`, is
non-content-addressed, and has no accepted receipt ID.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates with the pinned environment and directly imports:

```lean
import Mathlib.Combinatorics.SimpleGraph.Diam
import Mathlib.Combinatorics.SimpleGraph.Girth
import Mathlib.Combinatorics.SimpleGraph.StronglyRegular
```

All ten adjacent finite-graph, regularity, distance, diameter, girth, and strongly regular APIs
elaborate. This is real environment evidence, but the probe defines no Moore-graph predicate,
Hoffman-Singleton construction, canonical target, source transport, or proof body. The imports are
candidate substrate and cannot be certified minimal for an absent target.

A bounded exact-topic search of repository-local and pinned-mathlib Lean sources found no
Hoffman-Singleton or Moore-graph declaration. This is discovery-only feasibility evidence, not the
downstream immutable anchor audit and not a claim of global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The `lean-toolchain`,
`lake-manifest.json`, and probe-output SHA-256 values are respectively
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`,
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`, and
`26a23940f60057c0efe5fff40c0fe14e6d217083c63659a48bc18b769ff434d8`.

The automation-provided `Formalizations/Lean/.lake` link points to the canonical pinned artifacts
and was used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake`
mutation was run.

## Validation Record

Commands ran in this isolated worker clone on 2026-07-13 (Asia/Shanghai), from the repository root
unless a different working directory is shown.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0892` | 0 | rank 1038, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree are recorded above |
| scoped manifest, blueprint, skill, catalog, Stage0, intake, scope, and crosswalk inspection | 0 | the authoritative gloss does not select one proposition; every proposition-changing choice remains open |
| `sha256sum` over authority, intake, source, probe, toolchain, Lake, and relevant pinned mathlib inputs | 0 | hashes agree with `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-0892/check_intake.py` | 1 | historical intake replay stops at line 128 because it freezes intake authority state `[ ]` while current authority records provisional `[_]`; its exact nine-file inventory also predates this phase, so the statement worker records rather than rewrites historical evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake agree with the pinned environment above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree agree with the fingerprint; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0892/IntakeProbe.lean` | 0 | ten adjacent graph APIs elaborated; complete stdout SHA-256 is `26a23940...34d8`; no canonical target was stated |
| bounded exact-topic search in pinned mathlib and repo-local Lean | 1 | expected no-match exit; discovery only, not an anchor audit |
| prohibited Lean construct scan over the owned path | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, or unsafe declaration |
| JSON parse and scoped invariant check for `statement-blocker.json` | 0 each | IDs, open state, null target/imports, unchanged vector, four undefined mutations, false completion flags, exact paths, and absent self-test agree |
| whitespace checks for both new blocker artifacts | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test manifest exists because the exact-statement deliverable is blocked |

## Retry Condition And Status Boundary

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers must
then preserve and hash a lawful immutable primary or authoritative edition, select and
independently approve one exact result or explicit conjunction, and transcribe every incorporated
definition, ordered binder, hypothesis, conclusion, proof boundary, correction, erratum, and
boundary case. They must freeze the degree and diameter quantifiers, graph and finiteness model,
regularity, connectedness, Moore-bound, girth and strongly regular conventions, cardinality,
isomorphism representation, and the degree-57 boundary.

A fresh statement worker can then encode precisely that source-selected claim, minimize pinned
imports, serialize and hash its elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
