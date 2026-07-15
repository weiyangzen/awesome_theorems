# Exact-statement gate: blocked

Item: `S56-M-0116-STATEMENT`

Theorem: `THM-M-0116`

Base revision: `cb7809d0317a837cb067c0d3fe417c84f167b350` (tree
`312398b9378990dd26dbd22392237586d5ed1916`).

## Decision

No exact Lean 4 target can be truthfully elaborated for the frozen claim in the
pinned dependency closure. The claim is finite generation of the concrete
Neron-Severi group of a smooth projective algebraic surface over an
algebraically closed field, where that group is divisors modulo algebraic
equivalence. Pinned mathlib has the surrounding scheme, algebraically closed
field, smooth relative dimension, properness, group finiteness, projective
spectrum, and ring-level Picard APIs. It does not expose all root-critical
objects needed to express the claim:

- no general projective-morphism predicate for an arbitrary scheme over the
  base field;
- no concrete scheme-level divisor or Picard group suitable for this target;
- no algebraic-equivalence congruence on those divisors or line bundles; and
- no Neron-Severi quotient declaration.

Defining an abstract carrier named `NeronSeveriGroup`, an unconstrained
equivalence relation, or a structure field containing the desired quotient
semantics would invent a substitute rather than elaborate the frozen theorem.
Replacing projectivity by properness, or algebraic equivalence by numerical
equivalence, would also change the claim. Therefore the canonical expression,
minimal imports, expression fingerprint, checked transports, and the four
required semantic mutations are undefined rather than passed. The root remains
`H2 / M4 / R4`; lifecycle remains `planned`; audit and theorem completion are
false.

The prerequisite `S56-M-0116-INTAKE` is provisional `[_]`, not master-accepted
`[x]`. Investigation from that record is useful, but an accepted statement
transition would remain dependency-blocked even if an exact target were later
available.

## Rejected Legacy Substitute

`AwesomeTheorems.Stage1.S1_M_036.StatementShape` is discovery input only. It
quantifies over an arbitrary externally supplied additive group, so it never
defines divisors modulo algebraic equivalence. Its surface package omits
algebraic closedness and replaces projectivity with properness. Its successful
elaboration therefore validates only its stated interface boundary, not the
exact rev-5.6 target, and receives no statement or proof credit.

## Pinned Lean Boundary

`StatementInfrastructure.lean` checks adjacent native declarations using the
existing pinned artifacts. It elaborates `Scheme`, `Spec`, `IsAlgClosed`,
`IsProper`, `Smooth`, `SmoothOfRelativeDimension`, `Proj.toSpecZero`,
`AddGroup.FG`, and the ring-level `CommRing.Pic`. Expected-failure probes also
confirm that no declaration named `NeronSeveriGroup` or general
`AlgebraicGeometry.IsProjective` is available under those imports. The file
defines no canonical target, substitute predicate, axiom, or proof body, so its
imports are not claimed minimal for the absent target.

A bounded exact-topic search of pinned algebraic-geometry, ring-theory, and
geometry sources found no scheme-level Neron-Severi, algebraic-equivalence,
scheme Picard/divisor, or projective-morphism interface. The only `IsProjective`
matches were unrelated module-projectivity declarations. This is scoped local
surface evidence, not the later exhaustive anchor audit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake
`5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` at tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build,
clone, fetch, or dependency mutation was run.

## Validation Evidence

Commands ran in this worker clone on 2026-07-15 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0116` | 0 | rank 36, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0116/StatementInfrastructure.lean` | 0 | nine adjacent APIs elaborated and two expected missing-name checks passed; stdout SHA-256 `3e14279a...f4f3`; no target or proof body |
| bounded pinned-source exact-topic search | 0 | only unrelated ring/module `IsProjective` matches; none of the required scheme-level target interfaces was found |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_036.lean` | 0 | legacy parameterized boundary elaborated; its output confirms an abstract group parameter and ring-level Picard APIs, not the exact target |
| Lean/Lake version, manifest hashes, and mathlib revision/tree/status checks | 0 | pinned versions and hashes match `statement-blocker.json`; mathlib worktree is clean |
| prohibited construct scan over owned Lean files | 0 | no `sorry`, `admit`, `sorryAx`, `axiom`, bodyless constant, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0116/statement-blocker.json` | 0 | blocker JSON is valid |
| `git diff --check -- Stage1_Instances/THM-M-0116` | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test packet because the exact statement deliverable failed |

## Retry Condition

First master-accept the intake and independently approve the exact source and
definition mapping. Then pin or implement concrete, conclusion-free Lean
interfaces for projectivity over the base, the selected divisor or scheme
Picard group, algebraic equivalence as an additive congruence, and the resulting
Neron-Severi quotient. A fresh statement run can then elaborate only that
reviewed claim, minimize its imports, serialize its expression and environment,
compile every credited transport, and run removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations.

This records the first failed gate. It is not statement completion, worker
`[_]`, proof credit, audit completion, theorem completion, or master
acceptance. Because the assigned phase is not genuinely self-tested, no
statement receipt or `.stage1-worker-selftest.json` is emitted.
