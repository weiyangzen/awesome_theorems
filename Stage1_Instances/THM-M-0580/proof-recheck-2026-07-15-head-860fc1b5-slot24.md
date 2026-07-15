# THM-M-0580 proof-phase recheck at base 860fc1b5 (slot 24)

Item: `S56-M-0580-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `860fc1b58d914171000ca0f981bf903c32ad5db2`

Base tree: `70bebf93650eba444a713c765f558a7087c0070f`

## Verdict

`blocked`. No eligible terminal Lean 4 proof body exists in the repository, the pinned dependency
closure, or the bounded external candidates inspected for the exact declaration
`Stage1Instances.THM_M_0580.PerelmanPoincareTarget`. No proof body or receipt was added. The proof
item remains `[ ]`, the root vector remains `[H2, M4, R4]`, and the audit, exact root, and theorem
remain incomplete.

The immediate frozen root cut set remains:

- `M0580-N-SMOOTH`, the proposed topological smoothing package;
- `M0580-T-SMOOTH-POINCARE`, the proposed smooth three-dimensional Poincare package.

`root_of_smoothing_and_smooth_poincare` assumes both packages and only composes them. The diagnostic
`smoothThreeDimensionalPoincare_of_perelmanPoincareTarget` runs from the root back to the second
package, so using it to construct a root premise would be circular.

Pinned mathlib supplies the matching generalized, topological, and smooth signatures only through
`proof_wanted`. The pinned Batteries implementation elaborates those signatures inside
`withoutModifyingEnv` and discards them. The trust-zero probe after import confirms all three names
are unknown. Scoped retained-declaration searches found no alternate root or cut-set proof body.

## First Failed Gate

The proof node is not dependency-legal. The prerequisite obligation-tree contract is neither
master-accepted nor executable as a faithful proof architecture: `task-dag.json` has
`accepted_states: []` and records every prerequisite task as open. The generated `[_]` marker is
provisional, not master acceptance.

The frozen contracts also require an append-only prerequisite correction:

- `TopologicalThreeManifoldSmoothable` receives an already selected `ChartedSpace` and requires
  `Nonempty (IsManifold ... M)` for that atlas. It does not construct a compatible replacement
  smooth atlas; wrapping the proposition in `Nonempty` chooses no atlas.
- `SmoothThreeDimensionalPoincare` concludes the same homeomorphism as the root under an extra
  `IsManifold` instance. The root implies this package directly, so it is not a distinct smooth
  theorem.
- The metric, Ricci-flow, surgery, extinction, decomposition, and topology children have planned
  fingerprints rather than exact Lean propositions and own no proof bodies.

Changing these prerequisite contracts in the proof phase would violate the frozen registry and the
worker ownership boundary. Even after a corrected tree is accepted, the Ricci-flow, surgery,
finite-extinction, decomposition, and fundamental-group packages remain unformalized in the pinned
closure.

## Candidate Recheck

The repository and pinned mathlib searches found only statement surfaces, source metadata, the
conditional composition theorem, and its circular diagnostic converse. Four public Lean 4
candidates were inspected read-only in a disposable `/tmp` directory; none is eligible for pinning:

| Candidate and immutable revision | Result |
|---|---|
| `YuanXian-Theory/YXT-PoincareConjecture` at `020557f67392506deccfd30af9f0b2f0c2f38ef5` | The root and prerequisites contain `sorry`. |
| `frenzymath/Poincare-Conjecture` at `2d6abb09774efc7c1a5059f7e78b8679db3be6d2` | Declares itself incomplete; Morgan-Tian coverage stops at chapters 1-2 and contains placeholders. |
| `Spring-1211/OPenPoincare` at `36a51553004038e55d8ec0529e2f0a3eebe7f6e2` | The apparent endpoint depends on placeholder-bearing Morgan-Tian and endgame modules. |
| `HautevilleHouse/poincare-conjecture-canonical-lane-mathlib` at `094627249f637dccd9e92eff220b772961475506` | Explicitly keeps the theorem boundary open; its sphere endpoint is caller-supplied data, not a constructed root proof. |

These observations are discovery evidence only. No dependency was added or mutated, and no moving
external result is used as proof credit.

## Validation

All commands ran in this worker clone. The automation-provided canonical `.lake` symlink was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, or dependency mutation was run by
this worker. Lean outputs were confined to a disposable `/tmp` directory and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0580` | 0 | rank 115; planned; L0/rework-required; theorem incomplete |
| `git rev-parse HEAD HEAD^{tree} && git status --short` | 0 | base `860fc1b58d914171000ca0f981bf903c32ad5db2`; tree `70bebf93650eba444a713c765f558a7087c0070f`; only the automation-provided `.lake` symlink was initially untracked |
| isolated trust-zero `lake env lean` chain below | 0 | exact statement, conditional composition, and blocker probe elaborated; local theorem axiom reports were `[propext, Classical.choice, Quot.sound]`; all three `proof_wanted` names were absent |
| `python3 Stage1_Instances/THM-M-0580/check_obligation_tree.py` | 0 | 20 obligations and 42 typed edges passed; denominator `46585d643f518847529b9ef08ddd76ea206e6ca7a9645ce21aa28126d8c98a6d`; root open at M4 |
| `timeout 180 python3 Stage1_Instances/THM-M-0580/check_statement.py` | 143 | The helper was stopped after it spawned a slow full-manifest Lake elaboration. Its temporary file/process was removed; the direct isolated statement elaboration passed. |
| `timeout 120 python3 Stage1_Instances/THM-M-0580/check_anchor_audit.py` | 1 | Immutable local assertions ran first, then GitHub returned HTTP 403 rate limit exceeded; no external result was accepted or changed. |
| scoped retained-declaration search | 0 | no alternate exact-root or cut-set body; no retained theorem, lemma, or axiom for the three `proof_wanted` names |
| inverted prohibited-construct scan | 0 | no `sorry`, `admit`, `axiom`, `sorryAx`, `unsafe`, `implemented_by`, `native_decide`, or `external` token in the four owned Lean modules |
| `ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| pinned mathlib and Batteries revision/tree/status probes | 0 | mathlib `8a178386...` / tree `bdc39a31...`; Batteries `756e3321...` / tree `02666252...`; both clean |

The narrow Lean check was:

```bash
set -u
repo=$PWD
lean_root="$repo/Formalizations/Lean"
target="$repo/Stage1_Instances/THM-M-0580"
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
paths=("$lean_root/.lake/build/lib/lean")
for p in "$lean_root"/.lake/packages/*/.lake/build/lib/lean; do paths+=("$p"); done
lean_path=$(IFS=:; printf '%s' "${paths[*]}")
cd "$target"
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  timeout 300 lake env lean --trust=0 -t0 -o "$tmp/Statement.olean" Statement.lean
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  timeout 300 lake env lean --trust=0 -t0 -o "$tmp/ObligationTree.olean" ObligationTree.lean
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  timeout 300 lake env lean --trust=0 -t0 ProofBlockerProbe.lean
sha256sum "$tmp/Statement.olean" "$tmp/ObligationTree.olean"
```

The temporary olean SHA-256 values were
`8c69718898cfefd3f33ccce0ac95ca8f4e9a82bc28fda79b6b91ae01b7cffba6` for
`Statement.olean` and
`6f2ad414a2fe0d0dd9544cc489751163408ac7b85a9823e3935ff1663af7dcb8` for
`ObligationTree.olean`.

## Retry Condition

First publish and master-accept an append-only obligation-tree revision with a replacement-atlas
smoothing contract, faithful smooth-theorem semantics, exact Lean targets for every child, checked
composition, and declaration-covering recipes. Then implement those packages without placeholders.
Alternatively, integrate an immutable, licensed, compatible exact-root Lean 4 proof with a complete
dependency lock and exact-type, provenance, and trust checks.

Assuming either missing package, treating `proof_wanted` as an axiom, or presenting conditional
composition as root closure would violate the exact-target and proof-body gates. This is an owned
blocker artifact, not a proof receipt; it does not satisfy `S56-M-0580-PROOF`, propose state
promotion, or support theorem completion. Because the phase is not genuinely complete,
`.stage1-worker-selftest.json` remains absent.
