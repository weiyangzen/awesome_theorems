# THM-M-0612 proof recheck at `3ef7c6df` (slot40)

Item: `S56-M-0612-PROOF`

Date: `2026-07-15T15:04:23+08:00`

Base revision: `3ef7c6dff0c66bc8c02e842f4cea6b9936349094`

Base tree: `58db6c40c0fa9186c4a56a022a6a37d1c2be551b`

## Verdict

`blocked`. No eligible positive proof body was implemented or found for the
exact target `Stage1.THM_M_0612.StatementShape`. Its immediate remaining cut is
`M0612-T-SQUARED`, whose missing body is
`Stage1.THM_M_0612.RadiusSquaredObstruction`: it must derive `r ^ 2 <= R ^ 2`
from the frozen local symplectic-embedding and cylinder hypotheses.

The first deep unavailable package is `M0612-C-CAPACITY`. Neither this
repository nor the pinned Lean closure constructs a compatible symplectic
capacity and proves invariance, monotonicity, conformality, and the required
ball and cylinder values. The local/scale transports and the alternative
almost-complex and pseudoholomorphic-curve packages also remain open. Adding
any missing package as an axiom, bodyless declaration, or assumed theorem
premise would be a prohibited placeholder rather than proof progress.

`ObligationTree.lean` has real bodies only for the elementary transport from
`r ^ 2 <= R ^ 2` to `r <= R` and conditional root assembly that accepts the
entire missing obstruction as a premise. The local encoding and sanity modules
prove nonvacuity, openness, differentiability, form nondegeneracy, and
derivative injectivity. None closes a frozen root-cut obligation. The legacy
module has a different global-map interface and also has no terminal proof.

The prerequisite immutable audit found one external Lean 4 declaration named
for nonsqueezing, but its body and dependencies contain admissions. Fresh
repo-local and complete pinned-package scans found no eligible alternative to
pin or import. Proof-relevant sources, registry, graphs, audit, validation
specifications, and dependency pins are unchanged since the preceding recheck.

Therefore no proof source or positive receipt was added. The root stays
`[H2, M3, R4]`, with `root_closed=false`, `audit_complete=false`, and
`theorem_complete=false`. The obligation-tree prerequisite also remains
worker-provisional rather than master-accepted. Because the assigned positive
proof phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` is deliberately absent.

## Validation

All checks reused the automation-provided pinned artifacts read-only. No
`lake update`, `lake build`, dependency clone/fetch, checkout/repair, or other
`.lake` mutation was requested. Generated Lean output was isolated under
`/tmp` and removed. The untracked external `.lake` symlink makes this
nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0612` | 0 | Rank 256; planned; baseline L0/rework-required; legacy artifacts unaccepted; theorem incomplete. |
| `git status --short --untracked-files=all` before edits | 0 | Only the automation-provided untracked `Formalizations/Lean/.lake` symlink was present. |
| `python3 Stage1_Instances/THM-M-0612/check_obligation_tree.py` | 0 | 26 obligations and 58 typed edges passed; denominator `2cad29b7...a4bc8`; root open M3 because the squared-radius package remains M4. |
| `cd Formalizations/Lean && lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0612/Statement.lean` | 0 | The exact canonical statement elaborated under pinned Lean 4.29.0 with no output. |
| direct `lake env lean --trust=0 -t0` on each of the three importing modules | 1 each | Expected project-layout diagnostic: each reported unknown module prefix `Statement` because no target-local `Statement.olean` is installed in Lake's search path; the isolated replay below supplies it without mutating the project. |
| isolated pinned `lake env` Lean replay of all four owned modules | 0 | All four elaborated at trust level 0; each of ten axiom reports was exactly `[propext, Classical.choice, Quot.sound]`; temporary outputs were removed. |
| owned Lean prohibited-construct scan | 1 | Expected no-match exit; no `sorry`, `admit`, axiom/bodyless declaration, unsafe/oracle construct, or native decision shortcut occurs. |
| complete pinned-package topical scan | 1 | Expected no-match exit for nonsqueezing, Gromov width, symplectic capacity, or pseudoholomorphic declarations. |
| repo-local topical inventory | 0 | Hits were this dossier, legacy `S1_M_256`, and unrelated `THM-M-0611`; inspection found no exact terminal body. |
| scoped input audit since `9bce865a` | 0 | No proof input changed; only the preceding blocker JSON and Markdown entered this target path through integration commit `860fc1b5`. |
| pinned environment and input-hash checks | 0 aggregate | Lean 4.29.0 commit `98dc76e...16740`; mathlib `8a178386...ea95`, tree `bdc39a31...1c2b`; recorded source and pin hashes matched. |
| JSON, fail-closed identity, source-hash, whitespace, and absent-selftest checks | 0 aggregate | The blocker parses and matches the current base, exact cut, unchanged debt vector, empty proof-credit arrays, owned changed paths, clean fresh files, and deliberately absent completion self-test. |

The isolated replay compiled a temporary `Statement.olean`, then elaborated
`ObligationTree.lean`, `LocalEncoding.lean`, and `EncodingSanityProbe.lean`
using the Lean binary and `LEAN_PATH` selected by `lake env`. Output SHA-256
values were `e3b0c442...b855`, `039f16b7...35a`, `4515cf76...0a3c5`, and
`94de4565...81e` respectively.

The proof-source hashes remain `2de623b5...f919` for `Statement.lean`,
`0392a18a...07007` for `ObligationTree.lean`, `278177c5...a117` for
`LocalEncoding.lean`, and `1b61df00...ed82` for `EncodingSanityProbe.lean`.
The registry and typed-graphs hashes remain `635af26d...8850` and
`def70532...50b2`; the registry denominator remains `2cad29b7...a4bc8`.

## Retry Condition

Resume after a placeholder-free implementation of `M0612-T-SQUARED` and its
frozen nonlinear dependencies, or discovery of an immutable compatible Lean 4
terminal proof that can be pinned, exact-type transported, and checked without
changing the dependency lock.

This is fresh target-owned nonrelease blocker evidence, not a proof receipt. It
does not satisfy `S56-M-0612-PROOF`, propose checklist state, or support audit
completion, theorem completion, validation, release, or master acceptance.
