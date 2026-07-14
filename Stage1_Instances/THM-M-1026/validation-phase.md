# THM-M-1026 validation-phase evidence

Item: `S56-M-1026-VALIDATION`. Base revision:
`a1a7e939e58f103f5ff5d23af51437fa8658aa04`; base tree:
`d881fd9641fa3e5f3ebe5082b35672981e90adcf`.

## Validation scope

The structured recipe re-elaborates the exact frozen statement, the conditional
two-direction merge, all three converse proof declarations, and a separately
written converse plus conditional-root composition. `Validation.lean` imports
`ObligationTree` but not `Proof`, and never invokes a proof-phase declaration.
It independently reconstructs the stable normalizers, eventual weak limit, and
converse terminal while retaining necessity as an explicit premise at the root.
This is same-worker differential evidence, not an independent theorem proof or
the distinct verifier required for release.

Every Lean subprocess runs at trust level zero inside Bubblewrap with the host
root read-only, a fresh writable target directory, and outbound network denied.
The run uses the existing pinned Lean and canonical `.lake` artifacts without
updating, building, fetching, cloning, or mutating them. Reusing that warm cache
means this is nonrelease node evidence, not the cold empty-cache and offline-
restorable reproduction required by section 10.6.

## Commands and results

Commands ran from this worker clone on 2026-07-15 (Asia/Shanghai).

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and all 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique ordered targets at ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-1026
  exit 0: rank 502; planned L0/rework-required target; theorem incomplete

python3 Stage1_Instances/THM-M-1026/check_statement.py
  exit 0: canonical expression SHA-256 e39476697d12d054b84ab39c07251418d449ba5ea094c2bb37df9850c7caff93; four mutations distinguished

python3 Stage1_Instances/THM-M-1026/check_obligation_tree.py
  exit 0: frozen 16-obligation, 46-edge architecture passed and truthfully retained its pre-proof M3 root and two-direction cut set

python3 -I -B Stage1_Instances/THM-M-1026/check_validation.py
  exit 0: network-isolated trust-zero replay checked the exact statement,
  conditional merge, converse proof, and differential converse/conditional root;
  eight declarations reported exactly propext, Classical.choice, and Quot.sound

python3 -m json.tool Stage1_Instances/THM-M-1026/validation-spec.json
python3 -m json.tool Stage1_Instances/THM-M-1026/validation-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0 for each: valid JSON

PYTHONPYCACHEPREFIX=/tmp/stage1-m1026-validation-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-1026/check_validation.py
  exit 0: checker syntax compiled outside the repository tree

git diff --check -- Stage1_Instances/THM-M-1026 .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics
```

`check_proof.py` is deliberately not a validation recipe: it is coupled to the
old proof worker's self-test item ID. The validation checker instead rechecks
the proof phase, receipt, blocker, source hashes, obligation fingerprints, and
partial-root boundary directly before replaying the Lean sources.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact statement and mutation boundary | pass | The canonical expression hash agrees and four non-equivalent structural mutations remain distinct. |
| Kernel and composition replay | provisional partial pass | The frozen conditional merge, complete converse branch, differential converse, and conditional exact-root path elaborate. Necessity is never supplied. |
| Placeholder and unsafe boundary | pass | Comment-stripped sources and Lean output contain no sorry/admit/sorryAx, bodyless axiom/constant, opaque/unsafe/extern escape, implemented-by hook, or native decision shortcut. |
| Trust observation | provisional pass | Eight declarations report exactly `propext`, `Classical.choice`, and `Quot.sound`; no accepted theorem-specific foundation profile or complete transitive TCB closure exists. |
| Selected provenance | provisional pass | Local hashes, clean mathlib revision/tree/remote/license, direct bounded-function and convolution substrate, and anchor support artifacts agree. The characteristic-function and Levy files are support only; the Gaussian CLT is a rejected substitution. Complete transitive provenance remains open. |
| Proof dependency and structured authority | fail closed | `S56-M-1026-PROOF` is only worker `[_]` with `accepted=false`. The frozen graph therefore remains M3; its sharper M2 cut is only proposed after proof receipt acceptance. |
| Exact root | fail closed | `M1026-T-NECESSITY` has no body; the first missing lower package is `M1026-C-BLOCK-DECOMPOSITION`. A conditional merge cannot close the root. |
| Hermetic release replay | fail closed | Shared warm `.lake`; no new clean checkout, empty-cache cold bootstrap, complete TCB/SBOM archive, or offline restoration. |
| Independent verification | fail closed | Separate source path, but the same worker, clone, kernel, and cache; no distinct identity, signed attestation, independently provisioned runner, or independent minimal receipt/graph verifier. |

The first workflow gate is
`dependency.S56-M-1026-PROOF.master_acceptance`; the first theorem gate is
`proof.root_kernel_closure.M1026-T-NECESSITY`; the first release gate is
`S56-10.6-HERMETIC-COLD-BUILD`. The frozen pre-proof graph remains
`[H2, M3, R4]`; no debt vector is master-accepted.
After proof receipt acceptance only, the converse evidence proposes machine
debt `M2` with cut set `M1026-T-NECESSITY`. Primary-source `H0`, independently
reviewed `R0`, `AUDIT-Z`, `THEOREM-Z`, release, and theorem completion remain
false.
