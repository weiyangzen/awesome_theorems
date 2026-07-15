# THM-M-0579 proof-phase recheck at base 30228d98

Item: `S56-M-0579-PROOF`

Intent: `prove`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `30228d98c98c401cb60a3dfa09eec01bb904053f`

Base tree: `773a33c6344fb9787649fbc5edea99092ea68856`

## Verdict

`blocked`. The exact proposition `Stage1Instances.THMM0579.Statement` is the
full topological three-dimensional Poincare theorem. Neither the repository nor
its pinned Lean dependency closure contains an eligible retained proof body.
This attempt adds no proof body. The item stays `[ ]`, lifecycle stays
`planned`, the root vector stays `[H3, M3, R4]`, and audit and theorem
completion remain false. Because the requested proof phase is not complete,
`.stage1-worker-selftest.json` is intentionally absent.

The first failed gate is terminal proof-body availability. The frozen immediate
root cut contains `M0579-T-RECOGNITION` and `M0579-T-RIGIDITY`, both `M4`.
Their checked assembly theorem accepts these packages as premises; it does not
inhabit either package. Recognition still expands through open smoothing,
prime normalization, Ricci flow, surgery control, analytic estimates, finite
extinction, and recomposition packages.

The current trust-zero replay checked that

```text
(HomotopySphereRecognition and HomotopySphereTopologicalRigidity) iff Statement
```

The root gives recognition via `Homeomorph.toHomotopyEquiv` and gives rigidity
by ignoring its extra homotopy-equivalence premise. Consequently, the immediate
cut is root-equivalent rather than a difficulty-reducing proof decomposition.
Using `root_of_recognition_and_rigidity` without independently proven premises
would be circular. The route ingredients are also frozen as planned prose
targets rather than exact Lean interfaces.

Pinned mathlib contains matching signatures only as Batteries `proof_wanted`
source markers. Batteries elaborates them under `withoutModifyingEnv`, so the
import retains none of their names. The current negative probes reproduced
`Unknown constant` for all three matching names. The audited external candidates
are statement-only or placeholder-bearing and receive no proof credit.

The inherited `validation-specs.json` belongs to the obligation-tree phase and
lacks the strict structured proof-recipe fields. It is not proof-phase evidence.

## Validation

The standard, target-set, obligation-tree, and anchor-audit checks passed. The
required `lake env` route did not start Lean: Lake rejects the automation-provided
`flt-regular` checkout because its `HEAD` is `refs/heads/.invalid`. Worker policy
forbids repairing, updating, fetching, or otherwise mutating `.lake`.

A narrower current trust-zero elaboration did succeed without touching `.lake`:
the pinned Lean binary was invoked directly with `LEAN_PATH` composed from the
existing mathlib transitive package build directories recorded at the pinned
revisions in the root and mathlib manifests. Outputs were written only under a
disposable `/tmp` directory and removed. This is warm-cache, nonrelease blocker
evidence, not a proof receipt or a substitute for the required proof body.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0579` | 0 | Rank 114; lifecycle `planned`; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` | 0 | Only the automation-provided `Formalizations/Lean/.lake` symlink was untracked before writing these artifacts |
| `python3 Stage1_Instances/THM-M-0579/check_obligation_tree.py` | 0 | 16 obligations and 34 typed edges passed; denominator `984bcfffcea5afa7c11e3f2eb78ad31c2eed6b99e1a0913496186ceb1595776f`; root M3 and both cut packages M4 |
| `python3 Stage1_Instances/THM-M-0579/check_anchor_audit.py` | 0 | Frozen target, five candidates, discarded `proof_wanted` boundary, dependency pins, and noncompletion status agreed |
| `cd Formalizations/Lean && lake env lean --version` | 1 | Lake failed before Lean because it could not resolve `flt-regular` `HEAD` |
| Direct isolated trust-zero replay | 0 | `Statement.lean`, `AnchorAudit.lean`, `ObligationTree.lean`, and `ProofBlockerProbe.lean` elaborated against existing pinned artifacts |
| Axiom and absent-name output from that replay | 0 | Both diagnostic theorems reported only `propext`, `Classical.choice`, and `Quot.sound`; all three matching proof names reported `Unknown constant` |
| `cat .../flt-regular/.git/HEAD; git -C .../flt-regular rev-parse HEAD` | 128 | The file contains `ref: refs/heads/.invalid`; Git cannot resolve it |
| Pinned mathlib/Batteries revision probes | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` and `756e3321fd3b02a85ffda19fef789916223e578c` |
| Scoped retained-declaration search | 1 | Expected no-match; no retained theorem or lemma supplies a matching Poincare proof name |
| Prohibited-construct scan | 1 | Expected no-match across the four checked owned Lean modules |
| Frozen-input diff against `1228bcce` | 0 | The eight proof inputs plus toolchain and dependency manifest are unchanged |
| `python3 -m json.tool` on the new JSON | 0 | The current-base blocker record parsed successfully |
| Current-base blocker invariant probe | 0 | Item, theorem, base commit/tree, blocked state, noncompletion flags, absent bodies, empty receipts, and changed-path count agreed |
| `git diff --check` plus clean new-file checks | 0 | No whitespace errors in the owned artifacts |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test is absent because this proof item remains blocked |

The direct replay recipe from the repository root was:

```bash
set -euo pipefail
lean_root="$PWD/Formalizations/Lean"
toolchain="$HOME/.elan/toolchains/leanprover--lean4---v4.29.0"
target="$PWD/Stage1_Instances/THM-M-0579"
tmp=$(mktemp -d /tmp/thm-m-0579-direct-all-30228d98.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean_path="$lean_root/.lake/packages/mathlib/.lake/build/lib/lean"
for package in batteries plausible LeanSearchClient importGraph proofwidgets aesop Qq Cli; do
  lean_path="$lean_path:$lean_root/.lake/packages/$package/.lake/build/lib/lean"
done
lean_path="$lean_path:$toolchain/lib/lean"
cd "$target"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 "$toolchain/bin/lean" \
  --trust=0 -t0 -o "$tmp/Statement.olean" Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 "$toolchain/bin/lean" \
  --trust=0 -t0 -o "$tmp/AnchorAudit.olean" AnchorAudit.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 "$toolchain/bin/lean" \
  --trust=0 -t0 -o "$tmp/ObligationTree.olean" ObligationTree.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 "$toolchain/bin/lean" \
  --trust=0 -t0 -o "$tmp/ProofBlockerProbe.olean" ProofBlockerProbe.lean
```

The `Cli` build directory is absent, but no imported module needed it; the
four-module replay completed. All other paths used above exist and are pinned by
the manifests. No source or build artifact under `.lake` was written.

## Retry Condition

Implement the frozen missing packages locally without placeholders, or
integrate a licensed immutable compatible Lean 4 proof with exact transport and
complete kernel, composition, provenance, axiom, trust, and pinned-replay
evidence. Restore the canonical `flt-regular` checkout at manifest revision
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` outside this worker before a
future `lake env` replay.

Assuming a package, treating `proof_wanted` as a theorem, importing a
placeholder or statement-only candidate, or proving a conditional or special
case would substitute a different theorem. These artifacts are blocker
evidence, not a proof receipt. They do not satisfy `S56-M-0579-PROOF`, change
scheduler state, or claim audit completion, theorem completion, validation,
release, or master acceptance.
