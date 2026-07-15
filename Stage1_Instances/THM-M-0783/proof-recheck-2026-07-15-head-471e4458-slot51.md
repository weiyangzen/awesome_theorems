# THM-M-0783 proof recheck at `471e4458` (slot51)

Item: `S56-M-0783-PROOF`

Intent: `prove`

Recorded: `2026-07-15T20:19:14+08:00`

Base revision: `471e4458269351ee096972776c478d019941b679`

Base tree: `e30e1cefce39148420ccc4525b726d57f58ee94b`

## Verdict

`blocked`. No placeholder-free terminal proof body for
`Stage1Instances.THM_M_0783.MartinsAxiom` exists in the repository-local pinned dependency closure.
The exact target is object-level Martin's axiom, an additional set-theoretic axiom rather than an
ordinary theorem supplied by the selected Lean/mathlib foundation. The dossier provisionally
classifies it as `H5`; Blueprint section 3.1 makes that a barrier to ordinary proof execution.

The sole substantive proof leaf, `M0783-L-DENSE-FAMILY`, is definitionally
`ExpandedMartinsAxiom`, so it is the whole missing proposition. The existing
`root_of_denseFamilySolver` accepts that entire proposition as an explicit premise and transports it
to `MartinsAxiom`. This checks conditional child-to-root composition but provides no inhabitant and
no root proof credit.

Pinned mathlib contains only the strictly weaker Rasiowa-Sikorski construction for an `Encodable`
dense family in `Mathlib/Order/Ideal.lean`. A current scoped scan found no Martin's-axiom,
forcing-axiom, or dense-family-solver declaration in any installed pinned package source. The target
history likewise contains only the proposition, the empty-family boundary, conditional
composition, and blocker evidence; no unconditional proof body was found.

This worker does not claim to have formalized or newly validated an independence theorem. The
source and independent-review gates remain open. The directly checked blocker is narrower: there is
no allowed exact terminal body in the bounded pinned closure. Introducing an axiom or premise,
weakening the cardinal/ccc/order/density/filter contract, or substituting a consistency,
independence, CH-conditional, countable-family, or consequence theorem would change the foundation
or target and is forbidden.

The item remains `[ ]`, lifecycle remains `planned`, and the established proof-phase root vector
remains `[H5, M4, R4]`. No proof receipt, worker `[_]`, accepted state, audit completion, theorem
completion, validation, release, or master acceptance is claimed. Because the proof phase is not
genuinely complete, `.stage1-worker-selftest.json` is deliberately absent.

One prerequisite artifact remains internally stale: the `M0783-ROOT` node in
`typed-graphs.json` says `M3`, while its closure boundary, `anchor-audit.json`, the obligation-tree
checker, and proof receipts classify the open root as `M4`. This proof worker does not rewrite the
frozen prerequisite artifact; master reconciliation is still required.

## Failed Gate

The first failed gate is exact kernel closure of `M0783-L-DENSE-FAMILY` without placeholders,
undeclared premises, or a foundation extension. The proof-relevant root cut is:

```text
M0783-L-DENSE-FAMILY
```

The complete frozen cut additionally contains `M0783-X-SOURCE`, `M0783-X-FOUNDATION`,
`M0783-X-PROVENANCE`, `M0783-X-READABLE`, and `M0783-X-WORKFLOW`. Retry requires an immutable,
license-compatible Lean 4 terminal proof body for the exact target with acceptable exact-type,
axiom, placeholder, provenance, and composition reports. Alternatively, the master must redirect
this additional axiom to a theory-extension, consistency, or independence target. Such redirection
is a target-policy correction, not proof completion.

## Narrow Validation

The automation-provided `Formalizations/Lean/.lake` symlink was treated as read-only. No dependency
update, build, clone, fetch, or checkout repair was run. Preflight `git status --short` reported only
that symlink, so this is dirty-clone, nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `git status --short` | 0 | only `?? Formalizations/Lean/.lake`; owned target and self-test paths were clean |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 and the uniform L0/rework-required baseline passed |
| `python3 scripts/stage1_target.py show THM-M-0783` | 0 | rank 788, lifecycle `planned`, legacy artifacts unaccepted, theorem incomplete |
| `LEAN_NUM_THREADS=1 timeout --foreground --kill-after=10s 600s python3 Stage1_Instances/THM-M-0783/check_statement.py` | 0 | expression hash `c5896a33...5599ada`; all four structural mutations killed; pinned Lean 4.29.0 and mathlib `8a178386...ea95` |
| `python3 Stage1_Instances/THM-M-0783/check_obligation_tree.py` | 0 | 12 obligations and 28 typed edges passed; denominator `0581a4ed...25532c9`; root open M4 |
| `python3 Stage1_Instances/THM-M-0783/check_anchor_audit.py` | 0 | anchor boundary, six Lean probes, local statement status, and pinned mathlib revision passed |
| scoped prohibited-construct scan of owned Lean source | 1 | expected no-match: no `sorry`, `admit`, bodyless declaration, unsafe/oracle escape, or proof placeholder |
| scoped exact-candidate scan across installed pinned package Lean source | 1 | expected no-match: no Martin's-axiom, forcing-axiom, or dense-family-solver declaration found |
| scoped Rasiowa-Sikorski scan in pinned mathlib | 0 | only the weaker `Encodable`-family construction was found; no exact target |
| target-scoped Git history review | 0 | no unconditional proof body was found |
| JSON parse plus target-scoped blocker assertions | 0 | current base, blocked open state, unchanged vector, false completion flags, exact paths and cut, and absent self-test agreed |
| tracked and untracked whitespace checks on this handoff | 0 | no whitespace errors or diagnostics |

The statement checker uses the prescribed existing `lake env lean` route. Its successful result and
the obligation-tree checks validate the exact statement and already frozen conditional composition
only; they are blocker evidence, not a proof of Martin's axiom. Exact structured results and hashes
are recorded in the sibling JSON artifact.
