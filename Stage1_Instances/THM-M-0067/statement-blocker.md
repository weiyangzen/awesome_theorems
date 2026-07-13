# Exact-statement gate: blocked

Item: `S56-M-0067-STATEMENT`

Theorem: `THM-M-0067`

Base revision: `eb9c2192f79a480deff66d2c0f8e31032bcc2d9f` (tree
`57b76c2fceacd8819b0ec8b9abcd42cfcc74b8e2`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0067-INTAKE` has only provisional state
`[_]`, not master-accepted `[x]`, and its receipt is explicitly unaccepted. Rev-5.6 section 10.2
permits this provisional later-node inspection while concurrency is enabled, but master closure
would remain dependency ordered.

Independently, the exact-statement gate cannot pass. The catalog says only that a finite-group
representation is completely reducible when the characteristic does not divide the group order.
It supplies no source edition or theorem passage, scalar convention, finite-dimensionality choice,
representation encoding, definition of complete reducibility, characteristic encoding, ordered
binders, or boundary cases. The intake therefore deliberately leaves the canonical mathematical
statement, Lean expression, expression hash, and canonical environment fingerprint null.

These omissions change the proposition. In particular, complete reducibility may mean that every
invariant subspace has an invariant complement or that a finite-dimensional representation is a
direct sum of irreducibles. Selecting either reading without an approved source decision and
checked transports would invent or substitute mathematics absent from the received claim.
Rev-5.6 sections 5 and 5.1 make this ambiguity a hard blocker. There is consequently no honest
canonical target whose imports can be certified minimal and no target against which the required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary mutations can run. The root
vector remains `[H1, M3, R4]`.

## Source Boundary

The catalog's Heinrich Maschke/1899 attribution has no title or result locator. The intake records
two 1898 bibliographic candidates, DOI `10.1007/BF01448063` and DOI `10.1007/BF01444297`, but no
primary theorem passage, definitions, translation, proof boundary, correction or errata audit, or
independent review was accepted.

A bounded source check inspected Pavel Etingof, Oleg Golberg, Sebastian Hensel, Tiankai Liu, Alex
Schwendner, Dmitry Vaintrob, and Elena Yudovina, *Introduction to Representation Theory*, dated
2011-01-10, author-hosted PDF SHA-256
`2de50b9f1522d2ab80e2160955e5bd2b81c219214bb94ed0e9c45cfaf9bde22c`.
Definition 2.1 on printed page 23 defines a semisimple or completely reducible representation as a
direct sum of irreducibles. Theorem 3.1 on printed page 33 states Maschke's theorem for a finite
group and a field whose characteristic does not divide the group order; its proof reduces to
finding invariant complements for subrepresentations of finite-dimensional representations. This
is an authoritative modern lead, but it is not the catalog's cited source, has no independent
review packet here, and confirms rather than resolves the dimensionality and encoding choice.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates under the pinned toolchain with
`Mathlib.RepresentationTheory.Maschke`. It checks the representation semisimplicity predicate,
representation/module bridge, averaged-projection interfaces, and exact candidate instance
synthesis. The five printed candidate declarations report only `propext`, `Classical.choice`, and
`Quot.sound`. This is API feasibility evidence, not canonical statement or proof credit.

`StatementCandidateProbe.lean` records a narrower statement-only experiment. With the sole direct
import `Mathlib.RepresentationTheory.Semisimple`, the following candidate elaborates for arbitrary
universes and arbitrary representation spaces:

```text
forall k G V [Field k] [Group G] [Finite G] [NeZero (Nat.card G : k)]
  [AddCommGroup V] [Module k V] (rho : Representation k G V),
  Representation.IsSemisimpleRepresentation rho
```

Deleting that import makes the probe fail, so the import is minimal for this candidate module.
But the conclusion is definitionally `ComplementedLattice (Subrepresentation rho)`, and the
candidate has no finite-dimensionality premise. Mathlib's Maschke module itself calls the usual
finite-dimensional direct-sum-of-irreducibles formulation future work. Thus the candidate is
deliberately uncredited and cannot supply the assigned exact target.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `.lake` symlink was used
read-only. No update, build, clone, fetch, or dependency mutation ran.

## Validation Record

Commands ran from this worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0067` | 0 | rank 1098; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| initial `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink was untracked; base identifiers appear above |
| `python3 -B Stage1_Instances/THM-M-0067/check_intake.py` | 1 | the historical intake checker expects authoritative intake state `[ ]` and rejects the integration-updated `[_]`; it was not modified and is not statement evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and `status --short` | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0067/IntakeProbe.lean` | 0 | six adjacent APIs and candidate instance synthesis elaborated; five axiom reports printed; stdout SHA-256 `e37894f81dfade0a772d2064913feb840605895bf49a065be2f8398afec4eb4c`; no canonical target declared |
| bounded catalog, repo-local Lean, pinned mathlib, and modern-source inspection | 0 | found the unresolved complement and direct-sum forms but no approved source choice or checked exact transport |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0067/StatementCandidateProbe.lean` | 0 | the uncredited complement-form candidate elaborated with explicit universes; stdout SHA-256 `752562a5caf25e2cc0c211c1d3934c0c217740b85321124a91900bfac2fc479f` |
| delete the candidate probe's sole direct import and rerun `lake env lean` | 1 | expected failure at unknown statement vocabulary, establishing minimality for the uncredited candidate module only |
| prohibited-declaration scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration found |
| `python3 -m json.tool Stage1_Instances/THM-M-0067/statement-blocker.json` and scoped blocker assertions | 0 | JSON parsed; identity, base, blocked state, null canonical target/import/hash, unchanged vector, four unrunnable mutations, exact changed paths, and absent self-test agree |
| `git diff --check -- Stage1_Instances/THM-M-0067` plus per-new-file checks | 0 wrapper result | no whitespace diagnostics; raw no-index commands returned only the expected new-file difference status 1 |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact target did not elaborate |

## Retry Condition And Status Boundary

Accountable reviewers must preserve and hash a lawful immutable primary or authoritative source,
then independently approve one exact proposition with every incorporated definition, ordered
binder, hypothesis, conclusion, proof boundary, translation, correction, erratum, and boundary
case. They must fix the scalar field, dimensionality, representation convention, characteristic
encoding, and complemented-subrepresentation versus direct-sum meaning. A later statement run can
then encode exactly that claim, minimize pinned imports, serialize its elaborated expression and
environment, compile every credited transport, and execute all four required mutation classes.
Master acceptance of refreshed intake evidence is also required before an accepted statement
transition.

This is the assigned phase's truthful blocker result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. No `.stage1-worker-selftest.json`,
statement receipt, worker `[_]`, accepted state, statement fingerprint, proof body, or proof credit
is claimed.
