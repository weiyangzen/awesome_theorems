# THM-M-0612 proof recheck at `9bce865a` (slot39)

Item: `S56-M-0612-PROOF`

Date: `2026-07-15T13:54:34+08:00`

Base revision: `9bce865a14bcc270344ea909d6936c6ea22aa1c2`

Base tree: `523a9471aac257c4cf54acceee07172fab22f5b4`

## Verdict

`blocked`. No eligible positive proof body was implemented or found for the
exact target `Stage1.THM_M_0612.StatementShape`. Its immediate remaining cut is
`M0612-T-SQUARED`, whose missing body is the proposition
`Stage1.THM_M_0612.RadiusSquaredObstruction`: it must derive `r ^ 2 <= R ^ 2`
from the frozen local symplectic-embedding and cylinder hypotheses.

The first deep unavailable package is `M0612-C-CAPACITY`. Neither this
repository nor the available pinned Lean closure constructs a compatible
symplectic capacity and proves invariance, monotonicity, conformality, and the
required ball and cylinder values. The frozen local/scale route and the
higher-dimensional almost-complex and pseudoholomorphic-curve packages also
remain open. Supplying these as an axiom, bodyless declaration, or theorem
premise would be a prohibited placeholder, not a proof.

`ObligationTree.lean` has real proof bodies only for the elementary transport
from `r ^ 2 <= R ^ 2` to `r <= R` and the conditional root assembly that
accepts the entire missing obstruction as a premise. The local encoding and
sanity lemmas establish nonvacuity, openness, differentiability, form
nondegeneracy, and derivative injectivity; none closes the frozen root cut.
The legacy module uses a different global-map interface and likewise contains
no terminal proof.

The prerequisite immutable audit found one external Lean 4 declaration named
for nonsqueezing, but its body and dependencies contain admissions. Fresh
repo-local and pinned-package scans found no eligible alternative to pin or
import. Proof-relevant source, registry, graph, audit, validation-spec, and
dependency-pin hashes are unchanged since the preceding recheck.

Thus no proof source or positive receipt was added. The root stays
`[H2, M3, R4]`, with `root_closed=false`, `audit_complete=false`, and
`theorem_complete=false`. The prerequisite obligation-tree node is still
worker-provisional rather than master-accepted. Because the positive proof
phase is not genuinely self-tested as complete, `.stage1-worker-selftest.json`
is deliberately absent.

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
| `cd Formalizations/Lean && lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0612/Statement.lean` | 1 | Lake stopped before invoking Lean because shared `flt-regular` cannot resolve `HEAD`; its `.git/HEAD` is `refs/heads/.invalid`. |
| explicit-path pinned Lean `--trust=0 -t0` replay of all four owned modules | 0 | All four elaborated; each of ten axiom reports was exactly `[propext, Classical.choice, Quot.sound]`; temporary outputs were removed. |
| owned Lean prohibited-construct scan | 1 | Expected no-match exit; no `sorry`, `admit`, axiom, unsafe/oracle construct, or native decision shortcut occurs. |
| complete available pinned-package topical scan | 1 | Expected no-match exit for nonsqueezing, Gromov width, symplectic capacity, or pseudoholomorphic declarations. |
| repo-local topical inventory | 0 | Hits were this dossier, legacy `S1_M_256`, and unrelated `THM-M-0611`; inspection found no exact terminal body. |
| scoped input audit since `cc8afe07` | 0 | No proof input changed; only the preceding blocker JSON and Markdown entered this target path. |
| pinned environment and input-hash checks | 0 aggregate | Lean 4.29.0 commit `98dc76e...16740`; mathlib `8a178386...ea95`, tree `bdc39a31...1c2b`; recorded source and pin hashes matched. |
| JSON, fail-closed identity, source-hash, whitespace, and absent-selftest checks | 0 aggregate | The blocker parses and matches the current base, exact cut, unchanged debt vector, empty proof-credit arrays, clean fresh files, and deliberately absent completion self-test. |

The diagnostic replay constructed `LEAN_PATH` only from already-present root
and pinned-package build artifacts. It compiled a temporary `Statement.olean`
and replayed `ObligationTree.lean`, `LocalEncoding.lean`, and
`EncodingSanityProbe.lean`. Output SHA-256 values were `e3b0c442...b855`,
`039f16b7...35a`, `4515cf76...0a3c5`, and `94de4565...81e` respectively.

The proof-source hashes remain `2de623b5...f919` for `Statement.lean`,
`0392a18a...07007` for `ObligationTree.lean`, `278177c5...a117` for
`LocalEncoding.lean`, and `1b61df00...ed82` for `EncodingSanityProbe.lean`.
The registry file and typed-graphs hashes remain `635af26d...8850` and
`def70532...50b2`; the registry denominator remains `2cad29b7...a4bc8`.

## Retry Condition

Resume after a placeholder-free implementation of `M0612-T-SQUARED` and its
frozen nonlinear dependencies, or discovery of an immutable compatible Lean 4
terminal proof that can be pinned, exact-type transported, and checked without
changing the dependency lock. A prescribed `lake env` replay also requires the
read-only cache to expose manifest-pinned `flt-regular` commit
`56161b6e...1a27` through a valid checkout.

This is fresh target-owned nonrelease blocker evidence, not a proof receipt. It
does not satisfy `S56-M-0612-PROOF`, propose checklist state, or support audit
completion, theorem completion, validation, release, or master acceptance.
