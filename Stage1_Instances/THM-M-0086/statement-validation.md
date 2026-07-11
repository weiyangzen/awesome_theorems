# Statement validation

The canonical Lean target is `Stage1Instances.THM_M_0086.CanonicalStatement`. It uses the single
direct import `Mathlib.CategoryTheory.Abelian.FreydMitchell`; that module transitively exports the
generator declarations required to type the two auxiliary branches. `Statement.lean` contains an
unfolded checked `iff`, exact universe/typeclass serialization, and four `#check_failure` mutation
probes. The diagnostics emitted by those probes are expected output and Lean exits successfully.

The intake deliberately retained three roots because source identity is unresolved. This statement
therefore freezes their conjunction as the exact repository package without claiming that a
primary source calls the conjunction one theorem. That unresolved human-source question belongs to
the next anchor-audit phase and prevents H0, but no longer leaves the Lean expression ambiguous.

## Validation record

Base revision: `0a10648bed0f2cf439e264125af320deb9928048`.

Exact commands and final hashes are recorded in the statement receipt. Validation is nonrelease:
the worker clone has a pre-existing untracked `Formalizations/Lean/.lake` symlink to the canonical
pinned artifacts. No Lake update/build/fetch operation was run and no dependency artifact was
modified.

## Boundary

This artifact claims only a self-tested statement node. It claims no source audit, anchor audit,
proof closure, debt-vector promotion, audit completion, or theorem completion. The first remaining
gate is `S56-M-0086-ANCHOR_AUDIT`, including primary-source branch identity and immutable candidate
provenance.
