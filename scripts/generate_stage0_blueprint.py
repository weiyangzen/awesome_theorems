#!/usr/bin/env python3

from __future__ import annotations

from collections import Counter, OrderedDict
from dataclasses import dataclass
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
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


def default_blockers(theorem: Theorem) -> str:
    if theorem.discipline == "数学":
        return "待补充（重点检查定义展开、非构造性步骤、库缺失、测度/范畴/同调等高层抽象）"
    if theorem.discipline == "物理":
        return "待补充（重点检查适用尺度、近似假设、单位约定、实验可观测量、重整化或数值闭环）"
    if theorem.discipline == "计算机科学":
        return "待补充（重点检查计算模型固定、资源度量、对手模型、复杂度编码、可执行规范）"
    return "待补充"


def append_discipline_specific_lines(lines: list[str], theorem: Theorem) -> None:
    if theorem.discipline == "数学":
        lines.append("  - 等价表述: 待补充")
        lines.append("  - 所需公理: 待补充")
        lines.append("  - 经典逻辑/选择公理依赖: 待补充")
        lines.append("  - 现有 machine-checked 状态: 待补充")
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
    lines.append("")
    lines.append("## 执行边界")
    lines.append("")
    lines.append("- 唯一输入源：`Docs/researches/math_theorems.md`、`Docs/researches/physics_theorems.md`、`Docs/researches/cs_theorems.md`。")
    lines.append("- 本蓝图内每个定理只有一个 checklist item；未完成项只能由补全字段、补全引用链、补全形式化路径来推进，不能靠文档表面勾选。")
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
    lines.append("- 对证明链特别长或形式化障碍明显的条目，拆成“命题类型校准 / 陈述规范化 / 逻辑基础锁定 / 关键引理 / 主证明 / 证据闭环 / 形式化落地”几个子任务。")
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
                lines.append(f"- [ ] {theorem.uid} {theorem.name}")
                lines.append(f"  - 定理内容: {theorem.statement}")
                lines.append(f"  - 命题类型: {infer_proposition_type(theorem)}")
                lines.append(f"  - 形式化可验证性: {theorem.formal_status}")
                lines.append(f"  - 目标形式系统: {default_target_formal_system(theorem)}")
                lines.append(f"  - 逻辑基础/形式系统: {default_logic_foundation(theorem)}")
                lines.append(f"  - 提出假说时间: {theorem.proposed_time}")
                lines.append(f"  - 提出背景: 待补充")
                lines.append("  - 精确定义与前提条件: 待补充")
                lines.append(
                    f"  - 被证明的过程: 闭环1 = 假说内容 `{theorem.statement}`；证明/观测 = 待补充"
                )
                lines.append("  - 被证明年代或时间: 待补充")
                lines.append(f"  - 被证明的意义: 源文档重要性 = {theorem.importance}；具体意义待补充")
                lines.append("  - 证明路径上的定理或其他引例引理: 待补充")
                lines.append("  - 依赖图与关键引理: 待补充")
                lines.append(f"  - 证据类型: {default_evidence_type(theorem)}")
                lines.append(f"  - 形式化阻塞点: {default_blockers(theorem)}")
                lines.append(f"  - 提出者/来源: {theorem.proposer}")
                if theorem.source_domain:
                    lines.append(f"  - 原始领域标签: {theorem.source_domain}")
                append_discipline_specific_lines(lines, theorem)
                lines.append("  - 现有工件链接: 待补充")
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
    )


if __name__ == "__main__":
    main()
