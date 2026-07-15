# THM-M-0729 proof progress at `e57cfb09` (slot54)

Item: `S56-M-0729-PROOF`

Intent: `prove`

Base revision: `e57cfb0904e8a827b17320aba51bd41b96109c7c`

Base tree: `79ab3544eee575a45c51d85923144ed20f607f9e`

## Verdict

`blocked`, with genuine partial proof progress. `ProofProgressSerialization.lean`
adds placeholder-free bodies for a literal binary serialization of the finite
reachable proof oracle introduced by `ProofProgressCardinality.lean`. The proof
item remains `[ ]`, the lifecycle remains `planned`, and the root remains
`[H3, M3, R4]`. Neither directional inclusion nor `PCPTheorem` is closed.

The new development deterministically orders the reachable oracle positions,
encodes their Boolean assignment as a `Word`, and decodes a word back into an
assignment. It proves both exact-length round trips and injectivity. It then
strengthens the earlier semantic bridge to the exact statement that universal
oracle acceptance is equivalent to the existence of a binary certificate of
length

```text
(queriedPositions checker input).card.
```

Finally it defines the explicit polynomial

```text
((X + 1) ^ randomConstant) * C queryConstant
```

and proves that logarithmic randomness plus the constant query bound makes the
serialized certificate no longer than its evaluation on every input above the
frozen threshold. This is substantive support for `M0729-C-CERTIFICATE` and the
reverse direction. It does not close the frozen construction node because no
executable polynomial-time verifier or short-input branch is present.

## Remaining Blocker

The immediate machine root cut remains `M0729-D-NP-PCP` and
`M0729-D-PCP-NP`. The forward direction still requires verifier-to-constraint
normalization, the robust gap theorem, PCP composition, resource accounting,
perfect completeness, and soundness-half transport. The reverse direction now
has a checked, polynomially short binary certificate on the eventual branch,
but still lacks exhaustive verification of every random word, a bundled
`TM2ComputableInPolyTime encodePair encodeBool` witness, and the below-threshold
branch.

Pinned mathlib provides only the identity implementation at the
`TM2ComputableInPolyTime` level. Its apparent composition result is a discarded
source `proof_wanted` marker, not an importable declaration. An independent
read-only discovery query found
`facebookresearch/atlas-lean@34ffed396f376454c1a9b297f3fd74c5c801fb50`,
`Atlas/BooleanFunctions/code/PCP.lean`, declaration
`PCP.pcp_theorem_gap3SAT`. It cannot supply proof credit: its body is
`by sorry`, its reduction predicate is opaque, and its Gap3SAT target is not
the frozen class equality. It was not fetched or integrated.

The prerequisite `S56-M-0729-OBLIGATION_TREE` is provisional `[_]`, not master
accepted. That independently prevents proof-node master acceptance. The owned
path also contains many integrated blocker/recheck packets while the
authoritative DAG still records `attempts: 0` and no children. The integration
lane should apply the mandatory split rule rather than continue assigning this
monolithic proof item.

## Validation

All commands ran in this worker clone. The pre-existing untracked
`Formalizations/Lean/.lake` symlink points to canonical pinned artifacts and
was reused read-only. No `lake update`, `lake build`, dependency
clone/fetch/checkout, or `.lake` mutation was performed. Lean outputs were
confined to a disposable directory and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique targets at ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-0729` | 0 | Rank 766; `planned`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0729/check_statement.py` | 0 | Exact expression hash `2a3d6c88...7bbc5`; all four weakened mutations were distinguished. |
| `python3 Stage1_Instances/THM-M-0729/check_anchor_audit.py` | 0 | Immutable pins and hashes agreed; no exact root candidate is claimed; root M3. |
| `python3 Stage1_Instances/THM-M-0729/check_obligation_tree.py` | 0 | Passed 19 obligations and 76 typed edges; both inclusions remain open. |
| Disposable `lake env lean --trust=0 -t0` replay of `Statement.lean`, `ProofProgressCardinality.lean`, and `ProofProgressSerialization.lean` | 0 | All modules elaborated against pinned artifacts; every new declaration used only `propext`, `Classical.choice`, and `Quot.sound` or a subset, with no `sorryAx`. |
| Scoped exact-PCP search over repository and pinned mathlib Lean sources | 0 | 38 matching lines; no terminal inclusion or exact-root body was found; output SHA-256 `08bbb8df...9ec79`. |
| Pinned `TM2ComputableInPolyTime` API inventory | 0 | All hits are the structure/forgetful map, identity implementation, or discarded `proof_wanted` composition marker. |
| Prohibited-device scan of `ProofProgressSerialization.lean` | 1 expected | No `sorry`, `admit`, `axiom`, `sorryAx`, unsafe/oracle device, `external`, `implemented_by`, or `native_decide` occurred. |
| JSON parse plus blocked-progress invariant assertion | 0 | The paired artifact binds this item/base with false proof, root, audit, theorem, and self-test flags. |
| Scoped diff checks | 0 | The three new owned artifacts have no whitespace errors; no tracked unrelated path changed. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The completion manifest is absent because the proof phase is incomplete. |

`ProofProgressSerialization.lean` has SHA-256
`a8bfca6eda69d31f95367ae74213644c108de147daaa76317f2e733dcd99d39e`.
The disposable `Statement.olean`, `ProofProgressCardinality.olean`, and
`ProofProgressSerialization.olean` hashes were respectively
`171bd814...6591`, `c936e813...3944`, and `a2d93fc2...ad00`.

## Reopen Condition

Split the oversized item into dependency-legal children, then implement both
frozen inclusions. For the reverse lane, continue from the serialized
certificate by building exhaustive verification, its polynomial-time TM2
witness, and the short-input branch. Alternatively, integrate an immutable,
compatible terminal Lean proof with exact-type transport and complete
provenance.

This is nonrelease partial-progress evidence. It does not satisfy
`S56-M-0729-PROOF`, close an obligation or the root, promote scheduler state,
or claim audit completion, validation, release, theorem completion, receipt
acceptance, or master acceptance. Because the assigned phase is not genuinely
self-tested complete, `.stage1-worker-selftest.json` remains absent.
