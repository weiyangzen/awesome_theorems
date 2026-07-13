# THM-M-1140 proof-phase recheck at 5a080720

Item: `S56-M-1140-PROOF`

Intent: `prove`

Base revision: `5a080720059200b542aa35ee17a748b3251fe8d0`

Base tree: `d7029aa7599db39fbcc55e968a4fe70376143f27`

Recorded at: `2026-07-14T03:33:53+08:00`

## Verdict

`blocked`. The exact assigned proof phase remains open at the arbitrary-dimensional
`InteriorLocalRigidity` package. No placeholder-free local proof or eligible pinned import was
found, so the exact root remains `[H2, M3, R3]` and the item remains `[ ]`. This is fresh owned
blocker evidence, not a proof receipt, audit-completion claim, theorem-completion claim, validation
claim, release claim, scheduler transition, or master acceptance.

The frozen root quantifies over every `n : Nat`: a real-valued `HarmonicOnNhd` function on a
nonempty connected open subset of `EuclideanSpace Real (Fin n)` that attains its maximum at a
domain point is constant on the domain. Specializing to the complex plane, adding a
positive-dimension hypothesis, assuming local rigidity, or returning only the conditional
composition would change or leave open that target.

## Closed Support And Open Cut

`Proof.lean` genuinely proves `ConnectedLevelPropagation`. It makes the maximum-level set in the
domain subtype nonempty, closed by continuity, and open using the supplied local-equality
neighborhoods; connectedness then makes it the whole subtype. `ObligationTree.lean` genuinely
composes that package and a supplied `InteriorLocalRigidity` into the exact root. Neither
declaration constructs the missing analytic package.

The remaining root cut is:

1. `M1140-L-MEAN-VALUE`: an arbitrary-dimensional analytic local-equality mechanism.
2. `M1140-T-LOCAL-PACKAGE`: an inhabitant of `InteriorLocalRigidity`.
3. `M1140-ROOT`: exact composition after the local package closes.

The pinned mathlib revision supplies the finite-dimensional Laplacian definition, `C^2`
regularity, continuity, harmonicity openness, and algebraic closure. Its harmonic mean-value and
harmonic-to-real-analytic declarations are specialized to functions on the complex plane. A fresh
pinned-source search exposed only those complex-plane results, complex differentiable maximum
principles, and unrelated convex maximum principles; it found no declaration that inhabits the
general local package or root.

The adjacent `THM-M-1138` target now has a placeholder-free arbitrary-dimensional weak maximum
proof by strict-subharmonic perturbation. Rechecking that route does not close this target: on a
ball it recovers only the already assumed inequality `u z <= u y`, not the reverse inequality
needed for local equality. A Hopf-barrier upgrade would require substantial new formalization of
first contact or a tangent annulus, an exponential barrier and its positive Laplacian, a boundary
comparison, and a derivative contradiction. Pinned mathlib has no ready Laplacian
composition/product or barrier theorem, and `THM-M-1138` supplies only the local-maximum
Laplacian inequality and the norm-square computation. No unproved premise or speculative partial
barrier was introduced.

A public Sourcegraph recheck for Lean strong-maximum, harmonic local-max/constancy, and harmonic
mean-value declarations returned no new matching proof. The previously audited Atlas candidate
remains ineligible because its harmonic-to-mean-value closure contains unproved bodies and opaque
analytic objects. No external dependency was installed, cloned, fetched, or added to Lake.

## Validation

All Lean checks reused the automation-provided canonical pinned `.lake` link read-only. Source
copies and generated oleans were confined to fresh `/tmp` directories and removed. No `lake
update`, `lake build`, dependency clone/fetch, or `.lake` repair was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1140` | 0 | Rank 345; lifecycle `planned`; legacy artifacts unaccepted; theorem incomplete |
| isolated `lake env lean --trust=0` replay of `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` using the recipe below | 0 | All three modules elaborated; `harmonicStrongMaximumPrinciple_of_packages` and `connectedLevelPropagation` each reported only `propext`, `Classical.choice`, and `Quot.sound` |
| `python3 Stage1_Instances/THM-M-1140/check_obligation_tree.py` | 0 | 16 obligations and 36 typed edges passed; denominator `355cbcf...0bee`; frozen root open at `M3` |
| prohibited-construct scan over the three local Lean modules | 1 | Expected clean no-match for `sorry`, `admit`, `sorryAx`, custom axiom/constant, opaque/unsafe body, extern, `implemented_by`, or `native_decide` |
| prohibited-construct scan of adjacent `THM-M-1138/Proof.lean` | 1 | Expected clean no-match; the weak-maximum implementation is a genuine candidate input, but it does not prove local rigidity |
| scoped pinned-mathlib source search for strong maximum, harmonic local constancy, and harmonic mean value | 0 | Thirteen textual matches: complex-plane harmonic mean value, complex differentiable maximum principles, and unrelated convex results; no exact general proof body |
| ten public Sourcegraph Lean query families for strong maximum, `HarmonicOnNhd` local max/constancy, Laplacian maximum, and harmonic mean value | 0 | Every query completed with zero matches; no new candidate was found |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |

The isolated Lean recipe was:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-1140
tmp=$(mktemp -d /tmp/thm-m-1140-proof-slot63.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cp "$target/Statement.lean" "$tmp/Statement.lean"
cp "$target/ObligationTree.lean" "$tmp/ObligationTree.lean"
cp "$target/Proof.lean" "$tmp/Proof.lean"
cd "$tmp"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  "$lean" --trust=0 -o Statement.olean Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH=".:$lean_path" \
  "$lean" --trust=0 -o ObligationTree.olean ObligationTree.lean
LEAN_NUM_THREADS=1 LEAN_PATH=".:$lean_path" \
  "$lean" --trust=0 Proof.lean
```

Pinned environment: Lean commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`; `lake-manifest.json` SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Retry Condition

Resume positive proof work only with a placeholder-free arbitrary-dimensional harmonic
local-rigidity implementation, or an immutable compatible Lean 4 terminal theorem whose complete
transitive proof closure can be pinned, exact-type transported, provenance-audited, and
kernel-checked without changing the target. Because the assigned phase is not complete, no
`.stage1-worker-selftest.json` is written.
