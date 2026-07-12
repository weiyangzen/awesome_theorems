# THM-M-0985 validation-phase result

Item: `S56-M-0985-VALIDATION`  
Date: `2026-07-12`  
Base revision: `0b8b65976c8cabfaf26316eaee8539caba8f60d0`

The validation recipe re-elaborates the exact proof root and a second
same-checkout reconstruction which does not import `Proof.lean`. It binds the
proof inputs to their receipt hashes, checks the pinned mathlib revision and
clean source checkout, verifies the terminal source hash, and enforces the
observed Lean axiom and local placeholder/unsafe policies.

## Exact result

```text
python3 Stage1_Instances/THM-M-0985/check_validation.py
  exit 0
  PASS THM-M-0985 validation: exact proof root and independent reconstruction elaborate
  axioms: [propext, Classical.choice, Quot.sound]; placeholder/unsafe scan: pass
  provenance: mathlib 8a178386ffc0f5fef0b77738bb5449d50efeea95;
    StrongLaw.lean sha256 b74c93434df44eb75b2567f43a58b9e0353138660ad07b99263d8019bcf4f1c6
  FAIL-CLOSED hermetic release: shared warm .lake cache; no cold empty-cache
    offline replay or complete TCB/SBOM
  FAIL-CLOSED independent release: same checkout/runner; no distinct signed
    attestation or independent minimal verifier
```

The validator copies `Statement.lean`, `ObligationTree.lean`, `Proof.lean`, and
`Validation.lean` to a fresh temporary directory under the owned target path,
invokes narrowly scoped `lake env lean` checks, and removes the directory. The
pre-existing canonical pinned `.lake` symlink was reused without update,
build, clone, fetch, or dependency mutation. No network operation was used.

## Gate decisions

| Gate | Decision | Evidence or boundary |
|---|---|---|
| Exact-root kernel replay | pass | `Stage1Instances.THMM0985.Proof.kolmogorovStrongLaw` elaborates with the exact canonical type. |
| Same-checkout reconstruction | pass, nonrelease | `Validation.lean` reconstructs the exact root without importing `Proof.lean`. It is not a distinct runner. |
| Placeholder and unsafe scan | pass | No `sorry`, `admit`, local `axiom`, `sorryAx`, or `unsafe` declaration occurs in the checked modules. |
| Foundation observation | provisional pass | Both root declarations report exactly `propext`, `Classical.choice`, and `Quot.sound`; a release-grade complete TCB inventory is absent. |
| Local provenance | pass | Proof input hashes agree with the proof receipt; mathlib is clean at the manifest pin; terminal source hash agrees. |
| Hermetic release replay | fail closed | The run used shared warm compiled artifacts, not a clean checkout with empty caches, cold build, network-denied offline restoration, complete executable/olean inventory, and SBOM/licenses. |
| Independent verification | fail closed | One worker and mutable clone supplied no second signed attestation, independently provisioned runner, or independently implemented minimal verifier. |

The validation node is self-tested as a truthful gate report, pending master
acceptance. It establishes local exact-root kernel closure but grants no
release-grade `E0/E1`, `AUDIT-Z`, `THEOREM-Z`, theorem completion, or release.
The first failed release gate is rev-5.6 section 10.6 hermetic cold replay;
section 10.7 independent verification also fails. Human-source `H0`, readable
`R0`, full trust closure, release evidence, and master acceptance remain open.
