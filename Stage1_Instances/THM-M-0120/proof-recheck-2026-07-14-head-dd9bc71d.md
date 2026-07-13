# THM-M-0120 proof-phase recheck at current base

Item: `S56-M-0120-PROOF`  
Intent: `prove`  
Recheck date: 2026-07-14 (Asia/Shanghai)  
Base revision: `dd9bc71d70586d022d87833d780fbe15959b89b0`  
Base tree: `d096d4ef8804532c9165b75d369f49b7b74945d8`

## Verdict

`blocked`. No truthful positive proof body exists for the exact frozen proposition. The existing
placeholder-free declaration

```text
Stage1Instances.THMM0120.Proof.not_moriConeTheoremTarget :
  Not (Stage1Instances.THMM0120.MoriConeTheoremTarget.{0, 0, 0, 0})
```

kernel-checks at trust level zero. Its countermodel makes every explicit geometric proposition
hypothesis true for a proper identity morphism, while the statement leaves the numerical data
independent of those hypotheses: `N1 = Real`, `moriCone = {-1}`, `canonicalPairing = LinearMap.id`,
and `RationalCurve = Empty`. Applying the required decomposition equivalence to `-1` yields an
element `z0` of the nonnegative part with both `z0 = -1` and `0 <= z0`, a contradiction.

This refutes the current formal encoding, not the mathematical Mori cone theorem. A repaired,
narrower, or circularly strengthened proposition cannot be substituted for the assigned target.
The item remains `[ ]`; no positive proof body, provisional worker receipt, audit completion,
theorem completion, release, or master acceptance is claimed. The frozen predecessor registry
still records the root at `M3` and substantive geometric packages as open; this checked
countermodel establishes an `M5` exact-target mismatch without rewriting predecessor state.

## Failed Gate And Retry

The first failed gate is exact-target consistency. `S56-M-0120-STATEMENT` must be reopened and its
stand-ins replaced by intrinsic definitions or noncircular laws connecting the projective klt pair
to its numerical curve space, effective cone, canonical pairing, rational curves, and contractions.
Assuming `Conclusion`, its decomposition branch, or another required output package would be
circular. Positive proof work may resume only after a repaired target receives a new accepted
expression fingerprint and obligation-registry version, followed by a fresh anchor audit and proof
execution.

## Scoped Validation

All successful checks ran in this worker clone using the existing pinned Lean artifacts. No update,
build, clone, fetch, or dependency mutation was performed. The automation-provided untracked
`Formalizations/Lean/.lake` symlink makes this dirty, nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0120` | 0 | rank 39; planned lifecycle; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| `python3 Stage1_Instances/THM-M-0120/check_obligation_tree.py` | 0 | 25 obligations and 62 typed edges passed; denominator `69152b16...63081b1`; root remains `M3`; substantive packages remain open |
| `python3 Stage1_Instances/THM-M-0120/check_anchor_audit.py` | 0 | immutable local candidates, clean pinned mathlib, eight Lean probes, and the `M3` boundary agree |
| isolated pinned `lake env lean -R "$tmp" -t0` recheck | 0 | independently reran the exact statement and countermodel before the shared optional-package checkout changed; axiom report `[propext, Classical.choice, Quot.sound]` |
| isolated direct `lean --trust=0 -t0` recipe below | 0 | repeated the same exact statement and countermodel check from the pinned artifact directories after that external change; same axiom report |
| `/home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `test -z "$(git -C Formalizations/Lean/.lake/packages/mathlib status --porcelain)"` | 0 | pinned mathlib worktree clean |
| placeholder scan below | 1 | no matches; exit 1 is ripgrep's no-match result |
| `python3 -m json.tool Stage1_Instances/THM-M-0120/proof-blocker-2026-07-14.json` | 0 | historical structured blocker remains valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0120` | 0 | no whitespace errors in the owned-path delta |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test manifest deliberately absent |

Exact Lean recipe, run without asking Lake to resolve optional packages whose artifacts this target
does not import:

```bash
repo_root=$PWD
lean_root=/home/sansha-2/external/awesome_theorems/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0120
tmp=$(mktemp -d /tmp/thm-m-0120-proof-recheck.XXXXXX)
trap 'rm -rf "$tmp"' EXIT HUP INT TERM
lean=/home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean
lean_path=$(find "$lean_root/.lake/packages" -path '*/.lake/build/lib/lean' \
  -type d -print | sort | paste -sd: -)
lean_path="$lean_root/.lake/build/lib/lean:$lean_path"
cp "$target/Statement.lean" "$tmp/Statement.lean"
cp "$target/Proof.lean" "$tmp/Proof.lean"
cd "$tmp"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 600 "$lean" --trust=0 -t0 \
  -R "$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 600 "$lean" --trust=0 -t0 \
  -R "$tmp" "$tmp/Proof.lean"
```

Exact placeholder scan:

```bash
rg -n --pcre2 '\b(?:sorry|admit|axiom)\b|sorryAx|unsafe' \
  Stage1_Instances/THM-M-0120/Proof.lean
```

The relevant final output was:

```text
'Stage1Instances.THMM0120.Proof.not_moriConeTheoremTarget' depends on axioms:
[propext, Classical.choice, Quot.sound]
LEAN_RECHECK_EXIT=0
```

The content inputs at this base are unchanged: statement SHA-256
`69eabc83cd8b7fe8fa34d598c9de890eea09d8ee8357d551abf3e7727444fd6b`, proof-witness
SHA-256 `e5c342e97885f6a533fada4b928685ea4c2e888baa5e21699a454049f02f29ab`,
obligation-registry SHA-256 `cd24f57d66422f500f17b348bed362dddcdf032447861f2560518f95c1a48a2d`,
typed-graphs SHA-256 `9ca86f175b3413edd03fec0971bb165c9dd0396ade874a0b0c0c674ac861e23f`,
and anchor-audit SHA-256 `71ff1889e55e0f4387697db69ff7acae110f0530f94879ef68ae06370475090d`.

No `.stage1-worker-selftest.json` is written because the assigned positive proof deliverable is
blocked rather than genuinely self-tested as complete.

An independent isolated `lake env lean -R "$tmp" -t0` recheck succeeded before a concurrent
automation process left the shared optional `Formalizations/Lean/.lake/packages/flt-regular`
checkout without a resolvable `HEAD`. A later Lake invocation therefore exited 1 while inspecting
that unrelated optional package. The recorded direct-Lean recipe repeated the check without package
resolution and rechecked this target entirely from the existing pinned artifacts. This worker did
not fetch, repair, or otherwise mutate `.lake`.
