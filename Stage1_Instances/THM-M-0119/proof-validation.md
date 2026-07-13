# THM-M-0119 proof-phase blocker

Item: `S56-M-0119-PROOF`

Intent: `prove`

Base revision: `ffea62ba1a7c0b0f84d70fd07f87d3eef57fe330`

Base tree: `4662e08d189bd534919775f750c6909591aeafcb`

Recheck date: 2026-07-14 (Asia/Shanghai)

## Verdict

`blocked`. No consistent positive proof body exists for the exact frozen Lean
target. `KawamataViehwegData` stores the named geometric conditions and
`cohomologyModelsDivisorialSheaf` as independent propositions, while
`cohomology` is an arbitrary family of additive commutative groups. None of
the hypotheses imposes a law connecting that family to the geometry.

The existing placeholder-free declaration

```text
Stage1Instances.THMM0119.not_kawamataViehwegVanishingTarget :
  Not (Stage1Instances.THMM0119.KawamataViehwegVanishingTarget.{0, 0})
```

kernel-checks at trust level zero. Its model takes `k := Rat`, `X := Spec Rat`,
unit divisor types, every named geometric proposition equal to `True`, and
every cohomology group equal to `Int`. A purported root proof specialized to
degree one would produce `Subsingleton Int`, forcing `(0 : Int) = 1` and
contradicting `Int.zero_ne_one`. Lean reports exactly `propext`,
`Classical.choice`, and `Quot.sound` for the refutation.

This refutes the frozen abstract encoding, not the mathematical
Kawamata--Viehweg vanishing theorem. The conditional declarations in
`ObligationTree.lean` consume degreewise vanishing or an already-proved
vanishing conclusion, so they cannot repair the inconsistency or supply a
positive root body. Adding semantic laws in this phase would change the frozen
target.

The predecessor artifacts still record `[H4, M3, R4]`. This proof result
proposes `M5` as the exact-target-consistency diagnosis, but does not edit or
claim acceptance of that earlier state. No positive proof body, closed
obligation, proof receipt, audit completion, theorem completion, validation,
release, scheduler transition, or master acceptance is claimed.

## Failed Gate

The first failed gate is exact-target consistency at `M0119-S-DATA` and
`M0119-S-HYP`. Positive proof execution can resume only after reopening the
statement phase, replacing the disconnected stand-ins with native or
law-bearing definitions that genuinely tie the klt, divisor, positivity,
divisorial-sheaf, and cohomology data together, and accepting a new statement
fingerprint and obligation-registry version. Statement mutation, anchor audit,
obligation-tree construction, and proof execution must then be rerun.

The proof item remains `[ ]`. Because the assigned positive phase is not
genuinely self-tested as complete, `.stage1-worker-selftest.json` remains
absent.

## Validation

All checks ran in this worker clone with the existing pinned Lake closure. The
automation-provided untracked `Formalizations/Lean/.lake` symlink was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, network
access, or `.lake` mutation was performed. The temporary Lean object and logs
were created under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0119` | 0 | Rank 38; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0119/check_obligation_tree.py` | 0 | 33 obligations and 42 typed edges passed; denominator `d9c76b6b...92db`; the predecessor graph still records the root open `M3`. |
| `python3 Stage1_Instances/THM-M-0119/check_anchor_audit.py` | 0 | Immutable pins and local boundaries agreed; no exact positive-root candidate is claimed. |
| Isolated `lake env lean --trust=0 -t0` recipe below | 0 | The exact statement and countermodel refutation elaborated; the refutation reports `[propext, Classical.choice, Quot.sound]`. Statement-output SHA-256: `e7402bc1bb4f1bc6255436b7d7635869788000c47450782fa75cf8272dac644b`; proof-output SHA-256: `c6b29f07f5d9175a9aa2439c336d176a5cb200801d6a2769f0fa01754003eb42`. |
| `rg -n --pcre2 '\b(?:sorry\|admit\|sorryAx\|native_decide)\b\|^[[:space:]]*(?:axiom\|unsafe\|external)\b\|implemented_by' Stage1_Instances/THM-M-0119 --glob '*.lean'` | 1 | Expected no-match result: no prohibited construct in the owned Lean sources. |
| `cd Formalizations/Lean && lake env lean --version; git -C .lake/packages/mathlib rev-parse HEAD HEAD^{tree}; sha256sum lean-toolchain lake-manifest.json` | 0 | Lean `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib revision `8a178386...ea95`, tree `bdc39a31...c2b`; environment hashes match the structured blocker. |
| `python3 -m json.tool Stage1_Instances/THM-M-0119/proof-blocker.json` | 0 | The structured blocker is valid JSON. |
| Per-file `git diff --no-index --check /dev/null` for both fresh blocker artifacts | 0 aggregate | Both new files differ from `/dev/null` and emitted no whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json && test ! -e Stage1_Instances/THM-M-0119/proof-receipt.json` | 0 | Completion self-test manifest and positive proof receipt deliberately absent. |

Exact isolated Lean recipe, run from the repository root:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0119
tmp=$(mktemp -d /tmp/thm-m-0119-prooftest.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$target"
LEAN_PATH="$lean_path" "$lean" --trust=0 -t0 \
  -o "$tmp/Statement.olean" Statement.lean >"$tmp/statement.log" 2>&1
LEAN_PATH="$tmp:$lean_path" "$lean" --trust=0 -t0 \
  Proof.lean >"$tmp/proof.log" 2>&1
sha256sum "$tmp/statement.log" "$tmp/proof.log"
```

Exact source, registry, environment, output, failed-gate, and retry-condition
bindings are recorded in `proof-blocker.json`. This is durable negative kernel
evidence, not a positive proof receipt, and it does not satisfy
`S56-M-0119-PROOF`.
