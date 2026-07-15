# THM-M-1259 proof blocker

Item: `S56-M-1259-PROOF`  
Base revision: `6bf9ee93a322e7d25cf9249226222095f95d1cff`  
Date: 2026-07-16 (Asia/Shanghai)

## Verdict

`blocked`: the exact frozen Lean target is false, so no placeholder-free positive proof body can
truthfully inhabit it. The proof item remains `[ ]`. No theorem-completion or state-transition claim
is made.

`Stage1Instances.THM_M_1259.Counterexample.not_hormanderTarget` kernel-checks the exact type

```text
Not Stage1Instances.THM_M_1259.hormanderTarget
```

with only `propext`, `Classical.choice`, and `Quot.sound` in its axiom report. It instantiates the
universal target at `n = r = 0`, the top domain, zero coefficients and operator, and the zero
measure. Bracket generation is automatic in the subsingleton tangent space. The zero operator maps
a nonzero evaluation distribution to zero; zero is smooth relative to the zero measure, whereas a
nonzero distribution cannot be represented by a density relative to that measure.

This refutes the broadened formal encoding, not Hormander's mathematical theorem. Silently replacing
the arbitrary measure by Lebesgue measure, excluding admitted boundary cases, or assuming the open
analytic core would prove a different proposition and is forbidden by the proof gate.

## Dependency Reuse

The current v2 graph has no hard parent, transitive ancestor, hard edge, or direct reuse hint for
this target. The required ledger records that empty closure and audits both nonblocking shared-module
groups:

- `Mathlib.Analysis.FunctionalSpaces.SobolevInequality`: inspected through `THM-M-1245`; its global
  first-order Sobolev inequality is not the localized variable-coefficient commutator estimate or
  the distributional bootstrap needed here.
- `Mathlib.Analysis.Calculus.VectorField`: inspected through `THM-M-1258`; its bracket predicate and
  coordinate-field example do not prove hypoellipticity for arbitrary bracket-generating fields.

Neither weak co-mention supplies a common terminal proof body or checked transport, and neither
transfers proof credit.

## Validation

The narrow replay used the existing pinned artifacts read-only. It ran Lean 4.29.0 with `--trust=0`,
compiled `Statement.lean` to a temporary `Statement.olean`, then elaborated `Counterexample.lean`
against it. Both commands exited 0, and the exact negation's axiom report was
`[propext, Classical.choice, Quot.sound]`. The v2 DAG validator and target-manifest checks also
exited 0 during preflight. Exact command records are in the adjacent JSON packet.

After this required target-owned blocker JSON was written, the global standard validator reported
that the checked-in v2 DAG differs from a fresh deterministic inventory, because that inventory
sees newly added structured target evidence. A worker is forbidden to regenerate or edit the
authoritative DAG; the integration lane must reconcile this expected post-edit staleness.

No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was performed. Because
the positive proof phase is not self-tested complete, `.stage1-worker-selftest.json` is deliberately
absent.

## Retry Boundary

The statement phase must be reopened first. A source-audited target must bind the intended reference
measure and all required nondegenerate hypotheses, receive a new statement fingerprint and
obligation registry, and then rerun anchor, obligation-tree, proof, and validation work. Even after
that repair, the localized Hormander commutator estimate and regularity bootstrap remain real
formalization obligations.
