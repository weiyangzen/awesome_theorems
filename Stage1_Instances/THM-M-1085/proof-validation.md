# THM-M-1085 proof-phase validation

Item: `S56-M-1085-PROOF`. Base revision:
`3d3099d0d4002093cf89da97132bdf954605810b`.

## Implemented bodies

`LawReduction.lean` provides exact local bodies for finite-law normalization. The lower orthant is
proved measurable, and its probability, coordinate means, and coordinate covariances are
transported through the Gaussian vector's pushforward law. Coordinate Gaussianity, integrability,
and probability normalization are also derived from `HasGaussianLaw`.

The same module defines the coordinate covariance matrix, proves that it is the basis matrix of
the pushed-forward covariance bilinear form, and proves it positive semidefinite. It then identifies
each centered pushed-forward Euclidean law with `multivariateGaussian 0 covarianceMatrix`, covering
singular and repeated-coordinate laws. Finally, `slepianTarget_of_law` gives an exact checked bridge
from the remaining finite Gaussian-law comparison to the canonical target.

These bodies are substantive progress toward the planned normalization obligations
`M1085-N-LAWS` and `M1085-N-MATRIX`. Because those predecessor nodes still have prose-only planned
fingerprints and pending validation specifications, this worker claims no whole-node closure. The
accepted frozen registry is not edited; master integration must define exact node targets and
independently reconcile any later closure credit.

## Open boundary

`LawSlepianTarget` is a proposition, not an axiom and not a theorem claimed here. No inhabitant is
provided. The singular covariance interpolation, smoothing, derivative identity, mixed-derivative
sign, monotonicity, and lower-orthant indicator limit remain open. Consequently the canonical root
remains `M4`, the accepted closed-obligation set remains empty, and theorem completion is false.

## Commands and results

All commands reused the canonical pinned `.lake` symlink. No update, build, clone, fetch, or
dependency mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1085` | 0 | Rank 527, lifecycle `planned`, baseline `L0 / rework_required`, `theorem_complete: false`. |
| `python3 Stage1_Instances/THM-M-1085/check_obligation_tree.py` | 0 | Frozen 17-obligation, 65-edge registry passed; accepted root remained open at M4. |
| `bash Stage1_Instances/THM-M-1085/check_proof.sh` | 0 | Disposable `--trust=0` replay elaborated the exact statement and law-reduction module; twenty declarations were sorry-free and used only `propext`, `Classical.choice`, and `Quot.sound`; the exact statement mutation/hash validator and proof-evidence checker passed. |
| `rg -n '\b(sorry\|admit\|sorryAx\|implemented_by\|native_decide)\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe\|extern)[[:space:]]+' Stage1_Instances/THM-M-1085 --glob '*.lean'` | 1 | Expected no-match exit: no prohibited proof construct was found. |
| `python3 Stage1_Instances/THM-M-1085/check_proof.py` | 0 | Source hashes, frozen inputs, dependency pin, receipt, worker packet, changed paths, and open-root boundary agreed. |
| `python3 -m json.tool Stage1_Instances/THM-M-1085/proof-receipt.json` | 0 | Provisional node receipt is valid JSON. |
| `python3 -m json.tool .stage1-worker-selftest.json` | 0 | Worker handoff packet is valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-1085 .stage1-worker-selftest.json` | 0 | No scoped whitespace errors. |

The proof script discovers Lean and `LEAN_PATH` through `lake env`, copies only `Statement.lean` and
`LawReduction.lean` to `/tmp`, compiles with `LEAN_NUM_THREADS=1`, `--trust=0`, and `-t0`, parses
`#print sorries` and `#print axioms`, and deletes all temporary files on exit. The pre-existing
untracked `.lake` link is nonrelease automation state and was not modified.

`check_obligation_tree.py` was narrowed from a raw substring scan to the same comment-stripped
prohibited-declaration scan, so explanatory comments in proof modules do not break the predecessor
structural check while actual placeholders and axiom-like declarations still fail closed.

## Status boundary

This is self-tested partial proof-phase evidence only. It proposes `[_]` for the assigned phase but
does not claim an accepted state, root proof, validation/release result, audit completion, master
acceptance, or theorem completion.
