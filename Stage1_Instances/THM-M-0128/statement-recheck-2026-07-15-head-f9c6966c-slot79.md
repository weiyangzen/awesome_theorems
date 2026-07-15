# THM-M-0128 statement recheck: blocked

Item: `S56-M-0128-STATEMENT`

Base revision: `f9c6966c4a9f779a85442d309d9a4e6d4bbfe36b` (tree
`153efbfdf2465303d2ee3999dfbd92ee883d6220`). Rechecked on 2026-07-15
(`Asia/Shanghai`) in worker slot 79.

## Decision

The exact-statement gate remains blocked. The repository's three catalog
entries provide only the name "Shimura reciprocity law", a Goro Shimura
attribution, the year 1971, and the gloss "class field theory of CM fields".
They do not identify an exact edition/theorem/page, incorporated definitions,
hypotheses, conclusion, convention crosswalk, errata disposition, translation,
or independent review.

The provisional intake chooses a CM-special-point family only as prose scope:
for a CM datum and reflex field, an Artin/Galois translate of a CM special point
agrees with the translate induced by the reflex norm. It explicitly leaves
unresolved:

- CM field versus CM algebra and the CM-type/reflex construction;
- the reflex norm's variance and codomain;
- the idele versus idele-class domain and quotient descent;
- arithmetic versus geometric Artin reciprocity, including inversion;
- the canonical model, component, level, special point, and left/right actions;
- equality of points versus equality of orbits or double cosets.

These choices change binders, hypotheses, domains, variance, quotients, and
even the direction of the equation. Freezing a schematic Artin/reflex equation
would invent conventions not authorized by the source. Replacing the missing
objects with arbitrary carriers, functions, or proposition-valued fields would
reproduce the rejected legacy placeholder boundary; in particular,
`CMReciprocityInput.hasReciprocityLaw` assumes the desired compatibility.

The preceding recheck is integrated in this base revision. No authoritative
target input has resolved its blocker. The manifest, source records, intake
dossier, legacy Lean module, toolchain, dependency lock, guidelines, and
execution skill are unchanged since the preceding recheck's base. Intervening
blueprint/DAG changes concern unrelated integrations; their exact
`THM-M-0128` projections compare equal.

Consequently there is no honest canonical Lean expression whose imports can be
minimized or whose expression and environment can be fingerprinted. Checked
alternate transports and the removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations are undefined, not passed.
The first failed gate remains
`exact_source_statement_identity_and_convention_selection`.

The predecessor `S56-M-0128-INTAKE` is provisional `[_]`, without an accepted
receipt. Lifecycle stays `planned`; the inherited provisional intake vector
remains `H2 / M4 / R4` without statement-phase reclassification. Intake/master
review should reconcile `H2` against the rev-5.6 debt definitions when an exact
source statement is selected. The statement node stays `[ ]`. This recheck
claims no statement receipt, proof, debt change, audit completion, theorem
completion, or master acceptance.

## Pinned Lean Boundary

`StatementProbe.lean` was replayed with the existing pinned Lake artifacts. Its
two direct imports expose `NumberField.IsCMField` and
`NumberField.AdeleRing`. They are object-model anchors only. A bounded search of
the pinned number-theory, algebraic-geometry, and field-theory sources found no
concrete CM-type, reflex-field/reflex-norm, idele-class, Shimura datum/variety,
special-point, or Artin-reciprocity declaration. These are only the probe's
direct imports and provide no canonical-target import-minimality evidence.

The legacy module `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_046.lean`
also elaborated. Its documentation identifies its CM/Shimura/reflex/reciprocity
fields as placeholders, so its `StatementShape` receives no exact-target credit.

The replay used Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake
`5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided
`Formalizations/Lean/.lake` symlink was reused read-only. No update, build,
clone, fetch, or dependency mutation was performed.

## Validation Record

Commands ran from this worker clone unless a working directory is stated.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0128` | 0 | rank 46; planned; legacy slot `S1-M-046`; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | pre-edit status contained only the automation-provided untracked `.lake` symlink; base revision and tree match this record |
| read-only file inspection of the manifest, standard, skill, guidelines, source records, intake dossier, legacy module, probe, and prior recheck (not an executable command) | n/a | exact source identity, proposition, and conventions remain unresolved; the integrated blocker remains substantively correct |
| exact `git diff --quiet` argv over the 17 static target-input paths; per-revision `git show` plus `jq`/`awk` SHA-256 projection commands; two `git cat-file -e` checks (full records are in the companion JSON) | 0 for every command | static target sources, intake, legacy Lean, toolchain, and dependency lock are unchanged; exact `THM-M-0128` manifest/blueprint/DAG projections compare equal; the preceding recheck pair is integrated at HEAD |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0128/StatementProbe.lean` | 0 | `NumberField.IsCMField` and `NumberField.AdeleRing` elaborated; no canonical target or proof body was declared |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean AwesomeTheorems/Stage1/S1_M_046.lean` | 0 | legacy placeholder-bearing discovery module elaborated with empty output; no exact-target credit |
| from `Formalizations/Lean`: `lake env lean --version`; `lake --version` | 0 | Lean and Lake versions match the pinned environment above |
| from `Formalizations/Lean`: `git -C .lake/packages/mathlib status --short --untracked-files=all`; `git -C .lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | package worktree clean at the pinned revision and tree above |
| from `Formalizations/Lean`: bounded declaration-position search for CM-type, reflex-field/reflex-norm, idele-class, Shimura datum/variety, special-point, and Artin-reciprocity terms in pinned `NumberTheory`, `AlgebraicGeometry`, and `FieldTheory` sources | 1, expected no match | zero output; not a completed anchor audit |
| from `Formalizations/Lean`: prohibited-construct scan over the owned probe and legacy Lean module | 1, expected no match | zero output; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, `unsafe`, `implemented_by`, or `native_decide` token |
| `python3 -m json.tool Stage1_Instances/THM-M-0128/statement-recheck-2026-07-15-head-f9c6966c-slot79.json` | 0 | structured current-HEAD blocker record parsed as valid JSON; individual base, projection, Lean, whitespace, and self-test checks are recorded separately |
| `git diff --check -- Stage1_Instances/THM-M-0128`; `git diff --no-index --check /dev/null Stage1_Instances/THM-M-0128/statement-recheck-2026-07-15-head-f9c6966c-slot79.json`; same command for the Markdown file | 0 / 1 expected / 1 expected | no whitespace diagnostics; each no-index exit 1 is only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test is absent because the exact-statement deliverable did not pass |

## Retry Condition And Boundary

Retry only after the intake is master-accepted and accountable reviewers
preserve and approve one immutable primary or authoritative theorem passage with
its incorporated definitions, edition/theorem/page locator, corrections,
errata, exact translation, hypotheses, and all reciprocity/action conventions.
They must fix the CM datum, reflex construction, idelic domain, Artin
normalization, canonical-model/level data, action variance, conclusion equality,
ordered binders, and boundary cases. The corresponding concrete Lean object
model must then be implemented or imported at immutable pins. A fresh statement
worker can encode only that approved claim, minimize imports, fingerprint the
elaborated expression and environment, compile every credited transport, and
execute all four mutation classes.

This is fresh current-HEAD target-scoped blocker evidence only. Because the
positive statement deliverable did not pass, `.stage1-worker-selftest.json` is
intentionally absent and no worker `[_]` or master acceptance is requested.
