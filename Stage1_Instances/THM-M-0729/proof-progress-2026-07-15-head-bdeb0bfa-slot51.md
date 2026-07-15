# THM-M-0729 proof progress at `bdeb0bfa` (slot51)

Item: `S56-M-0729-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T22:10:26+08:00`

Base revision: `bdeb0bfae66ccfe8b672776c61bc4c74a25bef3d`

Base tree: `440ac842583ec6b7aa7be989ba908e8b745978b9`

## Verdict

`blocked`, with genuine partial proof progress. The assigned proof item remains
`[ ]`, the lifecycle remains `planned`, and the exact root remains
`[H3, M3, R4]`. Neither directional inclusion nor
`Stage1Instances.THM_M_0729.PCPTheorem` is closed.

`ProofProgressReverseBridge.lean` adds six placeholder-free declarations at
the current reverse-direction frontier. It defines the pair-uncurried exhaustive
certificate decision required by `PolytimeDecision`, proves its reduction to
the checked exhaustive verifier, and proves that a polynomial-time TM2
implementation of this exact Boolean decision is sufficient to construct the
frozen `InNP` witness. A dependency-local theorem packages both the existing
polynomial certificate characterization and the remaining machine premise.

This is substantive conditional assembly for `M0729-D-PCP-NP`. It deliberately
does not postulate or manufacture `PolytimeDecision`, so it closes no frozen
obligation. Its exact remaining premise is:

```text
PolytimeDecision (exhaustiveCertificateDecision checker)
```

## Remaining Blocker

The immediate root cut remains `M0729-D-NP-PCP` and `M0729-D-PCP-NP`.

The forward direction is the substantive PCP theorem: it still needs the
verifier-to-constraint reduction, a constant-gap robustness theorem, PCP
composition, logarithmic-randomness and constant-query accounting, perfect
completeness, and soundness-half transport. The existing
`root_of_directionalPackage` theorem assumes both inclusions and therefore
provides no proof credit for either.

The reverse direction now has checked finite-oracle serialization, an
all-input polynomial certificate bound, exhaustive random-word enumeration,
Boolean verifier correctness, and the exact conditional `InNP` assembly. It
still lacks the actual `TM2ComputableInPolyTime encodePair encodeBool` machine
and polynomial runtime proof. Pinned mathlib defines that structure and the
identity implementation, but its apparent composition result is only the
source marker `proof_wanted TM2ComputableInPolyTime.comp`, not an importable
declaration. A bounded repo, pinned-dependency, and locally loaded history
search found no exact compatible PCP proof body. These searches support the
blocker only; they are not a global-absence claim.

No definitional inconsistency, vacuity, or degenerate checker closes the exact
statement. In particular, a zero-bit random space has cardinality one, so
half-soundness forces rejection of no-instances rather than making completeness
automatic.

The prerequisite `S56-M-0729-OBLIGATION_TREE` is provisional `[_]`, not master
accepted. The authoritative proof item still records `attempts: 0` and no
children despite many integrated proof packets. The rev-5.6 five-tick rule now
requires the integration lane to split this oversized item into dependency-legal
children rather than continue scheduling the monolithic root.

## Validation

All commands ran in this worker clone. The pre-existing untracked
`Formalizations/Lean/.lake` symlink points to canonical pinned artifacts and
was reused read-only. No `lake update`, `lake build`, dependency clone/fetch,
checkout, or `.lake` mutation was run. Lean outputs were confined to a
disposable `/tmp` directory and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique targets at ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-0729` | 0 | Rank 766; `planned`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0729/check_statement.py` | 0 | Exact expression hash `2a3d6c88...7bbc5`; all four weakened mutations were distinguished. |
| `python3 Stage1_Instances/THM-M-0729/check_anchor_audit.py` | 0 | Immutable pins and source hashes agreed; no exact root candidate is claimed; root M3. |
| `python3 Stage1_Instances/THM-M-0729/check_obligation_tree.py` | 0 | Passed 19 obligations and 76 typed edges; both inclusions remain open. |
| Disposable six-module `lake env lean --trust=0 -t0` replay | 0 | Statement, four prior proof-progress modules, and the new reverse bridge elaborated against existing pinned artifacts. All six new declarations reported exactly `propext`, `Classical.choice`, and `Quot.sound`; no `sorryAx`. |
| Scoped exact-PCP search over repository and pinned mathlib Lean sources | 0 | 59 matching lines; no terminal directional inclusion or exact-root body; output SHA-256 `9e7dba7a...e935368b`. |
| Pinned `TM2ComputableInPolyTime` API inventory | 0 | Structure at `Computable.lean:179`, forgetful map, identity body, and `proof_wanted` composition marker at line 284 only. |
| Loaded repository history search for `Stage1_Instances/THM-M-0729/Proof.lean` | 1 expected | No such historical path was present in the locally loaded objects. |
| Prohibited-device scan of `ProofProgressReverseBridge.lean` | 1 expected | No `sorry`, `admit`, `axiom`, `sorryAx`, unsafe/oracle device, `external`, `implemented_by`, or `native_decide`. |
| `git diff --check -- Stage1_Instances/THM-M-0729 .stage1-worker-selftest.json` | 0 | No whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest absent because the proof phase is incomplete. |

The new source SHA-256 is
`fcd9b22c05f6148bd821f34bd74843810a72679b2a9c709523a9654a063fd95b`;
its disposable olean SHA-256 is
`d057396a1f28ce08c150dd9a85d334a3dbe40ac040d57dbe6d0bff73275dd420`.
The toolchain was Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; pinned mathlib was
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

## Reopen Condition

Split the proof item. In the reverse child, implement the explicit TM2 machine
for `exhaustiveCertificateDecision` and prove its polynomial bound. In separate
forward children, implement the frozen reduction, robustness, composition, and
resource packages. An alternative is an immutable compatible terminal Lean 4
proof with exact-type transport, dependency/license provenance, and successful
repo-local checking.

This is current-base nonrelease partial-progress and blocker evidence. It does
not satisfy `S56-M-0729-PROOF`, close an obligation or the root, promote
scheduler state, or claim audit completion, validation, release, theorem
completion, receipt acceptance, or master acceptance. Because the assigned
phase is not genuinely complete, `.stage1-worker-selftest.json` remains absent.
