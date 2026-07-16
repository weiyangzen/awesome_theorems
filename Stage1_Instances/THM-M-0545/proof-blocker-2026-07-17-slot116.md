# THM-M-0545 proof-phase blocker

## Verdict

`S56-M-0545-PROOF` is **blocked** at the exact frozen target. This artifact is
target-scoped negative evidence, not a proof of the mathematical Hodge
decomposition theorem and not a proof-phase completion claim.

The authoritative v2 dependency closure is empty. The refreshed
`dependency-reuse-ledger.json` binds graph SHA-256
`e8472863a24609e37868f215bbf0e0654b11a62f912a403ebca5feb8de5a3b9b`,
context SHA-256
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`,
and base revision `1cc6aa61bb055a5c032297ee457905c849af7608`.
There were zero parents to inspect and no provider material or acceptance was
consumed.

## Kernel evidence

Two target-owned, placeholder-free declarations independently refute the
universe-zero specialization of the frozen polymorphic target:

- `Stage1Instances.THMM0545.not_hodgeDecompositionTarget_degreeZero`
  proves that `IsExact D 0 e` is empty because it requires `j + 1 = 0`, while
  every `HasUniqueDecomposition 0 omega` requires an exact summand.
- `Stage1Instances.THMM0545.not_hodgeDecompositionTarget` uses scalar forms,
  zero exterior derivative and codifferential, and identity Laplacian. The
  nonzero degree-one form cannot be a sum of the forced-zero harmonic, exact,
  and coexact components.

Both declarations re-elaborated with `lake env lean --trust=0 -t0` in a fresh
temporary directory. Both report exactly `propext`, `Classical.choice`, and
`Quot.sound`; neither uses `sorry`, `axiom`, `unsafe`, an oracle, or a
placeholder. Their exact source and replay digests are bound in
`proof-receipt.json`.

## Failed gate

First failure: `P04-KERNEL/EXACT-TARGET-CONSISTENCY`.

The negative declarations close none of the fourteen positive machine
obligations. The root remains open, and the assigned positive proof predicate,
audit completion, validation, release, theorem completion, and master
acceptance remain false.

The validator candidate `check_proof.py` did not exist at the worker base. Its
bytes and the receipt must first be integrated; the scheduler then needs a
fresh current-HEAD implementation pass so unchanged-base authority replay can
select the HEAD-tracked validator.

After the required target-owned files were added, the structural standard and
theorem-DAG checks truthfully report deterministic evidence-inventory drift.
This worker may not regenerate the protected theorem DAG; the integration lane
must regenerate that projection when it copies these owned artifacts.

## Retry condition

Reopen `S56-M-0545-STATEMENT`; repair degree-zero exactness and replace the
unconstrained realization propositions with concrete pinned definitions or
source-justified noncircular law-bearing structures. After accepting a new
exact statement fingerprint, refreeze and rerun statement, anchor-audit,
obligation-tree, and proof phases in DAG order.
