# THM-M-1034 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the construction of the Ito stochastic
integral. It treats the legacy module as discovery material only and assigns it no proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Human root | Construct the Ito integral of square-integrable predictable integrands against Brownian motion by completing elementary adapted step processes in `L2` | The exact source edition and assumptions still require independent source review |
| Elementary layer | finite sums `sum H_i * (W(t_(i+1))-W(t_i))` with each coefficient measurable at the left endpoint | Time index, completed filtration, and almost-everywhere quotient choices are not yet frozen |
| Extension layer | Ito isometry, density/Cauchy extension, approximation independence, and uniqueness | These are obligations, not hypotheses that may be placed in a data structure to trivialize construction |
| Result layer | a linear `L2`-continuous integral, agreeing with elementary sums and satisfying the isometry | Terminal-time versus process-valued formulations require a checked transport |
| Lean substrate | probability space, filtration, Brownian motion, predictable/adapted processes, Bochner or `L2` integration | Exact imports, declaration type, and environment fingerprint belong to the statement phase |
| Exclusions | Stratonovich integration, general semimartingale integration, local integrands, and stochastic differential equations | Potential later generalizations; not part of this root |

The legacy `S1_M_227.lean` finite discrete sum is useful substrate, but its `StatementShape` assumes
the limit, isometry, and approximation facts inside its input data. It is therefore not accepted as
the construction theorem and is not the canonical target frozen here.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The first failed theorem gate is
the exact Lean statement gate: no elaborated expression hash, environment fingerprint, checked
encoding transports, or mutation tests exist. No theorem completion is claimed.

## Validation

The commands in `validation.md` validate manifest membership, repository consistency, JSON syntax,
and dossier-local hygiene on base revision `dbd29db42090d2fce49f69d84d4631769ef7e9c3` only.
