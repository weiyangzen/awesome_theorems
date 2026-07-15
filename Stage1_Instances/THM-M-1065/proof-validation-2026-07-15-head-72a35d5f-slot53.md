# THM-M-1065 partial proof validation at `72a35d5f`

Item: `S56-M-1065-PROOF`

Worker: Stage1 rev-5.6 slot53

Date: `2026-07-15T08:24:00+08:00`

Base revision: `72a35d5f64e32233c0bc77a57e47bd078475ad74`

Base tree: `a80eb91ed5629dee62d031e78bc87b509cf8e6eb`

## Result

The proof phase has new, placeholder-free partial progress. `Proof.lean` now proves
`measurableSet_discrepancyEvent`: for genuinely measurable increments, every frozen finite-horizon
running-discrepancy event is measurable. The proof expresses the bounded existential over
`1 <= k <= n` as a finite union and checks each summand using measurability of finite sums,
subtraction, absolute value, and a strict real inequality.

The same isolated replay revalidated `exists_commonIIDSequences`, which constructs on one infinite
product carrier an iid input-law sequence and an iid standard-Gaussian sequence. Both declarations
elaborated at trust level zero and reported exactly `propext`, `Classical.choice`, and `Quot.sound`.

These are partial proof bodies, not KMT. The product construction makes the two families mutually
independent rather than KMT-dependent and supplies no logarithmic discrepancy estimate. The event
lemma assumes `Measurable` increments; `HasLaw` alone carries only `AEMeasurable`. More importantly,
the frozen C-SPACE and EVENT-MEAS nodes have only planned textual fingerprints, no exact Lean
interfaces or terminal body IDs, and pending validation specifications. No checked composition
binds these bodies to one eventual KMT witness. Therefore this packet truthfully claims zero frozen
obligations closed, leaves the root `[H2, M4, R4]`, and keeps `theorem_complete=false`.

## Commands

All Lean checks reused the pre-existing automation-provided pinned Lake artifacts. No `lake update`,
`lake build`, dependency clone/fetch, or dependency mutation was run.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1065` | 0 | rank 507; planned hard-mathlib-anchor-and-wrapper lane; theorem incomplete |
| `bash Stage1_Instances/THM-M-1065/check_proof.sh` | 0 | isolated `Statement.lean -> Proof.lean` replay at `--trust=0 -t0`; both local declarations checked with exactly the allowed three axioms |
| `python3 Stage1_Instances/THM-M-1065/check_anchor_audit.py` | 0 | pinned mathlib substrate verified; no exact terminal KMT candidate credited |
| `python3 Stage1_Instances/THM-M-1065/check_obligation_tree.py` | 0 | 18 obligations and 75 typed edges passed; denominator `d5e21a3a...91ac2`; root open M4 |
| `rg -n -i --pcre2 '\b(?:Koml[oó]s|Tusn[aá]dy|KMT)\b|strong[ _-](?:approximation|invariance)' Formalizations/Lean/.lake/packages --glob '*.lean'` | 1 | expected no-match result; no KMT proof source found in the pinned package closure |
| prohibited-construct scan over owned `*.lean` | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, axiom/constant/opaque/unsafe/extern escape, `implemented_by`, `run_tac`, or `native_decide` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and status | 0 | mathlib `8a178386...ea95`, tree `bdc39a31...1c2b`, dependency worktree clean |
| receipt/blocker/self-test JSON validation and invariant assertions | 0 | identities, base, hashes, open-state boundary, zero closure credit, exact cut set, and changed paths agreed |
| `git diff --check -- Stage1_Instances/THM-M-1065 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The legacy `check_statement.py` performs five serial full elaborations and was interrupted during a
contention-heavy redundant recheck. This packet does not rely on that wrapper: the isolated proof
recipe compiled the exact unchanged `Statement.lean` first, and the canonical expression digest is
bound from the frozen prerequisite artifact. No temporary target-local file remains.

## Blocker

The first unavailable root-relevant construction remains `M1065-C-SPACE`: a dependent KMT
common-space coupling with both prescribed iid marginals. The quantitative finite-block coupling
and uniform exponential maximal-tail proof are also absent. The conservative root cut set is
`M1065-C-SPACE`, `M1065-L-BLOCK-COUPLING`, and `M1065-L-MAXIMAL-TAIL`.

At least six prior integrated unresolved proof ticks exist while scheduler authority still records
`attempts=0` and `children=[]`. Under the rev-5.6 split-after-five rule, the master should replace
another whole-root retry with dependency-legal child assignments and exact typed interfaces. This
worker did not edit scheduler or generated checklist authority.

## Status Boundary

This is self-tested partial proof evidence proposing worker state `[_]`, not an accepted proof
receipt. It does not satisfy `S56-M-1065-PROOF`, close a frozen obligation or the root, change
accepted state, or claim audit completion, theorem completion, validation, release, or master
acceptance.
