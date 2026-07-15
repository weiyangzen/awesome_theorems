# THM-M-0508 validation-phase result

Item: `S56-M-0508-VALIDATION`. Base revision:
`5b35bc151522d93c7f54966ef64f1fc630371537` (tree
`fe77824631ab2573a4596bddc1a2534c06cd23f8`).

## Result

The node is self-tested but blocked. `Validation.lean` rechecks the two
proof-phase interfaces and the frozen conditional root handoff, then separately
composes the exact root from `EventualPositiveRepresentationCount`. That
positivity proposition remains an explicit input: no inhabitant is present, so
this is not a proof of Vinogradov's theorem.

The validator copies `Statement.lean`, `AnchorAudit.lean`,
`ObligationTree.lean`, `Proof.lean`, and `Validation.lean` to a fresh temporary
directory. Each Lean invocation runs at trust level zero under Bubblewrap with
the host root read-only, only the temporary directory writable, the environment
fixed, and outbound networking unavailable. Existing pinned compiled package
artifacts are read through `LEAN_PATH`; no update, build, clone, fetch, or
dependency write is performed.

## Commands and results

Commands ran in the worker clone on 2026-07-15 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0508` | 0 | Rank 882, planned, L0/rework_required, theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0508/check_anchor_audit.py` | 0 | Bounded audit, ten pinned probes, rejected placeholder candidate, and immutable mathlib pin passed. |
| `python3 Stage1_Instances/THM-M-0508/check_obligation_tree.py` | 0 | 17 obligations and 86 typed edges passed; denominator `79ff122b...53bc2`; root remains open M4. |
| `bash Stage1_Instances/THM-M-0508/check_proof.sh` | 0 | Direct pinned Lean and scoped mathlib `lake env lean --trust=0 -t0` replays agreed; both exact proof interfaces were sorry-free and used only `propext`, `Classical.choice`, and `Quot.sound`. This ran before the validation worker packet because the historical proof checker recognizes only its own packet schema. |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0508/check_validation.py --worker-packet .stage1-worker-selftest.json` | 0 | Five network-isolated trust-zero Lean replays passed; closure has 5 roots, 2567 declarations, 103 modules, only `propext`, `Classical.choice`, and `Quot.sound`, no unexpected bodyless declaration, and no unsafe declaration. |
| JSON parsing for the spec, receipt, blocker, and worker packet | 0 | All four artifacts are valid JSON. |
| external-cache `py_compile` of `check_validation.py` | 0 | Checker syntax compiled without writing bytecode in the repository. |
| `git diff --check -- Stage1_Instances/THM-M-0508 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact kernel replay | pass, nonrelease | Exact statement, finite-count bridge, conditional handoff, two proof interfaces, and differential conditional composition elaborate at trust zero. |
| Placeholder/unsafe observation | pass in observed boundary | Local replay modules are token-scanned and assertion-checked; the five-root closure reports no unexpected bodyless or unsafe declaration. |
| Axiom observation | provisional pass | Checked declarations use only `propext`, `Classical.choice`, and `Quot.sound`; no theorem-specific foundation profile is accepted. |
| Selected provenance | pass, nonrelease | Frozen hashes, mathlib revision/tree/remote/cleanliness/license, and seven selected source/object pairs agree. Complete transitive provenance and TCB/SBOM closure are absent. |
| Proof dependency | fail closed | `S56-M-0508-PROOF` is worker-provisional `[_]`, not master-accepted `[x]`. |
| Predecessor recipes | fail closed | Graph nodes name `VAL-M0508-*`, but `validation-specs.json` is absent. This validation recipe cannot retroactively validate those missing specifications. |
| Exact root | fail | No body inhabits `EventualPositiveRepresentationCount`; the Fourier identity, arc partition, major-arc asymptotic, singular-series positivity, minor-arc estimate, and eventual-positivity assembly remain open. |
| Hermetic release | fail closed | This uses a shared warm cache, not a clean-checkout empty-cache cold build or offline-restorable deterministic bundle. |
| Independent verification | fail closed | The differential route uses this worker, checkout, kernel, and cache; no second signature, clean runner, or independent minimal verifier exists. |
| Human/readable review | fail closed | Pinpoint primary-source `H0` and independently reviewed `R0` remain open. |

The first failed node gate is
`dependency.S56-M-0508-PROOF.master_acceptance`; the mathematical root cut is
`M0508-N-FOURIER`, `M0508-B-ARCS`, `M0508-L-MAJOR`,
`M0508-L-SINGULAR`, and `M0508-L-MINOR`. The vector remains
`[H1,M4,R3]`, with `audit_complete=false` and `theorem_complete=false`.
Provisional `[_]` means only that this fail-closed validation packet is
implemented and self-tested; it grants no `E0/E1`, accepted `M0-*`, release,
or master acceptance.
