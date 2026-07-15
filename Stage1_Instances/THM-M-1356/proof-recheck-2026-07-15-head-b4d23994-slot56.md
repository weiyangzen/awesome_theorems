# THM-M-1356 proof-phase blocker at `b4d23994`

Item: `S56-M-1356-PROOF`

Intent: `prove`

Recorded: `2026-07-15T20:04:03+08:00` (`Asia/Shanghai`)

Base revision: `b4d239943a37f6c25c377bbfd85c0e1ec7f4acaa`

Base tree: `5f13e0e86bde3bcaaef38b979819490c648166e3`

## Verdict

`blocked`. No placeholder-free Lean body or immutable compatible import was
found for the exact arbitrary-degree Routh-Hurwitz target
`Stage1Instances.THM_M_1356.RouthHurwitzTarget`. The proof item remains `[ ]`,
the lifecycle remains `planned`, and the frozen root remains `[H1, M3, R4]`.
Audit completion and theorem completion are false.

The existing `Proof.lean` contains genuine checked work, but only for degree
one. It proves the coefficient adapter, the unique-root characterization, the
unique Hurwitz-minor formula, and their exact equivalence when `n = 1`. The
canonical target quantifies over every positive degree, so this specialization
does not close a frozen arbitrary-degree obligation and cannot satisfy the
assigned phase. The declarations in `ObligationTree.lean` are also conditional:
`root_of_directions` takes both complete implications as hypotheses and creates
neither of them.

The frozen registry has `50` obligations, of which `45` are machine-required;
all `45` required terminal body IDs remain null. The minimal open root cut is:

```text
M1356-B-STABLE-TO-MINORS
M1356-B-MINORS-TO-STABLE
```

The first failed gate is exact all-degree proof-body availability upstream of
both cut nodes. The frozen route still needs the alternating even/odd
polynomials, signed Euclidean/Sturm and Cauchy-index machinery, Hermite
hodograph root counting, regular plus nonregular Routh cases, no-pivot Hurwitz
block elimination, and the leading-minor product identity. Pinned mathlib and
`flt-regular` contain useful substrate but no Routh-Hurwitz, Hermite-Biehler, or
Hurwitz-matrix criterion terminal.

Supplemental read-only Sourcegraph searches for `RouthHurwitz`,
`routh_hurwitz`, `HurwitzMatrix`, `HermiteBiehler`, and `"Routh-Hurwitz"`
returned complete HTTP 200 streams with zero Lean matches. Three clean GitHub
repository-search responses also reported zero repositories; two more were
rate-limited and receive no negative-search credit. The immutable
near-candidate previously audited as
`PerAlexandersson/RealRooted@634a949d31683785b4181efbba6faff31e81e006`
does not unblock the target. Its root-critical `HermiteBiehler.lean`,
`HurwitzMatrix.lean`, and `VeroneseSection.lean` declarations contain explicit
`sorry` at the audited lines. It also states a different weak infinite
total-nonnegativity/right-half-plane criterion, not the frozen finite
strict-leading-minor equivalence. It receives no proof or integration credit.

## Scheduler Handoff

This proof root now has three integrated unresolved proof executions: the
degree-one partial implementation at base `51c2828e`, the blocker recheck at
base `a60b47b4`, and this current-base recheck. The authoritative DAG still
records `attempts: 0` and `children: []`; this worker may not edit it. A future
retry should target a frozen implementation leaf rather than repeat the whole
root. If the five-tick threshold is reached, the scheduler must split the item
as required by rev-5.6.

The direct prerequisite `S56-M-1356-OBLIGATION_TREE` is only worker-provisional
`[_]`, not master-accepted `[x]`. Its checker hard-pins base `431e77db...` and
therefore rejects current HEAD at the freshness assertion. This is a stale
predecessor receipt/checker boundary, not a Lean elaboration failure, and it
independently prevents master acceptance of this proof node on the present
base.

## Validation

All validation commands ran inside the worker clone. The pre-existing untracked
`Formalizations/Lean/.lake` symlink points to the scheduler's canonical pinned
artifacts and was reused read-only. Temporary Lean objects were written under
`/tmp` and removed. No `lake update`, `lake build`, dependency clone/fetch,
checkout, or `.lake` mutation was performed. One delegated audit worker used
the network read-only for the supplemental Sourcegraph/GitHub metadata searches
above; no retrieved source or dependency was persisted or credited. This is dirty
nonrelease evidence because that symlink is untracked.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All `15` assurance groups and `1546` uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | `1546` unique targets, ranks `1..1546`, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1356` | 0 | Rank `966`; planned; lane `hard_statement_first_partial_verification`; theorem incomplete. |
| `python3 -B Stage1_Instances/THM-M-1356/check_statement.py` | 0 | Exact expression SHA-256 `7901eb74...98bf`; four mutations killed; each direct-import deletion failed; pinned mathlib revision agreed. |
| `python3 -B Stage1_Instances/THM-M-1356/check_anchor_audit.py` | 0 | Exact local statement only; pinned mathlib topic inventory empty; external inventory empty; root `M3`. |
| `python3 -B Stage1_Instances/THM-M-1356/check_obligation_tree.py` | 1 | Failed only at its stale hard-pinned HEAD assertion (`431e77db...` versus this base), before substantive registry checks. |
| Isolated trust-zero `lake env lean` replay below | 0 | `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` elaborated; all printed local bodies report exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| Exact-topic `rg` over all `9040` Lean sources in pinned mathlib and `flt-regular` | 1 | Expected no-match for Routh-Hurwitz, Hermite-Biehler, Hurwitz matrix, determinant, or minor theorem names. |
| Same exact-topic `rg` over repo-local Lean outside this dossier | 1 | Expected no-match; no duplicate exact implementation exists. |
| Sourcegraph global Lean searches for five exact aliases | 0 | Five complete HTTP 200 streams, `matchCount: 0`, no skipped repositories; supplemental discovery only. |
| GitHub repository searches for five aliases | mixed | Three HTTP 200 responses had `total_count: 0`; two HTTP 403 responses were inconclusive and receive no negative-search credit. |
| Parser-oriented prohibited-device scan of the three checked Lean modules | 0 | Three files checked; zero `sorry`, `admit`, `sorryAx`, bodyless/custom axiom, unsafe/oracle, `native_decide`, `implemented_by`, or `run_tac` matches outside comments and strings. |
| Pinned package revision/status checks | 0 | mathlib `8a178386...ea95` / tree `bdc39a31...d8b`; flt-regular `56161b6e...ea27` / tree `32c9eace...893`; tracked package sources clean. |
| `git diff --quiet 51c2828e..HEAD --` frozen proof inputs and dependency pins | 0 | Statement, composition, registry, graphs, anchor inventory, validation specs, toolchain, and manifest are unchanged since the obligation-tree/partial-proof base. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

The narrow Lean replay was:

```bash
set -euo pipefail
repo=$PWD
target=$repo/Stage1_Instances/THM-M-1356
tmp=$(mktemp -d /tmp/s56m1356-b4d23994-slot56.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$target/Statement.lean" "$target/ObligationTree.lean" \
  "$target/Proof.lean" "$tmp/"
cd "$repo/Formalizations/Lean"
base_path=$(timeout --foreground --kill-after=5s 180s \
  lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 timeout --foreground --kill-after=5s 600s \
  lake env lean --trust=0 -t0 --root="$tmp" \
    -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_PATH="$tmp:$base_path" LEAN_NUM_THREADS=1 \
  timeout --foreground --kill-after=5s 600s \
    lake env lean --trust=0 -t0 --root="$tmp" \
      -o "$tmp/ObligationTree.olean" "$tmp/ObligationTree.lean"
LEAN_PATH="$tmp:$base_path" LEAN_NUM_THREADS=1 \
  timeout --foreground --kill-after=5s 600s \
    lake env lean --trust=0 -t0 --root="$tmp" \
      -o "$tmp/Proof.olean" "$tmp/Proof.lean"
sha256sum "$tmp/Statement.olean" "$tmp/ObligationTree.olean" \
  "$tmp/Proof.olean"
```

Replay output hashes:

| Output | SHA-256 |
|---|---|
| `Statement.olean` | `f847976776294835e9bb566c18d105573dd5494214c2ebb9b42dcd01d0fb3cf4` |
| `ObligationTree.olean` | `4b3dc2ef06d9f678ce5505f1a4e40c2b80dd1deb4f61d7651d4ee6d816021e4d` |
| `Proof.olean` | `dbd13ed0e7e38a5d548ba82675fd586ec9371180a772dda7f1adca99b3be66cf` |

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake
`5.0.0-src+98dc76e`; mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; flt-regular
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`, tree
`32c9eace926573a9981787ae97643e520353c893`.

## Retry Condition

Resume only a dependency-legal frozen child when a real placeholder-free body
is ready. A viable route must close the alternating/Sturm/Hermite/Routh engine
and the Hurwitz-minor product engine, derive both exact direction packages, and
compose them to the unchanged all-degree root. Alternatively, an immutable,
license-compatible exact Lean 4 terminal may be integrated into the pinned
closure after exact-type, trust, dependency, provenance, and placeholder gates
pass.

This artifact is a current-base proof blocker, not a proof receipt. It changes
no obligation, graph, debt vector, lifecycle, scheduler state, or accepted
receipt and claims no proof-phase completion, audit completion, theorem
completion, validation, release, or master acceptance. Because the assigned
phase is not genuinely complete, `.stage1-worker-selftest.json` is deliberately
absent.
