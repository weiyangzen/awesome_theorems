# THM-M-1235 current-base proof recheck

Item: `S56-M-1235-PROOF`

Intent: `prove`

Verdict: `blocked`

Base: `db0c298049d1dde29478ee95e1fe6f30c6fbf803`

Tree: `2a16d30ab1d6b3870e8eccdbb207a5cde55b2426`

## First failed gate

`S56-5.1-EXACT-TARGET-CONSISTENCY / M1235-S-DEFINITIONS` fails. The
frozen `Motion` structure stores conditions `(I)`--`(VIII)` as values of type
`Prop`; it does not store predicates of the five functions or proofs of those
predicates. The functions are therefore unconstrained. `SameMotion` nevertheless
requires equality of all five complete functions.

The existing placeholder-free declaration
`Stage1Instances.THMM1235.not_wolibnerGlobalExistenceAndUniqueness` changes an
alleged unique motion's `velocityX` to `velocityX + 1` while preserving every
other field. The result is another `Motion`, but evaluation at `(0, 0), 0`
contradicts `SameMotion`. Lean checks the exact negative type:

```text
Not Stage1Instances.THMM1235.WolibnerGlobalExistenceAndUniqueness
```

Consequently no positive proof body for the frozen proposition can be added in
a consistent Lean environment. This refutes the encoding, not Wolibner's
mathematical theorem. The proof phase remains `[ ]`; no completion self-test is
permitted.

## Current-base validation

The pinned Lake route is available on this base. Unlike the immediately prior
slot-16 packet, `flt-regular` now has a clean detached `HEAD` at its manifest
revision. No `lake update`, `lake build`, clone, fetch, checkout, network access,
or `.lake` mutation was performed. The automation-provided `.lake` symlink was
reused read-only, so this remains nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1235` | 0 | Rank 159; lifecycle `planned`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1235/check_obligation_tree.py` | 0 | 15 obligations and 37 typed edges passed; root remains open M3; existence and uniqueness remain M4. |
| `cd Formalizations/Lean && timeout 300 lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3...`. |
| `python3 Stage1_Instances/THM-M-1235/check_statement.py` | 0 | All four mutations were killed; canonical expression digest `77aec2f5...`; pinned mathlib matched. |
| Temporary trust-zero `lake env lean` compilation of copied `Statement.lean`, then `Proof.lean` | 0 | Exact statement and negative proof elaborated; both axiom reports were `[propext, Classical.choice, Quot.sound]`; olean digests `cbb0b493...` and `3af4a429...`. |
| Prohibited-construct scan of `Proof.lean` | 1 | Expected no-match exit; no prohibited construct was found. |
| Base, dependency, environment, and seven target-input identity checks | 0 | All revisions, trees, and SHA-256 values matched the JSON packet. |
| JSON parse and focused blocker-packet assertions | 0 | Packet syntax, identity, base, changed paths, blocked state, and noncompletion flags passed. |
| Tracked and per-untracked-file whitespace checks | 0 | No whitespace diagnostics; no-index checks returned only expected content differences. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is absent. |

The narrow trust-zero recipe copied only the two source files into a temporary
directory, then ran `lake env lean --trust=0 -t0 --root=... -o ...` from
`Formalizations/Lean`, setting `LEAN_PATH` to the temporary directory for the
second compilation. The temporary directory was removed afterward.

## Root cut set

The statement phase must be reopened. Conditions `(I)`--`(VIII)` must become
native predicates of the five functions with proof-bearing `Motion` fields.
Equality should be scoped to the source domain and `0 <= t <= T` unless the
primary source justifies global function equality. The source crosswalk,
canonical expression fingerprint, registry, typed graphs, and dependent
evidence then need a versioned re-freeze before proof execution resumes.

`S56-M-1235-OBLIGATION_TREE` is still only worker-provisional, not accepted, so
this proof node is independently dependency-blocked. Moreover, 30 earlier
structured proof-recheck JSON packets are present while the authoritative DAG
still records `attempts=0` and no children. The master/scheduler should
reconcile that history and apply the section 10.2 split/reopen rule rather than
schedule another identical proof-only retry.

## Status boundary

This packet adds negative, nonrelease blocker evidence only. It adds no proof
body, closure, graph edge, composition certificate, receipt, or state change.
It does not satisfy `S56-M-1235-PROOF`, audit completion, theorem completion,
validation, release, or master acceptance. Because the assigned phase is not
genuinely complete, `.stage1-worker-selftest.json` is deliberately absent.
