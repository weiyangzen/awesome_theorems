# Exact-statement gate: blocked

Item: `S56-M-0014-STATEMENT`

Theorem: `THM-M-0014`

Base revision: `5ae439adae290d44dcf08cc6439c5fb64154fe47` (tree
`51717feef6efc7076e60ee31e7a1ca0a246fec42`).

## Decision

The exact Lean 4 target cannot be truthfully selected from the admitted source record, so this
statement item remains `[ ]`. Its prerequisite intake is provisional worker state `[_]`, not
master-accepted state `[x]`; the intake receipt declares `accepted: false`, is not content
addressed, has no accepted receipt ID, and deliberately leaves the canonical mathematical claim
and formal target null. Rev-5.6 section 10.2 permits this dependency-ordered investigation, but
master acceptance remains required before any later statement transition can be accepted.

Independently of that dependency boundary, the catalog supplies only the classical gloss that every
finite abelian extension of the rational field is contained in a cyclotomic field. It supplies no
cited immutable source, incorporated definitions, binder-complete proposition, proof boundary,
errata disposition, or independent review. The intake's Washington and Marcus references are
discovery leads only. Adopting one of their formulations without the required source review would
manufacture statement identity rather than elaborate the exact received target.

The unresolved word "contained" changes the proposition's presentation. It may mean literal
subfield inclusion inside a fixed algebraic closure, an embedding of an abstract rational algebra,
or equivalence with an intermediate field of a cyclotomic extension. The record also does not fix
`FiniteDimensional` versus `NumberField`, the packaging of finite abelian Galois extension data, the
cyclotomic-field and algebra-instance model, positive versus nonzero index, whether the witness is
the conductor, the ordered binders, or the treatment of the trivial extension and indices zero,
one, and two. No checked transports identify these candidate encodings.

There is a separate ownership boundary. `THM-M-0419` is another manifest target for the
Kronecker-Weber theorem. Its `Statement.lean` elaborates one abstract-embedding presentation, and
the historical `S1_M_074.lean` records the same candidate shape, but both are foreign discovery
inputs. The authoritative manifest declares no alias, and no accepted duplicate reconciliation,
source-identity decision, or checked transport permits transferring their statement or evidence to
`THM-M-0014`.

Rev-5.6 sections 5 and 5.1 make statement ambiguity and a missing expression fingerprint hard
blockers. With no canonical proposition there is no honest import set to minimize, no serialized
expression or canonical-target environment fingerprint, no credited alternate wrapper, and no
meaningful removed-hypothesis, changed-domain, changed-binder-scope, or boundary-case mutation.
Those outputs are undefined, not passed. The lifecycle stays `planned` and the root vector remains
`[H1, M4, R3]`.

## Pinned Lean Boundary

`IntakeProbe.lean` re-elaborates seven adjacent APIs in the pinned environment: `NumberField`,
`IsAbelianGalois`, `CyclotomicField`, `CyclotomicField.algebraBase`,
`CyclotomicField.isCyclotomicExtension`, `IsCyclotomicExtension.isAbelianGalois`, and `AlgHom`.
This is real substrate validation, but the probe states no canonical target and provides no proof
body. Its imports therefore cannot be certified minimal for an absent target.

For discrimination only, the foreign `THM-M-0419/Statement.lean` also re-elaborates. It types the
candidate that every number field `K` with `IsAbelianGalois Q K` embeds into
`CyclotomicField n Q` for some nonzero `n`. Direct inspection additionally shows that this candidate
can be formed under `Mathlib.NumberTheory.Cyclotomic.Basic`, while Galois-only and
number-field-only imports omit required target vocabulary. This feasibility result does not settle
the source presentation, duplicate ownership, or statement identity and receives no
`THM-M-0014` statement credit.

A bounded exact-name search found no Kronecker-Weber declaration in pinned mathlib. Repo-local
matches were the foreign sibling statement and historical nonterminal material. These observations
are discovery-only evidence, not the downstream immutable anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No `lake update`, `lake build`, dependency
clone or fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0014` | 0 | rank 1064; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned mathlib revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0014/IntakeProbe.lean` | 0 | seven adjacent pinned APIs elaborated; no canonical target or proof body was declared |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0419/Statement.lean` | 0 | the foreign abstract-embedding candidate elaborated and printed; identity and ownership remain unresolved, so it receives no `THM-M-0014` credit |
| pipe the full foreign candidate with only `import Mathlib.NumberTheory.Cyclotomic.Basic` to `lake env lean /dev/stdin` | 0 | candidate formed under the single cyclotomic import; feasibility only |
| pipe `import Mathlib.FieldTheory.Galois.Abelian` plus `#check CyclotomicField` to `lake env lean /dev/stdin` | 1 expected | `Unknown identifier CyclotomicField`; Galois-only import is insufficient |
| pipe `import Mathlib.NumberTheory.NumberField.Basic` plus checks for `IsAbelianGalois` and `CyclotomicField` to `lake env lean /dev/stdin` | 1 expected | both identifiers are unknown; number-field-only import is insufficient |
| `rg -n -i --glob '*.lean' 'kronecker.?weber\|kroneckerweber' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 1 expected | no exact Kronecker-Weber name in pinned mathlib; discovery evidence only |
| the same `rg` query over `Formalizations/Lean/AwesomeTheorems` and `Stage1_Instances/THM-M-0419` | 0 | matches were confined to the foreign sibling and historical nonterminal material |
| `python3 -B Stage1_Instances/THM-M-0014/check_intake.py` before adding blocker artifacts | 0 | planned intake invariants replayed: null target, `[H1,M4,R3]`, duplicate boundary, and six open downstream tasks |
| `python3 -B Stage1_Instances/THM-M-0014/check_intake.py` after adding blocker artifacts | 1 | the historical intake checker freezes its original nine-file inventory; this statement run records the expected inventory mismatch rather than rewriting intake evidence |

## Retry Condition

The integration lane must master-accept the intake before accepting a later statement transition.
Accountable reviewers must preserve and hash a lawful immutable primary or authoritative source,
identify and independently approve the exact theorem and proof boundary, transcribe all incorporated
definitions, ordered binders, hypotheses, conclusion, corrections, and boundary cases, and issue an
accepted identity and canonical-root ownership decision for `THM-M-0014` versus `THM-M-0419`.

A fresh statement run can then encode precisely that claim, minimize the pinned imports, serialize
and hash the elaborated expression and environment, compile every credited transport, and execute
all four required mutation classes.

The historical intake checker also freezes the intake-only nine-file artifact inventory. Adding
these two later-phase blocker files therefore makes its public replay fail at that inventory
assertion. This statement phase does not rewrite the earlier checker, instance inventory, or receipt
because doing so would mutate historical intake evidence rather than validate the assigned node.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. `audit_complete` and `theorem_complete` remain false; no debt-vector change, node
receipt, worker `[_]`, proof, or master acceptance is claimed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json` is emitted.
