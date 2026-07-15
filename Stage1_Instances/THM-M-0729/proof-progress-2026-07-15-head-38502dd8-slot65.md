# THM-M-0729 proof progress at `38502dd8` (slot65)

Item: `S56-M-0729-PROOF`

Intent: `prove`

Base revision: `38502dd8cfdb1c7b89d62d802952ab596838ec7e`

Base tree: `334fd05726c0b982153d6aec154745629a2c9bc1`

## Verdict

`blocked`, with genuine partial proof progress. The proof item remains `[ ]`,
the lifecycle remains `planned`, and the exact root remains `[H3, M3, R4]`.
Neither directional inclusion nor `PCPTheorem` is inhabited.

`ProofProgress.lean` adds five placeholder-free support declarations. The
central result proves from the exact finite-cardinality `HasSoundnessHalf`
definition that a proof accepted for every random string forces language
membership. Together with perfect completeness this gives

```text
language input <-> exists proof, forall coins, checker.accepts input proof coins = true.
```

The rejection formulations prove that each proof oracle for a no-instance is
rejected on some random string. These arguments include zero randomness: the
type `Fin 0 -> Bool` has one inhabitant, so soundness is not vacuous. This is
provisional support for the frozen boundary package and the reverse inclusion;
it does not close a frozen obligation. In particular, it does not close
`M0729-L-SOUND`, whose output must establish the half-soundness inequality from
the forward PCP gap theorem rather than consume that inequality as a premise.

## Remaining blocker

The immediate root cut is unchanged:

- `M0729-D-NP-PCP` still requires verifier-to-constraint normalization, a
  robust gap theorem, PCP composition, logarithmic randomness and constant
  query accounting, perfect completeness, and soundness-one-half transport.
- `M0729-D-PCP-NP` still requires a finite consistent oracle-bit certificate,
  exhaustive enumeration of all random strings, polynomial certificate and
  runtime bounds including the below-threshold branch, and an actual bundled
  `TM2ComputableInPolyTime encodePair encodeBool` verifier witness.

Pinned mathlib provides deterministic Turing-machine and finite-cardinality
infrastructure, but no NP/PCP theory or terminal PCP theorem. It provides only
the identity polynomial-time machine at the needed level. The apparent
`Turing.TM2ComputableInPolyTime.comp` is a discarded source `proof_wanted` at
`Computable.lean:284`; querying it reports `Unknown constant`, so even ordinary
polynomial-time machine composition must be implemented before the reverse
verifier can be assembled.

The prerequisite `S56-M-0729-OBLIGATION_TREE` is provisional `[_]`, not master
accepted. That separately prevents proof-node master acceptance.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink was reused read-only. No `lake update`,
`lake build`, dependency clone/fetch/checkout, network request, or `.lake`
mutation was performed. Lean outputs were written only to disposable `/tmp`
directories and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 uniform-L0 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique targets at ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-0729` | 0 | Rank 766, `planned`, legacy artifacts unaccepted, theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0729/check_statement.py` | 0 | Exact expression hash `2a3d6c88...7bbc5`; four weakened mutations were distinguished. |
| `python3 Stage1_Instances/THM-M-0729/check_anchor_audit.py` | 0 | Immutable pins and source hashes agreed; no exact root candidate is claimed; root M3. |
| `python3 Stage1_Instances/THM-M-0729/check_obligation_tree.py` | 0 | Passed 19 obligations and 76 typed edges; both inclusions remain open. |
| Disposable combined `lake env lean --trust=0 -t0` replay | 0 | `Statement`, conditional `ObligationTree`, `ProofProgress`, and `ProofBlockerProbe` elaborated against pinned artifacts. All new declarations reported exactly `propext`, `Classical.choice`, and `Quot.sound`; the unavailable composition application failed as expected. |
| Scoped repository and all-pinned-package PCP source search | 0 | Exact probabilistic-PCP declarations remain confined to this dossier; no terminal inclusion or root body was found. Search output SHA-256: `78d4ddf3...57b2`. |
| `#print Turing.TM2ComputableInPolyTime.comp` | 1 expected | Pinned Lean reported `Unknown constant`; the source has only the discarded `proof_wanted`. |
| Prohibited-device scan over `ProofProgress.lean` | 1 expected | No `sorry`, `admit`, `sorryAx`, bodyless declaration, unsafe/oracle device, `native_decide`, or `implemented_by` was found. |

The combined replay produced disposable olean hashes
`5bc6f394...4dced` (`Statement`), `aaab13dc...0dd9`
(`ObligationTree`), and `0ab15a65...612` (`ProofProgress`). The new source
hash is `61a6352e...109`.

## Reopen condition

Implement both frozen inclusions and all required reduction, machine,
resource, certificate, enumeration, and boundary packages without
placeholders. Alternatively, integrate an immutable compatible terminal Lean
proof with exact-type transport and complete provenance, then rerun trust,
placeholder, composition, and node-specific validation.

This is nonrelease partial-progress evidence. It does not satisfy the assigned
proof item, authoritatively close an obligation, promote scheduler state, or
claim audit completion, validation, release, theorem completion, receipt
acceptance, or master acceptance. Because the positive proof phase is not
complete, `.stage1-worker-selftest.json` is deliberately absent.
