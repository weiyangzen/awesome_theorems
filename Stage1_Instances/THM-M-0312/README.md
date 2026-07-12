# THM-M-0312 rev-5.6 intake

This directory is the `planned` intake dossier for the theorem called the resonance theorem in the
repository and more commonly the Banach-Steinhaus theorem or Uniform Boundedness Principle. The
frozen root scope is the normed-space form: a pointwise bounded family of continuous semilinear maps
from a Banach space to a normed space has uniformly bounded operator norms.

Pinned mathlib contains the matching candidate declaration `banach_steinhaus` in
`Mathlib.Analysis.Normed.Operator.BanachSteinhaus`. The intake probe checks only that declaration's
public type and its nearby extended-nonnegative formulation. It does not accept exact statement
identity, source fidelity, proof-body provenance, axiom closure, or any machine proof state.

The root remains `[H1, M3, R3]`: the mathematical result is established in the literature but the
primary-source crosswalk is unaudited; a formal declaration candidate exists but has only been
probed; and no reviewed proof reconstruction exists. `audit_complete` and `theorem_complete` are
both false. Exact commands and results are recorded in `validation.md`.
