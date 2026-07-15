# THM-M-1566 proof-phase recheck at current base

Item: `S56-M-1566-PROOF`

Recorded at: `2026-07-15T09:16:19+08:00`

Base revision: `f3154d6bc995341e5ea34f1a36af1c66ba0574ae`

Base tree: `d5aa1e2a22e1541afc7502c652503905afa5c3bd`

## Verdict

`blocked`. No consistent positive proof body can inhabit the exact frozen Lean
target. The existing placeholder-free declaration

```text
Stage1Instances.THMM1566.not_GIPCorollary59Target :
  Not (Stage1Instances.THMM1566.GIPCorollary59Target.{0})
```

kernel-checks at trust level zero against a fresh temporary `Statement.olean`.
A universe-polymorphic proof of the positive target would specialize to
universe zero and contradict this declaration.

The frozen target quantifies over every `GIPCorollary59API`, but the API has no
adequacy condition tying its fields to the source mathematics and no
nonemptiness condition on `Solution`. The checked countermodel takes
`Omega := Unit`, the Dirac probability measure, `Unit` for every non-solution
carrier, and `Empty` for `Solution`. Its data assumptions are inhabited at
`alpha = beta = 3/4`. Applying the target produces an inhabitant of `Empty`.
Lean reports only `propext`, `Classical.choice`, and `Quot.sound` for the
refutation.

This refutes the frozen abstract encoding, not Gubinelli--Imkeller--Perkowski
Corollary 5.9. Merely requiring `Nonempty api.Solution` would remain
insufficient because the API may interpret `solvesLimitEquation` as `False`.
A repair needs concrete analytic semantics or substantive noncircular adequacy
laws. Adding either during this phase would change the frozen statement and
invalidate all downstream fingerprints. The conditional theorem
`root_of_existence_and_uniqueness` remains valid, but it consumes the open
existence and uniqueness packages and cannot close the root.

No positive proof body, proof receipt, or frozen obligation was added or
closed. The proof item remains `[ ]`; the recorded dossier vector remains
`[H1, M4, R3]`, with `[H1, M5, R3]` only the proposed diagnosis for the
refutable encoding. Proof-phase completion, root closure, audit completion,
validation, release, theorem completion, and master acceptance are all false.
Because the assigned phase is not complete, `.stage1-worker-selftest.json` is
deliberately absent.

## Failed Gate And Retry

The first failed gate is the positive kernel-closure gate for
`S56-M-1566-PROOF` / `M1566-ROOT`. The defect originates in the unconstrained
interface modeled by `M1566-S-INTERFACE`. In the checked model it directly
invalidates `M1566-T-EXISTENCE`, while `M1566-T-UNIQUENESS` is vacuous for the
empty solution carrier and remains open in the predecessor registry. The
actionable repair cut therefore starts at `S56-M-1566-STATEMENT`,
`M1566-S-INTERFACE`, `M1566-T-EXISTENCE`, and `M1566-ROOT`.

Resume only after an authorized statement revision replaces the universal
unconstrained API with a fixed source-faithful implementation or adds
noncircular adequacy hypotheses that entail the analytic semantics and an
appropriate solution type. Accept a new exact expression fingerprint, refreeze
the anchor audit and obligation registry, and rerun all downstream phases
before attempting a positive proof.

## Validation

All checks ran in this worker clone against the existing pinned Lake artifacts.
The automation-provided untracked `Formalizations/Lean/.lake` symlink was
reused read-only. No `lake update`, `lake build`, dependency clone/fetch,
network access, or `.lake` mutation was performed. Temporary Lean objects were
created under `/tmp` and removed by a shell trap. The worktree was already
non-clean solely because of that automation symlink, so this is nonrelease
evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1566` | 0 | Rank 182; planned lifecycle; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1566/check_statement.py` | 0 | Canonical expression SHA-256 `70ee4869...473a`; all four structural mutations were distinguished. |
| `python3 Stage1_Instances/THM-M-1566/check_anchor_audit.py` | 0 | Four candidates, four search records, five pinned Lean support probes, and the M4 boundary agreed. |
| `python3 Stage1_Instances/THM-M-1566/check_obligation_tree.py` | 0 | 15 obligations and 40 typed edges passed; denominator `7ae15c07...3fe640`; root remains open M4. |
| `python3 Stage1_Instances/THM-M-1566/validate_obligation_tree.py` | 0 | Exact statement and conditional composition elaborated; composition reports `[propext, Classical.choice, Quot.sound]`. |
| Isolated trust-zero `lake env lean` recipe below | 0 | Exact statement and refutation elaborated; object hashes are `1e1c07...2793` and `611605...62f3`; temporary directory was removed. |
| `rg -n '\b(sorry\|admit\|sorryAx\|native_decide\|implemented_by)\b\|^[[:space:]]*(axiom\|opaque\|constant\|unsafe\|external)[[:space:]]' Stage1_Instances/THM-M-1566 --glob '*.lean'` | 1 | Expected no-match exit; no prohibited proof escape occurs. |
| `python3 -m json.tool Stage1_Instances/THM-M-1566/proof-recheck-2026-07-15-head-f3154d6b.json` | 0 | The structured current-base blocker is valid JSON. |
| Inline Python assertions over the paired JSON and eight bound source hashes | 0 | Base identity, item identity, open-root flags, empty proof credit, `[ ]` state, changed paths, source hashes, and absent self-test agreed. |
| `git diff --no-index --check /dev/null` for each new artifact | 1, 1 | Expected added-file status with empty diagnostic output; no whitespace errors. |
| `git diff --check -- Stage1_Instances/THM-M-1566` | 0 | No whitespace errors in tracked owned-path changes. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no completion manifest. |

Exact isolated Lean recipe, run from the repository root:

```bash
set -euo pipefail
repo=$PWD
tmp=$(mktemp -d /tmp/thm-m-1566-proof-recheck-f3154d6b.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$repo/Stage1_Instances/THM-M-1566/Statement.lean" "$tmp/Statement.lean"
cp "$repo/Stage1_Instances/THM-M-1566/ProofCountermodel.lean" "$tmp/ProofCountermodel.lean"
lean=$(cd "$repo/Formalizations/Lean" && lake env which lean)
lean_path=$(cd "$repo/Formalizations/Lean" && lake env printenv LEAN_PATH)
cd "$tmp"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout --foreground 300s \
  "$lean" --trust=0 -t0 -R "$tmp" -o Statement.olean Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH=.:"$lean_path" timeout --foreground 300s \
  "$lean" --trust=0 -t0 -R "$tmp" -o ProofCountermodel.olean ProofCountermodel.lean
sha256sum Statement.olean ProofCountermodel.olean
```

The paired JSON artifact binds the input and environment fingerprints. This is
durable blocker evidence, not a proof receipt.
