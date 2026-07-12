# THM-M-1398 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label `刚性方程`
("stiff equations"). The complete source gloss is `刚性问题的数值解法` ("numerical solution of
stiff problems"), with a collective attribution and the period "twentieth century". It supplies
no bibliography, stiffness definition, numerical method, theorem-grade proposition, hypotheses,
or conclusion. The metadata label `已验证` is untrusted and gives no source or proof credit.

The wording can refer to a scalar or system ODE, a linear test equation or a nonlinear initial
value problem, and many inequivalent method families. It does not select implicit Euler,
Runge-Kutta, a multistep or backward differentiation method, or a particular exact-arithmetic
algorithm. Nor does it say whether the desired result is consistency, convergence, an error bound,
absolute stability, A-stability, L-stability, or another property. Selecting any familiar result
would substitute mathematics absent from the source.

This intake freezes that ambiguity rather than inventing a canonical proposition. Its provisional
root vector is `[H5, M4, R4]`: `H5` says this repository target is not yet a stable truth-valued
claim, not that correctly stated stiff-equation theorems are false. The pinned Lean probe confirms
only that generic ODE and error-bound APIs elaborate; they neither define stiffness nor prove a
numerical method correct for this target.

The lifecycle remains `planned`. All downstream tasks are open, and no exact statement, accepted
execution state, audit completion, theorem completion, or master acceptance is claimed.
