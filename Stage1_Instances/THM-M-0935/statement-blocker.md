# THM-M-0935 exact-statement gate: blocked

- Item: `S56-M-0935-STATEMENT`
- Base revision: `9c75282d42a7ef447d885d1d56997a79418bcd8a`
- Base tree: `cc5285432a02107fadffb68c698690d1b98ac5f2`
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the accepted repository inputs. The
catalog provides the name "Dias da Silva-Hamidoune theorem," the authors and year 1994, and only
the gloss "proof of the Erdos-Heilbronn conjecture." That identifies a result family, but it does
not select one proposition, give a source locator, or fix binders, hypotheses, conclusion, and
boundary conventions. The catalog's `verified` label is untrusted inventory metadata under
rev-5.6.

The intake records two materially different candidate roots. Later sources call the general
fixed-cardinality restricted-sumset bound

`|h^A| >= min(p, h * (|A| - h) + 1)`

the Dias da Silva-Hamidoune theorem. Other literature uses the same name for its `h = 2`
Erdos-Heilbronn specialization

`|A dot+ A| >= min(p, 2 * |A| - 3)`.

The inspected secondary sources also differ over whether the general range includes `h = 0` or
starts at `h = 1`. The primary 1994 article was not retrieved or inspected, and its internal
theorem, incorporated definitions, exact parameter range, proof boundary, corrections, and errata
are not admitted. No independent reviewer has selected the general theorem, the specialization,
or a checked package relating them. Selecting either candidate now would broaden, narrow, or
substitute proposition-changing mathematics. It would also preempt the unresolved ownership and
transport boundary with `THM-M-0934`.

Even after root selection, proposition-defining choices remain open: `F_p` versus `ZMod p`, set
versus finset presentation, fixed-cardinality subsets versus pairwise-distinct tuples, ordered
binders, nonemptiness, the exact `h` range, natural subtraction, saturation, and all empty,
singleton, `h = 0`, `h = 1`, `h = 2`, `h = |A|`, and `h > |A|` cases. These choices cannot be
filled by convention without changing the target.

Sections 5 and 5.1 of `Docs/Stage1_Blueprint_rev-5.6.md` make statement ambiguity and a missing
expression fingerprint hard blockers. The canonical human statement, Lean module and expression,
minimal imports, elaborated-expression hash, canonical-target environment fingerprint, checked
transports, and the four required mutation classes are therefore undefined, not passed. No
`Statement.lean`, declaration, proof body, weakened specialization, broadened family theorem,
axiom, or placeholder was added. The root remains `[H1, M4, R4]`.

The prerequisite `S56-M-0935-INTAKE` is provisional worker state `[_]`, not master-accepted state
`[x]`. Its receipt is unaccepted and non-content-addressed and supplies no accepted receipt ID.
Section 10.2 permits preparation of this dependency-ordered blocker, but accepted statement
closure remains independently impossible until the intake and exact source decision are accepted.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates with three direct imports:

- `Mathlib.Combinatorics.Additive.CauchyDavenport`
- `Mathlib.Combinatorics.Additive.SubsetSum`
- `Mathlib.Data.Finset.Powerset`

Its ten checks expose `Finset.powersetCard`, finite sums and images, `Finset.subsetSum`, `ZMod`, and
ordinary `ZMod.cauchy_davenport`. They define no restricted fixed-cardinality sumset target,
general `h`-fold bound, `h = 2` transport, or proof body. In particular,
`ZMod.cauchy_davenport` concerns an ordinary two-set sumset and does not enforce distinct
self-summands. The probe imports cannot be certified minimal for an absent canonical target and
receive no statement or proof credit.

A bounded exact-topic search over repository-local Lean, pinned mathlib, and the owned target found
only the probe disclaimer plus an unrelated Hamidoune URL in a different theorem's documentation.
It located no source-selected declaration. This is bounded feasibility evidence, not the later
anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The probe output SHA-256 is
`9e94f8b9f067be5c6256e50eef02f03fb344c7a23888feccf1e05cf4e8ef6e8b`.

The automation-provided `Formalizations/Lean/.lake` symlink points to the canonical pinned
artifacts and was used read-only. No `lake update`, `lake build`, dependency clone or fetch, or
other `.lake` mutation was run.

## Validation Evidence

Commands ran in this isolated worker clone on 2026-07-13 (Asia/Shanghai). Lean commands ran from
`Formalizations/Lean`; all others ran from the repository root unless noted. Exact executable
arguments, exits, result summaries, and current input fingerprints are preserved in
`statement-blocker.json`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0935` | 0 | rank 1474; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree are recorded above |
| scoped reads and SHA-256 checks over the standard, skill, manifest entry, catalog, Stage0 projection, execution DAG, intake dossier, toolchain, lockfile, and relevant mathlib sources | 0 | current authority and input fingerprints are recorded in the structured blocker |
| `python3 -B Stage1_Instances/THM-M-0935/check_intake.py` | 1 | the historical intake replay first fails because its frozen target-DAG row hash predates integration of intake `[_]`; this statement run records rather than rewrites historical evidence |
| pinned Lean, Lake, mathlib revision/tree, and package-status checks | 0 | Lean 4.29.0, Lake 5.0.0, and the expected clean pinned mathlib package worktree passed |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0935/IntakeProbe.lean` | 0 | ten adjacent APIs elaborated; output SHA-256 `9e94f8b9...6e8b`; no target or proof body was declared |
| bounded exact-topic search in pinned mathlib, repository-local Lean, and the owned target | 0 | only the probe disclaimer and an unrelated documentation URL matched; no source-selected declaration was located |
| prohibited-construct scan over owned Lean | 1, expected no match | no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, opaque declaration, or unsafe declaration |
| JSON parse, scoped blocker invariants, whitespace checks, scoped-change check, and absent-self-test check | 0 | blocked identity, null target/imports, unchanged vector, false completion fields, exact two-file scope, valid JSON, clean whitespace, and absent worker manifest agree |

## Retry Condition And Status Boundary

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers must
then lawfully preserve and hash an immutable primary or approved authoritative source, identify one
exact theorem and all incorporated definitions, settle corrections and errata, decide the general
`h` theorem versus `h = 2` specialization and the `THM-M-0934` boundary, and independently approve
the source-to-statement mapping. That review must fix the domain and set encoding, ordered binders,
primality and nonemptiness hypotheses, admissible `h` range, distinctness representation, exact
cardinality arithmetic, conclusion, foundation profile, and every boundary case.

A fresh statement worker can then encode precisely that accepted claim, prove its pinned direct
imports minimal, serialize and hash the elaborated expression and environment, compile every
credited transport, and execute the removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt change is proposed. Because the exact-statement deliverable did
not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or
master acceptance is claimed.
