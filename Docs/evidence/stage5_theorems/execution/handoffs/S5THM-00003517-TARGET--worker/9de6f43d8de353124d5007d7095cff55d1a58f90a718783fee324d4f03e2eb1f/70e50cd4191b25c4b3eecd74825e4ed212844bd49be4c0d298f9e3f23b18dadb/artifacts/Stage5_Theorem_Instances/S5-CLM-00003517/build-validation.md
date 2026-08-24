# Build validation

Required worker command:

`python3 _baseline/check_stage5_theorem_item.py --claim-card ../claim.json --work-root . --no-lean`

The receipt records the exact argv digest, stdout digest, stderr digest, start
and finish timestamps, and exit code.  This worker generation does not run
Lean, Lake, Elan, a network operation, or a canonical-tree command.

The Master gate is intentionally stronger: integrate the exact patch, perform
a clean offline source build of all three Lean artifacts with the pinned
toolchain at trust zero, recompute semantic identities and dependency bodies,
run substitution/deletion/tamper mutations, and only then issue a canonical
acceptance receipt.  A passing worker preflight alone cannot set
`master_accepted` or advance the Blueprint checkbox.
