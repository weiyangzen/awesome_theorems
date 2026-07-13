# THM-M-1481 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
`模拟退火` (simulated annealing). The catalog supplies only the gloss
`全局优化的随机方法` ("a randomized method for global optimization"), attributes it to
Scott Kirkpatrick in 1983, and labels it `已验证`. A method family and purpose do not form a
truth-valued proposition with ordered binders, hypotheses, and a conclusion. The verified label is
untrusted metadata and supplies neither human-source nor kernel-proof credit.

The likely historical source family is Kirkpatrick, Gelatt, and Vecchi's 1983 Science article
*Optimization by Simulated Annealing*. Bibliographic metadata and an accessible course-hosted
JSTOR scan confirm the article, authors, date, pages, DOI, and its statistical-mechanics analogy for
multivariate or combinatorial optimization. The repository neither cites this article nor includes
Gelatt and Vecchi. Pages 671-673 describe a heuristic, Metropolis acceptance, and slow staged
cooling; page 679 describes schedules chosen by trial and error and results suggested by numerical
studies. The article does not state one exact general global-optimization theorem matching the
catalog gloss.

A later theorem family, exemplified by Hajek's 1988 *Cooling Schedules for Optimal Annealing*,
gives necessary and sufficient convergence conditions in a specific finite-state cooling-schedule
setting. It is a useful statement-selection lead, but silently choosing it would replace the
catalog's 1983 method label with a later, narrower theorem.

The catalog fixes none of the state space, objective, proposal graph, transition probabilities,
acceptance rule, temperature schedule, initial distribution, convergence mode, global-minimum set,
or boundary cases. Pinned mathlib provides generic Markov-kernel, invariance, reversibility,
irreducibility, and finite-minimum interfaces. `IntakeProbe.lean` authenticates only those adjacent
APIs; it neither defines simulated annealing nor proves global optimization or convergence.

The provisional vector is `[H5, M4, R4]`. `H5` records that the received method gloss is not yet
a stable proposition; it does not refute source-correct simulated-annealing theorems. `M4` records
that no usable source-identical formal artifact has been identified for the unfrozen root. `R4`
records that no source-faithful proof reconstruction can attach to it. All six downstream phases
remain open. No exact statement, accepted proof state, audit completion, theorem completion,
accepted receipt, or master acceptance is claimed.
