# THM-M-1100 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "Markov chain
Monte Carlo" (MCMC). MCMC names a family of sampling methods, not a proposition with a truth value.
The repository supplies only "MCMC methods", Nicholas Metropolis, and 1953; it does not specify an
algorithm, target distribution, transition kernel, convergence mode, estimator, or conclusion.

The historical 1953 paper gives a concrete discovery boundary: a symmetric-proposal acceptance
algorithm for canonical-ensemble calculations. It does not by itself select a generic theorem
called "MCMC". The separate `THM-M-1101` Metropolis-Hastings target also prevents silently replacing
this target with the later general algorithm. One exact mathematical result must therefore be
selected and source-reviewed before the canonical human statement or Lean target can be frozen.

The provisional root vector is `[H5, M4, R4]`: the literal label is not yet a stable proposition,
no usable exact formal artifact has been located, and no proof reconstruction exists. The metadata
label `已验证` receives no source or machine-proof credit. No exact theorem, formal candidate,
audit completion, or theorem completion is claimed. The scope map, crosswalk, and open task DAG
record the correction boundary and downstream work; intake checks are recorded in `validation.md`.
