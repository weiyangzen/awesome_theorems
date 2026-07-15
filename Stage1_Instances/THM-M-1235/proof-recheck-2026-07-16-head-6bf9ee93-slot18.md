# THM-M-1235 proof-phase recheck at `6bf9ee93`

Item: `S56-M-1235-PROOF`

Intent: `prove`

Recheck date: `2026-07-16T04:53:59+08:00`

Base revision: `6bf9ee93a322e7d25cf9249226222095f95d1cff`

Base tree: `24acf86e69ab2e6fca9480c6269b6429874ba295`

## Verdict

`blocked`. No legal positive proof body can inhabit the exact frozen target. Two independent,
tracked, placeholder-free declarations freshly elaborate at Lean trust level zero:

```text
Stage1Instances.THMM1235.not_wolibnerGlobalExistenceAndUniqueness :
  Not Stage1Instances.THMM1235.WolibnerGlobalExistenceAndUniqueness

Stage1Instances.THMM1235.independently_not_wolibnerGlobalExistenceAndUniqueness :
  Not Stage1Instances.THMM1235.WolibnerGlobalExistenceAndUniqueness
```

`Motion.conditionI_areaPreservingSelfHomeomorphism` through
`Motion.conditionVIII_continuousSpatialDerivatives` are freely chosen values of type `Prop`. They
are not proofs of predicates constraining the five motion functions. The primary refutation changes
an alleged unique motion's `velocityX` to `velocityX + 1`; the independent refutation changes its
`pressure` to `pressure + 1`. Both structure updates preserve the frozen `Motion` type. `SameMotion`
would equate the changed function to the original, but evaluation at `(0, 0), 0` reduces that
equality to the contradiction `x + 1 = x`. Concrete source data discharge every explicit premise
because the domain and regularity fields are likewise freely chosen propositions.

This refutes the frozen formal encoding, not Wolibner's mathematical theorem. Proving a corrected,
weaker, specialized, or conditional proposition in this item would be forbidden target substitution.
The conditional `root_of_existence_and_uniqueness` in `ObligationTree.lean` assumes the substantive
existence and uniqueness packages and therefore supplies no positive root proof credit. The pinned
candidate audit still identifies no positive exact Wolibner proof anchor.

The item remains `[ ]`. No proof receipt, closed obligation, accepted state, audit completion,
theorem completion, validation completion, or release is claimed. No
`.stage1-worker-selftest.json` is written because the requested positive proof phase is not
genuinely complete or self-tested. The frozen graph remains `[H3, M3, R4]`; this run proposes only
an `H5/M5/R4` exact-target diagnosis for master reconciliation.

## Dependency Context

The required `dependency-reuse-ledger.json` now records schema
`stage1-dependency-reuse-ledger/1.1`, graph digest
`73e99d2276c8ba9fec8f89ed41b712308d7f5667e95ba8185e49f1f5bfd40eca`, target context digest
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`, and this base revision.
The exact v2 node has zero direct hard parents, transitive hard ancestors, incoming hard edges, reuse
hints, or shared groups. Consequently its inspections, decisions, and unresolved compatibility
lists are truthfully empty. This is a successfully audited empty context, not a mathematical
independence claim and not transferred proof credit.

## Failed Gate And Retry

The first failed gate is rev-5.6 section 5.1 exact-target consistency at
`M1235-S-DEFINITIONS`. Reopen `S56-M-1235-STATEMENT`; replace semantic proposition placeholders with
actual predicates of the five functions and make `Motion` carry proofs of conditions `(I)`-`(VIII)`.
Re-audit uniqueness over the source domain and `0 <= t <= T` against the primary source. Then
publish a versioned re-freeze of the canonical expression fingerprint, source crosswalk, obligation
registry, typed graphs, and dependent evidence before proof execution resumes.

The predecessor `S56-M-1235-OBLIGATION_TREE` is still worker-provisional (`[_]`) rather than
master-accepted, so proof acceptance is independently dependency-blocked. Later gates also remain
open: `validation-specs.json` uses legacy shell-command strings rather than the structured recipe
schema required by rev-5.6 section 10.5, and the intake README, crosswalk, and local task DAG have
not been reconciled with the later source pinpoints and checked refutation. None changes the earlier
truth blocker.

Fifty-seven earlier structured proof-recheck JSON packets were already present while the
authoritative DAG still records `attempts=0` and no children. The master/scheduler should reconcile
the execution history and reopen or split the invalid upstream statement work under section 10.2
instead of issuing another identical proof-only retry. This worker did not edit authoritative state.

## Validation

All checks ran inside this worker clone and reused the automation-provided untracked
`Formalizations/Lean/.lake` symlink read-only. No `lake update`, `lake build`, dependency
clone/fetch/checkout, network access, or `.lake` mutation was performed. Temporary Lean sources and
objects were removed. The shared dependency-cache symlink makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 1 | Its nested v2 validator reports that the checked-in theorem DAG differs from fresh deterministic generation after the mandatory ledger is present. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 1 | Same deterministic-generation failure; the checked graph itself still hashes to the exact assigned digest `73e99d22...`. |
| `python3 scripts/stage1_execution_cron.py --validate-only --workers 0` | 1 | Stops at the same v2 validator failure without modifying scheduler state. |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1235` | 0 | Rank 159; lifecycle `planned`; baseline `L0/rework_required`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1235/check_statement.py` | 0 | Expression digest `77aec2f5...` and pins matched; all four structural mutations were killed. |
| `python3 Stage1_Instances/THM-M-1235/check_obligation_tree.py` | 0 | 15 obligations and 37 typed edges passed; denominator `9e0bff35...`; root open M3, existence and uniqueness M4. |
| Schema-1.1 ledger validation and independent v2 closure reproduction | 0 | Base/graph/context identities and the complete empty context passed. |
| Isolated pinned-Lean replay below | 0 | The exact statement and both tracked negative modules elaborated with `--trust=0 -t0`; all four negative axiom reports were `[propext, Classical.choice, Quot.sound]`. |
| Prohibited-construct scans over both negative modules | 0 | Both scans produced the required no-match result; neither module contains `sorry`, `admit`, bodyless declarations, unsafe/oracle constructs, or `native_decide`. |
| Toolchain, dependency revision/tree, and frozen-input hash checks | 0 | Lean 4.29.0 at `98dc76e3...`; mathlib `8a178386...`; flt-regular `56161b6e...`; all recorded hashes matched and both dependency worktrees were clean. |
| Existing-packet boundary audit | 0 | All 57 predecessor JSON packets remain `[ ]`, root-open, and theorem-incomplete. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No completion self-test manifest exists for this blocked proof phase. |

Exact successful Lean recipe, run from the repository root:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-1235
tmp=$(mktemp -d /tmp/thm-m-1235-proof-6bf9ee93-slot18.XXXXXX)
trap 'rm -rf "$tmp"' EXIT HUP INT TERM
cp "$target/Statement.lean" "$tmp/Statement.lean"
cp "$target/Proof.lean" "$tmp/Proof.lean"
cp "$target/IndependentRefutation.lean" "$tmp/IndependentRefutation.lean"
cd "$lean_root"
base_path=$(env -u LEAN_PATH timeout --foreground --kill-after=5s 120 \
  lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$base_path" timeout --foreground --kill-after=10s 600 \
  lake env lean --trust=0 -t0 --root="$tmp" -o "$tmp/Statement.olean" \
  "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_path" timeout --foreground --kill-after=10s 600 \
  lake env lean --trust=0 -t0 --root="$tmp" -o "$tmp/Proof.olean" "$tmp/Proof.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_path" timeout --foreground --kill-after=10s 600 \
  lake env lean --trust=0 -t0 --root="$tmp" -o "$tmp/IndependentRefutation.olean" \
  "$tmp/IndependentRefutation.lean"
sha256sum "$tmp/Statement.olean" "$tmp/Proof.olean" \
  "$tmp/IndependentRefutation.olean"
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake `5.0.0-src+98dc76e`; mathlib revision/tree
`8a178386ffc0f5fef0b77738bb5449d50efeea95` /
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`; flt-regular revision/tree
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` /
`32c9eace926573a9981787ae97643e520353c893`.

Temporary object digests were
`cbb0b49360973c6a3e9e45d45965f51efbadf0914f10448c5e68e2dd3654497d` for
`Statement.olean`,
`3af4a429ebac82bfe937a5acd5039cfe0984cead67492d0f9b46d41f3e761169` for
`Proof.olean`, and
`a06c3ab25b0a901364d85a3ac1b2993452810f88edf013f3458545d6622b4b5d` for
`IndependentRefutation.olean`.

The structural failure after ledger creation is a separate repository validator defect. The v2
blueprint says the ledger is excluded from theorem-DAG discovery, and the generator excludes it from
shared-group discovery, but `inventory()` still includes every JSON file. The resulting fresh graph
therefore sees the required ledger and differs from the checked graph. This is later than the
exact-target truth failure and does not change the first failed proof gate.

## Status Boundary

This current-base artifact is negative, nonrelease blocker evidence. It does not satisfy
`S56-M-1235-PROOF`, propose `[_]` or `[x]`, or support audit or theorem completion. The retry must
begin with statement correction and a versioned re-freeze; repeating proof search against this
exact encoding cannot close the item.
