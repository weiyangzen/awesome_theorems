# S5-CLM-00003579 — Erdős problem 1028

This directory is the provisional worker handoff for the single target
`S5THM-00003579-TARGET`.  It binds the frozen provider declaration
`Erdos1028.erdos_1028` and the Stage6 alias `S6-CLM-00006420` /
`S6-VAR-00005308`.

The package contains the intake record, source/target crosswalk, content-
addressed anchors, typed proof-unit DAG, machine closure, readable
reconstruction, and release receipts.  The executable Lean surfaces use
`import Mathlib`; the exact numeric provider module and qualified declaration
are retained in provenance comments as required by the frozen execution
specification.

Worker validation is semantic/evidence-only (`--no-lean`).  The provisional
release is not Master acceptance: canonical integration must independently
recompute elaboration, dependencies, trust-zero M0 closure, mutation checks,
and cold offline replay.
