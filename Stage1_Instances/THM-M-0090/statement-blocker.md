# Exact-statement gate: blocked

Item: `S56-M-0090-STATEMENT`

Theorem: `THM-M-0090`

Base revision: `56cce0660d633175f8e66c4a538e5c7dce64652e` (tree
`94920deccabd41cd711821885fe08d62eed67a4e`).

## Decision

The statement item remains `[ ]`. Its prerequisite, `S56-M-0090-INTAKE`, has provisional worker
state `[_]`, not master-accepted state `[x]`. The intake receipt has `accepted: false`, is not
content-addressed, and has no accepted receipt ID. Its reviewer policy requires independent source,
formal, and integration review before downstream statement work, but no such accepted review is
recorded. The historical intake validator also cannot replay the current authority state because it
freezes the intake item at `[ ]` while the integration DAG now records `[_]`. This attempt records
that dependency boundary rather than rewriting historical intake evidence.

Independently, the exact-statement gate cannot pass from the received source record. The catalog
gives the name "Weyl character formula," Hermann Weyl, 1925, and only the gloss "a character formula
for Lie-group representations." It supplies no formula, bibliography, theorem/page, incorporated
definitions, ordered binders, hypotheses, corrections, boundary policy, or independent source
approval. The catalog's verified label is explicitly untrusted under rev-5.6.

The intake inspected a useful modern source lead: Etingof's 2024 MIT OpenCourseWare notes, Section
26, Theorem 26.4. It states the formal-character formula for the irreducible finite-dimensional
module `L_lambda` of a complex semisimple Lie algebra for a dominant integral highest weight
`lambda`. This supports `H1`, but it is not the catalog's cited source, has no accepted definition
and assumption transport, and has not passed correction review, lawful immutable preservation, or
independent review. It also does not decide whether the catalog intends this formal-character
theorem or a pointwise compact Lie-group theorem.

Material proposition choices therefore remain open:

- compact connected Lie group versus complex semisimple Lie algebra, including connectedness,
  simply connectedness, integrability, and central-quotient conventions;
- the representation category, coefficient field, finite dimensionality, irreducibility, highest
  weight, dominance, and integrality assumptions;
- maximal torus or Cartan subalgebra, positive roots, weight lattice, Weyl action and sign, Weyl
  vector, and normalization;
- a formal character in an integral group algebra, a denominator-free cross-multiplied identity,
  or a pointwise quotient on regular torus elements;
- singular denominator behavior, equality domain, ordered binders, and the rank-zero, trivial,
  zero-highest-weight, empty-root, non-dominant, and non-integrating boundary cases.

These choices change the target's binders, assumptions, conclusion, or boundary behavior.
Selecting a familiar quotient from memory, encoding only a root-system identity, proving the Weyl
dimension formula, or storing the desired identity in a premise would invent, narrow, or substitute
the theorem. Rev-5.6 sections 5 and 5.1 make statement ambiguity and the missing elaborated
expression fingerprint hard blockers.

There is consequently no honest canonical Lean target whose imports can be certified minimal, no
credited alternate encoding, and no meaningful removed-hypothesis, changed-domain,
changed-binder-scope, or boundary-case mutation suite. The lifecycle stays `planned`, the vector
stays `[H1, M4, R4]`, and no statement receipt or worker completion claim is emitted.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` was re-elaborated with the pinned environment. Its
three direct imports expose generic representation characters, Lie-module weights, a Lie-algebra
root system, and Weyl-group interfaces. It checks `FDRep.character`,
`Representation.character`, `LieModule.weightSpace`, `LieModule.Weight`,
`LieAlgebra.IsKilling.rootSystem`, `RootPairing.weylGroup`,
`RootPairing.weylGroupToPerm`, `RootPairing.weylGroupRootRep`, and
`RootPairing.weylGroupCorootRep`.

The probe does not declare a Weyl character formula, construct highest-weight representation data,
or connect the generic character to a Weyl numerator and denominator. A bounded exact-topic search
found no matching declaration in pinned mathlib; repo-local hits are distinct affine
Kac-Peterson/Weyl-Kac or Kazhdan-Lusztig material. The probe's imports are therefore only a
feasibility boundary and cannot be called minimal imports for an absent canonical target. Complete
probe stdout has SHA-256
`908889696cb550ba89898ce037db12b2fc5dbf96f9696b224b5206b1c9fab709`.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, dependency clone, fetch,
or other `.lake` mutation was performed.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`). Exact argv and result
records, source hashes, and environment pins are preserved in `statement-blocker.json`.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0090` | 0 | rank 1107; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base identifiers appear above |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib revision/tree and package status checks | 0 | pinned revision/tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0090/IntakeProbe.lean` | 0 | nine adjacent APIs elaborated; no target declaration or proof body; stdout hash recorded above |
| bounded `weyl.?character|character.?formula` search in pinned mathlib | 1 expected | no exact-topic match; discovery-only evidence |
| `python3 -B Stage1_Instances/THM-M-0090/check_intake.py` | 1 | historical replay stops because authoritative intake state changed from `[ ]` to provisional `[_]` |

The structured blocker was also parsed and checked for exact identity, null target and fingerprints,
unchanged debt, four unavailable mutation classes, false completion flags, and blocked status. A
prohibited Lean construct scan found no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`,
or `unsafe` declaration. New-file and scoped whitespace checks passed, and absence of the root
worker self-test manifest was explicitly checked.

## Retry Condition And Status Boundary

Accountable reviewers must preserve and hash a lawful immutable primary or approved authoritative
theorem passage and independently select its exact modern formulation. They must fix every
incorporated definition, ordered binder, hypothesis, conclusion, correction, erratum,
normalization, coercion, denominator condition, equality domain, and boundary case. Any transport
between a semisimple Lie-algebra formal character and the selected Lie-group statement must be
checked rather than assumed.

A future statement run may then encode exactly that approved model, minimize pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and execute all four required mutation classes. The integration lane must also revalidate and
master-accept the intake dependency before accepting that transition.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. `audit_complete: false` and `theorem_complete: false`; no debt-vector change is
proposed. Because the exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`,
statement receipt, worker `[_]`, or master acceptance is claimed.
