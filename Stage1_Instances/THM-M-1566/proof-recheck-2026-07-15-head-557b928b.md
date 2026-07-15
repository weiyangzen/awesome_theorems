# THM-M-1566 proof-phase recheck at current base

Item: `S56-M-1566-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `557b928b377b386864527c9fb4831d45857837aa`

Base tree: `e677879a6eb4cb9d6795ba1bd78726af06ab9465`

## Verdict

`blocked`. No consistent positive proof body can inhabit the exact frozen Lean
target. The existing placeholder-free declaration

```text
Stage1Instances.THMM1566.not_GIPCorollary59Target :
  Not (Stage1Instances.THMM1566.GIPCorollary59Target.{0})
```

kernel-checks at trust level zero against a fresh temporary `Statement.olean`.
Failure of the universe-zero specialization blocks a proof of the requested
universe-polymorphic target.

The target quantifies over every `GIPCorollary59API`, but the API has no
adequacy condition tying its fields to the source mathematics and no
nonemptiness condition on `Solution`. The checked countermodel takes
`Omega := Unit`, the Dirac probability measure, `Unit` for every non-solution
carrier, and `Empty` for `Solution`. Its data assumptions are inhabited at
`alpha = beta = 3/4`. Applying the claimed target supplies an inhabitant of
`Empty`. Lean reports only `propext`, `Classical.choice`, and `Quot.sound` for
the refutation.

This refutes the frozen abstract encoding, not Gubinelli--Imkeller--Perkowski
Corollary 5.9. Merely requiring `Nonempty api.Solution` is also insufficient:
an API may keep `Solution := Unit` while interpreting `solvesLimitEquation` as
`False`. Repair requires concrete analytic semantics or substantive,
noncircular adequacy laws. Adding either during this phase would change the
frozen statement and invalidate its downstream fingerprints. The conditional
theorem `root_of_existence_and_uniqueness` remains valid, but it consumes the
open existence and uniqueness packages and cannot close the root.

No positive proof body, proof receipt, or frozen obligation was added or
closed. The proof item remains `[ ]`; the recorded dossier vector remains
`[H1, M4, R3]`, with `[H1, M5, R3]` only the proposed diagnosis for the
refutable encoding. Proof-phase completion, root closure, audit completion,
validation, release, theorem completion, and master acceptance are all false.
Because the assigned phase is not complete, `.stage1-worker-selftest.json` is
deliberately absent.

## Failed gate and retry

The first failed gate is exact-target consistency at `M1566-S-INTERFACE`.
The predecessor graph records `M1566-T-EXISTENCE` and
`M1566-T-UNIQUENESS` as the root cut, but neither package can hold uniformly
for an API whose solution type is empty. The actionable cut therefore starts
at `S56-M-1566-STATEMENT`, `M1566-S-INTERFACE`, and `M1566-ROOT`.

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
created under `/tmp` and removed by a shell trap.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1566` | 0 | Rank 182; planned lifecycle; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1566/check_statement.py` | 0 | Canonical expression SHA-256 `70ee4869...473a`; all four structural mutations were distinguished. |
| `python3 Stage1_Instances/THM-M-1566/check_anchor_audit.py` | 0 | Four candidates, four search records, five pinned Lean support probes, and the M4 boundary agreed. |
| `python3 Stage1_Instances/THM-M-1566/check_obligation_tree.py` | 0 | 15 obligations and 40 typed edges passed; denominator `7ae15c07...3fe640`; the predecessor graph still records the root as open M4. |
| `python3 Stage1_Instances/THM-M-1566/validate_obligation_tree.py` | 0 | The exact statement and conditional composition elaborated; the composition reports `[propext, Classical.choice, Quot.sound]`. |
| Isolated trust-zero `lake env lean` recipe below | 0 | The exact statement and refutation elaborated; `not_GIPCorollary59Target` has the exact type above and reports `[propext, Classical.choice, Quot.sound]`. Object hashes were `1e1c07...2793` and `611605...62f3`; the temporary directory was removed. |
| `rg -n '\b(sorry\|admit\|sorryAx\|native_decide\|implemented_by)\b\|^[[:space:]]*(axiom\|opaque\|constant\|unsafe\|external)[[:space:]]' Stage1_Instances/THM-M-1566 --glob '*.lean'` | 1 | Expected no-match exit; no prohibited proof escape occurs. |
| `python3 -m json.tool Stage1_Instances/THM-M-1566/proof-recheck-2026-07-15-head-557b928b.json` | 0 | The current-base structured blocker record is valid JSON. |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-1566/proof-recheck-2026-07-15-head-557b928b.json` | 1 | Expected new-file difference with no whitespace diagnostic. |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-1566/proof-recheck-2026-07-15-head-557b928b.md` | 1 | Expected new-file difference with no whitespace diagnostic. |
| `git diff --check -- Stage1_Instances/THM-M-1566` | 0 | No whitespace errors in tracked owned-path differences. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no completion manifest. |

Exact isolated Lean recipe, run from the repository root:

```bash
set -euo pipefail
repo=$PWD
tmp=$(mktemp -d /tmp/thm-m-1566-proof-recheck-557b928b.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$repo/Stage1_Instances/THM-M-1566/Statement.lean" "$tmp/Statement.lean"
cp "$repo/Stage1_Instances/THM-M-1566/ProofCountermodel.lean" "$tmp/ProofCountermodel.lean"
lean_path=$(cd "$repo/Formalizations/Lean" && lake env printenv LEAN_PATH)
cd "$repo/Formalizations/Lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout --foreground 300s \
  lake env lean --trust=0 -t0 -R "$tmp" -o "$tmp/Statement.olean" \
  "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout --foreground 300s \
  lake env lean --trust=0 -t0 -R "$tmp" -o "$tmp/ProofCountermodel.olean" \
  "$tmp/ProofCountermodel.lean"
sha256sum "$tmp/Statement.olean" "$tmp/ProofCountermodel.olean"
```

The paired JSON artifact binds the source hashes and environment fingerprint.
This is durable blocker evidence, not a proof receipt.
