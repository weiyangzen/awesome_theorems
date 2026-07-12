# THM-M-0474 rev-5.6 anchor audit

This is the `planned` dossier for Fermat's little theorem. The repository catalog says only
`a^(p-1) congruent to 1 (mod p)`. Taken without hypotheses, that sentence is false: setting
`a = p` makes the left side congruent to zero. Intake therefore records the conventional
conditional interpretation, with `p` prime and natural `a` coprime to `p`, as the canonical local
target. `Statement.lean` freezes and elaborates that target. This formal selection does not silently
turn the incomplete catalog wording into an accepted primary-source statement.

## Current artifacts

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
- `AnchorAudit.lean` independently restates the frozen target and checks an exact wrapper over
  pinned `Nat.ModEq.pow_card_sub_one_eq_one`, including transitive sorry and axiom probes.
- `anchor-audit.json` classifies the immutable mathlib candidate, adjacent encodings, pinned
  external consumer, and bounded public-source inventory. `check_anchor_audit.py`,
  `anchor-audit-validation.md`, and `anchor-audit-receipt.json` bind the provisional node self-test.

## Status boundary

The root vector remains `[H1, M3, R4]`: no primary edition/theorem/page/errata review is accepted,
and no proof-phase wrapper or accepted proof state exists. The anchor phase has self-tested an exact
pinned mathlib candidate, classified conservatively as
`M0-W_candidate_pending_downstream_acceptance`; it has not promoted the authoritative root. Frozen
obligations, complete provenance/trust and TCB closure, composition, readable reconstruction,
hermetic validation, independent verification, and release remain later work. There is no full
audit completion or theorem completion; anchor-audit acceptance remains with the integration lane.
