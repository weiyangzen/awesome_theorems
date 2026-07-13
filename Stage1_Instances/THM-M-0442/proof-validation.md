# THM-M-0442 proof-phase recheck

Item: `S56-M-0442-PROOF`

Date: `2026-07-14` (`Asia/Shanghai`)

Base revision: `4990a9d6fa09beb7747e6822c6543c6123ca7504`

Base tree: `b74497bc09c004757aa3974f3bb0622d77e20106`

## Verdict

`blocked`, with revalidated supporting proof bodies. `Proof.lean` contains five
genuine, placeholder-free declarations. They prove the elementary order bounds,
transport the cardinality of the two allowed finite group shapes, and compose
these facts into

```text
MazurRationalTorsionTarget -> TorsionBoundAtMostSixteen.
```

This is only a consequence of the requested classification. It does not prove
the converse, inhabit any field of `ObligationTree.MazurEngine`, or close any
frozen obligation. The canonical root remains `[H1, M4, R4]`, with
`root_closed=false`, `audit_complete=false`, and `theorem_complete=false`.

The first unavailable deep package is `M0442-M-MODULI`: the pinned closure has
no compactified modular-curve/moduli-map body capable of connecting rational
torsion structures to the required rational-point classifications. The group
structure, cyclic and bicyclic restrictions, rational-point classification,
arithmetic exclusions, primary-source crosswalk, and trust/replay boundaries
also remain open. The external FLT `Mazur_statement` is both weaker and an
axiom, so importing or using it would not close the target.

The worker packet proposes only proof-phase state `[_]` for this replayed
partial execution. That state means the supporting implementation and its
self-test are ready for integration review; it does not mean a frozen
obligation, accepted state, the exact root, or theorem completion is closed.

## Validation

All commands ran in this worker clone using the existing canonical pinned Lake
artifacts. Temporary `.olean` files were written only below `/tmp` and removed.
No `lake update`, `lake build`, dependency clone/fetch, network access, or
`.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0442` | 0 | Rank 88; planned lifecycle; hard-mathlib-anchor lane; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0442/check_obligation_tree.py` | 0 | `PASS THM-M-0442 obligation freeze: 21 obligations, 20 proof edges; root open`. |
| `python3 Stage1_Instances/THM-M-0442/check_proof.py` | 0 | Isolated trust-zero replay of `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` passed; five supporting bodies and conditional `engine_compose` used only `propext`, `Classical.choice`, and `Quot.sound`; zero frozen obligations were claimed closed. |
| `rg -n '\b(sorry\|admit\|sorryAx\|native_decide\|implemented_by\|extern)\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0442 --glob '*.lean'` | 1 | Expected no-match exit; no prohibited proof device occurs in the owned Lean sources. |
| `python3 -m json.tool Stage1_Instances/THM-M-0442/proof-blocker.json >/dev/null` | 0 | Structured blocker record parsed. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git diff --check -- Stage1_Instances/THM-M-0442 .stage1-worker-selftest.json` | 0 | No whitespace errors. |
| `python3 -m json.tool .stage1-worker-selftest.json >/dev/null` | 0 | The provisional worker handoff parsed and retains every root-closure claim as false. |

The isolated replay performed by `check_proof.py` copies the three Lean modules
to a disposable directory, then invokes the pinned Lean binary with
`--trust=0 -t0`, an explicit existing `LEAN_PATH`, and a 300-second timeout per
module. It binds the exact source hashes, current base commit/tree, canonical
expression fingerprint, execution item, frozen cut set, dependency pins,
axiom output, and blocker boundary.

## Retry Condition

Resume after a frozen open obligation is implemented locally without
placeholders, or after an immutable compatible exact or stronger Lean 4 body
is available for pinned integration. Any such attempt must recheck exact type,
child-to-parent composition, terminal proof provenance, axioms, and the full
remaining cut before claiming progress toward the canonical root.
