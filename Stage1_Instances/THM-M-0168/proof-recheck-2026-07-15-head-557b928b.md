# THM-M-0168 proof recheck at `557b928b`

Item: `S56-M-0168-PROOF`

Date: `2026-07-15T07:54:09+08:00`

Base revision: `557b928b377b386864527c9fb4831d45857837aa`

Base tree: `e677879a6eb4cb9d6795ba1bd78726af06ab9465`

## Verdict

`blocked`. The exact target
`Stage1Instances.THM_M_0168.BernsteinMinimalGraphTarget` has no eligible
premise-free proof body in this repository or the pinned dependency closure.
The proof item remains `[ ]`; lifecycle remains `planned`; the root vector
remains `[H1, M2, R3]`; and no root, audit, validation, release, or theorem
completion is claimed.

The existing `Proof.lean` contains real placeholder-free work.
`constantPartials_to_affine` reconstructs the Frechet derivative from its two
coordinate values, compares against an explicit affine function, and applies
mathlib's connected-domain derivative theorem. Its exact wrapper provisionally
closes `M0168-T-INTEGRATE`. The other wrapper,
`bernstein_of_derivativeRigidity`, consumes `DerivativeRigidity` as a premise;
it does not prove that premise and is not a proof of Bernstein's theorem.

The remaining root cut is:

- `M0168-C-GRAPH`
- `M0168-N-PDE-MINIMAL`
- `M0168-L-STABILITY`
- `M0168-C-CUTOFF`
- `M0168-L-CURVATURE`
- `M0168-L-DERIVATIVE-RIGIDITY`

The first unavailable package is `M0168-C-GRAPH`: construction of the graph
immersion, induced metric, unit normal, and second fundamental form. The
PDE-to-minimality, Jacobi/stability, logarithmic-cutoff, curvature-vanishing,
and derivative-rigidity packages depend on unavailable analytic infrastructure.
Assuming one of them, declaring `DerivativeRigidity`, or claiming the
conditional wrapper as the root would be a placeholder or substituted theorem.

No statement loophole was found. `ContDiff Real 2` expresses genuine C2
regularity; the coordinate directions and iterated Frechet derivatives have
the intended meanings; the PDE signs and coefficients match the classical
two-variable minimal-surface equation; the domain is all of `Real x Real`; and
the conclusion is global affinity. A complete pinned-package scan found only
Bernstein approximation and Schroeder-Bernstein material. The audited external
atlas-lean candidate has pointwise curvature infrastructure and proof gaps, not
an exact entire-minimal-graph rigidity body.

## Validation

All checks ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts was reused
read-only. Lean output was confined to a disposable `/tmp` directory and
removed. No update, build, fetch, clone, network request, or `.lake` mutation
was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 unique targets and ranks passed. |
| `python3 scripts/stage1_target.py show THM-M-0168` | 0 | Rank 665; planned; hard-statement-first partial-verification lane; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0168/check_obligation_tree.py` | 0 | Eleven nodes and the typed acyclic proof graph passed; root remains frozen open. |
| isolated trust-zero Lean replay | 0 | `ObligationTree.lean` and `Proof.lean` elaborated; both axiom reports were exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| owned Lean prohibited-device scan | 1 | Expected no-match exit; no executable placeholder, bodyless declaration, unsafe escape, or native oracle occurs. |
| pinned and repo-local body searches | 0 aggregate | Only unrelated Bernstein declarations and this dossier's partial/conditional bodies were found. |
| proof-input diff from `5112156d` | 0 | Empty output; proof inputs and dependency pins have not changed since affine integration was added. |
| JSON parse and blocker-invariant assertions | 0 | Identity, base/tree, source hashes, open flags, cut set, changed paths, and absent self-test agreed. |
| whitespace checks | 0 | The scoped diff and both fresh blocker files had no whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest deliberately absent because the assigned proof phase is incomplete. |

The reliable replay copied the target modules rather than writing build
artifacts into the repository and put the disposable directory before Lake's
compiled paths:

```bash
set -euo pipefail
repo=$PWD
target=$repo/Stage1_Instances/THM-M-0168
lean_root=$repo/Formalizations/Lean
tmp=$(mktemp -d /tmp/thm-m-0168-proof-slot74.XXXXXX)
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

The proof sources have SHA-256 values `5e773260...1a78` (`Statement.lean`),
`642153a1...f24e` (`ObligationTree.lean`), and `2906d501...8299d`
(`Proof.lean`). The pinned toolchain is Lean 4.29.0 commit
`98dc76e3...16740`; pinned mathlib is `8a178386...ea95`, tree
`bdc39a31...1c2b`.

## Retry Condition

Resume after placeholder-free implementations of the graph, PDE/minimality,
stability, cutoff, curvature, and derivative-rigidity packages. Alternatively,
integrate an immutable compatible Lean 4 proof-bearing declaration of the exact
target with complete dependency, license, terminal-body, and type-transport
evidence.

This is current-base blocker evidence, not a proof receipt. It does not satisfy
`S56-M-0168-PROOF`, propose checklist state, or support root closure or theorem
completion. Because the assigned phase is not genuinely self-tested as
complete, `.stage1-worker-selftest.json` remains absent.
