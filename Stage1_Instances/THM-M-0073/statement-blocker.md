# Exact-statement gate: blocked

Item: `S56-M-0073-STATEMENT`

Theorem: `THM-M-0073`

Base revision: `48abbb2d2eeb89816c5ffc0ad8faafa4b9d24dd0` (tree
`0f26e2c78fb5fff9277cbbdfef5e145fd4ef06f1`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0073-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Preparation may proceed from that predecessor, but its
receipt is unaccepted and its instance deliberately leaves the canonical proposition and Lean
target null.

The repository record supplies only the name Goldschmidt theorem, David Goldschmidt attribution,
the year 1975, and the gloss "a basic result in fusion-system theory." It provides no citation,
theorem locator, displayed proposition, incorporated definitions, ordered binders, hypotheses,
conclusion, proof boundary, correction record, or reviewer. The 1975 paper *Strongly Closed
2-Subgroups of Finite Groups* matches the author and year; the 1974 paper *2-Fusion in Finite
Groups* matches the gloss; and modern sources use Alperin-Goldschmidt for a generation or
factorization theorem involving essential subgroups. No admitted passage selects one of these
roots.

Choosing an abstract saturated fusion system instead of classical conjugation fusion, an arbitrary
prime instead of the 1975 paper's 2-local setting, generation equality instead of explicit
factorization, or any definition of essentiality would change the proposition. The same is true of
decisions about all essential subgroups versus representatives, whether the carrier is indexed
separately, and trivial or empty-factorization cases. These are not notation choices and cannot be
filled from mathematical familiarity without inventing or substituting mathematics.

Rev-5.6 makes statement ambiguity and a missing elaborated-expression fingerprint hard blockers.
There is no honest canonical expression whose imports can be certified minimal, no approved
alternate encoding for a checked transport, and no target against which the required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations can run.
Those mutations are undefined, not passed. The vector remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with the single direct import
`Mathlib.GroupTheory.Focal`. It checks ten adjacent conjugacy, Sylow, normalizer, transfer, and
focal-subgroup interfaces. The two inspected declarations report only `propext`,
`Classical.choice`, and `Quot.sound`. The probe declares no fusion system, essential subgroup,
canonical target, checked transport, or proof body. Consequently its import is recorded only for
the adjacent probe and cannot be certified minimal for an absent target.

A bounded pinned-mathlib search for Goldschmidt, fusion-system, strongly-closed, and
essential-subgroup declarations returned no match. The corresponding repo-local Lean search found
only the probe's disclaimer. This is narrow discovery evidence, not a global absence proof or an
anchor audit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned
mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `.lake` symlink was used
read-only. No update, build, clone, fetch, or dependency mutation was run.

## Validation Record

Commands ran from this worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0073` | 0 | rank 1527; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `git blame -L 540,545 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; `git -C Formalizations/Lean/.lake/packages/mathlib status --short --untracked-files=all` | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0073/IntakeProbe.lean` | 0 | ten adjacent APIs elaborated; stdout was 1529 bytes with SHA-256 `2bcc942a57a1dfb0d1ad70e90eefe4e55a4b80860c5b06593211d18648952f0b`; no canonical target or proof declared |
| `set -o pipefail; git -C Formalizations/Lean/.lake/packages/mathlib grep -in -E 'Goldschmidt\|fusion.?system\|strongly.?closed\|essential.?subgroup' HEAD -- Mathlib \| head -100` | 1 (expected no match) | no exact-topic declaration was located in pinned mathlib |
| `rg -n -i --glob '*.lean' 'Goldschmidt\|fusion.?system\|strongly.?closed\|essential.?subgroup' Formalizations/Lean/AwesomeTheorems Stage1_Instances/THM-M-0073` | 0 | only two probe-disclaimer lines matched; no repo-local target declaration or proof body was identified |
| `python3 -B Stage1_Instances/THM-M-0073/check_intake.py` | 1 | historical intake validator fails closed because integration changed the authoritative intake state from `[ ]` to `[_]`; it was not edited or used as statement evidence |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque)\b\|^[[:space:]]*unsafe\b' Stage1_Instances/THM-M-0073` | 1 (expected no match) | no prohibited Lean declaration or proof escape was found |
| `python3 -m json.tool Stage1_Instances/THM-M-0073/statement-blocker.json`; scoped `jq -e` invariant check | 0 | valid JSON; identity, open blocked state, unchanged vector, null target/imports, four undefined mutations, false completion fields, exact change scope, and absent-self-test declaration agree |
| `git diff --check -- Stage1_Instances/THM-M-0073`; per-new-file `git diff --no-index --check /dev/null` | 0 / expected difference | no whitespace diagnostics in either new artifact |
| absence checks for `.stage1-worker-selftest.json`, `statement-receipt.json`, and `Statement.lean` | 0 | all intentionally absent because exact target elaboration did not pass |

The historical intake checker is bound to intake-time authority hashes and the intake's original
DAG state. The integration lane has since recorded the intake as `[_]`, so the checker fails closed
at that state assertion. It was not changed or represented as passing for this statement attempt.

## Retry Condition And Status Boundary

The integration lane must master-accept the intake before an accepted statement transition.
Accountable reviewers must lawfully preserve and hash one immutable primary or authoritative source,
reconcile the 1974 and 1975 papers with the modern Alperin-Goldschmidt name, and independently
approve one exact proposition. They must transcribe every incorporated definition, ordered binder,
hypothesis, conclusion, proof boundary, correction, erratum, transport, and boundary case. A later
statement run can then encode only that claim, minimize its pinned imports, serialize the elaborated
expression and environment, compile every credited transport, and run all four mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no vector change is proposed. No `.stage1-worker-selftest.json`,
statement receipt, worker `[_]`, master acceptance, statement fingerprint, or proof credit is
claimed.
