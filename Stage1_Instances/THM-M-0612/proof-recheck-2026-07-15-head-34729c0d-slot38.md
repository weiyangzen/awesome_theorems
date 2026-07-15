# THM-M-0612 proof recheck at `34729c0d` (slot38)

Item: `S56-M-0612-PROOF`

Date: `2026-07-15T13:13:20+08:00`

Base revision: `34729c0dff13ac1d1a2781d9c1ea4bf7c6a35398`

Base tree: `dde7f823b850641fc7dade0380327b6ac013ac07`

## Verdict

`blocked`. No eligible positive proof body was implemented or found for the
exact target `Stage1.THM_M_0612.StatementShape`. The remaining root cut is
`M0612-T-SQUARED`, whose exact missing body is
`Stage1.THM_M_0612.RadiusSquaredObstruction`: it must derive `r ^ 2 <= R ^ 2`
from the canonical local symplectic-embedding and cylinder hypotheses.

The first deep unavailable package is `M0612-C-CAPACITY`. Neither the
repository nor the available pinned Lean closure constructs a compatible
symplectic capacity and proves its invariance, monotonicity, conformality, and
ball and cylinder values. The frozen local/scale and higher-dimensional
pseudoholomorphic-curve packages also remain open. A separately inspected
capacity interface only assumes normalization and monotonicity as structure
fields; it supplies no capacity inhabitant or bridge to this target.

`ObligationTree.lean` contains two real but nonterminal bodies.
`radius_le_of_sq_le` proves the elementary ordered-field transport, while
`root_of_radiusSquaredObstruction` accepts the complete missing geometric
obstruction as a premise. Introducing that premise as an axiom, bodyless
declaration, or assumed package would be a prohibited placeholder. The local
encoding and sanity-probe lemmas establish nonvacuity, openness,
differentiability, form nondegeneracy, and derivative injectivity, but none
closes a frozen root-cut obligation.

The legacy `S1_M_256.lean` module has a different global-map interface and only
definitions plus conditional/order wrappers. The prerequisite external audit
found one named Lean 4 nonsqueezing declaration, but its body and dependencies
contain admissions. Current scans found no eligible terminal theorem in the
repository or pinned package sources.

No proof source or positive receipt was added. The root vector remains
`[H2, M3, R4]`, `root_closed=false`, and `theorem_complete=false`. The
obligation-tree prerequisite remains worker-provisional rather than
master-accepted. Because the assigned positive proof phase is not genuinely
self-tested as complete, `.stage1-worker-selftest.json` is deliberately absent.

## Validation

All checks reused the automation-provided pinned artifacts read-only. No
`lake update`, `lake build`, dependency clone/fetch, checkout/repair, or other
`.lake` mutation was requested. Generated Lean output was isolated under
`/tmp` and removed. The untracked `.lake` symlink makes this nonrelease
evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0612` | 0 | Rank 256; planned hard-mathlib-anchor-and-wrapper lane; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0612/check_obligation_tree.py` | 0 | 26 obligations and 58 typed edges passed; denominator `2cad29b7...a4bc8`; root open M3. |
| scoped `lake env lean --trust=0 -t0` replay | 1 | Lake stopped before Lean because shared `flt-regular` cannot resolve `HEAD`; it is `refs/heads/.invalid`. |
| explicit-path pinned Lean diagnostic | 0 | All four sources elaborated at trust level 0; every one of ten axiom reports was exactly `[propext, Classical.choice, Quot.sound]`. |
| owned Lean prohibited-construct scan | 1 | Expected no-match exit for `sorry`, `admit`, axioms/bodyless declarations, unsafe/oracle constructs, and `native_decide`. |
| complete pinned-package topical scan | 1 | Expected no-match exit for nonsqueezing, Gromov width, symplectic capacity, or pseudoholomorphic declarations. |
| repo-local topical inventory | 0 | Hits were this dossier, legacy `S1_M_256`, and unrelated `THM-M-0611`; no exact terminal body was found. |
| scoped input audit since `63a9ed9c` | 0 | Only the preceding blocker pair entered the target path; proof inputs, registry/graphs, audit receipt, validation specs, and pins were unchanged. |
| pinned environment checks | 0 aggregate | Lean 4.29.0 commit `98dc76e...16740`; mathlib `8a178386...ea95`, tree `bdc39a31...1c2b`; hashes matched. |
| JSON, identity, hash, invariant, and whitespace checks | 0 aggregate | Current base and hashes matched; blocker fields remained fail-closed; both fresh files were clean. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

The diagnostic replay used the pinned Lean binary and constructed `LEAN_PATH`
only from existing package build outputs. It wrote `Statement.olean` under
`/tmp`, then elaborated `ObligationTree.lean`, `LocalEncoding.lean`, and
`EncodingSanityProbe.lean`. The four output SHA-256 values were
`e3b0c442...b855`, `039f16b7...35a`, `4515cf76...0a3c5`, and
`94de4565...81e`.

The proof-relevant source SHA-256 values remain `2de623b5...f919` for
`Statement.lean`, `0392a18a...07007` for `ObligationTree.lean`,
`278177c5...a117` for `LocalEncoding.lean`, `1b61df00...ed82` for
`EncodingSanityProbe.lean`, `635af26d...8850` for the obligation registry,
and `def70532...50b2` for the typed graphs. The toolchain and Lake manifest
hashes are `651c8acc...b1d2` and `321626c8...2d81`.

## Retry Condition

Resume after a placeholder-free implementation of `M0612-T-SQUARED` and its
frozen nonlinear dependencies, or after discovery of an immutable compatible
Lean 4 terminal proof that can be pinned, exact-type transported, and checked
without changing the dependency lock. For the prescribed `lake env` replay,
the read-only cache must also expose manifest-pinned `flt-regular` commit
`56161b6e...1a27` through a valid checkout.

This is fresh owned blocker evidence, not a proof receipt. It does not satisfy
`S56-M-0612-PROOF`, propose checklist state, or support audit completion,
theorem completion, validation, release, or master acceptance.
