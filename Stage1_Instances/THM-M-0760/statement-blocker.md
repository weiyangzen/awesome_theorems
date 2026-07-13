# Exact-statement gate: blocked

Item: `S56-M-0760-STATEMENT`

Theorem: `THM-M-0760`

Base revision: `0f70149d61a952d44f907f4662a143372bcb4c44` (tree
`35328e4f56f47446a4e1dfdbe361a1b70a4b18a7`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0760-INTAKE` has provisional worker
state `[_]` in the authoritative execution DAG, not master-accepted state `[x]`. Rev-5.6 section
10.2 permits this dependency-ordered statement attempt, but the intake receipt is `accepted:
false`, contains no accepted receipt ID, and leaves the canonical statement and formal target
null. Master acceptance remains necessary before any future statement transition can be accepted.

The exact-statement gate cannot pass from the received repository record. The mathematical catalog
names the Myhill-Nerode theorem and says only that it is "a characterization of regular languages."
It gives no formula, cited theorem, alphabet domain, ordered binders, definition of regularity or
Nerode equivalence, conclusion package, proof boundary, boundary cases, or errata disposition. A
separate computer-science catalog row says "minimal DFA and distinguishable strings," but that row
projects to excluded target `THM-C-0134`; it does not determine this target's scope or transfer
evidence into it.

At least three proposition-changing decisions therefore remain open:

1. whether the root is only regularity iff finite Nerode index, or also contains the least-state
   cardinality result for recognizing DFAs;
2. whether the alphabet is arbitrary or finite; and
3. whether finite index is represented by a quotient/setoid of the Nerode relation or by the finite
   range of the residual-language map, together with the required checked transport.

Append orientation, right-invariance versus two-sided congruence, reachable-state conventions, and
empty-alphabet and empty-word behavior also remain unfrozen. Selecting any familiar variant would
invent, strengthen, specialize, or substitute mathematics rather than elaborate the exact received
target.

Rev-5.6 sections 5 and 5.1 make statement ambiguity and a missing expression fingerprint hard
blockers. There is consequently no canonical expression whose imports can be certified minimal,
no source-approved alternate encoding for a checked transport, and no canonical target against
which removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations can be
tested. Those mutations are undefined, not passed. The lifecycle remains `planned`, and the root
vector remains `[H5, M3, R4]`.

## Pinned Lean Boundary

Pinned mathlib contains a strong candidate:

```lean
Language.isRegular_iff_finite_range_leftQuotient :
  L.IsRegular <-> (Set.range L.leftQuotient).Finite
```

The existing `IntakeProbe.lean` was re-elaborated through its direct import
`Mathlib.Computability.MyhillNerode`. Ten candidate interfaces elaborated, and Lean reported the
candidate's axioms as `propext`, `Classical.choice`, and `Quot.sound`. The candidate covers the
residual-range characterization over an arbitrary alphabet, but it does not include the separate
minimum-state conclusion. The intake explicitly records it as an uncanonicalized M3 interface.
Re-labeling it as canonical here would violate that source boundary.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read only. No update, build, clone, fetch, or dependency
mutation was run.

## Validation Record

Validation ran on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0760` | 0 | rank 1346; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped inspection of the blueprint, skill, guidelines, target manifest/entry, execution DAG, catalog/Stage0 records, and complete intake dossier | 0 | the catalog does not select one source-complete proposition; intake deliberately leaves the canonical statement, binders, imports, expression hash, and canonical environment fingerprint open |
| `sha256sum` over current authority, source, intake, toolchain, lockfile, probe, and pinned Myhill-Nerode source inputs | 0 | current input digests agree with `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-0760/check_intake.py` | 1 | historical intake replay stops on its intake-time blueprint hash; current authorities changed after intake, and statement artifacts also extend its frozen nine-file inventory |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, x86_64 Linux, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e`, Lean 4.29.0 |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and `status --short` | 0 | pinned revision/tree above; no status output; dependency worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0760/IntakeProbe.lean` | 0 | ten candidate interfaces elaborated; exact residual-range candidate type and its three axioms printed; no canonical target or local proof declared |
| bounded `rg` search for Myhill-Nerode, Nerode, residual, and minimal-DFA declarations in pinned mathlib and shared Lean source | 0 | the exact-topic Lean result was the pinned residual-range module; no minimum-DFA root declaration was located; bounded discovery only, not an anchor audit |
| `python3 -m json.tool Stage1_Instances/THM-M-0760/statement-blocker.json` and scoped invariant check | 0 | identity, dependency state, null canonical target/imports, unchanged vector, four undefined mutations, false completion flags, and absent self-test packet agree |
| prohibited-construct scan over owned Lean files | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-0760` plus per-new-file `git diff --no-index --check` diagnostics inspection | 0 | no whitespace diagnostics; `git diff --no-index`'s ordinary new-file difference exit was handled separately from diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | no self-test packet because the exact-statement deliverable did not pass |

The historical intake checker is bound to intake-time authority hashes and its exact intake-only
file inventory. It is preserved as historical evidence rather than rewritten to make this failed
statement attempt pass.

## Retry Condition And Status Boundary

Accountable reviewers must preserve and hash a lawful immutable primary or authoritative source,
select and independently approve one exact proposition, and transcribe every incorporated
definition, ordered binder, hypothesis, conclusion, proof boundary, correction, and boundary case.
They must also decide the target boundary against `THM-C-0134`, the theorem-strength and alphabet
choices, and the relationship between residual-range and relational/quotient encodings.

A fresh statement worker can then encode precisely that source model, minimize pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and execute all four required mutation classes. The integration lane must also master-accept the
intake dependency before it can accept a statement transition.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. `audit_complete: false` and `theorem_complete: false`; no debt-vector change is
proposed. Because the exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`,
statement receipt, worker `[_]`, proof credit, or master acceptance is claimed.
