# THM-M-0168 proof recheck at `443b8bbc`

Item: `S56-M-0168-PROOF`

Date: `2026-07-15T11:38:19+08:00`

Base revision: `443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b`

Base tree: `c5771c47c12b80aba613e6d844570f83b39ded6d`

## Verdict

`blocked`. The exact target
`Stage1Instances.THM_M_0168.BernsteinMinimalGraphTarget` still has no
eligible premise-free proof body in this repository or the pinned dependency
closure. The proof item remains `[ ]`; lifecycle remains `planned`; the
provisional obligation-registry/proof-recheck root vector remains
`[H1, M2, R3]`; and root closure, audit completion, validation, release, and
theorem completion remain false.

The existing `Proof.lean` does contain a real placeholder-free proof of the
independent affine-integration package. `constantPartials_to_affine`
reconstructs the full Frechet derivative from its values on the two coordinate
directions and applies mathlib's connected-domain derivative theorem. Its
wrapper is an exact inhabitant of `ConstantPartialsToAffine`, so only
`M0168-T-INTEGRATE` has provisional proof support.

`bernstein_of_derivativeRigidity` is conditional: it consumes
`DerivativeRigidity` as a premise and does not construct that premise. It also
targets the proposition duplicated in the obligation-harness namespace; no
checked transport to the canonical declaration in `Statement.lean` is added.
The remaining mathematical root cut is:

- `M0168-C-GRAPH`
- `M0168-N-PDE-MINIMAL`
- `M0168-L-STABILITY`
- `M0168-C-CUTOFF`
- `M0168-L-CURVATURE`
- `M0168-L-DERIVATIVE-RIGIDITY`

The first unavailable package is `M0168-C-GRAPH`: there is no eligible body
constructing the graph immersion, induced metric, unit normal, and second
fundamental form required by the frozen route. The pinned source scan found no
minimal-surface, mean-curvature, or minimal-graph theorem. The exact-name scan
found no root or rigidity body outside this dossier. A broader Bernstein-name
scan found only unrelated approximation-polynomial or Schroeder-Bernstein
material. Assuming rigidity or presenting the conditional wrapper as the root
would be a placeholder or a substituted theorem and was not done.

## Validation

All repository writes are confined to this owned blocker record. No
`lake update`, `lake build`, dependency clone/fetch, or deliberate dependency
repair was run. Direct trust-zero elaboration in disposable `/tmp` directories,
using the pinned Lean 4.29.0 executable and the already compiled package paths,
rechecked `Statement.lean`, `ObligationTree.lean`, and `Proof.lean`. The two
proof axiom reports were exactly `propext`, `Classical.choice`, and
`Quot.sound`; their captured logs reproduced the earlier SHA-256 values
`bc3bace903d4c39a16358b20c3e54224d63ee7c77db690c5eb0911c5daf8bd80`
and `baf43808013b12ba38dc0daee1bcafd26cc40d07f9dc77d7a36221155ea8b04b`.

The prescribed `lake env` surface is currently unusable. Its invocation
returned exit 1 with:

```text
error: .../Formalizations/Lean/.lake/packages/flt-regular: could not resolve
'HEAD' to a commit; the repository may be corrupt, so you may need to remove
it and try again
```

At observation time, the shared symlink target's `flt-regular` directory had
only `.git`, `.git/HEAD` was `ref: refs/heads/.invalid`, and `git rev-parse
--verify HEAD` exited 128. The package directory was not repaired or fetched.
Because concurrent workers use this shared canonical cache, and a `lake env`
invocation can attempt dependency materialization, this run makes no
`lake_mutated=false` or hermetic/release claim. The direct replay is only
scoped, warm-cache blocker evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 unique targets and ranks passed. |
| `python3 scripts/stage1_target.py show THM-M-0168` | 0 | Rank 665; planned; hard-statement-first partial-verification lane; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0168/check_statement.py` | 1 | Blocked before elaboration because `lake env` could not resolve `flt-regular` HEAD. |
| `python3 Stage1_Instances/THM-M-0168/check_anchor_audit.py` | 0 | Audit boundary, five declared probes, pinned mathlib revision, and immutable external metadata passed. |
| `python3 Stage1_Instances/THM-M-0168/check_obligation_tree.py` | 0 | Eleven nodes and the typed acyclic proof graph passed; the root remains frozen open. |
| direct trust-zero disposable replay with pinned Lean and compiled package paths | 0 | Statement and the obligation/proof harness elaborated; proof axiom reports were exactly the three allowed classical/kernel axioms listed above. |
| owned Lean prohibited-device scans | 1, expected | No `sorry`, `admit`, `sorryAx`, bodyless declaration, unsafe escape, or native oracle occurs. |
| pinned geometry and outside-dossier exact-name source scans | 1, expected | No supporting minimal-surface geometry or exact root/rigidity body was found. |
| scoped input diff from proof integration commit `5112156d` | 0 | No statement, obligation, proof, registry, graph, audit, target-manifest, skill, toolchain, or dependency-manifest input changed. |
| `cd Formalizations/Lean && lake env lean --version` | 1 | The shared `flt-regular` package could not resolve `HEAD`. |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse --verify HEAD` | 128 | The shared package checkout has no valid HEAD. |

## Retry Condition

Resume proof work after placeholder-free implementations of graph geometry,
PDE/minimality, stability, logarithmic cutoff, curvature vanishing, and
derivative rigidity, or after an immutable compatible Lean 4 proof-bearing
declaration is available for pinned exact-type integration. For prescribed
`lake env` validation, the automation owner must separately restore the
manifest-pinned `flt-regular` artifact without treating this worker's shared
cache state as evidence.

This is a current-base blocker artifact, not a positive proof receipt. It does
not satisfy `S56-M-0168-PROOF`, propose scheduler state, or support theorem
completion. Because the assigned phase is not genuinely self-tested as
complete, `.stage1-worker-selftest.json` remains absent.
