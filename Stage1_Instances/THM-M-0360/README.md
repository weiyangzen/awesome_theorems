# THM-M-0360 intake

This is the planned rev-5.6 instance for the repository label "Herz-Stein theorem" (Chinese:
`赫茨-施坦定理`). The repository gives only the gloss "multipliers of Hardy spaces", attributes
it to Carl Herz and Elias Stein, and dates it 1968. Those fields identify a theorem family, not an
exact theorem: they do not specify the Hardy-space model, ambient dimension/group, multiplier
class, regularity condition, exponent range, or conclusion.

Accordingly, the intake deliberately does not manufacture a canonical proposition. The next
statement task must identify and inspect an exact primary source before choosing a Lean target.
`IntakeProbe.lean` only confirms that the pinned environment contains Fourier multipliers on
Schwartz functions and tempered distributions and generic `Lp` infrastructure. It neither defines
real Hardy spaces nor proves the claimed Hardy-space multiplier theorem.

## Status

- Lifecycle: `planned`; baseline `L0 / rework_required`.
- Root vector: `H3 / M4 / R4`.
- Exact human statement: open because the source and theorem variant are unresolved.
- Canonical Lean target: open; no proof or machine-closure credit.
- Audit complete: no. Theorem complete: no.
- Authority: structured files in this directory, subject to master acceptance.

