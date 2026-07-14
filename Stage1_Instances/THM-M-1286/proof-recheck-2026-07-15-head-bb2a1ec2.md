# THM-M-1286 proof-phase recheck at base bb2a1ec2

Item: `S56-M-1286-PROOF`

Intent: `prove`

Recorded: `2026-07-15T06:15:00+08:00` (`Asia/Shanghai`)

Base revision: `bb2a1ec294938a22b88699da0d30ced721d8ee7b`

Base tree: `d8d58ab94c83274db18efd3af989171acb898759`

## Verdict

`blocked`. No unconditional proof body can truthfully be added for the current canonical target.
The first failed gate is exact canonical statement fidelity, before either open analytic package can
receive proof credit.

`Statement.lean` defines `Euclidean n` as the ordinary Pi type `Fin n -> Real`. Its installed norm
is the finite-product supremum norm, not the Euclidean `l2` norm in the intake's classical Schwarz
rearrangement claim. Consequently, `IsSymmetricDecreasing` is radial-antitone in `l-infinity`
geometry and the vector-valued weak-gradient energy also uses the supremum norm.
`ProofAudit.lean` provides placeholder-free kernel certificates for the Pi norm formula, the norm
discrepancy at coordinates `(1, -1)`, the exponent-one energy integrand, and the product/cube ball
volume formula.

This is a mathematical encoding mismatch rather than a notation issue. Prior analysis gives an
`n = 2`, `p = 1` diamond-tent example whose input supremum-gradient energy is `2`, while its
equimeasurable sup-radial cube tent has energy `2 * sqrt 2`, reversing the frozen inequality. That
analysis is not credited as a kernel proof of `Not PolyaSzegoTarget`: formalizing the weak
derivatives, uniqueness, and integrals would require missing analytic infrastructure.

The positive proof architecture also remains open. The real proof body
`ObligationTree.exactTarget_of_packages` assumes `RearrangementConstruction` and
`GradientEstimate`; it implements neither premise. Focused searches found no compatible terminal
body in the repository or pinned mathlib. The only repository hits outside this target are the
neighboring `THM-M-1285` statement and conditional interfaces, not an implementation. No weaker,
conditional, anisotropic, quadratic-only, or differently typed theorem was substituted.

The item remains `[ ]`. No proof source, proof receipt, or completion self-test manifest was
written. This packet is current-base blocker evidence only.

## Narrow validation

All Lean checks reused the automation-provided symlink to canonical pinned Lake artifacts
read-only. No `lake update`, `lake build`, dependency clone/fetch, network access, or `.lake`
mutation was performed. Compiled outputs were isolated under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1286` | 0 | Rank 457; lifecycle `planned`; lane `hard_mathlib_anchor_and_wrapper`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1286/check_obligation_tree.py` | 0 | 18 obligations and 23 typed edges passed; denominator `e586a1f...ddaa4`; recorded root remains open at `M4`. |
| Isolated `lake env lean --trust=0 -t0` replay below | 0 | `Statement.lean`, the five diagnostic declarations in `ProofAudit.lean`, and the conditional composition in `ObligationTree.lean` elaborated. The three temporary olean sizes were 67,392, 100,776, and 77,176 bytes; the source `#print axioms` reports were `[propext, Classical.choice, Quot.sound]`. |
| Prohibited-construct `rg` over owned Lean files | 1, expected | No `sorry`, `admit`, `axiom`, `sorryAx`, `unsafe`, `implemented_by`, or `native_decide` occurrence. |
| Focused semantic `rg` in pinned mathlib | 1, expected | No compatible equimeasurability, symmetric-decreasing/Schwarz rearrangement, or Polya-Szego terminal body. |
| Same semantic `rg` over repository Lean sources excluding this target | 0 | Only `THM-M-1285` statement and conditional-interface material; no compatible terminal body. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD^{commit}` and `HEAD^{tree}` | 0 | Pinned mathlib commit `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. |
| `python3 -m json.tool Stage1_Instances/THM-M-1286/proof-recheck-2026-07-15-head-bb2a1ec2.json` | 0 | Structured current-base blocker is valid JSON. |
| `git diff --check` plus `git diff --no-index --check` for each packet file | 0 / 1, expected | No whitespace diagnostic; no-index returned the expected new-file difference status. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test is deliberately absent because the proof phase is blocked. |

Exact Lean replay, run from the repository root. Here `TMP` denotes a fresh external temporary
directory; its machine-specific absolute path is intentionally not recorded:

```bash
set -euo pipefail
ROOT=$PWD
TMP=$(mktemp -d "${TMPDIR:-/tmp}/thm-m-1286-slot57-bb2a1ec2.XXXXXX")
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/Stage1_Instances/THM-M-1286"
cd "$ROOT/Formalizations/Lean"
LEAN_NUM_THREADS=1 timeout 180 lake env lean --trust=0 -t0 -R ../.. \
  -o "$TMP/Stage1_Instances/THM-M-1286/Statement.olean" \
  ../../Stage1_Instances/THM-M-1286/Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP" timeout 180 lake env lean --trust=0 -t0 -R ../.. \
  -o "$TMP/ProofAudit.olean" \
  ../../Stage1_Instances/THM-M-1286/ProofAudit.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP" timeout 180 lake env lean --trust=0 -t0 -R ../.. \
  -o "$TMP/ObligationTree.olean" \
  ../../Stage1_Instances/THM-M-1286/ObligationTree.lean
wc -c "$TMP/Stage1_Instances/THM-M-1286/Statement.olean" \
  "$TMP/ProofAudit.olean" "$TMP/ObligationTree.olean"
```

Pinned input SHA-256 values are `ef428b6d...9bb` (`Statement.lean`), `09152048...47a9`
(`ProofAudit.lean`), `31690c4c...4d6b` (`ObligationTree.lean`), and `321626c8...2d81`
(`lake-manifest.json`).

## Retry condition

Reopen `S56-M-1286-STATEMENT`, replace the ordinary Pi type with a measure-compatible Euclidean
`l2` encoding, and rerun statement identity/transports/mutations, anchor audit, registry, typed
graphs, and obligation-tree gates. Then implement both analytic packages without placeholders or
pin and exact-type-check an immutable compatible Lean 4 proof body.

## Status boundary

Lifecycle remains `planned`; root vector remains `[H2, M4, R3]` as recorded by intake/README,
although `typed-graphs.json` has a stale `H3` conflict that integration must reconcile. Integration
should consider `M5` for the checked statement mismatch. No proof completion, audit completion,
validation, release, master acceptance, or theorem completion is claimed.
