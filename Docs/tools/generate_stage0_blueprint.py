#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

from collections import Counter, OrderedDict
from dataclasses import dataclass
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]
RESEARCH_DIR = ROOT / "Docs" / "researches"
OUTPUT_FILE = ROOT / "Docs" / "Stage0_Blueprint.md"


LIST_STYLE_SOURCES = [
    {
        "path": RESEARCH_DIR / "math_theorems.md",
        "discipline": "数学",
        "ignore_h2": {"概述", "目录"},
    },
    {
        "path": RESEARCH_DIR / "physics_theorems.md",
        "discipline": "物理",
        "ignore_h2": {"概述", "统计信息", "定理列表"},
    },
]

TABLE_STYLE_SOURCE = {
    "path": RESEARCH_DIR / "cs_theorems.md",
    "discipline": "计算机科学",
    "ignore_h2": {"目录", "统计信息", "参考文献"},
}

DISCIPLINE_PREFIX = {
    "数学": "M",
    "物理": "P",
    "计算机科学": "C",
}

DISCIPLINE_PRIORITY = {
    "数学": 0,
    "物理": 1,
    "计算机科学": 2,
}


@dataclass
class Theorem:
    discipline: str
    subcategory: str
    name: str
    proposer: str
    proposed_time: str
    statement: str
    importance: str
    formal_status: str
    source_file: str
    source_domain: str = ""
    uid: str = ""


TheoremOverrideKey = tuple[str, str, str, str, str]


THEOREM_OVERRIDES: dict[TheoremOverrideKey, dict[str, str]] = {
    (
        "数学",
        "费马大定理",
        "Pierre de Fermat",
        "1637",
        "x^n+y^n=z^n (n>2)无正整数解",
    ): {
        "命题类型": "数学定理 / 不存在性命题 / 丢番图方程结果",
        "目标形式系统": "首选 Lean 4 + mathlib；备选 Isabelle/HOL / Coq / HOL Light",
        "逻辑基础/形式系统": "Lean 路线以依赖类型论 + `Prop` + 按需 classical 为主；若迁移 Isabelle/HOL，则采用经典高阶逻辑",
        "提出背景": "费马在丢番图《算术》页边给出断言；现代证明路线则来自椭圆曲线、模形式、伽罗瓦表示与模性提升理论",
        "精确定义与前提条件": "变量域取 `ℕ` 或 `ℤ`；要求 `x ≠ 0 ∧ y ≠ 0 ∧ z ≠ 0`，`n ≥ 3`，方程为 `x ^ n + y ^ n = z ^ n`；形式化时先做 primitive solution 化简，再用指数整除约化把合数指数压回 `n = 4` 或奇素数指数。",
        "被证明的过程": "闭环0 = 合数指数约化：若 `4 ∣ n` 则归入 `n = 4`，否则取奇素数因子 `p ∣ n` 归入指数 `p`；闭环1 = `n = 4` 用勾股数分类 + 无限递降排除；闭环2 = `n = 3` 用三次分圆域与 descent 排除；闭环3 = 一般奇素数指数走 Frey 曲线、Ribet 降层、Wiles/Taylor-Wiles 模性路线导出矛盾。",
        "被证明年代或时间": "1994 公布，1995 发表修正后的完整论文链",
        "被证明的意义": "源文档重要性 = 高；它把整数方程问题与椭圆曲线、模形式、伽罗瓦表示联通，也是现代 proof assistant 测试高阶数论 formalization 能力的旗舰 benchmark",
        "证明路径上的定理或其他引例引理": "`Mathlib.NumberTheory.FLT.Basic` 中的 statement/reduction 工具、`fermatLastTheoremFour`、`fermatLastTheoremThree`、`FermatLastTheorem.of_odd_primes`、`flt_regular`、`CaseI.caseI`、`CaseII.caseII`、Frey 曲线构造、Ribet 降层、半稳定椭圆曲线模性定理、Taylor-Wiles patching 主链",
        "依赖图与关键引理": "顶层先做自然数/整数/有理数版本等价、primitive solution 化简与指数整除约化；其中所有 `4` 以上非素数指数都被 reduction layer 吸收：`4 ∣ n` 归入 `n = 4`，否则取奇素数因子 `p ∣ n` 归入指数 `p`。在独立主 branch 上，中层封闭 `n = 4` 的无限递降与 `n = 3` 的 generalized equation + multiplicity descent；再往上一层是 regular primes 的 `MayAssume + Case I + Case II + flt_regular`；底层未完成部分仍是奇素数指数的一般 Taylor-Wiles / Wiles 主链。",
        "定理树展开要求": "根节点 = FLT 主命题；必须继续展开到 `statement/reduction`、合数指数吸收层、`n = 4`、`n = 3`、`regular primes`、一般奇素数指数主链六层；其中 `n = 4` 与 `regular primes` 需要继续下钻到具体引理和 case split 节点；`n = 3` 只拆到真正承担证明工作的 mod `9` / generalized equation / multiplicity descent 节点，不向初等数论常识层过拆。",
        "叶子节点证明步数上限": "100 步",
        "当前定理树叶子控制状态": "`n = 4` 已拆成 `7` 个 canonical package，regular primes 已拆成 `11` 个 canonical package；两条线在 `machine_checked_audit`、`process_audit`、`eligibles` 三层材料里已对齐命名。跨文件统一的 `7` 个 canonical high-risk leaf 保持为：`raw coprime triple classification`、`square extraction for r*s with sign cleanup`、`strict natAbs descent hic`、`Case II ideal-factor layer / global product to local p-th powers`、`Case II distinguished root / p_pow_dvd_c_eta_zero`、`Case II descent core / three-root formula and raw descent`、`Case II close / merge / not_exists_solution'`。上述 canonical package、canonical high-risk leaf，以及先前单列的 package-level subitem `Int.gcd a n = 1 transfer`、`exists_ideal pairwise ideal coprimality interface`、`caseI_easier / aux-index exclusion`，现在都已各自拥有独立 `<=100` proof-step ledger 并在对应 completion surface 中记为 `checked`。regular primes 的 human-readable boundary sentence 仍固定保留为 `upstream theorem closure: yes / repo-local vendored theorem closure: no, anchor-only / repo-local anchor-only statement/module/theorem-name record: yes`；其中最后一段只表示锚点 statement/module/theorem-name 记录已到位，不表示本仓库已 vendoring 上游 `flt_regular` 证明本体。`eligibles` 中的 reader-facing labels / budget aliases 只作为讲解别名，不构成第二套 canonical node 名；跨文件同步仍以上述 package / leaf 名为准。`n = 3` 有意保持较粗粒度，不下钻到初等数论常识层。完整 Wiles/Taylor-Wiles 一般奇素数指数主链仍未闭合。",
        "证据类型": "无限递降证明 + 代数数论证明 + 模性证明 + 局部完整 machine-check + 总体大型协作 formalization",
        "形式化阻塞点": "真正瓶颈在模形式/Hecke 代数/伽罗瓦表示/deformation theory 基础设施，而非 statement 本身；论文中的“标准事实”必须被拆成细粒度 lemma，且对象表示与 API 稳定性要求极高",
        "等价表述": "自然数版本、整数版本、有理数版本可互转；完整 FLT 可约化为 `n = 4` 与所有奇素数指数；只需考虑 primitive solution",
        "所需公理": "自然数/整数/有理数标准代数结构、gcd/PID/UFD 相关结构、理想/商环/分圆域等代数数论对象；完整主证明还依赖更强的现代经典数学基础设施",
        "经典逻辑/选择公理依赖": "`n = 4` 路线较初等，但 `n = 3`、regular primes 与完整 Wiles/Taylor-Wiles 路线在工程上都应按 classical + noncomputable 的现代数学库组织方式准备",
        "现有 machine-checked 状态": "`Mathlib.NumberTheory.FLT.Basic` 已 machine-check statement/reduction 层（`FermatLastTheoremWith`、`FermatLastTheoremFor`、`FermatLastTheorem`、`FermatLastTheoremWith.mono`、`FermatLastTheoremFor.mono`、`FermatLastTheorem.of_odd_primes`、`fermatLastTheoremFor_iff_int`、`fermatLastTheoremFor_iff_rat`、`fermatLastTheoremWith_of_fermatLastTheoremWith_coprime`）；`Four.lean` 已完成 `n = 4`（`Fermat42`、`exists_minimal`、`coprime_of_minimal`、`not_minimal`、`not_fermat_42`、`fermatLastTheoremFour`，其下一层高负载节点包括 `PythagoreanTriple.coprime_classification'`、`Int.isCoprime_of_sq_sum'`、`Int.sq_of_gcd_eq_one`）；`Three.lean` 已完成 `n = 3`（mod `9` 的 Case 1、`FermatLastTheoremForThreeGen`、`Solution'`/`Solution`、`exists_Solution_of_Solution'`、`exists_Solution_multiplicity_lt`、`fermatLastTheoremThree`）；`flt-regular` 已完成 regular primes（`MayAssume.coprime`、`a_not_cong_b`、`exists_ideal`、`is_principal_aux` / `is_principal`、`exists_solution` / `exists_solution'`、`CaseI.caseI`、`CaseII.caseII`、`flt_regular`）；更细的 theorem-level 与 process-level 审计见专题文档 `§二`；完整 Wiles/Taylor-Wiles 总项目截至 2026-04-16 仍为 ongoing",
        "现有工件链接": "[权威总研究文档](../THM-M-0387/full_study.md)；[旗舰材料包](../THM-M-0387/README.md)；[机器证明审计](../THM-M-0387/machine_checked_audit.md)；[过程审计](../THM-M-0387/process_audit.md)；[本地验证记录](../THM-M-0387/build_validation.md)；[本地验证脚本](../THM-M-0387/run_local_validation.sh)；[Lean 样例入口](../THM-M-0387/FermatLastTheorem_Sample.lean)；[共享 Lean 库根模块](../Formalizations/Lean/AwesomeTheorems.lean)；[共享 Lean `n = 4` 路径模块](../Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/FLT4Path.lean)；[共享 Lean `n = 3` 路径模块](../Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/FLT3Path.lean)；[共享 Lean regular primes 路径模块](../Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/RegularPrimesPath.lean)；[共享 Lean 聚合模块](../Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/Sample.lean)；[Blueprint Guidelines](./Blueprint_Guidelines.md)；mathlib `Basic/Four/Three` 文档：<https://leanprover-community.github.io/mathlib4_docs/Mathlib/NumberTheory/FLT/Basic.html>、<https://leanprover-community.github.io/mathlib4_docs/Mathlib/NumberTheory/FLT/Four.html>、<https://leanprover-community.github.io/mathlib4_docs/Mathlib/NumberTheory/FLT/Three.html>；`flt-regular` 主入口与源码：<https://github.com/leanprover-community/flt-regular>；公开总项目：<https://github.com/ImperialCollegeLondon/FLT>；regular primes 论文页：<https://afm.episciences.org/16046>",
    },
}


H2_RE = re.compile(r"^##\s+(.*)$")
H3_RE = re.compile(r"^###\s+(.*)$")
THEOREM_RE = re.compile(r"^\*\*(.+?)\*\*$")
LIST_FIELD_RE = re.compile(r"^\s*-\s*(?:\*\*)?([^:*：]+?)(?:\*\*)?\s*[:：]\s*(.*)\s*$")


def strip_numeric_prefix(text: str) -> str:
    return re.sub(r"^\d+(?:\.\d+)?\s*", "", text).strip()


def normalize_title(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^\*\*(.+)\*\*$", r"\1", text)
    text = re.sub(r"^\d+\.\s*", "", text)
    return text.strip()


def normalize_subcategory(parent: str, child: str) -> str:
    parent = strip_numeric_prefix(parent)
    child = strip_numeric_prefix(child)
    if child.startswith(parent + "-"):
        leaf = child[len(parent) + 1 :].strip()
        return f"{parent} / {leaf}"
    if child.startswith(parent + " / "):
        return child
    return f"{parent} / {child}"


def normalize_field_key(key: str) -> str:
    key = key.strip()
    return key.replace(" ", "")


def theorem_override_key(theorem: Theorem) -> TheoremOverrideKey:
    return (
        theorem.discipline,
        theorem.name,
        theorem.proposer,
        theorem.proposed_time,
        theorem.statement,
    )


def theorem_overrides(theorem: Theorem) -> dict[str, str]:
    return THEOREM_OVERRIDES.get(theorem_override_key(theorem), {})


def ensure_theorem(
    entry: Theorem | None,
    items: list[Theorem],
) -> None:
    if entry is not None:
        items.append(entry)


def parse_list_style_source(path: Path, discipline: str, ignore_h2: set[str]) -> list[Theorem]:
    text = path.read_text()
    items: list[Theorem] = []
    current_h2: str | None = None
    current_h3: str | None = None
    current_entry: Theorem | None = None

    for raw_line in text.splitlines():
        line = raw_line.rstrip()

        h2_match = H2_RE.match(line)
        if h2_match:
            ensure_theorem(current_entry, items)
            current_entry = None
            heading = h2_match.group(1).strip()
            if heading in ignore_h2:
                current_h2 = None
                current_h3 = None
                continue
            current_h2 = heading
            current_h3 = None
            continue

        h3_match = H3_RE.match(line)
        if h3_match:
            ensure_theorem(current_entry, items)
            current_entry = None
            if current_h2 is None:
                continue
            current_h3 = normalize_subcategory(current_h2, h3_match.group(1).strip())
            continue

        theorem_match = THEOREM_RE.match(line.strip())
        if theorem_match and current_h2 is not None:
            theorem_name = normalize_title(theorem_match.group(1))
            if theorem_name.startswith("定理数量"):
                continue
            ensure_theorem(current_entry, items)
            current_entry = Theorem(
                discipline=discipline,
                subcategory=current_h3 or strip_numeric_prefix(current_h2),
                name=theorem_name,
                proposer="待补充",
                proposed_time="待补充",
                statement="待补充",
                importance="待补充",
                formal_status="待补充",
                source_file=str(path.relative_to(ROOT)),
            )
            continue

        if current_entry is None:
            continue

        field_match = LIST_FIELD_RE.match(line)
        if not field_match:
            continue

        key = normalize_field_key(field_match.group(1))
        value = field_match.group(2).strip() or "待补充"

        if key == "提出者":
            current_entry.proposer = value
        elif key == "时间":
            current_entry.proposed_time = value
        elif key == "陈述":
            current_entry.statement = value
        elif key == "重要性":
            current_entry.importance = value
        elif key == "形式化状态":
            current_entry.formal_status = value

    ensure_theorem(current_entry, items)
    return items


def is_table_row(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("|") and not re.match(r"^\|\s*-", stripped)


def parse_table_style_source(path: Path, discipline: str, ignore_h2: set[str]) -> list[Theorem]:
    text = path.read_text()
    items: list[Theorem] = []
    current_h2: str | None = None
    current_h3: str | None = None

    for raw_line in text.splitlines():
        line = raw_line.rstrip()

        h2_match = H2_RE.match(line)
        if h2_match:
            heading = h2_match.group(1).strip()
            if heading in ignore_h2:
                current_h2 = None
                current_h3 = None
                continue
            current_h2 = strip_numeric_prefix(heading)
            current_h3 = None
            continue

        h3_match = H3_RE.match(line)
        if h3_match:
            if current_h2 is None:
                continue
            current_h3 = normalize_subcategory(current_h2, h3_match.group(1).strip())
            continue

        if current_h2 is None or current_h3 is None or not is_table_row(line):
            continue

        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 8:
            continue
        if cells[0] in {"序号", "重要性级别", "形式化状态", "分支"}:
            continue
        if not re.match(r"^\d+(?:\.\d+)*$", cells[0]):
            continue

        name = normalize_title(cells[1])
        source_domain = cells[2]
        proposer = cells[3] or "待补充"
        proposed_time = cells[4] or "待补充"
        statement = cells[5] or "待补充"
        importance = cells[6] or "待补充"
        formal_status = cells[7] or "待补充"

        items.append(
            Theorem(
                discipline=discipline,
                subcategory=current_h3,
                name=name,
                proposer=proposer,
                proposed_time=proposed_time,
                statement=statement,
                importance=importance,
                formal_status=formal_status,
                source_file=str(path.relative_to(ROOT)),
                source_domain=source_domain,
            )
        )

    return items


def assign_ids(items: list[Theorem]) -> None:
    counters: Counter[str] = Counter()
    for item in items:
        prefix = DISCIPLINE_PREFIX[item.discipline]
        counters[prefix] += 1
        item.uid = f"THM-{prefix}-{counters[prefix]:04d}"


def group_by_discipline_and_subcategory(items: list[Theorem]) -> OrderedDict[str, OrderedDict[str, list[Theorem]]]:
    grouped: OrderedDict[str, OrderedDict[str, list[Theorem]]] = OrderedDict()
    for item in items:
        grouped.setdefault(item.discipline, OrderedDict())
        grouped[item.discipline].setdefault(item.subcategory, [])
        grouped[item.discipline][item.subcategory].append(item)
    return grouped


def dedupe_items(items: list[Theorem]) -> tuple[list[Theorem], int]:
    kept: dict[tuple[str, str, str, str, str, str], tuple[int, Theorem]] = {}
    removed = 0

    for index, item in enumerate(items):
        signature = (
            item.name,
            item.statement,
            item.proposer,
            item.proposed_time,
            item.importance,
            item.formal_status,
        )
        current = kept.get(signature)
        if current is None:
            kept[signature] = (index, item)
            continue

        kept_index, kept_item = current
        candidate_key = (DISCIPLINE_PRIORITY[item.discipline], index)
        kept_key = (DISCIPLINE_PRIORITY[kept_item.discipline], kept_index)
        if candidate_key < kept_key:
            kept[signature] = (index, item)
        removed += 1

    deduped = [entry[1] for entry in sorted(kept.values(), key=lambda pair: pair[0])]
    return deduped, removed


def infer_proposition_type(theorem: Theorem) -> str:
    unresolved_statuses = {"未解决", "待解决", "待证明", "部分解决"}
    if theorem.formal_status in unresolved_statuses:
        return "开放问题 / 猜想 / 未完全闭合命题"

    if theorem.discipline == "数学":
        if "引理" in theorem.name:
            return "引理"
        if "公式" in theorem.name:
            return "公式 / 恒等式"
        if "问题" in theorem.name:
            return "问题 / 判定命题"
        return "数学定理 / 命题"

    if theorem.discipline == "物理":
        keyword_map = [
            ("方程", "方程 / 动力学规律"),
            ("定律", "物理定律"),
            ("原理", "原理"),
            ("理论", "理论框架"),
            ("模型", "模型"),
            ("机制", "机制"),
            ("效应", "物理效应"),
            ("关系", "关系式 / 守恒关系"),
        ]
        for keyword, proposition_type in keyword_map:
            if keyword in theorem.name:
                return proposition_type
        return "物理命题 / 物理结果"

    if theorem.discipline == "计算机科学":
        keyword_map = [
            ("不可判定", "不可判定性结果"),
            ("不可解", "不可判定性 / 不可解性结果"),
            ("完备性", "完备性结果"),
            ("等价性", "等价性结果"),
            ("算法", "算法正确性 / 复杂度结果"),
            ("协议", "协议性质 / 安全性结论"),
            ("定理", "理论定理"),
            ("问题", "判定问题 / 开放问题"),
            ("构造", "构造性结果"),
        ]
        for keyword, proposition_type in keyword_map:
            if keyword in theorem.name:
                return proposition_type
        return "理论结果 / 复杂度结论 / 验证命题"

    return "待补充"


def default_target_formal_system(theorem: Theorem) -> str:
    if theorem.discipline == "数学":
        return "待选（Lean / Isabelle/HOL / HOL Light / Coq）"
    if theorem.discipline == "物理":
        return "待选（Lean + mathlib / Isabelle/HOL / 物理专用符号化工作流）"
    if theorem.discipline == "计算机科学":
        return "待选（Coq / Lean / Isabelle / TLA+ / model checker）"
    return "待补充"


def default_logic_foundation(theorem: Theorem) -> str:
    if theorem.discipline == "数学":
        return "待选（经典高阶逻辑 / 依赖类型论 / 集合论编码）"
    if theorem.discipline == "物理":
        return "待选（高阶逻辑 + 实分析/测度论/线性代数/偏微分方程基础）"
    if theorem.discipline == "计算机科学":
        return "待选（类型论 / 高阶逻辑 / 时序逻辑 / 程序逻辑 / 复杂性理论编码）"
    return "待补充"


def default_evidence_type(theorem: Theorem) -> str:
    if theorem.discipline == "数学":
        return "待判定（解析证明 / 构造性证明 / 计算机辅助证明）"
    if theorem.discipline == "物理":
        return "待判定（理论推导 / 实验观测 / 数值模拟 / 有效理论论证）"
    if theorem.discipline == "计算机科学":
        return "待判定（归约证明 / 算法证明 / 程序验证 / 安全归约 / 模型检验）"
    return "待补充"


def formal_status_bucket(theorem: Theorem) -> str:
    status = theorem.formal_status
    if "不可判定" in status:
        return "undecidable"
    if "独立于ZFC" in status:
        return "independent"
    if "已否证" in status:
        return "refuted"
    if any(keyword in status for keyword in ("部分", "进行中", "声称证明")):
        return "partial"
    if any(keyword in status for keyword in ("待研究", "待验证", "待解决", "待证明", "未解决")):
        return "open"
    if any(keyword in status for keyword in ("已验证", "已解决", "已证明", "准多项式时间解决")):
        return "closed"
    if "可验证" in status:
        return "verifiable"
    return "unknown"


def default_tree_requirement(theorem: Theorem) -> str:
    proposition_type = infer_proposition_type(theorem)
    bucket = formal_status_bucket(theorem)

    if theorem.discipline == "数学":
        if "引理" in proposition_type:
            base = "根节点 = 引理陈述；向下至少拆成前提规范化、关键代数/结构步骤、必要分情况节点；若某步仍依赖标准引理，则继续向下展开。"
        elif "公式" in proposition_type or "恒等式" in proposition_type:
            base = "根节点 = 公式/恒等式；向下至少拆成定义展开、变换链、边界或收敛条件节点、必要分情况节点。"
        else:
            base = "根节点 = 主定理；向下至少拆成定义/约化节点、关键引理节点、必要的 case split / induction / descent 节点。"
    elif theorem.discipline == "物理":
        base = "根节点 = 主物理结论；向下至少拆成建模前提、适用 regime、控制方程/守恒关系、近似闭合步骤、必要分情况节点。"
    elif theorem.discipline == "计算机科学":
        base = "根节点 = 主理论结论；向下至少拆成计算模型定义、关键引理、归约/正确性/复杂度/安全性节点、必要分情况节点。"
    else:
        base = "主命题必须继续展开到引理节点或分情况讨论节点。"

    if bucket in {"open", "undecidable", "independent", "refuted"}:
        return base + " 当前若尚无闭合证明，应至少给出候选证明树、已知 barrier results 或 case split 骨架。"
    if bucket == "partial":
        return base + " 已知闭合的分支要优先继续下钻到叶子；未闭合分支应明确标记 ongoing。"
    return base


def default_leaf_control_status(theorem: Theorem) -> str:
    bucket = formal_status_bucket(theorem)

    if bucket == "closed":
        return "已知存在闭合结果，但蓝图尚未完成逐叶审计；当前默认仍需继续拆到叶子节点，并检查每个叶子证明过程是否 <= 100 步。"
    if bucket == "partial":
        return "已有部分闭合分支或中间结果；已知分支需继续细化叶子预算，超出当前材料覆盖范围的部分应明确标记 ongoing。"
    if bucket == "verifiable":
        return "存在较强形式化可行性信号，但尚未确认闭合证明树；需先补定理树并做叶子预算审计。"
    if bucket == "open":
        return "主命题尚未闭合；当前先整理候选证明树、已知 reductions 与关键障碍，叶子预算检查暂不能视为完成。"
    if bucket == "undecidable":
        return "该结论类型应优先展开到编码、归约与对角线/语义障碍节点；叶子预算只对这些已闭合子证明单元生效。"
    if bucket == "independent":
        return "该命题应优先展开到相容性/独立性论证节点；在未明确双向相对一致性链之前，不视为叶子预算合规。"
    if bucket == "refuted":
        return "该条目应优先展开到反例构造、失败 case、或否证链的最小节点；反例链自身的叶子证明过程仍应控制在 100 步以内。"
    return "待补充（需检查是否已拆到叶子节点且每个叶子证明过程 <= 100 步）"


def default_blockers(theorem: Theorem) -> str:
    bucket = formal_status_bucket(theorem)

    if theorem.discipline == "数学":
        if bucket == "closed":
            return "已知困难通常不在“有没有证明”，而在 theorem tree 尚未拆细、叶子预算未审计、formal artifact 未逐条定位；仍需检查定义展开、非构造性步骤、库缺失、测度/范畴/同调等高层抽象。"
        if bucket == "partial":
            return "除定义展开、非构造性步骤、库缺失、测度/范畴/同调等高层抽象外，还需明确哪些分支已闭合、哪些分支必须继续标记 ongoing。"
        return "待补充（重点检查定义展开、非构造性步骤、库缺失、测度/范畴/同调等高层抽象）"
    if theorem.discipline == "物理":
        if bucket == "closed":
            return "已知困难通常在 regime 切分、近似假设、单位约定、实验可观测量与数值闭环尚未拆成可审计树，而不只是“有没有结果”。"
        return "待补充（重点检查适用尺度、近似假设、单位约定、实验可观测量、重整化或数值闭环）"
    if theorem.discipline == "计算机科学":
        if bucket == "closed":
            return "已知困难通常在计算模型、资源度量、对手模型、复杂度编码与可执行规范尚未拆成树形审计，而不只是缺少结论本身。"
        return "待补充（重点检查计算模型固定、资源度量、对手模型、复杂度编码、可执行规范）"
    return "待补充"


def append_discipline_specific_lines(lines: list[str], theorem: Theorem, overrides: dict[str, str]) -> None:
    if theorem.discipline == "数学":
        lines.append(f"  - 等价表述: {overrides.get('等价表述', '待补充')}")
        lines.append(f"  - 所需公理: {overrides.get('所需公理', '待补充')}")
        lines.append(
            f"  - 经典逻辑/选择公理依赖: {overrides.get('经典逻辑/选择公理依赖', '待补充')}"
        )
        lines.append(f"  - 现有 machine-checked 状态: {overrides.get('现有 machine-checked 状态', '待补充')}")
        return

    if theorem.discipline == "物理":
        lines.append("  - 适用 regime / 尺度: 待补充")
        lines.append("  - 近似层级: 待补充")
        lines.append("  - 实验可观测量: 待补充")
        lines.append("  - 量纲与单位/归一化约定: 待补充")
        lines.append("  - 误差模型 / 数值方案: 待补充")
        lines.append("  - 重整化 / 有效理论依赖: 待补充")
        return

    if theorem.discipline == "计算机科学":
        lines.append("  - 计算模型: 待补充")
        lines.append("  - 复杂度 / 资源度量: 待补充")
        lines.append("  - 对手模型 / 安全参数: 待补充")
        lines.append("  - 平均 / 最坏 / 摊还情形: 待补充")
        lines.append("  - 可执行规范 / 机器检查对象: 待补充")


def render_blueprint(items: list[Theorem]) -> str:
    grouped = group_by_discipline_and_subcategory(items)
    subcategory_counts = {
        discipline: len(subgroups) for discipline, subgroups in grouped.items()
    }
    theorem_counts = Counter(item.discipline for item in items)
    total_count = len(items)

    lines: list[str] = []
    lines.append("# Stage0 Blueprint")
    lines.append("")
    lines.append("## 定位")
    lines.append("")
    lines.append("- 本文件是后续执行型 cron 的唯一 authoritative blueprint。")
    lines.append("- 后续 todo、批次切分、进度回写、自动拆分都只能以本文件为 requirement source。")
    lines.append(f"- 当前 Stage0 目标不是伪造研究结论，而是把 `Docs/researches` 中现有的 {total_count} 个定理统一成可执行、可追踪、可拆分的结构化蓝图。")
    lines.append("- 一级类目只按学科展开：`数学`、`物理`、`计算机科学`。")
    lines.append("- 二级类目按源文档的主类目/次类目合并成一个稳定子分类路径，例如 `代数学 / 同调代数`、`凝聚态物理 / 超导`、`复杂性理论 / P vs NP 与 NP完全性`。")
    lines.append("- 已执行一次严格去重：仅当 `名称 + 提出者 + 提出时间 + 陈述 + 重要性 + 形式化状态` 完全一致时才视为同一条目；保留优先级为 `数学 > 物理 > 计算机科学`，同学科内保留最早出现者。")
    lines.append("")
    lines.append("## 执行边界")
    lines.append("")
    lines.append("- 唯一输入源：`Docs/researches/math_theorems.md`、`Docs/researches/physics_theorems.md`、`Docs/researches/cs_theorems.md`。")
    lines.append("- 本蓝图内每个定理只有一个 checklist item；未完成项只能由补全字段、补全引用链、补全形式化路径来推进，不能靠文档表面勾选。")
    lines.append("- 虽然每个定理在 Stage0 中只有一个 checklist item，但该 item 的内部证明结构必须按“定理树”展开，而不是停留在线性摘要。")
    lines.append("- 每个条目的定理树至少要展开到引理节点或分情况讨论节点；不能只保留主定理名。")
    lines.append("- 叶子节点必须是不再引用其他 theorem / lemma 的最小证明单元；每个叶子节点的证明过程上限为 `100` 步。")
    lines.append("- 若某叶子节点超过 `100` 步，则该条目默认仍未收敛，后续 cron 必须继续拆分。")
    lines.append("- 若某条目已有 machine-checked branch，后续补强顺序默认是：先补 `machine_checked_audit` / `process_audit` 的机器节点留痕，再补 `eligibles` 的人类可读展开。")
    lines.append("- 默认读者基线按“大学水平、具备相关学科基础”处理；对显然的基础动作，不应为了凑树深度而过度教学化细拆。")
    lines.append("- 若源文档未区分“提出时间”和“证明时间”，本蓝图先保留 `提出假说时间`，把 `被证明年代或时间` 置为 `待补充`，等待后续研究批次回填。")
    lines.append("- 若源文档只给出“重要性”而未给出具体学术意义，本蓝图将其映射为 `被证明的意义` 的最小占位信息。")
    lines.append("- 已把 `命题类型`、`目标形式系统`、`逻辑基础`、`证据类型`、`形式化阻塞点`、以及学科专属字段纳入每个 theorem item，供后续 cron 拆分。")
    lines.append("- 对同一 checklist item 连续多次无法收敛时，后续 cron 应把该定理自动拆为更细的研究子项，而不是直接跳过。")
    lines.append("")
    lines.append("## 勾选门槛")
    lines.append("")
    lines.append("- 只有当定理条目的结构化字段补全、形式化可验证性判断可追溯、证明闭环有可核查内容、证明路径引理链可追踪时，才能从 `[ ]` 变为 `[x]`。")
    lines.append("- `命题类型`、`目标形式系统`、`逻辑基础/形式系统`、`精确定义与前提条件`、`证据类型`、`形式化阻塞点` 不完整时，不得勾选。")
    lines.append("- 仅补充 prose 或仅补充摘要，不足以勾选。")
    lines.append("- 需要保留学科上下文，不允许把数学/物理/计算机里的同名结果混成一个 completion item。")
    lines.append("")
    lines.append("## 统计概览")
    lines.append("")
    lines.append("| 学科 | 二级类目数 | 定理数 |")
    lines.append("|---|---:|---:|")
    for discipline in ("数学", "物理", "计算机科学"):
        lines.append(
            f"| {discipline} | {subcategory_counts.get(discipline, 0)} | {theorem_counts.get(discipline, 0)} |"
        )
    lines.append(f"| 总计 | {sum(subcategory_counts.values())} | {len(items)} |")
    lines.append("")
    lines.append("## 字段模板")
    lines.append("")
    lines.append("- `定理内容`：当前版本优先映射源文档里的“陈述”。")
    lines.append("- `命题类型`：区分定理、猜想、方程、模型、效应、算法正确性、复杂度结论、不可能性结果等。")
    lines.append("- `形式化可验证性`：当前版本优先映射源文档里的“形式化状态”。")
    lines.append("- `目标形式系统`：明确 Lean / Coq / Isabelle / HOL Light / TLA+ / model checker 等目标落点。")
    lines.append("- `逻辑基础/形式系统`：记录 HOL、类型论、时序逻辑、程序逻辑、集合论编码等选择。")
    lines.append("- `提出假说时间`：当前版本优先映射源文档里的“时间”。")
    lines.append("- `提出背景`：默认 `待补充`，供后续研究批次补完。")
    lines.append("- `精确定义与前提条件`：记录变量域、量词范围、边界条件、正则性、单位制、近似前提。")
    lines.append("- `被证明的过程`：先放一个最小“假说内容 - 证明/观测”闭环占位，后续再细分子模块。")
    lines.append("- `被证明年代或时间`：源文档未显式给出的，一律 `待补充`。")
    lines.append("- `被证明的意义`：先保留源文档的“重要性”等级，再等待补上具体意义。")
    lines.append("- `证明路径上的定理或其他引例引理`：记录主证明依赖链。")
    lines.append("- `依赖图与关键引理`：用于 cron 自动拆分时生成子任务树。")
    lines.append("- `定理树展开要求`：要求主定理至少展开到引理或 case split 节点。")
    lines.append("- `叶子节点证明步数上限`：统一要求叶子节点证明过程不超过 `100` 步。")
    lines.append("- `当前定理树叶子控制状态`：记录当前是否已拆到满足 `100` 步预算。")
    lines.append("- `证据类型`：区分解析证明、构造性证明、实验观测、数值模拟、归约证明、程序验证等。")
    lines.append("- `形式化阻塞点`：记录库缺失、模型未固定、近似没写清、非构造性步骤等问题。")
    lines.append("- `现有工件链接`：论文、书籍、formal proof repo、mathlib/AFP 条目、脚本与数据位置。")
    lines.append("")
    lines.append("## 学科特有字段")
    lines.append("")
    lines.append("- 数学：`等价表述`、`所需公理`、`经典逻辑/选择公理依赖`、`现有 machine-checked 状态`。")
    lines.append("- 物理：`适用 regime / 尺度`、`近似层级`、`实验可观测量`、`量纲与单位/归一化约定`、`误差模型 / 数值方案`、`重整化 / 有效理论依赖`。")
    lines.append("- 计算机科学：`计算模型`、`复杂度 / 资源度量`、`对手模型 / 安全参数`、`平均 / 最坏 / 摊还情形`、`可执行规范 / 机器检查对象`。")
    lines.append("")
    lines.append("## 执行切分建议")
    lines.append("")
    lines.append("- 优先按二级类目推进，一个 batch 处理同一子分类内 6 到 8 个定理。")
    lines.append("- 对证明链特别长或形式化障碍明显的条目，拆成“命题类型校准 / 陈述规范化 / 逻辑基础锁定 / 定理树展开 / 关键引理 / 主证明 / 证据闭环 / 形式化落地”几个子任务。")
    lines.append("- 对已 machine-checked 的 branch，优先补到“机器节点再拆一层”的程度，再决定是否扩写 `eligibles`。")
    lines.append("- 任何 theorem item 在进入形式化落地之前，都应先完成一次叶子节点步数预算检查，确认叶子证明过程已压到 `100` 步以内。")
    lines.append("- 上层类目不能先被标记完成；必须等其下所有定理 item 都闭合。")
    lines.append("")

    for discipline, subgroups in grouped.items():
        lines.append(f"## {discipline}")
        lines.append("")
        for subcategory, theorems in subgroups.items():
            lines.append(f"### {subcategory}")
            lines.append("")
            lines.append(f"- 来源文件: `{theorems[0].source_file}`")
            lines.append(f"- 子分类定理数: `{len(theorems)}`")
            lines.append("")
            for theorem in theorems:
                overrides = theorem_overrides(theorem)
                lines.append(f"- [ ] {theorem.uid} {theorem.name}")
                lines.append(f"  - 定理内容: {theorem.statement}")
                lines.append(f"  - 命题类型: {overrides.get('命题类型', infer_proposition_type(theorem))}")
                lines.append(f"  - 形式化可验证性: {theorem.formal_status}")
                lines.append(f"  - 目标形式系统: {overrides.get('目标形式系统', default_target_formal_system(theorem))}")
                lines.append(
                    f"  - 逻辑基础/形式系统: {overrides.get('逻辑基础/形式系统', default_logic_foundation(theorem))}"
                )
                lines.append(f"  - 提出假说时间: {theorem.proposed_time}")
                lines.append(f"  - 提出背景: {overrides.get('提出背景', '待补充')}")
                lines.append(f"  - 精确定义与前提条件: {overrides.get('精确定义与前提条件', '待补充')}")
                lines.append(
                    f"  - 被证明的过程: {overrides.get('被证明的过程', f'闭环1 = 假说内容 `{theorem.statement}`；证明/观测 = 待补充')}"
                )
                lines.append(f"  - 被证明年代或时间: {overrides.get('被证明年代或时间', '待补充')}")
                lines.append(
                    f"  - 被证明的意义: {overrides.get('被证明的意义', f'源文档重要性 = {theorem.importance}；具体意义待补充')}"
                )
                lines.append(
                    f"  - 证明路径上的定理或其他引例引理: {overrides.get('证明路径上的定理或其他引例引理', '待补充')}"
                )
                lines.append(f"  - 依赖图与关键引理: {overrides.get('依赖图与关键引理', '待补充')}")
                lines.append(
                    f"  - 定理树展开要求: {overrides.get('定理树展开要求', default_tree_requirement(theorem))}"
                )
                lines.append(
                    f"  - 叶子节点证明步数上限: {overrides.get('叶子节点证明步数上限', '100 步')}"
                )
                lines.append(
                    f"  - 当前定理树叶子控制状态: {overrides.get('当前定理树叶子控制状态', default_leaf_control_status(theorem))}"
                )
                lines.append(f"  - 证据类型: {overrides.get('证据类型', default_evidence_type(theorem))}")
                lines.append(
                    f"  - 形式化阻塞点: {overrides.get('形式化阻塞点', default_blockers(theorem))}"
                )
                lines.append(f"  - 提出者/来源: {theorem.proposer}")
                if theorem.source_domain:
                    lines.append(f"  - 原始领域标签: {theorem.source_domain}")
                append_discipline_specific_lines(lines, theorem, overrides)
                lines.append(f"  - 现有工件链接: {overrides.get('现有工件链接', '待补充')}")
                lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    items: list[Theorem] = []
    for source in LIST_STYLE_SOURCES:
        items.extend(
            parse_list_style_source(
                path=source["path"],
                discipline=source["discipline"],
                ignore_h2=source["ignore_h2"],
            )
        )
    items.extend(
        parse_table_style_source(
            path=TABLE_STYLE_SOURCE["path"],
            discipline=TABLE_STYLE_SOURCE["discipline"],
            ignore_h2=TABLE_STYLE_SOURCE["ignore_h2"],
            )
        )

    items, removed_count = dedupe_items(items)
    assign_ids(items)
    OUTPUT_FILE.write_text(render_blueprint(items))

    counts = Counter(item.discipline for item in items)
    print(f"Wrote {OUTPUT_FILE.relative_to(ROOT)}")
    print(
        "Counts:",
        f"数学={counts['数学']}",
        f"物理={counts['物理']}",
        f"计算机科学={counts['计算机科学']}",
        f"总计={len(items)}",
        f"去重移除={removed_count}",
    )


if __name__ == "__main__":
    main()
