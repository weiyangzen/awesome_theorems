# THM-M-0005 proof-phase partial implementation

Item: `S56-M-0005-PROOF`

Intent: `prove`

Base revision: `40801f373a9b0443cc58ff8ec365fb5b75c8b8c3`

Base tree: `f3b8367a9ec13bd00b783bc4367d64003ffcde28`

Attempt date: 2026-07-14 (Asia/Shanghai)

## Verdict

`blocked`, with genuine partial proof progress. `Proof.lean` adds five placeholder-free declarations:

- `singularChains_projective` proves that every degree object of the singular chain complex over a
  commutative PID is projective. This is candidate evidence toward the projectivity bridge owned by
  `M0005-CHAIN-FREE`; it does not assert a separate `Module.Free` instance or compose into an
  algebraic Kunneth theorem by itself.
- `tensorMap` and `torMap` construct the functorial maps on the target's exact Sigma-indexed tensor
  and `Tor_1` terms.
- `tensorMap_component` and `torMap_component` prove the two component equations named by
  `M0005-COMPONENTS`.

The local bodies are field-level helper evidence toward `M0005-CHAIN-FREE` and
`M0005-COMPONENTS`. The frozen graph still records both as open; in particular, `M0005-COMPONENTS`
depends on the still-open `M0005-ALG-NAT` and `M0005-DIRECT-SUM` nodes. Only the master may reconcile
evidence and accept a dependency-legal node transition. These bodies do not close the assigned
phase: no local
or pinned body supplies the Eilenberg-Zilber comparison/equivalence/naturality or the algebraic
Kunneth inclusion, boundary, exactness, and naturality. Consequently the topological inclusion,
projection, exact sequence, their naturality, assembly, and the canonical root remain open. The
item remains `[ ]`, the root remains `[H1, M3, R3]`, and no `.stage1-worker-selftest.json` is written.

## Validation

Commands ran in this worker clone. The automation-provided canonical `.lake` symlink was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0005` | 0 | Confirmed rank 100, planned hard-mathlib lane, and `theorem_complete: false`. |
| `git status --short --untracked-files=all` | 0 | Reported the pre-existing automation `.lake` symlink and the three owned new files as untracked; no unrelated tracked change was present. |
| isolated pinned-tool recipe below (`lake env which lean`, then the resolved Lean executable) | 0 | The frozen statement and all five declarations in `Proof.lean` elaborated with `--trust=0`; only the four known statement linter warnings occurred. A direct `lake env lean` invocation from the Lake root was also attempted and failed because a pinned dependency's compile-time Git query saw the detached temporary source outside a Git worktree; this did not invalidate the successful resolved-tool replay. |
| `#print axioms` in `Proof.lean` | 0 | Every new declaration reported only `propext`, `Classical.choice`, and `Quot.sound`. |
| `python3 Stage1_Instances/THM-M-0005/check_obligation_tree.py` | 0 | The frozen 18-obligation, 51-edge architecture remained structurally valid. This validator still records the pre-proof open boundary and grants no closure itself. |
| `rg -n --pcre2 '\\b(?:sorry|admit|axiom)\\b|sorryAx|unsafe' Stage1_Instances/THM-M-0005 --glob '*.lean'` | 1 | No prohibited construct occurs in owned Lean sources; exit 1 is ripgrep's no-match result. |
| `git diff --check -- Stage1_Instances/THM-M-0005` | 0 | No whitespace errors in tracked changes; the three new files are untracked, so this command does not cover them. |
| `awk '/[[:blank:]]+$/{print FNR ":" $0; bad=1} END{exit bad}'` over the three new files | 0 | No trailing whitespace in untracked deliverables. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent because the proof phase is incomplete. |

The validated source SHA-256 is
`9257e31e3cbd321cb8aee61c663f6bb5b91f7af92e26bdbf6c7afb4c008950db`; the temporary
`Proof.olean` SHA-256 was
`1f9a0151f44c84e5501e300eb26814e42861af39d57b374f0ad888a5c43bd9f1`.

The isolated elaboration recipe placed all output in a temporary directory inside this disposable
worker clone and removed it on exit:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0005
tmp=$(mktemp -d "$repo_root/.tmp-thm-m-0005-proof.XXXXXX")
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cp "$target/KunnethStatement.lean" "$tmp/KunnethStatement.lean"
cp "$target/Proof.lean" "$tmp/Proof.lean"
cd "$tmp"
LEAN_PATH="$lean_path" "$lean" --trust=0 -R "$tmp" \
  -o "$tmp/KunnethStatement.olean" "$tmp/KunnethStatement.lean"
LEAN_PATH="$tmp:$lean_path" "$lean" --trust=0 -R "$tmp" \
  -o "$tmp/Proof.olean" "$tmp/Proof.lean"
```

The tool identity and environment still come from `lake env`; resolving the executable first avoids
changing Lake's process working directory while preserving the pinned Lean and dependency path.

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; `lake-manifest.json` SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

At 03:02 on the same date, after the successful replay, a different concurrent worker began
mutating the shared canonical `flt-regular` package directory (its HEAD became invalid while fetch
processes were active). A final repeat consequently failed before elaboration. This external shared
cache race is a known failure; this worker did not run those fetches or modify `.lake`. The hashes
above bind the successful earlier replay, but no release or hermetic-current-environment claim is
made.

## Remaining cut

The first newly unimplemented cut after this attempt is `M0005-EZ-MAP`. The authoritative frozen
graph continues to record `M0005-CHAIN-FREE` and `M0005-COMPONENTS` as open until master evidence
reconciliation. Pinned mathlib contains no
Eilenberg-Zilber/Alexander-Whitney product comparison, and the audited external Atlas declarations
terminate in `sorry` and mismatch the frozen target. The algebraic Kunneth maps and exactness are
also absent. Resume only when placeholder-free bodies for those branches and their exact transports
are available. This artifact is partial nonrelease evidence, not a proof receipt, checklist
transition, audit-completion claim, theorem-completion claim, or master acceptance.
