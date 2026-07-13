# THM-M-1440 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label `牛顿迭代法`
(Newton iteration). The entire catalog gloss is `方程求根的二次收敛方法` ("a quadratically
convergent method for finding roots of equations"), attributed to Isaac Newton in 1669. A method
name and a convergence slogan do not determine a proposition with ordered binders, hypotheses,
and a conclusion. The attribution, date, and `已验证` label are untrusted catalog metadata, not
source or proof evidence.

The named family is quadratic convergence of Newton root iteration, but materially different
theorems fit that phrase, including local and global claims. The catalog does not select scalar
real, scalar complex, or Banach-space Newton; a function class and derivative notion; a simple-root
and regularity premise; an initial neighborhood; a well-definedness condition for every division;
a convergence predicate; or one of the inequivalent definitions of quadratic convergence.
Supplying any one from memory would invent proposition-changing mathematics.

This intake freezes that ambiguity. The provisional root vector is `[H5, M4, R4]`. `H5` classifies
the catalog wording as not yet a stable proposition; it does not refute the standard Newton
convergence theorems. `M4` records that no source-identical formal target is usable, while `R4`
records that no proof reconstruction can attach to an unidentified root. Ordinary statement and
proof execution remain blocked until an approved source correction selects one exact theorem.

Pinned mathlib's `Mathlib.Dynamics.Newton` defines a polynomial Newton map and proves root/fixed-
point and nilpotent-ring facts. `IntakeProbe.lean` authenticates those interfaces, but the module
does not state the catalog's analytic quadratic-convergence claim. All six dependent phases remain
open in `task-dag.json`. No H0, M0, R0, accepted proof state, audit completion, theorem completion,
accepted receipt, or master acceptance is claimed.
