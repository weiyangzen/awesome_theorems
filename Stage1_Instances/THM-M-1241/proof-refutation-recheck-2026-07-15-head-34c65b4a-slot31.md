# THM-M-1241 proof refutation recheck at current base

Item: `S56-M-1241-PROOF`

Intent: `prove`

Recorded: `2026-07-15T20:01:12+08:00` (`Asia/Shanghai`)

Base revision: `34c65b4a5d82231740b5d5346afe3b11fd795d19`

Base tree: `d961c0376362e94e2f72d9f88ceb2ddf55134577`

## Verdict

`blocked`. The exact frozen proposition is false, so no positive proof body can be implemented or
imported in a consistent Lean environment. The tracked, placeholder-free declaration

```text
Stage1Instances.THM_M_1241.not_gagliardoNirenbergTarget :
  not Stage1Instances.THM_M_1241.GagliardoNirenbergTarget
```

was replayed from fresh temporary objects at this base with `lake env lean --trust=0 -t0`. Lean
reports exactly `[propext, Classical.choice, Quot.sound]` and `Declarations are sorry-free!`.

The counterexample specializes the frozen target to

```text
n = 1, m = 1, j = 0, q = infinity, r = 1, p = infinity, a = 1,
u = the constant function 1.
```

Every parameter hypothesis holds. The critical-case restriction is vacuous because it assumes
`1 < r`. The zero-order exceptional premise is not required because its antecedent contains
`r.toReal * m < n`, which becomes `1 < 1`. The constant function has order-zero
`L^infinity` seminorm `1` and order-one `L^1` derivative seminorm `0`, so the requested estimate
reduces to `1 <= C * 0 ^ 1 * 1 ^ 0`, hence `1 <= 0`, for every proposed constant.

This refutes only the frozen formal encoding. It indicates a missing explicit or implicit endpoint
side condition and does not refute a suitably corrected classical Gagliardo-Nirenberg theorem.
Correcting the proposition is outside this proof-phase assignment: doing so would change the
canonical expression fingerprint and require a new source-fidelity review, statement freeze,
obligation registry, typed graphs, and dependent evidence.

The first failed gate is `M1241-T-ENDPOINT`: its admitted `r = 1` instance requires the false
fixed-parameter conclusion exhibited above. The registry-v1 root cut remains `M1241-T-FINITE` plus
`M1241-T-ENDPOINT`, but the endpoint member is positively refuted rather than merely missing.
`Proof.lean` proves only an unregistered `p = 0` fragment, while
`root_of_finite_and_endpoint_packages` consumes rather than constructs both terminal packages.

The proof item remains `[ ]`, lifecycle remains `planned`, and no proof receipt, state change,
audit completion, theorem completion, validation, release, or master acceptance is claimed.
Because the assigned positive proof phase is not complete, `.stage1-worker-selftest.json` is
deliberately absent.

## Narrow validation

All commands ran in this worker clone. The automation-provided `Formalizations/Lean/.lake` symlink
was treated as read-only and reused the canonical pinned artifacts. Lean output was isolated in an
ephemeral directory and removed. No `lake update`, `lake build`, dependency clone/fetch, checkout
repair, or `.lake` mutation was performed. A delegated source search made three bounded read-only
HTTP attempts to the pinned NUMDAM PDF URL and one DuckDuckGo query. The NUMDAM HEAD request
returned HTTP 405, two GET attempts produced no surfaced status or usable retained source, and
DuckDuckGo timed out after 30 seconds (`curl` exit 28). Temporary output was confined to `/tmp` and
removed. These attempts supplied no proof credit and wrote no repository or dependency files.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and exactly 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1241` | 0 | Rank 422; lifecycle `planned`; theorem incomplete. |
| `env LEAN_NUM_THREADS=1 timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-1241/check_statement.py` | 0 | Exact statement fingerprint `bf613985e300aa3a5b5e8299a1e0e0e059369387e17c7f0d2c92dc8d8190eb82`; all four structural mutations killed; pinned toolchain and mathlib identity confirmed. |
| `python3 Stage1_Instances/THM-M-1241/check_obligation_tree.py` | 0 | 15 obligations and 31 typed edges passed; denominator `d2173828bd656ec7e4545903a4fdd42a5c759de71b31e46f8c4c189be864991e`; registry still projects root M3 and both terminal packages M4. |
| isolated Lake-derived trust-zero four-module recipe below | 0 | `Statement.lean`, `ObligationTree.lean`, `Proof.lean`, and `Counterexample.lean` elaborated into fresh nonempty temporary oleans. The checked composer, partial proofs, and exact refutation report only `propext`, `Classical.choice`, and `Quot.sound`; every printed sorry report says sorry-free. |
| prohibited-device scan over owned Lean files | 1 | Expected no-match result: no `sorry`, `admit`, `axiom`, `sorryAx`, `unsafe`, `extern`, `implemented_by`, or `native_decide` token. |
| `git -C Formalizations/Lean/.lake/packages/mathlib diff --quiet` | 0 | Pinned mathlib remained unmodified at revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. |
| first NUMDAM GET/PDF-text command (exact argv in JSON) | unrecorded | Ancillary evidence limitation: orchestration surfaced neither exit nor output after about 19 seconds; no hash/text or persistent output. |
| `curl -IL --max-time 20` against the pinned NUMDAM PDF URL, piped to `head` | 0 | Pipeline reported HTTP 405 with `Allow: GET`; no source evidence. |
| second NUMDAM GET/inspection command (exact argv in JSON) | unrecorded | Ancillary evidence limitation: orchestration surfaced neither exit nor output after about 27 seconds; no usable or persistent source. |
| DuckDuckGo query command (exact argv in JSON) | 28 | `curl` timed out after 30002 milliseconds; no result or proof credit. |
| formal-source diff against prior replay base `90a1d52c43113012c8aa0e2b110da02e58ce1724` | 0 | The target, refutation, partial proof, composer, registry, and typed graphs are unchanged. |
| `python3 -m json.tool Stage1_Instances/THM-M-1241/proof-refutation-recheck-2026-07-15-head-34c65b4a-slot31.json` | 0 | The structured blocker artifact is valid JSON. |
| no-index whitespace-check loop over both new blocker artifacts | 0 | Both untracked files passed `git diff --no-index --check` with the expected content-difference exit and no whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is absent. |

The successful kernel replay recipe was:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-1241
tmp=$(mktemp -d /tmp/thm-m-1241-34c65b4a-slot31-proof.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
base_lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$target"
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$base_lean_path" \
  timeout --foreground --kill-after=5s 300s lake env lean --trust=0 -t0 \
    -o "$tmp/Statement.olean" Statement.lean
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_lean_path" \
  timeout --foreground --kill-after=5s 300s lake env lean --trust=0 -t0 \
    -o "$tmp/ObligationTree.olean" ObligationTree.lean
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_lean_path" \
  timeout --foreground --kill-after=5s 300s lake env lean --trust=0 -t0 \
    -o "$tmp/Proof.olean" Proof.lean
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_lean_path" \
  timeout --foreground --kill-after=5s 300s lake env lean --trust=0 -t0 \
    -o "$tmp/Counterexample.olean" Counterexample.lean
test -s "$tmp/Statement.olean"
test -s "$tmp/ObligationTree.olean"
test -s "$tmp/Proof.olean"
test -s "$tmp/Counterexample.olean"
```

The fresh olean sizes were `76664`, `47368`, `71384`, and `136784` bytes in module order. Their
SHA-256 digests are recorded in the adjacent structured artifact.

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake `5.0.0-src+98dc76e`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

## Retry condition

Reopen source-fidelity and statement review. Either accept an H5/M5 target decision for this frozen
proposition, or identify a justified corrected theorem, re-elaborate it as a new canonical target,
and regenerate the obligation registry, typed graphs, and all dependent fingerprints before
retrying positive proof execution. Silently strengthening the current statement in this proof phase
would be an unauthorized theorem substitution.

This fresh current-base artifact is proof-refutation evidence, not a proof receipt. It does not
satisfy `S56-M-1241-PROOF`, propose scheduler state, or claim audit completion, theorem completion,
validation, release, receipt acceptance, or master acceptance.
