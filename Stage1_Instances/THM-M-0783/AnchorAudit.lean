import Mathlib.SetTheory.Cardinal.Continuum

/-!
# THM-M-0783: pinned anchor probes

These checks identify the pinned mathlib infrastructure used by the canonical
statement. They do not assert or prove Martin's axiom.
-/

#check Cardinal.mk
#check Cardinal.continuum
#check Cardinal.aleph0_lt_continuum
#check Set.Countable
#check Set.Nonempty
#check Set.Ici

