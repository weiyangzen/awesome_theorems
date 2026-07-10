#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

from collections import Counter, OrderedDict
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_FILE = ROOT / "Docs" / "Stage1_Blueprint.md"
APPLICABLE_FILE = ROOT / "Docs" / "Stage1_Blueprint_Applicable_Theorems.md"
TARGET_MANIFEST_FILE = ROOT / "Docs" / "Stage1_Targets_rev-5.6.json"
STANDARD_FILE = ROOT / "Docs" / "Stage1_Blueprint_rev-5.6.md"
TOP_N = 300

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_stage0_blueprint as stage0  # noqa: E402


@dataclass(frozen=True)
class Profile:
    key: str
    weight: int
    lean_basis: str
    theorem_tree: str
    blockers: str
    partial_scope: str


PROFILES: list[tuple[tuple[str, ...], Profile]] = [
    (
        ("数论 / 代数数论", "数论 / 丢番图方程"),
        Profile(
            key="arithmetic_geometry_number_theory",
            weight=130,
            lean_basis="Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。",
            theorem_tree="定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。",
            blockers="数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。",
            partial_scope="优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。",
        ),
    ),
    (
        ("几何学 / 代数几何",),
        Profile(
            key="algebraic_geometry",
            weight=128,
            lean_basis="Lean 4 + mathlib 的 scheme、sheaf、category theory、commutative algebra、topology API。",
            theorem_tree="对象/态射定义 -> 局部化/覆盖 -> sheaf/cohomology 层 -> base change / descent -> 主定理 branch。",
            blockers="scheme/cohomology/descent API 深，许多论文级标准事实需要拆成可命名 lemma；优先锁定已在 mathlib 存在的局部结构。",
            partial_scope="先验证 statement shape、核心对象定义、局部性质稳定性、特殊 base/ring 情形，以及可由 mathlib import 直接检查的 wrapper。",
        ),
    ),
    (
        ("代数学 / 同调代数", "代数学 / 范畴论"),
        Profile(
            key="homological_category_theory",
            weight=124,
            lean_basis="Lean 4 + mathlib 的 category theory、abelian category、chain complex、homological algebra API。",
            theorem_tree="范畴/函子前提 -> exactness / derived object -> naturality square -> spectral/long exact sequence branch -> terminal statement。",
            blockers="universe、simp-normal-form、自然变换与 exactness API 容易导致证明项复杂；必须保持 theorem names 与 mathlib API 对齐。",
            partial_scope="先做 category-level statement、自然性 square、短正合/长正合子结果、已存在 API 的 wrapper 与 theorem-tree ledger。",
        ),
    ),
    (
        ("微分方程 / 偏微分方程",),
        Profile(
            key="partial_differential_equations",
            weight=116,
            lean_basis="Lean 4 + mathlib 的 analysis、normed spaces、measure/integration、weak derivative 或 distribution-adjacent definitions。",
            theorem_tree="函数空间与边界条件 -> weak/classical formulation bridge -> energy estimate / compactness -> regularity / existence branch -> theorem wrapper。",
            blockers="PDE 基础设施在 Lean 4 中通常是 formalization_debt；必须把可验证范围限制到 statement、functional-analytic lemma、energy estimate 或特殊情形。",
            partial_scope="优先验证精确定义、弱形式陈述、基础估计、ODE/有限维近似、已在 analysis API 中可表达的 compactness/continuity 子引理。",
        ),
    ),
    (
        ("概率论与随机过程 / 随机过程", "概率论与随机过程 / 概率论基础"),
        Profile(
            key="probability_stochastic_processes",
            weight=112,
            lean_basis="Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。",
            theorem_tree="概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。",
            blockers="filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。",
            partial_scope="先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。",
        ),
    ),
    (
        ("其他重要领域 / 数学物理",),
        Profile(
            key="mathematical_physics",
            weight=110,
            lean_basis="Lean 4 + mathlib 的 analysis、linear operators、Hilbert spaces、measure theory、PDE/geometry 接口。",
            theorem_tree="公理化模型 -> 函数空间/算子前提 -> 谱/能量/变分结构 -> 关键估计 -> theorem wrapper。",
            blockers="必须把物理语言重写成数学命题；非公理化实验事实不进入 proof slot。",
            partial_scope="先验证公理化 statement、算子/空间定义、谱或变分子引理、特殊参数情形。",
        ),
    ),
    (
        ("拓扑学 / 代数拓扑", "拓扑学 / 微分拓扑"),
        Profile(
            key="topology_algebraic_differential",
            weight=106,
            lean_basis="Lean 4 + mathlib 的 topology、homotopy-adjacent API、manifold、homology/cohomology 相关结构。",
            theorem_tree="空间/流形前提 -> 不变量定义 -> functoriality/naturality -> exact sequence / obstruction branch -> 主定理。",
            blockers="同伦、谱序列、transversality、cobordism 等基础设施可能缺失；需优先做可检查的不变量与特殊情形。",
            partial_scope="先验证空间/流形对象、基本不变量、functoriality、低维/简单空间特例、已存在 mathlib theorem wrapper。",
        ),
    ),
    (
        ("几何学 / 微分几何",),
        Profile(
            key="differential_geometry",
            weight=104,
            lean_basis="Lean 4 + mathlib 的 manifold、smooth map、tensor/calculus、topology、analysis API。",
            theorem_tree="流形/丛/联络定义 -> 曲率或张量恒等式 -> 局部坐标 branch -> 全局化/compactness -> theorem wrapper。",
            blockers="坐标计算、smoothness automation、tensor notation 和 global/local bridge 是主要 formalization_debt。",
            partial_scope="先验证 statement、局部坐标 lemma、基础曲率/张量恒等式、低维或紧流形特殊情形。",
        ),
    ),
    (
        ("数理逻辑 / 证明论", "数理逻辑 / 模型论", "数理逻辑 / 集合论"),
        Profile(
            key="logic_model_set_proof_theory",
            weight=98,
            lean_basis="Lean 4 可编码语法、证明系统、模型语义、集合论对象；mathlib 可支持 order/set/cardinal/model-theoretic fragments。",
            theorem_tree="语法编码 -> 语义/证明关系 -> soundness/completeness/cut/compactness branch -> 主结果。",
            blockers="元理论编码、Gödel numbering、模型存在性与 universe 管理复杂；需要先定义可执行 syntax 与 proof relation。",
            partial_scope="先验证语法与推导系统、soundness 子结论、有限 fragment、已形式化 meta-theory wrapper。",
        ),
    ),
    (
        ("分析学 / 泛函分析", "分析学 / 调和分析"),
        Profile(
            key="functional_harmonic_analysis",
            weight=94,
            lean_basis="Lean 4 + mathlib 的 normed spaces、measure/integration、topology、operator theory API。",
            theorem_tree="空间/算子前提 -> boundedness/compactness -> convergence/duality -> main estimate / representation theorem。",
            blockers="Bochner/Pettis integral、distribution、Fourier analysis、operator spectrum 等 API 可能不完整。",
            partial_scope="先验证 normed-space statement、bounded linear map lemma、积分/极限交换条件、特殊空间情形。",
        ),
    ),
    (
        ("数论 / 解析数论",),
        Profile(
            key="analytic_number_theory",
            weight=92,
            lean_basis="Lean 4 + mathlib 的 number theory、analysis、asymptotics、series/integral API。",
            theorem_tree="算术函数定义 -> analytic transform / estimate -> asymptotic branch -> 主结论。",
            blockers="复杂分析、渐近估计、筛法、L-function API 是主要 formalization_debt。",
            partial_scope="先验证 statement、基础算术函数、有限和恒等式、渐近符号接口与已知 mathlib wrapper。",
        ),
    ),
    (
        ("其他重要领域 / 动力系统",),
        Profile(
            key="dynamical_systems",
            weight=88,
            lean_basis="Lean 4 + mathlib 的 topology、measure theory、analysis、ODE-adjacent API。",
            theorem_tree="phase space -> map/flow -> invariant/ergodic property -> stability/recurrence branch -> 主结论。",
            blockers="ergodic theory、smooth flow、hyperbolicity API 需要大量基础设施；优先离散时间与 compact metric spaces。",
            partial_scope="先验证 map/flow definitions、invariance、固定点/周期点特例、有限或紧空间情形。",
        ),
    ),
    (
        ("微分方程 / 常微分方程",),
        Profile(
            key="ordinary_differential_equations",
            weight=82,
            lean_basis="Lean 4 + mathlib 的 calculus、normed spaces、analysis、ODE 基础接口。",
            theorem_tree="向量场与初值 -> local existence/uniqueness branch -> continuation/stability -> 主结论。",
            blockers="ODE 通用库仍需审计；可先做 statement、线性系统、Lipschitz 条件和基础估计。",
            partial_scope="先验证初值问题陈述、Lipschitz/continuity 条件、线性/有限维特例、解的唯一性骨架。",
        ),
    ),
]

DEFAULT_PROFILE = Profile(
    key="general_hard_mathematics",
    weight=60,
    lean_basis="Lean 4 + mathlib；具体 API 需要 Stage1 anchor audit 后锁定。",
    theorem_tree="定义规整 -> 关键引理 -> case split / induction / compactness branch -> terminal theorem wrapper。",
    blockers="需先完成 mathlib / external Lean 4 source audit，避免把源文档的 `已验证` 误当成本仓库 completed。",
    partial_scope="先验证 statement、基础定义、可由 mathlib 直接表达的子引理、以及 repo-local wrapper skeleton。",
)


NAME_WEIGHTS = {
    "主猜想": 28,
    "Langlands": 28,
    "朗兰兹": 28,
    "Wiles": 26,
    "怀尔斯": 26,
    "费马": 26,
    "Hodge": 25,
    "霍奇": 25,
    "Riemann": 24,
    "黎曼": 24,
    "谱序列": 22,
    "Grothendieck": 22,
    "格罗滕迪克": 22,
    "指数定理": 21,
    "Atiyah": 21,
    "阿蒂亚": 21,
    "Poincare": 20,
    "庞加莱": 20,
    "Hasse": 18,
    "哈塞": 18,
    "Chebotarev": 18,
    "切博塔": 18,
    "密度": 12,
    "存在性": 10,
    "正则性": 10,
    "紧性": 8,
    "对偶": 8,
    "嵌入": 7,
    "不动点": 6,
}

STATUS_WEIGHTS = {
    "partial": 35,
    "closed": 18,
    "verifiable": 12,
    "unknown": 0,
}

EXCLUDED_BUCKETS = {"open", "independent", "refuted", "undecidable"}
CONJECTURE_MARKERS = ("猜想", "问题", "假设")
ACCEPTED_THEOREM_STATUSES = ("已验证", "已证明", "已解决", "准多项式时间解决")


def load_stage0_items() -> tuple[list[stage0.Theorem], int]:
    items: list[stage0.Theorem] = []
    for source in stage0.LIST_STYLE_SOURCES:
        items.extend(
            stage0.parse_list_style_source(
                path=source["path"],
                discipline=source["discipline"],
                ignore_h2=source["ignore_h2"],
            )
        )
    items.extend(
        stage0.parse_table_style_source(
            path=stage0.TABLE_STYLE_SOURCE["path"],
            discipline=stage0.TABLE_STYLE_SOURCE["discipline"],
            ignore_h2=stage0.TABLE_STYLE_SOURCE["ignore_h2"],
        )
    )
    items, removed_count = stage0.dedupe_items(items)
    stage0.assign_ids(items)
    return items, removed_count


def profile_for(item: stage0.Theorem) -> Profile:
    for keys, profile in PROFILES:
        if any(key in item.subcategory for key in keys):
            return profile
    return DEFAULT_PROFILE


def difficulty_score(item: stage0.Theorem) -> int:
    profile = profile_for(item)
    bucket = stage0.formal_status_bucket(item)
    score = profile.weight + STATUS_WEIGHTS.get(bucket, 0)
    text = f"{item.name} {item.statement} {item.subcategory}"
    for keyword, weight in NAME_WEIGHTS.items():
        if keyword in text:
            score += weight
    if item.importance == "高":
        score += 8
    if len(item.statement) > 28:
        score += 5
    if item.name in {"费马大定理"}:
        score += 80
    return score


def is_stage1_eligible(item: stage0.Theorem) -> bool:
    if item.discipline != "数学":
        return False
    bucket = stage0.formal_status_bucket(item)
    if bucket in EXCLUDED_BUCKETS:
        return False
    if "声称证明" in item.formal_status:
        return False
    if any(marker in item.name for marker in CONJECTURE_MARKERS) and not any(
        status in item.formal_status for status in ACCEPTED_THEOREM_STATUSES
    ):
        return False
    if item.importance == "低":
        return False
    profile = profile_for(item)
    return profile.weight >= 60


def blueprint_disposition(item: stage0.Theorem) -> tuple[str, str]:
    """Classify every mathematical record without treating the 300-slot queue as scope."""
    bucket = stage0.formal_status_bucket(item)
    if bucket == "open":
        return "open_problem_audit", "freeze the claim, audit H4, and formalize known barriers/partial results"
    if bucket == "independent":
        return "independence_formalization", "formalize the independence theorem and foundation profile"
    if bucket == "refuted":
        return "counterexample_formalization", "formalize the counterexample or refutation theorem"
    if bucket == "undecidable":
        return "undecidability_formalization", "formalize the undecidability theorem, not a decision procedure"
    if "声称证明" in item.formal_status:
        return "claimed_proof_audit", "audit the claimed proof and keep theorem completion closed"
    if any(marker in item.name for marker in CONJECTURE_MARKERS) and not any(
        status in item.formal_status for status in ACCEPTED_THEOREM_STATUSES
    ):
        return "partial_result_family_audit", "split proved partial results from the still-open canonical claim"
    if item.importance == "低":
        return "low_priority_proof_expansion", "blueprint applies; schedule after higher-value obligations"
    if profile_for(item).weight < 60:
        return "profile_adapter_required", "define a domain/Lean adapter profile before proof expansion"
    return "proof_expansion_eligible", stage1_lane(item)


def select_items(items: list[stage0.Theorem]) -> list[stage0.Theorem]:
    candidates = [item for item in items if is_stage1_eligible(item)]
    ordered = sorted(
        candidates,
        key=lambda item: (
            -difficulty_score(item),
            item.subcategory,
            item.uid,
        ),
    )

    selected: list[stage0.Theorem] = []
    per_subcategory: Counter[str] = Counter()
    soft_cap = 36

    for item in ordered:
        if len(selected) >= TOP_N:
            break
        if per_subcategory[item.subcategory] >= soft_cap:
            continue
        selected.append(item)
        per_subcategory[item.subcategory] += 1

    if len(selected) < TOP_N:
        selected_ids = {item.uid for item in selected}
        for item in ordered:
            if len(selected) >= TOP_N:
                break
            if item.uid in selected_ids:
                continue
            selected.append(item)
            selected_ids.add(item.uid)

    return selected


def stage1_lane(item: stage0.Theorem) -> str:
    bucket = stage0.formal_status_bucket(item)
    score = difficulty_score(item)
    if item.name == "费马大定理":
        return "flagship_deep_formalization_debt"
    if bucket == "partial":
        return "known_partial_branch_deepening"
    if score >= 160:
        return "frontier_deep_formalization_debt"
    if score >= 135:
        return "hard_mathlib_anchor_and_wrapper"
    return "hard_statement_first_partial_verification"


def machine_debt(item: stage0.Theorem) -> str:
    bucket = stage0.formal_status_bucket(item)
    if item.name == "费马大定理":
        return "regular primes 的 `repo_local_integration_debt` 已还清；完整 Wiles/Taylor-Wiles 主线保留 `formalization_debt`；无 active repo-local integration debt。"
    if bucket == "partial":
        return "允许存在 `formalization_debt` 或局部分支数学债；若发现外部 Lean 4 机器证明，必须立即 pin/import/check，不能留下 `repo_local_integration_debt`。"
    return "默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。"


def render_item(index: int, item: stage0.Theorem) -> list[str]:
    profile = profile_for(item)
    bucket = stage0.formal_status_bucket(item)
    score = difficulty_score(item)
    lane = stage1_lane(item)
    lines: list[str] = []
    lines.append(f"### S1-M-{index:03d} / {item.uid} {item.name}")
    lines.append("")
    lines.append("- Stage1 状态: `[ ] open`")
    lines.append(f"- 来源分类: `{item.subcategory}`")
    lines.append(f"- 源文档形式化状态: `{item.formal_status}`；Stage0 bucket: `{bucket}`")
    lines.append(f"- 难度分: `{score}`；Stage1 lane: `{lane}`；profile: `{profile.key}`")
    lines.append(f"- 定理内容: {item.statement}")
    lines.append("- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。")
    lines.append(f"- Lean 4 可部分验证依据: {profile.lean_basis}")
    lines.append(f"- Stage1 partial verification scope: {profile.partial_scope}")
    lines.append(f"- 机器证明债分类: {machine_debt(item)}")
    lines.append("- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。")
    lines.append("- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。")
    lines.append("- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。")
    lines.append(f"- theorem-tree seed: {profile.theorem_tree}")
    lines.append("- proof-package 初始切分:")
    lines.append("  1. statement normalization / notation freeze")
    lines.append("  2. mathlib object model and imported theorem audit")
    lines.append("  3. core reduction or bridge lemma package")
    lines.append("  4. high-risk leaf discovery and `<=100` local ledger")
    lines.append("  5. repo-local wrapper / pinned dependency / local proof-body closure gate")
    lines.append(f"- 形式化阻塞点: {profile.blockers}")
    lines.append("- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。")
    lines.append("- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。")
    lines.append("")
    return lines


def render_blueprint(selected: list[stage0.Theorem], all_items: list[stage0.Theorem], removed_count: int) -> str:
    math_items = [item for item in all_items if item.discipline == "数学"]
    eligible = [item for item in math_items if is_stage1_eligible(item)]
    excluded_by_bucket = Counter(
        stage0.formal_status_bucket(item)
        for item in math_items
        if stage0.formal_status_bucket(item) in EXCLUDED_BUCKETS
    )
    excluded_conjectural = [
        item
        for item in math_items
        if item.discipline == "数学"
        and (
            "声称证明" in item.formal_status
            or (
                any(marker in item.name for marker in CONJECTURE_MARKERS)
                and not any(status in item.formal_status for status in ACCEPTED_THEOREM_STATUSES)
            )
        )
    ]
    selected_subcats = Counter(item.subcategory for item in selected)
    selected_lanes = Counter(stage1_lane(item) for item in selected)

    lines: list[str] = []
    lines.append("# Stage1 Blueprint")
    lines.append("")
    lines.append("## 定位")
    lines.append("")
    lines.append("- 本文件是 Stage1 的 Lean 4-only 数学高难度 proof blueprint。")
    lines.append("- 本文件是生成的候选队列，不是 theorem completion 或 live execution-state authority。")
    lines.append("- 每个条目的规范 authority 是 `Docs/Stage1_Blueprint_rev-5.6.md`；仓库级选取规则服从 `Docs/Blueprint_Guidelines.md`。")
    lines.append("- `THM-M-0387` 是历史兼容 fixture，不是允许硬编码定理、路径、指标、公理或状态的模板。")
    lines.append(f"- rev-5.6 的规范 cover 是 `Docs/Stage1_Blueprint_Applicable_Theorems.md` 中且仅其中的 `{len(eligible)}` 个目标 ID；全部统一为 `L0 / rework_required`。")
    lines.append(f"- 本文件保留的 `{len(selected)}` 个旧 slot 只用于发现历史文件和安排返工；不提供更高 assurance、proof credit 或门禁豁免，其余 `{len(eligible) - len(selected)}` 个目标同样按完整标准执行。")
    lines.append("- 非数学条目、非 Lean4 路线、纯实验/模型检验路线、以及当前主命题仍为 open / independent / refuted / undecidable 的条目不进入本 Stage1 主队列。")
    lines.append("- Stage1 入选只表示进入 Lean 4 proof execution queue，不表示该 theorem 已 repo-local machine-checked。")
    lines.append("")
    lines.append("## 仓库级债务规则")
    lines.append("")
    lines.append("- `mathematical_debt`: 允许存在，用于组织未来猜想或 open-problem 研究；但本 Stage1 主队列默认排除主命题未闭合的条目。")
    lines.append("- `formalization_debt`: 允许存在，是本 Stage1 的主要工作对象；含义是人类证明已知但 Lean 4 kernel closure 尚未完成。")
    lines.append("- `repo_local_integration_debt`: 不允许作为完成态存在；若外部 Lean 4 机器证明存在，必须 pin/import/check 或列为 integration blocker。")
    lines.append("- 完成态只允许 `local_proof_body`、`local_wrapper_upstream_mathlib`、`external_upstream_pinned`；anchor-only URL/theorem name 不计完成。")
    lines.append("")
    lines.append("## 选择算法")
    lines.append("")
    lines.append(f"- Stage0 去重后总条目: `{len(all_items)}`；去重移除: `{removed_count}`。")
    lines.append(f"- Stage0 数学条目: `{len(math_items)}`。")
    lines.append(f"- Stage1 eligible 数学条目: `{len(eligible)}`。")
    lines.append(f"- Stage1 selected 数学条目: `{len(selected)}`。")
    lines.append(f"- 排除的数学债/非主队列 bucket: `{dict(excluded_by_bucket)}`。")
    lines.append(f"- 排除的 conjecture-named / 声称证明条目: `{len(excluded_conjectural)}`。")
    lines.append("- 难度分由领域权重、形式化状态、命名关键词、陈述复杂度与 M0387 flagship override 合成；同一子类设置 soft cap，避免单一领域挤满 300 个 slot。")
    lines.append("- 本选择算法是 execution triage，不是数学价值排名；后续执行可因 primary-source audit 结果调整 lane。")
    lines.append("")
    lines.append("## Stage1 Lane 统计")
    lines.append("")
    lines.append("| lane | count |")
    lines.append("|---|---:|")
    for lane, count in selected_lanes.most_common():
        lines.append(f"| `{lane}` | {count} |")
    lines.append("")
    lines.append("## 入选子类统计")
    lines.append("")
    lines.append("| 子类 | count |")
    lines.append("|---|---:|")
    for subcat, count in selected_subcats.most_common():
        lines.append(f"| {subcat} | {count} |")
    lines.append("")
    lines.append("## Completion Gate")
    lines.append("")
    lines.append("此生成文件中的 `[ ]` 是候选队列标记。条目只有在独立的结构化 instance/state/evidence bundle 中通过下列门禁后，才可在对应 authority 中升级；不得直接编辑本生成文件制造完成态：")
    lines.append("")
    lines.append("1. canonical Lean 4 target 已 elaboration/fingerprint，等价形式有 checked transport。")
    lines.append("2. obligation universe 在观察状态前冻结，typed proof/refinement/provenance/trust/workflow graphs 通过验证。")
    lines.append("3. wrapper、terminal body、axiom/TCB 与全传递依赖来源已解析；unique coverage 不受 alias/refactor 影响。")
    lines.append("4. structured node recipes 在 immutable clean snapshot 中执行，生成 content-addressed receipts。")
    lines.append("5. clean empty-cache cold build、network-denied offline replay、dependency cleanliness/SBOM/license 门禁通过。")
    lines.append("6. 每个 leaf 有 substantive semantic ledger；`<=100` 只决定是否继续拆分。")
    lines.append("7. required H/R 节点有 pinpoint source crosswalk、unique readable anchor 和独立 review。")
    lines.append("8. 第二个独立 runner 和 independently implemented minimal verifier 同意结果。")
    lines.append("9. deterministic evidence bundle 生成 README/meta/audit/status；audit 与 theorem completion 分开决定。")
    lines.append("")
    lines.append("## Selected Theorems")
    lines.append("")

    grouped: OrderedDict[str, list[stage0.Theorem]] = OrderedDict()
    for item in selected:
        grouped.setdefault(item.subcategory, []).append(item)

    index = 1
    for subcategory, items in grouped.items():
        lines.append(f"## {subcategory}")
        lines.append("")
        for item in items:
            lines.extend(render_item(index, item))
            index += 1

    return "\n".join(lines).rstrip() + "\n"


def render_applicable_list(
    selected: list[stage0.Theorem], all_items: list[stage0.Theorem], removed_count: int
) -> str:
    math_items = [item for item in all_items if item.discipline == "数学"]
    eligible = [item for item in math_items if is_stage1_eligible(item)]
    excluded = [item for item in math_items if not is_stage1_eligible(item)]
    excluded_dispositions = Counter(blueprint_disposition(item)[0] for item in excluded)
    target_lanes = Counter(stage1_lane(item) for item in eligible)
    grouped: OrderedDict[str, list[stage0.Theorem]] = OrderedDict()
    for item in selected:
        grouped.setdefault(item.subcategory, []).append(item)
    selected_order = [item for items in grouped.values() for item in items]
    selected_slots = {item.uid: index for index, item in enumerate(selected_order, start=1)}
    selected_ids = set(selected_slots)
    remaining_order = sorted(
        (item for item in eligible if item.uid not in selected_ids),
        key=lambda item: (-difficulty_score(item), item.subcategory, item.uid),
    )
    target_order = selected_order + remaining_order
    target_set_payload = "\n".join(sorted(item.uid for item in eligible)) + "\n"
    target_set_hash = hashlib.sha256(target_set_payload.encode("utf-8")).hexdigest()
    lines = [
        "# Stage1 rev-5.6 Lean 4 Target Theorems",
        "",
        "> Generated from `Docs/tools/generate_stage1_blueprint.py`",
        "> Normative target scope: exactly the 1546 metadata-screened Lean 4 theorem-proof candidates",
        "> The 55 non-eligible mathematical records are not covered by Stage1 rev-5.6",
        "> Inclusion is an intake decision, never a statement-elaboration or proof-completion claim",
        "",
        "## Scope Contract",
        "",
        f"- Stage0 records after deduplication: `{len(all_items)}`; removed duplicates: `{removed_count}`",
        f"- Stage0 mathematical records after deduplication: `{len(math_items)}`",
        f"- **Stage1 rev-5.6 covered target IDs: `{len(eligible)}`**",
        f"- Canonical sorted target-ID set SHA-256: `{target_set_hash}`",
        f"- Stage0 mathematical records outside this standard: `{len(excluded)}`",
        f"- Selected for the bounded priority queue: `{len(selected)}`",
        f"- Covered but not yet selected for that queue: `{len(eligible) - len(selected)}`",
        "",
        f"The table below contains all and only the `{len(eligible)}` covered theorem IDs. The "
        f"`{len(excluded)}` excluded records do not receive a Stage1 rev-5.6 target row, slot, lane, "
        "or conformance status. Open-problem, independence, refutation, undecidability, claimed-proof, "
        "partial-result-family, and low-priority work requires a separate standard or an explicit "
        "re-intake decision.",
        "",
        "## Uniform Rework Baseline",
        "",
        "All 1546 targets start uniformly at `L0 / rework_required`. Historical Stage1 files, slots, "
        "wrappers, source labels, and build results are discovery inputs only: they confer no higher "
        "assurance, accepted task state, proof credit, or exemption from the rev-5.6 gates.",
        "",
        "A target leaves this baseline only through its independent theorem instance state and "
        "accepted evidence receipts. The target manifest never stores a promoted assurance level.",
        "",
        "## Target Lane Summary",
        "",
        "| Lane | Count | Interpretation |",
        "|---|---:|---|",
        f"| `flagship_deep_formalization_debt` | {target_lanes['flagship_deep_formalization_debt']} | existing flagship dossier; deepest expansion |",
        f"| `known_partial_branch_deepening` | {target_lanes['known_partial_branch_deepening']} | partial formal evidence or branch structure worth deepening |",
        f"| `frontier_deep_formalization_debt` | {target_lanes['frontier_deep_formalization_debt']} | high-value, deep theorem architecture; large formalization debt |",
        f"| `hard_mathlib_anchor_and_wrapper` | {target_lanes['hard_mathlib_anchor_and_wrapper']} | start with exact statement and mathlib/external anchor audit |",
        f"| `hard_statement_first_partial_verification` | {target_lanes['hard_statement_first_partial_verification']} | stabilize the formal target before deeper proof planning |",
        "",
        "## Excluded Source Population",
        "",
        "These counts document the Stage0-to-Stage1 boundary only. They are not Stage1 targets.",
        "",
        "| Exclusion reason | Count |",
        "|---|---:|",
    ]
    for disposition, count in excluded_dispositions.most_common():
        lines.append(f"| `{disposition}` | {count} |")
    lines.extend([
        "",
        "## Covered Target List",
        "",
        "Execution rank is total and contiguous across all 1546 targets. Ranks 1-300 preserve the "
        "existing diversity-capped priority queue; ranks 301-1546 order the remaining covered "
        "targets by intake score, category, and stable theorem ID. Rank is scheduling metadata, not "
        "a mathematical-value or proof-completion score.",
        "",
        "| Execution rank | Legacy slot | Theorem ID | Name | Category | Source status (untrusted) | Baseline | Target lane | Intake score |",
        "|---:|---:|---|---|---|---|---|---|---:|",
    ])
    for rank, item in enumerate(target_order, start=1):
        slot = selected_slots.get(item.uid)
        slot_text = f"S1-M-{slot:03d}" if slot is not None else "-"
        display_name = item.name.replace("|", "\\|")
        formal_status = item.formal_status.replace("|", "\\|")
        lines.append(
            f"| {rank} | {slot_text} | `{item.uid}` | {display_name} | {item.subcategory} | "
            f"{formal_status} | `L0 / rework_required` | `{stage1_lane(item)}` | {difficulty_score(item)} |"
        )
    return "\n".join(lines).rstrip() + "\n"


def build_target_manifest(
    selected: list[stage0.Theorem], all_items: list[stage0.Theorem], removed_count: int
) -> dict[str, object]:
    """Build the machine authority consumed by the Stage1 execution skill."""
    math_items = [item for item in all_items if item.discipline == "数学"]
    eligible = [item for item in math_items if is_stage1_eligible(item)]
    excluded = [item for item in math_items if not is_stage1_eligible(item)]
    grouped: OrderedDict[str, list[stage0.Theorem]] = OrderedDict()
    for item in selected:
        grouped.setdefault(item.subcategory, []).append(item)
    selected_order = [item for items in grouped.values() for item in items]
    selected_slots = {item.uid: index for index, item in enumerate(selected_order, start=1)}
    selected_ids = set(selected_slots)
    remaining_order = sorted(
        (item for item in eligible if item.uid not in selected_ids),
        key=lambda item: (-difficulty_score(item), item.subcategory, item.uid),
    )
    target_order = selected_order + remaining_order
    target_set_payload = "\n".join(sorted(item.uid for item in eligible)) + "\n"
    target_set_hash = hashlib.sha256(target_set_payload.encode("utf-8")).hexdigest()
    excluded_dispositions = Counter(blueprint_disposition(item)[0] for item in excluded)
    targets: list[dict[str, object]] = []
    for rank, item in enumerate(target_order, start=1):
        slot = selected_slots.get(item.uid)
        targets.append(
            {
                "execution_rank": rank,
                "legacy_priority_slot": f"S1-M-{slot:03d}" if slot is not None else None,
                "theorem_id": item.uid,
                "name": item.name,
                "category": item.subcategory,
                "source_status_untrusted": item.formal_status,
                "baseline": "L0",
                "rework_required": True,
                "legacy_artifacts_accepted": False,
                "target_lane": stage1_lane(item),
                "intake_score": difficulty_score(item),
                "lifecycle_mode": "planned",
                "theorem_complete": False,
            }
        )
    return {
        "schema_version": "stage1-target-set/5.6.2",
        "standard": "Docs/Stage1_Blueprint_rev-5.6.md",
        "generated_projection": "Docs/Stage1_Blueprint_Applicable_Theorems.md",
        "scope": {
            "stage0_records": len(all_items),
            "stage0_removed_duplicates": removed_count,
            "stage0_mathematics_records": len(math_items),
            "covered_targets": len(eligible),
            "excluded_mathematics_records": len(excluded),
            "legacy_priority_slots": len(selected),
            "uniform_l0_targets": len(eligible),
            "canonical_sorted_target_id_set_sha256": target_set_hash,
        },
        "excluded_population_counts": dict(sorted(excluded_dispositions.items())),
        "targets": targets,
    }


def main() -> None:
    if not STANDARD_FILE.is_file():
        raise RuntimeError(f"missing Stage1 assurance standard: {STANDARD_FILE}")
    standard = STANDARD_FILE.read_text(encoding="utf-8")
    required_sections = (
        "Canonical Obligation Registry",
        "Typed Graph Contract",
        "Coverage and Anti-Goodhart Metrics",
        "Hermetic Lean 4 Reproduction",
        "Independent Verification and CI",
    )
    missing = [section for section in required_sections if section not in standard]
    if missing:
        raise RuntimeError(f"Stage1 assurance standard is incomplete: {missing}")
    items, removed_count = load_stage0_items()
    selected = select_items(items)
    if len(selected) != TOP_N:
        raise RuntimeError(f"expected {TOP_N} selected items, got {len(selected)}")
    OUTPUT_FILE.write_text(render_blueprint(selected, items, removed_count))
    APPLICABLE_FILE.write_text(render_applicable_list(selected, items, removed_count))
    TARGET_MANIFEST_FILE.write_text(
        json.dumps(build_target_manifest(selected, items, removed_count), ensure_ascii=False, indent=2)
        + "\n",
        encoding="utf-8",
    )
    subprocess.run(
        [sys.executable, str(Path(__file__).resolve().with_name("check_stage1_standard.py"))],
        cwd=ROOT,
        check=True,
    )
    print(f"Wrote {OUTPUT_FILE.relative_to(ROOT)}")
    print(f"Wrote {APPLICABLE_FILE.relative_to(ROOT)}")
    print(f"Wrote {TARGET_MANIFEST_FILE.relative_to(ROOT)}")
    print(
        f"Generated {len([item for item in items if is_stage1_eligible(item)])} uniform L0 targets; "
        f"retained {len(selected)} legacy slots as discovery metadata"
    )


if __name__ == "__main__":
    main()
