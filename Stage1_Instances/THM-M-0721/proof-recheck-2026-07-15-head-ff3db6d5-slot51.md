# THM-M-0721 proof recheck at `ff3db6d5` (slot51)

Item: `S56-M-0721-PROOF`

Intent: `prove`

Recheck date: `2026-07-15T16:04:53+08:00`

Base revision: `ff3db6d51326417873f49c410421f8f3e13be993`

Base tree: `9160a80a3e3588fd96fcd79323230668cc7d3df1`

## Verdict

`blocked`. No eligible proof body was implemented or found for the exact root
`Stage1Instances.THM_M_0721.ExistsNPCompleteLanguage`. The root remains
`[H1, M3, R4]`, and this proof item remains `[ ]`.

The checked declaration `root_of_candidate_packages` consumes, but does not construct, the two
immediate root packages:

- `M0721-T-SAT-IN-NP`, requiring a faithful binary SAT encoding, a correct bundled polynomial-time
  TM2 verifier, and a polynomial certificate bound;
- `M0721-T-UNIVERSAL-HARDNESS`, requiring arbitrary-verifier normalization, a Cook-Levin tableau
  construction, both correctness directions, and a bundled polynomial-time TM2 reduction.

All eleven SAT and Cook-Levin implementation packages remain open. They are currently represented
by planned prose fingerprints rather than exact Lean leaf signatures, so append-only registry
refinement is also required before leaf proof credit. Pinned mathlib supplies the TM2 substrate and
identity implementation but no NP, SAT-language, or Cook-Levin endpoint. Its relevant composition
item is source-level `proof_wanted`; trust-zero Lean confirms that no checked constant was created.
Repository, pinned-package, and history searches found no replacement.

The immutable audit's external candidates remain supporting-only, placeholder-dependent, or
contract-incompatible. The fresh replay on this run timed out during the first TLS handshake, so no
new network result is credited and the frozen content-addressed classifications remain unchanged.
Empty, universal, identity, fixed-source, classical-choice, or computable-reducibility shortcuts do
not supply the frozen universal polynomial-time machine witnesses.

The first failed gate is `M0721-N-SAT-ENCODING`. The immediate root cut is
`M0721-T-SAT-IN-NP` plus `M0721-T-UNIVERSAL-HARDNESS`. Because the positive proof phase is
incomplete, no proof receipt or `.stage1-worker-selftest.json` is emitted.

## Validation

The automation-provided untracked `Formalizations/Lean/.lake` symlink to canonical pinned artifacts
was reused read-only. No dependency update, build, clone, fetch, checkout, or `.lake` mutation was
performed.

| Command | Exit | Exact result |
|---|---:|---|
| `git rev-parse HEAD HEAD^{tree}; git status --short --untracked-files=all; readlink -f Formalizations/Lean/.lake` | 0 | Base `ff3db6d5...e993`, tree `9160a80a...df1`; initially only the automation-provided `.lake` symlink was untracked. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check && python3 scripts/stage1_target.py show THM-M-0721` | 0 | Passed 1546 unique targets; THM-M-0721 is rank 578, planned, L0/rework-required, theorem incomplete. |
| `LEAN_NUM_THREADS=1 timeout 600s python3 Stage1_Instances/THM-M-0721/check_statement.py` | 0 | Exact expression hash `758b1033...b204` matched; all four structural mutations were distinguished under the pinned environment. |
| `python3 Stage1_Instances/THM-M-0721/check_obligation_tree.py` | 0 | Passed 18 obligations and 45 typed edges; denominator `375921a1...b92a`; root remained M3 and both terminal packages M4. |
| From `Formalizations/Lean`, concatenate `Statement.lean` and `ObligationTree.lean` into `LEAN_NUM_THREADS=1 timeout 300s lake env lean --trust=0 -t0 --stdin` | 0 | Exact declarations and conditional composition elaborated; `root_of_candidate_packages` reported `[propext, Quot.sound]` and produced neither terminal package. |
| Scan owned Lean files for `sorry`, `admit`, `axiom`, `unsafe`, `proof_wanted`, or `sorryAx` | 1 expected | No prohibited proof device occurs in owned Lean files. |
| Search repo-local and pinned mathlib Lean source for the exact root, terminal packages, NP-completeness, SAT-language, or Cook-Levin endpoints | 1 expected | No eligible endpoint or terminal-package implementation exists. |
| Ask trust-zero Lean to `#print axioms Turing.TM2ComputableInPolyTime.comp` | 1 expected | Lean reported `Unknown constant`, confirming that source-level `proof_wanted` added no checked declaration. |
| Search Git history and target trees for `Proof.lean`, a proof receipt/checker, or an added root body | 0 | No historical proof artifact or root proof was found; only statement, architecture, and blocker evidence exist. |
| `timeout 180s python3 Stage1_Instances/THM-M-0721/check_anchor_audit.py` | 1 | Fresh immutable-source replay timed out during the first HTTPS TLS handshake; no fresh network-backed evidence is claimed. |
| From `Formalizations/Lean`, query Lean/Lake versions and pinned mathlib/flt-regular revisions, trees, and status | 0 | Lean 4.29.0 at `98dc76e...740`; Lake 5.0.0; mathlib `8a178386...ea95` and flt-regular `56161b6e...1a27`, both at recorded trees and clean. |
| `sha256sum` the frozen target and environment inputs | 0 | Every recorded source/environment hash matched. |
| Parse the structured blocker, assert its fail-closed invariants, diff-check both new artifacts, and assert `.stage1-worker-selftest.json` is absent | 0 | JSON identity/base/state/open-root/cut-set/no-proof invariants matched; no whitespace diagnostic; the completion self-test remained deliberately absent. |

## Reopen Condition

Append-only refine exact Lean signatures and implement the eleven frozen SAT and Cook-Levin
packages without placeholders, or identify an immutable compatible proof already present in the
pinned closure that can be exact-type checked, transported to the Bool-word TM2 encodings, and
provenance-audited without changing the dependency lock.

This is current-base nonrelease blocker evidence only. It does not satisfy
`S56-M-0721-PROOF`, change scheduler state, close a terminal package or the root, or claim audit
completion, theorem completion, validation, release, receipt acceptance, or master acceptance.
