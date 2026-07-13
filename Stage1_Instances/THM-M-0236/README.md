# THM-M-0236 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `单值性定理` (the monodromy
theorem). The repository supplies only the gloss `全纯函数沿曲线的解析延拓` ("analytic
continuation of holomorphic functions along paths"), a nineteenth-century date, and the
attribution "many mathematicians." Its `已验证` label is untrusted metadata. The gloss names a
topic but does not state a truth-valued proposition.

A stable secondary formulation distinguishes two standard branches. The homotopy form says that
continuations of one analytic element along endpoint-fixed homotopic paths have the same terminal
element. The simply-connected form says that an element continuable along every path in a
simply-connected domain determines a single-valued branch. The catalog chooses neither branch and
omits the domain, starting element, path class, continuation predicate, endpoint, hypotheses, and
conclusion. No canonical human or Lean statement is therefore frozen.

Pinned mathlib contains the checked abstract theorem
`IsLocalHomeomorph.monodromy_theorem`. It proves endpoint invariance for a homotopy family of lifts
through a separated local homeomorphism. Its documentation explains the intended analytic-germ
application, but the declaration does not build the etale space of analytic germs or prove the
analytic hypotheses needed for that application. Until exact source identity and these bridges
are audited, this is a strong formal candidate, not target proof credit.

The provisional vector is `[H1, M4, R4]`: the classical family is recognizable and published
source leads exist, but no definition-complete source statement or independent review is accepted;
no usable exact target artifact is credited; and no source-faithful proof reconstruction exists.
`IntakeProbe.lean` checks only three adjacent pinned declarations and the candidate's axiom report.
All six dependent phases remain open. No canonical proposition, H0, M0, R0, accepted state, audit
completion, theorem completion, or master acceptance is claimed.
