# Exact-statement gate: blocked

Item: `S56-M-0358-STATEMENT`  
Theorem: `THM-M-0358`  
Base revision: `7780ee2963f599a6bf06f39a12c6fddb7eafc914`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. The
record supplies only the title "Fourier multiplier theorem", the gloss "L^p boundedness of Fourier
multipliers", attribution to Lars Hormander, and the year 1960. It gives no publication, immutable
edition, theorem/page, multiplier definition, symbol hypothesis, ambient domain, exponent range,
operator construction, or quantitative conclusion.

Those omissions change the proposition. The label can denote a scale-uniform integral or localized
Sobolev criterion, a Hormander-Mihlin derivative criterion, the bounded-symbol `L^2` theorem, a
periodic/group theorem, or an endpoint result. These variants have different hypotheses and
conclusions. Moreover, the adjacent target `THM-M-0359` separately names the Mihlin multiplier
theorem, so silently choosing that familiar formulation risks merging two repository targets.

The intake lists possible source families only as discovery candidates. No exact source proposition,
incorporated definitions, errata disposition, or independent source review selects one. Choosing a
standard textbook formulation would therefore invent or substitute mathematics. The canonical
human statement fails before minimal imports, an exact Lean expression and fingerprint, checked
transports, or meaningful removed-hypothesis, changed-domain, binder-scope, and boundary mutations
can be produced. Machine state remains `M4`; no declaration, proof, placeholder, axiom, weakened
special case, statement acceptance, or theorem completion is claimed.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated only to distinguish a usable pinned environment
from a missing mathematical statement. Its three imports expose Fourier multiplier continuous
linear maps on Schwartz functions and tempered distributions, the `L^2` Fourier isometry, `MemLp`,
and `eLpNorm`. These are encoding ingredients, not the unspecified Hormander `L^p` theorem.

A narrow search of pinned mathlib found the Fourier multiplier infrastructure but no Hormander or
Mihlin `L^p` multiplier theorem. This negative bounded search does not prove that no differently
named or external formalization exists; it only confirms that the pinned local API does not resolve
the source ambiguity.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. Existing canonical `.lake` artifacts were used without
update, build, clone, fetch, or dependency mutation.

## Validation evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0358` | 0 | rank 851, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | hashes `651c8a...1d2` and `321626...d81`, recorded in the JSON blocker |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision above |
| repository `rg` search for the title, gloss, attribution, and multiplier variants | 0 | found only underspecified metadata and intake/discovery material; no source-frozen proposition |
| pinned-mathlib `rg` search for Hormander, Mihlin, and multiplier-theorem vocabulary | 0 | found multiplier infrastructure only; no matching `L^p` theorem (individual Hormander/Mihlin searches had no matches) |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0358/IntakeProbe.lean` | 0 | all seven substrate API checks elaborated; no canonical target asserted |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0358 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom found |

## Retry condition

An accountable source reviewer must preserve and hash an immutable primary-source edition, select
and transcribe one exact proposition with all incorporated definitions and assumptions, dispose of
errata, distinguish it from `THM-M-0359`, and independently approve the crosswalk. The selection
must fix the ambient space and dimension, Fourier normalization, symbol condition and scale
quantifiers, origin convention, exponent range and endpoints, operator construction, constant
quantifiers, and degenerate cases. A later statement run can then encode that same claim, minimize
pinned imports, serialize and hash the elaborated expression, check alternate transports, and run
all four required mutation classes.

This is the first failed gate, not completion of the statement node or any later node. The assigned
phase is not genuinely self-tested, so no `.stage1-worker-selftest.json` is emitted.
