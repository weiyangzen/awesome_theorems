# THM-M-1255 proof-phase validation

Item: `S56-M-1255-PROOF`

Base revision: `915698958f008ab3454659b876ec7da319a5a0e5`

Validation time: `2026-07-14T03:07:09+08:00`

## Implemented bodies

`Proof.lean` closes the exact frozen `M1255-L-COMMUTE` obligation by expressing coordinate
distributional derivatives as Fourier multipliers and using commutativity of the scalar multiplier
symbols. It then closes `M1255-C-ACTION`: commuting coordinate powers are assembled with
`MonoidHom.noncommPiCoprod`, lifted through the finitely supported exponent monoid with
`AddMonoidAlgebra.lift`, and packaged as the required `PolynomialActionPackage`. Lean checks that
each polynomial variable maps to the corresponding frozen `coordinateDerivative`.

The proof does not construct fundamental solutions. `M1255-N-FOURIER`, `M1255-L-DIVISION`, and
`M1255-C-FUNDSOL` remain open, and the remaining proof-graph root cut after accepting the new action
package is `M1255-C-FUNDSOL`. The pinned audit located no arbitrary-symbol tempered-distribution
division theorem to import. The classical distributional source claim versus the frozen tempered
strengthening also remains an unresolved source-fidelity boundary. The accepted frozen root remains
`M3` in the pre-proof artifacts; the partial child closure supports an `M2` proposal pending master
acceptance. Theorem completion is false.

## Commands and results

Commands ran in this worker clone. The proof checker resolved the pinned Lean executable and
`LEAN_PATH` through `lake env`, reused the existing canonical pinned `.lake` olean closure, and used
a disposable directory under `/tmp`. No worker command ran an update, build, clone, or fetch.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, passed |
| `python3 scripts/stage1_target.py show THM-M-1255` | 0 | rank 160, planned, L0/rework-required, theorem incomplete |
| `bash Stage1_Instances/THM-M-1255/check_proof.sh` | 0 | isolated trust-zero Statement and ObligationTree oleans plus the exact Proof module elaborated; the conditional composition and four printed proof declarations reported only `propext`, `Classical.choice`, and `Quot.sound` |
| `python3 Stage1_Instances/THM-M-1255/check_proof.py` | 0 | receipt identity, hashes, obligation fingerprints, open-root boundary, exact proof surfaces, and prohibited-device scan passed |
| `python3 Stage1_Instances/THM-M-1255/check_obligation_tree.py` | 0 | frozen 13-obligation, 25-edge architecture still validated structurally; its pre-proof closure boundary was not rewritten |
| `rg -n '\b(sorry|admit|sorryAx|implemented_by|native_decide|extern)\b|^[[:space:]]*(axiom|constant|opaque|unsafe)\b' Stage1_Instances/THM-M-1255/Proof.lean` | 1 | empty output: no prohibited placeholder, declaration, or proof device; exit 1 is ripgrep's no-match result |
| `python3 -m json.tool Stage1_Instances/THM-M-1255/proof-receipt.json` | 0 | valid JSON |
| `~/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| per-new-file `git diff --no-index --check /dev/null FILE` loop | 0 aggregate | every new proof artifact had no whitespace diagnostics; no-index exit 1 means only that each file differs from `/dev/null` |
| `git diff --check -- Stage1_Instances/THM-M-1255 .stage1-worker-selftest.json` | 0 | no tracked whitespace errors |

`Proof.lean` SHA-256 is `a7711cc2...2cd3`. Inputs are `Statement.lean`
`06e76a02...e94f`, `ObligationTree.lean` `65399202...fceb`, `obligation-registry.json`
`01908384...9db7`, and `typed-graphs.json` `f01cc5ce...3c30`. The registry denominator remains
`7cbea3ad...c2c9`. The toolchain is Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib is pinned at
`8a178386ffc0f5fef0b77738bb5449d50efeea95`.

## Status boundary

This is provisional worker proof-phase evidence for exactly `M1255-L-COMMUTE` and
`M1255-C-ACTION`, pending master acceptance. It is not a root-proof, validation, release, H0, R0,
hermetic, independent-runner, or theorem-completion receipt. The frozen obligation registry and
typed graphs intentionally remain unchanged for downstream reconciliation.
