# THM-M-1011 proof-phase validation

Item: `S56-M-1011-PROOF`

Base revision: `499a718cc7926abaf61e9721fe0d7485059403e6`

Validation date: `2026-07-14` (`Asia/Shanghai`)

## Implemented proof

`Proof.lean` proves the exact frozen
`Stage1Instances.THM_M_1011.CanonicalStatement` without adding `T2Space X` or
replacing the pseudometric domain.  It passes from `X` to
`SeparationQuotient X`, which carries the required metric, completeness, and
second-countability instances.

The quotient map has a choice of representatives.  Because the quotient map
is inducing and its composite with this representative map is the identity,
the representative map is continuous.  Pushforward along the two maps gives a
homeomorphism between the spaces of Borel probability measures.  The inverse
law on `X` uses the fact that a Borel set cannot distinguish topologically
inseparable points.  Uniform tightness maps forward to the quotient; pinned
mathlib Prokhorov gives compact closure there; the homeomorphism transports
compactness back.  The reverse implication is the existing pinned mathlib
body.

The exact root is therefore kernel inhabited by a repo-local proof.  Lean's
trust-zero axiom report is exactly `propext`, `Classical.choice`, and
`Quot.sound`; there is no `sorryAx`.

## Frozen boundary

The earlier `proof-blocker.json`, `proof-validation.md` content, and
`proof-recheck-2026-07-14-head-e8499ef6.{json,md}` truthfully described bounded
attempts made before this quotient proof was discovered.  This receipt
supersedes them as the current proof-phase result; they remain historical
evidence and are not positive receipts.

The frozen registry already represents `M1011-N-SEPARATION` as the required
semantic reduction, and this proof supplies it without changing the statement
or denominator.  Its typed graph and prose projection name only the previously
known direct-`T2Space X` route.  They remain immutable pre-proof artifacts;
the integration or downstream validation lane must reconcile the successful
quotient route and its terminal proof bodies before accepting graph closure.
The proof phase proposes `[_]` only.  `H0`, `R0`, complete transitive trust,
audit completion, validation, release, theorem completion, and master
acceptance are not claimed.

## Commands and results

All commands ran inside the worker clone.  The automation-provided `.lake`
symlink to the canonical pinned artifacts was reused read-only.  No update,
build, clone, fetch, network operation, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1011` | 0 | rank 260; planned; L0/rework-required; theorem-complete false |
| isolated `Statement.lean` then `Proof.lean` replay using `lake env which lean`, pinned `LEAN_PATH`, `LEAN_NUM_THREADS=1`, `--trust=0`, `-t0`, and a disposable `/tmp/Statement.olean` | 0 | exact quotient proof elaborated; `canonical` reported `[propext, Classical.choice, Quot.sound]` |
| two independent isolated trust-zero replays of the same owned proof source | 0 each | both reviewers obtained the same exact axiom set and no instance/coherence errors |
| `python3 Stage1_Instances/THM-M-1011/check_proof.py` | 0 | exact declaration inventory, frozen input hashes, receipt boundary, and prohibited-token checks passed |
| `python3 Stage1_Instances/THM-M-1011/check_obligation_tree.py` | 0 | frozen 14-obligation, 35-edge architecture passed; its pre-proof projection remained open M5 as expected |
| prohibited-construct scan over `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom/unsafe declaration, `implemented_by`, `native_decide`, or external declaration |
| `python3 -m json.tool` on the proof receipt, frozen structured artifacts, and worker packet | 0 | all selected JSON parsed |
| `git diff --check -- Stage1_Instances/THM-M-1011 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Environment and hashes

```text
Lean 4.29.0, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740
mathlib 8a178386ffc0f5fef0b77738bb5449d50efeea95
mathlib tree bdc39a3123201dae413a9d9be56ec242c19e5c2b

6bf24878f5041dc4aa1e7365b8a0c2b5c7d8fb65fe5ee389597081a8c9511d66  Statement.lean
4395f2cb5f788f3fd9ae19fabfd97659d4edeef88eafb952f1a80f03d2c17c9d  ObligationTree.lean
f8b6582c52e409df8fbace88d59fe8300efc018f07a40bf8f10a43aad75413ed  Proof.lean
e427e1638975db782747232bd2dcd9382df41424df592d94035dec05b31aaa40  obligation-registry.json
38b9505f9643c6a2bac4fd8f65d4723d031cfb18a26d905197bfd4d833819895  typed-graphs.json
```

## Status boundary

This is provisional, current-base, self-tested proof-node evidence.  The exact
root is locally kernel closed, but no scheduler state or generated checklist
was edited.  Only the integration lane may accept the receipt or reconcile the
frozen architecture, and downstream gates still keep `theorem_complete=false`.
