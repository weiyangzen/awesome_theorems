# Exact-statement gate: blocked

Item: `S56-M-0095-STATEMENT`

Theorem: `THM-M-0095`

Base revision: `ee8c1843ef3ce74178a990f4e64554c1558c51fa` (tree
`3a34df1cc2089854dc563ab4909cc0586713ad20`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0095-INTAKE` is provisional worker
state `[_]`, not master-accepted state `[x]`; its receipt has `accepted: false` and no accepted
receipt ID. Rev-5.6 permits assigned provisional later-node preparation, so this did not prevent
the present inspection, but it prevents dependency-ordered master acceptance. The historical
intake replay also freezes the earlier authoritative state `[ ]` and now stops at that state check.
This statement phase records the mismatch rather than rewriting intake evidence.

Independently and decisively, the exact-statement gate cannot pass from the received catalog
record. The catalog gives only the title `卡当分解定理` and the gloss
`半单李代数的根空间分解` (root-space decomposition of a semisimple Lie algebra). It gives no
bibliography or proposition locator and does not specify the scalar field, characteristic,
algebraic closure or splitting, finite dimensionality, semisimplicity encoding, choice or meaning
of a Cartan subalgebra, ordinary versus generalized root spaces, root index, internal-direct-sum
contract, companion clauses, or boundary cases. Its `已验证` label is explicitly untrusted under
rev-5.6.

The intake's modern lead does not remove the ambiguity. Etingof's MIT 18.745 notes, Section 19.4,
Proposition 19.11(i), give a direct decomposition for a finite-dimensional semisimple Lie algebra
over an algebraically closed characteristic-zero field, using a chosen Cartan subalgebra and
ordinary simultaneous eigenspaces. Parts (ii)-(iv) add bracket and bilinear-form properties. The
catalog neither cites this edition nor selects part (i) alone or the full package. No complete
definition and proof-node crosswalk, correction or historical audit, lawful preservation record,
or independent source review has been accepted. The lead therefore remains `H1`, not an approved
source root.

Selecting Proposition 19.11(i) from this lead, silently adding its field assumptions, adopting
mathlib's generalized root spaces, or strengthening semisimplicity to `IsKilling` would invent,
narrow, or substitute mathematics. Likewise, proving only a spanning equality would omit the
independence half of an internal direct sum. Rev-5.6 sections 5 and 5.1 make this unresolved
identity and the absent expression fingerprint hard blockers.

There is consequently no honest canonical Lean declaration for which imports can be certified
minimal. No `Statement.lean`, expression serialization, credited alternate transport, or mutation
suite was created. The required removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations are undefined rather than passed. Lifecycle remains `planned`, and the
debt vector remains `[H1, M3, R4]`. No statement receipt or worker completion claim is emitted.

## Pinned Lean Boundary

The discovery-only `IntakeProbe.lean` was re-elaborated using the pinned environment. Its one direct
import, `Mathlib.Algebra.Lie.Weights.Killing`, exposes nine adjacent ordinary/generalized weight,
root-space, independence, spanning, Cartan, bracket, and Killing-form interfaces. The complete
stdout SHA-256 is
`1e9dcca24da0029f252fed189c2372a4181e422ea4ce771fd9c49414641c0018`.

Pinned mathlib defines `LieAlgebra.rootSpace` using generalized weight spaces. It proves generalized
independence and spanning and provides `LieAlgebra.cartan_sup_iSup_rootSpace_eq_top`. Its bridge to
the ordinary eigenvector equation assumes `IsKilling`, while the pinned library documents the
characteristic-zero converse from semisimplicity as missing. These APIs are substantive `M3`
substrate, but the probe declares no canonical target or proof body. Its import therefore cannot be
called the minimal import for an absent target. A bounded exact-topic search found the intake
disclaimer and an adjacent Killing-module decomposition comment, not a source-selected declaration;
this is feasibility evidence only, not the downstream anchor audit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, dependency clone, fetch,
or other `.lake` mutation was performed.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0095` | 0 | rank 1112; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base identifiers appear above |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree recorded above; package worktree clean |
| `sha256sum` over the authority, source, intake, toolchain, and five inspected mathlib inputs | 0 | exact hashes are recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0095/IntakeProbe.lean` | 0 | nine adjacent APIs elaborated; stdout hash recorded above; no canonical target or proof body declared |
| bounded exact-topic search in pinned mathlib, repository-local Lean, and the owned dossier | 0 | one adjacent library comment and the intake disclaimer only; no source-selected exact declaration found |
| `python3 -B Stage1_Instances/THM-M-0095/check_intake.py` | 1 | historical intake replay stops because it freezes authority state `[ ]`, while the current execution DAG records provisional `[_]` |
| prohibited-construct scan over owned Lean files | 1, expected | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| JSON parse and structured blocker invariant check | 0 each | identity, null target/import/fingerprints, four undefined mutations, unchanged vector, and false completion flags agree |
| scoped and per-new-file whitespace checks | 0; 1 expected per new file | no whitespace diagnostics; no-index status is only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

## Retry Condition And Status Boundary

The integration lane must revalidate and master-accept the intake dependency before accepting a
statement transition. Accountable reviewers must also lawfully preserve and hash one complete
primary or authoritative edition, select and independently approve the exact proposition or
explicit clause package, and transcribe every incorporated definition, ordered binder, hypothesis,
conclusion, proof boundary, attribution, correction, and boundary case. The selection must resolve
the field, characteristic, dimension, splitting, semisimplicity, Cartan definition and choice,
ordinary/generalized root transport, root index, internal-direct-sum encoding, companion clauses,
and zero/rank-zero/non-split/positive-characteristic cases.

A fresh statement run may then encode exactly that approved source model, minimize pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. `audit_complete: false` and `theorem_complete: false`; no debt-vector change is
proposed. Because the exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`,
statement receipt, worker `[_]`, or master acceptance is claimed.
