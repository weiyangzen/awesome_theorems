# THM-M-1259 proof-phase recheck at base `46320e01`

Item: `S56-M-1259-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T14:01:34+08:00`

Base revision: `46320e01d1897482417e7b0d03a15a5b77ae5275`

Base tree: `2260ad94d18a6662ffc00f47b8955ae3a2a18184`

## Verdict

`blocked`. No consistent positive proof body can inhabit the exact frozen target. The existing
owned, placeholder-free declaration

```text
Stage1Instances.THM_M_1259.Counterexample.not_hormanderTarget :
  Not Stage1Instances.THM_M_1259.hormanderTarget
```

kernel-checks at trust level zero against the existing pinned mathlib artifacts.

The target permits `n = r = 0` and quantifies over every measure. At the zero measure,
`IsSmoothDistribution` characterizes only the zero distribution. In zero-dimensional Euclidean
space, bracket generation and coefficient smoothness are automatic, the bundled zero operator maps
the nonzero evaluation distribution to zero, and that zero image is smooth. The target would make
the nonzero evaluation distribution smooth relative to the zero measure, a contradiction.

This refutes only the overbroad frozen Lean encoding, not Hormander's mathematical theorem. No
positive proof body or proof receipt was added, no obligation was closed, and the item remains
`[ ]`. Lifecycle remains `planned`; the predecessor registry records `[H2, M4, R3]`. The checked
refutation warrants fail-closed `[H5, M5, R3]` classification under rev-5.6, but this proof worker
does not mutate predecessor or authoritative state. Audit and theorem completion are false.
Because the assigned proof deliverable is not genuinely complete,
`.stage1-worker-selftest.json` is deliberately absent.

## Failed Gate And Retry

The first failed gate is exact-target consistency under rev-5.6 sections 2, 3.1, and 5.1: the
canonical Lean proposition is kernel-refuted. Section 3.1 makes `H5` terminal and blocks ordinary
theorem-proof execution. The statement receipt also describes Lebesgue measure while the elaborated
root universally quantifies `mu : Measure (Euclidean n)`, and its recorded statement hash is stale.

Repair requires reopening `S56-M-1259-STATEMENT`, binding a source-audited reference measure and
every source-required nondegenerate condition, and accepting a new exact-expression fingerprint and
obligation-registry version. The anchor audit, obligation tree, and proof phase must then be rerun
against that repaired target. Even after repair, the localized commutator estimate and regularity
bootstrap need real Lean proof bodies or an eligible immutable pinned proof. The checked
`expandedCore_composes_hormanderTarget` is only a conditional wrapper from the unproved
`ExpandedHypoellipticCore` premise.

Thirty-one earlier proof-attempt/recheck/blocker JSON packets were tracked before this recheck. The
five-unresolved-tick threshold is far exceeded. Splitting a positive proof of a refuted proposition
cannot help; scheduling must redirect to the statement dependency rather than issue another
unchanged proof task. The sole predecessor is also only provisional `[_]`, not master-accepted
`[x]`; this independently prevents proof-node acceptance.

## Narrow Validation

All checks ran in this worker clone against existing pinned artifacts. No `lake update`, `lake
build`, dependency clone/fetch, network discovery, or `.lake` mutation was performed. The
automation-provided untracked `Formalizations/Lean/.lake` symlink makes this nonrelease evidence.

The top-level Lake project currently cannot resolve the existing `flt-regular` checkout's `HEAD`.
That artifact was recorded as a blocker rather than repaired. The successful narrow validation used
`lake env lean` from the healthy pinned mathlib subproject and explicitly supplied only existing
compiled dependency paths.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1259` | 0 | Rank 161; lifecycle `planned`; lane `hard_mathlib_anchor_and_wrapper`; theorem incomplete. |
| `cd Formalizations/Lean && timeout 30 lake env lean --version` | 1 | Could not resolve the existing `flt-regular` `HEAD`; no dependency mutation was attempted. |
| Pinned-mathlib `lake env lean --trust=0 -t0` replay below | 0 | `Statement.lean` and `Counterexample.lean` elaborated; exits were `0,0`; `not_hormanderTarget` reports `[propext, Classical.choice, Quot.sound]`. |
| Scoped prohibited-construct scan over `Statement.lean` and `Counterexample.lean` | 1 | Expected ripgrep no-match exit; no prohibited construct occurs. |
| `cd Formalizations/Lean/.lake/packages/mathlib && lake env lean --version && lake --version && lake env which lean && git rev-parse HEAD HEAD^{tree}` | 0 | Lean 4.29.0 commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake `5.0.0-src+98dc76e`; mathlib commit `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; pinned mathlib worktree clean. |
| `git diff --quiet c45f3c70..HEAD --` the five frozen proof inputs | 0 | `Statement.lean`, `Counterexample.lean`, registry, graphs, and anchor audit are unchanged since the refutation was first integrated. |
| `python3 -m json.tool` plus blocker invariants and `git diff --no-index --check` on each new file | 0 | JSON parsed, blocker invariants held, and neither packet file produced a whitespace diagnostic. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is absent because the proof phase is blocked. |

Exact isolated replay recipe:

```bash
set -u
repo=$PWD
base="$repo/Formalizations/Lean/.lake/packages"
tmp=$(mktemp -d /tmp/thm-m-1259-slot25-current.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lp="$base/mathlib/.lake/build/lib/lean"
for p in LeanSearchClient Qq aesop batteries importGraph plausible proofwidgets; do
  lp="$lp:$base/$p/.lake/build/lib/lean"
done
(
  cd "$base/mathlib"
  LEAN_NUM_THREADS=1 LEAN_PATH="$lp" timeout 600 lake env lean --trust=0 -t0 \
    -R "$repo/Stage1_Instances/THM-M-1259" \
    -o "$tmp/Statement.olean" \
    "$repo/Stage1_Instances/THM-M-1259/Statement.lean"
)
(
  cd "$base/mathlib"
  LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lp" timeout 600 lake env lean --trust=0 -t0 \
    -R "$repo/Stage1_Instances/THM-M-1259" \
    "$repo/Stage1_Instances/THM-M-1259/Counterexample.lean"
)
```

The replay ran from `2026-07-15T13:59:15+08:00` through
`2026-07-15T13:59:24+08:00`. Its statement and counterexample output SHA-256 values were,
respectively, `a65df923b3d080172ecece147795744282d5c908b6100d82cd24647762cabac6`
and `aa64bb5770bb5af2aee91a37c8eefca3ae90581899ef29779a8986b5110d1dd2`.
The temporary statement object SHA-256 was
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

The JSON companion binds the exact blocker, inputs, environment, commands, retry condition, and
changed paths. This packet is durable current-base blocker evidence only. It is not a proof receipt,
does not satisfy `S56-M-1259-PROOF`, and claims no scheduler transition or master acceptance.
