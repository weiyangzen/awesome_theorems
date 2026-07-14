# THM-M-0119 proof-phase recheck at base aabb761d

Item: `S56-M-0119-PROOF`

Intent: `prove`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `aabb761d975829b09920d981edc8220edb90e8c3`

Base tree: `a988020866eb03a08cd23d18d5e7711cb5d03742`

## Verdict

`blocked`. No consistent positive proof body exists for the exact frozen Lean
target. The existing placeholder-free declaration

```text
Stage1Instances.THMM0119.not_kawamataViehwegVanishingTarget :
  Not (Stage1Instances.THMM0119.KawamataViehwegVanishingTarget.{0, 0})
```

kernel-checks at trust level zero against a freshly compiled temporary
`Statement.olean`. A universe-polymorphic proof of the positive target would
specialize to universes `(0, 0)` and contradict this declaration.

The model takes `k := Rat`, `X := Spec Rat`, unit divisor types, every named
geometric proposition equal to `True`, and every cohomology group equal to
`Int`. Specializing a purported root proof at degree one produces
`Subsingleton Int`, so `Subsingleton.elim` forces `(0 : Int) = 1`, contrary to
`Int.zero_ne_one`. Lean reports exactly `propext`, `Classical.choice`, and
`Quot.sound` for the refutation.

This refutes the frozen abstract encoding, not the mathematical
Kawamata--Viehweg vanishing theorem. The geometric propositions and
`cohomologyModelsDivisorialSheaf` are independent fields, with no law tying
them to the arbitrary `cohomology` family. Adding such a law during this phase
would change the frozen target. The conditional composition lemmas in
`ObligationTree.lean` consume degreewise vanishing or an already-proved
vanishing conclusion and therefore cannot supply the missing proof.

No positive proof body, proof receipt, or frozen-obligation closure was added.
The proof item remains `[ ]`; the authoritative predecessor vector remains
`[H4, M3, R4]`. `M5` is the proposed machine diagnosis for this refutable
backend encoding, not an accepted state change. This countermodel does not
refute the human mathematical theorem, so this worker does not assign `H5`;
the integration lane must decide whether to correct the statement mismatch or
redirect the retained refuted target under section 3.1.

Audit completion, validation, release, theorem completion, and master
acceptance remain open. Because the assigned positive phase is not complete,
`.stage1-worker-selftest.json` is deliberately absent.

## Failed Gate And Retry

The first failed gate is the section 5 Theorem Intake Contract's requirement
that every backend encoding map to the canonical mathematical claim, at
`M0119-S-DATA` and `M0119-S-HYP`. The section 5.1 pinned elaboration,
serialization, checked-expansion, and recorded mutation checks are not
themselves reported as failing.

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

Checks ran in this worker clone against the existing pinned Lake closure. The
automation-provided untracked `Formalizations/Lean/.lake` symlink was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, network
access, or `.lake` mutation was performed. Temporary Lean outputs were written
under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `git rev-parse HEAD HEAD^{tree}; git status --short` | 0 | Base `aabb761d975829b09920d981edc8220edb90e8c3`, tree `a988020866eb03a08cd23d18d5e7711cb5d03742`; only the automation-provided `.lake` symlink was untracked before this recheck. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0119` | 0 | Rank 38; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0119/check_obligation_tree.py` | 0 | 33 obligations and 42 typed edges passed; denominator `d9c76b6b...92db`; root remains `M3`. |
| `python3 Stage1_Instances/THM-M-0119/check_anchor_audit.py` | 0 | Immutable pins and local boundaries agreed; no exact positive-root candidate is claimed. |
| Pinned Lake-environment `lean --trust=0 -t0` replay below | 0 | The exact statement and countermodel refutation elaborated; Lean reports `[propext, Classical.choice, Quot.sound]`. Statement-output SHA-256: `e7402bc1bb4f1bc6255436b7d7635869788000c47450782fa75cf8272dac644b`; proof-output SHA-256: `c6b29f07f5d9175a9aa2439c336d176a5cb200801d6a2769f0fa01754003eb42`; temporary `Statement.olean` SHA-256: `01729724a41a4bee420c56a7f3fbcd0d4dd681ba039a7633d3739c2239919e0b`. |
| `rg -n --pcre2 '\b(?:sorry\|admit\|sorryAx\|native_decide)\b\|^[[:space:]]*(?:axiom\|unsafe\|external)\b\|implemented_by' Stage1_Instances/THM-M-0119 --glob '*.lean'` | 1 | Expected no-match result: no prohibited construct occurs in the owned Lean sources. |
| `cd Formalizations/Lean && lake env lean --version && git -C .lake/packages/mathlib rev-parse HEAD HEAD^{tree} && test -z "$(git -C .lake/packages/mathlib status --porcelain)" && sha256sum lean-toolchain lake-manifest.json` | 0 | Lean `4.29.0`, commit `98dc76e...6740`; mathlib `8a178386...ea95`, tree `bdc39a31...c2b`, clean worktree; environment hashes match the structured record. |
| `python3 -m json.tool Stage1_Instances/THM-M-0119/proof-recheck-2026-07-15-head-aabb761d.json` | 0 | The current-base structured blocker record is valid JSON. |
| Per-file `git diff --no-index --check /dev/null` for both new artifacts | 0 aggregate | Both files produced the expected added-file difference status and no whitespace diagnostic. |
| `git diff --check -- Stage1_Instances/THM-M-0119` | 0 | No tracked-diff whitespace diagnostic; the per-file no-index checks cover the two untracked artifacts. |
| `test ! -e .stage1-worker-selftest.json && test ! -e Stage1_Instances/THM-M-0119/proof-receipt.json` | 0 | Completion self-test manifest and positive proof receipt deliberately absent. |

Exact pinned Lake-environment replay, run from the repository root:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0119
tmp=$(mktemp -d /tmp/thm-m-0119-prooftest.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cd "$lean_root"
LEAN_NUM_THREADS=1 timeout 300 lake env lean -R "$target" --trust=0 -t0 \
  -o "$tmp/Statement.olean" "$target/Statement.lean" \
  >"$tmp/statement.log" 2>&1
lean_path=$(lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 lake env lean \
  -R "$target" --trust=0 -t0 "$target/Proof.lean" \
  >"$tmp/proof.log" 2>&1
sha256sum "$tmp/statement.log" "$tmp/proof.log" "$tmp/Statement.olean"
```

The exact source hashes, environment, negative declaration, failed gate, and
retry condition are bound in
`proof-recheck-2026-07-15-head-aabb761d.json`. This is durable blocker evidence,
not a positive proof receipt.
