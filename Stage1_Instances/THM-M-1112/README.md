# THM-M-1112 rev-5.6 intake

This directory is the fail-closed `planned` intake for the repository label "random graph" and its
description "Erdos-Renyi random graph model". That description names a family of probability
models, not a unique theorem. In particular, it does not choose between the uniform fixed-edge
model `G(n, m)` and the independent-edge model `G(n, p)`, nor does it state a mathematical
conclusion about either model.

The intake therefore freezes the ambiguity rather than silently substituting a convenient random
graph theorem. The statement phase must select an inspected primary-source result, fix all finite
graph and probability conventions, and then elaborate an exact Lean proposition. The provisional
root vector is `[H3, M4, R4]`; no source-fidelity, statement, proof, audit-completion, or
theorem-completion credit is claimed.

The scope map records the model choices and boundary cases, the source crosswalk separates
repository metadata from candidate primary sources, and the open task DAG preserves every later
rev-5.6 phase. Intake checks and their exact results are recorded in `validation.md`.
