# THM-M-0578 proof-phase recheck at base fb0fd5be

Item: `S56-M-0578-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `fb0fd5be494d0813177dbdc959ec911d69a72015`

Base tree: `f6d39faae5fb024a71ee786e7a6b017d335841cd`

## Verdict

`blocked`. The exact frozen target
`Stage1Instances.THM_M_0578.MilnorExoticSphereTarget` has no eligible terminal
Lean 4 proof body in the repository or pinned dependency closure. No proof body
was added. The proof item stays `[ ]`, the root vector stays `[H3, M4, R4]`,
and root closure, audit completion, validation, release, and theorem completion
remain false.

The frozen immediate root cut set is unchanged:

- `M0578-C-BUNDLE`: construct the selected smooth Milnor bundle total space;
- `M0578-T-HOMEO`: identify it with the fixed unit seven-sphere by a homeomorphism;
- `M0578-O-NONDIFF`: exclude every smooth diffeomorphism to that sphere.

The first failed proof gate is terminal proof-body availability for
`M0578-C-BUNDLE`. The only local proof body,
`ObligationTree.root_of_exoticWitnessPackage`, consumes a premise that already
contains the smooth manifold, homeomorphism, and nondiffeomorphism certificate.
It is a valid conditional composition term, but it constructs none of the open
packages and supplies no root proof credit.

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`
contains the exact signature only as
`proof_wanted exists_homeomorph_isEmpty_diffeomorph_sphere_seven`.
`proof_wanted` elaborates the signature without retaining a declaration. A
trust-zero direct import probe therefore reports that name as unknown. Scoped
source searches found no alternate retained Milnor-sphere, exotic-sphere,
Eells-Kuiper, or Kervaire-Milnor proof body. The available bordism module says
that bordisms, bordism groups, and their basic theory remain future work, so it
does not provide the smooth-obstruction infrastructure required by this root.

Closing the frozen route requires a genuine formalization of the Milnor
sphere-bundle construction and conventions, a homotopy-sphere calculation and
topological identification, and distinguishing smooth-invariant computations
with invariance strong enough to derive `IsEmpty Diffeomorph`. Assuming any of
those packages, treating `proof_wanted` as an axiom, or returning only the
conditional composer would be a placeholder or substituted theorem and was not
done.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink to the canonical pinned artifacts was
reused read-only. Lean outputs were confined to a disposable directory and
removed. No `lake update`, `lake build`, dependency clone/fetch, network
request, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0578` | 0 | rank 622; planned lifecycle; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0578/check_statement.py` | 0 | exact target elaborated; all four structural mutations were distinguished; statement digest `c9d29902...d32c`. |
| `python3 Stage1_Instances/THM-M-0578/check_anchor_audit.py` | 0 | exact marker, pins, source hash, discard semantics, and M4 formalization-debt boundary passed. |
| `python3 Stage1_Instances/THM-M-0578/check_obligation_tree.py` | 0 | 13 obligations and 28 typed edges passed; denominator `67da617160dcfef6ea2eb819f105ab0e2a68a351476d55e5761d2e668e63aeda`; root remains open M4. |
| isolated trust-zero `lake env lean` recipe below | 0 | exact statement and conditional composition elaborated; `#print axioms` reported only `propext`, `Classical.choice`, and `Quot.sound`. |
| direct trust-zero probe of the `proof_wanted` name | 1 | expected negative evidence: `Unknown identifier` after importing its module. |
| scoped retained-body and prerequisite searches | 0/1 | only local statement/composition dossiers, legacy metadata, the discarded marker, and preliminary generic infrastructure were found; no eligible terminal body exists. |
| forbidden-construct scan of owned Lean files | 1 | expected no-match exit; no prohibited proof escape was found. |
| `python3 -m json.tool Stage1_Instances/THM-M-0578/proof-recheck-2026-07-15-head-fb0fd5be.json` | 0 | current-base blocker record is valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-0578` plus `git diff --no-index --check /dev/null <each new artifact>` | 0 / 1 | tracked-diff check passed; each added-file check returned the expected added-file status with no whitespace diagnostic. |
| `test ! -e .stage1-worker-selftest.json` | 0 | incomplete proof phase emitted no completion manifest. |

The isolated kernel replay uses the pinned executable and dependency path:

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

The paired JSON artifact binds the current base and tree, exact source hashes,
registry denominator, pinned environment, commands, and status boundary.

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
