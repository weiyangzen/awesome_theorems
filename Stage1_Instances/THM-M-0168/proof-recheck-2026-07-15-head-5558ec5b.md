# THM-M-0168 proof recheck at `5558ec5b`

Item: `S56-M-0168-PROOF`

Date: `2026-07-15T07:24:18+08:00`

Base revision: `5558ec5b162bfdfa95b44fafcf97b69a44d1ff37`

Base tree: `f17ce1a24cd65800f536301fdb66a12e18ef3ae3`

## Verdict

`blocked`. The exact target
`Stage1Instances.THM_M_0168.BernsteinMinimalGraphTarget` still has no eligible
premise-free proof body in this repository or the pinned dependency closure.
The proof item remains `[ ]`; lifecycle remains `planned`; the root vector
remains `[H1, M2, R3]`; and root closure, audit completion, validation,
release, and theorem completion remain false.

The previously integrated `Proof.lean` contains real, placeholder-free proof
work. `constantPartials_to_affine` reconstructs the full Frechet derivative
from its values in the two coordinate directions, compares the function with
an explicit affine model, and applies mathlib's connected-domain derivative
theorem. Its wrapper is an exact inhabitant of `ConstantPartialsToAffine`, so
the existing body provisionally closes `M0168-T-INTEGRATE`.

The other wrapper, `bernstein_of_derivativeRigidity`, still consumes
`DerivativeRigidity` as a premise. It does not construct that premise and is
not a proof of Bernstein's theorem. After removing the already implemented
integration package, the remaining root cut is:

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
any package, declaring `DerivativeRigidity`, or presenting the conditional
wrapper as the root would be a placeholder or substituted theorem and was not
done.

A complete pinned-package source scan found only Bernstein approximation
polynomials and Schroeder-Bernstein results, not minimal-surface rigidity.
Scoped repo-local search found no body outside this dossier. The prerequisite
immutable external audit's atlas-lean candidate supplies pointwise
mean-curvature infrastructure only; it neither states nor proves the entire
minimal-graph theorem and is not an exact body that can be pinned.

## Validation

All checks ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts was reused
read-only. Generated Lean output was confined to a disposable directory under
`/tmp` and removed. No `lake update`, `lake build`, dependency clone/fetch,
network request, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 unique targets and ranks passed. |
| `python3 scripts/stage1_target.py show THM-M-0168` | 0 | Rank 665; planned; hard-statement-first partial-verification lane; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0168/check_obligation_tree.py` | 0 | Eleven nodes and the typed acyclic proof graph passed; root remains frozen open. |
| isolated trust-zero replay described below | 0 | `ObligationTree.lean` and `Proof.lean` elaborated; printed axiom reports were exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| owned Lean prohibited-device scan | 1 | Expected no-match exit; no executable placeholder, bodyless declaration, unsafe escape, or native oracle occurs. |
| pinned and repo-local terminal-body searches | 0 aggregate | Only unrelated Bernstein declarations and this dossier's partial/conditional bodies were found. |
| current-base input diff | 0 | No statement, obligation, proof, registry, graph, audit, toolchain, or manifest input changed after the partial proof integration. |
| JSON parse and blocker-invariant assertions | 0 | Identity, base/tree, source hashes, open flags, exact cut set, changed paths, and absent completion manifest agreed. |
| scoped and fresh-file whitespace checks | 0 aggregate | Both new blocker files and the scoped diff had no whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest deliberately absent because the proof phase is incomplete. |

The reliable replay copied the two target sources rather than writing build
artifacts into the repository. It put the disposable directory before Lake's
compiled paths so a stale unrelated `ObligationTree.olean` could not shadow
the target module:

```bash
set -euo pipefail
repo=$PWD
target=$repo/Stage1_Instances/THM-M-0168
lean_root=$repo/Formalizations/Lean
tmp=$(mktemp -d /tmp/thm-m-0168-proof-slot77.XXXXXX)
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

The proof-relevant SHA-256 values are `5e773260...1a78` for
`Statement.lean`, `642153a1...f24e` for `ObligationTree.lean`,
`2906d501...8299d` for `Proof.lean`, `883e0c0a...ed9ba` for the obligation
registry, `1e8ac1d8...ac41` for the typed graphs, and
`f29dd210...d4f5b7` for the anchor audit. The pinned toolchain is Lean 4.29.0
commit `98dc76e3...16740`; mathlib is `8a178386...ea95`, tree
`bdc39a31...1c2b`.

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
