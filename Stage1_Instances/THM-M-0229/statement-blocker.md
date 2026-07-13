# Exact-statement gate: blocked

Item: `S56-M-0229-STATEMENT`

Theorem: `THM-M-0229`

Base revision: `db6914155f1f63e835364b89ba0a3b25f1d7f936` (tree
`a5488edccb2687c4ff0bbdccf4650e06b2e45337`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository record. The statement
item remains `[ ]`. Its prerequisite intake is provisional worker state `[_]`, not master-accepted
state `[x]`; its receipt says `accepted: false`, is not content-addressed, has no accepted receipt
ID, and deliberately leaves the canonical mathematical statement and Lean expression null.

Independently of that dependency boundary, the catalog supplies only the gloss "in a neighborhood
of an essential singularity, the function takes all complex values with at most one exception."
It does not supply a bibliography, pinpoint theorem, incorporated definitions, ordered binders,
complete hypotheses, proof boundary, correction history, translation review, or independent
source review. The catalog's `verified` label is untrusted metadata under rev-5.6.

The inspected stable *Encyclopedia of Mathematics* article is a useful secondary source lead. It
states a finite-value version for a single-valued analytic function near an isolated essential
singular point and treats the infinitely-often formulation as a consequence. The intake does not
accept that lead as the canonical source proposition: no immutable local source packet,
incorporated definition chain, assumption and errata crosswalk, or independent review exists.
Material choices therefore remain open:

- whether `f` is ambient on `Complex`, is defined on an open domain, or is a function on a
  punctured domain;
- the exact punctured analyticity and isolated-domain hypotheses;
- a source-faithful definition of an essential singularity, rather than an unreviewed negation of
  removable and pole cases;
- quantification over all neighborhoods, all sufficiently small positive radii, or a punctured
  neighborhood filter;
- finite complex values versus the Riemann sphere, whose meromorphic form has a different
  exception bound;
- one global exceptional value versus an exception that may vary with the neighborhood;
- mere attainment in every punctured neighborhood versus infinitely many distinct preimages
  accumulating at the singularity, and whether multiplicity is relevant;
- finite singularities versus infinity, the arbitrary ambient value `f a`, and regular,
  removable, pole, constant, empty-domain, and sharp omitted-value boundary cases.

Selecting familiar answers would manufacture a textbook variant rather than elaborate the exact
received target. Encoding the desired value-distribution conclusion itself as a structure field or
hypothesis would be circular. Both substitutions are forbidden. Rev-5.6 sections 5 and 5.1 make
statement ambiguity and a missing expression fingerprint hard blockers. With no canonical
proposition, there is no honest import set to minimize, no target or environment-expression
fingerprint, no credited alternate transport, and no meaningful removed-hypothesis,
changed-domain, changed-binder-scope, or boundary-case mutation. Those outputs are undefined, not
passed. The root vector remains `[H1, M4, R3]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with its three pinned imports:

```lean
import Mathlib.Analysis.Complex.RemovableSingularity
import Mathlib.Analysis.Meromorphic.Order
import Mathlib.Topology.ClusterPt
```

All twelve adjacent API checks elaborate. They do not identify the missing proposition.
`MeromorphicAt f a` in this mathlib revision means that some natural power of `z - a` times `f z`
is analytic at `a`; it describes regular, removable, and finite-order pole behavior rather than an
essential singularity. Using its negation as an essential-singularity definition would require a
source-checked equivalence and explicit punctured analyticity. Likewise, `MapClusterPt` can express
a cluster-value condition, but the source lead speaks about actual value attainment in every
neighborhood; no checked transport between those formulations is accepted.

A bounded exact-topic search found no Great Picard or essential-singularity declaration in pinned
mathlib or the repository Lean tree. This is discovery-only evidence, not the downstream immutable
anchor audit or a global absence claim. The probe's imports therefore cannot be certified minimal
for an absent target and receive no statement or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `.lake` symlink was used
read-only. No update, build, clone, fetch, or dependency mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`). The Lean commands
ran from `Formalizations/Lean`; the other commands ran from the repository root.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0229` | 0 | rank 1241; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| bounded read-only repository source, Stage0, intake dossier, and source-lead inspection | n/a | confirmed that the gloss and unaccepted secondary lead do not freeze a binder-complete, independently reviewed proposition; this manual inspection is not an executable recipe |
| `lake env lean --version`; `lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned mathlib revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0229/IntakeProbe.lean > /tmp/thm-m-0229-probe.out` | 0 | twelve adjacent punctured-neighborhood, analytic, meromorphic-order, and cluster-value APIs elaborated; no canonical target or proof body |
| `sha256sum /tmp/thm-m-0229-probe.out` | 0 | stdout SHA-256 `1c38c165d88ee0eb4f1e33770ad5f409f5a9c13b36490d08a8c974487ce35fcd` |
| `rg -n -i --glob '*.lean' 'great.?picard\|picard.?theorem\|essential.?singular' Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 1 | expected no-match result; discovery evidence only |
| `python3 -B Stage1_Instances/THM-M-0229/check_intake.py` | 1 | the historical intake checker expects its original authoritative intake item state `[ ]` and attempts `0`, while the integrated DAG now records provisional `[_]` and attempts `1`; this statement run records rather than rewrites historical intake evidence |
| `rg -n -i --glob '*.lean' '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0229` | 1 | expected no-match result: no prohibited declaration or token |
| `python3 -m json.tool Stage1_Instances/THM-M-0229/statement-blocker.json` | 0 | blocker JSON is syntactically valid |
| `jq -e` with the scoped identity, null-target, unchanged-vector, open-root-cut, and blocker-state predicate recorded in `statement-blocker.json` validation evidence | 0 | all blocker invariants and the absent worker completion claim agree |
| `sha256sum` over the authority, intake, toolchain, and pinned mathlib source inputs enumerated in `statement-blocker.json` | 0 | all recorded fingerprints agree with the files used by this run |
| `git diff --check -- Stage1_Instances/THM-M-0229` | 0 | no tracked whitespace diagnostic |
| `git diff --no-index --check -- /dev/null Stage1_Instances/THM-M-0229/statement-blocker.md` | 1 | expected added-file difference status; no whitespace diagnostic |
| `git diff --no-index --check -- /dev/null Stage1_Instances/THM-M-0229/statement-blocker.json` | 1 | expected added-file difference status; no whitespace diagnostic |
| `test ! -e .stage1-worker-selftest.json` | 0 | root self-test manifest intentionally absent because the statement deliverable did not pass |

## Retry Condition

The integration lane must master-accept the intake before accepting a later statement transition.
Accountable source reviewers must preserve and hash a lawful immutable primary or authoritative
source, transcribe one exact proposition and every incorporated definition, ordered binder,
hypothesis, conclusion, proof boundary, correction, translation, and boundary case, and
independently approve the mapping. In particular, they must decide the function/domain model,
isolated-essential-singularity predicate, neighborhood and global-exception scopes, finite-value
boundary, recurrence clause, multiplicity convention, and singularity-at-infinity policy.

A fresh statement run can then encode precisely that claim, minimize its pinned imports, serialize
and hash the elaborated expression and environment, compile every credited transport, and execute
all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change, statement receipt, worker `[_]`, or master
acceptance is claimed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json` is emitted.
