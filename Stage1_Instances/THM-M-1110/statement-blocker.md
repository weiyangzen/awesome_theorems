# Exact-statement gate: blocked

Item: `S56-M-1110-STATEMENT`  
Base revision: `3f82136c3696549591ee6c2bcbea856459213d36`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository source record. The
record gives only the label "Erdos-Schlein-Yau theorem", the year 2010, and the sentence
"universality of Wigner matrices". It supplies no theorem number, edition, or exact wording. The
intake consequently freezes only a theorem family and explicitly leaves the source variant open.

Within that family, each of the following choices changes the proposition rather than merely its
Lean encoding:

- real symmetric versus complex Hermitian matrices and the matching GOE/GUE reference law;
- entry independence, identical-distribution, centering, variance, diagonal, and tail hypotheses;
- correlation functions versus gap statistics, and the test-function class and normalization;
- fixed bulk energy versus energy averaging, including the averaging-window scale;
- pointwise, integrated, or uniform convergence and the order of the `n`, `k`, energy, and error
  quantifiers.

The intake's lead, Erdos-Schlein-Yau, *Universality of Random Matrices and Local Relaxation Flow*,
is not itself a selected result: the dossier records that no pinned copy was inspected theorem by
theorem and that exact locators, hypotheses, corrections, and repository intent remain open. A
second 2010 lead has six authors and cannot be substituted based on topic and date. Selecting a
familiar bulk-universality statement from either source would therefore invent missing mathematics
and could silently strengthen or weaken energy averaging, regularity, or symmetry assumptions.

The Stage0 entry confirms that precise definitions and prerequisites, proof process, dependencies,
axioms, and machine artifacts are all `待补充` (to be supplied). Its `已验证` metadata is explicitly
untrusted under rev-5.6. There is no repo-local Lean declaration for this theorem to crosswalk.
Consequently the phase fails at exact human-claim identity, before ordered binders, minimal imports,
an elaborated expression fingerprint, checked transports, or meaningful mutation tests can be
established. A generic structure whose fields assume the desired universality conclusion would be
a forbidden placeholder, not an elaboration of the theorem.

## Required unblock

An accountable source reviewer must select an immutable primary edition and exact numbered theorem
or displayed result, verify errata, and freeze its symmetry class, probability spaces and matrix
laws, entry assumptions, spectral observable, bulk domain, mean-spacing normalization, Gaussian
reference statistic, convergence mode, rates or uniformity, quantifier order, and all boundary
cases. A later statement worker can then encode that claim, minimize pinned imports, print and hash
the elaborated expression, and mutation-test proposition-changing alterations.

## Narrow validation evidence

Commands ran in this worker clone on 2026-07-12. The existing canonical `.lake` symlink was used
read-only; no update, build, clone, fetch, or dependency mutation was performed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1110` | exit 0; rank 550, planned, `L0/rework_required`, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; `651c8acc...b1d2` and `321626c8...2d81` |

First failed gate: exact source-statement identity. Known failures are the canonical Lean target,
minimal-import determination, expression fingerprint, checked transport, and mutation tests. The
assigned phase is therefore not self-tested or complete, and no `.stage1-worker-selftest.json` is
emitted. No theorem completion or downstream-node credit is claimed.
