# Current-base proof recheck

Item: `S56-M-1419-PROOF`

Theorem: `THM-M-1419`

Base revision: `fd50bb07f6632a2ad0bdc17737c200432ee242c8`

Base tree: `ed66432029954bfa5b17e0afda5f3817eeb32d48`

Attempt date: `2026-07-15` (`Asia/Shanghai`)

Worker: Stage1 rev-5.6 automation clone `slot71`

## Verdict

`blocked`; the assigned proof phase remains `[ ]`. No proof body, axiom,
placeholder, weakened theorem, dependency, frozen authority artifact, receipt,
or task state was added or changed. Because the proof phase did not close, no
`.stage1-worker-selftest.json` is emitted.

The first failed gate is exact-target fidelity at `M1419-S-INTERFACE`. The
frozen target quantifies a plain equivalence `T : Omega Equiv Omega`.
`MeasurePreserving T mu mu` and `Ergodic T mu` supply `Measurable T`, but no
frozen hypothesis supplies `Measurable T.symm`. Pinned mathlib stores inverse
measurability separately in `MeasurableEquiv`, and its theorem
`Ergodic.symm` requires a measurable equivalence.

This is the mathematical content needed for the backward filtration, not a
missing syntactic transport. The one-sided Oseledets theorem yields a
filtration, not the target's measurable invariant direct-sum splitting. An
earlier owned analysis gives the concrete obstruction family: the two-sided
fair Bernoulli shift with only its future-coordinate sigma algebra and the
triangular cocycle `A(omega) = [[4, 0], [omega_0, 1]]`. Equivariance forces the
fast line's slope to depend on past coordinates, contradicting the required
future measurability. That countermodel is not kernel-formalized here, so the
root is conservatively left at `M3`, not reclassified as `M5`.

The prose freeze is inconsistent with the Lean expression:
`source-statement-crosswalk.md` says inverse measurability was retained, but
the proposition retains only measurability of the *matrix* inverse and never
assumes measurability of the base inverse. A proof worker cannot silently add
that premise. The statement must be reopened and versioned before positive
proof work can be exact.

## Candidate update

A complete placeholder-free Lean 4.29 source port of
`marcmorningstar/lean4-ergodic-theory` now exists provisionally in sibling
worker `slot44`, under the different target `THM-M-1056`. Its 62-module port
contains `ErgodicTheory.oseledets_splitting`; the sibling receipt reports
trust-zero elaboration and only `propext`, `Classical.choice`, and `Quot.sound`.
That materially improves the future integration route, but it does not close
this item:

- the source and receipt are outside `THM-M-1419`'s owned path and accepted
  dependency closure;
- the sibling receipt is provisional `[_]`, `accepted=false`, and
  `theorem_complete=false`;
- the terminal theorem requires `T : X MeasurableEquiv X`, pointwise
  `Measurable A`, and pointwise `det (A x) != 0`;
- the frozen target has a plain equivalence and only almost-everywhere matrix
  measurability and invertibility;
- no checked bridge supplies inverse base measurability, repairs all
  almost-everywhere representatives, or proves every exact norm, cocycle,
  subspace-measurability, direct-sum, finrank, equivariance, growth, and index
  transport.

The terminal source at upstream revision
`ed3fa6b8a30594eeb791160563942ba115581aa0` has SHA-256
`e47ced0d869724a402369352f0ac0bd1f4bb8e57cfd7cefc2a44fa071c6e9407`.
These are discovery and provisional sibling facts, not proof credit for
`THM-M-1419`.

## Frozen architecture

The obligation-tree validator passes 14 obligations and 41 typed edges with
denominator
`ad6916330e2b03519a1c387301c0b7a418ed53c487c42d86691de96e56639599`,
but explicitly leaves the root open at `M3`. Twelve of thirteen
machine-required obligations have no terminal proof-body ID. The sole recorded
body, `target_of_construction_package`, consumes a package definitionally
equal to the complete root, so it is a conditional identity wrapper rather
than a substantive composition of the four required proof children.

The prerequisite `S56-M-1419-OBLIGATION_TREE` remains provisional rather than
master accepted. Sixteen earlier current-day proof recheck packets plus an
older blocker are present, while the authoritative DAG still records zero
attempts. Section 10.2 requires an unresolved item to be split after five
execution ticks. Only the master may reconcile packets with authoritative
ticks, split or version the node, reopen prerequisites, or change task state.

## Fresh validation

All commands ran in this worker clone. The automation-provided untracked
`.lake` symlink was reused read-only. No `lake update`, `lake build`, dependency
clone/fetch, network command, or deliberate `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 uniform-L0 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique ordered targets, ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-1419` | 0 | Rank 688; planned; rework required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1419/check_obligation_tree.py` | 0 | Passed 14 obligations and 41 typed edges; denominator `ad691633...5999`; root explicitly remains open `M3`. |
| `cd Formalizations/Lean && lake --version && lake env lean --version` | 0 | Lake `5.0.0-src+98dc76e`; Lean `4.29.0`, commit `98dc76e3...716fb04`. |
| Fresh temporary trust-zero replay of `OseledetsStatement.lean`, `ObligationTree.lean`, and an axiom probe through the pinned `lake env lean` executable | 0, 0, 0 | Both modules elaborated; olean hashes were `f5222f72...3a9169` and `4fd543d8...50a6`; wrapper axioms were exactly `[propext, Classical.choice, Quot.sound]`; the temporary directory was removed. |
| Pinned mathlib API inspection | 0 | `MeasurePreserving` stores forward measurability; `MeasurableEquiv` stores inverse measurability separately; `Ergodic.symm` requires `MeasurableEquiv`. |
| Pinned mathlib terminal-name search | 1 expected | No Oseledets, multiplicative-ergodic, or Kingman terminal declaration was found. |
| Token-anchored prohibited-device scan over owned Lean files | 1 expected | No `sorry`, `admit`, axiom declaration, unsafe injection, `native_decide`, `implemented_by`, or `extern` occurs. |
| Read-only sibling candidate inspection | 0 | Found 62 ordered modules and the exact bimeasurable terminal signature; receipt state is provisional `[_]`, not accepted. |
| `git diff --check` before this packet, then `git diff --no-index --check /dev/null <new-file>` for each packet file | 0, 1 expected, 1 expected | The tracked diff had no whitespace errors; each untracked new-file check returned Git's expected `1` for a nonempty diff and reported no whitespace diagnostic. The only pre-existing worktree entry was the automation-provided untracked `.lake` symlink. |

The replay wrote target oleans only under a fresh `/tmp` directory and removed
it. It confirms that the exact statement and circular wrapper still
elaborate; it does not prove the open Oseledets construction package.

## Retry condition

The master must first reopen `S56-M-1419-STATEMENT`, replace the plain base
equivalence with a measurable equivalence or add `Measurable T.symm`, accept a
new exact expression fingerprint and obligation-registry version, and rerun
the source, mutation, anchor, and obligation-tree gates. It must also reconcile
the tracked negative packets with authoritative execution ticks and split this
oversized proof item if at least five qualify. After that, an owned integration
task can vendor and provenance-audit the completed Lean 4.29 port and implement
the exact almost-everywhere and representation transports plus a checked
composition theorem consuming every required child.

This is current-base nonrelease blocker evidence only. Accepted receipt IDs
are empty; root vector remains `[H2, M3, R3]`. It does not satisfy
`S56-M-1419-PROOF`, close an obligation or root, change scheduler state, or
claim audit completion, theorem completion, validation, release, receipt
acceptance, or master acceptance.
