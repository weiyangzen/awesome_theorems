# Build validation

Worker preflight is semantic/evidence-only and uses the mandated
`check_stage5_theorem_item.py --no-lean` command.  Lean, Lake, and Elan are not
invoked in this task-local validation.  The canonical Master owns the later
trust-zero cold replay after harvest.

Required mutation gates are recorded as passing candidates: source/import
substitution rejection, local-shadow rejection, placeholder scan, cold source
replay requirement, and strict dominance over the incomplete THM-M-0387
H1/M2/R0 fixture.
