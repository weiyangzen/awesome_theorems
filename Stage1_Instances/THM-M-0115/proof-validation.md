# THM-M-0115 proof-phase handoff

Item: `S56-M-0115-PROOF`

Verdict: `blocked`; the assigned positive proof predicate is not satisfied.

The complete v2 hard-parent and transitive-ancestor inspection order is empty.
There are also no reuse hints or shared groups, so no provider declaration,
receipt, body, or checkbox state is consumed. The refreshed
`dependency-reuse-ledger.json` binds that empty audit to graph digest
`8be71ef1e4fa1c3de5aa420550ff915dbe0b9f165ac0d98518adf2d1fe25fd47`,
context digest
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`,
and worker base `307c34d30fc3763c82a944a142ae922b48ff18aa`.

## First failed gate

`P04-KERNEL/EXACT-TARGET-CONSISTENCY` fails. `Proof.lean` constructs a datum
at universes `(0,0)` with `X = Y = Spec(Q)`, identity maps, and `Int` as both
abstract theory carriers. Every named semantic compatibility proposition is
`True`, but `capY` is constantly `1` and `capX` is constantly `0`. All frozen
hypotheses therefore hold while the formula is `1 = 0`.

Lean checks
`Stage1Instances.THMM0115.Proof.not_grothendieckRiemannRochTarget` with exact
type `Not (GrothendieckRiemannRochTarget.{0,0})`. The declaration is sorry-free
under `--trust=0` and reports only `propext`, `Classical.choice`, and
`Quot.sound`.

This is not a refutation of mathematical Grothendieck-Riemann-Roch. It exposes
an overbroad abstract encoding: the proposition fields claiming that operations
have their standard meanings do not constrain those operations. A positive
proof of the exact frozen target would contradict this checked countermodel.
Statement repair, a new expression fingerprint, and downstream refreezing are
required before positive proof work can resume.

## Validation

The worker reused the automation-provided pinned `.lake` symlink read-only. It
did not run `lake update`, `lake build`, clone, fetch, or any dependency
mutation. The authoritative preflight checks passed before the owned proof
delta. The narrow validator command is:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0115/check_proof.py
```

Its stdout is exactly one `stage1-validator-semantic-result/1.0` object. A
successful replay reports `status=blocked`, `verdict=blocked`,
`phase_accepted=false`, `phase_predicate_proven=false`, and
`first_failed_gate=P04-KERNEL/EXACT-TARGET-CONSISTENCY`. The command exit is
zero because the negative evidence packet itself replayed exactly; it does not
mean the proof phase was accepted.

`check_proof.py` was absent at the worker base, so it is not yet an unchanged
HEAD-tracked validator eligible for scheduler selection. Integration must first
commit these exact target-owned bytes. The scheduler can then issue a fresh
claim and replay the unchanged validator from its new base.

This handoff closes no positive obligation and leaves `H4/M3/R4`,
`audit_complete=false`, and `theorem_complete=false` unchanged.
