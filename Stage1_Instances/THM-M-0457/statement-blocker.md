# Exact-statement gate: blocked

Item: `S56-M-0457-STATEMENT`  
Base revision: `e4f68760f8779f934ed18b07dad15e4512436d06`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository source record. The
entry is named "Arakelov theory", and its complete proposition-like description is "intersection
theory of arithmetic surfaces". These identify a mathematical theory, not one theorem with an
ordered binder list, hypotheses, and conclusion. The intake dependency deliberately leaves the
specific theorem open and forbids substituting an arithmetic Hodge index theorem, adjunction
formula, or an abstract structure that merely assumes the desired pairing.

The historical paper can be identified more precisely as S. J. Arakelov, "Intersection theory of
divisors on an arithmetic surface", *Mathematics of the USSR-Izvestiya* 8(6) (1974), 1167-1180,
DOI `10.1070/IM1974v008n06ABEH002141`. Its indexed abstract says that the article explains how to
construct, for a nonsingular model of a curve over a number field, a divisor theory and intersection
numbers analogous to those on a compact algebraic surface. This confirms that the repository label
refers to a construction/theory containing multiple results; it does not select a unique numbered
theorem. The publisher full text was not accessible as a PDF in this run, and no theorem/page,
verbatim claim, local definitions, assumptions, normalizations, or errata were available for a
source-to-binder crosswalk.

Consequently, choosing a pairing-existence theorem, well-definedness theorem, bilinearity or
symmetry result, arithmetic Hodge index theorem, or adjunction formula would invent missing
mathematics. An unconstrained Lean structure carrying an intersection pairing would instead make
the result true by assumption. Both moves are forbidden broadenings/substitutions. The first failed
gate is section 5 canonical human-claim identity, before minimal imports, an elaborated expression
fingerprint, checked transports, or meaningful removed-hypothesis, changed-domain, binder-scope,
and boundary mutations can be produced. Machine status therefore remains `M4`.

## Pinned Lean boundary

The existing pinned mathlib tree was searched for `Arakelov`, `arithmetic surface`, and `arithmetic
divisor`; no matching source file was found among 7,882 Mathlib files. This is only a narrow
repo-local substrate observation, not the later anchor audit. No canonical statement exists to put
in a `.lean` file, so running `lake env lean` on an invented proxy would not be valid statement
evidence. The available environment is Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, with pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. No dependency update, fetch, or `.lake` mutation was
performed.

## Required unblock

An accountable source reviewer must select one exact result and record a stable edition or scan,
numbered theorem and page, verbatim claim, referenced definitions, all surface/base/divisor/Green
function hypotheses, normalization and codomain of the intersection operation, boundary and
degenerate cases, and errata. The selection must also explain why that result, rather than another
result in the theory, is the intended interpretation of `THM-M-0457`. Only then can a statement
worker encode the claim, minimize pinned imports, preserve and hash its elaborated expression, and
run the required structural mutations.

## Narrow validation evidence

Commands ran from this worker clone on 2026-07-12.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0457` | exit 0; rank 305, planned, `L0/rework_required`, legacy artifacts unaccepted, theorem incomplete |
| `rg -l -i 'Arakelov|arithmetic surface|arithmetic divisor' Formalizations/Lean/.lake/packages/mathlib/Mathlib \| wc -l` | exit 0; `0` matching Mathlib files |
| `find Formalizations/Lean/.lake/packages/mathlib/Mathlib -type f \| wc -l` | exit 0; `7882` files searched |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; `651c8acc...b1d2` and `321626c8...2d81` |

Known failures are exact source-statement identity, minimal-import determination, canonical Lean
elaboration, expression fingerprinting, checked transports, and all four statement mutations. The
assigned phase is not self-tested or complete, so no `.stage1-worker-selftest.json` is emitted. No
theorem completion or downstream-node credit is claimed.
