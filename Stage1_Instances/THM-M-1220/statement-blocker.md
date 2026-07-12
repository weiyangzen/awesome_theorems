# Exact-statement gate: blocked

Item: `S56-M-1220-STATEMENT`  
Theorem: `THM-M-1220`  
Base revision: `bf8f1a403fb8c22395ec64f92f93fed974f23c83`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. Its
entire mathematical claim is "well-posedness theory of NLW". This names a research area and a
family of results rather than a proposition. The intake correctly leaves all of the following
choices unresolved:

- the displayed nonlinear wave equation, sign convention, and nonlinearity;
- the spatial domain, dimension, scalar field, boundary conditions, and time interval;
- the initial-data and solution spaces and their regularity;
- the classical, strong, mild, weak, or distributional solution concept;
- local, global, maximal-lifespan, or small-data scope;
- the exact existence, uniqueness class, continuous-dependence topology, persistence, and
  blow-up-alternative conclusions;
- focusing or defocusing sign, scaling regime, size restrictions, and endpoint cases.

These alternatives change the domains, ordered binders, hypotheses, and conclusion. Selecting a
semilinear, cubic, energy-critical, defocusing, or abstract evolution theorem would therefore
substitute a narrower claim, not formalize the assigned source statement. The neighboring Segal,
Ginibre-Velo, Shatah-Struwe, and Tao NLW entries confirm that such named specializations are
separate repository targets and cannot be borrowed to resolve this generic entry.

The repository supplies no primary source, edition, theorem/page, exact wording, definitions, or
errata record for this target. The metadata value `已验证` is untrusted under rev-5.6 and supplies
neither human-statement identity nor kernel evidence. Consequently the gate fails before a
canonical expression, minimal import set, expression fingerprint, checked alternate transports,
or meaningful removed-hypothesis, changed-domain, changed-binder-scope, and boundary mutations can
be established. No `Statement.lean`, proxy predicate, axiom, or broadened theorem is introduced.

## Repository and Lean boundary

A scoped repository search found NLW-related legacy modules for distinct targets, including the
Klainerman and Grillakis entries, but no target-specific module or declaration for `THM-M-1220`.
Those modules choose additional equations and hypotheses and are discovery evidence only. A
search of the pinned mathlib source for the phrases "nonlinear wave" and "wave equation" found no
candidate source file. Negative searches do not constitute the later anchor audit and do not prove
that no external formalization exists.

Because there is no canonical target, running Lean on an invented statement would test only that
substitute. The narrow real Lean validation for this blocked phase is therefore limited to
fingerprinting the already pinned executable and dependency state; no `.lake` mutation was
performed.

## Required unblock

An accountable source reviewer must select and pin a primary theorem and record its edition,
theorem/page, exact equation, every assumption and conclusion, definitions, conventions, and
errata. The review must freeze all choices listed above and approve a source-to-binder crosswalk.
A later statement worker can then encode that exact claim, minimize its pinned imports, serialize
the elaborated expression and environment, and run the four required mutation classes.

## Narrow validation evidence

Commands ran from this worker clone on 2026-07-12 (Asia/Shanghai). Commands involving Lake ran
from `Formalizations/Lean` and reused the existing pinned artifacts. No update, build, clone, or
fetch command was used.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1220` | 0 | rank 411; planned; legacy artifacts unaccepted; theorem incomplete |
| `rg -n -i 'nonlinear wave|NLW|wave equation|waveEquation' Formalizations/Lean --glob '!**/.lake/**'` | 0 | matches only distinct legacy targets; no `THM-M-1220` module or declaration |
| `find Formalizations/Lean/.lake/packages/mathlib/Mathlib -type f -name '*.lean' -print0 \| xargs -0 rg -l -i 'nonlinear wave\|wave equation'` | 0 | no output; no phrase-level candidate in the pinned mathlib source |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C .lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum lean-toolchain lake-manifest.json` | 0 | hashes `651c8acc...b1d2` and `321626c8...2d81` |

First failed gate: exact canonical human-claim identity. Known failures are exact Lean elaboration,
minimal-import determination, expression serialization, checked transports, and all four mutation
classes. The assigned phase is not self-tested to completion, statement acceptance and theorem
completion remain false, and no `.stage1-worker-selftest.json` is emitted.
