# THM-M-0417 validation-phase result

Item: `S56-M-0417-VALIDATION`

Base revision: `c45f3c7090cb4adf616d45e5414985f956e807b2`

The exact strict Minkowski root, frozen child composition, proof-phase module, and a separately
written exact wrapper elaborate against the pinned Lean 4.29.0/mathlib snapshot. The checker binds
the frozen inputs, rejects prohibited local and terminal constructs, verifies clean dependency pins,
and compares each root-relevant axiom report exactly with the three previously recorded baseline
axioms. This is narrow worker evidence, not acceptance of the still-uninstantiated foundation/TCB
profile.

## Exact validation

The structured recipe in `validation-spec.json` ran from repository root on 2026-07-13 UTC. It
copied the four Lean modules into a fresh temporary directory, invoked only `lake env lean`, and
removed the directory. The pre-existing canonical pinned `.lake` symlink was reused; no `lake
update`, `lake build`, dependency clone/fetch, network operation, or intentional `.lake` mutation
was performed. The final recorded replay ran from `17:14:40Z` through `17:17:53Z`.

```text
$ python3 Stage1_Instances/THM-M-0417/check_validation.py
exit 0
PASS narrow kernel replay: exact root, composition, proof, and separate reconstruction elaborated
PASS axiom observation: checked declarations report exactly the three recorded baseline axioms
PASS local provenance: frozen hashes, clean pinned mathlib, toolchain, and terminal source agree
OPEN source/trust boundaries: foundation approval, H0/R0 review, and transitive TCB closure are absent
BLOCKED release gates: warm shared .lake and no distinct independently provisioned verifier
```

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact kernel root | provisional pass | Direct pinned wrapper, local three-child reconstruction, and both transports to the frozen `Statement` elaborate. |
| Child composition | provisional pass | `root_compose` consumes the three frozen mathematical interfaces and yields the exact root. |
| Separate local probe | provisional pass | `Validation.independentMinkowskiConvexBody` imports only `Statement` and applies the pinned terminal declaration; it shares the terminal body and is not independent release evidence. |
| Placeholder and unsafe scan | pass | Four local modules and the pinned terminal body contain no `sorry`, `admit`, `sorryAx`, `native_decide`, local `axiom`, `unsafe`, or `external` escape. |
| Axiom observation | provisional pass | Parsed reports are exactly `propext`, `Classical.choice`, and `Quot.sound`; the instance foundation profile is not instantiated or accepted. |
| Local provenance | pass | Frozen input hashes, clean mathlib revision `8a178386...`, terminal source/blob/olean identity, toolchain, and manifest agree. |
| Full trust/provenance | fail closed | No complete transitive declaration/import closure, approved foundation profile, executable TCB/bootstrap inventory, SBOM, or license archive exists. |
| Human source/readability | fail closed | `M0417-X-SOURCE` remains H1 and there is no independently reviewed R0 reconstruction. |
| Structured freshness | fail closed | The obligation-tree graph and intake/public surfaces predate proof/validation and still describe pending or M3/open state; reconciliation is master-owned. |
| Hermetic release replay | fail closed | The run reused warm shared `.lake`; there was no clean checkout, empty caches, cold build, or offline archive restoration. |
| Independent verification | fail closed | One mutable worker and shared cache cannot supply distinct signed identities, an independently provisioned runner, or the required independent minimal verifier. |

## Boundary

This validation node is genuinely self-tested and has a provisional receipt. Seven mathematical
machine obligations have narrow local evidence, while `M0417-X-SOURCE` and `M0417-X-TRUST` remain
open. The receipt grants no accepted `E0/E1`, `M0-W`, `H0`, `R0`, `AUDIT-Z`, `THEOREM-Z`, release,
or master-acceptance credit. `audit_complete=false` and `theorem_complete=false`.
