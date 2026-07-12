# Exact-statement gate: blocked

Item: `S56-M-1308-STATEMENT`  
Theorem: `THM-M-1308`  
Base revision: `c326cc33b70825386f90cf5d885ad451004fbbff`

## Decision

The canonical Lean 4 target cannot yet be truthfully elaborated. The repository record identifies
the 1993 Christodoulou-Klainerman result and summarizes it only as stability of Minkowski space.
The intake identifies Christodoulou and Klainerman, *The Global Nonlinear Stability of the
Minkowski Space*, Princeton Mathematical Series 41 (1993), as a discovery anchor, but no stable
copy, exact theorem/page, terminal wording, definition crosswalk, or errata review is present in
the repository. The intake therefore deliberately leaves the formal statement open.

The missing source facts determine non-equivalent propositions: the topology and number of ends
of the initial hypersurface; the precise strong asymptotic-flatness class; regularity, decay
weights, and smallness norm; vacuum constraint equations and normalization conventions; the
maximal globally hyperbolic development interface; future and past causal-geodesic completeness;
and the exact curvature, foliation, peeling, and asymptotic conclusions. Choosing these facts from
a popular summary or a later stability theorem would substitute or broaden the assigned theorem.

Consequently there is no exact ordered binder list, hypothesis list, conclusion, boundary-case
policy, or source-approved alternate encoding from which to construct a canonical Lean
expression. An abstract structure that stores vacuum development, completeness, or decay as
proposition-valued fields would merely assume the substantive theorem and is not introduced.
Without the canonical expression, a minimal import set, normalized expression hash, checked
transports, and the required removed-hypothesis, changed-domain, changed-binder-scope, and boundary
mutation suite cannot be meaningfully established.

## Lean boundary

A scoped repository search found no target-specific Lean module or declaration for this theorem.
A phrase-level search of the pinned mathlib source for Lorentzian, Minkowski-spacetime,
Einstein-equation, vacuum-Ricci, and geodesic-completeness vocabulary found no candidate terminal
declaration. This limited negative search is infrastructure evidence only, not the later anchor
audit and not evidence that no external formalization exists.

Running Lean on an invented proxy would validate only that proxy. The narrow real Lean check for
this blocked statement phase is therefore the pinned executable and dependency fingerprint. No
Lake update, build, clone, fetch, or other `.lake` mutation was performed.

## Required unblock

An accountable source review must pin a stable edition and record the exact theorem/page and all
referenced definitions, assumptions, conventions, conclusion clauses, and known errata. It must
crosswalk those items to the ordered Lean binders and approve explicit treatment of Minkowski data
and every other boundary case. A later statement execution can then encode that exact claim,
minimize its pinned imports, serialize its elaborated expression and environment, check any
alternate transports, and run all four mutation classes.

## Narrow validation evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai). Lake commands ran from
`Formalizations/Lean` against the existing pinned artifacts.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1308` | 0 | rank 475; planned; L0/rework-required; theorem incomplete |
| `rg -n -i 'Christodoulou[- ]Klainerman\|global nonlinear stability of (the )?Minkowski' Formalizations/Lean/AwesomeTheorems Stage1_Instances/THM-M-1309 --glob '!**/.lake/**'` | 0 | one neighboring exclusion only; no target-specific Lean declaration |
| `rg -n -i 'Lorentzian\|Minkowski spacetime\|Einstein equation\|Ricci.*vacuum\|geodesically complete' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | no matching source line and no candidate terminal declaration |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && git -C .lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | hashes `651c8acc...b1d2` and `321626c8...2d81` |
| `git diff --check -- Stage1_Instances/THM-M-1308` | 0 | no whitespace errors |

First failed gate: exact canonical human-claim identity. Known failures are exact Lean
elaboration, minimal-import determination, expression/environment serialization, checked
transports, and all four mutation classes. The assigned deliverable is not self-tested to
completion, so no `.stage1-worker-selftest.json` is emitted. This artifact claims neither statement
acceptance nor audit/theorem completion and does not modify execution state.
