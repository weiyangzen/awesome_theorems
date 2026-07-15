# THM-M-1036 proof-phase blocker at `6bf9ee93` (slot22)

Item: `S56-M-1036-PROOF`

Date: `2026-07-16` (`Asia/Shanghai`)

Base revision: `6bf9ee93a322e7d25cf9249226222095f95d1cff`.

## Verdict

`blocked`. A legal positive proof body cannot inhabit the exact frozen target.
The tracked, placeholder-free declaration

```text
Stage1Instances.THM_M_1036.Counterexample.not_sdeExistenceUniquenessTarget :
  Not Stage1Instances.THM_M_1036.SdeExistenceUniquenessTarget.{0}
```

kernel-checks at trust level zero. `IntegralSemantics` supplies arbitrary
`timeIntegral` and `itoIntegral` operations, while `standard_time_integral`
and `standard_ito_integral` are bare propositions imposing no laws. The target
quantifies over every such semantics and concludes strong existence after
receiving proofs of those propositions.

`Counterexample.lean` sets both propositions to `True`, uses `Unit` with its
Dirac probability measure, state dimension one and noise dimension zero, and
defines `timeIntegral f _ omega = f 0 omega + 1`. At `t = 0`, the integral
equation yields `x = x + 1` in coordinate zero. Hence a positive proof of the
universe-polymorphic target would contradict its checked universe-zero
specialization.

This refutes the frozen Lean encoding, not the classical SDE theorem. A
repaired, strengthened, or narrower statement would be a forbidden theorem
substitution in this proof item. The item remains `[ ]`; no proof receipt,
self-test manifest, root closure, or theorem completion is claimed.

## Dependency Audit

The required `stage1-dependency-reuse-ledger/1.1` ledger binds graph digest
`73e99d2276c8ba9fec8f89ed41b712308d7f5667e95ba8185e49f1f5bfd40eca`,
context digest
`9a63616961f13f69c93c4d36e46aa0c017d8122e6cec361cc666c795cd4eefc3`,
and this base revision. There are no hard parents, transitive hard ancestors,
hard edges, or reuse hints.

The sole shared group was inspected through its other member, `THM-M-1028`.
It co-mentions
`Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Basic`, but its
checked declarations concern conditional Wiener path packages and Gaussian
substrate. They neither construct law-bearing time/Ito integrals nor discharge
THM-M-1036 strong existence or pathwise uniqueness. The nonblocking group is
therefore `not_applicable` and transfers no proof credit.

## Failed Gates

The first workflow failure is the prerequisite
`S56-M-1036-OBLIGATION_TREE`, still `[_]` rather than master-accepted `[x]`.
The decisive mathematical failure is statement consistency at
`M1036-X-INTEGRAL-SEMANTICS`. The minimal root cut is that obligation, with
the open chain continuing through `M1036-T-EXISTENCE` to `M1036-ROOT`.

Replace the bare semantic flags with a source-faithful, law-bearing time/Ito
integral construction or exact sufficient laws. Then publish a new statement
fingerprint and freshly freeze and master-accept the invalidated prerequisites
before resuming proof work. An explicit redirect to the checked barrier target
is the other legal route.

## Validation

All checks ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink was reused read only. No `lake update`,
`lake build`, dependency clone/fetch, network command, or deliberate `.lake`
mutation occurred. Generated Lean output stayed under `/tmp` and was removed.

The statement check passed with all three mutations killed and fingerprint
`3717483261012dabe49b9787ad1336001262cbdf7791dfd1094c217298ac8954`.
The obligation-tree check passed structurally with 18 obligations, 47 typed
edges, denominator
`7e425556f1efaf61324a9d453d76aa833189110b116824aaf32c2f390b328e69`,
and the root honestly open at M3. The dependency ledger passed the repository's
exact schema/context/revision validator.

The isolated trust-zero `lake env lean` replay compiled copied `Statement.lean`
and `Counterexample.lean` successfully. Both negative declarations reported
axioms exactly `[propext, Classical.choice, Quot.sound]`. The combined kernel
output SHA-256 was
`4b11faa31e8ad2a6401448d63176322e46bf814ff423c23016d4c7bfea426a55`.
The scoped prohibited-token scan found no `sorry`, `admit`, axiom declaration,
unsafe/oracle escape, or `sorryAx`. A pinned-mathlib search found no general
stochastic-integral or SDE existence-and-uniqueness API.

The two global structural commands returned 1: deterministic graph
regeneration inventories the newly required ledger under
`THM-M-1036/evidence_inventory`, while the checked-in graph necessarily
predates this worker artifact. The blueprint states that the derived ledger is
excluded from theorem-DAG discovery; the generator excludes it from shared
dependency-context discovery but not from `evidence_inventory`. The worker did
not edit the authoritative DAG or generator, as required. This validation
failure is recorded rather than concealed.

## Status Boundary

This is durable blocker evidence, not a proof receipt. Because the assigned
proof phase is not genuinely self-tested complete,
`.stage1-worker-selftest.json` is deliberately absent.
