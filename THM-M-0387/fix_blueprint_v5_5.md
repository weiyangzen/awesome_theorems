# THM-M-0387 Fix Blueprint v5.5

- Scope: `THM-M-0387`
- Date: `2026-04-24`
- Purpose: turn the review findings and `Docs/Blueprint_Guidelines.md` requirements into a standalone fix checklist.
- Rule: every item starts as `[ ]`; check only after the named evidence exists in public tracked files or the stated local command has been rerun successfully.

## Summary

- Total checklist items: `211`
- Lifecycle decision as of `2026-04-24 14:02:00 CST (+0800)`: this v5.5 fix blueprint is a temporary release-planning artifact, not a permanent folder-contract artifact; keep it through v5.5 closeout, then delete or archive it after fixes are merged and section K is complete.
- Authoritative progress surface: `THM-M-0387/full_study.md :: Execution Checklist`
- Public merge targets:
  - `THM-M-0387/full_study.md`
  - `THM-M-0387/machine_checked_audit.md`
  - `THM-M-0387/process_audit.md`
  - `THM-M-0387/eligibles/n4_proof_process.md`
  - `THM-M-0387/eligibles/n3_proof_process.md`
  - `THM-M-0387/eligibles/regular_primes_proof_process.md`
  - `THM-M-0387/README.md`
  - `THM-M-0387/build_validation.md`
  - `THM-M-0387/meta.json`
  - `THM-M-0387/run_local_validation.sh`

## A. Authoritative Status Surface

- [x] A01 Confirm `THM-M-0387/full_study.md :: Execution Checklist` is the single authoritative human-readable progress surface.
- [x] A02 Record in `full_study.md` that `machine_checked_audit.md`, `process_audit.md`, and `eligibles/` explain the checklist but do not override it.
- [x] A03 Remove or rewrite any progress summary that conflicts with the checklist total.
- [x] A04 Ensure `README.md` points readers to `full_study.md :: Execution Checklist` for execution progress.
- [x] A05 Ensure `eligibles/README.md` does not claim more completed units than the authoritative checklist.
- [x] A06 Ensure `meta.json` does not encode a completion claim that conflicts with the authoritative checklist.
- [x] A07 Ensure any future checklist update includes both a public merge target and a closure status for each unit.
- [x] A08 Ensure stale totals such as `0/18`, `13/18`, or `18/18` appear only if they match the v5.5 checklist dated `2026-04-24`.

## B. Execution Unit Gate Sync

- [x] B01 Reconcile `FLT-HR-001` status between `full_study.md`, `process_audit.md`, `machine_checked_audit.md`, and `eligibles/n4_proof_process.md`.
- [x] B02 Reconcile `FLT-HR-002` status between `full_study.md`, `process_audit.md`, `machine_checked_audit.md`, and `eligibles/n4_proof_process.md`.
- [x] B03 Reconcile `FLT-HR-003` status between `full_study.md`, `process_audit.md`, `machine_checked_audit.md`, and `eligibles/n4_proof_process.md`.
- [x] B04 Reconcile `FLT-HR-004` status between `full_study.md`, `process_audit.md`, `machine_checked_audit.md`, and `eligibles/n4_proof_process.md`.
- [x] B05 Reconcile `FLT-HR-005` status between `full_study.md`, `process_audit.md`, `machine_checked_audit.md`, and `eligibles/n4_proof_process.md`.
- [x] B06 Reconcile `FLT-HR-006` status between `full_study.md`, `process_audit.md`, `machine_checked_audit.md`, and `eligibles/n4_proof_process.md`.
- [x] B07 Reconcile `FLT-HR-007` status between `full_study.md`, `process_audit.md`, `machine_checked_audit.md`, and `eligibles/n4_proof_process.md`.
- [x] B08 Reconcile `FLT-HR-008` status between `full_study.md`, `process_audit.md`, `machine_checked_audit.md`, and `eligibles/regular_primes_proof_process.md`.
- [x] B09 Reconcile `FLT-HR-009` status between `full_study.md`, `process_audit.md`, `machine_checked_audit.md`, and `eligibles/regular_primes_proof_process.md`.
- [x] B10 Reconcile `FLT-HR-010` status between `full_study.md`, `process_audit.md`, `machine_checked_audit.md`, and `eligibles/regular_primes_proof_process.md`.
- [x] B11 Reconcile `FLT-HR-011` status between `full_study.md`, `process_audit.md`, `machine_checked_audit.md`, and `eligibles/regular_primes_proof_process.md`.
- [x] B12 Reconcile `FLT-HR-012` status between `full_study.md`, `process_audit.md`, `machine_checked_audit.md`, and `eligibles/regular_primes_proof_process.md`.
- [x] B13 Reconcile `FLT-HR-013` status between `full_study.md`, `process_audit.md`, `machine_checked_audit.md`, and `eligibles/regular_primes_proof_process.md`.
- [x] B14 Reconcile `FLT-HR-014` status between `full_study.md`, `process_audit.md`, `machine_checked_audit.md`, and `eligibles/regular_primes_proof_process.md`.
- [x] B15 Reconcile `FLT-HR-015` status between `full_study.md`, `process_audit.md`, `machine_checked_audit.md`, and `eligibles/regular_primes_proof_process.md`.
- [x] B16 Reconcile `FLT-HR-016` status between `full_study.md`, `process_audit.md`, `machine_checked_audit.md`, and `eligibles/regular_primes_proof_process.md`.
- [x] B17 Reconcile `FLT-HR-017` status between `full_study.md`, `process_audit.md`, `machine_checked_audit.md`, and `eligibles/regular_primes_proof_process.md`.
- [x] B18 Reconcile `FLT-HR-018` status between `full_study.md`, `process_audit.md`, `machine_checked_audit.md`, and `eligibles/regular_primes_proof_process.md`.
- [x] B19 For every `FLT-HR-*` marked completed, verify machine anchor evidence is named.
- [x] B20 For every `FLT-HR-*` marked completed, verify public merge target evidence is named.
- [x] B21 For every `FLT-HR-*` marked completed, verify independent `<=100` local ledger evidence is named.
- [x] B22 For every `FLT-HR-*` left open, ensure all other files avoid `checked/completed` wording for the same unit.
- [x] B23 Ensure completed status uses one canonical vocabulary across files: `completed` plus `Completion Gate = passed`.
- [x] B24 Ensure unfinished status uses one canonical vocabulary across files: `missing/open` plus `Completion Gate = missing/not passed`.

## C. Machine-Checked Boundary

- [x] C01 State that `n = 4` repo-local theorem-level closure is via mathlib import and wrapper theorem `flt4Path`.
- [x] C02 State that `n = 3` repo-local theorem-level closure is via mathlib import and wrapper theorem `flt3Path`.
- [x] C03 State that `flt4IntPath` is a repo-local derived wrapper from mathlib equivalence.
- [x] C04 State that `flt8ViaFlt4Path` is a repo-local derived wrapper using exponent divisibility monotonicity.
- [x] C05 State that the full FLT theorem is not repo-local machine-checked in this repository.
- [x] C06 State that regular primes theorem closure is upstream, not vendored into this repository.
- [x] C07 Preserve the exact regular-primes boundary sentence: `upstream theorem closure: yes / repo-local vendored theorem closure: no, anchor-only / repo-local anchor-only statement/module/theorem-name record: yes`.
- [x] C08 Ensure `RegularPrimesPath.lean` is described as statement-shape and upstream-anchor code, not as a local proof of `flt_regular`.
- [x] C09 Ensure `machine_checked_audit.md` separates local wrappers from upstream-only closure.
- [x] C10 Ensure `process_audit.md` separates local process ledgers from upstream theorem closure.
- [x] C11 Ensure `full_study.md` status language says `部分验证 / 进行中`, not global `已验证`.
- [x] C12 Ensure `README.md` status language says `部分验证 / 进行中`, not global `已验证`.
- [x] C13 Ensure `meta.json` status detail includes the upstream-only nature of regular primes.
- [x] C14 Ensure no public file says the repository vendors `flt_regular` unless a real vendored dependency is added.
- [x] C15 Ensure no public file says `RegularPrimesPath.lean` proves `flt_regular` locally.
- [x] C16 Ensure every machine-checked claim names a theorem, module, and source project.

## D. Local Build Validation

- [x] D01 Decide whether validation status dated `2026-04-24` is `pass`, `historical pass`, or `fail`.
- [x] D02 Rerun `bash THM-M-0387/run_local_validation.sh` in the validation environment dated `2026-04-24`.
- [x] D03 Record the absolute rerun date in `build_validation.md`.
- [x] D04 Record the exact command used for the rerun in `build_validation.md`.
- [x] D05 Record the exact success or failure outcome in `build_validation.md`.
- [x] D06 If validation fails because `lake` is missing, record that failure explicitly.
- [x] D07 If validation fails because a Lean toolchain download times out, record that failure explicitly.
- [x] D08 If validation passes, record the Lean version.
- [x] D09 If validation passes, record the Lake version.
- [x] D10 If validation passes, record the toolchain name.
- [x] D11 If validation passes, record which modules were built.
- [x] D12 If validation passes, record that `FermatLastTheorem_Sample.lean` file-check passed.
- [x] D13 If validation is historical only, label the previous successful build as historical rather than a dated reproducible pass.
- [x] D14 Ensure `build_validation.md` does not claim dated reproducibility after a dated failure.
- [x] D15 Ensure `run_local_validation.sh` invocation style is consistent with docs.
- [x] D16 Either make `run_local_validation.sh` executable or document `bash THM-M-0387/run_local_validation.sh` everywhere.
- [x] D17 Ensure `README.md` validation instructions match `build_validation.md`.
- [x] D18 Ensure `full_study.md` validation discussion matches `build_validation.md`.
- [x] D19 Ensure validation docs mention custom toolchain prerequisites.
- [x] D20 Ensure validation docs mention that `.lake/` and local caches are not tracked artifacts.

## E. Human-Readable Expansion Surfaces

- [x] E01 Confirm `eligibles/n4_proof_process.md` is the only public merge target for `FLT-HR-001` through `FLT-HR-007`.
- [x] E02 Confirm `eligibles/regular_primes_proof_process.md` is the only public merge target for `FLT-HR-008` through `FLT-HR-018`.
- [x] E03 Confirm `eligibles/n3_proof_process.md` remains a separate readable branch and is not part of the 18-unit automatic expansion gate.
- [x] E04 Ensure no public `human_steps/` directory is referenced as a completion surface.
- [x] E05 Ensure no `.cron/results/*` runtime path is referenced as a public archive target.
- [x] E06 Ensure no automation clone path is referenced as a public archive target.
- [x] E07 Ensure each eligible main稿 contains only stable static wording after merge-back.
- [x] E08 Remove process-only wording such as `本轮 worker` from public main稿.
- [x] E09 Remove process-only wording such as `slot` from public main稿 unless it is clearly historical/private context and not a public interface.
- [x] E10 Remove process-only wording such as `下一轮继续` from public main稿.
- [x] E11 Remove process-only wording such as `当前 frontier` from public main稿.
- [x] E12 Ensure reader-facing aliases are explicitly marked as aliases when used.
- [x] E13 Ensure aliases do not create a second canonical node system.
- [x] E14 Ensure canonical package names match across `machine_checked_audit.md`, `process_audit.md`, and `eligibles/`.
- [x] E15 Ensure canonical high-risk leaf names match across `machine_checked_audit.md`, `process_audit.md`, and `eligibles/`.
- [x] E16 Ensure every appendix-style merged execution unit has a stable heading matching its `FLT-HR-*` id.
- [x] E17 Ensure every appendix-style merged execution unit states its local scope boundary.
- [x] E18 Ensure every appendix-style merged execution unit states what it does not prove.
- [x] E19 Ensure every appendix-style merged execution unit names its machine or upstream hook.
- [x] E20 Ensure every appendix-style merged execution unit includes a local budget ledger.

## F. `n = 4` Package Review

- [x] F01 Verify `FLT-HR-001` has a public section headed `n = 4 / bridge packaging`.
- [x] F02 Verify `FLT-HR-001` names hooks `Fermat42`, `not_fermat_42`, and `fermatLastTheoremFour`.
- [x] F03 Verify `FLT-HR-001` includes a local ledger with total steps `<=100`.
- [x] F04 Verify `FLT-HR-002` has a public section headed `n = 4 / minimal normalization`.
- [x] F05 Verify `FLT-HR-002` names hooks `exists_minimal`, `coprime_of_minimal`, and `exists_pos_odd_minimal`.
- [x] F06 Verify `FLT-HR-002` includes a local ledger with total steps `<=100`.
- [x] F07 Verify `FLT-HR-003` has a public section headed `n = 4 / first triple classification`.
- [x] F08 Verify `FLT-HR-003` names hook `PythagoreanTriple.coprime_classification'`.
- [x] F09 Verify `FLT-HR-003` includes a local ledger with total steps `<=100`.
- [x] F10 Verify `FLT-HR-004` has a public section headed `n = 4 / second triple classification`.
- [x] F11 Verify `FLT-HR-004` names hook `PythagoreanTriple.coprime_classification'` for `(a, n, m)`.
- [x] F12 Verify `FLT-HR-004` includes a local ledger with total steps `<=100`.
- [x] F13 Verify `FLT-HR-005` has a public section headed `n = 4 / coprimality bridge`.
- [x] F14 Verify `FLT-HR-005` names hooks `Int.isCoprime_of_sq_sum` and `Int.isCoprime_of_sq_sum'`.
- [x] F15 Verify `FLT-HR-005` includes a local ledger with total steps `<=100`.
- [x] F16 Verify `FLT-HR-006` has a public section headed `n = 4 / square extraction and sign cleanup`.
- [x] F17 Verify `FLT-HR-006` names hook `Int.sq_of_gcd_eq_one` and the sign-cleanup obligations.
- [x] F18 Verify `FLT-HR-006` includes a local ledger with total steps `<=100`.
- [x] F19 Verify `FLT-HR-007` has a public section headed `n = 4 / smaller-solution construction and size comparison`.
- [x] F20 Verify `FLT-HR-007` names hooks or internal proof objects `hh`, `hic`, and `hic'` in `Fermat42.not_minimal`.
- [x] F21 Verify `FLT-HR-007` includes a local ledger with total steps `<=100`.
- [x] F22 Verify the `n = 4` status ledger lists all 7 packages exactly once.
- [x] F23 Verify the `n = 4` status ledger agrees with the authoritative checklist.
- [x] F24 Verify the `n = 4` high-risk leaf set uses the canonical names from `Docs/Blueprint_Guidelines.md`.

## G. Regular Primes Package Review

- [x] G01 Verify `FLT-HR-008` has a public section headed `regular primes / setup and regularity engine`.
- [x] G02 Verify `FLT-HR-008` names hooks `IsRegularPrime` and `isPrincipal_of_isPrincipal_pow_of_coprime`.
- [x] G03 Verify `FLT-HR-008` includes a local ledger with total steps `<=100`.
- [x] G04 Verify `FLT-HR-009` has a public section headed `regular primes / MayAssume primitive reduction`.
- [x] G05 Verify `FLT-HR-009` names hooks `MayAssume.coprime`, `MayAssume.p_dvd_c_of_ab_of_anegc`, and `a_not_cong_b`.
- [x] G06 Verify `FLT-HR-009` includes a local ledger with total steps `<=100`.
- [x] G07 Verify `FLT-HR-010` has a public section headed `regular primes / Case I outer statement`.
- [x] G08 Verify `FLT-HR-010` names hooks `CaseI.SlightlyEasier`, `CaseI.Statement`, and `CaseI.may_assume`.
- [x] G09 Verify `FLT-HR-010` includes a local ledger with total steps `<=100`.
- [x] G10 Verify `FLT-HR-011` has a public section headed `regular primes / Case I ideal extraction`.
- [x] G11 Verify `FLT-HR-011` names hooks `ab_coprime`, `auxf'`, `auxf`, and `exists_ideal`.
- [x] G12 Verify `FLT-HR-011` includes a local ledger with total steps `<=100`.
- [x] G13 Verify `FLT-HR-012` has a public section headed `regular primes / Case I principalization`.
- [x] G14 Verify `FLT-HR-012` names hooks `is_principal_aux` and `is_principal`.
- [x] G15 Verify `FLT-HR-012` includes a local ledger with total steps `<=100`.
- [x] G16 Verify `FLT-HR-013` has a public section headed `regular primes / Case I element recovery and close`.
- [x] G17 Verify `FLT-HR-013` names hooks `ex_fin_div`, `caseI_easier`, and `caseI`.
- [x] G18 Verify `FLT-HR-013` includes a local ledger with total steps `<=100`.
- [x] G19 Verify `FLT-HR-014` has a public section headed `regular primes / Case II pi-language reduction`.
- [x] G20 Verify `FLT-HR-014` names hooks `zeta_sub_one_dvd`, `span_pow_add_pow_eq`, `div_one_sub_zeta_mem`, and `div_zeta_sub_one_Bijective`.
- [x] G21 Verify `FLT-HR-014` includes a local ledger with total steps `<=100`.
- [x] G22 Verify `FLT-HR-015` has a public section headed `regular primes / Case II ideal-factor layer`.
- [x] G23 Verify `FLT-HR-015` names hooks `prod_c`, `exists_ideal_pow_eq_c`, `root_div_zeta_sub_one_dvd_gcd_spec`, and `c_div_principal`.
- [x] G24 Verify `FLT-HR-015` includes a local ledger with total steps `<=100`.
- [x] G25 Verify `FLT-HR-016` has a public section headed `regular primes / Case II distinguished root`.
- [x] G26 Verify `FLT-HR-016` names hooks `zeta_sub_one_dvd_root_spec`, `p_dvd_c_iff`, `p_dvd_a_iff`, `p_pow_dvd_c_eta_zero`, and `p_pow_dvd_a_eta_zero`.
- [x] G27 Verify `FLT-HR-016` includes a local ledger with total steps `<=100`.
- [x] G28 Verify `FLT-HR-017` has a public section headed `regular primes / Case II descent core`.
- [x] G29 Verify `FLT-HR-017` names hooks `exists_solution` and `exists_solution'`.
- [x] G30 Verify `FLT-HR-017` includes a local ledger with total steps `<=100`.
- [x] G31 Verify `FLT-HR-018` has a public section headed `regular primes / Case II close and merge`.
- [x] G32 Verify `FLT-HR-018` names hooks `not_exists_solution`, `not_exists_solution'`, `not_exists_Int_solution`, `not_exists_Int_solution'`, `caseII`, and `flt_regular`.
- [x] G33 Verify `FLT-HR-018` includes a local ledger with total steps `<=100`.
- [x] G34 Verify the regular primes status ledger lists all 11 packages exactly once.
- [x] G35 Verify the regular primes status ledger agrees with the authoritative checklist.
- [x] G36 Verify the regular primes high-risk leaf set uses the canonical names from `Docs/Blueprint_Guidelines.md`.

## H. Cross-File Consistency

- [x] H01 Compare all `n = 4` package names across `full_study.md`, `machine_checked_audit.md`, `process_audit.md`, and `eligibles/n4_proof_process.md`.
- [x] H02 Compare all regular-primes package names across `full_study.md`, `machine_checked_audit.md`, `process_audit.md`, and `eligibles/regular_primes_proof_process.md`.
- [x] H03 Compare all canonical high-risk leaf names across `Docs/Blueprint_Guidelines.md`, `machine_checked_audit.md`, `process_audit.md`, and `eligibles/`.
- [x] H04 Ensure `n = 3` is not over-expanded into trivial arithmetic leaves against the stated guideline.
- [x] H05 Ensure `n = 3` still has readable proof-process coverage in `eligibles/n3_proof_process.md`.
- [x] H06 Ensure `README.md` navigation includes the new fix blueprint if retained as a public planning artifact.
- [x] H07 Ensure `meta.json` `folder_contract` includes the fix blueprint only if it becomes a permanent contract file.
- [x] H08 Ensure all links in `THM-M-0387/README.md` resolve to existing tracked files.
- [x] H09 Ensure all links in `THM-M-0387/full_study.md` resolve to existing tracked files.
- [x] H10 Ensure all links in `THM-M-0387/eligibles/README.md` resolve to existing tracked files.
- [x] H11 Ensure no public file references `.cron/automation_repo*` as stable material.
- [x] H12 Ensure no public file references private runtime ledgers as stable material.
- [x] H13 Ensure all public status tables use the same branch names: `n = 4`, `n = 3`, `regular primes`.
- [x] H14 Ensure all public status tables use the same theorem id: `THM-M-0387`.
- [x] H15 Ensure all public material uses absolute dates for research or validation claims.
- [x] H16 Ensure all public material avoids vague temporal words such as `current` (review date `2026-04-24`) when not paired with an absolute date.

## I. Source and Primary Evidence

- [x] I01 Identify the exact mathlib revision used by the local Lean project.
- [x] I02 Identify the exact mathlib modules for `FermatLastTheoremFor`, `FermatLastTheorem`, and reduction lemmas.
- [x] I03 Identify the exact mathlib module for `fermatLastTheoremFour`.
- [x] I04 Identify the exact mathlib module for `fermatLastTheoremThree`.
- [x] I05 Identify the exact upstream `flt-regular` repository or source reference used for regular primes claims.
- [x] I06 Identify the exact upstream modules realizing regular primes setup.
- [x] I07 Identify the exact upstream modules realizing MayAssume.
- [x] I08 Identify the exact upstream modules realizing Case I.
- [x] I09 Identify the exact upstream modules realizing Case II.
- [x] I10 Identify the exact upstream terminal theorem declaration for `flt_regular`.
- [x] I11 Record whether upstream `flt-regular` is pinned by commit, release, or only by module-name reference.
- [x] I12 If upstream `flt-regular` is not pinned, add a TODO to pin it before making stronger reproducibility claims.

## J. Final Release Gate

- [x] J01 Run a grep check for `sorry`, `admit`, `axiom`, `constant`, and `opaque` in the THM-M-0387 Lean target files.
- [x] J02 Run the local validation script or record why it cannot run on an absolute date.
- [x] J03 Run a consistency grep for `missing`, `unchecked`, `open`, and stale progress totals.
- [x] J04 Run a consistency grep for `本轮 worker`, `slot`, `下一轮继续`, `当前 frontier`, and `.cron/results` in public files.
- [x] J05 Run a consistency grep for regular-primes overclaim wording.
- [x] J06 Confirm every completed checklist item has a machine anchor.
- [x] J07 Confirm every completed checklist item has a public merge target.
- [x] J08 Confirm every completed checklist item has an independent `<=100` ledger.
- [x] J09 Confirm every completed checklist item has synchronized status in README, full study, audits, and eligible稿.
- [x] J10 Confirm every open checklist item is not described as fully completed elsewhere.
- [x] J11 Confirm `build_validation.md` matches the local validation result dated `2026-04-24`.
- [x] J12 Confirm `meta.json` matches the status boundary dated `2026-04-24`.
- [x] J13 Confirm `README.md` accurately describes the repository as blueprint-first unless full local formal closure has been proven.
- [x] J14 Confirm this v5.5 fix blueprint has an accurate checklist item count.
- [x] J15 Decide whether to archive this v5.5 blueprint as a permanent planning artifact or delete it after fixes are merged.

## K. Post-Worker Lead Reviewer Closeout

These items are intentionally not assigned to the ten execution workers. They run after workers disappear, tmux sessions are gone, and the v5.5 checklist is either complete or ready for final integration review.

- [x] K01 Confirm no v5.5 worker tmux sessions are still running.
- [x] K02 Confirm no `codex exec` process is still running inside `.cron/automation_repo_slot*`.
- [x] K03 Confirm `.cron/`, `.ops/`, logs, worker clones, and runtime state are not staged for commit.
- [ ] K04 Review the final file/folder layout for human readability and remove accidental parallel public surfaces.
- [ ] K05 Decide whether `fix_blueprint_v5_5.md` remains as a permanent planning artifact or is archived/removed after completion.
- [ ] K06 If retained, add a concise link to `THM-M-0387/README.md` without making it compete with `full_study.md`.
- [ ] K07 If removed or archived, ensure README, todo snapshots, and references do not point to a missing blueprint.
- [ ] K08 Normalize headings, section order, and table style across `full_study.md`, audits, and eligible稿.
- [ ] K09 Confirm `THM-M-0387/` contains only durable public materials, not execution scratch files.
- [ ] K10 Confirm `eligibles/` contains only the three stable reader-facing proof-process documents plus its README.
- [ ] K11 Confirm validation evidence is in `build_validation.md`, not scattered through logs or chat-derived notes.
- [ ] K12 Confirm machine-boundary evidence is in `machine_checked_audit.md`, not duplicated inconsistently elsewhere.
- [ ] K13 Confirm process-tree evidence is in `process_audit.md`, not only in eligible narrative prose.
- [ ] K14 Confirm `full_study.md` remains the authoritative high-level study and progress surface.
- [ ] K15 Confirm all public links are relative, stable repository paths.
- [ ] K16 Confirm no absolute automation-clone path remains in public tracked files.
- [ ] K17 Run the final grep suite listed in section J again after all worker edits are integrated.
- [ ] K18 Run the final local validation command or record the blocking reason with an absolute date.
- [ ] K19 Refresh the total checklist count in this file if section K remains part of the tracked blueprint.
- [ ] K20 Only after K01-K19, remove the v5.5 scheduler via `.cron/bin/cleanup_cron.sh` or the matching launchd cleanup path.
