# THM-M-0168 proof-phase validation

Item: `S56-M-0168-PROOF`. Base revision:
`dc0f0264c1db312ac95025747d3212b689facb5e`.

## Implemented Body

`Proof.lean` supplies a genuine placeholder-free proof of the frozen
`M0168-T-INTEGRATE` bridge. Given a `C2` function whose two Frechet coordinate
derivatives are constant, `constantPartials_to_affine` reconstructs the whole
Frechet derivative from the coordinate basis, compares it with the explicit
affine model, and applies mathlib's connected-domain derivative theorem. The
declaration `constantPartialsToAffine_proof` exactly inhabits the frozen
`ConstantPartialsToAffine` package.

The file now also checks the definitional equivalence between the duplicated
obligation-harness target and the canonical statement target. The theorem
`canonical_bernstein_of_derivativeRigidity` composes into the canonical target,
but it still consumes `DerivativeRigidity` as an explicit premise. It therefore
receives composition evidence only, not root-closure credit.

## Open Boundary

The exact Bernstein theorem has no premise-free proof body in this repository
or pinned dependency closure. The first unavailable package is
`M0168-C-GRAPH`; graph geometry, PDE-to-minimality, stability, logarithmic
cutoff, curvature vanishing, and derivative rigidity remain open. The
remaining root cut is:

- `M0168-C-GRAPH`
- `M0168-N-PDE-MINIMAL`
- `M0168-L-STABILITY`
- `M0168-C-CUTOFF`
- `M0168-L-CURVATURE`
- `M0168-L-DERIVATIVE-RIGIDITY`

The root remains open at `M2`. The root vector stays `[H1, M2, R3]`, and
`audit_complete=false` and `theorem_complete=false`.

## Commands And Results

All commands ran in this worker clone on 2026-07-15 (`Asia/Shanghai`). No
`lake update`, `lake build`, dependency clone/fetch, network request, or `.lake`
mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 unique targets and ranks passed. |
| `python3 scripts/stage1_target.py show THM-M-0168` | 0 | Rank 665; planned; hard-statement-first partial-verification lane; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0168/check_obligation_tree.py` | 0 | Eleven nodes and the typed acyclic proof graph passed; the frozen root remains open. |
| `python3 Stage1_Instances/THM-M-0168/check_statement.py` | 1 | The top-level Lake environment rejected the shared `flt-regular` checkout because it has no resolvable `HEAD`; no repair or fetch was attempted. |
| `bash Stage1_Instances/THM-M-0168/check_proof.sh` | 0 | Disposable `--trust=0` compilation checked Statement, ObligationTree, the affine-integration body, the exact package wrapper, definitional canonical transport, and conditional canonical-root composition. Every axiom report was exactly `propext`, `Classical.choice`, and `Quot.sound`; the source hygiene scan passed. |
| `python3 Stage1_Instances/THM-M-0168/check_proof.py` | 0 | Target/DAG identity, source and pin hashes, frozen child fingerprint, open-root boundary, receipt, packet, and changed paths agreed. |
| `python3 -m json.tool Stage1_Instances/THM-M-0168/proof-receipt.json` | 0 | The provisional node receipt is valid JSON. |
| `python3 -m json.tool .stage1-worker-selftest.json` | 0 | The worker handoff packet is valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-0168 .stage1-worker-selftest.json` | 0 | No scoped whitespace errors. |

The proof checker selects Lean with `lake env` from the manifest-pinned mathlib
checkout at `8a178386ffc0f5fef0b77738bb5449d50efeea95`, then constructs `LEAN_PATH`
only from existing compiled pinned artifacts. It copies the three Lean sources
to `/tmp`, compiles fresh oleans with `LEAN_NUM_THREADS=1`, `--trust=0`, `-t0`,
and bounded timeouts, parses each axiom report, and removes the disposable
directory. This is warm-cache nonrelease evidence, not an empty-cache replay.

## Status Boundary

This self-test proposes `[_]` only for the proof-phase worker contribution and
provisional closure of `M0168-T-INTEGRATE`. Accepted state remains unchanged
until integration-lane review. This is not a premise-free proof of the root,
validation, independent verification, release, audit completion, or theorem
completion.
