# THM-M-1566 proof-phase recheck at current base

Item: `S56-M-1566-PROOF`

Recorded at: `2026-07-15T15:18:13+08:00`

Base revision: `350285c48208616b6e3ad74154d9183d16523cfa`

Base tree: `c4edebc115ec954e4940ed5faaa3ffacd4e56091`

## Verdict

`blocked`. No consistent positive proof body can inhabit the exact frozen Lean
target. The unchanged, placeholder-free declaration

```text
Stage1Instances.THMM1566.not_GIPCorollary59Target :
  Not (Stage1Instances.THMM1566.GIPCorollary59Target.{0})
```

was replayed at trust level zero against the existing pinned Lean and mathlib
objects. The countermodel sets `Omega := Unit`, uses the Dirac probability
measure, takes every non-solution carrier to be `Unit`, and takes
`Solution := Empty`. The numerical premises are inhabited at
`alpha = beta = 3/4`. Applying the positive target therefore supplies an
inhabitant of `Empty`.

This refutes the frozen abstract encoding, not Corollary 5.9 in the cited
Gubinelli--Imkeller--Perkowski paper. Merely requiring
`Nonempty api.Solution` would not repair the encoding: the universally
quantified API can instead make `solvesLimitEquation` false. A source-faithful
concrete semantics or substantive noncircular adequacy hypotheses are needed.
That repair belongs to the statement phase and requires new fingerprints and
refrozen downstream receipts before proof work can resume.

No positive proof body or proof receipt was added. The proof item remains
`[ ]`; `root_closed=false`, `audit_complete=false`, and
`theorem_complete=false`. Because the assigned phase is not complete,
`.stage1-worker-selftest.json` is deliberately absent.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`.lake` symlink was treated as read-only input. No update, build, dependency
clone/fetch, network operation, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1566` | 0 | Rank 182; planned lifecycle; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1566/check_statement.py` | 0 | Exact expression SHA-256 `70ee4869...e473a`; all four structural mutations were distinguished. |
| `python3 Stage1_Instances/THM-M-1566/check_anchor_audit.py` | 0 | Four candidates, four search records, five pinned Lean support probes, and the M4 boundary agreed. |
| `python3 Stage1_Instances/THM-M-1566/check_obligation_tree.py` | 0 | 15 obligations and 40 typed edges passed; denominator `7ae15c07...3fe640`; root remains open M4. |
| `python3 Stage1_Instances/THM-M-1566/validate_obligation_tree.py` | 0 | The exact statement and conditional composition elaborated; `root_of_existence_and_uniqueness` reported `[propext, Classical.choice, Quot.sound]`. |
| Isolated trust-zero `lake env lean` replay below | 0 | The exact statement and refutation elaborated; `not_GIPCorollary59Target` has the exact type above and reported `[propext, Classical.choice, Quot.sound]`. The fresh `Statement.olean` SHA-256 was `1e1c07...2793`; the temporary directory was removed. |
| `rg -n '\b(sorry\|admit\|sorryAx\|native_decide\|implemented_by)\b\|^[[:space:]]*(axiom\|opaque\|constant\|unsafe\|external)[[:space:]]' Stage1_Instances/THM-M-1566 --glob '*.lean'` | 1 | Expected no-match exit; no prohibited proof escape was found. |
| `git diff --quiet 48fb6596b..HEAD -- Stage1_Instances/THM-M-1566` | 0 | The decisive target sources are unchanged since the preceding slot27 blocker integration. |
| `python3 -m json.tool Stage1_Instances/THM-M-1566/proof-recheck-2026-07-15-head-350285c4-slot27.json` | 0 | The structured current-base blocker is valid JSON. |
| Inline Python assertions over identity, source hashes, negative evidence, state, and changed paths | 0 | Base identity, hashes, open-root flags, empty proof credit, `[ ]` state, and absent self-test agreed. |
| `git diff --no-index --check /dev/null` for each new artifact | 1, 1 | Expected added-file status with empty diagnostic output; no whitespace errors. |
| `git diff --check -- Stage1_Instances/THM-M-1566` | 0 | No whitespace errors in tracked owned-path changes. |
| Inline `git status --short` boundary assertion | 0 | Only the pre-existing `.lake` symlink and the two owned blocker artifacts are untracked. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no completion manifest. |

Exact isolated replay, run from the repository root:

```bash
set -euo pipefail
tmp=$(mktemp -d /tmp/thm-m-1566-proof-recheck-350285c4-slot27.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-1566/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-1566/ProofCountermodel.lean "$tmp/ProofCountermodel.lean"
lean=$(cd Formalizations/Lean && lake env which lean)
lean_path=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd "$tmp"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout --foreground 300s \
  "$lean" --trust=0 -t0 -R "$tmp" -o Statement.olean Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH=.:"$lean_path" timeout --foreground 300s \
  "$lean" --trust=0 -t0 -R "$tmp" ProofCountermodel.lean
```

## Failed Gate And Retry

The first failed gate is positive exact-root kernel closure at `M1566-ROOT`,
originating in the unconstrained `M1566-S-INTERFACE` and directly refuting
`M1566-T-EXISTENCE`. The predecessor graph lists existence and uniqueness as
the root cut, but proof work cannot close existence for the empty-solution API.

Resume only after an authorized statement revision replaces the unconstrained
universal API with a fixed source-faithful implementation or adds substantive
noncircular adequacy hypotheses. Accept a new exact expression fingerprint and
obligation-registry version, then rerun the statement, anchor-audit,
obligation-tree, and proof phases.

## Status Boundary

The proposed vector is `H1 / M5 / R3`; no authoritative state was changed.
This is current-base nonrelease blocker evidence, not a proof receipt or a
claim about the truth of the cited paper theorem. There is no accepted receipt,
provisional completion, master acceptance, or theorem-completion claim.
