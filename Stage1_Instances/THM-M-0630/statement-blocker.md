# Exact-statement gate: blocked

Item: `S56-M-0630-STATEMENT`

Theorem: `THM-M-0630`

Base revision: `997541734bb32f987fb15f163335a82512992120` (tree
`2c866b9d840d48c48ac839740c62d3b9440be0e5`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the received repository record. The
catalog gives only the name Stone-Cech compactification, the Stone/Cech attribution, the year 1937,
and the gloss `完全正则空间的最大紧化` ("the greatest compactification of a completely regular
space"). It does not define complete regularity, compactification, the order behind "greatest", a
competitor, the factor map, its uniqueness or surjectivity, universes, ordered binders, hypotheses,
conclusion, proof boundary, corrections, errata, or boundary cases. Its `已验证` label is untrusted
metadata under rev-5.6.

The intake identified Stone's 1937 Definition 21 and Theorems 78, 79, and 88 as a strong primary-
source family lead, but it did not admit one exact modern proposition. Definition 21 uses a T0
CR-space. Pinned mathlib's `CompletelyRegularSpace` has no T0/T1 requirement, whereas `T35Space`
makes `stoneCechUnit` a dense embedding. Stone's Theorem 88 supports a continuous image of the
constructed extension onto a competitor, while mathlib also exposes a unique-extension property
for arbitrary continuous maps and a categorical compact-Hausdorff reflection. Existence, greatest
compactification, unique extension, surjective domination, and adjunction are related but not
identical roots.

The prerequisite intake therefore deliberately leaves its `canonical_statement`, `canonical_claim`,
Lean module, declaration/expression, expression hash, and canonical-target environment fingerprint
null. Rev-5.6 sections 5 and 5.1 make statement ambiguity and a missing expression fingerprint hard
blockers. Choosing the T3.5 dense-embedding form, the weaker arbitrary-space reflection, a
surjective-factor theorem, or the categorical adjunction in this phase would invent or substitute
proposition-changing mathematics rather than elaborate an independently approved exact claim.

Without a canonical expression, no direct import can be certified minimal, no alternate encoding
can receive a checked transport, and removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations are undefined rather than passed. No `Statement.lean`, assumed interface,
axiom, placeholder, weakened target, broadened target, or proof body was added. Lifecycle remains
`planned`, and the root remains `[H1, M3, R4]`.

The prerequisite `S56-M-0630-INTAKE` has provisional worker state `[_]`, not master-accepted state
`[x]`. Its receipt declares `accepted: false`, is not content-addressed, and contains no accepted
receipt ID. A dependency-ordered blocker inspection is possible, but a later accepted statement
transition still requires dependency acceptance.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates with pinned Lean and mathlib. Its two
direct imports expose the Stone-Cech carrier and unit, compact and Hausdorff instances, continuous
dense unit, dense inducing and dense embedding variants, continuous extension, extension equation,
uniqueness, and categorical hom-set equivalence. The complete stdout has SHA-256
`5456f6851c254ebfb84245a1d66a91698b114b0344e94d467263a01bd18b8adf`; the six diagnostic axiom
reports are `[propext, Classical.choice, Quot.sound]`.

A scratch feasibility file also compiled and proved two plausible modern formulations with the
single direct import `Mathlib.Topology.Separation.CompletelyRegular`: a T3.5 dense-embedding form
with a unique continuous factor to every compact Hausdorff dense-embedding competitor, and a
variant requiring that factor to be surjective. It checked empty, singleton, and already compact
Hausdorff examples as well. The file SHA-256 was
`dd67e17bc1544418b6e35674fa829d77c206210c09c64e651b7cabb44dc533c7`; its complete stdout SHA-256
was `2cb5d78a1e1ba483c92631b1bfad0f5a6d6a9573ed755787678bae1f62b865e7`.

These are real feasibility observations, not canonical-statement evidence. The still weaker
arbitrary-topological-space reflection form needs only
`Mathlib.Topology.Compactification.StoneCech`. Which import is minimal depends on the source-
approved proposition that is currently absent.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `.lake` symlink was reused
read only. No update, build, clone, fetch, or dependency mutation was run; mathlib remained clean.

## Validation Evidence

Commands ran in this isolated worker clone on 2026-07-13 (`Asia/Shanghai`), from the repository
root unless another working directory is shown.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0630` | 0 | rank 1323, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped blueprint, skill, manifest, catalog, Stage0, intake, scope, crosswalk, and task-DAG inspection | 0 | the record is not binder-complete and deliberately leaves the canonical claim and Lean target null |
| `python3 -B Stage1_Instances/THM-M-0630/check_intake.py` before this phase wrote artifacts | 1 | historical intake replay stops at `stale source hash: authoritative_blueprint_sha256`; integration regenerated checklist state after that receipt |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib revision, tree, status, and source-hash checks | 0 | revision/tree and three source hashes agree with the intake record; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0630/IntakeProbe.lean` | 0 | fourteen adjacent interfaces and six diagnostic axiom reports elaborated; stdout hash recorded above |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean /tmp/S630Candidate.lean` | 0 | two plausible factor formulations and three boundary examples compiled and were proved; feasibility only; stdout hash recorded above |
| bounded exact-topic search in repo-local Lean and pinned mathlib | 0 | strong construction, separation, extension, and categorical candidates found; no source-approved canonical root or checked source transport found or credited |

The historical intake checker is evidence scoped to its earlier authority snapshot. Its failure
precedes this phase's files and reflects the integration lane's regenerated blueprint hash.
Rewriting `check_intake.py`, the intake instance or receipt, the target-local DAG, or shared
authorities would alter prior evidence or exceed this assignment, so this phase records the
mismatch instead.

## Retry Condition And Status Boundary

The integration lane must refresh, revalidate, and master-accept the intake dependency. Accountable
reviewers must lawfully preserve and hash one immutable primary or authoritative source; select and
independently approve one exact proposition; and transcribe every incorporated definition, ordered
binder, hypothesis, conclusion, proof boundary, translation, correction, erratum, universe choice,
and boundary case. The review must fix complete-regularity separation, the compactification and
competitor packages, the greatestness order and factor direction, and whether uniqueness and
surjectivity are part of the root.

A fresh statement worker can then encode precisely that approved claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node. The
node remains `[ ]`; lifecycle remains `planned`; the root remains `[H1, M3, R4]`, with
`audit_complete: false` and `theorem_complete: false`; no debt-vector change is proposed. Because
the assigned phase is not genuinely self-tested to its completion gate, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or master acceptance is claimed.
