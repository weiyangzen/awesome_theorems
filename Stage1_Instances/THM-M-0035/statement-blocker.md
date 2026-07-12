# Exact-statement gate: blocked

Item: `S56-M-0035-STATEMENT`

Theorem: `THM-M-0035`

Base revision: `f23ca64267b6746e12a641dcc66cc4dbaf1e2191` (tree
`d1872d3251ef6a9c395116467608691849d80496`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0035-INTAKE` has provisional worker
state `[_]` in the authoritative execution DAG, not master-accepted state `[x]`. Rev-5.6 section
10.2 permits this dependency-ordered attempt, so pending master acceptance did not prevent the
inspection. The intake receipt is non-content-addressed, declares `accepted: false`, and has no
accepted receipt ID. Master acceptance remains required before any future statement transition.

Independently, the exact-statement gate cannot pass from the received claim. The repository gives
only the title "Jacobson density theorem" and the gloss "the density theorem for primitive rings,"
with Nathan Jacobson, 1945, and an explicitly untrusted `已验证` label. It supplies no cited theorem
passage, definition of a primitive ring, unitality convention, left/right handedness, ordered
binders, hypotheses, conclusion, topology, boundary cases, proof boundary, or errata disposition.

The intake identifies N. Jacobson, "Structure theory of simple rings without finiteness
assumptions," *Transactions of the American Mathematical Society* 57(2) (1945), 228-245, DOI
`10.1090/S0002-9947-1945-0011680-8`, as a historical lead. A fresh Crossref check confirmed that
bibliographic metadata and exposed an AMS PDF locator, but the endpoint returned an HTML access
page rather than the article. No complete theorem passage was lawfully preserved or inspected.
The other source lead, Falko Lorenz, *Algebra, Volume II*, Chapter 28, F20 (2008), is cited by
pinned mathlib but likewise has not been inspected and independently accepted at theorem-passage
granularity. Bibliographic identity is not an exact mathematical statement.

Several material choices therefore remain open:

- whether the root is stated for a primitive ring or for a chosen faithful simple module;
- whether modules act on the left or right and how `End_R(M)` or its opposite acts on `M`;
- whether the conclusion is finite independent-family interpolation, finite-set agreement with an
  endomorphism, or density in a specified finite topology;
- whether faithfulness and simplicity are premises, incorporated in a primitive-ring predicate,
  or used only in a checked transport;
- the finite index representation, quantifier order, and treatment of empty and singleton
  families, repeated or dependent vectors, the zero ring/module, and finite endomorphism dimension.

These choices produce different propositions. Selecting one from convention, memory, or formal
convenience would invent, broaden, strengthen, or substitute mathematics. Sections 5 and 5.1 of
the rev-5.6 blueprint make statement ambiguity and a missing expression fingerprint hard blockers.
There is consequently no honest canonical expression whose imports can be certified minimal or
whose removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations can be
run. Those mutations are undefined, not passed. The root vector remains `[H1, M3, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned toolchain. Its sole direct import,
`Mathlib.RingTheory.SimpleModule.Basic`, exposes this strong candidate:

```lean
jacobson_density
  (f : Module.End (Module.End R M) M) (s : Finset M) :
  exists r, forall m in s, f m = r • m
```

under `[Ring R] [AddCommGroup M] [Module R M] [IsSemisimpleModule R M]`. It also exposes the
finite-over-the-endomorphism-ring surjectivity corollary. Both candidates elaborate at pinned
mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` and report axioms
`[propext, Classical.choice, Quot.sound]`.

This is real API validation, but it is not exact-statement evidence. `jacobson_density` is a
semisimple-module finite-set theorem; the catalogue gloss is about primitive rings, and no checked
source transport fixes faithfulness, simple-to-semisimple specialization, Schur division-ring and
opposite conventions, independent-family extension, or finite-topology equivalence. The
surjectivity corollary adds a finiteness premise. Neither may be silently substituted for the root,
and the probe import cannot be certified minimal for an absent canonical target.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, clone, fetch, or dependency
mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0035` | 0 | rank 1018; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| Crossref and AMS source-locator inspection | 0 | 1945 article metadata and PDF locator confirmed; the PDF endpoint returned HTML, so no theorem passage was inspected or credited |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0035/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; both candidate declarations reported the three axioms above; no canonical target was declared |
| bounded exact-topic search in pinned mathlib and repo-local Lean | 0 | the two pinned candidates were found; no relevant primitive-ring predicate or another THM-M-0035 Lean root was found; discovery-only evidence |
| `python3 -B Stage1_Instances/THM-M-0035/check_intake.py` | 1 | historical intake replay first stops because it freezes intake state `[ ]` while current authority records provisional `[_]`; it also retains its original exact nine-file inventory, so this statement phase records rather than rewrites historical intake evidence |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0035/statement-blocker.json` plus scoped blocker invariants | 0 | identity, dependency state, null target/imports, unchanged vector, four undefined mutations, false completion flags, and no-self-test boundary agree |
| scoped whitespace checks for both new files and `git diff --check -- Stage1_Instances/THM-M-0035` | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The historical intake checker freezes the original authority state `[ ]`, its nine-file intake
inventory, and the intake worker-packet contract. The integration lane subsequently recorded the
provisional intake state `[_]`, so replay already stops at that earlier state assertion. Adding
statement-phase blocker artifacts also intentionally makes its inventory historical. This run does
not rewrite `check_intake.py`, the intake receipt, instance manifest, target-local DAG, generated
blueprint, or authoritative execution DAG to manufacture agreement.

## Retry Condition And Status Boundary

An accountable source reviewer must preserve and hash a lawful immutable primary or authoritative
source, select and independently approve one exact theorem passage, and transcribe every
incorporated definition, ordered binder, hypothesis, conclusion, proof boundary, convention,
translation decision, erratum, and boundary case. A fresh statement worker can then encode exactly
that claim, minimize pinned imports, serialize and hash the elaborated expression and environment,
compile each credited transport, and execute all four mutation classes. The integration lane must
master-accept the intake dependency before accepting that future statement transition.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
