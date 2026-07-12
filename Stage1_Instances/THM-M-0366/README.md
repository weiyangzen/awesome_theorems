# THM-M-0366 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Coifman-McIntosh-Meyer theorem.
The repository gives the topic gloss "Cauchy integrals on Lipschitz curves", the three authors, and
1982. The title of the authors' 1982 paper identifies the intended headline result more closely:
the Cauchy integral defines a bounded operator on `L^2` for Lipschitz curves. The paper's exact
theorem text, curve model, truncation convention, measure, normalization, and quantitative bound
have not yet been inspected and independently reviewed.

The scope map therefore freezes the theorem family and its proposition-changing choices without
inventing a canonical formula. The root remains `[H2, M4, R4]`. A pinned Lean probe confirms that
mathlib provides Lipschitz maps, interval/path integrals, Cauchy circle integrals, and `L^p` APIs.
These are only encoding ingredients; they do not state or prove the singular-integral theorem.
Exact commands and results are recorded in `validation.md`.

