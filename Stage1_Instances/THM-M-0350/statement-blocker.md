# Exact-statement gate: blocked

Item: `S56-M-0350-STATEMENT`  
Theorem: `THM-M-0350`  
Base revision: `cc46a50150dae27c90dca0938294d8da17db9109`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. The
record gives only the title "Hilbert transform boundedness", attributes it to Marcel Riesz in
1928, and says "the Hilbert transform is bounded on `L^p`." It gives no formula, primary-source
pinpoint, exponent range, domain, scalar field, measure normalization, operator construction, or
conclusion with quantified constants.

Those omissions are proposition-changing. In particular, the record does not select between the
real-line singular integral and the periodic conjugate-function operator. It does not fix kernel
sign or the `1 / pi` normalization, real or complex values, truncated integrals versus an almost
everywhere principal value versus an `L^p` extension, or whether the claim is existence of a
bounded linear operator, a norm inequality with an unspecified constant, or the sharp estimate.
The endpoint exclusions `p = 1` and `p = infinity` are mathematically essential but are not stated
in the repository gloss.

The intake's citation of Marcel Riesz, *Sur les fonctions conjuguées*, **Mathematische
Zeitschrift** 27 (1928), 218-244, is explicitly a discovery candidate. No immutable edition,
pinpoint theorem, incorporated definitions, errata disposition, or independent source review has
selected a proposition from it. Silently choosing a standard modern real-line formulation, a
periodic formulation, an `L²` special case, or an abstract postulated operator would invent or
substitute mathematics.

Consequently the canonical human statement fails before a minimal import, exact Lean expression,
expression fingerprint, checked transports, or meaningful removed-hypothesis, changed-domain,
binder-scope, and boundary mutation tests can be produced. Machine state remains `M4`; statement
acceptance and theorem completion are false. No declaration, `sorry`, `admit`, axiom, placeholder,
weakened special case, or broadened target was introduced.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated only to distinguish a usable pinned environment
from a missing mathematical statement. Its two direct imports expose `MeasureTheory.Lp`,
`MeasureTheory.MemLp`, continuous linear maps, and Fourier multipliers on Schwartz functions and
tempered distributions. These are encoding ingredients, not a definition of the selected Hilbert
transform or an `L^p` boundedness proposition, so the probe receives no statement or proof credit.

Narrow search of pinned mathlib found no declaration named for a Hilbert transform, Cauchy
principal value, or conjugate-function theorem. That absence does not itself make the mathematical
statement impossible to encode, but it confirms that no existing exact declaration resolves the
source ambiguity.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The existing canonical `.lake` artifacts were used
read-only; no update, build, clone, fetch, or dependency mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0350` | 0 | rank 843, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | hashes `651c8a...1d2` and `321626...d81`, recorded in the JSON blocker |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision above |
| repository `rg` search for the theorem ID, title, gloss, and candidate paper | 0 | found only underspecified metadata and intake discovery material; no source-frozen proposition |
| pinned-mathlib `rg` search for Hilbert transform, Cauchy principal value, and conjugate function | 1 | no matching declaration (`rg` exit 1 means no match) |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0350/IntakeProbe.lean` | 0 | all six substrate API checks elaborated; no canonical target asserted |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0350 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom found |

## Retry condition

An accountable source reviewer must preserve and hash an immutable primary-source edition, select
and transcribe one exact proposition with all incorporated definitions and assumptions, dispose of
errata, and independently approve the crosswalk. The selection must fix the real-line or periodic
domain, scalar field, measure and kernel normalization, exponent representation and endpoints,
transform construction, constant quantifiers, and degenerate cases. A later statement run can then
encode that same claim, minimize pinned imports, serialize and hash the elaborated expression,
check alternate transports, and run all four required mutation classes.

This is the first failed gate, not completion of the statement node or any later node. The assigned
phase is not genuinely self-tested, so no `.stage1-worker-selftest.json` is emitted.
