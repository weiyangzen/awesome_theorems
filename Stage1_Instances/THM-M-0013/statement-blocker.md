# Exact-statement gate: blocked

Item: `S56-M-0013-STATEMENT`

Theorem: `THM-M-0013`

Base revision: `b09b188fbf6e0e288ddccb92314ef863d473ebad` (tree
`d64707bb77427b4e8569657bcd92a2c7f5713dc9`).

## Decision

The statement item remains `[ ]`. Its prerequisite, `S56-M-0013-INTAKE`, has only provisional
worker state `[_]`. The intake receipt is not content-addressed, declares `accepted: false`, has no
accepted receipt ID, and deliberately leaves the canonical mathematical statement and formal
target null. It also fails replay at this revision because its recorded blueprint hash is stale.
These facts require integration-lane revalidation and master acceptance before a future statement
transition, but they do not prevent this fail-closed inspection.

Independently and decisively, the exact-statement gate cannot pass from the received source record.
The repository gives the name "Fundamental theorem of Galois theory," attributes it to Evariste
Galois in 1832, and says only that field extensions correspond to subgroups of the Galois group.
It supplies no bibliography, binder-complete proposition, definition of Galois extension,
hypothesis list, clause boundary, topology, degenerate-case policy, correction history, or
independent source approval. Its `verified` label is explicitly untrusted under rev-5.6.

The intake inspected two materially different standard results without selecting either one:

- Milne, *Fields and Galois Theory* v5.10, Theorem 3.17 (pages 39-40), treats a finite normal
  separable extension and corresponds intermediate fields with all subgroups. Its full statement
  also includes index/degree, conjugacy, normality, and quotient clauses.
- Milne Theorem 7.13 (pages 98-99) treats a possibly infinite Galois extension and corresponds
  intermediate fields only with closed subgroups in the Krull topology, with analogous additional
  clauses.
- The immutable Stacks source at commit `3683021e95ea1610e2250658d59abc18fdf0bd7b`
  likewise states the finite theorem at Tag `09DW` and a distinct infinite theorem later in the
  same file.

The catalog does not select finite versus infinite scope, all versus closed subgroups, only the
order-reversing correspondence versus the full textbook clause bundle, or the precise Galois
hypotheses and boundary cases. These choices change the proposition. Selecting the convenient
finite mathlib definition, the infinite closed-subgroup definition, or only one inverse identity
would therefore narrow, broaden, or substitute the target. Rev-5.6 sections 5 and 5.1 make this
ambiguity and the missing elaborated-expression fingerprint hard blockers.

There is consequently no honest canonical Lean target whose imports can be certified minimal, no
credited alternate form, and no meaningful removed-hypothesis, changed-domain,
changed-binder-scope, or boundary-case mutation suite. The lifecycle remains `planned`, and the
root vector remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates against pinned mathlib and checks both candidate API
families. For the finite case, pinned
`Mathlib.FieldTheory.Galois.Basic` exposes

```text
IsGalois.intermediateFieldEquivSubgroup :
  [FiniteDimensional F E] -> [IsGalois F E] ->
  IntermediateField F E ≃o (Subgroup Gal(E/F))ᵒᵈ
```

For the possibly infinite case, pinned `Mathlib.FieldTheory.Galois.Infinite` exposes

```text
InfiniteGalois.IntermediateFieldEquivClosedSubgroup :
  [IsGalois k K] ->
  IntermediateField k K ≃o (ClosedSubgroup Gal(K/k))ᵒᵈ
```

The probe also checks the respective fixed-field and fixing-subgroup inverse APIs and selected
normality/open-subgroup interfaces. It defines no canonical target and assigns no statement or
proof credit. Its two direct imports cannot be certified minimal for an absent target. The complete
probe output has SHA-256
`24e8ccd7f3f0c02a8cc80266851f2412bdfbff2800b866450c4c25b8df06e379`.

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
| `python3 scripts/stage1_target.py show THM-M-0013` | 0 | rank 1063; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base identifiers appear above |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0013/IntakeProbe.lean` | 0 | eleven adjacent finite/infinite APIs elaborated; no canonical target or proof body declared; stdout hash recorded above |
| bounded Galois-correspondence search in pinned mathlib and repo-local Lean | 0 | found the two candidate API families and uses; no source-scope selection or exact received target |
| `python3 -B Stage1_Instances/THM-M-0013/check_intake.py` | 1 | historical intake replay stops at `source revision hash mismatch: authoritative_blueprint_sha256` |
| `python3 -m json.tool Stage1_Instances/THM-M-0013/statement-blocker.json` plus scoped `jq -e` invariants | 0 | valid JSON; identity, null target/imports, unchanged vector, four undefined mutations, false completion flags, and blocked state agree |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, axiom, constant, opaque, or unsafe declaration |
| per-new-file `git diff --no-index --check /dev/null ...`; scoped `git diff --check` | 1 for each new file; 0 scoped | expected new-file difference status with no whitespace diagnostics; no tracked whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The intake receipt recorded blueprint SHA-256 `ff073b9d...b4e55e` and execution-DAG SHA-256
`f0640ccd...71b11c`; current authority is `a2d983f3...cfb3e3` and
`b14331ea...05540`. This statement run records that stale predecessor evidence rather than
rewriting the historical intake receipt, instance, task DAG, generated checklist, or authoritative
execution DAG.

## Retry Condition And Status Boundary

Accountable reviewers must preserve and hash one immutable primary or authoritative source root,
select finite or infinite Galois theory, and independently approve its exact theorem passage. They
must transcribe every incorporated definition, ordered binder, hypothesis, correspondence
direction, subgroup closure/topology condition, supplementary clause, correction, erratum, and
boundary case. A fresh statement run can then encode exactly that source model, minimize the pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes. The integration lane must revalidate and
master-accept the intake before accepting that future transition.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. `audit_complete: false` and `theorem_complete: false`; no debt-vector change is
proposed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or master acceptance is claimed.
