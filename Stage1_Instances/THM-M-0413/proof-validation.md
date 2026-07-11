# THM-M-0413 proof-phase validation

Item: `S56-M-0413-PROOF`  
Base revision: `081824d18f2e6414e9aad5a74d8ada82eaa1c9ea`

## Implemented bodies

`Proof.lean` supplies placeholder-free bodies for the four frozen mathematical components and two
exact-root certificates. `exactRoot` directly instantiates the pinned terminal theorem
`IsIntegralClosure.isDedekindDomain` at `Z`, `Q`, `K`, and the ring of integers.
`exactRootFromComponents` separately assembles the domain, Noetherian, dimension-at-most-one, and
integrally-closed witnesses with the `IsDedekindDomain` constructors. The integrally-closed body
spells out the fraction-ring and integrality-transitivity argument rather than invoking the final
Dedekind instance.

The upstream terminal body is pinned at mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; its exact source hash and wrapper hash are recorded in
`proof-receipt.json`. This closes the proof-phase mathematical interfaces, but it does not accept
human-source fidelity, readable reconstruction, transitive trust/provenance, hermetic validation,
or independent release. Audit and theorem completion therefore remain false.

## Commands and exact results

Commands ran in the worker clone on 2026-07-12. The existing canonical pinned `.lake` artifact was
reused; no update, build, clone, fetch, or `.lake` mutation was performed.

```text
$ (cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0413/Proof.lean)
exit 0
exactRoot and exactRootFromComponents have the exact quantified root type
all six printed declarations depend only on [propext, Classical.choice, Quot.sound]

$ python3 Docs/tools/check_stage1_standard.py
exit 0: 15 assurance groups and 1546 uniform-L0 targets passed

$ python3 scripts/stage1_target.py check
exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

$ python3 scripts/stage1_target.py show THM-M-0413
exit 0: rank 68, planned, L0/rework_required, theorem_complete false

$ python3 Stage1_Instances/THM-M-0413/validate_obligation_tree.py
exit 0: 10 obligations, 12 proof edges, acyclic root reachability, typed graphs, ledgers <=100

$ rg -n '\\b(sorry|admit|sorryAx)\\b|^[[:space:]]*(axiom|unsafe)[[:space:]]' \
    Stage1_Instances/THM-M-0413/Proof.lean
exit 1 with empty output: pass, no prohibited declaration or placeholder

$ python3 -m json.tool Stage1_Instances/THM-M-0413/proof-receipt.json >/dev/null
exit 0

$ git diff --check -- Stage1_Instances/THM-M-0413 .stage1-worker-selftest.json
exit 0 with no output
```

This is narrow proof-phase evidence pending master acceptance. Validation and release are separate
downstream nodes.
