# THM-M-0168 proof recheck at `30228d98`

Item: `S56-M-0168-PROOF`

Date: `2026-07-15T13:07:28+08:00`

Base revision: `30228d98c98c401cb60a3dfa09eec01bb904053f`

Base tree: `773a33c6344fb9787649fbc5edea99092ea68856`

## Verdict

`blocked`. The exact target
`Stage1Instances.THM_M_0168.BernsteinMinimalGraphTarget` has no eligible
premise-free proof body in this repository or the pinned dependency closure.
The proof item remains `[ ]`; lifecycle remains `planned`; the provisional
obligation-registry/proof-recheck root vector remains `[H1, M2, R3]`; and root
closure, audit completion, validation, release, and theorem completion remain
false. The earlier intake authority `instance.json` still records
`[H1, M4, R4]`; this blocked attempt does not rewrite or silently reconcile
that stale vector.

The integrated `Proof.lean` contains real placeholder-free work.
`constantPartials_to_affine` reconstructs the full Frechet derivative from its
values on the two coordinate vectors, compares the function with an explicit
affine model, and invokes mathlib's connected-domain derivative theorem. Its
wrapper is an exact inhabitant of `ConstantPartialsToAffine`, so the body
provisionally closes only `M0168-T-INTEGRATE`.

The frozen registry and typed graphs remain unchanged and intentionally retain
the pre-proof architectural cut. This recheck records the integration body as
a provisional observation only; it does not manufacture an accepted receipt.

The other wrapper, `bernstein_of_derivativeRigidity`, consumes
`DerivativeRigidity` as a premise. It does not construct that premise and is
not a proof of Bernstein's theorem. It also composes the separately namespaced
target duplicated in `ObligationTree.lean`; there is no checked transport to
the canonical `Statement.lean` declaration. After crediting only the existing
integration package inside that harness, the remaining root cut is:

- `M0168-C-GRAPH`
- `M0168-N-PDE-MINIMAL`
- `M0168-L-STABILITY`
- `M0168-C-CUTOFF`
- `M0168-L-CURVATURE`
- `M0168-L-DERIVATIVE-RIGIDITY`

The first unavailable package is graph geometry: construction of the graph
immersion, induced metric, unit normal, and second fundamental form. The
PDE-to-minimality, Jacobi/stability, logarithmic-cutoff, curvature-vanishing,
and derivative-rigidity packages depend on missing analytic infrastructure.
Assuming one of them or presenting the conditional wrapper as root closure
would be a placeholder or substituted theorem and was not done.

A complete pinned-package Lean-source search found no occurrence of minimal
surfaces, mean curvature, or minimal graphs. Its 163 Bernstein result lines
were only approximation-polynomial and Schroeder-Bernstein material. The
scoped repo-local search found no exact body outside this dossier, and history
contains no later proof implementation. The prerequisite immutable anchor
audit's atlas-lean candidate supplies pointwise mean-curvature infrastructure
only; it neither states nor proves the entire minimal-graph theorem.

## Validation

All checks ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink points to the shared canonical cache. No
`lake update`, `lake build`, dependency clone/fetch, cache repair, or deliberate
`.lake` mutation was performed.

The prescribed `lake env` path was attempted once and failed immediately
because the shared `flt-regular` checkout's `.git/HEAD` contains
`ref: refs/heads/.invalid`. Concurrent automation uses the cache, so this
worker makes no cache-integrity or no-mutation claim. Narrow nonrelease replay
used the pinned Lean executable and only already-built pinned package paths;
all generated output lived in disposable `/tmp` directories and was removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 unique targets and ranks passed. |
| `python3 scripts/stage1_target.py show THM-M-0168` | 0 | Rank 665; planned; hard-statement-first partial-verification lane; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0168/check_statement.py` | terminated | Still blocked in its prescribed Lake child after 30 seconds; process terminated and temporary source removed. The separate bounded Lake probe below captured the exact invalid-HEAD error. |
| `python3 Stage1_Instances/THM-M-0168/check_anchor_audit.py` | 0 | Audit boundary, five Lean probes, pinned mathlib revision, and immutable external metadata passed. |
| `python3 Stage1_Instances/THM-M-0168/check_obligation_tree.py` | 0 | Eleven nodes and the typed acyclic graph passed; root remains frozen open. |
| Direct trust-zero canonical-statement replay | 0 | `Statement.lean` elaborated; captured log SHA-256 was `779f510c...72fc`. |
| Direct trust-zero obligation/proof replay | 0 | Both sources elaborated; axiom reports were exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| Owned Lean prohibited-device scans | 1, expected | No executable placeholder, bodyless declaration, unsafe escape, or native oracle occurs. |
| Pinned and repo-local terminal-body searches | 1, expected | No minimal-surface geometry or outside-dossier exact body was found. |
| Scoped input diff from `5112156d` | 0 | Statement, obligations, proof, registry, graphs, audit, target manifest, skill, toolchain, and dependency manifest are unchanged. |
| `cd Formalizations/Lean && timeout --foreground 15s lake env lean --version` | 1 | `flt-regular` could not resolve `HEAD`. |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse --verify HEAD` | 128 | No valid commit; `.git/HEAD` names `refs/heads/.invalid`. |

The reliable obligation/proof replay copied the target modules rather than
writing build artifacts into the repository and put the disposable directory
before all compiled paths:

```bash
set -euo pipefail
repo=$PWD
target=$repo/Stage1_Instances/THM-M-0168
packages=$(readlink -f "$repo/Formalizations/Lean/.lake/packages")
tmp=$(mktemp -d /tmp/thm-m-0168-proof-slot59.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$target/ObligationTree.lean" "$tmp/ObligationTree.lean"
cp "$target/Proof.lean" "$tmp/Proof.lean"
lean=$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean
lean_path="$packages/mathlib/.lake/build/lib/lean:$packages/batteries/.lake/build/lib/lean:$packages/Qq/.lake/build/lib/lean:$packages/aesop/.lake/build/lib/lean:$packages/proofwidgets/.lake/build/lib/lean:$packages/importGraph/.lake/build/lib/lean:$packages/LeanSearchClient/.lake/build/lib/lean:$packages/plausible/.lake/build/lib/lean"
cd "$tmp"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout --foreground 300s \
  "$lean" --trust=0 -t0 -R "$tmp" \
  -o "$tmp/ObligationTree.olean" "$tmp/ObligationTree.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout --foreground 300s \
  "$lean" --trust=0 -t0 -R "$tmp" "$tmp/Proof.lean"
```

The SHA-256 values of the captured obligation and proof logs were
`bc3bace903d4c39a16358b20c3e54224d63ee7c77db690c5eb0911c5daf8bd80`
and `baf43808013b12ba38dc0daee1bcafd26cc40d07f9dc77d7a36221155ea8b04b`.
The proof sources remain `5e773260...1a78` (`Statement.lean`),
`642153a1...f24e` (`ObligationTree.lean`), and `2906d501...8299d`
(`Proof.lean`). The pinned toolchain is Lean 4.29.0 commit
`98dc76e3...16740`; pinned mathlib is `8a178386...ea95`, tree
`bdc39a31...1c2b`.

## Retry Condition

Resume after placeholder-free implementations of the graph, PDE/minimality,
stability, cutoff, curvature, and derivative-rigidity packages. Alternatively,
integrate an immutable compatible Lean 4 proof-bearing declaration of the exact
target with complete dependency, license, terminal-body, and type-transport
evidence. Separately restore the manifest-pinned `flt-regular` checkout before
prescribed `lake env` validation.

This is current-base blocker evidence, not a proof receipt. It does not satisfy
`S56-M-0168-PROOF`, propose checklist state, or support root closure or theorem
completion. Because the assigned phase is not genuinely self-tested as
complete, `.stage1-worker-selftest.json` remains absent.
