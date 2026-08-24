#!/usr/bin/env python3
"""Extract a pinned, auditable Stage 5 theorem source set from mathlib.

This extractor deliberately does *not* treat every proposition in mathlib as an
important mathematical theorem.  A declaration must have at least one of these
human-curation signals:

* it is linked from mathlib's ``docs/1000.yaml`` (the 1000+ Theorems project), or
* it is named in a bullet under a module-doc heading containing ``Main results``,
  ``Main theorems``, or ``Main statements``.

The ``.ilean`` index supplies the declaring module and exact source range.  Lean
then loads the compiled ``.olean`` and independently reports the declaration
kind, formal type, and declaration docstring.  Only constants that Lean reports
as ``ConstantInfo.thmInfo`` survive.  Consequently the output is a source
artifact with formal proof evidence, not a regex-only inventory.

Typical use (from the repository root)::

    python3 Docs/tools/extract_mathlib_theorems_v5.py \
      --output /tmp/Mathlib_Theorems_v5.json

The defaults require 1,000 baseline records and 500 dynamic-expansion records.
The output is deterministic for a fixed repository checkout, mathlib commit,
build cache, and optional 1000+ checkout.  It intentionally contains no wall
clock timestamp.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import dataclasses
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from typing import Any, Iterable, Iterator, Sequence

import yaml


SCHEMA_VERSION = "awesome-theorems/mathlib-theorem-source/1.0"
GENERATOR_VERSION = "1.1.0"

# A coarse, explicitly-labelled crosswalk.  Exact MSC data from the 1000+
# checkout, when supplied, always takes precedence for the linked record.
MODULE_ROOT_TO_MSC2020: dict[str, tuple[str, str]] = {
    "Algebra": ("08", "General algebraic systems"),
    "AlgebraicGeometry": ("14", "Algebraic geometry"),
    "AlgebraicTopology": ("55", "Algebraic topology"),
    "Analysis": ("26", "Real functions and analysis"),
    "CategoryTheory": ("18", "Category theory; homological algebra"),
    "Combinatorics": ("05", "Combinatorics"),
    "Computability": ("68", "Computer science (computability)"),
    "Condensed": ("18", "Category theory; homological algebra"),
    "Data": ("00", "General and overarching topics"),
    "Dynamics": ("37", "Dynamical systems and ergodic theory"),
    "FieldTheory": ("12", "Field theory and polynomials"),
    "Geometry": ("51", "Geometry"),
    "GroupTheory": ("20", "Group theory and generalizations"),
    "InformationTheory": ("94", "Information and communication"),
    "LinearAlgebra": ("15", "Linear and multilinear algebra; matrix theory"),
    "Logic": ("03", "Mathematical logic and foundations"),
    "MeasureTheory": ("28", "Measure and integration"),
    "ModelTheory": ("03", "Mathematical logic and foundations"),
    "NumberTheory": ("11", "Number theory"),
    "Order": ("06", "Order, lattices, ordered algebraic structures"),
    "Probability": ("60", "Probability theory and stochastic processes"),
    "RepresentationTheory": ("20", "Group theory and generalizations"),
    "RingTheory": ("16", "Associative rings and algebras"),
    "SetTheory": ("03", "Mathematical logic and foundations"),
    "Topology": ("54", "General topology"),
}

DECLARATION_KINDS = (
    "theorem",
    "lemma",
    "def",
    "abbrev",
    "opaque",
    "axiom",
    "structure",
    "class",
    "inductive",
    "instance",
)
DECLARATION_KIND_RE = re.compile(r"\b(" + "|".join(DECLARATION_KINDS) + r")\b")
MAIN_HEADING_MARKERS = ("main result", "main theorem", "main statement")
INLINE_CODE_RE = re.compile(r"`([^`\n]+)`")
EXPLICIT_RESULT_TERMS = (
    "theorem",
    "lemma",
    "inequality",
    "identity",
    "formula",
    "law",
    "principle",
    "criterion",
    "classification",
    "reciprocity",
    "decomposition",
    "duality",
    "fixed-point",
    "fixed point",
)


class ExtractionError(RuntimeError):
    """An input or verification invariant failed."""


@dataclasses.dataclass(frozen=True)
class DeclarationIndexEntry:
    name: str
    module: str
    source_path: Path
    source_rel: str
    ilean_path: Path
    olean_path: Path
    ranges: tuple[int, int, int, int, int, int, int, int]
    source_syntax_kind: str | None
    source_header_year: int | None


@dataclasses.dataclass
class Candidate:
    entry: DeclarationIndexEntry
    signals: list[dict[str, Any]] = dataclasses.field(default_factory=list)


@dataclasses.dataclass(frozen=True)
class ModuleCacheInventory:
    """A complete one-to-one source/ilean/olean module inventory."""

    source_count: int
    ilean_count: int
    olean_count: int
    ilean_paths: tuple[Path, ...]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def run_text(args: Sequence[str], cwd: Path, *, input_text: str | None = None,
             timeout: int | None = None) -> str:
    completed = subprocess.run(
        list(args),
        cwd=cwd,
        input=input_text,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
        check=False,
    )
    if completed.returncode != 0:
        raise ExtractionError(
            f"command failed ({completed.returncode}): {' '.join(args)}\n"
            f"stdout:\n{completed.stdout}\n"
            f"stderr:\n{completed.stderr}"
        )
    return completed.stdout.strip()


def infer_repo_root(script_path: Path) -> Path:
    # Docs/tools/<this file> -> repository root
    return script_path.resolve().parents[2]


def source_path_for_module(mathlib_root: Path, module: str) -> Path:
    pieces = module.split(".")
    if not pieces or pieces[0] != "Mathlib":
        raise ExtractionError(f"unexpected non-Mathlib module in index: {module}")
    return mathlib_root.joinpath(*pieces).with_suffix(".lean")


def declaration_syntax_kind(lines: list[str], ranges: Sequence[int]) -> str | None:
    """Find the declaration command immediately preceding the selected name.

    ``.ilean`` positions are zero-based.  The selection start points at the
    declaration name, so the last declaration keyword before that point is much
    more reliable than searching the whole range (whose docstring may itself
    contain words such as "theorem" or "lemma").
    """

    start_line, _, _, _, selection_line, selection_col, _, _ = ranges
    if start_line < 0 or selection_line >= len(lines) or start_line > selection_line:
        return None
    prefix_lines = lines[start_line:selection_line]
    prefix_lines.append(lines[selection_line][:selection_col])
    matches = list(DECLARATION_KIND_RE.finditer("\n".join(prefix_lines)))
    return matches[-1].group(1) if matches else None


def source_header_year(source_text: str) -> int | None:
    match = re.search(r"Copyright\s*\(c\)\s*(\d{4})", source_text[:1200])
    return int(match.group(1)) if match else None


def validate_complete_module_cache(mathlib_root: Path) -> ModuleCacheInventory:
    """Require every Mathlib source module to have matching index/object files.

    A partial ``lake exe cache get`` used to change the screened universe while
    still allowing a superficially valid artifact to be emitted.  Comparing
    relative module-name sets (rather than counts alone) also rejects a stale
    cache where one missing module is masked by one removed module.
    """

    source_root = mathlib_root / "Mathlib"
    build_root = mathlib_root / ".lake" / "build" / "lib" / "lean" / "Mathlib"
    if not source_root.is_dir() or not build_root.is_dir():
        raise ExtractionError(
            f"mathlib source/build roots are unavailable: {source_root}, {build_root}"
        )

    def keyed(paths: Iterable[Path], root: Path) -> dict[str, Path]:
        return {
            path.relative_to(root).with_suffix("").as_posix(): path
            for path in paths
        }

    sources = keyed(source_root.rglob("*.lean"), source_root)
    ileans = keyed(build_root.rglob("*.ilean"), build_root)
    oleans = keyed(build_root.rglob("*.olean"), build_root)
    source_names = set(sources)
    ilean_names = set(ileans)
    olean_names = set(oleans)
    if source_names != ilean_names or source_names != olean_names:
        problems: list[str] = []
        comparisons = (
            ("missing .ilean", source_names - ilean_names),
            ("missing .olean", source_names - olean_names),
            ("cache-only .ilean", ilean_names - source_names),
            ("cache-only .olean", olean_names - source_names),
        )
        for label, names in comparisons:
            if names:
                examples = ", ".join(sorted(names)[:5])
                suffix = " ..." if len(names) > 5 else ""
                problems.append(f"{label} ({len(names)}): {examples}{suffix}")
        raise ExtractionError(
            "mathlib module cache is incomplete or stale: "
            f"source={len(sources)}, ilean={len(ileans)}, olean={len(oleans)}; "
            + "; ".join(problems)
        )
    return ModuleCacheInventory(
        source_count=len(sources),
        ilean_count=len(ileans),
        olean_count=len(oleans),
        ilean_paths=tuple(ileans[name] for name in sorted(ileans)),
    )


def load_declaration_index(
    mathlib_root: Path,
) -> tuple[dict[str, DeclarationIndexEntry], ModuleCacheInventory]:
    inventory = validate_complete_module_cache(mathlib_root)

    result: dict[str, DeclarationIndexEntry] = {}
    source_cache: dict[Path, tuple[list[str], int | None]] = {}
    for ilean_path in inventory.ilean_paths:
        try:
            payload = json.loads(ilean_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ExtractionError(f"cannot parse {ilean_path}: {exc}") from exc
        module = payload.get("module")
        if not isinstance(module, str) or not module.startswith("Mathlib."):
            continue
        source_path = source_path_for_module(mathlib_root, module)
        if not source_path.is_file():
            raise ExtractionError(f"indexed source file is missing: {source_path}")
        if source_path not in source_cache:
            source_text = source_path.read_text(encoding="utf-8")
            source_cache[source_path] = (source_text.splitlines(), source_header_year(source_text))
        lines, year = source_cache[source_path]
        olean_path = ilean_path.with_suffix(".olean")
        if not olean_path.is_file():
            # A candidate without its compiled theorem constant cannot pass the
            # later Lean gate, so it must not enter the index.
            continue
        declarations = payload.get("decls", {})
        if not isinstance(declarations, dict):
            raise ExtractionError(f"invalid decls map in {ilean_path}")
        for name, raw_ranges in declarations.items():
            if (
                not isinstance(name, str)
                or not isinstance(raw_ranges, list)
                or len(raw_ranges) != 8
                or not all(isinstance(value, int) for value in raw_ranges)
            ):
                raise ExtractionError(f"invalid declaration range for {name!r} in {ilean_path}")
            ranges = tuple(raw_ranges)
            source_rel = source_path.relative_to(mathlib_root).as_posix()
            result[name] = DeclarationIndexEntry(
                name=name,
                module=module,
                source_path=source_path,
                source_rel=source_rel,
                ilean_path=ilean_path,
                olean_path=olean_path,
                ranges=ranges,  # type: ignore[arg-type]
                source_syntax_kind=declaration_syntax_kind(lines, ranges),
                source_header_year=year,
            )
    return result, inventory


def first_module_docstring(source_text: str) -> str | None:
    match = re.search(r"/-!(.*?)-/", source_text, re.DOTALL)
    return match.group(1) if match else None


def clean_inline_identifier(raw: str) -> str:
    return raw.strip().rstrip(".,:;")


def iter_main_doc_bullets(module_doc: str) -> Iterator[tuple[str, str]]:
    """Yield ``(heading, exact bullet text)`` from curated Main-* sections."""

    active = False
    active_level = 0
    active_heading = ""
    bullet: list[str] | None = None

    def finish() -> tuple[str, str] | None:
        if bullet is None:
            return None
        text = " ".join(part.strip() for part in bullet if part.strip()).strip()
        return (active_heading, text) if text else None

    for line in module_doc.splitlines() + ["# END"]:
        heading_match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if heading_match:
            finished = finish()
            if finished is not None:
                yield finished
            bullet = None
            level = len(heading_match.group(1))
            heading = heading_match.group(2).strip()
            if active and level <= active_level:
                active = False
            if any(marker in heading.casefold() for marker in MAIN_HEADING_MARKERS):
                active = True
                active_level = level
                active_heading = heading
            continue
        if not active:
            continue
        bullet_match = re.match(r"^\s*[-*]\s+(.+)", line)
        if bullet_match:
            finished = finish()
            if finished is not None:
                yield finished
            bullet = [bullet_match.group(1).strip()]
        elif bullet is not None and line.strip():
            bullet.append(line.strip())


def signal_key(signal: dict[str, Any]) -> str:
    return json.dumps(signal, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def add_signal(candidates: dict[str, Candidate], index: dict[str, DeclarationIndexEntry],
               name: str, signal: dict[str, Any]) -> None:
    entry = index.get(name)
    if entry is None or entry.source_syntax_kind not in {"theorem", "lemma"}:
        return
    candidate = candidates.setdefault(name, Candidate(entry=entry))
    encoded = signal_key(signal)
    if all(signal_key(existing) != encoded for existing in candidate.signals):
        candidate.signals.append(signal)


def collect_main_doc_signals(mathlib_root: Path, index: dict[str, DeclarationIndexEntry],
                             candidates: dict[str, Candidate]) -> None:
    modules: dict[str, Path] = {}
    for entry in index.values():
        modules.setdefault(entry.module, entry.source_path)
    for module, source_path in sorted(modules.items()):
        source_text = source_path.read_text(encoding="utf-8")
        module_doc = first_module_docstring(source_text)
        if module_doc is None:
            continue
        for heading, description in iter_main_doc_bullets(module_doc):
            if len(description) < 40 or "todo" in description.casefold():
                continue
            for raw_name in INLINE_CODE_RE.findall(description):
                name = clean_inline_identifier(raw_name)
                if name not in index:
                    continue
                add_signal(
                    candidates,
                    index,
                    name,
                    {
                        "kind": "mathlib_module_main_result",
                        "module": module,
                        "heading": heading,
                        "description": description,
                        "source_path": source_path.relative_to(mathlib_root).as_posix(),
                    },
                )


def thousand_yaml_declaration_names(entry: dict[str, Any]) -> list[str]:
    if "decl" in entry:
        return [str(entry["decl"])]
    if "decls" in entry:
        raw = entry["decls"]
        if not isinstance(raw, list):
            raise ExtractionError(f"1000.yaml decls is not a list: {entry!r}")
        return [str(value) for value in raw]
    # A `statement` entry is intentionally not accepted as proof evidence.
    return []


def load_thousand_plus_metadata(root: Path | None) -> tuple[dict[str, dict[str, Any]], str | None]:
    if root is None:
        return {}, None
    theorem_dir = root / "_thm"
    if not theorem_dir.is_dir():
        raise ExtractionError(f"1000+ checkout lacks _thm/: {root}")
    commit = run_text(["git", "rev-parse", "HEAD"], root)
    result: dict[str, dict[str, Any]] = {}
    for path in sorted(theorem_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        parts = re.split(r"^---\s*$", text, flags=re.MULTILINE)
        if len(parts) < 3:
            raise ExtractionError(f"invalid 1000+ front matter: {path}")
        data = yaml.safe_load(parts[1])
        if not isinstance(data, dict) or "wikidata" not in data:
            raise ExtractionError(f"invalid 1000+ record: {path}")
        key = str(data["wikidata"]) + str(data.get("id_suffix", ""))
        title = next(
            (line[2:].strip() for line in text.splitlines() if line.startswith("# ")),
            None,
        )
        result[key] = {
            "title": title,
            "msc_classification": str(data.get("msc_classification", "")) or None,
            "wikipedia_links": data.get("wikipedia_links", []),
        }
    return result, commit


def collect_docs_1000_signals(mathlib_root: Path, index: dict[str, DeclarationIndexEntry],
                              candidates: dict[str, Candidate],
                              thousand_plus: dict[str, dict[str, Any]]) -> None:
    path = mathlib_root / "docs" / "1000.yaml"
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ExtractionError(f"invalid 1000.yaml mapping: {path}")
    for external_id, raw_entry in payload.items():
        if not isinstance(raw_entry, dict) or "title" not in raw_entry:
            raise ExtractionError(f"invalid 1000.yaml entry {external_id!r}")
        external_key = str(external_id)
        upstream = thousand_plus.get(external_key, {})
        for name in thousand_yaml_declaration_names(raw_entry):
            signal: dict[str, Any] = {
                "kind": "mathlib_1000_theorems",
                "external_id": external_key,
                "title": str(raw_entry["title"]),
                "source_path": "docs/1000.yaml",
                "formalization_status": "formalized",
            }
            if upstream:
                signal["upstream_title"] = upstream.get("title")
                signal["msc2020"] = upstream.get("msc_classification")
                signal["wikipedia_links"] = upstream.get("wikipedia_links", [])
            add_signal(candidates, index, name, signal)


def has_signal(candidate: Candidate, kind: str) -> bool:
    return any(signal.get("kind") == kind for signal in candidate.signals)


def exact_summary(candidate: Candidate) -> str:
    docs = [
        str(signal["title"])
        for signal in candidate.signals
        if signal.get("kind") == "mathlib_1000_theorems" and signal.get("title")
    ]
    if docs:
        return docs[0]
    module_summary = module_main_summary(candidate)
    if module_summary is None:
        raise ExtractionError(f"candidate has no readable importance signal: {candidate.entry.name}")
    return module_summary


def module_main_summary(candidate: Candidate) -> str | None:
    module_descriptions = [
        str(signal["description"])
        for signal in candidate.signals
        if signal.get("kind") == "mathlib_module_main_result" and signal.get("description")
    ]
    return module_descriptions[0] if module_descriptions else None


def lean_kind_expression() -> str:
    return """match ci with
      | .thmInfo _ => \"theorem\"
      | .axiomInfo _ => \"axiom\"
      | .defnInfo _ => \"definition\"
      | .opaqueInfo _ => \"opaque\"
      | .quotInfo _ => \"quotient\"
      | .inductInfo _ => \"inductive\"
      | .ctorInfo _ => \"constructor\"
      | .recInfo _ => \"recursor\"
"""


def lean_batch_source(modules: Sequence[str], names: Sequence[str]) -> str:
    imports = "\n".join(f"import {module}" for module in modules)
    encoded_names = ", ".join(json.dumps(name, ensure_ascii=False) for name in names)
    return f"""{imports}
import Lean.DocString
import Lean.Util.CollectAxioms

open Lean Elab Command

run_cmd Lean.Elab.Command.liftTermElabM do
  let env ← getEnv
  let rawNames : Array String := #[{encoded_names}]
  let names := rawNames.map String.toName
  -- Reuse one traversal state for the batch.  Calling `collectAxioms`
  -- separately for every theorem repeatedly walks the same dependency DAG.
  -- Absence of `sorryAx` from the union proves its absence for every member.
  let (_, axiomState) := ((names.forM Lean.CollectAxioms.collect).run env).run {{}}
  let axiomNames := axiomState.axioms.map Name.toString |>.qsort (· < ·)
  let usesSorry := axiomState.axioms.contains ``sorryAx
  for rawName in rawNames do
    let n := rawName.toName
    let some ci := env.find? n | throwError m!\"missing declaration {{n}}\"
    let kind := {lean_kind_expression()}
    let formalType ← Meta.ppExpr ci.type
    let docstring ← findDocString? env n
    let out := Json.mkObj [
      (\"name\", toJson rawName),
      (\"runtime_kind\", toJson kind),
      (\"formal_type\", toJson (toString formalType)),
      (\"declaration_docstring\", toJson docstring),
      (\"axiom_dependencies\", toJson axiomNames),
      (\"uses_sorry\", toJson usesSorry)
    ]
    IO.println out.compress
"""


def chunk_modules(module_to_names: dict[str, list[str]], batch_modules: int) -> list[tuple[list[str], list[str]]]:
    modules = sorted(module_to_names)
    batches: list[tuple[list[str], list[str]]] = []
    for start in range(0, len(modules), batch_modules):
        batch = modules[start:start + batch_modules]
        names = sorted(name for module in batch for name in module_to_names[module])
        batches.append((batch, names))
    return batches


def run_lean_batch(lean_project: Path, batch: tuple[list[str], list[str]], timeout: int) -> dict[str, dict[str, Any]]:
    modules, names = batch
    source = lean_batch_source(modules, names)
    stdout = run_text(
        ["lake", "env", "lean", "--stdin"],
        lean_project,
        input_text=source,
        timeout=timeout,
    )
    result: dict[str, dict[str, Any]] = {}
    for line in stdout.splitlines():
        stripped = line.strip()
        if not stripped.startswith("{"):
            continue
        try:
            record = json.loads(stripped)
        except json.JSONDecodeError:
            continue
        name = record.get("name")
        if isinstance(name, str):
            result[name] = record
    missing = sorted(set(names) - set(result))
    if missing:
        raise ExtractionError(
            f"Lean batch for {modules[0]}..{modules[-1]} omitted {len(missing)} declarations: "
            + ", ".join(missing[:12])
        )
    return result


def extract_with_lean(lean_project: Path, candidates: dict[str, Candidate], *,
                      batch_modules: int, jobs: int, timeout: int) -> dict[str, dict[str, Any]]:
    module_to_names: dict[str, list[str]] = {}
    for name, candidate in candidates.items():
        module_to_names.setdefault(candidate.entry.module, []).append(name)
    batches = chunk_modules(module_to_names, batch_modules)
    merged: dict[str, dict[str, Any]] = {}
    if jobs == 1:
        for batch in batches:
            merged.update(run_lean_batch(lean_project, batch, timeout))
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as executor:
            futures = [executor.submit(run_lean_batch, lean_project, batch, timeout) for batch in batches]
            for future in concurrent.futures.as_completed(futures):
                merged.update(future.result())
    return merged


def explicit_result_signal(candidate: Candidate) -> bool:
    for signal in candidate.signals:
        text = " ".join(
            str(signal.get(key, "")) for key in ("title", "upstream_title", "description")
        ).casefold()
        if any(term in text for term in EXPLICIT_RESULT_TERMS):
            return True
    return False


def exact_msc(candidate: Candidate) -> tuple[str, str] | None:
    exact_codes = [
        str(signal["msc2020"])
        for signal in candidate.signals
        if signal.get("msc2020")
    ]
    if exact_codes:
        return exact_codes[0], "1000_plus_curated"
    pieces = candidate.entry.module.split(".")
    root = pieces[1] if len(pieces) > 1 else ""
    mapped = MODULE_ROOT_TO_MSC2020.get(root)
    if mapped:
        return mapped[0], "mathlib_module_root_crosswalk"
    return None


def baseline_sort_key(item: tuple[Candidate, dict[str, Any]]) -> tuple[Any, ...]:
    candidate, lean = item
    return (
        -int(has_signal(candidate, "mathlib_1000_theorems")),
        -int(explicit_result_signal(candidate)),
        -int(bool(lean.get("declaration_docstring"))),
        -int(candidate.entry.source_syntax_kind == "theorem"),
        -min(len(exact_summary(candidate)), 1000),
        candidate.entry.module,
        candidate.entry.name,
    )


def dynamic_sort_key(item: tuple[Candidate, dict[str, Any]]) -> tuple[Any, ...]:
    candidate, lean = item
    year = candidate.entry.source_header_year or 0
    return (
        -int(year >= 2023),
        -year,
        -int(bool(lean.get("declaration_docstring"))),
        -int(explicit_result_signal(candidate)),
        -int(candidate.entry.source_syntax_kind == "theorem"),
        candidate.entry.module,
        candidate.entry.name,
    )


def build_record(candidate: Candidate, lean: dict[str, Any], *, rank: int, cohort: str,
                 commit: str, mathlib_root: Path, hash_cache: dict[Path, str]) -> dict[str, Any]:
    entry = candidate.entry

    def digest(path: Path) -> str:
        if path not in hash_cache:
            hash_cache[path] = sha256_file(path)
        return hash_cache[path]

    range_start_line, range_start_col, range_end_line, range_end_col, \
        selection_start_line, selection_start_col, selection_end_line, selection_end_col = entry.ranges
    # `.ilean` is zero-based; GitHub and human-facing locators are one-based.
    human_start = range_start_line + 1
    human_end = range_end_line + 1
    source_url = (
        "https://github.com/leanprover-community/mathlib4/blob/"
        f"{commit}/{entry.source_rel}#L{human_start}-L{human_end}"
    )
    msc = exact_msc(candidate)
    formal_type = str(lean["formal_type"])
    declaration_docstring = lean.get("declaration_docstring")
    if declaration_docstring:
        formal_docstring = str(declaration_docstring)
        formal_docstring_origin = "declaration_docstring"
    else:
        # Every selected record without a declaration-level docstring is
        # required by the selection gate to occur in a Main-* module docstring.
        formal_docstring = module_main_summary(candidate)
        if formal_docstring is None:
            raise ExtractionError(
                f"selected declaration has no formal docstring source: {entry.name}"
            )
        formal_docstring_origin = "module_main_result_docstring"
    record_id = "ML4-" + hashlib.sha256(
        f"{commit}\0{entry.name}".encode("utf-8")
    ).hexdigest()[:20].upper()
    record: dict[str, Any] = {
        "source_record_id": record_id,
        "selection_rank": rank,
        "selection_cohort": cohort,
        "declaration": entry.name,
        "declaration_kind": entry.source_syntax_kind,
        "raw_category": entry.source_syntax_kind,
        "raw_status": "lean_checked_thmInfo_sorry_free",
        "formal_proof_state": "kernel_checked_sorry_free",
        "source_syntax_kind": entry.source_syntax_kind,
        "display_label": next(
            (
                str(signal["title"])
                for signal in candidate.signals
                if signal.get("kind") == "mathlib_1000_theorems" and signal.get("title")
            ),
            entry.name,
        ),
        "exact_curated_summary": exact_summary(candidate),
        "declaration_docstring": declaration_docstring,
        "formal_docstring": formal_docstring,
        "formal_docstring_origin": formal_docstring_origin,
        "formal_docstring_sha256": sha256_bytes(formal_docstring.encode("utf-8")),
        "formal_type": formal_type,
        "formal_type_sha256": sha256_bytes(formal_type.encode("utf-8")),
        "material_status": {
            "status": "proved_formal",
            "basis": "Loaded from the pinned compiled mathlib environment as Lean.ConstantInfo.thmInfo.",
            "as_of_commit": commit,
        },
        "proof_evidence": {
            "verification": "lean_checked_environment_thmInfo_and_collectAxioms_without_sorryAx",
            "batch_axiom_dependency_union": lean.get("axiom_dependencies", []),
            "uses_sorry": lean.get("uses_sorry"),
            "compiled_module": entry.module,
            "olean_path": entry.olean_path.relative_to(mathlib_root).as_posix(),
            "olean_sha256": digest(entry.olean_path),
            "ilean_path": entry.ilean_path.relative_to(mathlib_root).as_posix(),
            "ilean_sha256": digest(entry.ilean_path),
        },
        "source": {
            "module": entry.module,
            "path": entry.source_rel,
            "source_sha256": digest(entry.source_path),
            "url": source_url,
            "range": {
                "line_start": human_start,
                "column_start_zero_based": range_start_col,
                "line_end": human_end,
                "column_end_zero_based": range_end_col,
            },
            "selection_range": {
                "line_start": selection_start_line + 1,
                "column_start_zero_based": selection_start_col,
                "line_end": selection_end_line + 1,
                "column_end_zero_based": selection_end_col,
            },
            "header_copyright_year": entry.source_header_year,
        },
        "importance_signals": sorted(candidate.signals, key=signal_key),
        "rights": {
            "source_license": "Apache-2.0",
            "use": "formal_statement_docstring_and_bibliographic_metadata",
            "attribution": "The mathlib Community",
        },
    }
    if msc:
        code, basis = msc
        record["msc2020"] = {"code": code, "basis": basis}
    return record


def canonical_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def build_artifact(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = args.repo_root.resolve()
    lean_project = repo_root / "Formalizations" / "Lean"
    mathlib_root = lean_project / ".lake" / "packages" / "mathlib"
    commit = run_text(["git", "rev-parse", "HEAD"], mathlib_root)
    dirty = run_text(["git", "status", "--porcelain"], mathlib_root)
    if dirty:
        raise ExtractionError("the pinned mathlib checkout is dirty; refusing non-reproducible extraction")
    commit_date = run_text(["git", "show", "-s", "--format=%cI", "HEAD"], mathlib_root)
    lean_version = run_text(["lean", "--version"], lean_project).splitlines()[0]
    lake_version = run_text(["lake", "--version"], lean_project).splitlines()[0]

    thousand_plus_root = args.thousand_plus_root.resolve() if args.thousand_plus_root else None
    thousand_plus, thousand_plus_commit = load_thousand_plus_metadata(thousand_plus_root)

    declaration_index, module_inventory = load_declaration_index(mathlib_root)
    candidates: dict[str, Candidate] = {}
    collect_main_doc_signals(mathlib_root, declaration_index, candidates)
    collect_docs_1000_signals(mathlib_root, declaration_index, candidates, thousand_plus)
    if len(candidates) < args.baseline_count + args.dynamic_count:
        raise ExtractionError(
            f"only {len(candidates)} source-screened candidates; "
            f"need {args.baseline_count + args.dynamic_count}"
        )

    lean_records = extract_with_lean(
        lean_project,
        candidates,
        batch_modules=args.batch_modules,
        jobs=args.jobs,
        timeout=args.batch_timeout,
    )
    verified: list[tuple[Candidate, dict[str, Any]]] = []
    runtime_rejected: list[dict[str, str]] = []
    for name, candidate in sorted(candidates.items()):
        lean = lean_records[name]
        has_formal_docstring = bool(lean.get("declaration_docstring")) or has_signal(
            candidate, "mathlib_module_main_result"
        )
        if (
            lean.get("runtime_kind") == "theorem"
            and lean.get("uses_sorry") is False
            and has_formal_docstring
        ):
            verified.append((candidate, lean))
        else:
            rejection_reason = (
                "not_thmInfo" if lean.get("runtime_kind") != "theorem"
                else "uses_sorryAx" if lean.get("uses_sorry") is not False
                else "no_declaration_or_module_main_docstring"
            )
            runtime_rejected.append({
                "declaration": name,
                "runtime_kind": str(lean.get("runtime_kind")),
                "uses_sorry": str(lean.get("uses_sorry")),
                "reason": rejection_reason,
            })

    required = args.baseline_count + args.dynamic_count
    if len(verified) < required:
        raise ExtractionError(
            f"only {len(verified)} candidates survived Lean's thmInfo gate; need {required}"
        )

    baseline_sorted = sorted(verified, key=baseline_sort_key)
    baseline = baseline_sorted[:args.baseline_count]
    baseline_names = {candidate.entry.name for candidate, _ in baseline}
    remaining = [item for item in verified if item[0].entry.name not in baseline_names]
    dynamic = sorted(remaining, key=dynamic_sort_key)[:args.dynamic_count]
    selected = [(item, "baseline") for item in baseline] + [
        (item, "dynamic_expansion") for item in dynamic
    ]

    hash_cache: dict[Path, str] = {}
    records = [
        build_record(
            candidate,
            lean,
            rank=rank,
            cohort=cohort,
            commit=commit,
            mathlib_root=mathlib_root,
            hash_cache=hash_cache,
        )
        for rank, ((candidate, lean), cohort) in enumerate(selected, start=1)
    ]
    documented = sum(record["declaration_docstring"] is not None for record in records)
    docs_1000_count = sum(
        any(signal["kind"] == "mathlib_1000_theorems" for signal in record["importance_signals"])
        for record in records
    )
    module_main_count = sum(
        any(signal["kind"] == "mathlib_module_main_result" for signal in record["importance_signals"])
        for record in records
    )
    roots: dict[str, int] = {}
    for record in records:
        pieces = record["source"]["module"].split(".")
        root = pieces[1] if len(pieces) > 1 else pieces[0]
        roots[root] = roots.get(root, 0) + 1

    artifact: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "generator": {
            "path": "Docs/tools/extract_mathlib_theorems_v5.py",
            "version": GENERATOR_VERSION,
        },
        "source_snapshot": {
            "repository": "https://github.com/leanprover-community/mathlib4.git",
            "commit": commit,
            "commit_date": commit_date,
            "license": "Apache-2.0",
            "license_sha256": sha256_file(mathlib_root / "LICENSE"),
            "citation": "The mathlib Community, The Lean Mathematical Library, CPP 2020",
            "lean_version": lean_version,
            "lake_version": lake_version,
            "available_source_modules": module_inventory.source_count,
            "available_ilean_modules": module_inventory.ilean_count,
            "available_olean_modules": module_inventory.olean_count,
            "module_cache_complete": True,
        },
        "optional_thousand_plus_snapshot": (
            {
                "repository": "https://github.com/1000-plus/1000-plus.github.io.git",
                "commit": thousand_plus_commit,
                "license": "Unlicense",
                "records_loaded": len(thousand_plus),
            }
            if thousand_plus_commit
            else None
        ),
        "selection_policy": {
            "truth_gate": (
                "Lean runtime reports ConstantInfo.thmInfo from the pinned checked environment, "
                "and transitive collectAxioms does not contain sorryAx"
            ),
            "importance_gate_any_of": [
                "mathlib docs/1000.yaml formalized declaration",
                "declaration named in a module-doc Main results/theorems/statements bullet",
            ],
            "excluded": [
                "statement-only docs/1000 entries",
                "definitions, axioms, opaque constants, instances, structures, and inductives",
                "Main-section bullets shorter than 40 characters or marked TODO",
                "records lacking both a declaration docstring and a Main-section module docstring",
            ],
            "baseline_count": args.baseline_count,
            "dynamic_expansion_count": args.dynamic_count,
            "dynamic_ordering": "recent source header year, then documentation and explicit-result signals",
        },
        "counts": {
            "indexed_declarations": len(declaration_index),
            "source_screened_candidates": len(candidates),
            "lean_verified_theorem_candidates": len(verified),
            "runtime_rejected": len(runtime_rejected),
            "selected_total": len(records),
            "selected_baseline": args.baseline_count,
            "selected_dynamic_expansion": args.dynamic_count,
            "selected_with_declaration_docstring": documented,
            "selected_with_module_main_signal": module_main_count,
            "selected_with_docs_1000_signal": docs_1000_count,
            "selected_by_module_root": dict(sorted(roots.items())),
            "verified_reserve_after_selection": len(verified) - len(records),
        },
        "runtime_rejections": runtime_rejected,
        "records": records,
    }
    artifact_without_digest = canonical_json_bytes(artifact)
    artifact["content_digest_before_self_field"] = sha256_bytes(artifact_without_digest)
    return artifact


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=infer_repo_root(Path(__file__)),
        help="awesome_theorems repository root (auto-detected by default)",
    )
    parser.add_argument("--output", required=True, type=Path, help="JSON artifact to write or check")
    parser.add_argument(
        "--thousand-plus-root",
        type=Path,
        help="optional fixed checkout of 1000-plus/1000-plus.github.io for exact MSC metadata",
    )
    parser.add_argument("--baseline-count", type=int, default=1000)
    parser.add_argument("--dynamic-count", type=int, default=500)
    parser.add_argument("--batch-modules", type=int, default=30)
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--batch-timeout", type=int, default=300)
    parser.add_argument(
        "--check",
        action="store_true",
        help="compare the generated bytes with --output instead of writing",
    )
    args = parser.parse_args(argv)
    for name in ("baseline_count", "dynamic_count", "batch_modules", "jobs", "batch_timeout"):
        if getattr(args, name) <= 0:
            parser.error(f"--{name.replace('_', '-')} must be positive")
    return args


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        artifact = build_artifact(args)
        data = canonical_json_bytes(artifact)
        output = args.output.resolve()
        if args.check:
            if not output.is_file():
                raise ExtractionError(f"--check target does not exist: {output}")
            current = output.read_bytes()
            if current != data:
                raise ExtractionError(
                    f"artifact drift: {output} has sha256={sha256_bytes(current)}, "
                    f"generated sha256={sha256_bytes(data)}"
                )
            action = "checked"
        else:
            output.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(
                mode="wb", prefix=output.name + ".", suffix=".tmp", dir=output.parent, delete=False
            ) as handle:
                temp_path = Path(handle.name)
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temp_path, output)
            action = "wrote"
        counts = artifact["counts"]
        print(
            f"{action} {output}: selected={counts['selected_total']} "
            f"baseline={counts['selected_baseline']} dynamic={counts['selected_dynamic_expansion']} "
            f"verified_pool={counts['lean_verified_theorem_candidates']} "
            f"sha256={sha256_bytes(data)}"
        )
        return 0
    except (ExtractionError, OSError, subprocess.TimeoutExpired, yaml.YAMLError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
