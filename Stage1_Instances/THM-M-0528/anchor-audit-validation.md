# Anchor-audit validation record

Item: `S56-M-0528-ANCHOR_AUDIT`  
Base revision: `32ebb5b683ce29d721974e08403e48f86ecd7bd9`

## Result

Pinned mathlib at `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains the exact pointwise
terminal theorem `IsCoveringMap.eq_of_comp_eq` in `Mathlib.Topology.Covering.Basic`. Its binder
order, preconnectedness premise, two continuity premises, composite equality, witness agreement,
and function-equality conclusion match every binder of the frozen target. `AnchorAudit.lean`
independently elaborates a full-target adapter, rather than relying on a name match.

The pinned source defines the terminal body through the separated-map uniqueness theorem and the
local injectivity of a covering map's local-homeomorphism structure. Lean reports exactly
`propext`, `Classical.choice`, and `Quot.sound` for both the upstream theorem and the adapter. The
complete transitive trust audit remains downstream. Bounded public searches found no independent
external Lean 4 implementation; the GitHub code-search lane was rate-limited and is not claimed as
a negative result.

The anchor is classified `M1`: exact immutable closure and adapter feasibility are checked, but the
proof phase must own the canonical wrapper after the obligation registry is frozen. This audit
does not claim proof credit, H0, audit completion for the theorem as a whole, or theorem completion.

## Commands and results

Commands ran on 2026-07-12 using only existing pinned `.lake` artifacts. No update, build, clone,
or fetch was performed.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0528/AnchorAudit.lean` | 0 | Exact adapter elaborated; upstream type printed; both axiom sets were `propext`, `Classical.choice`, `Quot.sound` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0528/Statement.lean` | 0 | Frozen target and checked pointwise transport re-elaborated |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD^{tree}` | 0 | `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `sha256sum Formalizations/Lean/.lake/packages/mathlib/Mathlib/Topology/Covering/Basic.lean Formalizations/Lean/.lake/packages/mathlib/LICENSE` | 0 | `c9f48cf1...3890`, `b40930bb...33e1` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0528` | 0 | Rank 585, planned, legacy artifacts unaccepted, theorem incomplete |
| Sourcegraph exact-name and Hatcher-comment queries | 0 | Both returned `matchCount=0`; response hashes are recorded in `anchor-audit.json` |
| GitHub REST repository search for covering-map Lean 4 projects | 0 | `total_count=0`, complete response; response hash recorded |
| GitHub REST code search for the exact declaration | 0 | Rate-limit response; explicitly not treated as a negative search |

## Open gates

The obligation-tree phase must register the upstream bridge and its relevant terminal dependencies.
The proof phase must then add the canonical exact-target wrapper. Provenance, transitive trust,
hermetic replay, independent validation, source acceptance, and release remain open.
