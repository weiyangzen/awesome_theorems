# Source-statement crosswalk

## Available source record

`Docs/researches/math_theorems.md` and `Docs/Stage0_Blueprint.md` provide only the name "Tao theorem",
the phrase "global well-posedness of critical NLS", attribution to Terence Tao, year 2006, and an
untrusted `已验证` label. They provide no title, journal, DOI, theorem number, page, equation,
hypotheses, definitions, or errata. Stage0 explicitly leaves exact definitions and machine status
open. No primary-source claim is therefore made at intake.

## Crosswalk

| Source element | Information fixed | Information still required for Lean | Intake result |
|---|---|---|---|
| "critical NLS" | an NLS with a scaling-critical regime | equation, sign, exponent, dimension, critical space | unresolved |
| "global well-posedness" | a global solution theory is intended | solution predicate, existence, uniqueness, dependence, maximal interval | unresolved |
| "Tao" / 2006 | author and approximate date metadata | exact publication and theorem locator | insufficient to identify theorem |
| `已验证` | repository screening label only | inspectable proof and kernel receipt | no credit |

## Candidate boundary

Tao authored multiple results involving critical NLS, and nearby literature distinguishes
mass-critical from energy-critical equations, focusing from defocusing signs, radial from
non-radial data, and global existence from scattering. These are materially inequivalent Lean
targets. A downstream source audit must locate the intended 2006 primary publication and verify its
actual theorem before any candidate is adopted.

Repo search found `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_153.lean`, described there as a
Cazenave-Weissler critical-NLS statement candidate. It is discovery evidence for possible analytic
APIs only; different attribution and the absence of a source identity prevent statement or proof
credit for THM-M-1217.
