# Exact-statement gate: blocked

Item: `S56-M-1100-STATEMENT`  
Theorem: `THM-M-1100`  
Base revision: `c83a05a429c195d51008196099c68c42b7fd9ec1`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. Its
entire mathematical wording is `MCMC methods`, attributed to Nicholas Metropolis in 1953. This is
a method family, not a proposition. The Stage0 record leaves the definitions, hypotheses, proof
route, axioms, and machine artifact open. The metadata value `已验证` is explicitly untrusted under
rev-5.6 and supplies neither a source statement nor kernel evidence.

The intake identifies Metropolis et al., *Equation of State Calculations by Fast Computing
Machines* (1953), DOI `10.1063/1.1699114`, only as a discovery candidate. It does not transcribe an
exact result or independently freeze its assumptions. In particular, the available material does
not select:

- a state space, target probability measure or normalized density, and support conventions;
- a proposal and acceptance/rejection transition kernel, including zero-density cases;
- initialization and symmetry, irreducibility, aperiodicity, recurrence, integrability, or
  minorization hypotheses;
- invariance, detailed balance, convergence, an ergodic-average law, or a quantitative rate as the
  conclusion, nor the associated topology and quantifier order;
- the intended boundary between this historical item and the separately scheduled generic
  Metropolis-Hastings algorithm `THM-M-1101`.

These choices produce inequivalent propositions. Choosing one would broaden or substitute the
source label rather than elaborate it. Encoding an abstract kernel while assuming its invariance
or convergence would make the desired conclusion an input, not formalize an MCMC correctness
theorem. Accordingly the human-claim identity gate fails before a canonical Lean expression,
minimal-import proof, checked transport, or meaningful hypothesis/domain/binder/boundary mutation
can exist. Machine state remains `M4`; no statement or theorem completion is claimed.

## Lean boundary

The pinned environment is usable. `Mathlib.Probability.Kernel.Invariance` exposes general notions
of reversibility and invariance, including `Kernel.IsReversible` and
`Kernel.isReversible_isInvariant`. Those declarations do not define the 1953 algorithm and do not
choose a source-matched proposition. The existing `IntakeProbe.lean` elaborates the generic kernel
substrate only, so its successful check is environment evidence and not exact-statement evidence.

## Validation record

Commands ran from this worker clone on 2026-07-12 (Asia/Shanghai). Existing canonical `.lake`
artifacts were read only; no update, build, clone, fetch, or dependency mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1100` | 0 | rank 540, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | hashes `651c8a...b1d2` and `321626...2d81` recorded in the JSON blocker |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| repository search for `MCMC methods`, the theorem labels, and the 1953 paper | 0 | only underspecified catalogue records, intake material, and separately owned targets; no frozen proposition |
| pinned-mathlib search for Metropolis/MCMC and reversibility APIs | 0 | generic reversibility/invariance API and a Monte Carlo bibliography entry; no source-specific sampler statement |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1100/IntakeProbe.lean` | 0 | generic `Kernel`, `IsMarkovKernel`, and `Invariant` declarations elaborated; not a canonical target |

## Retry condition

An accountable reviewer must preserve and inspect an immutable primary-source edition, identify an
exact result and page/equation locators, audit errata, and freeze every mathematical choice above.
An independent review must approve the source crosswalk and the boundary with `THM-M-1101`. A later
statement run can then encode the exact claim, minimize its pinned imports, serialize and hash its
elaborated expression, check equivalent transports, and run all required structural mutations.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.
