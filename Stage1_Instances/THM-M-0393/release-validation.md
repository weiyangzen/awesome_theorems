# THM-M-0393 Release Decision Handoff

## Exact verdict

`S56-M-0393-RELEASE` is **blocked**. The lifecycle remains `planned`, the root vector remains
`[H3, M4, R3]`, `audit_complete=false`, and `theorem_complete=false`. No receipt is accepted and
no theorem-completion promotion is proposed.

The first failed gate is `G02-TOPOLOGY`: `S56-M-0393-VALIDATION` remains `[_]`, not master-accepted
`[x]`. Independently, the exact root has no body or composition certificate. The validated lemma
proves only that possible integers `g` are finite once `g^n | m`; it does not prove that a
solution's gcd has that divisibility. Thus `M0393-N1` itself and all 17 canonical obligations remain
open.

## Dependency and reuse audit

The v2 graph file has SHA-256
`fb17743ff737fd3c528467b6f992a7235a36f0842b528e57de3e4c6d660d3518`, and the target context is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`. It records no direct hard
parent, transitive hard ancestor, hard edge, reuse hint, or shared group. Therefore the mandated
parent inspection order is exactly empty. `dependency-reuse-ledger.json` records that complete empty
closure; it does not claim mathematical independence or transfer proof credit.

## Evidence reconciliation

The partial proof and independently written same-workspace replay elaborate with only `propext`,
`Classical.choice`, and `Quot.sound` reported. Their local placeholder scans pass. This is narrow
kernel evidence for a strict subclaim, not Thue's theorem and not a closed registry node.

Direct replay of frozen `Statement.lean` fails because `evalBinary` depends on a noncomputable
instance but is not declared `noncomputable`. The dossier also lacks accepted H0 source review,
accepted R0 reconstruction, root provenance/axiom/TCB closure, an immutable clean snapshot, cold
offline reproduction, SBOM/licenses, two independent signed runners, an independently implemented
minimal verifier, required CI/mutation results, a deterministic evidence bundle, and bundle-derived
public projections.

The HEAD-tracked `check_release.py` now emits exactly one
`stage1-validator-semantic-result/1.0` JSON object. It truthfully reports `status=blocked`,
`phase_accepted=false`, `audit_complete=false`, `theorem_complete=false`, and 17 open obligations.
Exit zero means the negative reconciliation is internally consistent; it does not mean release is
accepted.

The HEAD/base validator was legacy prose, so this required typed-output repair necessarily changes
its blob. Current scheduler policy also requires the selected validator's HEAD blob to equal its
worker-base blob. Consequently this handoff can establish and test the correct target-owned bytes,
but only integration followed by a fresh revalidation base can make those bytes review-eligible.

## Worker checks

The handoff re-runs the structural standard, theorem DAG, phase-contract, target-manifest, obligation
tree, partial Lean modules, exact semantic release validator, JSON syntax, and diff hygiene checks.
The phase contract, target manifest, obligation tree, Lean modules, semantic validator, JSON, and
diff hygiene pass. The global standard and v2 theorem-DAG checks fail closed because the generator
inventories newly required target JSON evidence while this worker is expressly forbidden to
regenerate `Docs/Stage1_Theorem_DAG_v2.json`; master integration must reconcile that derived
projection. No dependency update, build, clone, fetch, network operation, or `.lake` mutation is
performed. The automation-provided `.lake` symlink remains untracked nonrelease state.

## Retry boundary

The owning phases must repair and refreeze the statement and close the exact root proof graph. The
integration lane must accept the full dependency chain. A separate release-grade execution must
then close source/readability review, trust/provenance, cold offline reproduction, supply-chain,
independent-verification, deterministic-bundle, public-reconciliation, and master-acceptance gates.
