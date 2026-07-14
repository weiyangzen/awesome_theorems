# THM-M-1286 proof-phase recheck at current base

Item: `S56-M-1286-PROOF`

Intent: `prove`

Recorded: `2026-07-15T07:22:29+08:00` (`Asia/Shanghai`)

Base revision: `5558ec5b162bfdfa95b44fafcf97b69a44d1ff37`

Base tree: `f17ce1a24cd65800f536301fdb66a12e18ef3ae3`

## Verdict

`blocked`. No unconditional proof body can truthfully be added for the frozen canonical target.
The first failed gate is exact statement fidelity, before either open analytic package can receive
proof credit.

`Statement.lean` defines `Euclidean n` as the ordinary Pi type `Fin n -> Real`. The installed norm
is the finite-product supremum norm, not the Euclidean `l2` norm used by the classical Schwarz
rearrangement claim in the intake. Thus `IsSymmetricDecreasing`, metric balls, and the norm inside
the vector-valued gradient `eLpNorm` all use `l-infinity` geometry. `ProofAudit.lean` gives checked,
placeholder-free certificates for the Pi norm, the two-dimensional norm discrepancy, the
exponent-one energy integrand, and the product/cube ball-volume formula.

This is a mathematical encoding mismatch, not a notation issue. The existing counterexample
analysis at `n = 2`, `p = 1` is not claimed as a kernel proof of
`Not PolyaSzegoTarget`: formalizing its weak derivatives, rearrangement uniqueness, and exact
integrals requires analytic infrastructure that is not present in the pinned closure.

Even if statement fidelity were set aside, the positive proof architecture remains open.
`ObligationTree.exactTarget_of_packages` is a real checked composition body, but it assumes both
`RearrangementConstruction` and `GradientEstimate`. It implements neither premise. Current-base
searches found no compatible terminal body in the repository or pinned mathlib. No weaker,
conditional, specialized, anisotropic, or differently typed theorem was substituted.

The item remains `[ ]`. No proof source, proof receipt, or completion self-test manifest was
written. This file and its JSON companion are blocker evidence only.

## Narrow validation

The worker reused the automation-provided `.lake` symlink to the canonical pinned artifacts
read-only. No `lake update`, `lake build`, dependency clone/fetch, network access, or `.lake`
mutation was performed. Lean outputs were isolated in a temporary directory and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1286` | 0 | Rank 457; lifecycle `planned`; lane `hard_mathlib_anchor_and_wrapper`; `theorem_complete=false`. |
| `python3 Stage1_Instances/THM-M-1286/check_obligation_tree.py` | 0 | 18 obligations and 23 typed edges passed; denominator `e586a1f...ddaa4`; root remains open at `M4`. |
| Isolated trust-zero Lean replay below | 0 | `Statement.lean`, five diagnostics in `ProofAudit.lean`, and conditional composition in `ObligationTree.lean` elaborated. Olean sizes were 67,392, 100,776, and 77,176 bytes. All six `#print axioms` reports were `[propext, Classical.choice, Quot.sound]`. |
| `rg -n --pcre2 '\b(?:sorry\|admit\|axiom)\b\|sorryAx\|unsafe\|implemented_by\|native_decide' Stage1_Instances/THM-M-1286 --glob '*.lean'` | 1, expected | No prohibited construct occurs in owned Lean source. |
| `rg -n -i 'equimeasur\|symmetric.?decreas\|schwarz.?rearrang\|polya.?szego\|pólya.?szegő' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1, expected | No compatible pinned-mathlib proof candidate. |
| The same semantic search over repository Lean sources, excluding this target | 0 | Only neighboring `THM-M-1285` statement and conditional-interface material; no terminal body. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | Commit `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. |
| Scoped `git diff --quiet 799262a5..HEAD` over target inputs and the Lean locks | 0 | Statement, proof diagnostics, obligation artifacts, toolchain, and dependency lock are unchanged since the latest integrated checked blocker. |
| `python3 -m json.tool Stage1_Instances/THM-M-1286/proof-recheck-2026-07-15-head-5558ec5b-slot58.json` | 0 | Structured current-base blocker is valid JSON. |
| `git diff --check` plus normalized `git diff --no-index --check /dev/null FILE` for both packet files | 0 | No whitespace diagnostics; each raw no-index invocation returned the expected new-file status `1`. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test deliberately absent because proof execution is blocked. |

The exact Lean replay was run from the repository root. `TMP` was a fresh external temporary
directory:

```bash
set -euo pipefail
ROOT=$PWD
TMP=$(mktemp -d "${TMPDIR:-/tmp}/thm-m-1286-slot58-5558ec5b.XXXXXX")
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

The checked input SHA-256 values are `ef428b6d...9bb` (`Statement.lean`),
`09152048...47a9` (`ProofAudit.lean`), `31690c4c...4d6b` (`ObligationTree.lean`),
`c7d331ee...d20` (`obligation-registry.json`), `9c225e12...7e2` (`typed-graphs.json`),
`f05ca7a6...33c` (`anchor-audit.json`), `2ee56fb5...4e9a` (`validation-specs.json`), and
`321626c8...2d81` (`lake-manifest.json`).

## Retry condition

Reopen `S56-M-1286-STATEMENT`, replace the ordinary Pi type with a measure-compatible Euclidean
`l2` encoding, and rerun statement identity, transport, mutation, anchor, registry, graph, and
obligation-tree gates. Then implement the rearrangement-construction and gradient-estimate packages
without placeholders, or pin and exact-type-check an immutable compatible Lean 4 proof body.

## Status boundary

Lifecycle remains `planned`; the recorded root vector remains `[H2, M4, R3]`, with statement
mismatch warranting integration review. This packet does not satisfy `S56-M-1286-PROOF` and claims
no audit completion, validation, release, master acceptance, or theorem completion.
