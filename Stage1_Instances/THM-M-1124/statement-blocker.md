# Statement-phase blocker

Item: `S56-M-1124-STATEMENT`  
Theorem: `THM-M-1124`  
Base revision: `bce5c3a2691f71daf054f0f11b5cf66c120a7306`

## Verdict

The exact-statement gate is blocked and the machine status remains `M4`. No canonical Lean target,
expression fingerprint, transport, or mutation suite was created. Consequently this phase is not
self-tested and must not be presented for master acceptance.

The repository's entire source claim is the label "Lawler-Schramm-Werner theorem", the year 2001,
and the gloss "SLE and critical phenomena". That description does not select a proposition. In
particular, the 2001 Lawler-Schramm-Werner literature contains at least the distinct half-plane and
plane Brownian intersection-exponent families. Selecting either family, or one convenient exponent
from a family, would decide proposition-changing geometry, events, parameters, normalization, and
conclusions that the repository never states.

The accepted intake therefore deliberately leaves open the exact paper and numbered result, the
plane or half-plane setting, Brownian path/excursion/packet representation, avoidance or
disconnection event, stopping geometry, exponent definition, admissible parameter range, formula,
normalization, and boundary cases. No immutable primary-source theorem transcription resolving
those choices exists in the repository. Freezing them from memory or bibliographic metadata would
invent missing mathematics and violate the rev-5.6 exact-claim hard stop.

There is also no honest coarse Lean fallback. The scoped repository and pinned-mathlib searches
found no theorem-specific declaration for Lawler-Schramm-Werner or Brownian intersection exponents.
An abstract structure carrying the avoidance asymptotic or exponent formula as a `Prop` field would
assume the desired theorem rather than express it, and is expressly excluded by the intake scope.

## First failed gate and retry condition

First failed gate: rev-5.6 exact canonical mathematical claim and source-statement identity, before
Lean elaboration.

Retry only after an immutable primary edition has been inspected and independently cross-checked,
with all of the following frozen:

- paper, numbered theorem/corollary, page, definitions, edition hash, and errata status;
- plane versus half-plane domain and all starting, stopping, and independence conditions;
- the precise avoidance, nonintersection, or disconnection event;
- the exponent's limiting/asymptotic definition and normalization;
- every multiplicity or real parameter, its range, and all degenerate/boundary cases;
- the exact explicit formula and ordered quantifier structure.

Only then can a source-faithful Lean object model be implemented with minimal pinned imports and
checked by exact-expression, transport, and mutation probes. Lean availability is not the blocker;
the missing uniquely identified mathematical proposition is.

## Commands and results

Commands ran from the worker-clone root on 2026-07-12 (Asia/Shanghai), except where a subshell is
shown. Existing `.lake` artifacts were read only. No update, build, clone, fetch, or dependency
mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1124` | 0 | rank 564, lifecycle planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `651c8acc...b1d2` and `321626c8...2d81` |
| `rg -n -i 'Lawler.?Schramm.?Werner\|Brownian intersection exponent\|intersection exponents\|SLE and critical phenomena\|critical phenomena' . --glob '!Formalizations/Lean/.lake/**' --glob '!Stage1_Instances/THM-M-1124/**'` | 0 | only broad repository metadata and neighboring dossier references; no exact source transcription or Lean target |
| `rg -n -i 'Lawler.?Schramm.?Werner\|Brownian intersection exponent\|intersection exponents' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems` | 1 | no matching pinned-mathlib or repository Lean declaration (`rg` exit 1 means no matches) |

No `lake env lean <target>` command is recorded because there is no source-frozen target to
elaborate. Elaborating a chosen special case or an assumption-bearing boundary structure would be
false evidence, not the smallest real validation. No `.stage1-worker-selftest.json` is written
because the assigned statement phase is not genuinely self-tested.
