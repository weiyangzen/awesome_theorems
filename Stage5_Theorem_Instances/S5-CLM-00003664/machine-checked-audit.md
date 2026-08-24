# Machine-checked audit — S5-CLM-00003664

The target declares an `M0-L` candidate with an empty machine cut set and no
observed non-foundation axioms. The pinned FormalConjectures declaration is
not used as proof authority. The source module spelling and qualified name are
preserved as provenance comments, while executable files use `import Mathlib`.

This worker was expressly restricted to the `--no-lean` preflight. Therefore
the structured closure record is a harvest candidate, not a canonical build
receipt. Master remains required to recompute the elaborated expression,
transitive constants, declaration bodies, dependencies, axioms, and cold
from-source trace at trust zero before acceptance.
