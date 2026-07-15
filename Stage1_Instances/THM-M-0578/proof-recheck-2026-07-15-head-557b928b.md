# THM-M-0578 proof-phase recheck at base 557b928b

Item: `S56-M-0578-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `557b928b377b386864527c9fb4831d45857837aa`

Base tree: `e677879a6eb4cb9d6795ba1bd78726af06ab9465`

## Verdict

`blocked`. The exact frozen target
`Stage1Instances.THM_M_0578.MilnorExoticSphereTarget` still has no eligible
terminal Lean 4 proof body in the repository or pinned dependency closure. No
proof body was added. The proof item stays `[ ]`, the root vector stays
`[H3, M4, R4]`, and root closure, audit completion, validation, release, and
theorem completion remain false.

The frozen immediate root cut set is unchanged:

- `M0578-C-BUNDLE`: construct the selected smooth Milnor bundle total space;
- `M0578-T-HOMEO`: identify it with the fixed unit seven-sphere by a homeomorphism;
- `M0578-O-NONDIFF`: exclude every smooth diffeomorphism to that sphere.

The first failed proof gate is terminal proof-body availability for
`M0578-C-BUNDLE`. The local theorem
`ObligationTree.root_of_exoticWitnessPackage` is valid checked composition, but
its premise already contains the smooth manifold, homeomorphism, and
nondiffeomorphism certificate. It constructs none of the open packages and
therefore supplies no root proof credit.

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`
contains the exact signature only as
`proof_wanted exists_homeomorph_isEmpty_diffeomorph_sphere_seven`.
`proof_wanted` elaborates a signature without retaining a declaration. A
trust-zero direct import probe reports that name as unknown. The locally
available mathlib `master` ref also retains only the marker, and all-ref source
history finds its introduction but no proof-bearing replacement.

A fresh scoped search produced 20 Lean-source hits outside this dossier. They
are confined to `THM-M-0605`'s duplicate statement and conditional witness
assembly, legacy metadata probes, one neighboring prose comment, and mathlib's
discarded marker. None is an unconditional proof of the target or of an open
root-cut package.

The tempting standard-sphere witness was checked rather than assumed away. A
trust-zero scratch theorem proves
`not IsEmpty (S^7 Diffeomorph S^7)` by applying the alleged emptiness proof to
`Diffeomorph.refl`. Thus the standard smooth sphere cannot satisfy the target.
Choosing a different atlas together with the required emptiness certificate is
exactly the missing exotic-smooth-structure theorem, not an encoding shortcut.

The repository base changed after the prior `5558ec5b` recheck and incorporated
that packet. A whitelist diff and exact hashes show no change to the statement,
composition interface, frozen registry and graphs, anchor ledger, validation
specs, Lean toolchain, or dependency manifest. This packet rebinds the still
valid blocker analysis to the current base rather than treating stale-base
evidence as fresh.

Closing the frozen route requires a genuine formalization of the Milnor
sphere-bundle construction and conventions, a homotopy-sphere calculation and
topological identification, and distinguishing smooth-invariant computations
with invariance strong enough to derive `IsEmpty Diffeomorph`. Assuming any of
those packages, treating `proof_wanted` as an axiom, or returning only the
conditional composer would be a placeholder or substituted theorem and was
not done.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts was reused
read-only. Lean outputs were confined to disposable directories and removed.
No `lake update`, `lake build`, dependency clone/fetch, network request, or
`.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0578` | 0 | rank 622; planned lifecycle; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0578/check_statement.py` | 0 | exact target elaborated; all four structural mutations were distinguished; statement digest `c9d29902...d32c`. |
| `python3 Stage1_Instances/THM-M-0578/check_anchor_audit.py` | 0 | exact marker, pins, source hash, discard semantics, and M4 formalization-debt boundary passed. |
| `python3 Stage1_Instances/THM-M-0578/check_obligation_tree.py` | 0 | 13 obligations and 28 typed edges passed; denominator `67da617160dcfef6ea2eb819f105ab0e2a68a351476d55e5761d2e668e63aeda`; root remains open M4. |
| isolated trust-zero `lake env lean` replay | 0 | exact statement and conditional composition elaborated; `#print axioms` reported only `propext`, `Classical.choice`, and `Quot.sound`. |
| trust-zero standard-sphere loophole/name probe | 0 | identity diffeomorphism refutes `IsEmpty` for the standard witness, with only the three expected axioms; the imported `proof_wanted` name is unknown. |
| scoped retained-body and prerequisite search | 0 | 20 hits outside the dossier are duplicate statements/composition, metadata, prose, or the discarded marker; no eligible terminal body exists. |
| local mathlib `master` and all-ref history inspection | 0 | `master` still has `proof_wanted`; only introduction commit `041fe1fa487` contains the exact marker change. |
| forbidden-construct scan of owned Lean files | 1 | expected no-match exit; no prohibited proof escape was found. |
| scoped `git diff --name-status 5558ec5b..HEAD` | 0 | empty for the proof-input whitelist and Lean pins; the whole-target delta contains only the prior blocker packet. |
| `python3 -m json.tool Stage1_Instances/THM-M-0578/proof-recheck-2026-07-15-head-557b928b.json` | 0 | current-base blocker record is valid JSON. |
| owned-path and added-file `git diff --check` recipes | 0 | no whitespace diagnostic; expected added-file statuses were handled by the wrapper. |
| `test ! -e .stage1-worker-selftest.json` | 0 | incomplete proof phase emitted no completion manifest. |

The isolated kernel replay used the pinned executable and dependency path:

```bash
set -euo pipefail
tmp=$(mktemp -d /tmp/thm-m-0578-proof-557b928b.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-0578/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-0578/ObligationTree.lean "$tmp/ObligationTree.lean"
lean=$(cd Formalizations/Lean && lake env which lean)
lean_path=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 600s \
  "$lean" --trust=0 -t0 -R "$tmp" -o "$tmp/Statement.olean" \
  "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 600s \
  "$lean" --trust=0 -t0 -R "$tmp" "$tmp/ObligationTree.lean"
```

The scratch loophole probe imported the same pinned Poincare module, defined
the standard unit seven-sphere, derived a contradiction from an assumed
`IsEmpty` using `Diffeomorph.refl`, printed its axioms, and used
`#check_failure` on the discarded marker name. It elaborated under trust zero
and was removed after the run. The paired JSON artifact binds this evidence to
the current base/tree, input hashes, registry denominator, and environment.

## Retry Condition

Resume after placeholder-free implementations of `M0578-C-BUNDLE`,
`M0578-T-HOMEO`, and `M0578-O-NONDIFF` with their frozen child obligations.
Alternatively, integrate an immutable compatible Lean 4 proof-bearing
declaration of the exact root with a complete dependency lock and license, then
rerun the exact-type, trust, provenance, and composition checks.

This is blocker evidence, not a proof receipt. It does not satisfy
`S56-M-0578-PROOF`, proposes no state promotion, and supports neither root
closure nor theorem completion. Because the assigned phase is not genuinely
self-tested as complete, `.stage1-worker-selftest.json` remains absent.
