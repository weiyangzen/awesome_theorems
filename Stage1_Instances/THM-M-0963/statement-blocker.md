# Exact-statement gate: blocked

Item: `S56-M-0963-STATEMENT`

Theorem: `THM-M-0963`

Base revision: `5fe11f4b5e32a06ffb4432460319fc8ae906fe7b` (tree
`64c5aacf7cf3eb79008f5a1970151e3e53cb9966`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0963-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. The intake receipt declares `accepted: false`, is not
content-addressed, lists no accepted receipt IDs, and was recorded against an older repository and
older blueprint and execution-DAG inputs. No accepted dependency receipt exists.

Independently, the exact-statement gate cannot pass. The catalog supplies only the
Ray-Chaudhuri-Wilson theorem name, Ray-Chaudhuri/Wilson attribution, the year 1975, and the gloss
"an upper bound for an L-intersecting family." It omits the ground set, uniformity, definition and
cardinality of `L`, parameter range, family representation, ordered binders, exact bound, source
locator, proof boundary, corrections, errata, and all boundary cases. Its `verified` label is
untrusted under rev-5.6.

The primary bibliographic lead is D. K. Ray-Chaudhuri and R. M. Wilson, *On t-designs*, *Osaka
Journal of Mathematics* 12 (1975), no. 3, 737-744, ISSN `0030-6126`, zbMATH `0342.05018`.
Project Euclid requests returned access-control HTML rather than article content, and the Osaka
repository timed out. Consequently no immutable primary article, exact theorem or corollary,
incorporated definition chain, proof clause, correction, or erratum was inspected and independently
approved.

Immutable secondary sources consistently state the familiar candidate: for positive integers
`0 < s <= k <= n`, an `s`-element set `L` of nonnegative integers, and an L-intersecting
`k`-uniform family of subsets of `[n]`, the family has at most `choose n s` members. This identifies
the theorem family, but rev-5.6 does not permit a secondary restatement or a discovery-only Lean
shape to be silently promoted over the intake's explicit primary-source blocker.

The proposition-changing choices remain open: exactly `s` versus at most `s` permitted values;
finite set versus indexed list for `L`; a finset of distinct blocks versus an indexed family with a
no-duplicates premise; `Fin n` versus an abstract finite ground type; distinct-pair versus self-pair
intersection; the exact `0 < s <= k <= n` endpoints; upper bound alone versus tightness; and the
cases `s = 0`, `k = 0`, `n = 0`, `s = k`, `k = n`, empty `L`, empty or singleton families,
duplicate indexed blocks, `0` in `L`, values above `k`, and out-of-range binomial parameters.

Sections 5 and 5.1 make statement ambiguity and a missing expression fingerprint hard blockers.
There is therefore no canonical expression whose imports can be minimized, no expression or
canonical-environment fingerprint, no credited alternate encoding, and no meaningful
removed-hypothesis, changed-domain, changed-binder-scope, or boundary-case mutation suite. All four
mutation classes are undefined, not passed. No `Statement.lean`, theorem declaration, proof body,
weakened special case, broadened interface, or circular premise was added. The root remains
`[H1, M3, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates under the pinned toolchain with direct import
`Mathlib.Data.Finset.Powerset`. Seven adjacent finite-set, pairwise-intersection,
fixed-cardinality-powerset, and binomial APIs elaborate, as does
`Stage1.THM_M_0963.Intake.CandidateTargetShape`. That declaration is explicitly an unproved,
noncanonical proposition definition. The probe output is 717 bytes and eight lines with SHA-256
`58d9e070cd2e558e1e8770dfe19bd0e2cc16409cfa135d997067a09ca4478714`; stderr is empty.
Its import cannot be certified minimal for an absent canonical target.

A bounded exact-topic search over selected repository-local Lean, pinned mathlib, and this owned
path found only the probe's explanatory Ray-Chaudhuri-Wilson occurrence and generic intersecting-
family documentation. No source-identical terminal declaration was located. This is feasibility
evidence only, not the downstream anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided canonical `.lake` symlink
was used read-only. No dependency update, build, clone, fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran in this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0963` | 0 | rank 1497; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped catalog, Stage0, manifest, blueprint, skill, intake, secondary-source, primary-availability, and pinned-source inspection | 0 | confirmed the null canonical target, inaccessible primary passage, precise secondary candidate, and unresolved proposition choices |
| `python3 -B Stage1_Instances/THM-M-0963/check_intake.py` | 1 | historical intake checker expects authoritative intake state `[ ]`; integration has advanced it provisionally to `[_]`; the stale intake evidence was not rewritten |
| `cd Formalizations/Lean && lake env lean --version`; `lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0963/IntakeProbe.lean` | 0 | seven adjacent APIs and the unproved candidate proposition shape elaborated; stdout hash recorded above; stderr empty |
| bounded Ray-Chaudhuri-Wilson/L-intersecting Lean search | 0 | only discovery prose and generic intersecting-family documentation matched; no source-identical terminal declaration located |
| prohibited-construct scan over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

Final JSON, invariant, whitespace, and absent-self-test checks are recorded in the structured
blocker beside this report.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must
lawfully preserve and hash one immutable primary edition, select and independently approve the
exact theorem or corollary and incorporated definitions, and map every ordered binder, premise,
conclusion, proof boundary, correction, erratum, family convention, intersection convention,
parameter endpoint, tightness clause, and boundary case.

A fresh statement worker can then encode precisely that reviewed claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof
credit, or master acceptance is claimed.
