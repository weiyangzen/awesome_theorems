# Exact-statement gate: blocked

Item: `S56-M-0021-STATEMENT`

Theorem: `THM-M-0021` (Brauer-Siegel theorem)

Base revision: `5ae439adae290d44dcf08cc6439c5fb64154fe47` (tree
`51717feef6efc7076e60ee31e7a1ca0a246fec42`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0021-INTAKE` has provisional worker
state `[_]` in the authoritative execution DAG, not master-accepted state `[x]`. Rev-5.6 section
10.2 permits this dependency-ordered statement inspection, so pending master acceptance did not
prevent the attempt. The intake receipt is non-content-addressed, declares `accepted: false`, and
has no accepted receipt ID. Master acceptance remains necessary before any future statement
transition can be accepted.

Independently, the exact-statement gate cannot pass from the received claim. The two identical
repository records say only "asymptotic estimates of number-field class numbers." They do not
identify a source proposition or determine:

- an explicit sequence, a directed family, or another varying-field encoding;
- normal, Galois, fixed-degree, bounded-degree, or other family restrictions;
- the exact degree-versus-discriminant growth hypothesis;
- class number alone or the class-number/regulator product;
- absolute discriminant, square-root discriminant, root discriminant, and logarithmic
  normalization conventions;
- a limit, asymptotic equivalence, or bounds, including codomain and filter; or
- rational, degree-one, repeated-field, bounded-discriminant, finite-family, and logarithmic
  boundary cases.

These choices yield materially different propositions. The intake records Brauer's 1947 and 1950
papers only as uninspected bibliographic leads. No immutable primary passage, exact part and page,
incorporated definitions, premise map, correction or erratum disposition, relationship to Siegel's
contribution, or independent source review has been admitted. Selecting a familiar modern variant
from convention would invent, narrow, broaden, or substitute mathematics.

Sections 5 and 5.1 of the rev-5.6 standard make statement ambiguity and a missing elaborated
expression fingerprint hard blockers. There is therefore no canonical expression whose imports
can honestly be certified minimal, no credited alternate form to transport, and no meaningful
removed-hypothesis, changed-domain, changed-binder-scope, or boundary mutation. Those four tests
are undefined rather than passed. The root vector remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned toolchain. Its two direct imports,
`Mathlib.NumberTheory.NumberField.ClassNumber` and
`Mathlib.NumberTheory.NumberField.Units.Regulator`, expose `NumberField.classNumber`,
`NumberField.Units.regulator`, `NumberField.discr`, their adjacent positivity/nonzero facts, and
`Filter.Tendsto`. The probe elaborates successfully, but it deliberately declares no
Brauer-Siegel proposition or proof body. Its imports are therefore API-discovery inputs, not a
minimal import certificate for the absent target.

Pinned mathlib also contains fixed-field ideal-counting asymptotics and Dedekind-zeta/class-number
formula infrastructure. Neither is the varying-field Brauer-Siegel claim, and neither receives
statement or proof credit here. A bounded name search found no Brauer-Siegel-named declaration in
the pinned mathlib tree; this is discovery evidence only, not the downstream anchor audit or an
absence proof.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided canonical `.lake` symlink
was used read-only. No update, build, clone, fetch, or dependency mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0021` | 0 | rank 1068; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `sha256sum` over authority, intake, toolchain, and pinned mathlib inputs | 0 | hashes are recorded in `statement-blocker.json` and were independently compared with the files |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0021/IntakeProbe.lean` | 0 | eight adjacent number-field invariant and generic-filter API checks elaborated; no canonical target or proof body was declared |
| bounded Brauer-Siegel name search in pinned mathlib | 1 | expected no-match result; no named declaration found, with no absence or anchor-audit claim |
| `python3 -B Stage1_Instances/THM-M-0021/check_intake.py` | 1 | historical intake replay first stops at `source revision hash mismatch: authoritative_blueprint_sha256`; this phase records rather than rewrites stale intake evidence |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| JSON parse and scoped invariant check for `statement-blocker.json` | 0 each | blocker identity, dependency, null target/imports, unchanged vector, four undefined mutations, false completion flags, exact two-file scope, and absent self-test agree |
| `git diff --check -- Stage1_Instances/THM-M-0021` plus per-new-file no-index checks | 0; 1 each | no whitespace diagnostics; both no-index exits are only the expected new-file differences |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The historical intake validator binds an older blueprint and execution-DAG snapshot and the
original nine-file intake inventory. This statement phase does not rewrite `check_intake.py`, the
intake receipt, instance manifest, target-local DAG, generated blueprint, or authoritative DAG to
manufacture agreement.

## Retry Condition And Status Boundary

Accountable source reviewers must preserve and hash a lawful immutable primary or authoritative
source, select and independently approve one exact Brauer-Siegel passage, and transcribe every
incorporated definition, ordered binder, family restriction, growth hypothesis, invariant,
normalization, conclusion, filter, proof boundary, correction, erratum, and boundary case. A fresh
statement worker can then encode precisely that claim, minimize pinned imports, serialize and hash
the elaborated expression and environment, compile every credited transport, and execute all four
required mutation classes. The integration lane must also revalidate and master-accept the intake
dependency before accepting that later statement transition.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof
credit, or master acceptance is claimed.
