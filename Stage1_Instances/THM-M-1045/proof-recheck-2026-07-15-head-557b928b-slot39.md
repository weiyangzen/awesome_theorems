# THM-M-1045 proof phase: current-base recheck

Item: `S56-M-1045-PROOF`

Intent: `prove`

Base revision: `557b928b377b386864527c9fb4831d45857837aa`

Base tree: `e677879a6eb4cb9d6795ba1bd78726af06ab9465`

Rechecked: `2026-07-15T07:55:48+08:00` (`Asia/Shanghai`)

## Verdict

`blocked`. No positive proof body can truthfully establish the exact frozen
`Stage1Instances.THM_M_1045.CameronMartinTarget`. The proof item remains `[ ]`, and no root
`.stage1-worker-selftest.json` is written.

`WienerData.paleyWienerIntegral` is constrained only by measurability, although the root quantifies
over every `WienerData` and requires the exact Radon-Nikodym density for that field. The existing
placeholder-free `ProofBlockerCurrent.lean` replaces only that field by the measurable constant-one
pairing. For `h = 0` and `g = 0`, the frozen target makes the self Radon-Nikodym derivative equal
`ENNReal.ofReal (Real.exp 1)` almost everywhere. `Measure.rnDeriv_self` makes it equal one, and
`1 < exp 1` yields a contradiction. Lean checks:

```text
Stage1Instances.THM_M_1045.no_target_of_wienerData
  (W : WienerData) : Not CameronMartinTarget
```

This result is conditional on a supplied `W : WienerData`. It refutes the overbroad Lean encoding
for every advertised datum; it neither constructs such a datum nor refutes the mathematical
Cameron-Martin theorem. Proving `WienerData` empty would only close the universal proposition
vacuously and would be a substituted theorem, so it is not eligible proof work.

The fail-closed vector proposed for master reconciliation is `[H1, M3, R3] -> [H1, M5, R3]`.
No predecessor authority or typed graph was rewritten by this proof worker.

## Failed Gate

Exact-target consistency fails at `M1045-S-DEFINITIONS`. The unconstrained pairing invalidates
`M1045-L-PALEY-WIENER`, blocking `M1045-B-DENSITY`, `M1045-T-ASSEMBLE`, and `M1045-ROOT`.
Separately, `S56-M-1045-OBLIGATION_TREE` is only worker-provisional `[_]`, so dependency-ordered
master acceptance is still outstanding.

Two additional statement risks need repair: the path measurable-space definition comaps `top`
rather than establishing the claimed cylinder/Borel sigma-algebra, and `timeMeasure` pushes all
real volume through `Real.toNNReal`, collapsing the negative half-line to zero rather than selecting
ordinary volume on `NNReal`.

Positive proof work can resume only after the statement constructs the Paley-Wiener integral or
adds source-justified, noncircular linearity, isometry, Gaussian-law, and compatibility laws; fixes
the path and time measure encodings; publishes a new exact fingerprint; and reruns the anchor audit
and a version-2 obligation registry with accepted typed graphs.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts was reused read-only. No Lake
update/build, dependency fetch/clone, or `.lake` mutation ran. Lean output was isolated under
`/tmp` and removed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 ordered targets at L0/rework-required passed. |
| `python3 scripts/stage1_target.py show THM-M-1045` | 0 | Rank 238, planned, legacy artifacts unaccepted, theorem incomplete. |
| `timeout 300 python3 -B Stage1_Instances/THM-M-1045/check_statement.py` | 0 | Exact fingerprint `e1b35bb7...5cea`; all four mutations distinguished. |
| `python3 -B Stage1_Instances/THM-M-1045/check_anchor_audit.py` | 0 | Target, support probes, inventory, and mathlib pin agreed. |
| `python3 -B Stage1_Instances/THM-M-1045/check_obligation_tree.py` | 0 | 15 obligations and 30 edges passed; root remains open at M3. |
| Isolated pinned Lean recipe below | 0 | Statement and blocker elaborated with `--trust=0 -t0`; blocker axioms are exactly `[propext, Classical.choice, Quot.sound]`. |
| Prohibited-construct scan below | 1 expected | No prohibited construct occurs in the checked blocker source. |
| `git diff --check -- Stage1_Instances/THM-M-1045` | 0 | No whitespace errors. |
| `git diff --no-index --check /dev/null <each new artifact>` | 1 expected | Each file differs from `/dev/null`; empty diagnostics mean no whitespace errors. |
| `python3 -m json.tool Stage1_Instances/THM-M-1045/proof-recheck-2026-07-15-head-557b928b-slot39.json` | 0 | Structured packet parsed. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No success manifest exists for this blocked phase. |

Exact narrow Lean recipe:

```bash
set -euo pipefail
repo="$PWD"
target="$repo/Stage1_Instances/THM-M-1045"
lean_root="$repo/Formalizations/Lean"
tmp=$(mktemp -d /tmp/thm-m-1045-proof-557b928b-slot39.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean_bin=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$target"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 "$lean_bin" \
  --trust=0 -t0 -o "$tmp/Statement.olean" Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 "$lean_bin" \
  --trust=0 -t0 ProofBlockerCurrent.lean
```

Exact prohibited-construct scan:

```bash
rg -n --pcre2 \
  '\b(?:sorry|admit|axiom)\b|sorryAx|unsafe|implemented_by|native_decide|^[[:space:]]*(?:constant|opaque|extern|external)[[:space:]]' \
  Stage1_Instances/THM-M-1045/ProofBlockerCurrent.lean
```

Pinned identities are Lean `4.29.0` commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib
commit/tree `8a178386ffc0f5fef0b77738bb5449d50efeea95` /
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

This is fresh nonrelease blocker evidence, not a proof receipt. It supplies no positive root proof
credit and makes no provisional-state, audit-completion, validation, release, theorem-completion,
or master-acceptance claim.
