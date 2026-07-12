# THM-M-1386 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-1386`, the repository label
`Sturm分离定理` (Sturm separation theorem). The catalog attributes the result to Jacques Sturm in
1836 and gives only the gloss `线性无关解的零点交错` (zeros of linearly independent solutions
interlace). It supplies no citation, differential equation, definitions, hypotheses, conclusion,
or proof source. Its `已验证` field is untrusted metadata under rev-5.6.

The wording identifies a classical theorem family but not one binder-complete proposition. It does
not fix the self-adjoint or normal ODE form, coefficient regularity, interval and endpoint model,
solution semantics, real or complex scalar field, linear-independence witness, consecutive-zero
predicate, or whether interlacing means existence, uniqueness, both directions, or a globally
indexed alternation. Selecting these from memory would change rather than transcribe the target.

Paul R. Beesack's *On Sturm's Separation Theorem*, *Canadian Mathematical Bulletin* 15(4)
(1972), pp. 481-487, DOI `10.4153/CMB-1972-086-7`, was inspected as an authoritative source-family
lead. Page 481 states the classical compact-interval theorem for `(r y')' + s y = 0` with continuous
`r,s` and positive `r`; Theorem 1 then gives a materially broader open-interval result with explicit
nonsingular and singular endpoint cases. The catalog does not cite this article or select the
classical statement versus that extension, so neither is silently adopted as the canonical root.

An immutable Numdam record also locates Sturm's 1836 primary article and explicitly links a two-page
errata item. Both scans are image-only in this intake and their exact theorem and correction impact
remain untranscribed and unreviewed. They establish a serious primary-source lead, not H0 closure.

`instance.json` therefore freezes the provisional root vector `[H1, M4, R4]`. `H1` records a
credible source-family statement whose exact source identity and assumptions remain unaudited and
unapproved, not an H0 source crosswalk. `IntakeProbe.lean` elaborates only adjacent pinned calculus,
order, and linear-independence interfaces. These interfaces provide no statement or proof credit.
All six downstream tasks remain open in `task-dag.json`.

No canonical mathematical or Lean statement, H0, M0, R0, accepted proof state, audit completion,
theorem completion, or master acceptance is claimed.
