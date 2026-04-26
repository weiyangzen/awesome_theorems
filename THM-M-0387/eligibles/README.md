# THM-M-0387 Eligible Derivatives

本目录放的是 `THM-M-0387` 的衍生展开稿。

它们不是新的 formal artifact，而是把 `n = 4`、`n = 3` 与 `regular primes` 三个分支，
分别改写成“研究生层次可连续阅读”的证明过程说明稿；其中 regular primes 的定理闭合来自上游 `flt-regular`，
本仓库保留 anchor-only 的 statement/module/theorem-name 记录，不 vendoring 证明本体。

这三份文档的定位是：

1. 不混写。
2. 不只列 theorem 名。
3. 尽量把 paper proof、formal object、descent / reduction 结构三者对齐。

## 文件列表

- `n4_proof_process.md`
  `n = 4` 的人类可读证明过程。
- `n3_proof_process.md`
  `n = 3` 的人类可读证明过程。
- `regular_primes_proof_process.md`
  `regular primes` 分支的人类可读证明过程。

截至 `2026-04-24`，`n = 4` 与 `regular primes` 的 execution unit 已有 `18/18` 个公开归档面达到 `completed` / `Completion Gate = passed`；
`FLT-HR-018` 的 `Human-Readable Expansion` 与 `Local Budget Ledger` 已合并进 `regular_primes_proof_process.md`，
不再单独列出一个 `human_steps/` 子目录。

## execution unit 合并边界

- `FLT-HR-001` 到 `FLT-HR-007` 的唯一公开合并目标是 `eligibles/n4_proof_process.md`。
- `FLT-HR-008` 到 `FLT-HR-018` 的唯一公开合并目标是 `eligibles/regular_primes_proof_process.md`。
- `eligibles/n3_proof_process.md` 保持为单独可读分支，不属于上述 `18` 个 execution unit 的自动展开闸门。
- 可读标题、中文说明和 reader-facing alias 只解释 canonical node；它们不创建第二套 canonical node system。跨文件同步时，canonical package 与 canonical high-risk leaf 名称以 `machine_checked_audit.md`、`process_audit.md` 和本目录主稿中反引号标出的 canonical 名称为准。
- execution unit 状态只使用 `completed` / `Completion Gate = passed` 或 `missing/open` / `Completion Gate = missing/not passed`；
  theorem-level `checked` anchor 不等于公开归档面的 completion gate。
- completion surface 与公开归档只使用本目录中的 tracked Markdown 主稿；`human_steps/` 不是 completion surface，`.cron/results/*` 不是公开归档目标，自动化工作副本路径也不是公开归档目标。

## appendix-style unit hook 与 budget 索引

下表只索引公开合并面的机器 / 上游 hook 与局部预算 ledger；具体证明说明以对应主稿中的稳定 `FLT-HR-*` heading 为准。

| unit | merged public file | named machine or upstream hook | local budget ledger |
|---|---|---|---|
| `FLT-HR-001` | `n4_proof_process.md` | `Fermat42`, `not_fermat_42`, `fermatLastTheoremFour`, repo-local anchor `FLT4Path.lean` / `flt4Path` | `Local Budget Ledger`, `14` steps |
| `FLT-HR-002` | `n4_proof_process.md` | `Fermat42.exists_minimal`, `Fermat42.coprime_of_minimal`, `Fermat42.exists_pos_odd_minimal` | `Local Budget Ledger`, `16` steps |
| `FLT-HR-003` | `n4_proof_process.md` | `PythagoreanTriple.coprime_classification`, `PythagoreanTriple.coprime_classification'` | `Local Budget Ledger`, `33` steps |
| `FLT-HR-004` | `n4_proof_process.md` | `PythagoreanTriple.coprime_classification'` for `(a, n, m)`, with `htt`, `h3`, `ha2`, `h4` as local API inputs | `Local Budget Ledger`, `13` steps |
| `FLT-HR-005` | `n4_proof_process.md` | `Int.isCoprime_of_sq_sum`, `Int.isCoprime_of_sq_sum'` | `Local Budget Ledger`, `12` steps |
| `FLT-HR-006` | `n4_proof_process.md` | `Int.sq_of_gcd_eq_one` over `(m, r*s)`, `(r*s, m)`, and `(r, s)` | `Local Budget Ledger`, `25` steps |
| `FLT-HR-007` | `n4_proof_process.md` | `Fermat42.not_minimal`, `Minimal`, `Int.natAbs_le_self_sq`, `Int.le_self_sq` | `Local Budget Ledger`, `19` steps |
| `FLT-HR-008` | `regular_primes_proof_process.md` | upstream `flt-regular`: `IsRegularPrime`, `isPrincipal_of_isPrincipal_pow_of_coprime`; repo-local anchor-only `RegularPrimesPath.lean` / `flt_regular` | `Local Budget Ledger`, `13` steps |
| `FLT-HR-009` | `regular_primes_proof_process.md` | upstream `flt-regular`: `MayAssume.coprime`, `MayAssume.p_dvd_c_of_ab_of_anegc`, `a_not_cong_b` | `Local Budget Ledger`, `37` steps |
| `FLT-HR-010` | `regular_primes_proof_process.md` | upstream `flt-regular`: `CaseI.SlightlyEasier`, `CaseI.Statement`, `CaseI.may_assume` | `Local Budget Ledger`, `21` steps |
| `FLT-HR-011` | `regular_primes_proof_process.md` | upstream `flt-regular`: `irreducible_aux`, `irreducible`, `exists_ideal` | `Local Budget Ledger`, `21` steps |
| `FLT-HR-012` | `regular_primes_proof_process.md` | upstream `flt-regular`: `is_principal_aux`, `is_principal` | `Local Budget Ledger`, `13` steps |
| `FLT-HR-013` | `regular_primes_proof_process.md` | upstream `flt-regular`: `ex_fin_div`, `caseI_easier`, `caseI` | `Local Budget Ledger`, `25` steps |
| `FLT-HR-014` | `regular_primes_proof_process.md` | upstream `flt-regular`: `caseII_statement`, `caseII` π-language entrance hooks | `Local Budget Ledger`, `18` steps |
| `FLT-HR-015` | `regular_primes_proof_process.md` | upstream `flt-regular`: `prod_c`, `exists_ideal_pow_eq_c`, `root_div_zeta_sub_one_dvd_gcd_spec`, `c_div_principal` | `Local Budget Ledger`, `25` steps |
| `FLT-HR-016` | `regular_primes_proof_process.md` | upstream `flt-regular`: distinguished-root and `find_root` / `find_root'` hooks recorded under the Case II root layer | `Local Budget Ledger`, `20` steps |
| `FLT-HR-017` | `regular_primes_proof_process.md` | upstream `flt-regular`: `exists_solution`, `exists_solution'`, three-root descent and Kummer-normalization hooks | `Local Budget Ledger`, `35` steps |
| `FLT-HR-018` | `regular_primes_proof_process.md` | upstream `flt-regular`: `not_exists_solution'`, `not_exists_solution`, `caseII` | `Local Budget Ledger`, `34` steps |

Regular primes 的边界在每一行保持同一口径：upstream theorem closure 为 yes；repo-local vendored theorem closure 为 no、anchor-only；repo-local anchor-only statement/module/theorem-name record 为 yes。

## 与主材料的关系

- 若你要看总入口，先读 [`../README.md`](../README.md)。
- 若你要看 theorem-level 审计，读 [`../machine_checked_audit.md`](../machine_checked_audit.md)。
- 若你要看 process-level 审计总表，读 [`../process_audit.md`](../process_audit.md)。
- 若你要看长篇总研究文档，读 [`../full_study.md`](../full_study.md)。

本目录的三份稿子，正好对应：

- `process_audit.md` 里的 `n = 4` 分支
- `process_audit.md` 里的 `n = 3` 分支
- `process_audit.md` 里的 `regular primes` 分支

只是这里把它们分别展开成完整可读稿，不再压缩成一张表。
