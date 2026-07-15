# THM-M-0729 proof-phase recheck at base 7d7c49d1

Item: `S56-M-0729-PROOF`
Date: `2026-07-15T09:13:13+08:00`
Base revision: `7d7c49d13e3186c744ae6258f05a71e1f15fe129`

## Verdict

`blocked`. No eligible Lean 4 proof body for the exact binary PCP target
`Stage1Instances.THM_M_0729.PCPTheorem` was found on the recorded repo-local,
pinned-dependency, and bounded external audit surfaces. No proof body or
obligation closure was added. The proof item remains `[ ]`, the root vector
remains `[H3, M3, R4]`, and root closure, audit completion, validation,
release, and theorem completion remain false.

The immediate proof cut contains both `M0729-D-NP-PCP` and
`M0729-D-PCP-NP`. The forward inclusion needs the frozen verifier-to-constraint
normalization, robust gap theorem, PCP composition, logarithmic-randomness and
constant-query bounds, perfect completeness, and exact soundness-half
transport. The reverse inclusion needs a finite proof-bit certificate,
exhaustive random-string verification with a polynomial cost proof, and the
below-threshold branch.

`root_of_directionalPackage` is checked child-to-root composition, but its
premise already contains both missing inclusions. It constructs neither one.
Assuming `DirectionalPackage`, adding an axiom or bodyless declaration, or
returning this conditional composer as the proof deliverable would be a
placeholder or a substituted theorem and was not done.

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`
contains supporting deterministic Turing-machine, finite-cardinality,
polynomial, and logarithm APIs, but no NP/PCP development or PCP theorem. Its
`Computable.lean` additionally leaves `TM2ComputableInPolyTime.comp` as a
`proof_wanted` marker, so even generic polynomial-time machine composition is
not an importable theorem. The prerequisite bounded immutable anchor audit
found no compatible external terminal proof to pin. No global-absence claim is
made because authenticated GitHub code search was unavailable.

## Validation

All commands ran in this worker clone. The pre-existing untracked
`Formalizations/Lean/.lake` symlink points to canonical pinned artifacts and
was reused read-only. Lean outputs were confined to a disposable directory and
removed. No `lake update`, `lake build`, dependency clone/fetch, network
request, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 unique targets and ranks passed. |
| `python3 scripts/stage1_target.py show THM-M-0729` | 0 | Rank 766; planned; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0729/check_statement.py` | 0 | Exact expression hash `2a3d6c...7bbc5`; all four weakened mutations were distinguished. |
| `python3 Stage1_Instances/THM-M-0729/check_anchor_audit.py` | 0 | Immutable pins and hashes passed; no exact PCP root candidate is claimed. |
| `python3 Stage1_Instances/THM-M-0729/check_obligation_tree.py` | 0 | 19 obligations and 76 typed edges passed; both directions remain open M3. |
| Isolated pinned `lake env lean --trust=0 -t0` replay | 0 | Exact statement, conditional composition, and `ProofBlockerProbe.lean` elaborated; axioms were exactly `propext`, `Classical.choice`, and `Quot.sound`; the theorem-shaped polynomial-time composition application failed as expected. |
| Scoped repository and pinned-mathlib PCP search | 0 | PCP target declarations were confined to this dossier; no terminal inclusion/root body was found. |
| Search for `proof_wanted TM2ComputableInPolyTime.comp` | 0 | Pinned mathlib records only the discarded marker at `Computable.lean:284`. |
| Prohibited-device scan of checked local Lean files | 1 | Expected no-match exit; no prohibited proof device was found. |
| Scoped diff from prior blocker integration `9864b47f` | 0 | No statement, registry, graph, audit, pin, manifest, or execution-skill input changed. |
| JSON parse and exact `jq -e` blocker-invariant predicate | 0 | The paired structured artifact is valid and reports blocked/open/false completion throughout. |
| Grouped assertion around three `git diff --no-index --check /dev/null <new-file>` checks plus scoped `git diff --check` | 0 | Each no-index check returned expected difference exit 1 without a whitespace diagnostic; the tracked scoped check returned 0. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no completion manifest. |

The trust-zero replay used disposable copies and this command shape from the
worker root:

```bash
set -euo pipefail
tmp=$(mktemp -d /tmp/thm-m-0729-slot27.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-0729/{Statement,ObligationTree,ProofBlockerProbe}.lean "$tmp/"
lake_bin=$(cd Formalizations/Lean && lake env which lake)
lean_path=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd "$tmp"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300s \
  "$lake_bin" env lean --trust=0 -t0 -R "$tmp" -o Statement.olean Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300s \
  "$lake_bin" env lean --trust=0 -t0 -R "$tmp" -o ObligationTree.olean ObligationTree.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300s \
  "$lake_bin" env lean --trust=0 -t0 -R "$tmp" ProofBlockerProbe.lean
```

## Reopen Condition

Resume only after placeholder-free implementations of both frozen directional
packages and their reduction, resource, certificate, enumeration, and boundary
dependencies are available. Alternatively, integrate an immutable compatible
Lean 4 terminal proof of the exact target with full dependency and license
evidence, then repeat exact-type, trust, provenance, and composition checks.

This packet is blocker evidence, not a proof receipt. It does not satisfy
`S56-M-0729-PROOF`, promote scheduler state, or support theorem completion.
Because the assigned phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` remains absent.
