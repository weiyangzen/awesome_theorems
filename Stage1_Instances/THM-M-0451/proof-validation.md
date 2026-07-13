# THM-M-0451 proof-phase validation

Item: `S56-M-0451-PROOF`. Base revision:
`c45f3c7090cb4adf616d45e5414985f956e807b2`.

## Implemented bodies

`Proof.lean` implements Tate's generic limiting argument. A uniformly bounded
one-step expansion error gives a Cauchy normalized orbit, its selected limit,
the exact limit formula, a uniform `C / (r - 1)` comparison, and exact scaling
under the expanding map. The code specializes this construction to the
statement's exact sequence and `xHeight / 2` normalization.

For elliptic points, an explicit uniform doubling estimate now conditionally
supplies `M0451-HEIGHT`, `M0451-LIMIT`, `M0451-BOUNDED`, and
`M0451-NONNEGATIVE`. Adding an explicit approximate parallelogram estimate
conditionally supplies the exact `M0451-PARALLELOGRAM` identity and all-integer
`M0451-QUADRATIC` law. A separate finite-orbit argument gives
`M0451-TORSION-ZERO` directly from the doubling estimate. The purely algebraic
torsion consequence of an already supplied integer square law is also checked.

These are implication theorems, not premises in disguise: the file declares no
elliptic height estimate and no package inhabitant. Consequently no frozen
obligation is newly closed. `M0451-APPROX` and `M0451-ZERO-TORSION` remain open,
the canonical engine remains uninhabited, and the exact root remains unproved.

## Commands and results

Validation ran in the worker clone on 2026-07-14. Existing pinned Lake
artifacts were reused without update, build, fetch, clone, network access, or
`.lake` mutation.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0451` | 0 | rank 93 remains planned, rework-required, and theorem-incomplete |
| `python3 Stage1_Instances/THM-M-0451/check_obligation_tree.py` | 0 | the frozen 17-obligation, 44-edge architecture passed with the root open |
| `python3 -B Stage1_Instances/THM-M-0451/check_proof.py` | 0 | isolated temporary-olean replay passed; all eleven axiom probes reported exactly `propext`, `Classical.choice`, and `Quot.sound` |
| `python3 -m json.tool Stage1_Instances/THM-M-0451/proof-receipt.json` | 0 | provisional receipt parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0451-proof-pycache python3 -m py_compile Stage1_Instances/THM-M-0451/check_proof.py` | 0 | checker syntax compiled outside the repository |
| prohibited-construct scan over target Lean sources | 1 (expected) | no `sorry`, `admit`, `sorryAx`, axiom/constant/opaque/unsafe declaration, native oracle, external implementation, or `extern` matched |
| `git diff --check -- Stage1_Instances/THM-M-0451 .stage1-worker-selftest.json` plus new-file checks | 0 | no whitespace diagnostics |

The narrow replay compiles `Statement.lean` and `ObligationTree.lean` to a
temporary directory, then elaborates `Proof.lean` against those oleans and the
canonical pinned dependency path. It leaves no olean in the repository.

## Open boundary

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`
has no elliptic canonical-height theorem and no proof of the required uniform
x-coordinate-height estimates. The audited external Heights project has
adjacent estimates but is not a compatible pinned terminal proof of this exact
target. The reverse torsion-kernel direction also needs Northcott-style
finiteness absent from the pinned closure. Importing neither gap, the worker
truthfully proposes only self-tested partial proof progress with
`root_closed=false` and `theorem_complete=false`.
