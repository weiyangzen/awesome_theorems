# THM-M-0474 rev-5.6 intake

This is the `planned` dossier for Fermat's little theorem. The repository catalog says only
`a^(p-1) congruent to 1 (mod p)`. Taken without hypotheses, that sentence is false: setting
`a = p` makes the left side congruent to zero. Intake therefore records the conventional
conditional interpretation, with `p` prime and `a` coprime to `p`, as the candidate scope that the
statement phase must confirm against an exact source. It does not silently credit the incomplete
catalog wording as an exact theorem.

## Intake artifacts

- `instance.json` is the structured planned instance and assurance boundary.
- `scope-map.md` fixes the candidate mathematical reading, semantic prerequisites, variants, and
  exclusions without selecting a final natural-versus-integer encoding.
- `source-statement-crosswalk.md` maps the catalog wording to its missing assumptions and to
  discovery-only declarations in pinned mathlib.
- `task-dag.json` leaves all six downstream rev-5.6 phases open.
- `IntakeProbe.lean` checks that the relevant pinned APIs elaborate and kernel-checks the
  coprimality/nondivisibility bridge plus the `a = p` counterexample to the unconditional reading.
- `validation.md` and `intake-receipt.json` record the exact bounded worker checks and their limits.

## Status boundary

The proposed root vector is `[H1, M3, R4]`: the classical theorem is identifiable, but no primary
edition/theorem/page/errata review is accepted; an exact pinned Lean candidate is callable, but the
canonical statement, fingerprints, mutations, provenance, and trust gates belong to later phases;
and no readable proof reconstruction has been audited. There is no accepted proof state, audit
completion, or theorem completion.
