# THM-M-1537 proof recheck at `499a718c`

Item: `S56-M-1537-PROOF`

Intent: `prove`

Verdict: `blocked`

Worker state proposed: `[ ]` (no transition)

Base revision: `499a718cc7926abaf61e9721fe0d7485059403e6`

Base tree: `ed2a23c0266f4d921ad97562392226015eee80be`

## Exact target

The frozen target is
`Stage1Instances.THM_M_1537.BekensteinHawkingAreaLaw`. It universally quantifies
over a `SemiclassicalBlackHole` and concludes

```text
B.thermodynamicEntropy = entropyFromArea B
```

from the three regime propositions, nonnegative horizon area, and positive
physical constants. None of those premises constrains the independent
`thermodynamicEntropy` field.

## Kernel obstruction

`ObligationTree.lean` defines
`Stage1Instances.THM_M_1537.independentEntropyCountermodel` with horizon area
zero, entropy one, all four constants equal to one, and all three regime
propositions true. The placeholder-free theorem

```text
Stage1Instances.THM_M_1537.not_bekensteinHawkingAreaLaw :
  Not Stage1Instances.THM_M_1537.BekensteinHawkingAreaLaw
```

applies any proposed law to that admissible record and derives the false
equality `1 = 0`. A direct trust-zero replay through the pinned Lean 4 binary
elaborated both the exact statement and this refutation. The declarations
`areaLaw_of_bridge` and `not_bekensteinHawkingAreaLaw` reported only
`propext`, `Classical.choice`, and `Quot.sound`.

Therefore no consistent proof body, exact pinned import, or valid wrapper can
close the frozen positive target. `areaLaw_of_bridge` is conditional on
`AreaLawBridge`, which is definitionally the same refuted universal equality.
The historical `S1_M_200` file likewise stores or assumes an area-law boundary
and proves consequences; it does not derive this unconstrained root.

## Validation

The accepted narrow replay invoked the pinned Lean binary directly with an
explicit `LEAN_PATH` over already-built canonical package artifacts. It did
not invoke Lake dependency resolution, update, build, clone, fetch, or network
access. Its exact output hashes are recorded in the paired JSON artifact.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups, 1546 targets, and execution-skill checks passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 ordered targets passed the uniform L0/rework-required check. |
| `python3 scripts/stage1_target.py show THM-M-1537` | 0 | Rank 200; lifecycle `planned`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1537/check_statement.py` | 1 | The initial run found that the automation-provided shared `flt-regular` checkout had no resolvable `HEAD`; a later retry was stopped after more than 30 seconds in Lake dependency handling. No dependency repair or fetch was attempted. |
| `python3 Stage1_Instances/THM-M-1537/check_anchor_audit.py` | 0 | Exact statement, six pinned mathlib probes, partial Physlib candidate, and `M4` audit boundary agree. |
| `python3 Stage1_Instances/THM-M-1537/check_obligation_tree.py` | 0 | Nine obligations and 16 typed edges passed; root remains refuted at `M5`. |
| direct pinned `lean --trust=0 -t0` replay | 0 | Exact statement, conditional composition, and countermodel refutation elaborated. |
| prohibited-construct `rg` scan | 1 | Expected no-match exit; no `sorry`, `admit`, axiom declaration, unsafe injection, or native-decide shortcut was found. |
| pinned `lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`. |

The statement validator's Lake failure is a validation limitation, not the
mathematical blocker and not permission to mutate `.lake`. The direct replay
uses the same pinned Lean and already-built mathlib artifacts, avoids the
unrelated incomplete checkout, and independently reproduces the prior hashes:

```text
Statement.olean  21763c76f8db541140516a7e0e4a158bdadd228e85a254c17fe5d35e710c4224
statement output ff89d33cc918db629fe730ab7c1a2e5b507b7373f6446a98bf776a2cc07661fb
obligation output a3249e7c677d02614229aef9780b2e1266026bf5fc7f233d1b025808cb2e802b
```

## Gate decision

The first failed proof gate is `M1537-B-PHYSICS`: exact-target consistency.
The minimal remaining root cut is the same obligation. The prerequisite
`S56-M-1537-OBLIGATION_TREE` is also only worker-provisional `[_]`, not
master-accepted `[x]`.

Positive proof work may resume only after an authorized upstream statement or
model repair genuinely relates thermodynamic entropy to horizon area. That
repair must pass new statement, anchor-audit, and obligation-tree gates before
the proof phase is retried. Adding the area law as a structure field or axiom,
assuming `AreaLawBridge`, weakening the target, or proving a substituted
theorem would not satisfy this item.

No `.stage1-worker-selftest.json` is written because the requested positive
proof phase is not genuinely complete. This packet is fresh nonrelease blocker
evidence only; it is not a proof receipt, scheduler transition, audit or theorem
completion claim, release decision, or master acceptance.
