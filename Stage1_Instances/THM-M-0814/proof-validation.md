# THM-M-0814 proof-phase validation

Item: `S56-M-0814-PROOF`. Base revision:
`b62c08f262435e44a30ad3fc88a4712e3954afc7`.

## Implemented bodies

`Proof.lean` proves the exact frozen `WeakDuality` interface. For each supported chain it chooses
one arc supplied by the disconnecting-set premise, bounds that component by its sum over all cut
arcs used by the chain, commutes the finite chain and arc sums, identifies each inner sum with
`arcLoad`, and applies feasibility. The proof permits multiple crossings and therefore does not
silently strengthen the disconnecting-set definition to an exactly-once property.

The same module proves the exact no-chain branch with zero flow and the empty disconnecting set.
It also composes local weak duality into the conditional cut certificate and exact root spine. The
resulting root theorem retains only `MaximalFlowAttainment` and `EqualCutForMaximalFlow` as explicit
universal premises. `noChain_case` is not yet connected to that root by a checked case-split
interface. Both universal products therefore remain open, so the root remains open and
`theorem_complete=false`.

This packet provisionally proposes closure of `M0814-L-WEAK-DUALITY`. The no-chain theorem is
substantive partial progress toward `M0814-B-NO-CHAIN`, whose frozen target remains a prose-only
planned interface; it receives no closure claim until the integration lane reconciles an exact
type. The frozen registry and typed graphs retain their pre-proof open snapshot, and only the
integration lane may accept proof evidence or update authoritative state.

## Commands and results

Validation ran in the worker clone on 2026-07-15. It reused only the existing canonical pinned
`.lake` artifacts; no update, build, dependency clone/fetch, network operation, or `.lake` mutation
was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and all 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1 through 1546, all L0/rework-required

python3 scripts/stage1_target.py show THM-M-0814
  exit 0: rank 1373, lifecycle planned, L0/rework-required, theorem_complete=false

bash Stage1_Instances/THM-M-0814/check_proof.sh
  exit 0: fresh isolated Statement, ObligationTree, and Proof compilation passed with
  --trust=0; all four proof declarations reported exactly
  [propext, Classical.choice, Quot.sound]

python3 -B Stage1_Instances/THM-M-0814/check_proof.py
  exit 0: proof scope, exact target, frozen hashes, pins, receipt, blocker, packet, and
  open-root boundary passed

python3 -B Stage1_Instances/THM-M-0814/check_obligation_tree.py
  exit 1 at the historical base-revision assertion: the immutable predecessor validator remains
  bound to its own obligation-tree worker commit, while this proof worker is based on its later
  integration commit. Its generated artifacts and frozen hashes are independently checked by
  check_proof.py; no proof-phase claim relies on overriding that fail-closed historical assertion.

rg -n -i --glob '*.lean' '\b(sorry|admit|sorryAx)\b|^[[:space:]]*(axiom|constant|opaque|unsafe)[[:space:]]|implemented_by|native_decide|extern[[:space:]]' \
  Stage1_Instances/THM-M-0814/Proof.lean
  exit 1 with empty output: expected pass; no prohibited construct found

python3 -m json.tool Stage1_Instances/THM-M-0814/proof-receipt.json
python3 -m json.tool Stage1_Instances/THM-M-0814/proof-blocker.json
python3 -m json.tool .stage1-worker-selftest.json
  each exit 0: valid JSON

git diff --check -- Stage1_Instances/THM-M-0814 .stage1-worker-selftest.json
  exit 0: no scoped whitespace errors
```

The proof source SHA-256 is
`b7f4d1e28d4e9add0ca9f21943bb104b1dd450106a217b9b8298013afe250e76`.
Lean is version 4.29.0 at commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, and mathlib is
pinned at `8a178386ffc0f5fef0b77738bb5449d50efeea95`.

Accepted state remains `[H1, M3, R4]`. Maximum-flow attainment, the equal-cut source construction,
source H0, readable R0, complete provenance and trust, cold hermetic replay, independent
verification, validation, release, `AUDIT-Z`, `THEOREM-Z`, and theorem completion remain open.
