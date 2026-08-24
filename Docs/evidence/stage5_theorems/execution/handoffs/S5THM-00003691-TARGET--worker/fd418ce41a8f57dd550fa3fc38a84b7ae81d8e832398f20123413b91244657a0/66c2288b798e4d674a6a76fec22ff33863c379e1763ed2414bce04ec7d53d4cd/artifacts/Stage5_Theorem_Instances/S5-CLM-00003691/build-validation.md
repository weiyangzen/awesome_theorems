# Build validation — S5-CLM-00003691

Authorized worker validation is the task-local semantic/evidence preflight:

```text
/usr/bin/python3 _baseline/check_stage5_theorem_item.py \
  --claim-card ../claim.json --work-root . --no-lean
```

The actual command uses the absolute paths frozen in `claim.json`. Its stdout,
stderr, start/finish timestamps, argument digest, and exit status are recorded
in the worker result after the final sealed package passes.

Static package gates performed before that command:

- exactly eighteen required writable artifacts exist and are nonempty;
- all three Lean files actively import only `Mathlib` and include the exact
  numeric provider import and qualified declaration in provenance comments;
- no `sorry`, `admit`, `axiom`, `unsafe`, `opaque`, local definition,
  abbreviation, notation, syntax, macro, local instance, or namespace alias is
  present in the Lean declaration surface;
- all JSON files parse strictly and all sealed validator artifacts reproduce
  their canonical authority hash;
- the source file digest matches the frozen locator;
- semantic environment, machine closure, readability, and release identities
  agree and all H/M/R cut sets are empty.

No worker Lean/Lake/Elan execution is permitted or claimed. Cold offline
trust-zero compilation and full environment recomputation are Master gates.
