# THM-M-0578 proof-phase recheck at base a1a7e939

Item: `S56-M-0578-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `a1a7e939e58f103f5ff5d23af51437fa8658aa04`

Base tree: `d881fd9641fa3e5f3ebe5082b35672981e90adcf`

## Verdict

`blocked`. No eligible terminal Lean 4 proof body exists in the repository or
pinned dependency closure for the exact frozen proposition
`Stage1Instances.THM_M_0578.MilnorExoticSphereTarget`. This attempt adds no
proof body and leaves the root vector at `[H3, M4, R4]`. The proof item remains
`[ ]`; root closure, audit completion, validation, release, and theorem
completion remain false.

The frozen immediate root cut set is unchanged:

- `M0578-C-BUNDLE`, construction of the selected smooth Milnor bundle total space;
- `M0578-T-HOMEO`, a homeomorphism to the fixed unit seven-sphere;
- `M0578-O-NONDIFF`, exclusion of every smooth diffeomorphism to that sphere.

The first failed proof gate is terminal proof-body availability for
`M0578-C-BUNDLE`. The checked theorem
`ObligationTree.root_of_exoticWitnessPackage` only consumes an
`ExoticWitnessPackage`. That premise already contains a smooth seven-manifold,
a homeomorphism to the fixed sphere, and the complete nondiffeomorphism
certificate. The theorem performs valid child-to-parent composition but
constructs none of those inputs and supplies no root proof credit.

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`
contains the exact source shape only as
`proof_wanted exists_homeomorph_isEmpty_diffeomorph_sphere_seven`.
`proof_wanted` checks its signature without retaining a declaration. A direct
trust-zero import probe reports the name as unknown, so it cannot be imported,
wrapped, or counted as an axiom-free terminal body. A scoped Lean-source search
found no alternate retained proof of the root or any cut-set package.

Closing the frozen route requires a genuine formalization of the Milnor
sphere-bundle construction and its boundary conventions, a homotopy-sphere
calculation and topological identification with the standard sphere, and
candidate/standard smooth-invariant computations plus invariance strong enough
to derive `IsEmpty Diffeomorph`. Assuming any package, treating `proof_wanted`
as an axiom, or returning the conditional composition would be a placeholder
or a substituted theorem and was not done.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink was reused read-only. Lean outputs were
confined to a disposable `/tmp` directory and removed. No `lake update`,
`lake build`, dependency clone/fetch, network access, or `.lake` mutation was
performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0578` | 0 | rank 622; planned lifecycle; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0578/check_anchor_audit.py` | 0 | exact `proof_wanted` marker, pins, source hash, discard semantics, and M4 formalization-debt boundary passed. |
| `python3 Stage1_Instances/THM-M-0578/check_obligation_tree.py` | 0 | 13 obligations and 28 typed edges passed; denominator `67da617160dcfef6ea2eb819f105ab0e2a68a351476d55e5761d2e668e63aeda`; root remains open M4. |
| isolated trust-zero `lake env lean` recipe below | 0 | exact statement and conditional composition elaborated; `#print axioms` reported only `propext`, `Classical.choice`, and `Quot.sound`. |
| direct trust-zero probe of `exists_homeomorph_isEmpty_diffeomorph_sphere_seven` | 1 | expected negative evidence: `Unknown identifier` after importing `Mathlib.Geometry.Manifold.PoincareConjecture`. |
| scoped `rg` search for the exact target, marker, Milnor sphere, and exotic seven-sphere terms | 0 | hits were limited to the two local statement/composition dossiers, three legacy metadata references, and mathlib's discarded marker; no terminal proof body was found. |
| forbidden-construct `rg` scan of owned Lean files | 1 | expected no-match exit; no prohibited proof escape was found. |
| `python3 -m json.tool Stage1_Instances/THM-M-0578/proof-recheck-2026-07-15-head-a1a7e939.json` | 0 | the current-base blocker record is valid JSON. |
| `git diff --no-index --check /dev/null <each new artifact>` | 1 each | expected added-file status with no whitespace diagnostic. |
| `test ! -e .stage1-worker-selftest.json` | 0 | the incomplete phase emitted no completion manifest. |

The isolated kernel replay used the pinned executable and dependency path:

```bash
set -euo pipefail
tmp=$(mktemp -d /tmp/thm-m-0578-proof-recheck.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-0578/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-0578/ObligationTree.lean "$tmp/ObligationTree.lean"
lean=$(cd Formalizations/Lean && lake env which lean)
lean_path=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd "$tmp"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300s \
  "$lean" --trust=0 -t0 -R "$tmp" -o Statement.olean Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH=.:"$lean_path" timeout 300s \
  "$lean" --trust=0 -t0 -R "$tmp" ObligationTree.lean
```

The paired JSON artifact binds the exact source hashes, registry denominator,
toolchain, pinned mathlib revision/tree, commands, and results.

## Retry Condition

Resume after placeholder-free implementations of `M0578-C-BUNDLE`,
`M0578-T-HOMEO`, and `M0578-O-NONDIFF` with their frozen child obligations.
Alternatively, integrate an immutable compatible Lean 4 proof-bearing
declaration of the exact root with a complete dependency lock and license, then
rerun the node-scoped exact-type, trust, provenance, and composition checks.

This is an owned blocker artifact, not a proof receipt. It does not satisfy
`S56-M-0578-PROOF` or propose state promotion. Because the assigned proof phase
is not genuinely self-tested as complete, `.stage1-worker-selftest.json`
remains absent.
