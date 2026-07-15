# THM-M-0424 proof recheck at `6bf9ee93` (slot 9)

Item: `S56-M-0424-PROOF`

Intent: `prove`

Recorded at: `2026-07-16T05:00:00+08:00`

Base revision: `6bf9ee93a322e7d25cf9249226222095f95d1cff`

Base tree: `24acf86e69ab2e6fca9480c6269b6429874ba295`

## Verdict

`blocked`. No positive proof body can inhabit the exact frozen target.

The target-owned, placeholder-free declaration

```text
Stage1Instances.THM_M_0424.UniverseCounterexample.not_brauerGroupStatement :
  Not Stage1Instances.THM_M_0424.BrauerGroupStatement.{1,0}
```

was replayed at Lean trust level zero against this base. A positive
universe-polymorphic proof would specialize to `{1,0}` and contradict this
kernel-checked theorem.

At that specialization, `K := Type 0 : Type 1` admits a field structure by
`Infinite.nonempty_field`. Any `BrauerGroupLawData.{1,0} K` contains a
`oneRep : CSA.{1,0} K` and an algebra equivalence from its `Type 0` carrier to
`K`. The underlying equivalence would make `Type 0` small in `Type 0`,
contradicting `not_small_type`. This refutes only the frozen Lean encoding, not
the classical Brauer-group theorem.

The mandatory v2 dependency context was audited before proof work. The target
has no hard parents, transitive hard ancestors, hard edges, or reuse hints. Its
three shared-module groups were inspected through actual member targets
`THM-M-0039`, `THM-M-0037`, and `THM-M-0038`. Each member has only provisional
intake evidence and proof state `[ ]`; none supplies a reusable terminal body.
The resulting schema-1.1 ledger is
`Stage1_Instances/THM-M-0424/dependency-reuse-ledger.json`, bound to graph SHA
`73e99d2276c8ba9fec8f89ed41b712308d7f5667e95ba8185e49f1f5bfd40eca`
and context SHA
`f6c5258e1d42d3812d7d616b9a9135ed71401872573195920e5bf8aa56d99683`.

There is also an independent downstream gap. Pinned
`Mathlib.Algebra.BrauerGroup.Defs` explicitly leaves the tensor-product
abelian-group construction as a TODO, and the pinned closure has no
`CommGroup (BrauerGroup K)` instance or forward tensor-product CSA theorem.
The legacy `AwesomeTheorems.Stage1.S1_M_078` module contains conditional data
interfaces only, not an inhabitant of the exact target.

Exact-target consistency first fails at
`S56-5.1-EXACT-TARGET-CONSISTENCY / M0424-S-BOUNDARY`, witnessed through
`M0424-C-ONE`. Repair requires reopening the statement phase, relating the
field and representative universes or adding a sufficient size boundary, then
publishing a new expression fingerprint and refreezing every dependent
artifact. The repaired target would still need real tensor-product and group
law bodies.

No positive proof body or receipt was added. Lifecycle remains `planned`, the
accepted root vector remains `[H1,M3,R3]`, proof remains `[ ]`, and theorem
completion remains false. The evidence supports a proposed machine diagnosis
of `M5`, but this proof worker does not own the statement, registry, or task
state and cannot accept that transition. The direct prerequisite
`S56-M-0424-OBLIGATION_TREE` is provisional `[_]`. This is the fifty-seventh
documented unresolved proof retry, far beyond the five-tick split threshold.
Because the phase is not complete, `.stage1-worker-selftest.json` is absent.

## Scoped validation

All checks ran in this worker clone using the automation-provided `.lake`
symlink read-only. Lean outputs were isolated in `/tmp` and removed. No
`lake update`, `lake build`, dependency clone/fetch, network request, or
`.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard, target manifest, and all 1546 uniform-L0 targets passed before the derived ledger was written. A later replay correctly reported that the generated evidence inventory now differs because the required ledger is a new target-owned artifact; only the master may regenerate the authoritative DAG. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 theorems, 10822 legacy states, 2 hard edges, 5 hints, 310 groups, and acyclicity passed before the derived ledger was written. Post-artifact replay reaches the expected master-owned inventory-regeneration boundary without changing the stable dependency context. |
| Post-artifact replay of the two commands above | 1 | Expected integration boundary: `checked-in theorem DAG differs from a fresh deterministic generation` because the new ledger and blocker JSON enter the target evidence inventory. The worker did not edit the master-owned DAG. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ranks at the uniform L0/rework-required baseline. |
| `python3 scripts/stage1_target.py show THM-M-0424` | 0 | Rank 78, lifecycle planned, theorem incomplete. |
| `validate_dependency_reuse_ledger(...)` with exact graph and base revision | 0 | Schema `stage1-dependency-reuse-ledger/1.1`, zero hard-parent inspections, and all three shared-group decisions passed. |
| Isolated `lake env lean --trust=0 -t0` replay of `Statement.lean` and `UniverseCounterexample-2026-07-14-head-5753c6ed.lean` | 0 | Exact target refuted at `{1,0}`; all `assert_no_sorry` checks passed; axioms were exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| `python3 Stage1_Instances/THM-M-0424/check_obligation_tree.py` | 0 | 18 obligations, 35 typed edges, denominator `83afccaebaea7322e89808dde65a4cff0cd758498ff63f70fbf8b00cf1e42a00`; root remains open M3. |
| Prohibited-construct scan of target-owned Lean sources | 1 | Expected no-match: no `sorry`, `admit`, `sorryAx`, declared axiom/bodyless constant, unsafe/external injection, `native_decide`, or `implemented_by`. |
| Search for `CommGroup (BrauerGroup ...)` in the pinned closure | 1 | Expected no-match. |
| `git diff --check -- Stage1_Instances/THM-M-0424` | 0 | No whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion handoff deliberately absent. |

The isolated Lean replay reproduced these SHA-256 values:

```text
Statement output:       efa2ea0ea05ce852276dd67e3abe1c6f3c705670f8c435bebcf57be1456b4e51
Statement olean:        3cf07b674053f73ba89b4b05c86e12c87cece6b588f3ee71ff389db747a1c2c2
Counterexample output:  c309037999d6b2be51e46f3e5a1e3ce8f67255764f213671c71f0df4696e8dcb
Counterexample olean:   73972a794d9812a5d5398ecf4b35ab924352e1d526e1a8d77ebca72bdd5177a2
```

Status boundary: this is current-base, nonrelease blocker evidence. It does
not satisfy `S56-M-0424-PROOF`, propose `[_]`, close the root, complete the
audit or theorem, validate a release, or claim master acceptance.
