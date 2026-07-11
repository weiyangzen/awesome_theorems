# THM-M-0392 Validation Handoff

Item: `S56-M-0392-VALIDATION`

## Verdict boundary

This validation node is self-tested only as a fail-closed provisional handoff. The three partial
proof obligations implemented by `Proof.lean` and separately reconstructed by `Validation.lean`
kernel-elaborate. The required integral-points finiteness bridge `M0392-X-SIEGEL` has no checked
terminal body, so the canonical Mordell-finiteness root remains open. This handoff claims neither
audit completion nor theorem completion.

## Kernel, trust, and provenance results

Both modules elaborate with Lean 4.29.0. All six checked declarations report only `propext`,
`Classical.choice`, and `Quot.sound`; neither local module contains `sorry`, `admit`, an axiom
declaration, or an unsafe declaration. The fail-closed verifier reloads the frozen eight-node
registry, typed graph, and node ledger, checks their identities, verifies the proof receipt's source
and input hashes, checks its exact three-obligation partial closure, and requires the root and Siegel
bridge to remain machine-open.

The receipt binds the pinned mathlib revision plus source and `.olean` digests for the affine and
normal-form modules used by the local proofs. No terminal provenance packet can exist for
`M0392-X-SIEGEL` because no terminal declaration was identified.

## Commands and results

Commands ran from base revision `8532255651da718bca9900badd6c74ba110cc9ab` on 2026-07-12
(`Asia/Shanghai`; receipt timestamp `2026-07-11T19:30:09Z` UTC).

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0392
  exit 0: rank 2; lifecycle planned; theorem_complete=false

cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0392/Proof.lean
  exit 0: four local declarations elaborated; each reports only propext,
  Classical.choice, and Quot.sound

cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0392/Validation.lean
  exit 0: three independently reconstructed declarations elaborated; each reports only
  propext, Classical.choice, and Quot.sound

python3 Stage1_Instances/THM-M-0392/check_validation.py
  exit 0: eight-node identity, proof-receipt freshness, pinned provenance, three
  partial closures, fail-closed root, independent probe, and placeholder policy verified

rg -n '\b(sorry|admit)\b|^[[:space:]]*(axiom|unsafe)\b' \
  Stage1_Instances/THM-M-0392/Proof.lean \
  Stage1_Instances/THM-M-0392/Validation.lean
  exit 1 with empty output: pass, no prohibited construct found

python3 -m json.tool Stage1_Instances/THM-M-0392/validation-receipt.json
  exit 0: receipt is valid JSON

git diff --check -- Stage1_Instances/THM-M-0392 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was performed. The
pre-existing canonical pinned `.lake` symlink was reused.

## Failed gates

The first failed gate is the proof prerequisite: `M0392-X-SIEGEL`, exact-root closure, and master
acceptance are absent. The same-workspace independent probe is useful cross-check evidence, not the
distinct signed runner required by section 10.7. Empty-cache hermetic replay, root provenance and
trust closure, H0/R0 review, SBOM/licenses, deterministic bundling, and release acceptance remain
open.
