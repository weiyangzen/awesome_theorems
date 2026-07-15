# THM-M-0783 proof recheck at `34c65b4a` (slot51)

Item: `S56-M-0783-PROOF`

Intent: `prove`

Recorded: `2026-07-15T19:56:48+08:00`

Base revision: `34c65b4a5d82231740b5d5346afe3b11fd795d19`

Base tree: `d961c0376362e94e2f72d9f88ceb2ddf55134577`

## Verdict

`blocked`. There is no placeholder-free proof body for the exact proposition
`Stage1Instances.THM_M_0783.MartinsAxiom` in the repository-local pinned dependency closure. The
frozen target records object-level Martin's axiom, an additional set-theoretic axiom rather than an
ordinary theorem supplied by the selected Lean/mathlib foundation. The dossier provisionally
classifies the target as `H5`; Blueprint section 3.1 makes that a barrier to ordinary proof
execution pending a target decision.

The sole substantive proof leaf, `M0783-L-DENSE-FAMILY`, is definitionally
`ExpandedMartinsAxiom`, so it contains the whole missing proposition. It must uniformly construct a
filter meeting every suitably bounded dense family in every nonempty ccc partial order, for every
cardinal below the continuum. The existing `root_of_denseFamilySolver` takes that entire proposition
as an explicit premise and transports it to the canonical target. This is valid conditional
composition, not an unconditional proof body.

Pinned mathlib supplies the Rasiowa-Sikorski construction for an `Encodable` dense family in
`Mathlib/Order/Ideal.lean`. An independently written scratch theorem confirmed at trust level zero
that it proves the `Countable I` boundary. That result is strictly weaker than the frozen target,
which quantifies over every `I` with `#I <= kappa` for every `kappa < continuum`; it receives no
target proof credit. A current scoped scan found no Martin's-axiom, forcing-axiom, or
dense-family-solver declaration in any installed pinned package source.

This worker does not claim to have formalized or newly validated a theorem of independence. The
dossier's source and independent-review gates remain open. The proof blocker is narrower: no
allowed exact terminal body is available in the bounded pinned closure, while adding an axiom or
premise and weakening or substituting the theorem are all forbidden.

This attempt therefore does not introduce `MartinsAxiom` or `DenseFamilySolver` with an axiom,
bodyless declaration, placeholder, or extra premise; weaken the cardinal, ccc, order, density,
family, or filter contract; or substitute a relative-consistency, independence, countable-family,
CH-conditional, or consequence theorem. Each route changes the foundation or theorem and cannot
satisfy the assigned proof phase.

The item remains `[ ]`, lifecycle remains `planned`, and the root remains `[H5, M4, R4]`. No proof
receipt, worker `[_]`, accepted state, audit completion, theorem completion, validation, release, or
master acceptance is claimed. Because the positive proof phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.

The reported root vector follows the obligation-tree closure boundary and receipt; its `H5` value is
provisional and not independently accepted. One prerequisite
artifact is internally stale: the `M0783-ROOT` node in `typed-graphs.json` says `M3`, while that
file's closure boundary, the anchor audit, the obligation-tree checker, and proof-phase receipts use
`M4`. This proof worker does not alter prerequisite obligation artifacts; the master should
reconcile that field separately. It does not close the substantive `M4` dense-family leaf.

## Failed Gate

The first failed gate is exact kernel closure of `M0783-L-DENSE-FAMILY` without placeholders,
undeclared premises, or a foundation extension. The proof-relevant cut is:

```text
M0783-L-DENSE-FAMILY
```

The complete frozen cut additionally contains `M0783-X-SOURCE`, `M0783-X-FOUNDATION`,
`M0783-X-PROVENANCE`, `M0783-X-READABLE`, and `M0783-X-WORKFLOW`. A retry requires an immutable,
license-compatible Lean 4 terminal body for the exact target with acceptable exact-type, axiom,
placeholder, provenance, and composition reports. Alternatively, the master must redirect this
additional axiom to a theory-extension, consistency, or independence target. That is a target-policy
correction, not proof completion.

## Narrow Validation

The automation-provided `Formalizations/Lean/.lake` symlink was treated as read-only. No `lake
update`, `lake build`, dependency clone/fetch, or checkout repair was run. Narrow elaboration used
only `lake env lean` with existing pinned object directories; temporary outputs lived in the owned
target directory and were removed. Preflight `git status --short` reported only that untracked
automation symlink, so this is dirty-clone, nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `git status --short` | 0 | only the automation-provided untracked `Formalizations/Lean/.lake` symlink; owned target and self-test paths were clean |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 and the uniform L0/rework-required baseline passed |
| `python3 scripts/stage1_target.py show THM-M-0783` | 0 | rank 788, lifecycle `planned`, legacy artifacts unaccepted, theorem incomplete |
| `LEAN_NUM_THREADS=1 timeout --foreground --kill-after=10s 600s python3 Stage1_Instances/THM-M-0783/check_statement.py` | 0 | expression hash `c5896a33...5599ada`; all four structural mutations killed; pinned Lean 4.29.0 and mathlib `8a178386...ea95` |
| `python3 Stage1_Instances/THM-M-0783/check_obligation_tree.py` | 0 | 12 obligations and 28 typed edges passed; denominator `0581a4ed...25532c9`; root open M4 |
| `python3 Stage1_Instances/THM-M-0783/check_anchor_audit.py` | 0 | anchor boundary, six probes, local statement status, and pinned mathlib revision passed |
| exact command recipe `LEAN_OBJECT_PATH="$PWD/Formalizations/Lean/.lake/build/lib/lean:$(find "$PWD/Formalizations/Lean/.lake/packages" -type d -path '*/.lake/build/lib/lean' -print \| sort \| paste -sd: -)"`, then pinned `lake env lean --trust=0 -t0 -R` on isolated copies of `Statement.lean` and `ObligationTree.lean` | 0 | exact statement and conditional composition elaborated; axiom report `[propext, Classical.choice, Quot.sound]`; temporary outputs removed |
| same exact pinned recipe on an independently written `Countable I` boundary theorem using `Mathlib.Order.Ideal` | 0 | only the weaker Rasiowa-Sikorski boundary elaborated; axiom report `[propext, Classical.choice, Quot.sound]`; scratch SHA-256 `9cb738d8...c7eb581`; temporary outputs removed |
| scoped prohibited-construct scan of owned Lean source | 1 | expected no-match: no `sorry`, `admit`, bodyless declaration, unsafe/oracle escape, or proof placeholder |
| scoped exact-candidate scan across installed pinned package Lean sources | 1 | expected no-match: no Martin's-axiom, forcing-axiom, or dense-family-solver declaration found |
| scoped Rasiowa-Sikorski scan in pinned mathlib | 0 | only the weaker `Encodable`-family construction was found; no exact target |
| target-scoped Git history review | 0 | history contains the local proposition, conditional architecture, and blocker evidence only; no unconditional body was found |
| JSON parse plus target-scoped blocker assertions | 0 | current base, blocked open state, unchanged vector, false proof/completion flags, exact changed paths, and absent self-test agreed |
| tracked and untracked whitespace checks on the target handoff | 0 | no whitespace errors or diagnostics |

The successful Lean commands validate the exact statement, the frozen conditional child-to-root
composition, and the strict countable-family boundary only. They are evidence for this blocker
boundary, not a proof of Martin's axiom. Exact structured details and hashes are recorded in the
sibling JSON artifact.
