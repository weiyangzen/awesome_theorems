# THM-M-0282 exact-statement gate: blocked

Item: `S56-M-0282-STATEMENT`

Base revision: `2226f559136f12fde46b1bf73cdf629043b8a648` (tree
`33cb254ed06b1391379b8e7f88c5e23188957b62`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0282-INTAKE` is provisional worker
state `[_]`, not master-accepted state `[x]`. Its receipt has `accepted: false`, is not content
addressed, and contains no accepted receipt ID. More importantly, that intake deliberately leaves
the exact human claim, canonical Lean expression, minimal imports, ordered binders, hypotheses,
expression fingerprint, and canonical-target environment fingerprint unresolved.

The repository supplies only the title "Chebyshev's inequality," Pafnuty Chebyshev, 1867, and the
gloss "an upper bound on the probability that a random variable deviates from its expectation."
It contains no formula, bibliography, definitions, ordered binders, assumptions, exact conclusion,
proof boundary, correction history, or reviewer. A second target, `THM-M-0992`, has the same title,
attribution, year, importance, status, and a near-identical probability-tail gloss. Category and
legacy scheduling do not establish whether these are deliberate duplicate encodings, a catalogue
duplication to repair, or distinct propositions.

The inspected 1867 source confirms the probability family but does not select a unique modern
statement. Its opening result concerns a sum, followed by an average form. Although the printed
theorem calls its quantities arbitrary, the proof uses product joint weights and therefore relies
on mutual independence. It does not state the required positive or nonzero domain of `alpha`, and
its strict inside-interval lower bound needs a checked complement and boundary transport to become
a modern closed-tail upper bound. Original/translation, priority, corrections, errata, and
independent review also remain open.

Consequently, proposition-changing choices are still unresolved:

- the historical independent-sum or average theorem versus a modern single-variable theorem;
- a probability measure versus an arbitrary finite-measure generalization;
- `MemLp X 2 P` and real variance versus weaker measurability and extended variance;
- a positive real threshold versus a nonzero nonnegative threshold;
- a strict versus closed deviation event and every expectation, variance, coercion, and division
  convention;
- constant variables, zero variance, zero or negative thresholds, null spaces, and nonexistent or
  infinite moments.

Copying `THM-M-0992/Statement.lean`, choosing either pinned mathlib declaration, or reallocating
this ID to the deterministic similarly-sorted sum inequality would decide mathematics and target
identity that the received record does not authorize. Rev-5.6 treats that ambiguity as a hard
statement blocker.

There is no canonical expression whose imports can be certified minimal, no expression or
environment-expression fingerprint, and no approved alternate encoding for a checked transport.
The required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations
are undefined rather than passed. The root vector remains `[H1, M3, R4]`.

## Pinned Lean Boundary

The discovery-only `IntakeProbe.lean` was re-elaborated with its sole direct import,
`Mathlib.Probability.Moments.Variance`. The pinned module exposes two materially different
candidate surfaces:

- `ProbabilityTheory.meas_ge_le_variance_div_sq` assumes a finite measure, `MemLp X 2 mu`, and a
  positive real threshold, and returns a real-variance bound through `ENNReal.ofReal`;
- `ProbabilityTheory.meas_ge_le_evariance_div_sq` assumes only almost-everywhere strong
  measurability and a nonzero nonnegative threshold, and returns an extended-variance bound.

Both declarations and six adjacent interfaces elaborated. Their axiom reports are
`[propext, Classical.choice, Quot.sound]`. This authenticates exact-topic pinned interfaces and
supports the existing `M3` classification only. The probe declares no canonical target, checked
source transport, mutation, or proof body. Its import cannot be certified minimal for an absent
canonical expression.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read only. No update, build, dependency clone or fetch,
or other `.lake` mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`). Lean commands ran
from `Formalizations/Lean`; other commands ran from the repository root unless noted.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0282` | 0 | rank 1288; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped manifest, blueprint, skill, catalogue, Stage0, intake, duplicate-target, historical-source, and pinned-candidate inspection | 0 | the records fix a probability family but do not select a binder-complete proposition or allocate the duplicate target |
| `python3 -B Stage1_Instances/THM-M-0282/check_intake.py` | 1 | historical intake replay expects base `2eea9830...`; current HEAD is `2226f559...`; prior intake evidence was not rewritten |
| `lake env lean --version`, `lake --version`, and pinned mathlib revision/tree/status checks | 0 | Lean, Lake, and mathlib match the environment above; the mathlib package worktree is clean |
| `lake env lean ../../Stage1_Instances/THM-M-0282/IntakeProbe.lean` | 0 | eight interfaces and two axiom reports elaborated; stdout is 1641 bytes with SHA-256 `e95be81d3c5910ef5d867e9217c870ccfb3541beb34370e09bccbe64910cf95c`; no target or proof body was declared |
| prohibited-declaration scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, bodyless `constant`, `opaque`, or `unsafe` declaration |
| JSON parse, scoped invariant and input-hash assertions | 0 | blocker IDs, base, hashes, null target/imports, unchanged vector, false completion flags, mutations, exact two-file scope, and absent-self-test boundary agree |
| trailing-whitespace, final-newline, `git diff --check`, and per-file no-index checks | 0 aggregate | both blocker artifacts passed text hygiene; each no-index command returned only its expected new-file difference exit 1 |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test exists because the exact-statement deliverable did not pass |

There is no applicable `lake env lean <canonical-statement>.lean` command. Treating the candidate
probe as that validation would manufacture the target and misstate feasibility evidence as exact
statement evidence. The historical `check_intake.py` is bound to its intake-time base, authority
hashes, and nine-file inventory; its stale replay was recorded rather than "fixed" in this later
phase.

## Retry Condition

The integration lane must master-accept refreshed intake evidence and resolve the
`THM-M-0282`/`THM-M-0992` allocation. Accountable reviewers must preserve and hash a lawful
immutable primary or authoritative source, select and independently approve one exact proposition,
and crosswalk every incorporated definition, ordered binder, universe, hypothesis, conclusion,
proof boundary, original/translation and priority relationship, correction, erratum, transport,
and boundary case. They must explicitly settle the historical versus modern form, independence,
probability normalization, moment and measurability premises, variance codomain, threshold type,
event convention, and coercions.

A fresh statement run may then encode only that approved claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and execute all four required mutation classes.

This is a truthful blocked statement attempt, not completion of this node or any downstream node.
Lifecycle remains `planned`; `audit_complete: false` and `theorem_complete: false`; no debt-vector
change, statement receipt, worker `[_]`, master acceptance, proof credit, or theorem completion is
claimed. Because the assigned exact-statement phase did not pass, no
`.stage1-worker-selftest.json` is emitted.
