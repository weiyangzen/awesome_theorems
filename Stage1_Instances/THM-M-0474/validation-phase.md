# THM-M-0474 validation-phase result

Item: `S56-M-0474-VALIDATION`

Base revision: `7a489588a59dbd7cca44de7e3b8c3bafcb7448f5`

Validation time: `2026-07-12T19:10:18Z`

The node-scoped validator re-elaborated the exact frozen statement, conditional composition,
proof-phase root, all ten semantic proof children, four parent composition certificates, and a
separately written exact root in fresh temporary local modules. `Validation.lean` imports neither
`Proof` nor `ObligationTree`: it derives the target from `Nat.ModEq.pow_totient` and
`Nat.totient_prime`, rather than calling the proof phase's direct Fermat theorem. This is useful
same-worker differential evidence, not rev-5.6 independent verification.

## Exact results

All commands ran from the repository root on 2026-07-13 (Asia/Shanghai), unless a working
directory is shown. The validator fixed the recorded locale, timezone, and toolchain variables,
used only existing `lake env` resolution, and removed its temporary modules. It did not update,
build, clone, fetch, or mutate `.lake`.

```text
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LANG=C.UTF-8 LC_ALL=C.UTF-8 TZ=UTC \
  python3 Stage1_Instances/THM-M-0474/check_validation.py
  exit 0
  PASS S56-M-0474-VALIDATION: exact proof root, frozen composition, and totient differential root kernel-replayed
  PASS trust observation: all checked proof routes are sorry-free and use only propext, Classical.choice, and Quot.sound
  PASS local provenance: frozen hashes, clean mathlib pin/tree, terminal sources, and oleans agree
  STALE authoritative graph: pre-proof M3 root awaits dependency-ordered master reconciliation
  BLOCKED proof dependency: S56-M-0474-PROOF is provisional rather than master-accepted
  BLOCKED hermetic gate: shared warm canonical .lake is not a cold empty-cache offline replay
  BLOCKED independent gate: differential source ran in this worker and shared cache, not a distinct signed runner

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1 through 1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0474
  exit 0: rank 938, planned, L0/rework_required, theorem_complete=false

python3 Stage1_Instances/THM-M-0474/check_proof.py
  exit 0: predecessor proof receipt, exact pinned root, frozen composition, and hashes passed

python3 Stage1_Instances/THM-M-0474/check_obligation_tree.py
  exit 0: 21 frozen obligations and 43 typed edges passed; accepted root remains H1/M3/R4

python3 Stage1_Instances/THM-M-0474/check_anchor_audit.py
  exit 0: seven candidates, pinned sources, hashes, and fail-closed status passed

cd Formalizations/Lean &&
  python3 ../../Stage1_Instances/THM-M-0474/check_statement.py
  exit 0: exact expression, minimal imports, checked transport, and four mutations passed

python3 Stage1_Instances/THM-M-0474/check_intake.py
  exit 0: planned dossier, empty accepted state, and six open local tasks passed

git diff --check -- Stage1_Instances/THM-M-0474 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact kernel replay | provisional pass | Exact statement, direct and composed roots, semantic children, composition certificates, and totient differential root elaborate under pinned Lean 4.29.0. |
| Placeholder/unsafe scan | pass | Four Lean modules pass a comment-stripped source scan, and 21 declarations pass kernel-level `assert_no_sorry`/`#print sorries` checks. |
| Trust observation | provisional pass | Checked proof routes report subsets of exactly `propext`, `Classical.choice`, and `Quot.sound`; full release TCB acceptance remains absent. |
| Local provenance | pass | Frozen input hashes, exact statement fingerprint, denominator, clean mathlib revision/tree, three terminal sources, Git blobs, and imported oleans agree. |
| Proof dependency | fail closed | `S56-M-0474-PROOF` has worker evidence only and is not master-accepted. |
| Structured root state | fail closed / stale | `typed-graphs.json` and `instance.json` deliberately remain pre-proof `H1/M3/R4` with no accepted receipt; reconciliation is master-controlled. |
| Hermetic release replay | fail closed | Shared warm `.lake`; no clean checkout, empty-cache cold offline restoration, complete TCB inventory, SBOM/license archive, or deterministic bundle. |
| Independent verification | fail closed | The totient source route differs locally, but ran in this worker and shared cache; no distinct identity, runner, signature, or minimal release verifier. |

This is genuinely self-tested validation-phase work and a truthful fail-closed result. It grants no
`E0/E1`, accepted `M0-*`, `AUDIT-Z`, `THEOREM-Z`, release, or theorem-completion credit.
`audit_complete=false` and `theorem_complete=false`.
