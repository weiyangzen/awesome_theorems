# THM-M-0406 proof-phase handoff

Item: `S56-M-0406-PROOF`

Base revision: `94009a6bebd743588e09c3b45bfbf18bf9b5c5e3`

## Verdict

`blocked`. The exact frozen Lean proposition has no consistent positive proof
body. The existing target-owned, placeholder-free declaration

```text
Stage1Instances.THMM0406.not_corvajaZannierTheoremOne :
  Not (CorvajaZannierTheoremOne.{0,0} (k := Rat))
```

replays at trust level zero. Its surface has four selected boundary components,
unit weights and intersection numbers, true geometric premises, one point, and
an empty curve type. Every frozen premise holds while the conclusion would
produce an inhabitant of `Empty`.

This refutes only the abstract transcription, not Corvaja--Zannier's
mathematical theorem. The source also quantifies all divisor pairs, including
diagonal pairs, whereas `HasTheoremOneBoundary` requires the intersection
equation only for distinct divisors.

## Dependency audit

The authoritative v2 node has no direct hard parent, transitive hard ancestor,
reuse hint, or shared lemma group. The required inspection order is therefore
the empty list. `dependency-reuse-ledger.json` binds that audited empty closure
to graph digest `eaee68bd...7153` and context digest `068170c7...5c5c`. No
provider body, receipt, checkbox state, or evidence credit was consumed.

## Validation boundary

`check_proof.py` verifies the open task identity, exact v2 claim tuple
`(258, 4, S56-M-0406-PROOF)`, empty reuse context, frozen input hashes, all
fourteen open obligations, prohibited-construct hygiene, pinned Lean/mathlib
closure, receipt bindings, and the trust-zero countermodel. It emits exactly
one `stage1-validator-semantic-result/1.0` object with `status=blocked`,
`phase_accepted=false`, and `theorem_complete=false`.

The validator candidate did not exist at this worker base. Consequently this
packet is not eligible for unchanged-base master replay until integration lands
the exact validator blob and allocates a fresh base-bound review. The required
repair is upstream: reopen and replace the false statement encoding, accept a
new fingerprint and obligation registry, rerun predecessor phases, and split
the repeatedly blocked proof work before another positive proof attempt.

Adding the receipt and validator also makes the checked-in theorem DAG's
derived evidence inventory stale. The post-write standard and DAG checks fail
on that expected deterministic difference; the worker contract forbids editing
the DAG, so regeneration belongs to integration.
