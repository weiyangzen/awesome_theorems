# Exact-statement gate: blocked

Item: `S56-M-0980-STATEMENT`

Theorem: `THM-M-0980`

Base revision: `5fe11f4b5e32a06ffb4432460319fc8ae906fe7b` (tree
`64c5aacf7cf3eb79008f5a1970151e3e53cb9966`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0980-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. The intake receipt declares `accepted: false`, has no
accepted receipt ID, and deliberately leaves the canonical mathematical statement and formal
target null. Its historical replay is also stale against the current integrated blueprint hash.
Dependency-ordered investigation is possible, but master acceptance remains required before any
eventual statement transition can be accepted.

Independently, the exact-statement gate cannot pass. The two duplicate repository records supply
only the name "Bennett inequality," George Bennett, the year 1962, and the gloss "tail probability
of a sum of random variables." They give no source, selected proposition, definitions, ordered
binders, hypotheses, constants, conclusion, proof boundary, corrections, reviewer, or boundary
conventions. The adjacent `verified` label is explicitly untrusted under rev-5.6.

The intake identifies George Bennett's 1962 article *Probability Inequalities for the Sum of
Independent Random Variables* as the likely primary source. Only matching bibliographic metadata
was admitted. The article text, an exact proposition with a stable pinpoint locator, incorporated definitions, exact
assumptions and constants, proof boundary, corrections, and errata were not inspected and
independently approved. This source-family lead therefore cannot select a canonical proposition.

The proposition-changing choices remain open: finite or countable indexing; the probability space,
measurability, integrability, and independence convention; centering; one-sided versus absolute and
common versus individual bounds; variance or second-moment input; the exact Bennett rate,
normalization, constants, and zero-case extension; the direction and strictness of the tail event;
the probability codomain; binder order; alternate encodings; and every empty, deterministic, zero,
and endpoint case. Remembered and secondary Bennett formulas differ on these choices. Selecting one
would invent or substitute mathematics rather than elaborate the exact received target.

Rev-5.6 sections 5 and 5.1 make statement ambiguity and a missing expression fingerprint hard
blockers. There is therefore no honest canonical expression for which imports can be certified
minimal, no credited alternate encoding for a checked transport, and no canonical target against
which the required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case
mutations can run. Those mutation results are undefined, not passed. The root vector remains
`[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates with two direct imports for moment-generating
functions, generic Chernoff bounds, independent finite sums, and variance. Six adjacent APIs check
successfully. Four representative theorem axiom reports contain `propext`, `Classical.choice`, and
`Quot.sound`. The probe defines no probability model, bounded-summand data, Bennett rate, canonical
target, transport, or proof body, so its imports cannot be certified minimal for an absent target.

A bounded exact-topic search over pinned mathlib and repository-local Lean found only this probe's
disclaimer and a legacy Bernstein planning string, not a target-specific declaration. This is
discovery-only evidence, not the later immutable anchor audit or a global absence claim.

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
| `python3 scripts/stage1_target.py show THM-M-0980` | 0 | rank 1514; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| exact `sha256sum` argv over the 15 authority, intake, and lock inputs listed in `statement-blocker.json` | 0 | every digest matched the structured blocker; scoped reading confirmed the sparse claim, null target, and open choices |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package status | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0980/IntakeProbe.lean` | 0 | six adjacent APIs and four axiom reports elaborated; stdout SHA-256 `b61ecb4ca6a9cd0732ab4d7f70202d9673ab7f1ae06a4f6e54873d69b7c370b2`; empty stderr |
| bounded search for Bennett names and the article title | 0 | only the intake disclaimer and a legacy planning string matched; output SHA-256 `1884d6895b0f58e39d8ee46c65fa0048423fc01a7aebd53f2e1a5df12dfcb732`; no target-specific declaration located |
| `python3 -B Stage1_Instances/THM-M-0980/check_intake.py` | 1 | historical intake checker rejects its stale recorded hash for the now-integrated blueprint; it was not rewritten or represented as current statement evidence |
| exact prohibited-construct `rg` argv recorded in `statement-blocker.json` | 0 | inner search returned expected exit 1/no-match; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| exact JSON parse, Python invariant/byte checks, tracked and untracked whitespace checks, and absent-self-test argv recorded in `statement-blocker.json` | 0 each | structured blocker and assigned ownership passed; `.stage1-worker-selftest.json` remains absent |

## Retry Condition And Status Boundary

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers must
then lawfully preserve and hash a complete immutable primary or approved authoritative source,
select one exact proposition with a stable pinpoint locator, and independently approve its definitions, ordered binders,
hypotheses, conclusion, proof boundary, corrections, errata, and all boundary cases. They must
freeze the index and probability model, independence and centering, boundedness and variance
conventions, Bennett rate and constants, parameter ranges, tail event, codomain, and degenerate
cases.

A fresh statement worker can then encode precisely that reviewed claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport, and
execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
