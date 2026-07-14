# THM-M-1259 proof-phase recheck at base 15d20dda

Item: `S56-M-1259-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T06:10:11+08:00`

Base revision: `15d20dda8662e4144f32be899edc174f7a431574`

Base tree: `b39eec687e4f172c4ce04e08a255e593a428cf95`

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
positive proof body or receipt was added, no obligation was closed, and the item remains `[ ]`.
Lifecycle remains `planned`; the predecessor registry records `[H2, M4, R3]`. The refuted exact
target warrants fail-closed `[H5, M5, R3]` classification under rev-5.6, but this proof worker does
not mutate predecessor or authoritative state. Audit and theorem completion are false.
`.stage1-worker-selftest.json` is deliberately absent because the assigned proof phase is not
complete.

## Failed gate and retry

The first failed gate is exact-target consistency. Rev-5.6 section 3.1 makes `H5` a terminal
classification and blocks ordinary theorem-proof execution. The statement receipt also describes
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

Sixteen earlier proof-attempt/recheck JSON packets are tracked. This exceeds the five-tick split
threshold. Splitting a positive proof of a refuted proposition cannot help; scheduling must redirect
to the statement dependency rather than issue the same proof task again.

## Narrow validation

All Lean and repository validation commands ran in this worker clone against the existing pinned
Lake artifacts. No `lake update`, `lake build`, dependency clone/fetch, network discovery, or
`.lake` mutation was performed. The automation-provided untracked
`Formalizations/Lean/.lake` symlink makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1259` | 0 | Rank 161; lifecycle `planned`; lane `hard_mathlib_anchor_and_wrapper`; theorem incomplete. |
| isolated pinned `lake env lean --trust=0 -t0` replay | 0 | `Statement.lean` and `Counterexample.lean` both elaborated; exits were `0,0`. |
| prohibited-construct scan over `Statement.lean` and `Counterexample.lean` | 1 | Expected ripgrep no-match exit; no prohibited construct occurs. |
| `cd Formalizations/Lean && lake env lean --version && lake --version && git -C .lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | Lean 4.29.0 commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake `5.0.0-src+98dc76e`; mathlib commit `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. |
| `git diff --quiet 11a448c9..HEAD --` the five frozen proof inputs | 0 | `Statement.lean`, `Counterexample.lean`, registry, graphs, and anchor audit are unchanged since the preceding integrated recheck. |

Exact isolated replay recipe:

```bash
set -u
tmp=$(mktemp -d /tmp/thm-m-1259-slot35.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd Formalizations/Lean && lake env which lean)
lean_path=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 600 "$lean" --trust=0 -t0 \
  -R Stage1_Instances/THM-M-1259 -o "$tmp/Statement.olean" \
  Stage1_Instances/THM-M-1259/Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 600 "$lean" --trust=0 -t0 \
  -R Stage1_Instances/THM-M-1259 \
  Stage1_Instances/THM-M-1259/Counterexample.lean
```

The replay ran from `2026-07-15T06:09:26+08:00` through
`2026-07-15T06:10:11+08:00`. Its statement and counterexample output SHA-256 values were,
respectively, `a65df923b3d080172ecece147795744282d5c908b6100d82cd24647762cabac6` and
`aa64bb5770bb5af2aee91a37c8eefca3ae90581899ef29779a8986b5110d1dd2`. The integrated axiom report
for `not_hormanderTarget` is exactly:

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

The JSON companion binds the exact blocker, inputs, environment, commands, retry condition, and
changed paths. This packet is durable current-base blocker evidence only. It is not a proof receipt,
does not satisfy `S56-M-1259-PROOF`, and claims no scheduler transition or master acceptance.
