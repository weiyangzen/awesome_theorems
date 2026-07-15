# THM-M-0729 proof progress at `a1ba351e` (slot52)

Item: `S56-M-0729-PROOF`

Intent: `prove`

Base revision: `a1ba351e42fd9eefe315119ef09c0b958358bb8e`

Base tree: `eed1b90627305460f9cee46277fc7c0cb235d1df`

## Verdict

`blocked`, with genuine partial proof progress. The proof item remains `[ ]`,
the lifecycle remains `planned`, and the exact root remains `[H3, M3, R4]`.
Neither directional inclusion nor `PCPTheorem` is inhabited.

`ProofProgressShortInputs.lean` adds sixteen placeholder-free declarations to the
reverse PCP-to-NP lane. It uses finiteness of binary words shorter than the
frozen threshold to bound every short-input reachable-oracle certificate by
one constant. Adding that constant to the existing eventual polynomial yields
one checked polynomial certificate bound for every input.

The module also implements a structurally recursive enumeration of every
`Fin n -> Bool` random string and a Boolean exhaustive certificate verifier.
It proves that the enumeration has exactly `2 ^ n` entries and a polynomial
global length bound under the frozen logarithmic-randomness estimate. It also
proves that the verifier returns true exactly when the decoded finite oracle is
accepted for every random string. Combining these results with perfect
completeness and half-soundness gives a global characterization:

```text
language input <-> exists binary certificate,
  certificate.length <= polynomial(input.length) /\
  exhaustiveCertificateVerifier checker input certificate = true.
```

This supplies substantive support for `M0729-B-SHORT`,
`M0729-C-CERTIFICATE`, `M0729-L-ENUMERATE`, and `M0729-D-PCP-NP`. It closes no
frozen obligation: the exhaustive verifier still lacks the bundled
`TM2ComputableInPolyTime encodePair encodeBool` implementation and cost proof
required by `PolytimeDecision`.

## Remaining Blocker

The immediate machine root cut remains `M0729-D-NP-PCP` and
`M0729-D-PCP-NP`. The forward direction still requires verifier-to-constraint
normalization, a robust gap theorem, PCP composition, logarithmic-randomness
and constant-query accounting, perfect completeness, and soundness-half
transport.

The reverse direction now has global certificate length, exhaustive random-word
enumeration, and extensional Boolean-verifier correctness. Pinned mathlib,
however, exposes only the `TM2ComputableInPolyTime` structure, its forgetful
map, and the identity implementation. The apparent composition declaration in
`Computable.lean` is a discarded `proof_wanted`, not an importable theorem.
Building the missing witness therefore requires new low-level TM2 machine
composition, loops, stack copying, and polynomial timing proofs.

The prerequisite `S56-M-0729-OBLIGATION_TREE` is provisional `[_]`, not master
accepted. The owned path also contains far more than five integrated proof
attempts while the authoritative DAG still says `attempts: 0` and
`children: []`; the integration lane should apply the mandatory split rule.

## Validation

All commands ran in this worker clone. The pre-existing untracked
`Formalizations/Lean/.lake` symlink points to canonical pinned artifacts and
was reused read-only. No `lake update`, `lake build`, dependency clone/fetch,
or `.lake` mutation was run. Lean outputs were confined to a disposable
directory outside the repository.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique targets at ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-0729` | 0 | Rank 766; `planned`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0729/check_statement.py` | 0 | Exact expression hash `2a3d6c88...7bbc5`; all four weakened mutations were distinguished. |
| `python3 Stage1_Instances/THM-M-0729/check_anchor_audit.py` | 0 | Immutable pins and hashes agreed; no exact root candidate is claimed; root M3. |
| `python3 Stage1_Instances/THM-M-0729/check_obligation_tree.py` | 0 | Passed 19 obligations and 76 typed edges; both inclusions remain open. |
| Disposable five-module `lake env lean --trust=0 -t0` replay | 0 | Statement and all four proof-progress modules elaborated; every new declaration used only `propext`, `Classical.choice`, and `Quot.sound` or a subset, with no `sorryAx`. |
| Scoped exact-PCP search over repository and pinned mathlib sources | 0 | 45 matching lines; no terminal inclusion or exact-root body; output SHA-256 `1c3fdeb2...378152`. |
| Pinned `TM2ComputableInPolyTime` API search | 0 | Only structure/forgetful map/identity plus discarded `proof_wanted`; output SHA-256 `ead503f2...8a1c0`. |
| Prohibited-device scan of `ProofProgressShortInputs.lean` | 1 expected | No `sorry`, `admit`, `axiom`, `sorryAx`, unsafe/oracle device, `external`, `implemented_by`, or `native_decide`. |
| `git diff --check -- Stage1_Instances/THM-M-0729 .stage1-worker-selftest.json` | 0 | No whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest absent because the proof phase is incomplete. |

The new Lean source SHA-256 is
`ba6d4d0f9459bab2effdd18344ef565eea77b2fd52518a3e1a5687c42edc1297`;
its disposable olean SHA-256 is
`c4582661ae8246aff98bbb116fbcad2dd77392a291f3fed954b8b909496410de`.

## Reopen Condition

Split the oversized item into dependency-legal children. For the reverse lane,
implement and prove polynomial-time the TM2 machine realizing the checked
exhaustive verifier. Separately implement the complete forward PCP packages,
or integrate an immutable compatible exact terminal proof with complete
provenance.

This is nonrelease partial-progress evidence. It does not satisfy
`S56-M-0729-PROOF`, close an obligation or the root, promote scheduler state,
or claim audit completion, validation, release, theorem completion, receipt
acceptance, or master acceptance. Because the assigned proof phase is not
genuinely complete, `.stage1-worker-selftest.json` remains absent.
