# THM-M-0395 release reconciliation

## Verdict

The `S56-M-0395-RELEASE` worker verdict is `blocked`. The release phase is not accepted:
`audit_complete=false`, `theorem_complete=false`, and the lifecycle and root vector remain `planned`
and `[H1, M4, R3]`. This is a self-tested negative reconciliation, not `AUDIT-Z`, `THEOREM-Z`,
theorem completion, release acceptance, or master acceptance.

The first failed gate is `G02-TOPOLOGY`. The sole task-state authority records
`S56-M-0395-VALIDATION` as `[_]`, not `[x]`. Its target-owned receipt is provisional, binds ancestor
revision `c6c42c0e2299434c893a99fb40cc6f586e261523`, and lacks the current contract's normalized
acceptance, self-test, semantic-result, base-tree, and release-grade fields. It also binds the old
validation-runner bytes; this handoff repairs that runner rather than pretending to refresh a
predecessor receipt from the release phase. The stale receipt cannot support release acceptance.

## DAG and reuse audit

The exact claim tuple is `(v2_execution_rank=8, phase_layer=6,
phase_item_id=S56-M-0395-RELEASE)`. The theorem DAG digest is
`e8472863a24609e37868f215bbf0e0654b11a62f912a403ebca5feb8de5a3b9b`, and the target context digest
is `068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`. The complete parent
inspection order is empty: there are no direct hard parents, transitive hard ancestors, hard edges,
reuse hints, or shared groups. The schema-1.1 target-owned ledger records that exact empty closure.
No provider body was inspected, copied, imported, transported, or credited, and no provider
acceptance was transferred.

## Evidence boundary

`Statement.lean` still elaborates the exact Faltings target. The three local proof transports and
three independently written same-workspace probes also elaborate under the pinned Lean 4.29.0 and
mathlib environment, reporting only `propext`, `Classical.choice`, and `Quot.sound`. This is warm,
nonrelease kernel evidence for elementary transport lemmas. Both predecessor receipts correctly
close no frozen obligation. There is no declaration proving `Stage1Rev56.THMM0395.Statement`, and all
seventeen root-relevant obligations plus exact root composition remain open.

The proof and validation shell runners previously wrote `Statement.olean` beside the owned source,
while Lean resolved the imported module from Lake's build path. They now compile copied sources in
disposable worker-local directories, extend `LEAN_PATH` explicitly, and use `--trust=0`. The repaired
checks pass, but their changed bytes make the old validation receipt stale. This release handoff
records that invalidation; it does not issue a replacement validation receipt or transfer acceptance.

The dossier remains H1 and R3. It has no accepted pinpoint primary-source/errata review, independent
H0/R0 review, complete root provenance/axiom/trust/TCB closure, immutable clean snapshot, empty-cache
cold/offline replay, SBOM/license closure, deterministic evidence bundle, accepted bundle-derived
public projections, two qualifying independent attestations, or independently implemented minimal
verifier. Consequently neither `AUDIT-Z` nor `THEOREM-Z` is established.

The HEAD-tracked `check_release.py` now emits exactly one
`stage1-validator-semantic-result/1.0` JSON object. Its typed result is `status=blocked`,
`verdict=blocked`, `phase_accepted=false`, `audit_complete=false`, `theorem_complete=false`, and
`open_obligations=17`. Exit zero means the negative reconciliation is internally consistent; it does
not mean release is accepted.

The worker base validator emitted legacy prose, so the mandatory typed-output repair changes its
blob. Scheduler policy requires a selected validator's HEAD blob to equal its worker-base blob.
Therefore this handoff establishes and tests the correct target-owned bytes, but integration followed
by fresh revalidation is required before those bytes can be review-eligible.

## Worker checks

The handoff runs the repository structural validators, target manifest checks, target-owned
obligation/validation checks, narrow Lean re-elaboration, exact semantic release validator, strict
JSON syntax checks, Python compilation with bytecode outside the repository, and diff hygiene. It
does not run `lake update`, `lake build`, dependency clone/fetch, or mutate `.lake`. The
automation-provided `.lake` symlink is reused read-only and remains untracked nonrelease state.

After adding the newly contract-required release receipt, specification, and dependency ledger, the
repository-wide standard and theorem-DAG checks are expected to report generated inventory drift.
The worker is forbidden to regenerate `Docs/Stage1_Theorem_DAG_v2.json`; the master integration lane
must reconcile that read-only projection after copying the owned-path evidence.

## Retry boundary

First close and master-accept every predecessor and the unchanged exact Faltings root, and reconcile
the full frozen audit. Then close accepted H0/R0, provenance/trust/TCB/SBOM/license, immutable
cold/offline reproduction, deterministic bundling and public reconciliation, distinct independent
attestations, the minimal verifier, protected CI, and final master release gates.
