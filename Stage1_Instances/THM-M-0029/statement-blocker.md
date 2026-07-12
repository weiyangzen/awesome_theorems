# Exact-statement gate: blocked

Item: `S56-M-0029-STATEMENT`

Theorem: `THM-M-0029`

Base revision: `dc2eb1390c8f2a88e7afcbdbd35f92ab43f64fb8` (tree
`25138aaafcff80ee47bf04805bccd804978e6754`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0029-INTAKE` has provisional worker
state `[_]` in the authoritative execution DAG, not master-accepted state `[x]`. Rev-5.6 section
10.2 permits this dependency-ordered attempt from a provisional predecessor, but master acceptance
remains required before a future statement transition can be accepted.

The exact-statement gate cannot pass from the received repository claim. The catalog names
Nakayama's lemma, attributes it to Tadashi Nakayama in 1951, and says only that it is "about
generators of modules." It gives no citation, formula, definition, ring convention, handedness,
ordered binders, hypotheses, conclusion, boundary cases, proof boundary, or errata disposition.
Its `已验证` label is untrusted metadata under rev-5.6.

The publisher-hosted primary-source candidate inspected at intake confirms the ambiguity. Tadasi
Nakayama's *A Remark on Finitely Generated Modules*, Nagoya Mathematical Journal 3 (1951), pages
139-140, DOI `10.1017/S0027763000012265`, contains five distinct assertions. Assertion II says
that if `N` is the radical of a possibly nonunital ring `R` and a finitely generated right
`R`-module `m` satisfies `m = mN`, then `m = 0`. Assertions I, III, IV, and V have materially
different premises and conclusions. The paper's module-generator language does not establish that
the catalog intended assertion II rather than assertion I, another assertion, or a modern
generator-lifting formulation. The observed PDF SHA-256 is
`1a2eeb7d75a2b8373ea8eddfef547714029550b296bda80d65714134cbd36515`.

Modern sources likewise group inequivalent formulations under the same name. Pinned mathlib
exposes at least a commutative determinant-trick annihilator form, a commutative
Jacobson-radical vanishing form, relative-generation consequences, and a quotient-generator
lifting form. The original assertion II instead uses a possibly nonunital ring and right module.
Choosing the convenient pinned vanishing theorem would silently specialize the ring and module
model; choosing the generator-lifting declaration would change the conclusion. Neither is a
notation-only elaboration of the received catalog record.

Rev-5.6 sections 5 and 5.1 make ambiguity and a missing expression fingerprint hard blockers.
There is therefore no honest canonical expression whose imports can be certified minimal, no
source-approved alternate form for a checked transport, and no canonical target against which the
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations can be
tested. Those mutations are undefined, not passed. The root vector remains `[H1, M3, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with direct import
`Mathlib.RingTheory.Nakayama`. It checks eight public interfaces spanning finite generation,
annihilating scalars, Jacobson-radical vanishing, relative generation, and quotient-generator
lifting. All checks pass in the pinned environment. This is real interface validation, but the
probe declares no canonical target, transport, or proof body. Its import cannot be certified
minimal for an absent target and supplies no statement or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, clone, fetch, or dependency
mutation was run.

## Validation Record

Commands ran from this worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0029` | 0 | rank 1074; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `git blame -L 228,233 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog fields originate at repository commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sha256sum /tmp/thm-m-0029-nakayama.pdf`; `pdfinfo`; `pdftotext -layout` and scoped inspection | 0 | the cached publisher PDF has the hash above, is two pages, and contains distinct assertions I-V; no exact catalog-to-assertion identity follows |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short`; `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | package worktree clean; pinned revision and tree recorded above |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0029/IntakeProbe.lean` | 0 | all eight candidate Nakayama interfaces elaborated; no canonical target or proof was declared |
| `python3 -m json.tool Stage1_Instances/THM-M-0029/statement-blocker.json` plus scoped blocker invariants | 0 | identity, dependency state, null target/imports, unchanged vector, four undefined mutations, false completion flags, and no-self-test boundary agree |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped whitespace checks and `git diff --check -- Stage1_Instances/THM-M-0029` | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the statement deliverable did not pass |

The historical intake checker is bound to the intake-time authority hashes and exact nine-file
inventory. The integration lane has since changed the generated intake state to `[_]`, and this
phase adds blocker artifacts. It is therefore historical rather than a validator for this failed
statement attempt; it was not edited or represented as passing.

## Retry Condition And Status Boundary

Accountable reviewers must preserve and hash a lawful immutable primary or authoritative source,
select and independently approve one exact proposition, transcribe every incorporated definition,
ordered binder, hypothesis, conclusion, proof boundary, correction, and boundary case, and decide
how the source's ring units and right-module convention map into Lean. A fresh statement worker can
then encode precisely that claim, minimize pinned imports, serialize and hash the elaborated
expression and environment, compile every credited transport, and execute all four required
mutation classes. The integration lane must also master-accept the intake dependency before it can
accept a statement transition.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
