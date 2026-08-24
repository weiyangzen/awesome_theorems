# Build validation

The generation-level command is the pinned task-local semantic preflight:

```text
check_stage5_theorem_item.py --claim-card claim.json --work-root work --no-lean
```

It is run with network denied and without Lean, Lake, or Elan.  The canonical
Master subsequently replays Statement.lean, Proof.lean, and Audit.lean from
source at trust zero.  The current receipt records the command identity,
source and artifact digests, mutation outcomes, and the requirement for that
independent replay.
