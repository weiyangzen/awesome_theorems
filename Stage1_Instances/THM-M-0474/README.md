# THM-M-0474 rev-5.6 statement

This is the `planned` dossier for Fermat's little theorem. The repository catalog says only
`a^(p-1) congruent to 1 (mod p)`. Taken without hypotheses, that sentence is false: setting
`a = p` makes the left side congruent to zero. Intake therefore records the conventional
conditional interpretation, with `p` prime and natural `a` coprime to `p`, as the canonical local
target. `Statement.lean` now freezes and elaborates that target. This formal selection does not
silently turn the incomplete catalog wording into an accepted primary-source statement.

## Statement artifacts

- `instance.json` is the structured planned instance and assurance boundary.
- `scope-map.md` fixes the selected natural-number reading, semantic prerequisites, variants, and
  exclusions.
- `source-statement-crosswalk.md` maps the catalog wording to its missing assumptions and to
  discovery-only declarations in pinned mathlib.
- `task-dag.json` leaves all six downstream rev-5.6 phases open.
- `IntakeProbe.lean` checks that the relevant pinned APIs elaborate and kernel-checks the
  coprimality/nondivisibility bridge plus the `a = p` counterexample to the unconditional reading.
- `Statement.lean` and `statement.json` preserve the canonical expression, its minimal imports,
  environment fingerprint, one checked premise transport, and four structural mutations.
- `check_statement.py`, `statement-validation.md`, and `statement-receipt.json` record the bounded
  self-test and its limits. `validation.md` and `intake-receipt.json` remain historical intake
  evidence.

## Status boundary

The root vector remains `[H1, M3, R4]`: the exact intake-selected target, expression fingerprint,
minimal imports, checked nondivisibility transport, and four required mutations are self-tested,
but no primary edition/theorem/page/errata review is accepted. The proof-bearing mathlib module is
not imported by the statement artifact, and formal-candidate provenance, proof, trust, composition,
and readable reconstruction remain later work. There is no accepted proof state, audit completion,
or theorem completion; statement acceptance remains with the integration lane.
