# THM-M-1063 proof-phase validation

Item: `S56-M-1063-PROOF`

Intent: `prove`

Base revision: `443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b`

Base tree: `c5771c47c12b80aba613e6d844570f83b39ded6d`

Date: `2026-07-15` (`Asia/Shanghai`)

## Implemented bodies

`Proof.lean` contains two unconditional, placeholder-free declarations. The first divides the
increments by positive `sigma` and proves the resulting sequence is a.e. measurable, independent,
identically distributed, in `L2`, centered, and variance one. The second invokes the pinned
mathlib scalar central limit theorem and proves convergence of the variance-normalized real
partial sums to `gaussianReal 0 1`.

These are genuine checked contributions toward `M1063-N-STANDARDIZE` and
`M1063-X-SCALAR-CLT`. This packet claims zero entire frozen obligations closed: both registry
interfaces still have planned fingerprints and null terminal body IDs, and the standardization
body does not transport the whole polygonal path target. The scalar result is only time-one
real-valued convergence, not finite-dimensional convergence, weighted triangular-array
convergence, tightness, or convergence in continuous path space.

## Commands and results

All commands ran inside this worker clone. No `lake update`, `lake build`, dependency clone/fetch,
or `.lake` mutation was performed. The automation-provided canonical `.lake` symlink was reused
read-only.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Rev-5.6 standard, 15 assurance groups, and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-1063` | 0 | Rank 506; lifecycle `planned`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1063/check_obligation_tree.py` | 0 | Frozen 31-obligation registry and 125 typed edges passed; root open at M4. |
| `cd Formalizations/Lean && timeout 30 env -u LEAN_PATH lake env lean --version` | 1 | Top-level Lake stopped before elaboration because `flt-regular/.git/HEAD` points to the missing branch `.invalid`; the worker did not repair it. |
| `bash Stage1_Instances/THM-M-1063/check_proof.sh` | 0 | Lake-first replay fell back to the pinned Lean 4.29 executable and existing compiled import path; both declarations elaborated with `--trust=0` and reported exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| `python3 Stage1_Instances/THM-M-1063/check_proof.py` | 0 | Item identity, ownership, frozen inputs, source policy, pins, open-root boundary, receipt, blocker, dirty paths, and worker packet agreed. |
| `python3 -m json.tool` on the receipt, blocker, and worker packet | 0 | All structured artifacts parsed. |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m1063-proof-pycache python3 -m py_compile Stage1_Instances/THM-M-1063/check_proof.py` | 0 | Checker compiled without repository bytecode output. |
| `git diff --check -- Stage1_Instances/THM-M-1063 .stage1-worker-selftest.json` plus checker-enforced new-file hygiene | 0 | No whitespace, CR, NUL, missing-final-newline, or trailing-space issue. |

The direct fallback command used only the installed `leanprover/lean4:v4.29.0` executable and
compiled `*/.lake/build/lib/lean` directories already present under the manifest-pinned cache.
Lean is commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib is revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. This is warm, dirty, nonrelease evidence.

## Status boundary

The frozen graph remains M4 with cut `M1063-L-CLT`, `M1063-L-MODULUS`,
`M1063-L-ASCOLI`, `M1063-L-PROKHOROV`, `M1063-L-LAW-UNIQUE`, and `M1063-T-API`.
The intake record still says M3; this packet records rather than reconciles that pre-existing
disagreement. The first unavailable package is path construction and path-valued measurability,
followed by FIDI, tightness, limit identification, and API composition. The proposal is `[_]`
for the self-tested partial contribution only. Proof-phase completion, accepted state, validation,
release, `AUDIT-Z`, and `THEOREM-Z` remain open; `theorem_complete=false` remains unchanged.
