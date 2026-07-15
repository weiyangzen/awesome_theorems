# THM-M-0168 proof recheck at `4e4f31e4`

Item: `S56-M-0168-PROOF`

Date: `2026-07-15T08:05:18+08:00`

Base revision: `4e4f31e4342e7160fe132b536fb7dc565fa1ded0`

Base tree: `e2c22705bcd18e365b5ac54abb241f70b338a853`

## Verdict

`blocked`. The exact target
`Stage1Instances.THM_M_0168.BernsteinMinimalGraphTarget` has no eligible
premise-free proof body in this repository or the pinned dependency closure.
The proof item remains `[ ]`; lifecycle remains `planned`; the provisional
obligation-registry/proof-recheck root vector remains `[H1, M2, R3]`; and
root closure, audit completion, validation, release, and theorem completion
remain false. The earlier intake authority `instance.json` still records
`[H1, M4, R4]`; this blocked attempt does not rewrite or silently reconcile
that stale vector.

The integrated `Proof.lean` contains real, placeholder-free proof work.
`constantPartials_to_affine` reconstructs the full Frechet derivative from
its values in the two coordinate directions, compares the function with an
explicit affine model, and applies mathlib's connected-domain derivative
theorem. Its wrapper is an exact inhabitant of `ConstantPartialsToAffine`, so
the body provisionally closes only `M0168-T-INTEGRATE`.

The pre-proof registry and typed graphs remain frozen: they still list all
seven packages, including `M0168-T-INTEGRATE`, in the architectural cut and
set `closure_metrics_observed=false`. This recheck records the integration
body as a provisional observation only. It does not rewrite that frozen
authority or manufacture an accepted receipt.

The other wrapper, `bernstein_of_derivativeRigidity`, consumes
`DerivativeRigidity` as a premise. It does not construct that premise and is
not a proof of Bernstein's theorem. Moreover, it composes the separately
namespaced target duplicated in `ObligationTree.lean`; this attempt adds no
checked transport to the canonical declaration in `Statement.lean`. After
crediting the implemented integration package only within that harness, the
remaining root cut is:

- `M0168-C-GRAPH`
- `M0168-N-PDE-MINIMAL`
- `M0168-L-STABILITY`
- `M0168-C-CUTOFF`
- `M0168-L-CURVATURE`
- `M0168-L-DERIVATIVE-RIGIDITY`

The first unavailable package is graph geometry: the immersion, induced
metric, unit normal, and second fundamental form. The PDE-to-minimality,
Jacobi/stability, logarithmic-cutoff, curvature-vanishing, and final
derivative-rigidity packages depend on it and are likewise absent. Assuming
one of these packages or presenting the conditional wrapper as the root
would be a placeholder or substituted theorem and was not done.

A complete pinned-package Lean-source search found no occurrence of minimal
surfaces, mean curvature, or minimal graphs. Its Bernstein hits were only
approximation-polynomial and Schroeder-Bernstein material. The scoped
repo-local search found no exact body outside this dossier. The prerequisite
immutable anchor audit's atlas-lean candidate supplies pointwise
mean-curvature infrastructure only; it neither states nor proves the entire
minimal-graph theorem and cannot be pinned as an exact body.

## Validation

All checks ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts was reused
read-only. Generated Lean output was confined to a disposable `/tmp`
directory and removed. No `lake update`, `lake build`, dependency
clone/fetch, network request, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 unique targets and ranks passed. |
| `python3 scripts/stage1_target.py show THM-M-0168` | 0 | Rank 665; planned; hard-statement-first partial-verification lane; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0168/check_statement.py` | 0 | Four structural mutations were rejected; target fingerprint, toolchain, and mathlib pin agreed. |
| `python3 Stage1_Instances/THM-M-0168/check_anchor_audit.py` | 0 | Audit boundary, five Lean probes, pinned revision, and immutable external metadata passed. |
| `python3 Stage1_Instances/THM-M-0168/check_obligation_tree.py` | 0 | Eleven nodes and the typed acyclic graph passed; the root remains frozen open. |
| Isolated trust-zero replay described below | 0 | `ObligationTree.lean` and `Proof.lean` elaborated; printed axiom reports were exactly `propext`, `Classical.choice`, and `Quot.sound`; no canonical-statement transport is claimed. |
| Owned Lean prohibited-device scans | 1, expected | No executable placeholder, bodyless declaration, unsafe escape, or native oracle occurs. |
| Pinned and repo-local terminal-body searches | 1 for geometry/exact names | No minimal-surface geometry or exact root body was found; all 163 Bernstein lines were unrelated. |
| Scoped input diff from proof integration | 0 | Statement, obligations, proof, registry, graphs, audit, target manifest, skill, toolchain, and dependency manifest are unchanged. |
| JSON parse and blocker-invariant assertions | 0 | Identity, base/tree, hashes, open flags, exact cut, changed paths, and absent completion manifest agreed. |
| Scoped and fresh-file whitespace checks | 0 aggregate | The scoped diff and both new blocker files had no whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest deliberately absent because the proof phase is incomplete. |

The isolated replay copied the target sources instead of writing build
artifacts into the repository. It put the disposable directory before
Lake's compiled paths so an unrelated `ObligationTree.olean` could not
shadow this module:

```bash
set -euo pipefail
repo=$PWD
target=$repo/Stage1_Instances/THM-M-0168
lean_root=$repo/Formalizations/Lean
tmp=$(mktemp -d "${TMPDIR:-/tmp}/thm-m-0168-proof.XXXXXX")
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
base_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cp "$target/ObligationTree.lean" "$tmp/ObligationTree.lean"
cp "$target/Proof.lean" "$tmp/Proof.lean"
cd "$tmp"
LEAN_NUM_THREADS=1 LEAN_PATH="$base_path" timeout 300s \
  "$lean" --trust=0 -t0 -R "$tmp" \
  -o "$tmp/ObligationTree.olean" "$tmp/ObligationTree.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_path" timeout 300s \
  "$lean" --trust=0 -t0 -R "$tmp" "$tmp/Proof.lean"
```

The SHA-256 values of the captured combined stdout/stderr logs were
`bc3bace903d4c39a16358b20c3e54224d63ee7c77db690c5eb0911c5daf8bd80`
for the obligation log and
`baf43808013b12ba38dc0daee1bcafd26cc40d07f9dc77d7a36221155ea8b04b`
for the proof log. The proof-relevant source SHA-256 values are
`5e773260...1a78` for `Statement.lean`, `642153a1...f24e` for
`ObligationTree.lean`, `2906d501...8299d` for `Proof.lean`,
`883e0c0a...ed9ba` for the obligation registry, `1e8ac1d8...ac41` for the
typed graphs, and `f29dd210...d4f5b7` for the anchor audit. The pinned
toolchain is Lean 4.29.0 commit `98dc76e3...16740`; mathlib is
`8a178386...ea95`, tree `bdc39a31...1c2b`.

## Retry Condition

Resume after placeholder-free implementations of the graph,
PDE/minimality, stability, cutoff, curvature, and derivative-rigidity
packages. Alternatively, integrate an immutable compatible Lean 4
proof-bearing declaration of the exact target with complete dependency,
license, terminal-body, and type-transport evidence.

This is current-base blocker evidence, not a proof receipt. It does not
satisfy `S56-M-0168-PROOF`, propose checklist state, or support root closure
or theorem completion. Because the assigned phase is not genuinely
self-tested as complete, `.stage1-worker-selftest.json` remains absent.
