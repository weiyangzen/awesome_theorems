# THM-M-0819 proof-phase validation

Item: `S56-M-0819-PROOF`. Base revision:
`7505614b75de56cf10bbd196a4aaa0ca2a117064`.

## Implemented proof

`Proof.lean` now declares
`Stage1Instances.THM_M_0819_Proof.dilworthPrimary : DilworthPrimaryTarget`, the exact frozen
arbitrary-poset finite-width statement. The implementation does not specialize the carrier to a
finite type and does not substitute the modern finite-poset equality for the root.

The finite core is an Apache-2.0 current-pin port of Vlad Tsyrklevich's immutable
`vlad902/misc-lean-proofs@f82f920f05a381bb1ce5e8903bde33e27f4365b6` source. The upstream
source hash is `4bc86897588087f472b358830bba157b92994e2b0dd44c66805f57c29211c985`.
The upstream Apache-2.0 `LICENSE` is included byte-for-byte at SHA-256
`c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4`. The full Lean source
delta is 26 insertions and 5 deletions, comprising a 9-line prominent port notice plus 17 proof-port
insertions: one `IsChain.image` API migration and one repair
of a dependent rewrite whose old `simp` invocation no longer progresses. The port elaborates under
the repository pin without recovery holes.

For the arbitrary carrier, the proof fixes the attained exact-`k` antichain. Each finite test set is
enlarged by that antichain, the finite theorem supplies an exact `Fin k` coloring, and pinned
`Set.Finite.rado_selection_subtype` stitches the local colorings into a global one. Agreement on a
two-point set proves each color fiber is a chain; equality to the element's own color proves unique
membership. The checked statement lemmas discharge `k = 0`.

This is a provisional `M0-L` machine-proof proposal for all 23 frozen required-machine obligations.
The frozen registry and graphs retain their pre-proof snapshot. Only the integration lane may accept
the proposal or update authoritative state.

## Commands and results

The following commands ran in the worker clone on 2026-07-15. No `lake update`, `lake build`,
dependency clone/fetch, network action, or `.lake` mutation was performed.

```text
bash Stage1_Instances/THM-M-0819/check_proof.sh
  exit 0: fresh isolated Statement, finite proof, and exact root compilation passed with
  --trust=0; root was sorry-free and reported [propext, Classical.choice, Quot.sound]

python3 -B Stage1_Instances/THM-M-0819/check_proof.py
  exit 0: exact target, frozen denominator and hashes, source/provenance markers,
  provisional receipt, pinned mathlib identity, and prohibited constructs passed

python3 -B Stage1_Instances/THM-M-0819/check_obligation_tree.py
  exit 1: historical checker hardcodes its original obligation-tree worker HEAD
  dc600635160cace0916df5234bf8808c39dc656d and exits before content validation at the current
  proof base; the frozen input hashes and denominator are checked independently by check_proof.py

python3 Docs/tools/check_stage1_standard.py
  exit 0: rev-5.6 structural standard passed

python3 scripts/stage1_target.py check
  exit 0: target manifest structural check passed

python3 scripts/stage1_target.py show THM-M-0819
  exit 0: rank 1377, L0/rework-required, planned, theorem_complete=false

rg prohibited proof escapes over FiniteDilworth.lean and Proof.lean
  exit 1 with empty output: expected pass; no prohibited construct found

python3 -m json.tool Stage1_Instances/THM-M-0819/proof-receipt.json
  exit 0: valid JSON

git diff --check -- Stage1_Instances/THM-M-0819 .stage1-worker-selftest.json
  exit 0: no scoped whitespace errors
```

The root proof source SHA-256 is
`c64e830b6c1a8770319bdaf9549dcd0a8a557da6710272c127560a931da8cd22`; the ported finite
source SHA-256 is `825275407850c60f8fe1417a2cee408fb262b60f26eaa9ab30662ea46829e2c1`.

Accepted state remains `[H1, M3, R3]` until dependency-ordered master acceptance. Human-source H0,
independently accepted R0, complete provenance and trust review, cold hermetic replay, independent
verification, validation, release, `AUDIT-Z`, `THEOREM-Z`, and theorem completion remain open.
