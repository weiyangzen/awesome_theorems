# THM-M-1259 proof-phase recheck at base 47111bb1

Item: `S56-M-1259-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T20:09:59+08:00`

Base revision: `47111bb19566742918ac6be4a1a454070335b4a3`

Base tree: `bd0fbe7149aca8f36842e6acc8f1d40d3e28f4c0`

## Verdict

`blocked`. No consistent positive proof body can inhabit the exact frozen target. The existing
owned, placeholder-free declaration

```text
Stage1Instances.THM_M_1259.Counterexample.not_hormanderTarget :
  Not Stage1Instances.THM_M_1259.hormanderTarget
```

freshly kernel-checks against the pinned closure at trust level zero.

The target permits `n = r = 0` and quantifies over every measure. At the zero measure,
`IsSmoothDistribution` characterizes only the zero distribution. In zero-dimensional Euclidean
space, bracket generation and coefficient smoothness are automatic, the bundled zero operator maps
the nonzero evaluation distribution to zero, and that zero image is smooth. The target would
therefore make the nonzero evaluation distribution smooth relative to the zero measure, a
contradiction.

This refutes only the overbroad frozen Lean encoding, not Hormander's mathematical theorem. No
positive proof body or proof receipt was added, no obligation was closed, and the item remains
`[ ]`. Lifecycle remains `planned`; the predecessor registry records `[H2, M4, R3]`. The refuted
exact target warrants fail-closed `[H5, M5, R3]` classification under rev-5.6, but this proof worker
does not mutate predecessor or authoritative state. Audit and theorem completion are false.
`.stage1-worker-selftest.json` is deliberately absent because the assigned proof deliverable is not
genuinely complete.

## Failed Gate And Retry

The first failed gate is exact-target consistency. Rev-5.6 section 3.1 makes `H5` a terminal
classification and blocks ordinary theorem-proof execution. The statement receipt describes
Lebesgue measure while the elaborated root universally quantifies `mu : Measure (Euclidean n)`, and
its recorded statement hash is stale. Repair therefore requires reopening
`S56-M-1259-STATEMENT`, binding a source-audited reference measure and every source-required
nondegenerate condition, and accepting a new exact-expression fingerprint and obligation-registry
version. The anchor audit, obligation tree, and proof phase must then be rerun against that repaired
target.

Even after repair, the localized commutator estimate and regularity bootstrap need real Lean proof
bodies or an eligible immutable pinned proof. The checked
`expandedCore_composes_hormanderTarget` is only a conditional wrapper from the unproved
`ExpandedHypoellipticCore` premise.

Fifty-two proof-attempt/recheck/blocker JSON packets were tracked before this recheck, including
the canonical `proof-blocker.json`. This exceeds the five-tick split threshold. Splitting a positive
proof of a refuted proposition cannot help; scheduling must redirect to the statement dependency
rather than issue the same proof task again. The sole predecessor
`S56-M-1259-OBLIGATION_TREE` is also provisional `[_]`, rather than master-accepted `[x]`.

## Narrow Validation

All Lean and repository validation commands ran in this worker clone against the existing pinned
Lake artifacts. No `lake update`, `lake build`, dependency clone/fetch, network discovery, or
`.lake` mutation was performed. The automation-provided untracked `Formalizations/Lean/.lake`
symlink makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1259` | 0 | Rank 161; lifecycle `planned`; lane `hard_mathlib_anchor_and_wrapper`; theorem incomplete. |
| isolated pinned `lake env lean --trust=0 -t0` replay | 0 | `Statement.lean` and `Counterexample.lean` elaborated; exits were `0,0`; the refutation's axioms are `[propext, Classical.choice, Quot.sound]`. |
| prohibited-construct scan over `Statement.lean` and `Counterexample.lean` | 1 | Expected ripgrep no-match exit; no prohibited construct occurs. |
| pinned toolchain and mathlib identity checks | 0 | Lean 4.29.0 commit `98dc76e3...6740`; Lake `5.0.0-src+98dc76e`; mathlib commit `8a178386...ea95`, tree `bdc39a31...c2b`, clean. |
| structured artifact and DAG-state checks | 0 | The registry and graphs parse; predecessor is `[_]`; assigned proof item is `[ ]`. |
| frozen-input diff from `c45f3c70` | 0 | All five proof inputs are unchanged since `Counterexample.lean` was integrated. |
| JSON parse, blocker-invariant assertions, and no-index whitespace checks | 0 | The packet parses, preserves the fail-closed boundary, and both new artifacts have no whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest is absent because the proof phase is blocked. |

Exact isolated replay recipe:

```bash
set -u
repo=$PWD
target="$repo/Stage1_Instances/THM-M-1259"
tmp=$(mktemp -d /tmp/thm-m-1259-slot17.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean_path=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
(
  cd Formalizations/Lean
  LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 600 lake env lean --trust=0 -t0 \
    -R "$target" -o "$tmp/Statement.olean" "$target/Statement.lean"
)
(
  cd Formalizations/Lean
  LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 600 lake env lean --trust=0 -t0 \
    -R "$target" "$target/Counterexample.lean"
)
```

The Lean replay ran from `2026-07-15T20:08:34+08:00` through
`2026-07-15T20:08:56+08:00`. Its statement and counterexample output SHA-256 values were,
respectively, `a65df923b3d080172ecece147795744282d5c908b6100d82cd24647762cabac6` and
`aa64bb5770bb5af2aee91a37c8eefca3ae90581899ef29779a8986b5110d1dd2`. The temporary
`Statement.olean` hash was
`af3e33999cd4eedfd8a60474a4de35cee950f926809bb4712b3a6931d2d5130d`. The axiom report for
`not_hormanderTarget` is exactly:

```text
[propext, Classical.choice, Quot.sound]
```

Scoped prohibited-construct scan:

```bash
rg -n --pcre2 '\b(?:sorry|admit|axiom)\b|sorryAx|unsafe|implemented_by|native_decide|\bexternal\b' \
  Stage1_Instances/THM-M-1259/Statement.lean \
  Stage1_Instances/THM-M-1259/Counterexample.lean
```

The scan returned no matches. Frozen source SHA-256 identities are:

| Input | SHA-256 |
|---|---|
| `Statement.lean` | `8258728ff71980a4431fb47213487c8d7655c64d0dd0f3ab2e9b058f8a95c0c7` |
| `Counterexample.lean` | `91e1610bf3fab308b7d8025415eae1db9e2d284a7e06c415baf3be47bfa74ad1` |
| `obligation_registry.json` | `2eb6b3db5d79dbed5b9f22dd467cfb964b15a3441927919e635670715342d1a0` |
| `typed_graphs.json` | `d48d5c6724a1716e82685ad535cfc8dcc1df6f3f75fc5fe691d6e13fcab7259b` |
| `anchor_audit.json` | `ac668a1aee1297b698c01d328b809eff8094acac21a955763e6ac5ab92a9434d` |
| `source_statement_crosswalk.md` | `62c46ee2dac6429821c45dbba90c73f447240c81956f90c38cd53bfaea497dff` |
| `statement_receipt.md` | `21992f2e11bdf4aa52f4c1bf19cb64d158bca41521b0ca7071a6e00b22c6a8a1` |
| `lean-toolchain` | `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` |
| `lake-manifest.json` | `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81` |

The pre-existing `.lake` symlink target is the scheduler's canonical pinned
`Formalizations/Lean/.lake`. Its exact absolute link text is retained only in the private worker
run, not in this public artifact. SHA-256 of the exact stdout from `readlink
Formalizations/Lean/.lake` (including its trailing newline) is
`e7d8a6bce8b934a5b0dc162324c830c4f26e1146c65bb31e8063491a3f47bfcc`. The JSON packet records
this validation action's owner, attestor, freshness, review, invalidation, support, revocation, and
incident policy. The two newly written blocker artifacts are themselves the current patch output;
their hashes are intentionally not embedded recursively inside their own contents.

The JSON companion binds the exact blocker, inputs, environment, commands, retry condition, and
changed paths. This packet is durable current-base blocker evidence only. It is not a canonical
validation or proof receipt, does not satisfy `S56-M-1259-PROOF`, and claims no scheduler transition
or master acceptance. Packet structure and whitespace validation completed after creation.
