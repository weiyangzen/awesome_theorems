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
TARGET_MANIFEST_FILE = ROOT / "Docs" / "Stage1_Targets_rev-5.6.json"
STANDARD_FILE = ROOT / "Docs" / "Stage1_Assurance_Standard_rev-5.6.md"
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
        "standard": "Docs/Stage1_Assurance_Standard_rev-5.6.md",
        "task_state_authority": "Docs/Stage1_Blueprint_v2.md",
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
    print(f"Wrote {TARGET_MANIFEST_FILE.relative_to(ROOT)}")
    print(
        f"Generated {len([item for item in items if is_stage1_eligible(item)])} uniform L0 targets; "
        f"retained {len(selected)} legacy slots as discovery metadata"
    )


if __name__ == "__main__":
    main()
