# THM-M-0168 proof recheck at `3c3068d5`

Item: `S56-M-0168-PROOF`

Date: `2026-07-15T12:25:00+08:00`

Base revision: `3c3068d5f6ad9d773ce52d46d68a43c2a9272683`

Base tree: `f9413d0895f280a855bb16104daf0403d51a24fb`

## Verdict

`blocked`. The exact canonical target
`Stage1Instances.THM_M_0168.BernsteinMinimalGraphTarget` has no eligible
premise-free proof body in this repository or its pinned Lean dependency
closure. The proof item remains `[ ]`, lifecycle remains `planned`, the
provisional proof-tree root remains `[H1, M2, R3]`, and root closure, audit
completion, validation, release, and theorem completion remain false.

The existing `Proof.lean` contains real placeholder-free proof work.
`constantPartials_to_affine` reconstructs the full Frechet derivative from
its two coordinate values, compares `u` with an explicit affine function,
and uses mathlib's connected-domain derivative theorem. Its wrapper is an
exact inhabitant of `ConstantPartialsToAffine`, so it provisionally supports
only `M0168-T-INTEGRATE`.

`bernstein_of_derivativeRigidity` instead consumes `DerivativeRigidity` as a
premise. It does not construct that premise and is not a proof of Bernstein's
theorem. It also targets the proposition duplicated in the obligation
harness; there is no checked transport to the canonical declaration in
`Statement.lean`. After crediting the integration body only, the remaining
root cut is:

- `M0168-C-GRAPH`
- `M0168-N-PDE-MINIMAL`
- `M0168-L-STABILITY`
- `M0168-C-CUTOFF`
- `M0168-L-CURVATURE`
- `M0168-L-DERIVATIVE-RIGIDITY`

The first unavailable package is `M0168-C-GRAPH`: no eligible body constructs
the graph immersion, induced metric, unit normal, and second fundamental form
required by the frozen route. The dependent PDE/minimality, stability,
logarithmic-cutoff, curvature-vanishing, and derivative-rigidity packages are
also absent. Pinned-source and repo-local exact-name searches found no such
terminal proof body. The prerequisite immutable anchor audit offers only
pointwise mean-curvature infrastructure, not entire minimal-graph rigidity.
Assuming rigidity or presenting the conditional wrapper as the root would be
a placeholder or substituted theorem and was not done.

## Validation

All writes are confined to this owned blocker record. No `lake update`,
`lake build`, dependency clone/fetch, or dependency repair was run. A direct
trust-zero replay copied the three Lean sources to a disposable `/tmp`
directory, used the pinned Lean 4.29.0 executable with the already compiled
package paths, isolated the network with `bwrap`, and removed all generated
files. `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` elaborated.
The axiom reports for `compose_root`, `constantPartials_to_affine`, and
`bernstein_of_derivativeRigidity` were exactly `propext`, `Classical.choice`,
and `Quot.sound`. The obligation and proof logs reproduced SHA-256 values
`bc3bace9...daf8bd80` and `baf43808...ea8b04b`.

The required `lake env` surface is presently unavailable. A bounded
`cd Formalizations/Lean && timeout 15s lake env lean --version` returned 124.
Inspection showed the shared automation-provided `.lake` symlink's
`flt-regular/.git/HEAD` is `ref: refs/heads/.invalid`; `git rev-parse HEAD`
fails. The attempted Lake command spawned `git fetch --tags --force origin`;
the worker terminated that child before completion and used no further Lake
command. The worker did not run a dependency fetch command, repair, remove, or
otherwise deliberately mutate the shared package.
Consequently this replay is warm-cache blocker evidence, not prescribed
`lake env`, hermetic, cache-integrity, or release evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 unique targets and ranks passed. |
| `python3 scripts/stage1_target.py show THM-M-0168` | 0 | Rank 665; planned; hard-statement-first partial-verification lane; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0168/check_statement.py` | terminated | Its Lake child spawned a dependency-fetch process after encountering the invalid shared `flt-regular` HEAD; the processes were terminated before completion and the generated temporary source was removed. |
| `python3 Stage1_Instances/THM-M-0168/check_anchor_audit.py` | 0 | Audit boundary, five declared probes, pinned mathlib revision, and immutable external metadata passed. |
| `python3 Stage1_Instances/THM-M-0168/check_obligation_tree.py` | 0 | Eleven nodes and the typed acyclic proof graph passed; the root remains frozen open. |
| direct network-isolated trust-zero replay with pinned Lean and compiled package paths | 0 | All three Lean sources elaborated; axiom reports were exactly the three allowed classical/kernel axioms above. |
| anchored prohibited-device scan over owned Lean sources | 1, expected | No executable placeholder, bodyless declaration, unsafe escape, or native oracle occurs. |
| pinned geometry and outside-dossier exact-name source scans | no eligible hits | Only unrelated Bernstein approximation and Schroeder-Bernstein material was found. |
| scoped input diff from proof integration commit `5112156d` | 0 | Statement, obligation, proof, registry, graphs, audit, manifest, skill, toolchain, and dependency manifest are unchanged. |
| `cd Formalizations/Lean && timeout 15s lake env lean --version` | 124 | Timed out while Lake attempted to materialize the dependency whose shared checkout has invalid HEAD. |

Proof-relevant source SHA-256 values remain `5e773260...1a78` for
`Statement.lean`, `642153a1...f24e` for `ObligationTree.lean`,
`2906d501...8299d` for `Proof.lean`, `883e0c0a...ed9ba` for the registry,
`1e8ac1d8...ac41` for typed graphs, and `f29dd210...d4f5b7` for the anchor
audit. The pinned toolchain is Lean 4.29.0 commit `98dc76e3...16740`; mathlib
is `8a178386...ea95`, tree `bdc39a31...1c2b`.

## Retry Condition

Resume proof work after placeholder-free implementations of the six remaining
mathematical packages, or after an immutable compatible Lean 4 proof-bearing
declaration becomes available for pinned exact-type integration. Separately,
the automation owner must restore the manifest-pinned `flt-regular` artifact
before prescribed `lake env` validation can run without dependency access.

This is current-base blocker evidence, not a positive proof receipt. It does
not satisfy `S56-M-0168-PROOF`, propose scheduler state, or support root or
theorem completion. Because the assigned phase is not genuinely self-tested
as complete, `.stage1-worker-selftest.json` remains absent.
