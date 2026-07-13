# THM-M-1237 proof-phase validation

Item: `S56-M-1237-PROOF`. Base revision:
`bb6fb28ac1c55ecb52f3f1c84e7fbb35c26b47ad`.

## Implemented body

`Proof.lean` closes the exact frozen construction obligation `M1237-C`.
`representativeFamily` chooses `u.function`, which agrees with itself everywhere and hence almost
everywhere. Lean checks the exact `RepresentativeFamily` type without a placeholder or added axiom.

The same module proves `not_valueEstimateFamily : Not ValueEstimateFamily`. The counterexample
uses dimension one, the singleton domain `{0}`, `p = 2`, `alpha = 1/2`, and zero Sobolev/extension
data. The spike that is one at zero and zero elsewhere agrees almost everywhere with the zero input
because volume restricted to a singleton is zero. Instantiating the frozen family with this
representative, `C = 0`, and `x = 0` forces `1 <= 0`.

This is a proof-architecture blocker, not a counterexample to the canonical existential root. The
root asks for one jointly selected representative and constant; the frozen value interface instead
quantifies over every representative and every constant. `HolderEstimateFamily` has the analogous
arbitrary-representative issue. The architecture must couple these outputs, or an exact direct root
proof must bypass it. The root remains `M3`; theorem completion is false.

## Validation record

Commands ran from the worker clone on 2026-07-14. Lean outputs were written only to a disposable
directory under `/tmp`, removed on exit. Existing pinned Lake artifacts were reused; no update,
build, clone, fetch, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `bash Stage1_Instances/THM-M-1237/check_proof.sh` | 0 | Statement, frozen composition, partial proof, and interface counterexample elaborated; both local declarations reported `[propext, Classical.choice, Quot.sound]` |
| `python3 Stage1_Instances/THM-M-1237/check_proof.py` | 0 | Exact hashes, registry denominator, proof surfaces, open-root boundary, and prohibited-device scan passed |
| `python3 Stage1_Instances/THM-M-1237/check_obligation_tree.py` | 0 | Frozen 10-obligation, 32-edge architecture still validates structurally; this does not negate the semantic counterexample |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | Ordered 1546-target manifest passed |
| `python3 scripts/stage1_target.py show THM-M-1237` | 0 | Rank 175, planned, L0/rework-required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1237/proof-phase.json` | 0 | Valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1237/proof-receipt.json` | 0 | Valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1237 .stage1-worker-selftest.json` | 0 | No whitespace errors |

First failed gate: `M1237-L-VALUE`. Remaining open root cut after the partial closure is
`M1237-L-HOLDER` and `M1237-L-VALUE`. Retry after the prerequisite architecture is repaired and
accepted, or after a placeholder-free exact direct root body becomes available. No validation,
release, master-acceptance, or theorem-completion claim is made.
