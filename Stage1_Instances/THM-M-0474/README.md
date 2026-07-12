# THM-M-0474 rev-5.6 dossier

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
- `obligation-registry.json` freezes 21 semantic obligations independently of candidate closure
  status. `typed-graphs.json` separates proof, refinement, provenance, evidence, trust,
  documentation, and workflow relations; `validation-specs.json` binds one structured recipe to
  every obligation.
- `ObligationTree.lean` checks the conditional exact child-to-root composition without installing
  the mathlib theorem. `build_obligation_artifacts.py`, `check_obligation_tree.py`,
  `obligation-tree.md`, `obligation-tree-validation.md`, and `obligation-tree-receipt.json` record
  the deterministic freeze, semantic expansion, and provisional self-test.

## Status boundary

The root vector remains `[H1, M3, R4]`: no primary edition/theorem/page/errata review is accepted,
and no proof-phase wrapper or accepted proof state exists. The exact pinned candidate remains
`M0-W_candidate_pending_proof_phase_and_master_acceptance`. The obligation phase has frozen and
self-tested the denominator, full visible terminal-source expansion, seven typed graphs, and a
conditional composition interface; it has not promoted the authoritative root. Complete
provenance/trust and TCB closure, proof installation, readable reconstruction, hermetic validation,
independent verification, and release remain later work. There is no full audit completion or
theorem completion; dependency-ordered acceptance remains with the integration lane.
