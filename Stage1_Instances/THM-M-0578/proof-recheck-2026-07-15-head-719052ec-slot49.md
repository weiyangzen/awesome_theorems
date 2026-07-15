# THM-M-0578 proof-phase recheck at base 719052ec (slot49)

Item: `S56-M-0578-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `719052ec5fae5190f38e013d646fd7461d29be5d`

Base tree: `a8de041884ae39d41031493cb436b3e4a66bbfa0`

## Verdict

`blocked`. The exact frozen proposition
`Stage1Instances.THM_M_0578.MilnorExoticSphereTarget` still has no eligible
terminal Lean 4 proof body in the repository or pinned dependency closure. No
proof body was added. The proof item remains `[ ]`, the root vector remains
`[H3, M4, R4]`, and root closure, validation, release, audit completion, and
theorem completion remain false.

The frozen immediate root cut remains:

- `M0578-C-BUNDLE`: construct the selected smooth Milnor bundle total space;
- `M0578-T-HOMEO`: identify it with the fixed unit seven-sphere by a homeomorphism;
- `M0578-O-NONDIFF`: exclude every smooth diffeomorphism to that sphere.

The first failed proof gate is terminal proof-body availability for
`M0578-C-BUNDLE`. The checked theorem
`ObligationTree.root_of_exoticWitnessPackage` is conditional composition only:
its premise already contains the smooth manifold, homeomorphism, and
nondiffeomorphism certificate. It constructs none of the open packages and
cannot receive root proof credit.

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`
contains the exact signature only as
`proof_wanted exists_homeomorph_isEmpty_diffeomorph_sphere_seven`.
`proof_wanted` does not retain a declaration in the environment. The checked
source and all-ref history still provide only the discarded marker, not a
proof-bearing replacement.

A current search of the existing pinned package sources found no retained
Milnor/exotic-sphere, Eells-Kuiper, or homotopy-sphere proof. Nearby generic
fiber-bundle and manifold APIs do not construct the required smooth Milnor
sphere bundle. The generalized-Poincare homeomorphism bridge in the same
module is also `proof_wanted`, and the pinned closure has no distinguishing
smooth invariant with enough invariance to derive `IsEmpty Diffeomorph`.
Mathlib's bordism module explicitly leaves bordisms and bordism groups as
future work.

The standard-sphere shortcut remains invalid: `Diffeomorph.refl` inhabits the
standard sphere's self-diffeomorphism type, so that type cannot be `IsEmpty`.
Supplying a different atlas together with the required emptiness certificate
would be exactly the missing exotic-smooth-structure theorem, not an encoding
shortcut.

The repository base advanced after the prior `b62c08f2` recheck by integrating
that blocker packet. A proof-input whitelist diff is empty and all frozen
source hashes are unchanged. The mathematical blocker therefore persists at
this base.

Closing the route requires placeholder-free Lean implementations of the
Milnor sphere-bundle construction and boundary conventions, its homeomorphism
to the fixed unit seven-sphere, and distinguishing smooth-invariant
computations with invariance strong enough to derive `IsEmpty Diffeomorph`.
Assuming a missing package, crediting `proof_wanted`, or returning only the
conditional composer would violate the exact theorem boundary and was not
done.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink points at shared canonical pinned
artifacts and was reused read-only. No `lake update`, `lake build`, dependency
clone/fetch, checkout repair, network request, or dependency mutation command
was issued. The statement validator was started under a 180-second timeout;
under concurrent worker load the orchestration call returned before that run
produced a result, so it is not credited below. No temporary target file
remains.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0578` | 0 | Rank 622; planned; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0578/check_anchor_audit.py` | 0 | Exact marker and discard semantics passed at the pins; root remains M4 formalization debt. |
| `python3 Stage1_Instances/THM-M-0578/check_obligation_tree.py` | 0 | 13 obligations and 28 typed edges passed; denominator `67da617160dcfef6ea2eb819f105ab0e2a68a351476d55e5761d2e668e63aeda`; root remains open M4. |
| `cd Formalizations/Lean && timeout --foreground 60s lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`. |
| source hashes and pinned Git revision probes | 0 | All statement, registry, graph, audit, validation-spec, toolchain, and manifest hashes match the previous recheck; mathlib is pinned at `8a178386...`. |
| existing pinned-package retained-body and prerequisite search | 0 | Only the discarded marker was found; the required construction, classification bridge, and smooth obstruction remain unavailable. |
| forbidden-construct scan of owned Lean files | 1 | Expected no-match exit; no prohibited proof escape was found. |
| scoped `git diff --name-status b62c08f2..HEAD` | 0 | Empty for all proof-input files and Lean pins; the whole-target delta contains only the prior blocker packet. |
| companion JSON parse and added-file/final whitespace checks | 0 | JSON is valid; both expected added-file diff exits had no diagnostic, and the final target-local check passed. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest is absent because the proof phase is incomplete. |

## Retry Condition

Resume after placeholder-free implementations of `M0578-C-BUNDLE`,
`M0578-T-HOMEO`, and `M0578-O-NONDIFF` with their frozen child obligations.
Alternatively, integrate an immutable compatible Lean 4 proof-bearing
declaration of the exact root with a complete dependency lock, license record,
and terminal-body provenance, then rerun node-scoped exact-type, trust,
provenance, and composition checks.

This is a current-base nonrelease blocker record. It is not a proof receipt,
does not satisfy `S56-M-0578-PROOF`, proposes no state change, and supports
neither root closure nor theorem completion. Because the assigned proof phase
is incomplete, `.stage1-worker-selftest.json` is intentionally absent.
