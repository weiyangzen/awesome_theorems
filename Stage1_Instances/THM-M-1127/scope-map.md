# Scope map

## Preserved source scope

- Subject: the one-dimensional wave equation.
- Result family: a d'Alembert representation described as a general solution.
- Attribution and date: Jean le Rond d'Alembert, 1746, according to repository metadata.

This is all the repository source fixes. The usual formula is a candidate family,
not yet the canonical theorem.

## Decisions required before statement freeze

The statement phase must identify a primary source and freeze: the spatial and
time domains; scalar field; wave speed and whether it is positive; normalization
of `u_tt = c^2 u_xx`; classical, weak, or distributional solution notion;
differentiability of `u`, `F`, and `G`; initial displacement and velocity data;
the integral term and base point for the initial-value form; and whether the
claim proves construction only, necessity only, uniqueness, or both directions.
It must explicitly treat `c = 0`, negative speed parameters, zero data, endpoints,
and whole-line versus bounded/periodic domains.

## Explicit exclusions

- Silently selecting only the forward calculation for `F (x-c*t)+G (x+c*t)`.
- Substituting the initial-value formula for a two-way general-solution theorem,
  or conversely.
- A discrete, bounded-domain, higher-dimensional, or weak-solution wave theorem.
- Treating the inventory label `已验证` as source or kernel evidence.
- Treating `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_142.lean` as a legacy
  artifact for this theorem: that file declares THM-M-1314 (Penrose inequality),
  so the matching intake score is not a theorem-ID crosswalk.
