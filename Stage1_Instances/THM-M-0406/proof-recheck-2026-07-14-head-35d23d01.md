# THM-M-0406 proof-phase recheck at 35d23d01

Item: `S56-M-0406-PROOF`

Intent: `prove`

Base revision: `35d23d0193cd7c8fccb1d09f22534c6eba066b02`

Base tree: `4325d20b5ec8db888f28fcedc79cc1b7745c0c68`

Recheck date: 2026-07-14 (Asia/Shanghai)

## Verdict

`blocked`. No consistent positive proof body exists for the exact frozen Lean
target. `SurfaceData.curve` is an unconstrained type, so the existing
placeholder-free countermodel chooses `curve := Empty`. With four boundary
components, unit weights and intersections, and all named geometric premises
true, every frozen premise holds while the conclusion would produce an
inhabitant of `Empty`.

The trust-zero kernel replay checks:

```text
Stage1Instances.THMM0406.not_corvajaZannierTheoremOne :
  Not (Stage1Instances.THMM0406.CorvajaZannierTheoremOne.{0, 0} (k := Rat))
```

Its axiom report is exactly `[propext, Classical.choice, Quot.sound]`. This
refutes the overbroad abstract encoding, not the mathematical
Corvaja--Zannier theorem. `SurfaceDegeneracyEngine` is definitionally the same
refutable proposition, so its conditional adapter supplies no positive body.
Adding curve existence, changing `SurfaceData`, or proving a realizable
specialization would alter or substitute the frozen target.

The root remains `[H1, M5, R3]`. The first failed gate is
`M0406-S-DEFINITIONS` / exact-target consistency, and the remaining root cut is
`M0406-S-DEFINITIONS` plus `M0406-ROOT`. The proof item stays `[ ]`; no proof
receipt, scheduler transition, audit completion, theorem completion, release,
or master acceptance is claimed. Because the assigned proof phase is not
complete, `.stage1-worker-selftest.json` is deliberately absent.

## Validation

All checks ran in this worker clone using the existing pinned Lake closure.
The automation-provided untracked `Formalizations/Lean/.lake` symlink was
reused read-only. No `lake update`, `lake build`, dependency clone/fetch,
network access, or `.lake` mutation was performed.

A read-only primary-source comparison consulted immutable arXiv source
`math/0206100`; it was research context, not machine-validation evidence, and
did not fetch a dependency. A preliminary `check_anchor_audit.py` invocation
exited 1 while the shared read-only `flt-regular` checkout temporarily lacked a
resolvable `HEAD`. No repair or fetch was performed. The final invocation below
passed after external provisioning restored the manifest-pinned revision.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0406` | 0 | Rank 19; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0406/check_obligation_tree.py` | 0 | Fourteen obligations and 26 typed edges passed; denominator `46deb9e2...d90a7`; the frozen predecessor graph reports root open `M4`. |
| `python3 Stage1_Instances/THM-M-0406/check_anchor_audit.py` | 0 | Six candidates with immutable pins and substrate witnesses passed; root remains open. |
| Isolated `lake env lean --trust=0 -t0` recipe below | 0 | The statement and countermodel elaborated; both countermodel theorems report exactly `[propext, Classical.choice, Quot.sound]`. Statement-output SHA-256: `0f59d3486b6464922278f83f5e3871c79e0c2e7964d1e3a8a412f16e567b385b`; proof-output SHA-256: `942b7cc706eaa0b7aa1143e3ecfba1f8387659e19954b5b978ea77b98188a1f8`. |
| `rg -n '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*axiom\b\|^[[:space:]]*unsafe\b' Stage1_Instances/THM-M-0406 --glob '*.lean'` | 1 | Expected no-match result: no prohibited construct occurs in the owned Lean sources. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | Mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse HEAD HEAD^{tree}` | 0 | flt-regular `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`, tree `32c9eace926573a9981787ae97643e520353c893`. |
| `python3 -m json.tool Stage1_Instances/THM-M-0406/proof-recheck-2026-07-14-head-35d23d01.json >/dev/null` | 0 | The structured blocker record parsed. |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-0406/proof-recheck-2026-07-14-head-35d23d01.{json,md}` (run once per file, with expected difference status asserted) | 0 | Neither new owned artifact has whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest deliberately absent because the positive proof phase is blocked. |

Exact isolated Lean recipe, run from the repository root:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0406
tmp=$(mktemp -d /tmp/thm-m-0406-head-35d23d01.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$target/Statement.lean" "$target/Proof.lean" "$tmp/"
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$tmp"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" "$lean" --trust=0 -t0 \
  --root="$tmp" -o Statement.olean Statement.lean >statement.log 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH=".:$lean_path" "$lean" --trust=0 -t0 \
  --root="$tmp" Proof.lean >proof.log 2>&1
sha256sum statement.log proof.log
```

The structured companion record binds source hashes, environment pins, exact
results, the failed gate, retry condition, changed paths, and status boundary.

## Retry Condition

Reopen the statement phase and replace the refuted abstract encoding with a
source-faithful proposition whose intrinsic, noncircular geometric semantics
rule out this model. Then accept new statement and obligation-registry
versions and rerun the anchor-audit and obligation-tree gates before another
proof attempt. Merely assuming `Nonempty X.curve` or the desired conclusion is
not a source-faithful repair.
