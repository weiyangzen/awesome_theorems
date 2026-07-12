# Exact-statement gate: blocked

Item: `S56-M-0844-STATEMENT`

Theorem: `THM-M-0844`

Base revision: `5c38e670073bc890a78e61556f36d2c6b35d257d` (tree
`95a189ecdfe548d9cff4faaebc111079babceb92`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record gives only the eponym `Alon-Fischer-Newman theorem`, attributes it to Alon, Fischer,
and Newman in 2007, and supplies the noun phrase `testing of the regularity lemma`. It cites no
paper or theorem and provides no definition, ordered binder, hypothesis, conclusion, proof
boundary, correction, erratum, or formal artifact. Stage0 explicitly leaves precise definitions
and premises open, and the catalog label `verified` is untrusted under rev-5.6.

Bibliographic discovery does not remove the ambiguity. Crossref, DBLP, and Semantic Scholar match
the three-author 2007 article *Efficient Testing of Bipartite Graphs for Forbidden Induced
Subgraphs*, SIAM Journal on Computing 37(3), pages 959-976, DOI `10.1137/050627915`. The publisher
PDF endpoint returned HTTP 403, while the Semantic Scholar author-copy lead timed out during this
bounded attempt. No immutable primary theorem text, numbered locator, incorporated definitions,
proof boundary, correction or errata disposition, or independent review has been admitted.

The matching article contains a result family rather than selecting the catalog's intended root.
Later literature attributes to it a polynomial-size, ultra-strong regularity lemma for bipartite
graphs of bounded VC-dimension. Metadata also describes an efficient tester for bipartite graph
properties characterized by finite forbidden induced subgraphs. These are not interchangeable
with the four-author Alon-Fischer-Newman-Shapira characterization of testable graph properties,
the two-author Fischer-Newman testing-versus-estimation theorem, or ordinary Szemeredi regularity.

The repository therefore does not decide:

- a bounded-VC homogeneous-partition theorem versus a forbidden-induced-subgraph testing theorem;
- finite bipartite or simple graphs and their two-sorted or one-sorted representation;
- the neighborhood-family and VC-dimension conventions;
- the partition, density, homogeneity, regularity, error, and exceptional-part conventions;
- the forbidden family or graph-property representation, induced containment, and edit distance;
- tester adaptivity, randomness, success probability, query model, and complexity conclusion; or
- parameter dependence, ordered binders, thresholds, rounding, and degenerate cases.

Those choices yield inequivalent propositions. Selecting any familiar candidate would invent,
broaden, strengthen, or substitute mathematics rather than elaborate the received target.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing expression
fingerprint hard blockers. The intake correctly leaves the canonical human claim, Lean module and
expression, minimal imports, and expression/environment fingerprints null at `[H5, M4, R4]`.
Without a canonical target, alternate transports and the required removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations are undefined, not passed. No
`Statement.lean`, axiom, placeholder, assumed tester interface, weakened example, or broadened
theorem was introduced.

The prerequisite `S56-M-0844-INTAKE` is also only provisional worker state `[_]`, not
master-accepted `[x]`. Rev-5.6 section 10.2 permits this dependency-ordered blocker attempt, but
master acceptance remains independently required before any future statement transition.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates with the pinned environment. Its three direct imports
expose VC dimension, bipartite graphs, density, finite partitions, uniformity, and ordinary
Szemeredi regularity. All eight checks pass. The probe does not connect graph neighborhoods to VC
dimension, define an induced-subgraph property tester, state an AFN partition result, select a
canonical target, provide a checked source transport, or contain a proof body. Its imports cannot
be certified minimal for a target that has not been selected and receive no statement or proof
credit.

A bounded exact-topic search of repository-local and pinned-mathlib Lean sources found no AFN,
forbidden-induced-bipartite testing, testable-graph, or ultra-strong-regularity occurrence. This is
discovery-only feasibility evidence, not the downstream immutable anchor audit or a claim of
global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The `lean-toolchain`,
`lake-manifest.json`, and probe-output SHA-256 values are respectively
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`,
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`, and
`28739e9f581ad4ca91839f2259050894c2f657fe93ffd853e8c683936355ce43`.

The automation-provided `Formalizations/Lean/.lake` link points to canonical pinned artifacts and
was used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake`
mutation was run.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai), from the repository root unless a
different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0844` | 0 | rank 1033, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree are recorded above |
| scoped manifest, blueprint, skill, catalog, Stage0, intake, scope, and crosswalk inspection | 0 | only an eponym and noun phrase are authoritative; every proposition-changing choice remains open |
| Crossref, DBLP, Semantic Scholar, publisher, and author-copy source checks | mixed | the three-author 2007 publication family was confirmed; no primary theorem text was admitted, publisher returned 403, and the author copy timed out |
| `sha256sum` over authority, intake, toolchain, and pinned mathlib inputs | 0 | hashes agree with `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-0844/check_intake.py` | 1 | historical intake replay freezes the pre-integration authoritative intake state `[ ]`; the current DAG records `[_]`, so this phase records rather than rewrites that historical evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake agree with the pinned environment above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree agree with the fingerprint; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0844/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; full stdout SHA-256 is `28739e...43`; no canonical target was stated |
| bounded exact-topic search in pinned mathlib and repo-local Lean | 1 | expected no-match exit; discovery only, not an anchor audit |
| prohibited Lean construct scan over the owned path | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, or unsafe declaration |
| JSON parse and scoped invariant check for `statement-blocker.json` | 0 each | IDs, open state, null target/imports, unchanged vector, four undefined mutations, false completion flags, exact paths, and absent self-test agree |
| whitespace checks for both added blocker artifacts | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test manifest exists because the exact-statement deliverable is blocked |

## Retry Condition

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers must
preserve and hash an immutable primary or authoritative source, select and independently approve
one exact numbered root, and transcribe every incorporated definition, ordered binder, hypothesis,
conclusion, threshold, proof boundary, correction, and erratum. They must reconcile the
bounded-VC regularity, forbidden-induced testing, four-author characterization, two-author
estimation, and ordinary-regularity candidates and freeze every graph, VC, partition,
homogeneity, tester, distance, probability, query, parameter, and boundary convention.

A fresh statement worker can then encode precisely that source-selected claim, minimize pinned
imports, serialize and hash its elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node. The
root remains `[H5, M4, R4]`, with `audit_complete: false` and `theorem_complete: false`; no debt
change is proposed. Because the assigned phase is not genuinely self-tested to its completion gate,
no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or master acceptance is
claimed.
