# THM-M-0729 proof progress at `88a5a5c6` (slot59)

Item: `S56-M-0729-PROOF`

Intent: `prove`

Base revision: `88a5a5c6fe6bac0d813a74ca20fa553eaf2a6d68`

Base tree: `a0a75048a918a3bf566c3dbcf6b4352c3b2ee8e4`

## Verdict

`blocked`, with genuine partial proof progress. `ProofProgressCardinality.lean`
adds placeholder-free bodies for the finite-randomness and finite-certificate
bridge needed by the reverse PCP-to-NP direction. The proof item remains `[ ]`,
the lifecycle remains `planned`, and the root remains `[H3, M3, R4]`. Neither
directional inclusion nor `PCPTheorem` is closed.

The new development proves that random words have their indexed length and
that the random space has cardinality `2 ^ r`. It defines the finite set of all
oracle positions reachable on a fixed input, proves that a checker depends only
on those positions, replaces an arbitrary total proof oracle by a finite
assignment without changing universal acceptance, counts those assignments,
and bounds the reachable-position set by

```text
2 ^ checker.randomLength input * queryConstant.
```

It also derives the exact accepting-versus-rejecting cardinality consequence
of `HasSoundnessHalf`, its exponential form, and existence of rejecting coins
for a no-instance. These results give substantive support for
`M0729-C-CERTIFICATE`, `M0729-L-ENUMERATE`, `M0729-S-BOUNDARY`, and
`M0729-D-PCP-NP`; they do not close any frozen obligation because certificate
serialization, polynomial bounds, and a bundled polynomial-time verifier are
still absent.

## Remaining Blocker

The immediate machine root cut remains `M0729-D-NP-PCP` and
`M0729-D-PCP-NP`. The forward direction still requires verifier-to-constraint
normalization, the robust gap theorem, PCP composition, resource accounting,
perfect completeness, and soundness-half transport. The reverse direction now
has a checked finite-oracle semantic reduction, but still lacks a binary
certificate encoding, exhaustive verifier implementation and cost proof, the
below-threshold branch, and an actual
`TM2ComputableInPolyTime encodePair encodeBool` witness. Pinned mathlib has no
NP/PCP development, terminal PCP theorem, or retained polynomial-time
composition declaration; the apparent composition result remains only a
source `proof_wanted` marker.

The prerequisite `S56-M-0729-OBLIGATION_TREE` is provisional `[_]`, not master
accepted. That independently prevents proof-node master acceptance. The owned
path also contained seventeen integrated blocker/recheck JSON packets before
this run, while the authoritative DAG still records `attempts: 0` and no
children. The integration lane should apply the mandatory split rule rather
than continue assigning this monolithic proof item.

## Validation

All commands ran in this worker clone. The pre-existing untracked
`Formalizations/Lean/.lake` symlink points to canonical pinned artifacts and
was reused read-only. No `lake update`, `lake build`, dependency
clone/fetch/checkout, or `.lake` mutation was performed. Lean outputs were
confined to disposable directories and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique targets at ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-0729` | 0 | Rank 766; `planned`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0729/check_statement.py` | 0 | Exact expression hash `2a3d6c88...7bbc5`; all four weakened mutations were distinguished. |
| `python3 Stage1_Instances/THM-M-0729/check_anchor_audit.py` | 0 | Immutable pins and hashes agreed; no exact root candidate is claimed; root M3. |
| `python3 Stage1_Instances/THM-M-0729/check_obligation_tree.py` | 0 | Passed 19 obligations and 76 typed edges; both inclusions remain open. |
| Disposable `lake env lean --trust=0 -t0` replay of `Statement.lean` then `ProofProgressCardinality.lean` | 0 | Both modules elaborated against pinned artifacts; all eleven printed declarations used only `propext`, `Classical.choice`, and `Quot.sound` or a subset, with no `sorryAx`. |
| Scoped exact-PCP search over repository and pinned mathlib Lean sources | 0 | 27 matching lines; exact probabilistic-PCP declarations remained confined to this dossier, with only conditional root assembly and no terminal directional body; output SHA-256 `33a78b16...bb91a`. |
| Prohibited-device scan of `ProofProgressCardinality.lean` | 1 expected | No `sorry`, `admit`, `axiom`, `sorryAx`, `unsafe`, `implemented_by`, or `native_decide` occurred. |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-0729/ProofProgressCardinality.lean` with expected new-file diff normalized | 0 | No whitespace errors. |

The new source SHA-256 is
`6fab3e0769ab3ab156e2113bbac895b52a8d9b0f375332ce8bfaef46e245fe52`.
The disposable `Statement.olean` and `ProofProgressCardinality.olean` hashes
were `171bd814...6591` and `c936e813...3944`, respectively.

## Reopen Condition

Split the oversized item into dependency-legal children, then implement both
frozen inclusions. For the reverse lane, continue from the finite assignment by
serializing it into a polynomially bounded binary certificate, building the
exhaustive verifier and its polynomial runtime witness, and handling short
inputs. Alternatively, integrate an immutable compatible terminal Lean proof
with exact-type transport and complete provenance.

This is nonrelease partial-progress evidence. It does not satisfy
`S56-M-0729-PROOF`, close an obligation or the root, promote scheduler state,
or claim audit completion, validation, release, theorem completion, receipt
acceptance, or master acceptance. Because the assigned phase is not genuinely
self-tested complete, `.stage1-worker-selftest.json` remains absent.
