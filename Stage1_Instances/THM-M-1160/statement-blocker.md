# Exact-statement gate: blocked

Item: `S56-M-1160-STATEMENT`  
Theorem: `THM-M-1160`  
Base revision: `767bcb5c33375def04fc8f536c5a5e3f27c31aa0`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository source record. The
entire mathematical wording is `位势在边界上的行为` ("behavior of potentials at the boundary"),
under the title "jump relations for potentials". This identifies a family of results, not one
proposition. In particular, the record does not select:

- a single-layer, double-layer, Newtonian, logarithmic, Cauchy, heat, or other potential;
- a kernel, normalization, ambient dimension, scalar field, or density space;
- a domain, boundary regularity class, boundary orientation, or trace convention;
- interior/exterior, normal-derivative, or nontangential boundary values;
- pointwise versus almost-everywhere scope, or the topology of the limiting assertion;
- the coefficient and sign of the jump, the principal-value term, or the exact equality;
- exceptional dimensions, boundary points, zero-density behavior, or unbounded-domain conditions.

These choices yield inequivalent theorems. For example, continuity of a single-layer potential,
the normal-derivative jump of a single layer, the value jump of a double layer, and the
Plemelj-Sokhotski formula are not interchangeable encodings. Selecting the familiar double-layer
formula merely from the title would invent missing mathematics and broaden the source record.

The Stage0 entry confirms that precise definitions, assumptions, proof, references, and machine
artifacts are all absent. The manifest's `已验证` value is explicitly untrusted metadata, not a
source-statement identifier or kernel receipt. The accepted intake dependency likewise records
this ambiguity at `[H4, M4, R4]` and deliberately makes no theorem-family choice.

Consequently this phase fails at canonical human-claim identity, before ordered binders,
hypotheses, a conclusion, minimal imports, an elaborated expression fingerprint, checked alternate
transports, or meaningful removed-hypothesis, changed-domain, changed-binder-scope, and boundary
mutations can be established. Creating an abstract structure with the desired relation as a field
would only assume the missing theorem and is prohibited by the intake scope.

## Repository and pinned-library boundary

The manifest assigns no accepted legacy priority slot, and there is no target-specific historical
Lean module to re-audit. A scoped repository search found only an unrelated abstract
Riemann-Hilbert interface in `AwesomeTheorems/Stage1/S1_M_178.lean`; its jump relation is a
caller-supplied proposition with a proof field. It is neither a concrete potential-theory theorem
nor an admissible substitute for this target.

A scoped search of the pinned mathlib source found no declaration text matching jump relations,
single- or double-layer potentials, or Plemelj-Sokhotski. This is limited discovery evidence, not
the later anchor audit. More importantly, a library candidate could not by itself resolve which
human theorem this ambiguous source record denotes.

## Required unblock

An accountable source reviewer must identify a stable primary source by edition, theorem/page, and
exact wording, including referenced definitions, assumptions, conventions, and errata. The review
must freeze the potential and kernel, normalization, dimension and scalar field, density and trace
spaces, domain and boundary hypotheses, orientation and signs, quantifier order, exact jump formula,
limit semantics, and all boundary and degenerate cases. A later statement worker can then encode
that claim without substitution, minimize its pinned imports, serialize and hash the elaborated
expression, check any alternate transports, and execute the four required mutation classes.

## Narrow validation evidence

Commands ran from this worker clone on 2026-07-12 using the existing pinned environment. No
`lake update`, build, dependency clone/fetch, or mutation of `.lake` was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1160` | 0 | rank 363; planned; no accepted legacy artifacts; theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | `651c8acc...b1d2` and `321626c8...2d81` |
| `rg -n -i 'jump relation\|jumpRelations\|jump_relation\|double.?layer\|single.?layer\|Plemelj\|Sokhotski' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | no matching pinned mathlib source text |

First failed gate: exact source-statement identity. Known failures are the canonical Lean target,
minimal-import determination, expression fingerprint, checked transports, and all four mutation
classes. The assigned phase is not self-tested or complete, so no `.stage1-worker-selftest.json`
is emitted. No statement acceptance, audit completion, or theorem completion is claimed.
