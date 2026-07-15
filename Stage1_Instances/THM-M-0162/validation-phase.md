# THM-M-0162 validation-phase result

Item `S56-M-0162-VALIDATION` was run against the provisional proof snapshot at
base `443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b` (tree
`c5771c47c12b80aba613e6d844570f83b39ded6d`). Validation added no mathematical
proof content. `Validation.lean` is only a trust probe over the existing exact
root and the three frozen equation packages.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Fresh-output kernel replay | pass, provisional | Bubblewrap denied network access and compiled `Statement.lean`, `ObligationTree.lean`, `Proof.lean`, and the proof-only probe with `--trust=0`, fixed locale/timezone, one Lean thread, and fresh temporary `.olean` outputs. |
| Exact conclusion and composition | pass, provisional | `frenetSerret : FrenetSerretTarget`; `root_of_equation_packages` is the checked root composer over the three exact equation packages. |
| Placeholder/unsafe/oracle hygiene | pass for inspected local sources and checked roots | Lean's transitive `assert_no_sorry`/`#print sorries` checks pass for all four declarations. A nested-comment-aware source scan finds no `sorry`, `admit`, `sorryAx`, bodyless axiom/constant, `opaque`, `unsafe`, `extern`, `implemented_by`, or `native_decide`. This is not a complete transitive declaration audit. |
| Axiom observation | pass, provisional | Each equation package and the exact root reports exactly `propext`, `Classical.choice`, and `Quot.sound`. The foundation policy is still unaccepted. |
| Selected local provenance | pass, provisional | Local source and proof-receipt hashes, frozen denominator, mathlib revision/tree/remote/license, clean mathlib source checkout, and pinned toolchain identity agree. Complete declaration/import/compiled-artifact provenance is absent. |
| Dependency legality and structured freshness | fail closed | `S56-M-0162-PROOF` is only `[_]`, not master accepted. The frozen registry and typed graphs predate proof closure and still report `H1/M3/R4`, `root_closed=false`, and no accepted proof evidence. |
| Hermetic release replay | fail closed | The replay used the automation-provided shared warm `.lake`. The root Lake package set also lacks a valid pinned `flt-regular` HEAD, so root `lake env` resolution failed and attempted package fetches during preflight. No such failed run is credited. There was no clean checkout, empty-cache cold build, offline restoration, full TCB/SBOM, deterministic bundle, or signed attestation. |
| Independent verification | fail closed | The trust-only probe uses this worker, checkout, kernel, and shared cache. There is no distinct runner, verifier identity/signature, second attestation, or independently implemented minimal verifier. |

## Commands and results

Commands ran on 2026-07-15 (`Asia/Shanghai`). No `lake update`, `lake build`,
dependency clone, or manual dependency fetch/repair was run. During early
preflight, root `lake env` package discovery encountered the concurrently
created invalid `flt-regular` checkout and initiated unsuccessful automatic
fetch attempts before failing; those runs are excluded from validation evidence.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups; 1546 uniform-L0 Lean 4 targets

python3 scripts/stage1_target.py check
  exit 0: 1546 unique ordered targets, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0162
  exit 0: rank 661, planned, theorem_complete false

cd Formalizations/Lean && lake env lean --version
  exit 1: root package resolution failed because .lake/packages/flt-regular
  had no resolvable HEAD; excluded from pinned evidence

cd Formalizations/Lean/.lake/packages/mathlib && lake env lean --version
  exit 0: Lean 4.29.0, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740

bash Stage1_Instances/THM-M-0162/check_validation.sh
  exit 0: network-denied, trust-zero, fresh-output replay passed
  all four declarations depend on [propext, Classical.choice, Quot.sound]
  all four declarations are transitively sorry-free
  Statement.olean sha256: 600c5c2245299aab10f2b06d7c5e265b13645ea765535b4eb6cd5bcdacb740cb
  ObligationTree.olean sha256: 49337fdb13e00d360fc326802d5b9d130ccd4b0ca2b0a75c3868127fe702714e
  Proof.olean sha256: d05074e8f9cbfcdf27e08aa7195c4e5d8ea3eca6e96871abcd5d0a35d10b7984
  Validation.olean sha256: 8753f976886261190656a942cdd16023af5285548e1ef09a0b365a05fabce75c

python3 -I -B Stage1_Instances/THM-M-0162/check_obligation_tree.py
  exit 0: 17 obligations and 49 typed edges passed; authoritative root
  remained open M3 with denominator 28db67d8...ca23ff

python3 -I -B Stage1_Instances/THM-M-0162/check_validation.py
  exit 0: narrow validation passed while dependency, authority, complete
  trust/provenance, hermetic release, and independent gates failed closed
```

The first node gate failure is
`S56-M-0162-VALIDATION-PREREQUISITE-NOT-ACCEPTED`; the first release gate
failure is `S56-10.6-HERMETIC-COLD-BUILD`. The accepted vector remains
`H1/M3/R4`. This packet claims no accepted receipt, `E0/E1`, accepted `M0-L`,
`AUDIT-Z`, `THEOREM-Z`, theorem completion, release, or master acceptance.
