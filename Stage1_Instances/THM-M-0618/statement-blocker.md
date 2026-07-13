# Exact-statement gate: blocked

Item: `S56-M-0618-STATEMENT`

Theorem: `THM-M-0618`

Base revision: `d05520867fab3367a9b61b9544c3e12241204f54` (tree
`fb2cfc62077d5b53e9938632cd6361dd60872067`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the received source record. The
catalog gives only the title Heine-Borel theorem, the Heine/Borel attribution and 1895 date, and
the gloss `R^n中有界闭集等价于紧集` (in `R^n`, bounded and closed sets are equivalent to compact
sets). It supplies no bibliography, theorem locator, definition of `R^n`, dimension convention,
boundedness definition, ordered binders, exact equivalence orientation, proof boundary, errata
record, or independent source review. Stage0 explicitly leaves precise definitions and premises
open. The catalog's `已验证` label is untrusted under rev-5.6.

These omissions are proposition-changing. In Lean, the conventional all-natural-dimensions
candidate could quantify over
`s : Set (EuclideanSpace Real (Fin n))`, while other readings use `Fin n -> Real`, require
positive `n`, fix a dimension externally, or use an arbitrary finite-dimensional real normed
space. Boundedness could be bornological/metric, coordinatewise, or containment in a ball. The
catalog does not say whether its word order denotes the full compact iff closed-and-bounded claim
directly or a source theorem proving only the nontrivial closed-and-bounded-to-compact direction
with the converse incorporated separately. It also does not resolve `n = 0`.

The accepted intake deliberately records these choices as open, leaves the canonical human claim
and formal target null, and names source-statement identity as the first blocker. Selecting the
familiar Euclidean expression now would therefore invent decisions that this target has not
admitted. Replacing it by mathlib's more general proper-Hausdorff-pseudometric-space theorem would
broaden the requested `R^n` root. Neither a conventional candidate nor a broader theorem becomes
exact merely because it elaborates.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing expression
fingerprint hard blockers. With no approved canonical proposition, no direct import can be
certified minimal for the target, no elaborated target expression or environment-expression
fingerprint can be admitted, and no alternate transport or removed-hypothesis, changed-domain,
changed-binder-scope, or boundary mutation can be credited. The four mutations are undefined, not
passed. No `Statement.lean`, axiom, placeholder, weakened special case, broadened theorem, or proof
body was introduced. The root remains `[H1, M3, R4]`.

The prerequisite `S56-M-0618-INTAKE` has only provisional worker state `[_]`, not master-accepted
state `[x]`. Its receipt declares `accepted: false`, is not content-addressed, and contains no
accepted receipt ID. Rev-5.6 permits dependency-ordered preparation, but a statement transition
cannot be accepted until the dependency and this node independently pass their gates.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. Its two direct
imports expose `EuclideanSpace`, the named proper-space Heine-Borel equivalence, its one-way
ingredients, compact/closed/bounded interfaces, and finite-dimensional properness. All seven
checks pass. The direct equivalence and finite-dimensional properness each report only `propext`,
`Classical.choice`, and `Quot.sound` in their axiom output. This is real interface evidence, but the
probe declares no canonical target, checked source-to-Lean transport, statement mutation, or proof
body.

A feasibility-only candidate outside the owned artifact set was also checked with the single
direct import `Mathlib.Analysis.InnerProductSpace.PiL2`:

```lean
def Candidate : Prop :=
  forall (n : Nat) (s : Set (EuclideanSpace Real (Fin n))),
    IsCompact s <-> IsClosed s /\ Bornology.IsBounded s
```

It elaborates in the pinned environment, and the corresponding wrapper using
`Metric.isCompact_iff_isClosed_bounded` elaborates. This demonstrates that the pinned APIs can
express the conventional candidate and that `PiL2` is sufficient as a single direct import for
that candidate. It does not select the candidate as the exact received theorem, establish source
identity, or certify minimal imports for an absent canonical target.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symbolic link and canonical artifacts were used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0618` | 0 | rank 1312; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree appear above |
| catalog, Stage0, intake dossier, scope map, crosswalk, manifest, blueprint, skill, and target-local DAG inspection | 0 | confirmed that the received record does not select a binder-complete proposition and the intake deliberately leaves the exact target null |
| `git blame -L 4587,4592 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded exact-topic `rg` in repository-local Lean and pinned mathlib | 0 | found the intake candidate, the explicitly documented general proper-space theorem and related uses, but no admitted source-identical `R^n` specialization |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib revision/tree and package-status checks | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0618/IntakeProbe.lean` | 0 | seven adjacent APIs elaborated; two axiom reports list `propext`, `Classical.choice`, and `Quot.sound`; stdout SHA-256 `595dfde3b964b3bac43408cface3faeef50a1e3b0d11237a860e0e3257b5264f` |
| `lake env lean /tmp/THM_M_0618_Candidate.lean` from `Formalizations/Lean` | 0 | the conventional Euclidean target and wrapper elaborated with the single direct import `Mathlib.Analysis.InnerProductSpace.PiL2`; stdout SHA-256 `237885ef07857ddd7178cd94a9a139cf79ac099503d8332e6ec2eb255b9de4d1`; feasibility only |
| `python3 -B Stage1_Instances/THM-M-0618/check_intake.py` | 1 | the historical intake checker expects the intake authority at `[ ]`, attempts 0 and its original authority hashes; current integration state is `[_]`, attempts 1, so the old replay fails before this phase and was not rewritten |
| prohibited-declaration scan over owned Lean files | 1 | expected no-match result: no `sorry`, `admit`, `sorryAx`, axiom, constant, opaque, or unsafe declaration; diagnostic `#print axioms` is permitted |

The intake checker is frozen to the intake run's original authority state and nine-file inventory.
It is historical evidence, not a later-phase validator. This statement attempt records its stale
authority failure rather than modifying the intake instance, receipt, checker, target-local DAG,
generated blueprint, or authoritative execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must master-accept the intake dependency before accepting a later statement
transition. Accountable reviewers must preserve and hash a lawful immutable primary or
authoritative source, transcribe and independently approve one exact proposition with every
incorporated definition, ordered binder, hypothesis, conclusion, proof boundary, correction,
erratum, translation, and boundary case, and explicitly decide the `R^n` carrier, dimension range,
boundedness encoding, equivalence boundary, and `n = 0` convention.

A fresh statement worker can then encode precisely that approved claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile each credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`,
master acceptance, statement fingerprint, or proof credit is claimed.
