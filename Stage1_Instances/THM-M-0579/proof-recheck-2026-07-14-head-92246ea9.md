# THM-M-0579 proof-phase recheck at base 92246ea9

Item: `S56-M-0579-PROOF`

Recheck date: 2026-07-14 (Asia/Shanghai)

Base revision: `92246ea92c0c44282c05728798bc7c7e4a5a1464`

Base tree: `bd58be98bf3046078c016d44fb4a677ea231cb23`

## Verdict

`blocked`. No eligible retained Lean 4 proof body was found for the exact frozen
proposition `Stage1Instances.THMM0579.Statement`. This recheck adds no proof
source and leaves the root vector at `[H3, M3, R4]`. The proof item remains
`[ ]`; the audit, root, and theorem remain incomplete.

The frozen immediate root cut set is unchanged:

- `M0579-T-RECOGNITION`, the homotopy-sphere recognition package;
- `M0579-T-RIGIDITY`, the three-dimensional topological rigidity package.

The recognition branch expands through smoothing, prime normalization, Ricci
flow with surgery, surgery invariants, Perelman analytic estimates, finite
extinction, and surgery recomposition. The local theorem
`root_of_recognition_and_rigidity` checks only the composition of recognition
and rigidity into the exact root. Both packages are premises of that theorem,
not proof bodies it constructs, so the composition earns no root proof credit.
Moreover, the rigidity premise already asks for the root conclusion after an
extra homotopy-equivalence premise; it is an honest interface boundary, not a
difficulty-reducing terminal theorem. A scoped trust-zero probe proved
`Statement.{u} ↔ HomotopySphereRecognition.{u} ∧
HomotopySphereTopologicalRigidity.{u}`: a root homeomorphism supplies recognition
through `Homeomorph.toHomotopyEquiv`, and supplies rigidity by ignoring its extra
premise. Thus the frozen cut is logically equivalent to the root. Correcting
that architecture requires the obligation-tree authority to publish an
append-only registry revision; this proof worker does not silently rewrite it.

Pinned mathlib contains the matching topological signature only as
`proof_wanted SimplyConnectedSpace.nonempty_homeomorph_sphere_three`.
Batteries elaborates `proof_wanted` under `withoutModifyingEnv`, so the helper
declaration is discarded. A trust-zero `#check_failure` probe confirms that the
matching generalized, topological, and smooth names are absent after import.
A scoped retained-declaration search found no alternate local or pinned body.
The immutable candidates already frozen in `anchor-audit.json` provide either
a three-dimensional statement plus an unrelated dimension-zero proof, or an
explicit `sorry` body. Neither can be pinned or imported for proof credit.

## Validation

All commands ran in this worker clone. Lean outputs were confined to a
disposable `/tmp` directory and removed. No `lake update`, `lake build`,
dependency clone/fetch, or `.lake` mutation was performed. The automation-
provided untracked `.lake` symlink was reused read-only, so this is nonrelease
evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0579` | 0 | rank 114; planned; L0/rework-required; theorem incomplete |
| `python3 Stage1_Instances/THM-M-0579/check_obligation_tree.py` | 0 | 16 obligations and 34 typed edges passed; denominator `984bcfffcea5afa7c11e3f2eb78ad31c2eed6b99e1a0913496186ceb1595776f`; root remains open at M3 and both cut-set packages remain M4 |
| `python3 Stage1_Instances/THM-M-0579/check_anchor_audit.py` | 0 | frozen target, five candidates, dependency pins, discarded `proof_wanted` boundary, and noncompletion status agreed |
| isolated trust-zero `lake env lean` recipe below | 0 | `Statement.lean` and the conditional composition in `ObligationTree.lean` elaborated; no mathematical package premise was closed |
| trust-zero cut-equivalence probe | 0 | proved `Statement.{u} ↔ HomotopySphereRecognition.{u} ∧ HomotopySphereTopologicalRigidity.{u}`; the theorem reported only `propext`, `Classical.choice`, and `Quot.sound` |
| trust-zero `#check_failure` probe for the three matching mathlib names | 0 | each source marker was confirmed absent from the imported environment |
| forbidden-construct scan of `Statement.lean`, `AnchorAudit.lean`, and `ObligationTree.lean` | 1 | expected no match for `sorry`, `admit`, `axiom`, `sorryAx`, `unsafe`, `implemented_by`, `native_decide`, or `external` |
| scoped retained-declaration search | 1 | expected no match for a theorem, lemma, definition, opaque declaration, or abbreviation supplying any matching sphere-three proof name |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |

The successful isolated elaboration recipe, run from the repository root, was:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0579
tmp=$(mktemp -d /tmp/thm-m-0579-proof-slot32-92246ea9.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$target"
LEAN_PATH="$lean_path" "$lean" --trust=0 -o "$tmp/Statement.olean" Statement.lean
LEAN_PATH="$tmp:$lean_path" "$lean" --trust=0 ObligationTree.lean
```

The direct absence probe imported
`Mathlib.Geometry.Manifold.PoincareConjecture` and used `#check_failure` on:

```text
ContinuousMap.HomotopyEquiv.nonempty_homeomorph_sphere
SimplyConnectedSpace.nonempty_homeomorph_sphere_three
SimplyConnectedSpace.nonempty_diffeomorph_sphere_three
```

The proof-relevant input hashes were unchanged:

```text
Statement.lean              307061f5847f145fb8cb4e91116ed8ab0c76e3ddc0e9301486fd879be1cf3de8
ObligationTree.lean         f5214263374c23fd2f235cdf4d06bc9cadfd50d4abbe41de32dd55a7e35f0c63
obligation-registry.json    8b70a187e8d4e071c3a658f8b5d8d31fb78dcb2fabc1bedeeddca3fd4c62b31a
typed-graphs.json           e8a756448de68ee250734fc480a06bd3fc55f1827f6da5a847b6bd31677ddce7
anchor-audit.json           0285a80d4d59466d71fdd1d163e1c6a09f7a96b1d0372ea8f682fd69c251f7e7
validation-specs.json       353bdfdcd8341bb9bbd3b3c324b634804144b119ed0b8d0ed161e28d222074aa
```

## Retry Condition

Resume only after placeholder-free implementations of both frozen terminal
packages and their dependencies, or after discovery of a licensed immutable
Lean 4 proof with a compatible dependency lock and exact checked transport to
the canonical root. Such a body must then pass kernel, axiom, placeholder,
provenance, trust, and composition checks without mutating the pinned closure.
Assuming either package, treating `proof_wanted` as an axiom, or returning the
current conditional composition would substitute proof premises for the
requested theorem. Before package-level execution, the obligation-tree
authority should also replace the tautological recognition/rigidity cut with a
new versioned decomposition whose terminal contracts reduce the root rather
than restate it.

This is an owned blocker artifact, not a proof receipt. It does not satisfy
`S56-M-0579-PROOF`, propose a state change, or support audit or theorem
completion. Because the assigned positive proof phase is not genuinely
self-tested as complete, `.stage1-worker-selftest.json` remains absent.
