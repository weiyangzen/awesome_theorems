# Exact-statement gate: blocked

Item: `S56-M-0483-STATEMENT`

Theorem: `THM-M-0483`

Base revision: `464759128569180ab640c412cd80bc5dd2c3b44a` (tree
`8da3c9130640d08d4e179450a0418368d0454745`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0483-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Its receipt is unsigned, non-content-addressed,
`accepted: false`, and supplies no accepted receipt ID. Dependency-ordered preparation can proceed,
but master closure remains dependency ordered.

Independently, the exact-statement gate fails. The repository record supplies only the title
`梅森素数判定`, the gloss `梅森数的素性检验` (primality testing or determination of Mersenne
numbers), Edouard Lucas attribution, and the year 1876. It supplies no publication, formula,
Mersenne-number definition, exponent domain, ordered binders, hypotheses, conclusion, recurrence,
certificate, proof boundary, correction history, or reviewer. Its `已验证` label is untrusted
metadata.

The missing choices alter the proposition rather than merely its notation:

- Lucas's 1876 result that `2^127 - 1` is prime, represented by `Nat.Prime (mersenne 127)`;
- the general necessary condition `Nat.Prime (mersenne p) -> Nat.Prime p`;
- a historical Lucas recurrence or congruence criterion whose exact indexing and hypotheses must
  come from an admitted source; or
- the modern Lucas-Lehmer correctness criterion, presumptively owned by adjacent `THM-M-0484`,
  which the catalog separately calls the 1930 fast test.

Pinned mathlib's archive labels its anonymous proposition `Nat.Prime (mersenne 127)` as Edouard
Lucas (1876). That is the strongest date-matching disambiguation lead, but it is a modern formal
discovery artifact, not the missing primary-source proposition or an independent target-allocation
decision. Selecting it would silently turn a family-level testing claim into one finite primality
certificate. Selecting the general Lucas-Lehmer criterion would instead absorb the neighboring
target without review. `Nat.Prime.of_mersenne` is only a necessary property and cannot replace a
complete primality determination theorem.

Boundary cases make careless broadening concrete. Pinned
`Archive/Examples/MersennePrimes.lean` proves both `Nat.Prime (mersenne 2)` and
`not LucasLehmerTest 2`; therefore an unqualified Lucas-Lehmer equivalence is false. The source must
also decide exponents 0 and 1, natural subtraction, composite exponents, recurrence indexing below
its intended lower bound, and zero-modulus behavior.

Section 5 of the rev-5.6 blueprint makes statement ambiguity and a missing elaborated-expression
fingerprint hard blockers. There is consequently no honest canonical expression for which a
minimal import, fixed elaboration context, checked alternate transport, or removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutation can be certified. Those mutations
are undefined, not passed. No `Statement.lean`, canonical declaration, proof body, statement
fingerprint, or receipt was created. The provisional root vector remains `[H1, M3, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates using the one direct import
`Mathlib.NumberTheory.LucasLehmer`. It checks the Mersenne definition, necessary exponent theorem,
Lucas-Lehmer test and residue, and the sufficiency and necessity directions. All six interfaces
elaborate. The three theorem axiom reports each list only `propext`, `Classical.choice`, and
`Quot.sound`; complete stdout has SHA-256
`4249ced0c5026b5c37fe7d76c2effe3e36af1f68a09321d80fc6e7387336f770`.

This is exact-topic discovery evidence, not target elaboration. The import is sufficient for the
probe but cannot be certified minimal for an absent target. The probe declares no canonical root,
checked source transport, or proof body, and the downstream anchor, provenance, trust, and
composition gates remain untouched.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was reused read-only. No `lake update`, `lake build`, dependency
clone or fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0483` | 0 | rank 1364; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided untracked `.lake` symlink existed; base revision and tree appear above |
| authority, source, scope, crosswalk, task DAG, receipt, and intake inspection | 0 | confirmed provisional dependency, sparse family claim, null formal target, and unresolved source, scope, ownership, definition, binder, conclusion, and boundary choices |
| `sha256sum` over authority, source, intake, toolchain, dependency lock, and pinned exact-topic module inputs | 0 | exact digests are recorded in `statement-blocker.json` |
| `git blame -L 3546,3551 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version`; `lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib revision, tree, and package-status checks | 0 | pinned revision/tree match the values above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0483/IntakeProbe.lean` | 0 | six exact-topic interfaces elaborated; three theorem bodies reported the listed axioms; output hash recorded above; no canonical target or proof body declared |
| bounded case-insensitive Mersenne and Lucas-Lehmer search in repo-local Lean and pinned mathlib | 0 | found the exact-topic module, exponent-127 archive example, and other-target discovery references; no target-owned canonical declaration or reviewed allocation |
| `python3 -B Stage1_Instances/THM-M-0483/check_intake.py` | 1 | historical intake replay stops at its intake-time execution-DAG row fingerprint because integration has changed intake from `[ ]` to `[_]`; this phase did not rewrite historical intake evidence |

The scoped prohibited-declaration scan over the owned Lean probe returned the expected no-match
exit: there is no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe`
declaration. The structured blocker was parsed and checked for item identity, null target/imports,
unchanged debt, four undefined mutation classes, false completion fields, exact two-file ownership,
and the no-self-test boundary. Scoped tracked and new-file whitespace checks passed.

## Retry Condition And Status Boundary

Accountable reviewers must lawfully preserve and hash an immutable primary or approved authoritative
Lucas source, select and independently approve one exact proposition, and transcribe every
incorporated definition, ordered binder, hypothesis, conclusion, proof boundary, dependency,
correction, erratum, translation, and boundary case. They must explicitly decide whether this target
owns the exponent-127 primality result or another precise 1876 criterion and reconcile that decision
with the separate 1930 `THM-M-0484` target. Refreshed intake evidence must also be master-accepted.

A later statement run can then encode exactly that claim, minimize its pinned imports, serialize and
hash the elaborated expression and environment, compile every credited transport, and execute all
four mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`,
accepted state, statement fingerprint, proof credit, or master acceptance is claimed.
