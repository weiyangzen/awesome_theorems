# THM-M-1061 proof-phase validation

Item: `S56-M-1061-PROOF`  
Theorem: `THM-M-1061`  
Base revision: `557b928b377b386864527c9fb4831d45857837aa`
Run date: `2026-07-15`

## Implemented bodies

`Proof.lean` now contains nine additional placeholder-free local theorem
bodies. Four project the exact closed/open LDP and lower-semicontinuity/compact
sublevel interfaces. Three prove, rather than assume, the pointwise estimate

```text
-B <= LogExpIntegral mu a F n <= B
```

from probability, positive speed, and `|F| <= B`. The final two prove the
generic EReal liminf/limsup convergence step and its exact specialization to
the frozen `LogExpIntegral` sequence and variational supremum.

These bodies are exact ingredients or conditional composition. They do not
implement the LDP lower localization, compact finite cover, compact-core
integral estimate, bounded tail estimate, analytic lower/upper terminals, or a
premise-free proof of `VaradhanIntegralLemmaTarget`. Therefore this packet
claims zero whole frozen obligations closed, leaves the root at M3, and does
not claim theorem completion.

## Exact commands and results

Commands ran inside this worker clone. The pre-existing canonical pinned
`.lake` symlink was reused read-only; no update, build, dependency clone/fetch,
or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1061` | 0 | rank 504, lifecycle `planned`, theorem incomplete |
| `python3 Stage1_Instances/THM-M-1061/check_obligation_tree.py` | 0 | frozen 15-obligation registry and 49 typed edges pass; predecessor snapshot leaves root M3/open |
| `bash Stage1_Instances/THM-M-1061/check_proof.sh` | 0 | concatenated exact statement plus proof elaborates with `lake env lean --trust=0`; all nine new declarations report exactly `propext`, `Classical.choice`, and `Quot.sound` |
| `python3 Stage1_Instances/THM-M-1061/check_proof.py` | 0 | scope, pins, hashes, frozen premises, receipt/blocker boundaries, placeholder policy, and a fresh Lean replay pass |
| `python3 -m json.tool Stage1_Instances/THM-M-1061/proof-receipt.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1061/proof-blocker.json` | 0 | valid JSON |
| prohibited-device scan enforced by `check_proof.py` | 0 | no executable `sorry`, `admit`, `sorryAx`, bodyless axiom/constant, `unsafe`, `opaque`, `extern`, `implemented_by`, or `native_decide` |
| `git diff --check -- Stage1_Instances/THM-M-1061 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## First failed gate

The first open machine gate is still `M1061-L-LOWER-LOCAL`: the exact open-set
LDP projection now has a checked body, but the proof relating a localized
exponential integral to the measure of an open neighborhood is absent. The
compact-cover/core, tail, analytic lower, and analytic upper bodies also remain
open. The conditional limit merge cannot close while those premises are open.

The prerequisite anchor audit found no exact terminal Varadhan or Laplace
principle theorem in pinned mathlib or the audited immutable external sources.
Retry therefore requires local implementations of those analytic blocks, or
an immutable compatible Lean 4 terminal declaration that can be pinned,
exact-type transported, and checked in this dependency closure.

Status boundary: self-tested partial proof progress only. This is not master
acceptance, validation/release evidence, root M0, `AUDIT-Z`, `THEOREM-Z`, or
theorem completion.
