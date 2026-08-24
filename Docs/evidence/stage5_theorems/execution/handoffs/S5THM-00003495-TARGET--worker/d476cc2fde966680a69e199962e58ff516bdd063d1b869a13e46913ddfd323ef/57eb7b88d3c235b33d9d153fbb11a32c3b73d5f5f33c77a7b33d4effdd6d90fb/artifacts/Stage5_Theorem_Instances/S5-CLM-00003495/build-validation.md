# Build validation — S5-CLM-00003495

Worker gate: `/usr/bin/python3 _baseline/check_stage5_theorem_item.py --claim-card ../claim.json --work-root . --no-lean`.

The worker is prohibited from invoking Lean, Lake, or Elan.  The command above
checks strict JSON, authority seals, exact ownership, source binding,
placeholder/shadow rejection, M0/R0 evidence, and the provisional release
conjunction.  Canonical Master validation must additionally compile all three
Lean surfaces from source at trust zero, replay mutations, and recompute the
semantic environment.
