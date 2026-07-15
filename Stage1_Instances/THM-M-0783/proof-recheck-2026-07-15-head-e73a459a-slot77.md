# THM-M-0783 proof recheck at `e73a459a` (slot77)

Item: `S56-M-0783-PROOF`

Intent: `prove`

Recorded: `2026-07-15T18:22:38+08:00`

Base revision: `e73a459aa33f8b656019c9c36e3d5dfc84dffc30`

Base tree: `81105927f8e46d0076dd20433240ecf0fd185cea`

## Verdict

`blocked`. No placeholder-free proof body for the exact proposition
`Stage1Instances.THM_M_0783.MartinsAxiom` exists in the repository-local pinned dependency closure.
The target is object-level Martin's axiom, an additional set-theoretic axiom rather than a theorem
derivable from the selected Lean/mathlib foundation. Blueprint section 3.1 classifies `H5` as a
terminal classification that blocks ordinary theorem-proof execution pending target redirection.

The sole substantive proof leaf, `M0783-L-DENSE-FAMILY`, is definitionally
`ExpandedMartinsAxiom`. It must construct a filter meeting every suitably bounded dense family in
every nonempty ccc partial order, uniformly for every cardinal below the continuum. The existing
`root_of_denseFamilySolver` consumes that entire proposition as an explicit premise and transports
it to the canonical target. It is checked conditional composition, not an unconditional proof body.

Pinned mathlib contains the Rasiowa-Sikorski construction for an `Encodable` family in
`Mathlib/Order/Ideal.lean`. This countable-family result is strictly weaker than the frozen target and
cannot receive proof credit. A fresh scoped scan found no Martin's-axiom, forcing-axiom, or
dense-family-solver declaration in any installed pinned package source.

This attempt does not introduce the target with `axiom`, a bodyless declaration, or an extra premise;
use a placeholder; weaken the cardinal, ccc, order, density, family, or filter contract; or
substitute a relative-consistency, independence, countable-family, CH-conditional, or consequence
theorem. Those routes change the foundation or target and cannot satisfy this proof phase.

The item remains `[ ]`, lifecycle remains `planned`, and the root remains `[H5, M4, R4]`. No proof
receipt, worker `[_]`, accepted state, audit completion, theorem completion, validation, release, or
master acceptance is claimed. Because the positive proof phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.

## Failed Gate

The first failed gate is exact kernel closure of `M0783-L-DENSE-FAMILY` without placeholders,
undeclared premises, or a foundation extension. The proof-relevant cut is:

```text
M0783-L-DENSE-FAMILY
```

The full frozen cut additionally contains `M0783-X-SOURCE`, `M0783-X-FOUNDATION`,
`M0783-X-PROVENANCE`, `M0783-X-READABLE`, and `M0783-X-WORKFLOW`. A retry requires an immutable,
license-compatible Lean 4 terminal body for the exact target with acceptable exact-type, axiom,
placeholder, provenance, and composition reports. Alternatively, the master must redirect this
additional axiom to a theory-extension, consistency, or independence target. That is a target-policy
correction, not proof completion.

## Narrow Validation

The automation-provided `Formalizations/Lean/.lake` symlink was treated as read-only. No `lake
update`, `lake build`, dependency clone/fetch, or checkout repair was run. Narrow elaboration used
`lake env lean` only with the existing pinned toolchain and package objects; fresh outputs were
isolated under `/tmp` and removed. Preflight `git status --short` reported only that untracked
automation symlink, so this is dirty-clone, nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `git status --short` | 0 | only the automation-provided untracked `Formalizations/Lean/.lake` symlink; the owned target and self-test paths were clean |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0783` | 0 | rank 788, planned, legacy artifacts unaccepted, theorem incomplete |
| `LEAN_NUM_THREADS=1 timeout --foreground --kill-after=10s 600s python3 Stage1_Instances/THM-M-0783/check_statement.py` | 0 | canonical expression hash `c5896a33...5599ada`; all four structural mutations killed; pinned Lean 4.29.0 and mathlib `8a178386...ea95` |
| `python3 Stage1_Instances/THM-M-0783/check_obligation_tree.py` | 0 | 12 obligations and 28 typed edges passed; denominator `0581a4ed...25532c9`; root open M4 |
| `python3 Stage1_Instances/THM-M-0783/check_anchor_audit.py` | 0 | anchor boundary, six probes, statement status, and pinned mathlib revision passed |
| pinned `lake env lean --trust=0 -t0` on isolated copies of `Statement.lean` and `ObligationTree.lean` | 0 | exact statement and conditional composition elaborated; olean hashes `a3bd8eef...415c6` and `0098b71d...f550`; axiom report `[propext, Classical.choice, Quot.sound]`; temporary outputs removed |
| scoped prohibited-construct scan of owned Lean source | 1 | expected no-match: no `sorry`, `admit`, bodyless declaration, unsafe/oracle escape, or proof placeholder |
| scoped exact-candidate scan across installed pinned package Lean sources | 1 | expected no-match: no Martin's-axiom, forcing-axiom, or dense-family-solver declaration was found |
| scoped Rasiowa-Sikorski scan in pinned mathlib | 0 | only the weaker `Encodable`-family construction was found; no exact target |

The successful Lean commands validate the exact statement and the already frozen conditional
child-to-root composition. They are evidence for this blocker boundary, not a proof of Martin's
axiom. Exact structured details and hashes are recorded in the sibling JSON artifact.
