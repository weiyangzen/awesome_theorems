# Exact-statement gate: blocked

Item: `S56-M-0921-STATEMENT`

Theorem: `THM-M-0921`

Base revision: `a3b18eec39bf04be025b1641cae02f4d44fdf11a` (tree
`fdfff18dea4c6798c5b322b6088dfe556109c134`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0921-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`; the intake receipt declares `accepted: false`, is not
content-addressed, and has no accepted receipt ID. Rev-5.6 section 10.2 permits this
dependency-ordered inspection while concurrency is enabled, but any statement acceptance remains
dependency ordered.

Independently and decisively, the exact-statement gate fails. The repository supplies only the
title "Catalan numbers" and the gloss "counting in many combinatorial problems." It gives no
bibliography, definition of the sequence or object family, finite package boundary, ordered
binder, hypothesis, conclusion, proof boundary, correction history, or boundary convention. Its
`verified` label is untrusted metadata under rev-5.6.

The intake correctly leaves the canonical mathematical claim and Lean expression null. The gloss
can denote materially different roots, including:

- the recursive definition or recurrence for the Catalan sequence;
- the central-binomial quotient formula or its divisibility form;
- the generating-function equation;
- the number of binary trees under a fixed node convention;
- the number of Dyck words or paths under a fixed length convention; or
- a bounded package or schema of enumerations for other Catalan families.

The catalog does not select any one of these and does not say which or how many interpretations
make up "many." It also leaves open the index domain, whether `n = 0` is included, natural-number
versus field division, the counted carrier, labels, rooting, size statistic, and quotient by
isomorphism, rotation, or reflection. Selecting one familiar identity, or conjoining the available
mathlib theorems, would narrow, broaden, or manufacture the received target rather than elaborate
it exactly.

The intake's inspected Stanley *Catalan Addendum* is an authoritative subject-family lead, but the
catalog does not cite that mutable edition, Exercise 6.19, a particular interpretation, or a
proposition combining interpretations. No immutable source admission, pinpoint proof crosswalk,
correction audit, or independent approval selects a root. Rev-5.6 sections 5 and 5.1 make this
ambiguity and the missing elaborated-expression fingerprint hard blockers.

There is consequently no honest canonical Lean target whose imports can be certified minimal, no
credited alternate encoding, and no meaningful removed-hypothesis, changed-domain,
changed-binder-scope, or boundary-case mutation suite. The lifecycle remains `planned`, and the
root vector remains `[H5, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates under the pinned environment. Its direct imports
authenticate several adjacent interfaces:

```text
catalan_succ (n : Nat) :
  catalan (n + 1) = sum (fun i : Fin n.succ => catalan i * catalan (n - i))
catalan_eq_centralBinom_div (n : Nat) : catalan n = n.centralBinom / (n + 1)
succ_mul_catalan_eq_centralBinom (n : Nat) : (n + 1) * catalan n = n.centralBinom
Tree.treesOfNumNodesEq_card_eq_catalan (n : Nat) :
  (Tree.treesOfNumNodesEq n).card = catalan n
DyckWord.card_dyckWord_semilength_eq_catalan (n : Nat) :
  Fintype.card {p // p.semilength = n} = catalan n
PowerSeries.catalanSeries_sq_mul_X_add_one :
  PowerSeries.catalanSeries ^ 2 * PowerSeries.X + 1 = PowerSeries.catalanSeries
```

The exact pretty-printed recurrence uses Lean's bounded-sum notation; the text above is only a
readable description of the checked interface, not a selected canonical target. The probe defines
no target, source transport, or proof body and assigns no statement or proof credit. Its imports
cannot be certified minimal for an absent target. The complete probe stdout has SHA-256
`6905bdd34565c91d65693680081ade0d6ba72930cc34d97ecc1dae9980422797`; stderr is empty.

A bounded topic search found the same pinned Catalan recurrence, closed form, binary-tree count,
Dyck-word count, and generating-series candidates. That is statement-feasibility evidence only,
not the downstream immutable anchor audit or a source-based selection among them.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned
mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, dependency clone, fetch,
or other dependency mutation was run; the pinned mathlib worktree remained clean.

## Validation Record

Commands ran on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0921` | 0 | rank 1463; planned; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink was untracked; base identifiers appear above |
| authority, source, intake, toolchain, lockfile, and imported mathlib `sha256sum` commands | 0 | current input fingerprints are recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version`; `lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package status | 0 | pinned revision/tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0921/IntakeProbe.lean` | 0 | eight adjacent interfaces elaborated and four axiom reports contained only `propext`, `Classical.choice`, and `Quot.sound`; stdout 1021 bytes with hash recorded above; no target theorem |
| bounded Catalan-topic `rg` search over pinned mathlib, repo-local Lean, and this target | 0 | found several materially different candidates; no catalog-selected root or bounded package |
| `python3 -B Stage1_Instances/THM-M-0921/check_intake.py` | 1 | historical intake checker stops because it expects intake authority `[ ]`, while the integrated execution DAG records provisional `[_]` |
| prohibited declaration scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0921/statement-blocker.json` plus scoped invariant checks | 0 | finalized structured blocker parses and its blocked/null-target invariants agree |
| scoped `git diff --check` plus per-new-file no-index checks | 0 aggregate | no whitespace diagnostics; each no-index exit 1 is only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest is absent because the exact-statement deliverable did not pass |

The intake checker is a historical receipt checker. It binds the earlier intake authority state,
shared-input hashes, base revision, and original nine-file inventory. This statement attempt
records its exact replay limitation rather than rewriting the intake receipt, checker, instance,
target-local task DAG, generated blueprint, or authoritative execution DAG to manufacture
agreement.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence before a future statement can be
accepted. Accountable reviewers must preserve and hash a lawful immutable source edition, select
one exact Catalan-number proposition or an explicit finite multi-root package, and independently
approve its full theorem and proof boundary. They must transcribe every incorporated definition,
ordered binder, hypothesis, conclusion, object family, size and labelling convention, equivalence
relation, division convention, correction, erratum, and boundary case, and define the composition
rule for any package.

A fresh statement attempt can then encode precisely that approved claim or package, minimize the
pinned imports, serialize and hash each elaborated expression and environment, compile every
credited transport, and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement item or any
downstream item. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
