# Exact-statement gate: blocked

Item: `S56-M-0098-STATEMENT`

Theorem: `THM-M-0098`

Base revision: `95073b656f2c285c788e4814325a47fdb4dc1879`

## Decision

The exact Lean 4 target is **blocked** at canonical claim identity. The complete repository record
names the "Langlands program fundamental lemma" but gives only the gloss "a correspondence between
automorphic representations and Galois representations." The title normally points to the
Langlands-Shelstad endoscopic Fundamental Lemma, whose conclusion is a normalized orbital-integral
identity. The gloss instead points to a local or global Langlands correspondence. These are
different theorem families, not alternate encodings of one proposition.

The existing self-tested planned intake therefore leaves the canonical claim, domains, binders,
hypotheses, conclusion, boundary cases, Lean module, expression, and expression hash null. It
requires an immutable primary source and independent reconciliation or an authoritative
source-correction decision before any of them can be selected. Choosing either branch from one
metadata field would broaden or substitute the target. Copying sibling `THM-M-0434` or
`THM-M-0430`, narrowing to a familiar proved special case, or putting the desired
equality/correspondence into an abstract structure would violate that boundary. The intake itself
is only `[_]` pending master acceptance; this report grants it no accepted state.

Without one exact proposition, "minimal imports" is undefined. There is likewise no meaningful
expression fingerprint, alternate-form transport, or removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutation suite. The root remains `[H5, M4, R4]`: provisional
`H5` classifies the current catalog record as not a stable proposition, not either candidate theorem
as false or independent.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated with its six direct imports. It checks
`AlgebraicGeometry.Scheme`, `Field.absoluteGaloisGroup`,
`MeasureTheory.Measure.IsHaarMeasure`, `IsNonarchimedeanLocalField`,
`NumberField.AdeleRing`, and `Representation`. These are adjacent APIs for the two incompatible
readings. They do not select or elaborate either root and receive no statement or proof credit.

A bounded source search in the pinned Mathlib tree found no endoscopy, orbital-integral,
transfer-factor, or Langlands declaration under the recorded terms. That negative result is only a
local feasibility boundary; it is not the later anchor audit. The sibling legacy files are also
ineligible: `S1_M_058.lean` supplies an expected correspondence and compatibility as structure
fields, while `S1_M_083.lean` supplies orbital-integral/transfer data through statement-boundary
interfaces. Neither is a source-faithful canonical target for this ID.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and
Mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. The existing untracked
`Formalizations/Lean/.lake` link to the canonical pinned artifacts was used read-only. No update,
build, dependency clone, fetch, or other dependency mutation was run.

## Validation evidence

Commands ran in this worker clone on `2026-07-12` (`Asia/Shanghai`). The Lean commands ran from
`Formalizations/Lean`; all others ran from the repository root unless stated otherwise.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0098` | 0 | rank 899, `planned`, legacy artifacts unaccepted, theorem incomplete |
| `lake env lean ../../Stage1_Instances/THM-M-0098/IntakeProbe.lean` | 0 | all six adjacent APIs elaborated and their types were printed; no canonical target was checked |
| `lake env lean --version && lake --version` | 0 | Lean and Lake versions match the fingerprint above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | the checked Mathlib revision matches the manifest pin |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Stage1_Instances/THM-M-0098/IntakeProbe.lean` | 0 | hashes `651c8a...1d2`, `321626...d81`, and `fcbd2a...bf2c` match the structured blocker |
| `rg -n -i 'endoscop\|orbital[ _-]?integral\|transfer[ _-]?factor\|langlands' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | no match in the pinned Mathlib source; exit 1 is the expected no-match result |
| repository search for the target ID, title, gloss, and English title | 0 | only conflicting catalog metadata and the fail-closed intake were found; no exact proposition |
| `rg -n '\b(sorry\|admit)\b\|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-0098 -g '*.lean'` | 1 | expected no-match result; the target's Lean probe contains no prohibited placeholder or axiom declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0098/statement-blocker.json >/dev/null` | 0 | structured blocker parsed successfully |
| per-file `git diff --no-index --check /dev/null` for the two new owned artifacts | 1 per file | expected add-file diff status with no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest is absent because the statement completion gate did not pass |

## Retry condition

An accountable reviewer must preserve and hash an immutable primary-source edition or approve an
authoritative catalog correction, reconcile the title, gloss, attribution, and date, transcribe one
exact result and its referenced definitions, audit assumptions and errata, and independently approve
the mapping. The selected source must freeze local/global or group/Lie-algebra scope as applicable,
all domains and ordered binders, compatibility or normalization conventions, directionality,
conclusion, and boundary cases.

A later statement worker must then encode that exact claim using native or immutably pinned Lean
objects, minimize imports, serialize and hash its elaborated expression and environment, compile all
credited transports, and run the four required mutation classes. Until then this is a blocker, not
completion of the statement node or any downstream node. `statement_elaborated`, `audit_complete`,
and `theorem_complete` remain false; the assigned phase is not genuinely self-tested, so
`.stage1-worker-selftest.json` is intentionally absent.
