# THM-M-0786 proof execution blocked at 6bf9ee93

Item: `S56-M-0786-PROOF`

Base revision: `6bf9ee93a322e7d25cf9249226222095f95d1cff`

Execution date: `2026-07-16` (`Asia/Shanghai`)

## Verdict

The proof phase remains blocked at `[ ]`. No premise-free Lean declaration
inhabits the exact frozen
`Stage1Instances.THM_M_0786.BorelDeterminacyTarget`, no proof receipt is
issued, and no worker self-test manifest is written.

The required v2 dependency inspection is complete. This theorem has no direct
hard parents, transitive hard ancestors, hard edges, reuse hints, or shared
lemma groups. `dependency-reuse-ledger.json` records that empty audited closure
at graph digest `73e99d22...40eca` and context digest
`068170c7...5c5c`; the schema-1.1 validator accepts it. Consequently there is
no parent artifact capable of closing the root or transferring proof credit.

## First Failed Gate

The first failed root-critical gate is `M0786-L-BORELDET`. The immutable
external declaration `GaleStewartGame.borel_determinacy` exists in
`sven-manthe/A-formalization-of-Borel-determinacy-in-Lean` at revision
`42bc874b2357ca7e7573b31854a0d09761e11e41`, but its module is not in the
repository's pinned Lake closure. Its upstream pins also differ from the local
Lean 4.29.0 and mathlib `8a178386...ea95` pins.

A bounded, ephemeral port experiment sharpens this from a missing-module
observation to a concrete proof-chain failure. A trust-zero, placeholder-free
adapter for the full Nat game, Borel predicate, legal-position strategies, and
both winner branches elaborates; its source SHA-256 is
`7dcc9eb7be77bc07880308babfb569162692a0fbe36db40ebdd6e462ac548f16`.
That adapter is non-credit exploratory evidence because the external terminal
module is neither pinned nor kernel-available.

The earliest current no-placeholder external module that fails is
`BorelDet.Proof.Zero.lift`, source SHA-256
`a95b946edd86bcd75bdc7d52c1c0fdf869e58412d42942a43bbdc75c39df91ef`.
A fresh trust-zero compilation of this most advanced port exited 1 with two
dependent payoff-subtype diagnostics in `LLift.losable`: at line 202 `hx'`
does not acquire the `body G.tree` membership instance required by
`G.payoff`, and at line 205 the normalized prefix-plus-drop stream has not yet
been transported to `H.x ++ stream` at the expected dependent body type.
Downstream Zero and One strategy modules and the terminal
`borel_determinacy` module therefore cannot be imported or credited.

The existing
`Stage1Instances.THM_M_0786.ObligationTree.root_of_payoffSolver` does not
resolve this cut. Its `PayoffSolver` premise is definitionally the entire
canonical theorem, so replaying that conditional composer would substitute a
weaker assumed result for the requested proof.

## Validation

The automation-provided canonical `.lake` symlink was reused read-only. No
`lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was
performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0786` | 0 | rank 791; planned; L0/rework-required; theorem incomplete |
| `cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-0786/Statement.lean` | 0 | exact canonical target elaborated and printed |
| `cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-0786/check_obligation_tree.py` | 0 | 14 obligations and 44 typed edges passed; denominator `38847179...71c3`; root open at M3 |
| `cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-0786/check_anchor_audit.py` | 0 | local pin and negative inventory matched; immutable external anchor matched; root M3, candidate M5 |
| isolated `lake env which lean` trust-zero compilation of copied `Statement.lean`, then `ObligationTree.lean` with its temporary local olean | 0 | exact statement and conditional composer elaborated; the composer reports only `propext`, `Classical.choice`, and `Quot.sound` |
| `scripts.stage1_execution_cron.validate_dependency_reuse_ledger(..., expected_observed_graph_sha256=73e99d22...40eca, expected_repository_revision=6bf9ee93...d1cff)` | 0 | empty parent/ancestor/edge/hint/group closure accepted under schema 1.1 |
| scoped `rg`/artifact search of pinned mathlib, repository Lean sources, and `Formalizations/Lean/.lake` | 0 | no eligible Borel-determinacy declaration or pinned BorelDet source/olean found |
| trust-zero compile of `<temporary-port>/AdapterScratch.lean` | 0 | six substantive adapter declarations are sorry-free and depend exactly on `propext`, `choice`, and `Quot.sound`; non-credit experiment only |
| trust-zero compile of the most advanced `<temporary-port>/BorelDet/Proof/Zero/lift.lean` against its compiled prerequisites | 1 | two dependent payoff-subtype transport diagnostics in `LLift.losable`; external theorem chain remains open |
| `python3 -m json.tool` over both new JSON artifacts | 0 | both structured records parsed |
| `git diff --check -- Stage1_Instances/THM-M-0786` | 0 | no whitespace errors |

Repository-wide standard and v2 DAG checks were invoked during a heavily
concurrent scheduler tick but did not complete within the bounded worker
window. Their absence is not treated as success; the targeted manifest,
ledger, Lean, registry, anchor, JSON, and whitespace checks above are the
recorded evidence for this blocked run.

## Retry Condition

Complete the placeholder-free Lean 4.29 port beginning with
`BorelDet.Proof.Zero.lift` and every downstream Zero/One strategy and terminal
module, or provide the exact external revision in an accepted immutable
dependency closure. Then pin or vendor that closure under repository policy,
add the checked canonical adapter and a premise-free root declaration, and run
exact-type, axiom, placeholder, provenance, and composition validation.

This is current-head dependency audit and blocker evidence only. It does not
satisfy `S56-M-0786-PROOF`, change scheduler state, close any root-critical
obligation, or claim H0, M0, R0, audit completion, theorem completion,
validation, release, receipt acceptance, or master acceptance.
