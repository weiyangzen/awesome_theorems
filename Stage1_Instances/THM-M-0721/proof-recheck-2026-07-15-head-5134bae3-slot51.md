# THM-M-0721 proof recheck at 5134bae3

Item: `S56-M-0721-PROOF`

Base revision: `5134bae303d5f5104698e8c96d7af4c26306eb47`

Base tree: `54e4bd2793df37c5451b86659fbd95a83504c25a`

## Verdict

`blocked`. No eligible proof body was implemented or found for the exact root
`Stage1Instances.THM_M_0721.ExistsNPCompleteLanguage`. The root remains
`[H1, M3, R4]`, and the proof item remains `[ ]`.

The checked declaration `root_of_candidate_packages` is only conditional composition. It consumes,
but does not construct, the two immediate root packages:

- `M0721-T-SAT-IN-NP`, requiring a faithful binary SAT encoding, a bundled polynomial-time TM2
  verifier, correctness, and a polynomial certificate bound;
- `M0721-T-UNIVERSAL-HARDNESS`, requiring arbitrary frozen-`InNP` verifier normalization, a
  Cook-Levin tableau construction, both correctness directions, and a bundled polynomial-time TM2
  reduction.

All eleven SAT and Cook-Levin implementation packages remain open. Pinned mathlib supplies the TM2
substrate and an identity machine, but no NP, SAT-language, or Cook-Levin endpoint. Its nearby
`TM2ComputableInPolyTime.comp` entry is source-level `proof_wanted`; trust-zero Lean confirms that it
does not create a checked declaration. Scoped repository, pinned-package, and history searches
found no replacement.

There is no definitional shortcut. Empty, universal, singleton, identity, or fixed-source languages
do not supply universal hardness. A reduction that branches on `source input` would require a
polynomial-time decision procedure not supplied by arbitrary verifier-based `InNP`; a universal
encoded-verifier language still requires the missing machine encoding, simulation correctness, and
polynomial-runtime development.

The first failed gate is `M0721-N-SAT-ENCODING`. The immediate root cut is
`M0721-T-SAT-IN-NP` plus `M0721-T-UNIVERSAL-HARDNESS`. Because the positive proof phase is
incomplete, no `Proof.lean`, proof receipt, or `.stage1-worker-selftest.json` is emitted.

## Validation

The automation-provided untracked `Formalizations/Lean/.lake` symlink to canonical pinned artifacts
was reused read-only. No dependency update, build, clone, fetch, checkout, or `.lake` mutation was
performed.

| Command | Exit | Exact result |
|---|---:|---|
| `git rev-parse HEAD HEAD^{tree}; git status --short --untracked-files=all; readlink -f Formalizations/Lean/.lake` | 0 | Base `5134bae3...eb47`, tree `54e4bd27...25a`; initially only the automation-provided `.lake` symlink was untracked. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique targets at ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-0721` | 0 | Rank 578, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete. |
| `LEAN_NUM_THREADS=1 timeout 600s python3 Stage1_Instances/THM-M-0721/check_statement.py` | 0 | Exact expression hash `758b1033...b204` matched; all four structural mutations were distinguished. |
| `python3 Stage1_Instances/THM-M-0721/check_obligation_tree.py` | 0 | Passed 18 obligations and 45 typed edges; denominator `375921a1...b92a`; root remained M3 and both terminal packages M4. |
| From `Formalizations/Lean`, concatenate `Statement.lean` and `ObligationTree.lean` into `LEAN_NUM_THREADS=1 timeout 300s lake env lean --trust=0 -t0 --stdin` | 0 | Exact declarations and conditional composition elaborated; `root_of_candidate_packages` reported `[propext, Quot.sound]` and supplied neither terminal package. |
| Scan owned Lean files for `sorry`, `admit`, `axiom`, `unsafe`, `proof_wanted`, or `sorryAx` | 1 expected | No prohibited proof device occurs in owned Lean files. |
| Search repo-local and pinned mathlib Lean source for the exact root, terminal packages, NP-completeness, SAT-language, or Cook-Levin endpoints | 1 expected | No eligible endpoint or terminal-package implementation exists. |
| Ask trust-zero Lean to `#print axioms Turing.TM2ComputableInPolyTime.comp` | 1 expected | Lean reported `Unknown constant`, confirming that source-level `proof_wanted` added no checked declaration. |
| Search Git history for `Proof.lean`, a proof receipt, or a proof checker under this target | 1 expected | No historical proof artifact was found. |
| Query Lean/Lake versions and pinned mathlib/flt-regular revisions, trees, and status | 0 | Lean 4.29.0 at `98dc76e...740`; Lake 5.0.0; mathlib `8a178386...ea95` and flt-regular `56161b6e...1a27`, both at recorded trees and clean. |
| `sha256sum` the frozen target and environment inputs | 0 | Every recorded source/environment hash matched. |

## Reopen Condition

Append-only refine exact Lean signatures and implement the eleven frozen SAT and Cook-Levin
packages without placeholders, or identify an immutable compatible proof already present in the
pinned closure that can be exact-type checked, transported to the Bool-word TM2 encodings, and
provenance-audited without changing the dependency lock.

This is current-base warm-cache nonrelease blocker evidence only. It does not satisfy
`S56-M-0721-PROOF`, change scheduler state, close either terminal package or the root, or claim
audit completion, theorem completion, validation, release, receipt acceptance, or master
acceptance.
