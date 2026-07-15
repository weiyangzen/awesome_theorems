# THM-M-0119 proof-phase recheck at base 311725fc

Item: `S56-M-0119-PROOF`

Intent: `prove`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `311725fcdfab3953078cfe98e90f3189ffcdb252`

Base tree: `3b889d2dfc4156a017562af672af9364893db8a7`

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
phase would change the frozen target.

The two conditional declarations in `ObligationTree.lean` also elaborated at
trust level zero and reported no axioms. They consume degreewise vanishing or
an already-proved vanishing conclusion, however, so they close no positive
root obligation and cannot supply the missing proof.

No positive proof body, proof receipt, or frozen-obligation closure was added.
The proof item remains `[ ]`; lifecycle remains `planned`; and the predecessor
vector remains `[H4, M3, R4]`. `M5` is the proposed machine diagnosis for this
refutable backend encoding, not an accepted state change. This countermodel
does not refute the human mathematical theorem, so this worker does not assign
`H5`.

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

The automation-provided untracked `Formalizations/Lean/.lake` symlink resolves
to the shared canonical pinned artifacts. At recheck time,
`packages/flt-regular` contained only `.git`, its `.git/HEAD` was
`ref: refs/heads/.invalid`, and it could not resolve `HEAD`. The target anchor
checker therefore failed. A bounded project-root `lake env lean --version`
probe also produced no output before timing out after 20 seconds. This worker
did not run `lake update`, `lake build`, clone or fetch a dependency, use the
network, or repair or otherwise mutate `.lake`.

The narrow source recheck still ran through `lake env lean`: invoking Lake from
the target directory avoids loading the broken project dependency graph, while
an explicit read-only `LEAN_PATH` supplies the existing pinned package build
directories. Temporary Lean outputs were written under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `git rev-parse HEAD HEAD^{tree}; date --iso-8601=seconds; git status --short --untracked-files=all` | 0 | Base `311725fcdfab3953078cfe98e90f3189ffcdb252`, tree `3b889d2dfc4156a017562af672af9364893db8a7`; only the automation-provided `.lake` symlink was untracked before this recheck. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0119` | 0 | Rank 38; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0119/check_obligation_tree.py` | 0 | 33 obligations and 42 typed edges passed; denominator `d9c76b6b...92db`; root remains `M3`. |
| `python3 Stage1_Instances/THM-M-0119/check_anchor_audit.py` | 1 | Failed because the shared canonical `flt-regular` package could not resolve `HEAD`; no dependency mutation was attempted. |
| Bounded project-root `lake env lean --version` | 124 | No output before the 20-second bound; independent checkout inspection found that `flt-regular` could not resolve `HEAD`. |
| Read-only `flt-regular` HEAD and pinned-object inspection | 128 | `.git/HEAD` was `ref: refs/heads/.invalid`, the package directory contained only `.git`, and `rev-parse HEAD` failed; the manifest-pinned commit object remained local. |
| Target-directory `lake env lean --trust=0 -t0` replay below | 0 | Started `2026-07-15T13:03:31+08:00` and ended `2026-07-15T13:03:49+08:00`; the statement, countermodel refutation, and conditional composition module elaborated at trust level zero. Statement-output SHA-256: `e7402bc1bb4f1bc6255436b7d7635869788000c47450782fa75cf8272dac644b`; proof-output SHA-256: `c6b29f07f5d9175a9aa2439c336d176a5cb200801d6a2769f0fa01754003eb42`; obligation-output SHA-256: `f2ba3ac92c0cdff043432949d1445d9b85aa8114a413fa9392b7982e801c7f5b`; temporary `Statement.olean` SHA-256: `01729724a41a4bee420c56a7f3fbcd0d4dd681ba039a7633d3739c2239919e0b`. |
| `rg -n --pcre2 '\b(?:sorry\|admit\|sorryAx\|native_decide)\b\|^[[:space:]]*(?:axiom\|unsafe\|external)\b\|implemented_by' Stage1_Instances/THM-M-0119 --glob '*.lean'` | 1 | Expected no-match result: no prohibited construct occurs in the owned Lean sources. |
| Direct Lean version, mathlib revision/tree/status, and toolchain/manifest hash checks | 0 | Lean `4.29.0` commit `98dc76e...6740`; mathlib `8a178386...ea95`, tree `bdc39a31...c2b`, clean dependency worktree; toolchain and manifest hashes agree. |
| `python3 -m json.tool Stage1_Instances/THM-M-0119/proof-recheck-2026-07-15-head-311725fc-slot9.json` | 0 | The current-base structured blocker record is valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-0119` plus per-file `git diff --no-index --check /dev/null` for both changed paths | 0 aggregate | No tracked or untracked-file whitespace diagnostic was emitted; the no-index checks had the expected added-file difference status. |
| `test ! -e .stage1-worker-selftest.json && test ! -e Stage1_Instances/THM-M-0119/proof-receipt.json` | 0 | Completion self-test manifest and positive proof receipt are deliberately absent because the proof phase is blocked. |

Exact narrow replay, begun from the repository root:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0119
lean_path=$(find -L "$lean_root/.lake/packages" \
  -path '*/.lake/build/lib/lean' -type d -print | sort | paste -sd: -)
tmp=$(mktemp -d /tmp/thm-m-0119-slot9-lakeenv-311725fc.XXXXXX)
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

Exact source hashes, environment boundaries, negative declaration,
composition boundary, failed gate, and retry condition are bound in
`proof-recheck-2026-07-15-head-311725fc-slot9.json`. This is durable blocker
evidence, not a positive proof receipt.
