# THM-M-0523 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
"Manin-Drinfeld theorem". The standard mathematical theorem concerns torsion divisor classes
formed from differences of cusps on modular curves. The repository source instead glosses the
item as properties of Heegner points on elliptic curves. Those are materially different claims.

The intake preserves that conflict rather than silently replacing the repository wording with the
standard theorem. A duplicate repository item, `THM-M-0124`, has a legacy Lean statement-shape
artifact about cusp differences, but rev-5.6 rejects legacy proof credit and duplicate-ID evidence.
That artifact is recorded only as a discovery lead.

The root remains `[H3, M4, R4]`. A pinned Lean probe confirms that mathlib exposes arithmetic
subgroups, cusps, and finite cusp orbits needed for a future statement. It does not expose or prove
the compactified modular curve, Jacobian/Picard divisor-class target, or Manin-Drinfeld conclusion.
Exact commands and results are in `validation.md`.
