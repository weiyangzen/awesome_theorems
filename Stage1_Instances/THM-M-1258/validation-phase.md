# THM-M-1258 validation-phase result

Item: `S56-M-1258-VALIDATION`. Base revision:
`723677fe13f105920423b0f6bf1a88edcdbfffbe`.

The structured recipe in `validation-spec.json` ran without network access or `.lake` mutation. In
a fresh temporary module directory it elaborated the exact statement, composition harness, proof,
and `Validation.lean`, an independently written reconstruction of the coordinate-field witness
that does not import `Proof`. All printed declarations depend only on `propext`,
`Classical.choice`, and `Quot.sound`; the source scan found no `sorry`, `admit`, `sorryAx`, `axiom`,
or `unsafe` declaration. Input hashes, the frozen denominator, and the clean pinned mathlib revision
were checked.

## Commands and results

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1258` | 0 | rank 436; planned; theorem_complete false |
| `python3 Stage1_Instances/THM-M-1258/check_obligation_tree.py` | 0 | 9 obligations, 22 typed edges, frozen denominator passed; authoritative root open |
| `python3 Stage1_Instances/THM-M-1258/check_validation.py` | 0 | kernel, axiom, placeholder, hash, pin, composition, proof, and differential reconstruction checks passed; release gates failed closed |
| `python3 -m json.tool Stage1_Instances/THM-M-1258/validation-spec.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1258/validation-receipt.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1258 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

This is nonrelease warm-cache evidence. The authoritative `typed-graphs.json` predates the proof
body and still reports `root_closed=false` with `M1258-L-SPAN` as its cut; workers may not reconcile
that state. The first release failure is the section 10.6 cold empty-cache hermetic gate. Complete
TCB/SBOM/license and offline-restoration evidence is absent. The local differential reconstruction
is not section 10.7 independent verification because it shares this checkout, toolchain, and
writable dependency cache and has no distinct attestor. Therefore `audit_complete=false` and
`theorem_complete=false`; this receipt supports only provisional worker state pending master
acceptance.
