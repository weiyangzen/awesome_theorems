# Statement gate blocker

Item: `S56-M-0437-STATEMENT`  
Theorem: `THM-M-0437`  
Verdict: blocked; no exact canonical Lean target is claimed.

## First failed gate

The repository metadata does not identify an exact mathematical proposition. It gives the title
"志田簇", the gloss "Hodge型志田簇的构造", an attribution to Goro Shimura, and the year 1964,
but no primary-source work, theorem number, page, hypotheses, or definitions. The intake reasonably
records "Hodge-type Shimura varieties" as a normalization hypothesis, while explicitly leaving the
exact source variant open. That phrase still does not select one proposition. In particular, it
does not decide between:

1. construction or algebraicity of the complex double quotient for a Hodge-type Shimura datum;
2. existence and characterization of a canonical model over the reflex field;
3. a moduli/representability theorem obtained through an embedding into a Siegel datum; or
4. a stronger integral-canonical-model construction with level and reduction hypotheses.

These roots have materially different domains, ordered binders, level assumptions, conclusions,
and boundary cases. Choosing one from the title alone would broaden or substitute the source claim.
The intake crosswalk also says that exact theorem/page selection remains open and forbids choosing
between these variants by convenience. Consequently rev-5.6 section 5's exact-statement gate cannot
truthfully produce a canonical expression, serialized expression hash, checked transports, or
meaningful removed-hypothesis/domain/binder-scope/boundary mutations.

The historical module
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_066.lean` cannot repair the identity failure. Its
`StatementShape` quantifies over three caller-supplied predicates for moduli representability,
Hodge realization, and the canonical-model property. Its arithmetic `ShidaDatum` likewise stores
the Hodge-type, level, and PEL conditions as unconstrained `Prop` fields. The module itself labels
this as a statement-shape boundary rather than a terminal theorem. It elaborates successfully in
the pinned environment, but it is not an exact encoding of any of the candidate source theorems and
receives no rev-5.6 statement credit.

The pinned mathlib source contains no declaration matching `Shimura`, `HodgeType`, "Hodge type",
"reflex field", or "canonical model". This negative local search is not an external-candidate
audit; it only confirms that the missing exact root cannot be replaced by a known pinned mathlib
definition during this statement phase. No `sorry`, axiom, opaque proxy predicate, placeholder,
or alternate theorem was introduced. Machine debt remains `M4` because an exact usable formal
target has not been identified.

## Environment fingerprint

- Repository base revision: `91cf43768c2b03b5c98d8ca436c450ba5a70babb`.
- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain pin: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- Lake manifest SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Historical discovery module SHA-256:
  `37ccb3ce9bf04d067ec979679a67adafbe5f2fb41e825e6731f200df53eab16a`.

The worker clone uses the canonical pinned `.lake` directory through the existing
`Formalizations/Lean/.lake` symlink. No update, build, fetch, or clone command was used.

## Validation evidence

Commands ran from the repository root unless a leading `cd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard passed: 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | Manifest passed: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0437` | 0 | Rank 66, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_066.lean` | 0 | Historical interface/statement-shape module elaborated with no diagnostics; it does not supply an exact source-faithful root |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Checked mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i 'Shimura\|Hodge type\|HodgeType\|reflex field\|canonical model' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | No matching declaration or source occurrence in pinned mathlib |

## Retry condition

Provide an immutable primary-source edition and an exact theorem/page that identifies the selected
construction theorem, with its definitions, hypotheses, notation, and any errata. The statement
phase must then map all assumptions, choose source-faithful Lean definitions for the Shimura datum,
Hodge embedding, level, reflex field, quotient/moduli object, and canonical-model property, and
elaborate and mutation-test that expression with minimal pinned imports.

Until that condition is met, statement acceptance, audit completion, and theorem completion are
false. Because the assigned phase is not self-tested to its completion gate, no
`.stage1-worker-selftest.json` is emitted.
