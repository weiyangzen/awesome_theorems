# THM-M-1437 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog label
`Feigenbaum普适性` (`Feigenbaum universality`). The repository attributes the item to Mitchell
Feigenbaum, dates it to 1975, and gives only the gloss `倍周期分岔的普适常数` (`the universal
constant of period-doubling bifurcations`). The catalog status `已验证` is explicitly untrusted
under rev-5.6.

That wording does not select a truth-valued proposition. It can refer to existence of the parameter
scaling constant delta, a limit formula defining it, its approximate value, universality over a
specified class of unimodal maps, spatial scaling by alpha, convergence to a renormalization fixed
point, or hyperbolicity and a unique unstable eigenvalue. These claims require different map
classes, normalizations, binders, hypotheses, and conclusions.

The two located Feigenbaum papers are discovery leads, not a source selection. The 1978 abstract
describes both alpha and delta laws and calls its treatment heuristic. The 1979 abstract formulates
a renormalization and spectral route but makes a key unique-eigenvalue assertion conjectural. The
catalog's 1975 date identifies neither paper nor an immutable earlier source.

This intake therefore freezes the ambiguity rather than substituting a remembered theorem. The
provisional root vector is `[H5, M4, R4]`: `H5` says the received catalog wording is not yet a stable
proposition, not that a correctly stated Feigenbaum theorem is false. `IntakeProbe.lean` checks only
adjacent pinned iteration, periodic-point, and limit APIs. No exact Lean target, H0, M0, R0,
accepted proof state, audit completion, theorem completion, or master acceptance is claimed.
