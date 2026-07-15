# THM-M-0128 statement recheck: blocked

Item: `S56-M-0128-STATEMENT`

Base revision: `aef94f39853f9222e48f83b2358a6822aafd3c50` (tree
`8c42e198fdbcc36b0f5cc0f865e0961715a35c17`). Rechecked on 2026-07-15
(`Asia/Shanghai`) in worker slot 75.

## Decision

The exact-statement gate remains blocked. The repository's upstream record gives
only the name "Shimura reciprocity law", Goro Shimura attribution, the year 1971,
and the gloss "class field theory of CM fields". It supplies no exact theorem,
page, incorporated definitions, hypotheses, conclusion, convention crosswalk,
errata disposition, or independent review.

The provisional intake selects the CM-special-point family as a human scope: for
a CM datum and reflex field, an Artin/Galois translate of a CM special point
agrees with the translate induced by the reflex norm. That prose is not an exact
formula. The intake and crosswalk explicitly leave unresolved:

- CM field versus CM algebra and the representations of the CM type, reflex
  field, and reflex norm;
- the idele versus idele-class domain and quotient descent;
- arithmetic versus geometric Artin reciprocity, including the possible inverse;
- the canonical model, component, level, special point, and left/right actions;
- equality of points versus equality of orbits or double cosets.

These choices change binders, hypotheses, domains, variance, and sometimes the
direction of the equation. Freezing the schematic equation
`Artin_E(s) * x = reflexNorm_Phi(s) * x` would invent conventions not authorized
by a source and might state the inverse or a differently quotiented theorem.
Encoding the missing objects as arbitrary types/functions or proposition-valued
fields would instead reproduce the rejected legacy placeholder boundary. In
particular, the legacy `CMReciprocityInput.hasReciprocityLaw` assumes the desired
compatibility rather than expressing an independently defined target.

No authoritative target input has resolved these gaps since the integrated
blocker. The manifest, source records, legacy Stage1 blueprint, execution skill,
intake dossier, legacy Lean module, toolchain, and dependency lock are unchanged.
The rev-5.6 blueprint and execution DAG changed for unrelated integrations only;
their `THM-M-0128` projections are unchanged.

Consequently there is no honest canonical Lean expression whose imports can be
minimized or whose elaborated expression and environment can be fingerprinted.
Checked alternate transports and the removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations are undefined, not passed. The
first failed gate remains
`exact_source_statement_identity_and_convention_selection`.

The predecessor `S56-M-0128-INTAKE` is also provisional `[_]`, without a master
acceptance receipt. Lifecycle stays `planned`, the root vector remains
`H2 / M4 / R4`, and this statement node stays `[ ]`. This recheck claims no
statement receipt, proof, debt change, audit completion, or theorem completion.

## Pinned Lean Boundary

`StatementProbe.lean` was replayed using the existing pinned Lake artifacts. Its
two direct imports expose `NumberField.IsCMField` and
`NumberField.AdeleRing`. They are adjacent object-model anchors only. A bounded
search of the pinned number-theory, algebraic-geometry, and field-theory sources
found no concrete CM-type, reflex-field/reflex-norm, idele-class, Shimura
datum/variety, special-point, or Artin-reciprocity declaration. The probe imports
are minimal only for that substrate probe, not for the absent canonical target.

The legacy module
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_046.lean` also elaborated. Its
own documentation calls its CM/Shimura/reflex/reciprocity fields placeholders,
and its `StatementShape` merely consumes those proposition fields. Successful
replay therefore provides discovery-boundary evidence, not exact-target credit.

The replay used Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake
`5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided
`Formalizations/Lean/.lake` symlink was reused read-only. No update, build,
clone, fetch, or other dependency mutation was performed.

## Validation Record

Commands ran from this worker clone unless a working directory is stated.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0128` | 0 | rank 46; planned; legacy slot `S1-M-046`; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | pre-edit status contained only the automation-provided untracked `.lake` symlink; base revision and tree match this record |
| scoped manifest, standard, skill, source, intake, legacy-module, probe, and prior-blocker inspection | 0 | exact source identity, proposition, and conventions remain unresolved; the integrated blocker remains substantively correct |
| `git diff 9b87a8f31a5e6a549ab5449871f0b311cab9a6ec..HEAD` over authoritative target inputs and normalized target projections | 0 | no target-source, intake, legacy Lean, toolchain, or dependency-lock change; `THM-M-0128` blueprint/DAG projections are unchanged |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0128/StatementProbe.lean` | 0 | `NumberField.IsCMField` and `NumberField.AdeleRing` elaborated; no canonical target or proof body was declared |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean AwesomeTheorems/Stage1/S1_M_046.lean` | 0 | legacy placeholder-bearing discovery module elaborated with empty output; no exact-target credit |
| from `Formalizations/Lean`: `lake env lean --version`; `lake --version` | 0 | Lean and Lake versions match the pinned environment above |
| mathlib package `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | package worktree clean at the pinned revision and tree above |
| bounded pinned-mathlib exact-topic search | 1, expected no match | no concrete CM-type/reflex/Shimura/special-point/Artin-reciprocity match in the searched source families; not a completed anchor audit |
| prohibited-construct scan over the owned probe and legacy Lean module | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, `unsafe`, `implemented_by`, or `native_decide` occurrence |
| `python3 -m json.tool` on the recheck JSON | 0 | structured current-HEAD blocker record parsed |
| scoped blocker invariant assertions | 0 | item/base identity, blocked state, unchanged vector, null canonical fields, four undefined mutations, current input hashes, two-file scope, and self-test absence agree |
| scoped tracked and per-new-file `git diff --check` | 0 | no whitespace diagnostics; no-index exit 1 was only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test is absent because the exact-statement gate failed |

## Retry Condition And Boundary

Retry only after dependency acceptance and accountable reviewers preserve and
approve an immutable primary or authoritative theorem passage, including its
incorporated definitions, edition, theorem/page locator, corrections, errata,
translation, assumptions, and reciprocity/action conventions. They must choose
the exact CM datum, reflex construction, idelic domain, Artin normalization,
canonical-model/level data, action variance, conclusion equality, ordered
binders, and boundary cases. The required concrete CM-type, reflex-norm,
reciprocity, and special-point Lean object model must then be implemented or
imported at immutable pins. A fresh statement worker can encode only that
approved claim, prove import minimality, fingerprint its elaborated expression
and environment, compile every credited transport, and execute all four mutation
classes.

This is fresh current-HEAD target-scoped blocker evidence only. Because the
positive statement deliverable did not pass, `.stage1-worker-selftest.json` is
intentionally absent and no worker `[_]` or master acceptance is requested.
