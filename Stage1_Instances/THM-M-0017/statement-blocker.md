# Exact-statement gate: blocked

Item: `S56-M-0017-STATEMENT`

Theorem: `THM-M-0017`

Base revision: `936bf2b9e968abd3b79b5b36d32f2f2bff648c7e` (tree
`8c9d3261b0ba9a81deb5bfc19a335a02cb80f962`).

## Decision

The statement item remains `[ ]`. Its prerequisite, `S56-M-0017-INTAKE`, has only provisional
worker state `[_]`. The intake receipt declares `accepted: false`, is not content-addressed, has no
accepted receipt ID, and deliberately leaves the canonical mathematical statement and formal
target null. Replay also fails at this revision because the recorded repository base is no longer
`HEAD`; the recorded blueprint and execution-DAG hashes are stale as well. These dependency facts
require integration-lane revalidation and master acceptance before a future master-accepted `[x]`
statement transition, but they do not prevent provisional dependency-ordered preparation or this
fail-closed inspection.

Independently and decisively, the exact-statement gate cannot pass from the received source record.
The catalog supplies the name "Steinitz theorem," attributes it to Ernst Steinitz in 1910, and says
only "characterization of algebraically closed fields." It supplies no citation, binder-complete
proposition, definitions, assumptions, equivalence direction, boundary-case policy, correction
history, or independent source approval. Its `verified` label is explicitly untrusted under
rev-5.6.

The intake directly inspected a primary paper and found several proposition-changing candidates:

- Section 21, Satz 9, page 287: existence and essential uniqueness of an algebraic closure;
- Section 21, Satz 8, page 286: the more general existence and essential uniqueness of an
  extension sufficient to split a polynomial family;
- Section 17, Satz 2, page 261: a smallest algebraically closed subextension in an already
  algebraically closed overfield; and
- a modern classification reading: algebraically closed fields are classified by characteristic
  and transcendence degree.

The catalog does not select among these roots. It also does not decide whether Satz 9 means an
existence claim alone or an existence-and-uniqueness bundle, or whether the modern reading is an
`iff`, a sufficient isomorphism construction from explicit transcendence bases, or an uncountable
same-cardinality specialization. Those choices change the proposition. Selecting a convenient
mathlib interface would therefore narrow, broaden, or substitute the theorem. Rev-5.6 sections 5
and 5.1 make this ambiguity and the absent elaborated-expression fingerprint hard blockers.

There is consequently no honest canonical Lean target whose imports can be certified minimal, no
credited alternate form, and no meaningful removed-hypothesis, changed-domain,
changed-binder-scope, or boundary-case mutation suite. The lifecycle remains `planned`, and the
root vector remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates against the pinned environment and checks thirteen
adjacent interfaces. The algebraic-closure family includes `AlgebraicClosure`,
`AlgebraicClosure.isAlgebraic`, `IsAlgClosure`, and `IsAlgClosure.equiv`. Together these expose a
chosen same-universe algebraic closure, its algebraicity, the algebraic-closure predicate, and a
base-preserving algebra equivalence between two algebraic closures.

The classification family includes `IsAlgClosed.equivOfTranscendenceBasis`, which returns a ring
equivalence from an equivalence between explicit transcendence-basis index types, and
`IsAlgClosed.ringEquiv_of_equiv_of_char_eq`, which returns a nonempty ring equivalence under shared
`CharP` data, uncountability, and a nonempty equivalence of the underlying types.

Pinned mathlib also explicitly calls
`Field.exists_primitive_element_iff_finite_intermediateField` the Steinitz theorem, but that result
concerns primitive elements of algebraic extensions and is outside the catalog gloss. The probe
defines no canonical target and assigns no statement or proof credit. Its three direct imports
cannot be certified minimal for an absent target. The complete probe output has SHA-256
`03a5ac814996affe830397a7592de35c64bd25e13772a38bcdc85057123a91d8`.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned
mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, dependency clone, fetch,
or other dependency mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0017` | 0 | rank 1066; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base identifiers appear above |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0017/IntakeProbe.lean` | 0 | thirteen adjacent algebraic-closure, classification, transcendence-basis, cardinality, and namesake APIs elaborated; no canonical target or proof body declared; stdout hash recorded above |
| bounded Steinitz/algebraic-closure search in pinned mathlib and repo-local Lean | 0 | found the candidate classification and algebraic-closure APIs plus the incompatible primitive-element namesake; no source-scope selection or exact received target |
| `python3 -B Stage1_Instances/THM-M-0017/check_intake.py` | 1 | historical intake replay stops at its recorded repository-base assertion; current blueprint and execution-DAG hashes also differ from the receipt |
| `python3 -m json.tool Stage1_Instances/THM-M-0017/statement-blocker.json`; scoped `jq -e` blocker invariants | 0 | valid JSON; identity, null target/imports/fingerprints, unchanged vector, four undefined mutations, false completion flags, exact scope, empty accepted evidence, and blocked state agree |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, axiom, constant, opaque, or unsafe declaration |
| per-new-file and scoped whitespace checks | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The intake receipt recorded base revision `d7507761...d419d7`, blueprint SHA-256
`02f31c3b...894f0d2`, and execution-DAG SHA-256 `55a6de4d...c245c`. Current authority is the base
shown above, blueprint `001dd6c3...a116eb`, and execution DAG `203319f4...af3d3`. This statement run
records that stale predecessor evidence rather than rewriting the historical intake receipt,
instance, task DAG, generated checklist, or authoritative execution DAG.

## Retry Condition And Status Boundary

Accountable reviewers must preserve and hash one lawful immutable primary or authoritative source,
select and independently approve one exact Steinitz theorem passage and claim boundary, and
transcribe every incorporated definition, ordered binder, hypothesis, conclusion, uniqueness or
classification direction, correction, erratum, and boundary case. A fresh statement run can then
encode exactly that source model, minimize pinned imports, serialize and hash the elaborated
expression and environment, compile every credited transport, and execute all four required
mutation classes. The integration lane must also revalidate and master-accept the intake before
accepting any resulting statement transition.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. `audit_complete: false` and `theorem_complete: false`; no debt-vector change is
proposed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or master acceptance is claimed.
