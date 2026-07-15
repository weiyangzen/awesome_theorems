# THM-M-1235 current-base proof recheck

Item: `S56-M-1235-PROOF`

Intent: `prove`

Verdict: `blocked`

Base: `db0f66d878c785ce802d44a6c3c1d7adb6d9a131`

Tree: `fe54922cd929b31f0cca2373bca0c79a487bcc17`

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

The pinned Lake route is available on this base. No `lake update`, `lake build`,
clone, fetch, checkout, network access, or `.lake` mutation was performed. The
automation-provided `.lake` symlink was reused read-only, so this remains
nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1235` | 0 | Rank 159; lifecycle `planned`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1235/check_obligation_tree.py` | 0 | 15 obligations and 37 typed edges passed; denominator `9e0bff352aff0e8315b2e5d9067ad143dcc8eb1a5fbf5f4a81ca703dcfaaf9ba`; root remains open M3. |
| `python3 Stage1_Instances/THM-M-1235/check_statement.py` | 0 | All four mutations were killed; canonical expression digest `77aec2f5...`; pinned mathlib matched. |
| `cd Formalizations/Lean && timeout --foreground --kill-after=5s 120 lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3...`. |
| Temporary trust-zero `lake env lean` compilation of copied `Statement.lean`, then `Proof.lean` | 0 | Exact statement and negative proof elaborated; both axiom reports were `[propext, Classical.choice, Quot.sound]`; olean digests `cbb0b493...` and `3af4a429...`. |
| Prohibited-construct scan of `Proof.lean` | 1 | Expected no-match exit; no prohibited construct was found. |
| Base, dependency, environment, and seven target-input identity checks | 0 | All revisions, trees, and SHA-256 values matched the JSON packet. |
| JSON parse and focused blocker-packet assertions | 0 | Packet syntax, identity, base, changed paths, blocked state, and noncompletion flags passed. |
| Tracked and per-untracked-file whitespace checks | 0 | No whitespace diagnostics; no-index checks returned only expected content differences. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is absent. |

The successful trust-zero replay copied `Statement.lean` and `Proof.lean` into a
fresh temporary directory below `Formalizations/Lean` and, from that Lake
project, obtained the pinned `LEAN_PATH` with
`lake env printenv LEAN_PATH`. It then compiled each source using
`LEAN_NUM_THREADS=1`, `timeout 600`, and
`lake env lean --trust=0 -t0 --root=... -o ...`; `Proof.lean` used the temporary
directory at the front of `LEAN_PATH`. The temporary directory was removed.

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; `flt-regular`
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`. Frozen source SHA-256 values:

- `Statement.lean`: `e59d7e8cb43f010533d3354022a042a38a27edc95337775da69c6cc8676a1697`
- `Proof.lean`: `f4afdf626cadef5e7acc9047ef8c517506de7d31fa49a9ed261f2fcc53cb6156`
- `ObligationTree.lean`: `1f244092eded09ae8a474ad4cab0bd1dadac3157c7bbde6b7d73fce4d0d24fb5`
- `obligation-registry.json`: `967ef5ce046879f2da967678e3a7353c44e69a0286804b10397fd4b446a4779e`
- `typed-graphs.json`: `a60f1a527b26db45d619fb50819be8a54804268290d9b345bf2f744bfea47e11`
- `anchor-audit.json`: `e97e800b23920f911df8fb349dfa036fba13fbed790ca104c7291e6ea536f48e`
- `validation-specs.json`: `ac97fc72f4f5eb27cacb154ea03d0bf6c9c765b081316f2fba63313465f3f081`

The temporary object digests were
`cbb0b49360973c6a3e9e45d45965f51efbadf0914f10448c5e68e2dd3654497d`
for `Statement.olean` and
`3af4a429ebac82bfe937a5acd5039cfe0984cead67492d0f9b46d41f3e761169`
for `Proof.olean`.

## Root cut set

The statement phase must be reopened. Conditions `(I)`--`(VIII)` must become
native predicates of the five functions with proof-bearing `Motion` fields.
Equality should be scoped to the source domain and `0 <= t <= T` unless the
primary source justifies global function equality. The source crosswalk,
canonical expression fingerprint, registry, typed graphs, and dependent
evidence then need a versioned re-freeze before proof execution resumes.

`S56-M-1235-OBLIGATION_TREE` is still only worker-provisional, not accepted, so
this proof node is independently dependency-blocked. Moreover, 32 earlier
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
