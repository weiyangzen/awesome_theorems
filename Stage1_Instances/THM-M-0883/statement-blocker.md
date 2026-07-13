# Exact-statement gate: blocked

Item: `S56-M-0883-STATEMENT`

Theorem: `THM-M-0883`

Base revision: `46a0f2a3ea74765a0467c489264b838ffbb70675` (tree
`7b1b5269d7da840fd086da731d6f92903c209c35`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record supplies only the family label `Lubotzky-Phillips-Sarnak construction`, the three
authors, the year 1988, and the gloss `construction of Ramanujan graphs`. It provides no citation,
definition, ordered binder, hypothesis, conclusion, construction data, theorem locator, proof
boundary, correction, erratum, or formal artifact. Stage0 explicitly leaves the precise definitions
and premises open, and the catalog's `verified` label is untrusted under rev-5.6.

The intake identified the matching article, A. Lubotzky, R. Phillips, and P. Sarnak, *Ramanujan
graphs*, *Combinatorica* 8(3) (1988), 261-277, DOI `10.1007/BF02126799`. The inspected publisher
abstract advertises a large explicit family of regular Cayley graphs, the Ramanujan spectral bound,
and an asymptotic girth property. The article body was subscription-restricted, however, so no
immutable theorem text, incorporated definition chain, exact construction, branch conditions,
proof boundary, correction or erratum review, or independent source approval was admitted. The
immutable 2017 author survey `arXiv:1711.06558v1` confirms only the broader family: LPS gave explicit
infinite families of degree `q + 1` for prime `q`. It cannot select the 1988 proposition.

The missing choices change the proposition. They include the prime, congruence, and quadratic-
residue inputs and binder dependencies; the `PSL`/`PGL` branch, finite field, quotient, and
generators; the graph category and Cayley convention; one graph versus an infinite or explicit
family; degree and cardinality; connectedness and bipartiteness; trivial eigenvalues, multiplicity,
and the spectral boundary; and whether the girth claim belongs to the root and with which exact
asymptotic quantifiers. Choosing a familiar LPS formulation from general knowledge or the abstract
would therefore invent, omit, broaden, or substitute proposition-changing mathematics. General
expander, Margulis, generic Ramanujan-graph, Morgenstern, and MSS results cannot replace this target.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing elaborated-
expression fingerprint hard blockers. The intake correctly leaves the canonical human statement,
Lean module and expression, ordered binders and hypotheses, minimal imports, and expression and
environment fingerprints null at `[H1, M4, R4]`. With no canonical target, checked transports and
the required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations
are undefined, not passed. No `Statement.lean`, assumed construction interface, axiom, placeholder,
weakened theorem, or broadened theorem was introduced.

The prerequisite `S56-M-0883-INTAKE` is provisional worker state `[_]`, not master-accepted `[x]`.
Dependency-ordered investigation can record this blocker, but master acceptance of refreshed intake
evidence remains independently required before any later statement transition can be accepted.

## Pinned Lean boundary

The existing discovery-only `IntakeProbe.lean` was re-elaborated with the existing pinned artifacts.
Its six direct imports expose finite simple graphs and regularity, adjacency matrices and Hermitian
spectra, projective special and general linear group quotients, Legendre symbols, and real square
roots. All eleven checks pass under Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The complete probe stdout SHA-256 is
`a7ec652010c73111f342fdc66e3a5ada6352476e7e425638114febfbb8445379`.

The probe defines no LPS parameters, generators, Cayley graph, family, Ramanujan predicate, girth
claim, canonical target, transport, or proof body. Its imports therefore cannot be certified minimal
for an absent target and receive no statement or proof credit. A bounded exact-topic search of
repository-local and pinned-mathlib Lean sources found no LPS or Ramanujan-graph occurrence. This is
discovery-only evidence, not the downstream immutable anchor audit or a global absence claim.

The automation-provided `Formalizations/Lean/.lake` symlink was used read-only. No `lake update`,
`lake build`, dependency clone or fetch, or other `.lake` mutation was run.

## Validation evidence

Commands ran from this worker clone on 2026-07-13 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0883` | 0 | rank 1435; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree are recorded above |
| the two exact `sha256sum` argument lists recorded in `statement-blocker.json` | 0 each | all 18 authority/intake hashes and six pinned adjacent-source hashes agree with the structured blocker |
| `python3 -B Stage1_Instances/THM-M-0883/check_intake.py` | 1 | historical intake replay stops at its first failed assertion because it expects pre-integration intake state `[ ]`; no later checker assertion ran |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake agree with the pinned environment above |
| pinned mathlib revision, tree, and package status checks | 0 | revision and tree agree; package worktree is clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0883/IntakeProbe.lean` | 0 | eleven adjacent APIs elaborated; stdout hash recorded above; no canonical target or proof body |
| bounded exact-topic Lean search | 1 | expected no-match exit; no LPS or Ramanujan-graph occurrence under the bounded terms |
| prohibited Lean construct scan over the owned path | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, or unsafe declaration |
| the exact JSON parse and `python3 -c` invariant commands recorded in `statement-blocker.json` | 0 each | IDs, open state, null target/imports, unchanged vector, four undefined mutations, false completion flags, exact paths, and absent self-test agree |
| `git diff --check -- Stage1_Instances/THM-M-0883 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics |
| `git diff --no-index --check -- /dev/null Stage1_Instances/THM-M-0883/statement-blocker.md` and likewise for `statement-blocker.json` | 1 each | expected raw added-file difference status; both diagnostic streams were empty |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test manifest exists because the exact-statement deliverable is blocked |

## Retry condition and status boundary

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers must
lawfully preserve and hash an immutable 1988 article edition, select and independently approve the
exact theorem or result bundle, and transcribe every incorporated definition, ordered binder,
hypothesis, conclusion, construction branch, exception, boundary case, proof boundary, correction,
and erratum. They must freeze all number-theoretic parameters, `PSL`/`PGL` and generator data, graph
and family conventions, explicitness claim, degree and cardinality, connectedness and bipartiteness,
spectrum and trivial-eigenvalue conventions, girth scope, and neighboring-target ownership.

A fresh statement worker can then encode precisely that source-selected claim, minimize its pinned
imports, serialize and hash its elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node. The
root remains `[H1, M4, R4]`; `audit_complete: false` and `theorem_complete: false`; no debt change,
statement receipt, worker `[_]`, accepted state, or master acceptance is claimed. Because the
assigned phase did not pass its exact-statement gate, `.stage1-worker-selftest.json` remains absent.
