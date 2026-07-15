# THM-M-0325 partial proof-phase validation (slot35)

Item: `S56-M-0325-PROOF`

Base revision: `174152e95bbc5c1bc2e2ea607cd904f47eb51053`

Base tree: `b74f022b047260bfefaadef8bae73ba4f89d23c8`

## Implemented bodies

`Proof.lean` adds eleven local, placeholder-free theorem bodies at the scalar
and Hilbert-form boundary of the frozen architecture. They provide:

- direct application of `ScalarUnitBoundedBy` to arbitrary unit-polydisc and
  sign-valued realizations;
- derivation of `0 <= C` from any scalar unit-polydisc bound;
- scalar and Hilbert zero-matrix identities and bounds;
- the unit-ball real-inner-product estimate;
- a pointwise coefficient-inner-product estimate;
- the coefficient `l1` bound for `HilbertMatrixForm`; and
- the resulting unconditional `HilbertUnitBoundedBy` coefficient bound.

These are genuine proof bodies and partial progress toward
`M0325-B-SCALAR` and the later expectation/package assembly. The frozen
`M0325-B-SCALAR` formal target is still only a planned prose signature, so
zero frozen obligations are claimed closed.

## Boundary

The proof does not construct the universal real Grothendieck/Krivine
transform, correlated Gaussian-sign rounding, measurability/integrability and
finite-sum interchange, inverse-sine expectation identity, or an inhabitant of
`GrothendieckProofPackage`. `target_of_proofPackage` remains a conditional
identity and cannot substitute for the absent package. The first failed gate
remains `M0325-K-TRANSFORM`, the minimal open root cut remains
`[M0325-T-PACKAGE]`, and the root remains `[H2, M3, R4]`.

This is a self-tested partial proof contribution proposed as `[_]` for
integration-lane review. It is not theorem completion and claims neither the
proof item as a whole nor any validation, release, audit, or master-accepted
state.

## Smallest real validation

All Lean checks reused the automation-provided canonical pinned `.lake`
artifacts read-only. No `lake update`, `lake build`, dependency clone/fetch,
or dependency write was performed. Because the canonical `flt-regular`
checkout is currently incomplete and makes the repository Lake workspace
reject environment construction, `check_proof.sh` uses the pinned Lake binary
in a disposable minimal tool-probe directory to select Lean 4.29.0, then
constructs `LEAN_PATH` from existing compiled package paths. All local outputs
are created beneath `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0325` | 0 | rank 214, planned, legacy artifacts unaccepted, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0325/check_anchor_audit.py` | 0 | anchor invariants passed at mathlib `8a178386...a95` |
| `python3 Stage1_Instances/THM-M-0325/check_obligation_tree.py` | 0 | 15 obligations and 33 typed edges passed; root open M3 and analytic package M4 |
| `bash Stage1_Instances/THM-M-0325/check_proof.sh` | 0 | isolated fresh-output trust-zero replay of statement, conditional composition, anchor substrate, and eleven local proof bodies passed; every new theorem reported only `propext`, `Classical.choice`, and `Quot.sound` |
| `rg -l -i --glob '*.lean' 'grothendieck.?inequal\|grothendieckinequality\|krivine' Formalizations/Lean/.lake/packages` | 1 | expected no-match; no analytic Grothendieck/Krivine body exists in the current pinned closure |
| `rg -n -i --pcre2 --glob '*.lean' '(random.?hyperplane\|hyperplane.?round\|Gaussian.?sign\|sign.?Gaussian\|arcsin.?law\|Sheppard)' Formalizations/Lean/.lake/packages` | 1 | expected no-match; no required correlation, arcsine-law, or hyperplane-rounding body exists in the current pinned closure |
| `rg -n --pcre2 '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe\|extern)\b\|implemented_by\|native_decide' Stage1_Instances/THM-M-0325/Proof.lean` | 1 | expected no-match; no placeholder, custom axiom, unsafe/oracle escape, or proof shortcut occurs |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `8a178386...a95`, tree `bdc39a31...2c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --porcelain=v1` | 0 | zero output; the pinned mathlib dependency tree is clean |
| `for f in .stage1-worker-selftest.json Stage1_Instances/THM-M-0325/Proof.lean Stage1_Instances/THM-M-0325/check_proof.py Stage1_Instances/THM-M-0325/check_proof.sh Stage1_Instances/THM-M-0325/proof-receipt-slot35.json Stage1_Instances/THM-M-0325/proof-validation-slot35.md Stage1_Instances/THM-M-0325/proof-blocker-slot35.json; do out=$(mktemp /tmp/m0325-diffcheck.XXXXXX); git diff --no-index --check /dev/null "$f" >"$out" 2>&1; test $? -eq 1; test ! -s "$out"; rm -f "$out"; done` | 0 | all seven new-file checks had the expected difference exit and emitted zero whitespace diagnostics |

## Retry condition

The twenty prior tracked root-sized blocker rechecks already exceed rev-5.6
section 10.2's five-tick split threshold. The authoritative DAG nevertheless
records zero attempts and no children, and this worker may not change it. The
master should create dependency-legal children for the eight open analytic
obligations and freeze exact Lean signatures for their current prose targets.
