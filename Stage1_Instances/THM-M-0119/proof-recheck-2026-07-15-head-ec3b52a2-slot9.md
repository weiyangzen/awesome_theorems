# THM-M-0119 proof-phase recheck at base ec3b52a2

Item: `S56-M-0119-PROOF`

Intent: `prove`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `ec3b52a20f5e28de012c23dce1af403343b9a1cb`

Base tree: `b08b83715d8f74868d1f31bbe82a7951b26edad1`

## Verdict

`blocked`. No consistent positive proof body exists for the exact frozen Lean
target. The existing placeholder-free declaration

```text
Stage1Instances.THMM0119.not_kawamataViehwegVanishingTarget :
  Not (Stage1Instances.THMM0119.KawamataViehwegVanishingTarget.{0, 0})
```

kernel-checks at trust level zero against a freshly compiled temporary
`Statement.olean`. A universe-polymorphic proof of the requested target would
specialize to universes `(0, 0)` and contradict this declaration.

The countermodel takes `k := Rat`, `X := Spec Rat`, unit divisor types, every
named geometric proposition equal to `True`, and every cohomology group equal
to `Int`. Specializing a purported target proof at degree one produces
`Subsingleton Int`; `Subsingleton.elim` would force `(0 : Int) = 1`, contrary
to `Int.zero_ne_one`. Lean reports exactly `propext`, `Classical.choice`, and
`Quot.sound` for the refutation.

This refutes the frozen abstract encoding, not the mathematical
Kawamata--Viehweg vanishing theorem. The geometric propositions and
`cohomologyModelsDivisorialSheaf` are independent fields, with no law tying
them to the arbitrary `cohomology` family. Adding such a law in the proof
phase would change the frozen target. The conditional composition lemmas in
`ObligationTree.lean` consume degreewise vanishing or an already-proved
vanishing conclusion, so they cannot supply the missing proof.

No positive proof body, proof receipt, or frozen-obligation closure was added.
The authoritative per-target `task-dag.json` still records all predecessor
receipt lists as empty and the proof task as `open`; the generated blueprint's
provisional predecessor markers do not grant acceptance. Lifecycle remains
`planned`, and the recorded vector remains `[H4, M3, R4]`. `M5` is only the
proposed machine diagnosis for this refutable backend encoding. The
countermodel does not refute the human mathematical theorem, so this worker
does not assign `H5`.

Audit completion, validation, release, theorem completion, and master
acceptance remain open. Because the assigned proof phase is not complete,
`.stage1-worker-selftest.json` is deliberately absent.

## Failed Gate And Retry

The first failed gate is the section 5 Theorem Intake Contract's requirement
that every backend encoding map to the canonical mathematical claim, at
`M0119-S-DATA` and `M0119-S-HYP`.

The frozen graph's authoritative remaining root cut set is still
`M0119-X-APIS`, `M0119-N-RESOLUTION`, `M0119-L-SMOOTH`, and
`M0119-C-PUSH`. The countermodel additionally proposes the invalidation and
retry boundary `S56-M-0119-STATEMENT`, `M0119-S-DATA`, `M0119-S-HYP`, and
`M0119-ROOT`; it does not silently rewrite the frozen graph.

Positive proof work can resume only after reopening the statement phase,
replacing the disconnected stand-ins with native or law-bearing definitions
that genuinely tie the klt, divisor, positivity, divisorial-sheaf, and
cohomology data together without assuming vanishing, accepting a new statement
fingerprint and obligation-registry version, and rerunning statement mutation,
anchor audit, obligation-tree construction, and proof execution.

## Validation

All checks ran in this worker clone with the existing pinned Lake closure. The
automation-provided untracked `Formalizations/Lean/.lake` symlink was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, network
access, or `.lake` mutation was performed. Temporary Lean objects and logs
were written under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `git rev-parse HEAD HEAD^{tree}; date --iso-8601=seconds; git status --short --untracked-files=all` | 0 | Base `ec3b52a20f5e28de012c23dce1af403343b9a1cb`, tree `b08b83715d8f74868d1f31bbe82a7951b26edad1`; only the automation-provided `.lake` symlink was untracked before this recheck. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0119` | 0 | Rank 38; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0119/check_obligation_tree.py` | 0 | 33 obligations and 42 typed edges passed; denominator `d9c76b6b...92db`; root remains `M3`. |
| `python3 Stage1_Instances/THM-M-0119/check_anchor_audit.py` | 0 | Immutable pins and local boundaries agreed; no exact positive-root candidate is claimed. |
| Pinned `lake env lean --trust=0 -t0` replay below | 0 | Started `2026-07-15T14:31:07+08:00` and ended `2026-07-15T14:31:41+08:00`; statement, refutation, and conditional composition elaborated. Statement/proof/obligation output SHA-256 values: `e7402bc1...644b`, `c6b29f07...eb42`, `f2ba3ac9...7f5b`; temporary `Statement.olean`: `01729724...e0b`. |
| `rg -n --pcre2 '\\b(?:sorry|admit|sorryAx|native_decide)\\b|^[[:space:]]*(?:axiom|unsafe|external)\\b|implemented_by' Stage1_Instances/THM-M-0119 --glob '*.lean'` | 1 | Expected no-match result: no scanned prohibited construct occurs in the owned Lean sources. |
| `cd Formalizations/Lean && lake env lean --version; git -C .lake/packages/{mathlib,flt-regular} rev-parse HEAD HEAD^{tree}; sha256sum lean-toolchain lake-manifest.json` | 0 | Lean `4.29.0`, commit `98dc76e3...6740`; pinned mathlib and flt-regular revisions/trees resolve with clean worktrees; toolchain and manifest hashes agree with the structured record. |
| `test ! -e .stage1-worker-selftest.json && test ! -e Stage1_Instances/THM-M-0119/proof-receipt.json` | 0 | Completion self-test manifest and positive proof receipt deliberately absent because the exact target is refuted. |
| JSON parse and blocker-invariant/source-hash check | 0 | The current-base blocker is valid JSON; item, base, blocked state, noncompletion boundary, changed paths, and all nine source hashes agree. |
| Scoped tracked and added-file `git diff --check` | 0 | No whitespace diagnostic was emitted. |

Exact narrow Lean recipe, run from the repository root:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0119
lean_path=$(find -L "$lean_root/.lake/packages" \
  -path '*/.lake/build/lib/lean' -type d -print | sort | paste -sd: -)
tmp=$(mktemp -d /tmp/thm-m-0119-slot9-lakeenv-ec3b52a2.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cd "$target"
PATH="$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin:$PATH" \
  LEAN_PATH="$lean_path" LEAN_NUM_THREADS=1 \
  timeout --foreground --kill-after=10s 900s \
  lake env lean --trust=0 -t0 -o "$tmp/Statement.olean" Statement.lean \
  >"$tmp/statement.log" 2>&1
PATH="$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin:$PATH" \
  LEAN_PATH="$tmp:$lean_path" LEAN_NUM_THREADS=1 \
  timeout --foreground --kill-after=10s 900s \
  lake env lean --trust=0 -t0 Proof.lean >"$tmp/proof.log" 2>&1
PATH="$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin:$PATH" \
  LEAN_PATH="$lean_path" LEAN_NUM_THREADS=1 \
  timeout --foreground --kill-after=10s 900s \
  lake env lean --trust=0 -t0 ObligationTree.lean \
  >"$tmp/obligation.log" 2>&1
sha256sum "$tmp/statement.log" "$tmp/proof.log" \
  "$tmp/obligation.log" "$tmp/Statement.olean"
```

Exact source, registry, environment, output, failed-gate, and retry-condition
bindings are recorded in the paired JSON artifact. This is durable blocker
evidence, not a positive proof receipt, and it does not satisfy
`S56-M-0119-PROOF`.
