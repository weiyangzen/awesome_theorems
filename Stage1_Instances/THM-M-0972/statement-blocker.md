# Exact-statement gate: blocked

Item: `S56-M-0972-STATEMENT`

Theorem: `THM-M-0972`

Base revision: `27400857bccc93638c97e9c65859ddf5d5b5f4da` (tree
`3762537e0e5ae46cd70b086da49a69e2fd7b275c`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0972-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. The intake receipt declares `accepted: false`, has no
accepted receipt ID, and deliberately leaves the canonical mathematical statement and formal
target null. Dependency-ordered investigation is possible, but master acceptance remains required
before any eventual statement transition can be accepted.

Independently, the exact-statement gate cannot pass. The repository record supplies only the title
"Janson inequality," Svante Janson attribution, the year 1990, and the gloss "probability of the
union of rare events." It gives no source, selected theorem, definitions, binders, hypotheses,
formula, proof boundary, corrections, reviewer, or boundary conventions. The adjacent `verified`
label is explicitly untrusted under rev-5.6.

The intake records an immutable secondary variant map and two matching 1990 primary-source leads,
but no exact primary proposition has been admitted or independently reviewed. The name can denote
at least two inequivalent nonoccurrence estimates, a Boppana-Spencer product refinement, or
Janson's lower-tail estimate and its quadratic weakening. The catalog's union wording also does
not say whether it intends a union probability or the complementary nonoccurrence event `X = 0`.
Selecting a formula or conjunction would therefore invent or substitute proposition-changing
mathematics rather than elaborate the exact received target.

The remaining encoding choices include homogeneous versus coordinate-dependent sampling; family
indexing and duplicate configurations; empty configurations; ordered versus unordered overlap
pairs and diagonal terms; the definitions and codomains of `lambda`, `Delta`, and `DeltaBar`;
nonoccurrence versus full lower tail; strict versus weak inequalities; and all zero-mean,
zero-denominator, empty-family, endpoint-probability, and threshold-boundary cases.

Rev-5.6 sections 5 and 5.1 make statement ambiguity and a missing expression fingerprint hard
blockers. There is no honest canonical expression for which imports can be certified minimal, no
credited alternate encoding for a checked transport, and no canonical target against which the
required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations can
run. Those mutation results are undefined, not passed. The root vector remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates with four direct imports for independent random sets,
event independence, generic lower-tail Chernoff interfaces, finite union bounds, and binomial random
graphs. Eleven adjacent APIs check successfully. The probe defines no configuration count, overlap
sum, canonical Janson target, transport, or proof body, so its imports cannot be certified minimal
for an absent target.

A bounded exact-topic search over pinned mathlib and repository-local Lean returned no match. This
is discovery-only evidence, not the later immutable anchor audit or a global absence claim. The
intake's separately recorded external Atlas candidate is also uncredited: its inspected Janson
chains reach explicit `sorry`, and its restrictive license remains unresolved.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, clone, fetch, or other
dependency mutation was run.

## Validation Record

Commands ran in this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0972` | 0 | rank 1506; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped catalog, Stage0, manifest, blueprint, skill, and intake inspection | 0 | confirmed the sparse catalog claim, null canonical target, unresolved source selection, and union/nonoccurrence ambiguity |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package status | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0972/IntakeProbe.lean` | 0 | eleven adjacent APIs elaborated; stdout SHA-256 `ce661417facb99c70002c3e59ceea29af3e21171e973a6249e1bd409a0227864`; no canonical target or proof body |
| bounded case-insensitive search for Janson declarations | 1, expected no match | empty output; no target-specific declaration located in the bounded local surface |
| `python3 -B Stage1_Instances/THM-M-0972/check_intake.py` | 1 | historical intake checker rejects the integration-updated authoritative intake state `[_]`; it is stale intake evidence and was not rewritten |

Final JSON, invariant, prohibited-construct, whitespace, and absent-self-test checks are recorded in
the structured blocker beside this report.

## Retry Condition And Status Boundary

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers must
lawfully preserve and hash a complete immutable primary or approved authoritative source, select
one exact proposition or explicit conjunction, and independently approve its definitions, ordered
binders, hypotheses, conclusion, proof boundary, corrections, errata, and boundary cases. They must
also reconcile the catalog's union wording with the selected nonoccurrence or lower-tail form.

A fresh statement worker can then encode precisely that reviewed claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
