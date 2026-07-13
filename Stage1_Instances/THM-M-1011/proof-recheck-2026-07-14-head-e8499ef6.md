# THM-M-1011 proof recheck at `e8499ef6`

Item: `S56-M-1011-PROOF`

Date: `2026-07-14` (`Asia/Shanghai`)

Base revision: `e8499ef6898f9562fb480587db7eb9220c04b6fc`

Base tree: `d88a39b243dd6a835f2e7463b9805d1cb175fb80`

## Verdict

`blocked`. This current-base retry located no eligible proof body for the exact
target `Stage1Instances.THM_M_1011.CanonicalStatement`. Its forward implication
remains cut at `M1011-N-SEPARATION`: the frozen context provides a complete,
second-countable `PseudoMetricSpace X`, but it does not provide `T2Space X`.
The only located pinned tightness-to-compactness declaration,
`MeasureTheory.isCompact_closure_of_isTightMeasureSet`, explicitly requires
that additional instance.

`ObligationTree.lean` contains three genuine placeholder-free bodies.
`compact_to_tight` proves the exact reverse implication.
`tight_to_compact_of_t2` proves the forward implication only after accepting an
explicit `T2Space X` dictionary, and `canonical_of_t2` composes both directions
under the same extra premise. Neither conditional declaration inhabits the
frozen root, so returning it would strengthen or substitute the theorem.

A separation-quotient route remains mathematically plausible but is not a
ready pinned wrapper. Mathlib supplies a metric and completeness instance for
`SeparationQuotient X`, an open quotient map, second-countability descent, and
tightness under measure mapping. The bounded audit located no corresponding
probability-measure equivalence or transport of weak closure compactness back
to the original measure space. Constructing those transports is substantive
proof work and requires a versioned change to the frozen proof architecture.
No counterexample was established; the result here is unsupported, not false.

No proof body or accepted receipt was added. The root vector remains
`[H1, M5, R4]`; `proof_phase_complete=false`, `root_closed=false`,
`audit_complete=false`, and `theorem_complete=false`. The proof item remains
`[ ]`. Because the positive proof deliverable is not genuinely self-tested as
complete, `.stage1-worker-selftest.json` is deliberately absent.

## Validation

All checks reused the automation-provided canonical pinned `.lake` artifacts
read-only. No `lake update`, `lake build`, dependency clone/fetch, network
operation, or `.lake` mutation was performed. The untracked `.lake` symlink
makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1011` | 0 | rank 260; planned hard-mathlib-anchor-and-wrapper lane; theorem incomplete |
| `env LEAN_NUM_THREADS=1 python3 Stage1_Instances/THM-M-1011/check_statement.py` | 0 | expression `5711575e...e812`; all four mutations killed; real time 143.53 s |
| `env LEAN_NUM_THREADS=1 python3 Stage1_Instances/THM-M-1011/check_anchor_audit.py` | 0 | four candidates; root M5; forward anchor displayed its `T2Space E` premise; real time 21.40 s |
| `python3 Stage1_Instances/THM-M-1011/check_obligation_tree.py` | 0 | 14 obligations, 35 typed edges, denominator `3dd41add...bdd90`; exact root open M5 |
| isolated trust-zero Lean recipe below | 0 | exact statement, reverse implication, and two conditional bodies elaborated; `canonical_of_t2` reported `[propext, Classical.choice, Quot.sound]` |
| prohibited-construct scan of `Statement.lean` and `ObligationTree.lean` | 0 wrapper | no `sorry`, `admit`, custom `axiom`, `sorryAx`, `unsafe`, `implemented_by`, `native_decide`, or `external` token |
| source/environment hashes and pinned mathlib identity | 0 | all hashes matched the structured recheck record; mathlib `8a178386...a95`, tree `bdc39a31...b2b` |
| JSON parsing and blocker invariant checks | 0 | selected structured records parsed and blocked/open flags agreed |
| `git diff --check -- Stage1_Instances/THM-M-1011` | 0 | no whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion manifest deliberately absent |

The isolated replay wrote only to a disposable `/tmp` directory and removed it
with a shell trap:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-1011
tmp=$(mktemp -d /tmp/thm-m-1011-proof-recheck-head-e8499ef6.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$target"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  "$lean" --trust=0 -t0 -o "$tmp/Statement.olean" Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  "$lean" --trust=0 -t0 ObligationTree.lean
```

The output hashes were `28074606...d6d5b5` for the statement log,
`8136e407...683272` for the obligation log, and `0299007a...8f613e` for
the temporary `Statement.olean`. Frozen source SHA-256 values were
`6bf24878...1d66` for `Statement.lean`, `4395f2cb...7c9d` for
`ObligationTree.lean`, `e427e163...aaa40` for the registry, and
`7d75a5b6...a93a2` for the anchor audit.

One earlier statement-validator attempt encountered a transient Lake
dependency Git-resolution error during heavy concurrent validation. The
recorded serial rerun succeeded and its temporary source was removed.

## Known Predecessor Gaps

The prerequisite items are worker-provisional `[_]`, not master-accepted
`[x]`. Existing public metadata also remains inconsistent: `README.md` retains
older intake wording and `[H2, M4, R4]` before later reporting M5;
`anchor-audit.json` says R3 while the instance and graph boundary say R4; and
the instance's owned-artifact inventory omits several already-present
validation and proof-evidence files. This proof-only attempt does not silently
rewrite predecessor-phase authority.

## Retry Condition

Resume after a placeholder-free proof of the exact non-T2 forward implication
and a versioned proof-architecture update, or reopen the statement phase and
re-freeze the intended Polish-space claim with `MetricSpace X` or explicit
`T2Space X`, then rerun every downstream gate.

This append-only artifact is blocker evidence, not a proof receipt. It does
not satisfy `S56-M-1011-PROOF`, propose checklist state, or support audit,
theorem, validation, release, or master-completion claims.
