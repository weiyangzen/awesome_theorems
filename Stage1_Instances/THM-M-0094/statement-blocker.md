# Exact-statement gate: blocked

Item: `S56-M-0094-STATEMENT`

Theorem: `THM-M-0094`

Base revision: `250f9e73cbbb3ebd2da9d0cefff78f0ab8c0d056` (tree
`b6e8138c58e31e82f8209cb70fbc0fb253f3654a`).

## Decision

The statement item remains `[ ]`. Its prerequisite, `S56-M-0094-INTAKE`, has provisional worker
state `[_]`, not master-accepted state `[x]`. The intake receipt has `accepted: false`, is not
content-addressed, and has no accepted receipt ID. It requires independent source and formal review
plus integration-lane master acceptance before a dependent statement may be accepted. The intake
validator also cannot replay the current authority state because it freezes the intake item at
`[ ]`, whereas integration now records `[_]`. This attempt records that dependency boundary rather
than rewriting historical intake evidence.

Independently and decisively, the exact-statement gate cannot pass from the received source record.
The catalog supplies only the title "Borel-Weil-Bott theorem," a Borel/Weil/Bott attribution, the
year 1954, and the gloss "geometric realization of representations of compact Lie groups." It
supplies no formula, bibliography, source edition, theorem/page, incorporated definitions, ordered
binders, hypotheses, correction history, boundary policy, or independent source approval. The
catalog's verified label is explicitly untrusted under rev-5.6.

The intake records a precise modern lead, Jacob Lurie's *A Proof of the Borel-Weil-Bott Theorem*,
Theorem 5. In its conventions, a complex reductive algebraic group `G`, Borel subgroup `B`, flag
variety `X = G/B`, character lattice, and shifted line bundle `L_lambda := L_{rho-lambda}` are
fixed. The theorem gives total cohomology vanishing for nonregular `lambda`; for regular `lambda`,
the only nonzero cohomology is in the length of the unique Weyl element sending `lambda` to a
dominant weight and is dual to the irreducible representation of highest weight
`w(lambda) - rho`. The inspected PDF has SHA-256
`57d1df87dc0641ec70bc2e353830897dcabd88dd973d82365ee30713f0a1f8f1`.

That note is not the catalog's cited source, is not the original historical source, has not been
preserved as an admitted immutable source packet, and lacks a completed assumption/correction
crosswalk and independent review. Bott's 1957 *Homogeneous Vector Bundles* is only a bibliographic
lead because its article content was access-blocked during intake. The repository's 1954 date and
combined attribution remain unreconciled. Selecting Lurie's conventions as canonical would
therefore invent a source-selection decision that the assigned phase is not authorized to make.

Material proposition choices remain open:

- compact connected, compact connected semisimple, or complex reductive algebraic group, together
  with any compact-to-complex transport;
- analytic or algebraic flag variety and cohomology category, maximal torus and Borel subgroup;
- homogeneous line-bundle construction, sign or dual convention, coefficient field, and action;
- integral weights, positive roots, Weyl vector, ordinary or dot action, regularity, singularity,
  unique Weyl element, and length convention;
- total vanishing, the unique surviving degree, the returned irreducible representation, highest
  weight, dualization, and equivariance packaging;
- ordered binders, universes, typeclass context, and trivial, rank-zero, torus, central,
  disconnected, wall, nonintegral, nondominant, and degree-zero boundary cases.

These choices change the target's domain, hypotheses, conclusion, or boundary behavior. The
degree-zero Borel-Weil theorem is only a special case and cannot replace the full higher-cohomology
Borel-Weil-Bott root. Generic sheaf cohomology, Lie weights, root systems, group representations,
or a structure that assumes the desired cohomology result are also not admissible substitutes.
Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing elaborated
expression fingerprint hard blockers.

There is consequently no honest canonical Lean target whose imports can be certified minimal, no
credited alternate encoding, and no meaningful removed-hypothesis, changed-domain,
changed-binder-scope, or boundary-case mutation suite. The lifecycle stays `planned`, the vector
stays `[H1, M4, R4]`, and no statement receipt or worker completion claim is emitted.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` was re-elaborated with the pinned environment. Its
six direct imports expose eleven generic global-section, sheaf-cohomology, scheme-module,
Lie-weight/root, representation/irreducibility, and Lie-group interfaces. Three inspected adjacent
theorems report only `propext`, `Classical.choice`, and `Quot.sound`. The probe does not construct a
flag variety or homogeneous line bundle and declares no Borel-Weil-Bott target or proof body.

Bounded exact-topic searches found no Borel-Weil or Borel-Weil-Bott declaration in pinned mathlib
or the repo-local formal modules and no flag-variety or homogeneous-line-bundle declaration in
pinned mathlib. The probe is therefore only a feasibility boundary. Its imports cannot be called
minimal for an absent canonical target, and it supplies no statement or proof credit. Complete
probe stdout has SHA-256
`aef2267700d64ad128c97ae0e86c34d00ae1b4947f5ed82a9de701b52d86f1b5`.

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
| `python3 scripts/stage1_target.py show THM-M-0094` | 0 | rank 1111; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; the base identifiers appear above |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | the pinned Lean and Lake versions recorded above |
| mathlib revision/tree and package status checks | 0 | the pinned revision/tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0094/IntakeProbe.lean` | 0 | eleven adjacent APIs elaborated; three theorem interfaces reported only the three axioms above; no canonical target or proof body; stdout hash recorded above |
| bounded exact-topic searches in pinned mathlib and repo-local formal modules | 1 expected | no Borel-Weil/Bott, flag-variety, or homogeneous-line-bundle declaration matched |
| `python3 -B Stage1_Instances/THM-M-0094/check_intake.py` | 1 | historical intake replay stops at its assertion that the authoritative intake item state is `[ ]`; integration now records provisional `[_]` |
| `python3 -m json.tool Stage1_Instances/THM-M-0094/statement-blocker.json` | 0 | the structured blocker parses as valid JSON |
| scoped blocker invariant assertions | 0 | identity, base, dependency, null target/imports/fingerprints, unchanged debt, four unavailable mutation classes, false completion flags, and exact two-file scope agree |
| scoped prohibited Lean construct scan | 1 expected | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in the owned Lean probe |
| scoped and new-file whitespace checks | 0 / 1 expected | no whitespace diagnostics; no-index returns 1 only for each expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | the worker self-test manifest is intentionally absent because the exact-statement deliverable did not pass |

## Retry Condition And Status Boundary

The integration lane must revalidate and master-accept the intake dependency. Accountable reviewers
must preserve and hash a lawful immutable primary or approved authoritative full
Borel-Weil-Bott theorem passage, reconcile the attribution and date, and independently select one
exact modern formulation. They must fix every incorporated definition, ordered binder, hypothesis,
conclusion, proof boundary, translation, correction, erratum, alternate-form relationship, and
boundary case, together with any compact-group/algebraic-group and analytic/algebraic transports.

A future statement run may then encode precisely that approved claim, minimize pinned imports,
serialize and hash its elaborated expression and environment, compile every credited transport,
and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. `audit_complete: false` and `theorem_complete: false`; no debt-vector change is
proposed. Because the exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`,
statement receipt, worker `[_]`, proof credit, or master acceptance is claimed.
