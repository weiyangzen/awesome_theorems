#!/usr/bin/env python3
"""Freeze the complete 1962--2025 Putnam source denominator.

The repository artifacts produced here are deliberately prose-free.  They
bind all 1,051 PutnamGAP rows and all twelve 2025 Kedlaya rows to immutable
archive bytes, exact field/item spans, and hashes, then project them onto the
768-coordinate Putnam grid.  The original problem and solution text remains
in operator-supplied external archives.

``--write`` and ``--audit-source-archives`` require both pinned archives.
``--check`` is repository-only and independently replays every manifest,
candidate, projection, rights, count, and digest invariant without access to
the copyrighted source prose.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import sys
import tarfile
import tempfile
from typing import Any, Iterable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[4]
OUTPUT_DIR_REL = Path("Docs/catalog/v5/curation/putnambench_v5_6")
INVENTORY_REL = OUTPUT_DIR_REL / "Full_Putnam_Source_Inventory_v5_6.json"
CANDIDATES_REL = OUTPUT_DIR_REL / "Full_Putnam_Source_Candidates_v5_6.jsonl"
PROBLEMS_REL = OUTPUT_DIR_REL / "Full_Putnam_Seed_Problems_v5_6.jsonl"
PUTNAMGAP_MANIFEST_REL = OUTPUT_DIR_REL / "PutnamGAP_Source_Locator_Manifest_v5_6.jsonl"
KEDLAYA_MANIFEST_REL = OUTPUT_DIR_REL / "Kedlaya_2025_Source_Locator_Manifest_v5_6.jsonl"
PB_INVENTORY_REL = OUTPUT_DIR_REL / "PutnamBench_Source_Inventory_v5_6.json"
PB_PROBLEMS_REL = OUTPUT_DIR_REL / "PutnamBench_Source_Problems_v5_6.jsonl"

PB_AUTHORITY = "2cc7b0be42fb242a750d3eda12e1437fb7486c26a55bfef01ed76e32e1d31049"
PB_INVENTORY_SHA256 = "f8407e1aefe39daea09bfa4f940533130139e2e6c65a2eff3e0688d68013ff95"
PB_PROBLEMS_SHA256 = "85727d9216226b14be5bc52a2a7cf8aad11d3834ca10192acb4df1331631889d"
FULL_SOURCE_AUTHORITY = "08fb966f533d6ab0f29b08f02ef55de77752f20471bcec3c65915a518df7df84"

PUTNAMGAP_REPOSITORY = "https://github.com/YurenHao0426/PutnamGAP"
PUTNAMGAP_COMMIT = "aee05407afc7e621e8d9c7f909f4f25ccb8131c0"
PUTNAMGAP_TREE = "0f55aee4f4b911e767785a7c5977fbe36f58dbbe"
PUTNAMGAP_DATASET_TREE = "b63f9d05c18f3c51347b4cda8c45ef41e7385060"
PUTNAMGAP_ARCHIVE_ROOT = f"PutnamGAP-{PUTNAMGAP_COMMIT}"
PUTNAMGAP_ARCHIVE_URL = (
    "https://codeload.github.com/YurenHao0426/PutnamGAP/tar.gz/"
    + PUTNAMGAP_COMMIT
)
PUTNAMGAP_ARCHIVE_SHA256 = "ebf565f54083e6e54cbcd74ec9998211328c2d0491df02281876695da737b506"
PUTNAMGAP_ARCHIVE_BYTES = 15_945_135
PUTNAMGAP_FILE_COUNT = 1_056
PUTNAMGAP_ROW_COUNT = 1_051
PUTNAMGAP_REQUIRED_FILES = {
    "LICENSE": ("6d1f7715bf937b0a2de6a3bada41b523ea27c6103b6257f9fc3affb9844682ff", 2_694),
    "README.md": ("8f2e835f93f0e7b31f21a3a7bf4fe78e3a034bbe17f89163bb5dbd389f91e526", 12_223),
    "dataset.parquet": ("f50cbb93e1f1e141c726ebb0a4591af1f41546090e4d554ecbbc5a2692af0dbf", 12_004_747),
}

KEDLAYA_CANONICAL_ROOT = "https://kskedlaya.org/putnam-archive/"
KEDLAYA_CANONICAL_STATEMENT_URL = KEDLAYA_CANONICAL_ROOT + "2025.tex"
KEDLAYA_CANONICAL_SOLUTION_URL = KEDLAYA_CANONICAL_ROOT + "2025s.tex"
KEDLAYA_STATEMENT_CAPTURE_URL = (
    "https://web.archive.org/web/20260326040053id_/"
    "https://kskedlaya.org/putnam-archive/2025.tex"
)
KEDLAYA_SOLUTION_CAPTURE_URL = (
    "https://web.archive.org/web/20260326040213id_/"
    "https://kskedlaya.org/putnam-archive/2025s.tex"
)
KEDLAYA_MIRROR_REPOSITORY = "https://github.com/rpxgit/The-Putnam-Archive"
KEDLAYA_REVISION = "bd9408c626737480f9b76ab7e287dad6980154c8"
KEDLAYA_TREE = "42343fd26c12ffb37597c917ed5374bbc03b276b"
KEDLAYA_ARCHIVE_ROOT = f"The-Putnam-Archive-{KEDLAYA_REVISION}"
KEDLAYA_ARCHIVE_URL = (
    "https://codeload.github.com/rpxgit/The-Putnam-Archive/tar.gz/"
    + KEDLAYA_REVISION
)
KEDLAYA_ARCHIVE_SHA256 = "795f53b60d7e6ae4a6ef1c1e2ec998ceefb817d585199752b75bbc09ac59bc0d"
KEDLAYA_ARCHIVE_BYTES = 7_836_269
KEDLAYA_FILE_COUNT = 146
KEDLAYA_TEX_ROOT = "Problems & Solutions (1995-Present)/TeX"
KEDLAYA_STATEMENT_PATH = f"{KEDLAYA_TEX_ROOT}/2025.tex"
KEDLAYA_SOLUTION_PATH = f"{KEDLAYA_TEX_ROOT}/2025s.tex"
KEDLAYA_REQUIRED_FILES = {
    "LICENSE": ("1f3c658548cfbc02e6b2f7bef425e3ad4bbff91a5f14dad520d275999f9af53a", 1_058),
    "README.md": ("47400e0c20b789d2e6ef8b2a05288c2d6e5cd557fb7a97a7f30445227dad16d5", 3_201),
    KEDLAYA_STATEMENT_PATH: ("524bf4ed186d8329bdd1e1dda5785a61458ce4f5a35277299e82c1fa44a627a2", 3_824),
    KEDLAYA_SOLUTION_PATH: ("784b6c75e132b446f51d5a475445f9bd3699a9bd7c8598e5c9459ef3e7876d25", 33_175),
}

PUTNAMGAP_RIGHTS_ID = "putnamgap-original-problem-solution-maa-restricted"
KEDLAYA_RIGHTS_ID = "kedlaya-2025-problem-solution-redistribution-restricted"

PG_INDEX_RE = re.compile(
    r"^(?P<year>[0-9]{4})-(?:(?P<edition>[0-9]+)-)?"
    r"(?P<section>[AB])-(?P<number>[0-9]+)$"
)
PROBLEM_KEY_RE = re.compile(r"^putnam_(?P<year>[0-9]{4})_(?P<section>[ab])(?P<number>[1-6])$")
KEDLAYA_ITEM_RE = re.compile(rb"(?m)^\\item\[([AB][1-6])\]\n")
KEDLAYA_END_ITEMIZE_RE = re.compile(rb"(?m)^\\end\{itemize\}[ \t]*$")
SHA_RE = re.compile(r"^[0-9a-f]{64}$")

PG_REQUIRED_KEYS = {
    "checked", "difficulty", "index", "params", "problem_type", "question",
    "sci_consts", "solution", "tag", "type", "variants", "vars",
}
PG_OPTIONAL_KEYS = {"iteratively_fixed", "infinite_fixed", "infinite_fix_iterations"}

KEDLAYA_EXPECTED_HASHES = {
    "A1": ("2bdf7270b931545e20c66875d1292b2fdadcb5ba200b1618c6be5ad17c3eb782", "a65642529fce25d8100fd9cefc6d44501351979b0a9f13266b9bcd37b00ce05b"),
    "A2": ("0921ba3feb6e81af815e5f57a548b2a4388fbadfa6f27f0b3313e8125273db5a", "7ea1626c5aa05373ac59c301a3e3e752315985eff5419855c2a595973489e161"),
    "A3": ("0865b7e04bf0acb6fe14aa4770aea1acf0825d22b01fef601ce0c6a79a22c1f0", "2ae3f143a954eebca89bf578c77a00f6146b255567edb694009e33a42c7cf6e0"),
    "A4": ("6c1092e35174095ef9c19a80835abc9f5de3e3b690732b49efa29b975c046d14", "44125b76c376d0344a52d9bc0e4b54e7338dfd9de4cef46a96a7ee72c3dcfc72"),
    "A5": ("cbb699194fff220afba80612f2bc8b6024cde4be015f5d74b2cb974175d38ecd", "8d97d0a41d5609075247b6ca3e611d42268e2441a8eb7c7c5419eba247c294ff"),
    "A6": ("573aac8172a56167e2c627695be5ed8713ef40ba93fb0a3a959a1f3335e3f4e0", "986c42f2368cbf1a0d5075ddaeb3623f13652b31392986b829d160a58149ac48"),
    "B1": ("7c4ccffbdc1e5e92fa73a00b6dc774baa495f43e01e252b6dceaeab2c967e559", "f5782bf7dc628f7dc0443c6a1b1cbda0663ef1a6996ac7ab4796f19f93f00f8f"),
    "B2": ("5188d31564bc03b9b38e240f4eac9921f5db10587ff08326151f3167f18ce3da", "0c6bd5ebcf3bac8b804ad9e3fb3f6e00ae9605864c522ba3abe7d6d7c509dc6f"),
    "B3": ("80d1e17ede2a6c1c48b5e775b3e123f15100a73bc8da4c84e6f5e063d08274dc", "1ba7f81b73e5908c6ccb1ad67f61365dfb60f21e36e77aca9946e489dad622ed"),
    "B4": ("7b944d38de9860a1b90bb5c25d8a823362341b19bc185a7c76983d8d843d62d4", "497ae79942bf5e6aa11ea56cc9ae3bdf1d8f15e3674321095e8d9d444157139c"),
    "B5": ("aed24119abca6c3832244860cd055f1914dc021cf28715a1b305fa18ec0b5946", "d583e487a9edeadb8a402bfafabbe0008891184fe7c80a859c87bef2eae3d202"),
    "B6": ("c2e1ca386773ef8c41fb34c71d74820ec5246418e1bb3176559a522652430f45", "13493cd21819e81284b8c14ae8ee34c199b47a4e2c3da79fa78ddd75908c38c4"),
}


class FreezeError(RuntimeError):
    """Raised when a source or generated invariant fails closed."""


@dataclass(frozen=True)
class SourceFile:
    relative_path: str
    archive_member_path: str
    data: bytes
    git_mode: str


@dataclass(frozen=True)
class FrozenArchive:
    files: Mapping[str, SourceFile]
    file_count: int
    git_tree_sha1: str


def require(condition: bool, message: str) -> None:
    if not condition:
        raise FreezeError(message)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def encoded_json(value: Mapping[str, Any]) -> bytes:
    return canonical(value) + b"\n"


def encoded_jsonl(rows: Sequence[Mapping[str, Any]]) -> bytes:
    return b"".join(canonical(row) + b"\n" for row in rows)


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def hash_without(value: Mapping[str, Any], *fields: str) -> str:
    ignored = set(fields)
    return sha256(canonical({key: item for key, item in value.items() if key not in ignored}))


def set_digest(values: Iterable[str]) -> str:
    return sha256(canonical(sorted(values)))


def seal(row: dict[str, Any]) -> dict[str, Any]:
    require("row_sha256" not in row, "row already sealed")
    row["row_sha256"] = hash_without(row, "row_sha256")
    return row


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key!r}")
        result[key] = value
    return result


def reject_json_constant(value: str) -> Any:
    raise FreezeError(f"non-finite JSON number: {value}")


def strict_json_loads(payload: bytes, source: str) -> Any:
    try:
        return json.loads(
            payload.decode("utf-8", errors="strict"),
            object_pairs_hook=strict_object,
            parse_constant=reject_json_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise FreezeError(f"invalid strict JSON in {source}: {error}") from error


def git_object_sha1(kind: bytes, payload: bytes) -> bytes:
    header = kind + b" " + str(len(payload)).encode("ascii") + b"\0"
    return hashlib.sha1(header + payload).digest()  # noqa: S324 - Git identity.


def git_blob_sha1(payload: bytes) -> str:
    return git_object_sha1(b"blob", payload).hex()


def reconstruct_git_tree_sha1(files: Mapping[str, SourceFile]) -> str:
    blob_ids = {path: git_object_sha1(b"blob", source.data) for path, source in files.items()}
    directories = {""}
    for path in files:
        parts = path.split("/")
        directories.update("/".join(parts[:index]) for index in range(1, len(parts)))
    tree_ids: dict[str, bytes] = {}
    for directory in sorted(directories, key=lambda item: len(item.split("/")) if item else 0, reverse=True):
        prefix = f"{directory}/" if directory else ""
        children: dict[str, tuple[str, bytes]] = {}
        for path, source in files.items():
            if path.startswith(prefix):
                remainder = path[len(prefix):]
                if "/" not in remainder:
                    children[remainder] = (source.git_mode, blob_ids[path])
        for child, tree_id in tree_ids.items():
            parent, name = child.rsplit("/", 1) if "/" in child else ("", child)
            if parent == directory:
                children[name] = ("40000", tree_id)

        def tree_sort_key(item: tuple[str, tuple[str, bytes]]) -> bytes:
            name, (mode, _oid) = item
            return (name + ("/" if mode == "40000" else "")).encode("utf-8")

        body = b"".join(
            mode.encode("ascii") + b" " + name.encode("utf-8") + b"\0" + oid
            for name, (mode, oid) in sorted(children.items(), key=tree_sort_key)
        )
        tree_ids[directory] = git_object_sha1(b"tree", body)
    return tree_ids[""].hex()


def load_archive(
    path: Path,
    *,
    label: str,
    expected_sha256: str,
    expected_bytes: int,
    expected_root: str,
    expected_files: int,
    expected_tree: str,
    required_files: Mapping[str, tuple[str, int]],
) -> FrozenArchive:
    require(path.is_file(), f"{label} archive missing: {path}")
    require(path.stat().st_size == expected_bytes, f"{label} archive byte length drifted")
    require(file_sha256(path) == expected_sha256, f"{label} archive SHA-256 drifted")
    files: dict[str, SourceFile] = {}
    seen: set[str] = set()
    explicit_directories: set[str] = set()
    try:
        with tarfile.open(path, mode="r:gz") as archive:
            for member in archive.getmembers():
                pure = PurePosixPath(member.name)
                require(not pure.is_absolute() and ".." not in pure.parts, f"unsafe {label} archive member")
                require(pure.parts and pure.parts[0] == expected_root, f"unexpected {label} archive root")
                normalized = pure.as_posix()
                require(normalized not in seen, f"duplicate {label} archive member: {normalized}")
                seen.add(normalized)
                if len(pure.parts) == 1:
                    require(member.isdir(), f"{label} archive root is not a directory")
                    continue
                relative = PurePosixPath(*pure.parts[1:]).as_posix()
                if member.isdir():
                    explicit_directories.add(relative)
                    continue
                if member.isfile():
                    stream = archive.extractfile(member)
                    require(stream is not None, f"cannot read {label} member: {normalized}")
                    data = stream.read()
                    mode = "100755" if member.mode & 0o111 else "100644"
                elif member.issym():
                    data = member.linkname.encode("utf-8")
                    mode = "120000"
                else:
                    raise FreezeError(f"unsupported {label} member type: {normalized}")
                require(relative not in files, f"duplicate {label} source path: {relative}")
                files[relative] = SourceFile(relative, normalized, data, mode)
    except tarfile.TarError as error:
        raise FreezeError(f"invalid {label} tar archive: {error}") from error
    require(len(files) == expected_files, f"{label} file count drifted: {len(files)}")
    inferred_directories: set[str] = set()
    for relative in files:
        parts = relative.split("/")
        inferred_directories.update("/".join(parts[:index]) for index in range(1, len(parts)))
    require(explicit_directories <= inferred_directories, f"{label} archive has an empty directory")
    tree = reconstruct_git_tree_sha1(files)
    require(tree == expected_tree, f"{label} reconstructed Git tree drifted: {tree}")
    for relative, (wanted_sha, wanted_bytes) in required_files.items():
        require(relative in files, f"{label} required file missing: {relative}")
        source = files[relative]
        require(len(source.data) == wanted_bytes, f"{label} required file size drifted: {relative}")
        require(sha256(source.data) == wanted_sha, f"{label} required file SHA drifted: {relative}")
    return FrozenArchive(files=files, file_count=len(files), git_tree_sha1=tree)


def byte_position(payload: bytes, offset: int) -> tuple[int, int]:
    require(0 <= offset <= len(payload), "byte offset outside payload")
    line = payload.count(b"\n", 0, offset) + 1
    previous = payload.rfind(b"\n", 0, offset)
    column = offset + 1 if previous < 0 else offset - previous
    return line, column


def span(payload: bytes, start: int, end: int) -> dict[str, int]:
    require(0 <= start <= end <= len(payload), "invalid byte span")
    start_line, start_column = byte_position(payload, start)
    end_line, end_column = byte_position(payload, end)
    return {
        "start_byte": start,
        "end_byte_exclusive": end,
        "start_line": start_line,
        "start_column_utf8_byte": start_column,
        "end_line": end_line,
        "end_column_utf8_byte_exclusive": end_column,
    }


def source_file_binding(source: SourceFile) -> dict[str, Any]:
    return {
        "archive_member_path": source.archive_member_path,
        "upstream_relative_path": source.relative_path,
        "file_sha256": sha256(source.data),
        "byte_length": len(source.data),
        "git_blob_sha1": git_blob_sha1(source.data),
        "git_mode": source.git_mode,
    }


def parse_pg_index(native_index: str) -> tuple[int, int, str, int]:
    match = PG_INDEX_RE.fullmatch(native_index)
    require(match is not None, f"PutnamGAP native index malformed: {native_index}")
    return (
        int(match.group("year")),
        int(match.group("edition") or "1"),
        match.group("section"),
        int(match.group("number")),
    )


def target_key(year: int, section: str, number: int) -> str:
    return f"putnam_{year}_{section.lower()}{number}"


def coordinate(problem_key: str) -> dict[str, Any]:
    match = PROBLEM_KEY_RE.fullmatch(problem_key)
    require(match is not None, f"invalid Putnam problem key: {problem_key}")
    return {
        "competition": "William Lowell Putnam Mathematical Competition",
        "year": int(match.group("year")),
        "section": match.group("section").upper(),
        "problem_number": int(match.group("number")),
    }


def full_grid_keys() -> set[str]:
    return {
        f"putnam_{year}_{section}{number}"
        for year in range(1962, 2026)
        for section in ("a", "b")
        for number in range(1, 7)
    }


def text_anomalies(question: str, solution: str) -> list[str]:
    anomalies: list[str] = []
    for field, value in (("question", question), ("solution", solution)):
        if r"\end{itemize}" in value:
            anomalies.append(f"source_{field}_contains_end_itemize")
        if r"\end{document}" in value:
            anomalies.append(f"source_{field}_contains_end_document")
            tail = value.split(r"\end{document}", 1)[1]
            if tail.strip():
                anomalies.append(f"source_{field}_has_bytes_after_end_document")
    return anomalies


def build_putnamgap_manifest(archive: FrozenArchive) -> list[dict[str, Any]]:
    source_paths = sorted(
        path for path in archive.files
        if re.fullmatch(r"dataset/[^/]+\.json", path)
    )
    require(len(source_paths) == PUTNAMGAP_ROW_COUNT, "PutnamGAP JSON denominator drifted")
    parsed: list[tuple[tuple[int, int, str, int], str, SourceFile, dict[str, Any]]] = []
    native_ids: set[str] = set()
    total_bytes = 0
    for path in source_paths:
        source = archive.files[path]
        require(source.git_mode == "100644", f"PutnamGAP dataset mode drifted: {path}")
        document = strict_json_loads(source.data, path)
        require(isinstance(document, dict), f"PutnamGAP row is not an object: {path}")
        keys = set(document)
        require(PG_REQUIRED_KEYS <= keys <= PG_REQUIRED_KEYS | PG_OPTIONAL_KEYS, f"PutnamGAP top-level schema drifted: {path}")
        require(isinstance(document["checked"], bool), f"PutnamGAP checked type drifted: {path}")
        for field in ("difficulty", "index", "problem_type", "question", "solution", "type"):
            require(isinstance(document[field], str), f"PutnamGAP {field} type drifted: {path}")
        require(document["question"] and document["solution"], f"PutnamGAP empty prose field: {path}")
        for field in ("params", "sci_consts", "tag", "vars"):
            require(isinstance(document[field], list) and all(isinstance(item, str) for item in document[field]), f"PutnamGAP {field} type drifted: {path}")
        require(isinstance(document["variants"], dict), f"PutnamGAP variants type drifted: {path}")
        if "iteratively_fixed" in document:
            require(document["iteratively_fixed"] is True, f"PutnamGAP iteratively_fixed drifted: {path}")
        if "infinite_fixed" in document or "infinite_fix_iterations" in document:
            require(
                document.get("index") == "2023-B-6"
                and document.get("infinite_fixed") is True
                and document.get("infinite_fix_iterations") == 13,
                f"PutnamGAP infinite-fix fields drifted: {path}",
            )
        native_index = document["index"]
        require(native_index == Path(path).stem, f"PutnamGAP filename/index mismatch: {path}")
        require(native_index not in native_ids, f"duplicate PutnamGAP native index: {native_index}")
        native_ids.add(native_index)
        parsed_index = parse_pg_index(native_index)
        parsed.append((parsed_index, native_index, source, document))
        total_bytes += len(source.data)
    require(total_bytes == 28_236_411, f"PutnamGAP JSON byte denominator drifted: {total_bytes}")
    parsed.sort(key=lambda item: (item[0][0], item[0][1], 0 if item[0][2] == "A" else 1, item[0][3]))

    rows: list[dict[str, Any]] = []
    mapped_keys: set[str] = set()
    for row_index, (parsed_index, native_index, source, document) in enumerate(parsed):
        year, edition, section, number = parsed_index
        if 1962 <= year <= 2024 and edition == 1 and number in range(1, 7):
            disposition = "mapped_in_scope_coordinate"
            target = target_key(year, section, number)
            require(target not in mapped_keys, f"duplicate PutnamGAP grid target: {target}")
            mapped_keys.add(target)
        elif year < 1962:
            disposition = "out_of_scope_pre_1962"
            target = None
        else:
            raise FreezeError(f"unexpected PutnamGAP coordinate: {native_index}")
        candidate_id = f"putnamgap/{PUTNAMGAP_COMMIT}/{native_index}"
        question = document["question"]
        solution = document["solution"]
        row = {
            "schema_version": "awesome-theorems/putnamgap-source-locator/5.6",
            "source_candidate_id": candidate_id,
            "native_index": native_index,
            "source_row_index": row_index,
            "index_order": {
                "year": year,
                "edition": edition,
                "section": section,
                "problem_number": number,
            },
            "source_file_binding": source_file_binding(source),
            "record_locator": {
                "record_index_within_file": 0,
                "json_pointer": "",
                "record_span": span(source.data, 0, len(source.data)),
                "record_raw_sha256": sha256(source.data),
                "record_canonical_sha256": sha256(canonical(document)),
                "native_index_pointer": "/index",
                "native_index_value_sha256": sha256(native_index.encode("utf-8")),
                "statement_pointer": "/question",
                "statement_value_sha256": sha256(question.encode("utf-8")),
                "solution_pointer": "/solution",
                "solution_value_sha256": sha256(solution.encode("utf-8")),
            },
            "disposition": disposition,
            "target_problem_key": target,
            "rights_id": PUTNAMGAP_RIGHTS_ID,
            "anomaly_codes": text_anomalies(question, solution),
            "exact_statement_or_solution_text_embedded": False,
        }
        rows.append(seal(row))
    require(len(rows) == 1_051, "PutnamGAP manifest row count drifted")
    require(len(mapped_keys) == 756, "PutnamGAP mapped grid denominator drifted")
    require(Counter(row["disposition"] for row in rows) == Counter({"mapped_in_scope_coordinate": 756, "out_of_scope_pre_1962": 295}), "PutnamGAP disposition counts drifted")
    return rows


def trim_ascii_span(payload: bytes, start: int, end: int) -> tuple[int, int]:
    whitespace = b" \t\r\n"
    while start < end and payload[start] in whitespace:
        start += 1
    while end > start and payload[end - 1] in whitespace:
        end -= 1
    return start, end


def extract_kedlaya_items(source: SourceFile) -> dict[str, dict[str, Any]]:
    payload = source.data
    require(b"\r" not in payload and payload.decode("ascii"), f"non-ASCII/CR bytes in {source.relative_path}")
    matches = list(KEDLAYA_ITEM_RE.finditer(payload))
    labels = [match.group(1).decode("ascii") for match in matches]
    wanted = [f"{section}{number}" for section in ("A", "B") for number in range(1, 7)]
    require(labels == wanted, f"Kedlaya item sequence drifted in {source.relative_path}: {labels}")
    result: dict[str, dict[str, Any]] = {}
    for index, (label, match) in enumerate(zip(labels, matches, strict=True)):
        raw_start = match.end()
        if index + 1 < len(matches):
            raw_end = matches[index + 1].start()
        else:
            closing = KEDLAYA_END_ITEMIZE_RE.search(payload, raw_start)
            require(closing is not None, f"Kedlaya outer itemize terminator missing: {source.relative_path}")
            raw_end = closing.start()
        body_start, body_end = trim_ascii_span(payload, raw_start, raw_end)
        require(body_start < body_end, f"empty Kedlaya item: {source.relative_path}/{label}")
        body = payload[body_start:body_end]
        marker = payload[match.start():match.end()]
        result[label] = {
            "source_file_binding": source_file_binding(source),
            "item_label": label,
            "item_ordinal": index,
            "item_marker_span": span(payload, match.start(), match.end()),
            "item_marker_sha256": sha256(marker),
            "item_body_span": span(payload, body_start, body_end),
            "item_body_sha256": sha256(body),
            "span_extraction_rule": "labeled_item_body_ascii_whitespace_trimmed_zero_based_half_open",
        }
    return result


def build_kedlaya_manifest(archive: FrozenArchive) -> list[dict[str, Any]]:
    statement_items = extract_kedlaya_items(archive.files[KEDLAYA_STATEMENT_PATH])
    solution_items = extract_kedlaya_items(archive.files[KEDLAYA_SOLUTION_PATH])
    rows: list[dict[str, Any]] = []
    for row_index, label in enumerate(f"{section}{number}" for section in ("A", "B") for number in range(1, 7)):
        statement = statement_items[label]
        solution = solution_items[label]
        expected_statement, expected_solution = KEDLAYA_EXPECTED_HASHES[label]
        require(statement["item_body_sha256"] == expected_statement, f"Kedlaya statement item hash drifted: {label}")
        require(solution["item_body_sha256"] == expected_solution, f"Kedlaya solution item hash drifted: {label}")
        native_index = f"2025-{label[0]}-{label[1]}"
        candidate_id = f"kedlaya/{KEDLAYA_REVISION}/{native_index}"
        anomalies: list[str] = []
        if label in {"A2", "A6"}:
            anomalies.append("source_solution_reported_typographical_issue_requires_review")
        row = {
            "schema_version": "awesome-theorems/kedlaya-putnam-source-locator/5.6",
            "source_candidate_id": candidate_id,
            "native_index": native_index,
            "source_row_index": row_index,
            "coordinate": {
                "year": 2025,
                "section": label[0],
                "problem_number": int(label[1]),
            },
            "statement_binding": statement,
            "solution_binding": solution,
            "disposition": "mapped_in_scope_coordinate",
            "target_problem_key": target_key(2025, label[0], int(label[1])),
            "rights_id": KEDLAYA_RIGHTS_ID,
            "anomaly_codes": anomalies,
            "exact_statement_or_solution_text_embedded": False,
        }
        rows.append(seal(row))
    return rows


def load_pb(repository_root: Path) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    inventory_path = repository_root / PB_INVENTORY_REL
    problems_path = repository_root / PB_PROBLEMS_REL
    require(inventory_path.is_file() and problems_path.is_file(), "PutnamBench frozen parent assets missing")
    require(file_sha256(inventory_path) == PB_INVENTORY_SHA256, "PutnamBench inventory bytes drifted")
    require(file_sha256(problems_path) == PB_PROBLEMS_SHA256, "PutnamBench problem bytes drifted")
    inventory_payload = inventory_path.read_bytes()
    inventory = strict_json_loads(inventory_payload, str(PB_INVENTORY_REL))
    require(isinstance(inventory, dict) and encoded_json(inventory) == inventory_payload, "PutnamBench inventory is not canonical")
    require(inventory.get("authority_sha256") == PB_AUTHORITY, "PutnamBench authority drifted")
    require(inventory["authority_sha256"] == hash_without(inventory, "authority_sha256"), "PutnamBench authority seal invalid")
    rows, payload = load_jsonl(problems_path, "PutnamBench problems")
    require(sha256(payload) == PB_PROBLEMS_SHA256 and len(rows) == 675, "PutnamBench problem denominator drifted")
    by_key: dict[str, dict[str, Any]] = {}
    for index, row in enumerate(rows):
        require(row.get("row_sha256") == hash_without(row, "row_sha256"), f"PutnamBench row seal invalid: {index}")
        key = row.get("problem_key")
        require(isinstance(key, str) and key not in by_key, f"PutnamBench key invalid: {index}")
        by_key[key] = row
    require(set(by_key) <= full_grid_keys(), "PutnamBench key outside full grid")
    return inventory, by_key


def load_jsonl(path: Path, label: str) -> tuple[list[dict[str, Any]], bytes]:
    require(path.is_file(), f"{label} missing: {path}")
    payload = path.read_bytes()
    require(payload.endswith(b"\n"), f"{label} lacks final newline")
    rows: list[dict[str, Any]] = []
    for index, line in enumerate(payload.splitlines(keepends=True)):
        require(line.endswith(b"\n") and line != b"\n", f"{label} line framing invalid: {index}")
        value = strict_json_loads(line[:-1], f"{label}[{index}]")
        require(isinstance(value, dict), f"{label} row is not an object: {index}")
        require(canonical(value) + b"\n" == line, f"{label} row is not canonical: {index}")
        rows.append(value)
    return rows, payload


def build_candidates(
    pg_rows: Sequence[Mapping[str, Any]],
    kedlaya_rows: Sequence[Mapping[str, Any]],
    pg_manifest_sha: str,
    kedlaya_manifest_sha: str,
) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for manifest_index, source_row in enumerate(pg_rows):
        locator = source_row["record_locator"]
        row = {
            "schema_version": "awesome-theorems/full-putnam-source-candidate/5.6",
            "source_candidate_id": source_row["source_candidate_id"],
            "source_branch": "putnamgap",
            "source_binding": {
                "source_id": f"putnamgap:{PUTNAMGAP_COMMIT}",
                "path": PUTNAMGAP_MANIFEST_REL.as_posix(),
                "file_sha256": pg_manifest_sha,
                "locator": {
                    "manifest_row_index": manifest_index,
                    "manifest_row_sha256": source_row["row_sha256"],
                    "native_index": source_row["native_index"],
                },
                "evidence_sha256": source_row["row_sha256"],
                "rights_id": PUTNAMGAP_RIGHTS_ID,
            },
            "source_statement_sha256": locator["statement_value_sha256"],
            "source_solution_sha256": locator["solution_value_sha256"],
            "source_problem_key": source_row["native_index"],
            "source_year": source_row["index_order"]["year"],
            "disposition": source_row["disposition"],
            "target_problem_key": source_row["target_problem_key"],
            "rights_id": PUTNAMGAP_RIGHTS_ID,
        }
        candidates.append(seal(row))
    for manifest_index, source_row in enumerate(kedlaya_rows):
        row = {
            "schema_version": "awesome-theorems/full-putnam-source-candidate/5.6",
            "source_candidate_id": source_row["source_candidate_id"],
            "source_branch": "kedlaya_2025",
            "source_binding": {
                "source_id": f"kedlaya-putnam-archive:{KEDLAYA_REVISION}",
                "path": KEDLAYA_MANIFEST_REL.as_posix(),
                "file_sha256": kedlaya_manifest_sha,
                "locator": {
                    "manifest_row_index": manifest_index,
                    "manifest_row_sha256": source_row["row_sha256"],
                    "native_index": source_row["native_index"],
                },
                "evidence_sha256": source_row["row_sha256"],
                "rights_id": KEDLAYA_RIGHTS_ID,
            },
            "source_statement_sha256": source_row["statement_binding"]["item_body_sha256"],
            "source_solution_sha256": source_row["solution_binding"]["item_body_sha256"],
            "source_problem_key": source_row["native_index"],
            "source_year": 2025,
            "disposition": "mapped_in_scope_coordinate",
            "target_problem_key": source_row["target_problem_key"],
            "rights_id": KEDLAYA_RIGHTS_ID,
        }
        candidates.append(seal(row))
    require(len(candidates) == 1_063, "full source candidate denominator drifted")
    return candidates


def build_problems(
    candidates: Sequence[Mapping[str, Any]],
    pg_by_id: Mapping[str, Mapping[str, Any]],
    kedlaya_by_id: Mapping[str, Mapping[str, Any]],
    pb_by_key: Mapping[str, Mapping[str, Any]],
) -> list[dict[str, Any]]:
    by_target: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for candidate in candidates:
        if candidate["disposition"] in {"mapped_in_scope_coordinate", "alternate_or_duplicate_source_variant"}:
            by_target[str(candidate["target_problem_key"])].append(candidate)
    grid = full_grid_keys()
    require(set(by_target) == grid, "candidate projection does not equal full Putnam grid")
    rows: list[dict[str, Any]] = []
    for problem_key in sorted(grid):
        projected = sorted(by_target[problem_key], key=lambda row: str(row["source_candidate_id"]))
        require(len(projected) == 1, f"full Putnam coordinate lacks a unique primary source: {problem_key}")
        primary = projected[0]
        candidate_id = str(primary["source_candidate_id"])
        source_manifest_row = pg_by_id.get(candidate_id) or kedlaya_by_id.get(candidate_id)
        require(source_manifest_row is not None, f"candidate manifest row missing: {candidate_id}")
        pb = pb_by_key.get(problem_key)
        row = {
            "schema_version": "awesome-theorems/full-putnam-source-problem/5.6",
            "problem_key": problem_key,
            "coordinate": coordinate(problem_key),
            "source_branch": primary["source_branch"],
            "source_candidate_ids": [candidate_id],
            "source_statement_sha256": primary["source_statement_sha256"],
            "source_solution_sha256": primary["source_solution_sha256"],
            "putnambench_problem_row_sha256": pb["row_sha256"] if pb is not None else None,
            "formal_variant_ids": list(pb["formal_variant_ids"]) if pb is not None else [],
            "rights_id": primary["rights_id"],
            "anomaly_codes": list(source_manifest_row["anomaly_codes"])
            + ([] if pb is not None else ["outside_putnambench_component_union"]),
        }
        rows.append(seal(row))
    require(len(rows) == 768, "full Putnam seed denominator drifted")
    return rows


def build_rights() -> dict[str, Any]:
    return {
        "registry": {
            PUTNAMGAP_RIGHTS_ID: {
                "license_expression": "NOASSERTION",
                "source_scope": "original Putnam problem statements and canonical solutions",
                "copyright_holder_or_provenance": "Mathematical Association of America; four cited MAA Press volumes",
                "putnamgap_cc_by_4_0_applies_to_original_problem_or_solution_text": False,
                "redistribution_basis_claimed_by_catalog": None,
                "catalog_may_store_locator_and_hash_metadata": True,
            },
            KEDLAYA_RIGHTS_ID: {
                "license_expression": "NOASSERTION",
                "problem_rights": "MAA copyright; further redistribution restricted",
                "solution_rights": "Bhargava/Kedlaya/Ng authorship; link requested in lieu of reproduction",
                "mirror_mit_license_applies_to_problem_or_solution_text": False,
                "redistribution_basis_claimed_by_catalog": None,
                "catalog_may_store_locator_and_hash_metadata": True,
            },
        },
        "catalog_release_policy": {
            "catalog_relicenses_source": False,
            "exact_original_problem_text_redistributed": False,
            "exact_canonical_solution_text_redistributed": False,
            "independently_written_statement_required": True,
            "independently_written_proof_and_relation_summary_required": True,
        },
    }


def build(
    repository_root: Path,
    putnamgap_archive_path: Path,
    kedlaya_archive_path: Path,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    pg_archive = load_archive(
        putnamgap_archive_path,
        label="PutnamGAP",
        expected_sha256=PUTNAMGAP_ARCHIVE_SHA256,
        expected_bytes=PUTNAMGAP_ARCHIVE_BYTES,
        expected_root=PUTNAMGAP_ARCHIVE_ROOT,
        expected_files=PUTNAMGAP_FILE_COUNT,
        expected_tree=PUTNAMGAP_TREE,
        required_files=PUTNAMGAP_REQUIRED_FILES,
    )
    kedlaya_archive = load_archive(
        kedlaya_archive_path,
        label="Kedlaya mirror",
        expected_sha256=KEDLAYA_ARCHIVE_SHA256,
        expected_bytes=KEDLAYA_ARCHIVE_BYTES,
        expected_root=KEDLAYA_ARCHIVE_ROOT,
        expected_files=KEDLAYA_FILE_COUNT,
        expected_tree=KEDLAYA_TREE,
        required_files=KEDLAYA_REQUIRED_FILES,
    )
    pg_rows = build_putnamgap_manifest(pg_archive)
    kedlaya_rows = build_kedlaya_manifest(kedlaya_archive)
    pg_payload = encoded_jsonl(pg_rows)
    kedlaya_payload = encoded_jsonl(kedlaya_rows)
    candidates = build_candidates(pg_rows, kedlaya_rows, sha256(pg_payload), sha256(kedlaya_payload))
    _pb_inventory, pb_by_key = load_pb(repository_root)
    pg_by_id = {str(row["source_candidate_id"]): row for row in pg_rows}
    kedlaya_by_id = {str(row["source_candidate_id"]): row for row in kedlaya_rows}
    problems = build_problems(candidates, pg_by_id, kedlaya_by_id, pb_by_key)
    candidates_payload = encoded_jsonl(candidates)
    problems_payload = encoded_jsonl(problems)
    grid = full_grid_keys()
    pb_keys = set(pb_by_key)
    inventory: dict[str, Any] = {
        "schema_version": "awesome-theorems/full-putnam-source-inventory/5.6",
        "putnambench_source_inventory_authority_sha256": PB_AUTHORITY,
        "source_snapshots": {
            "putnamgap": {
                "source_snapshot_id": f"putnamgap:{PUTNAMGAP_COMMIT}",
                "repository": PUTNAMGAP_REPOSITORY,
                "commit": PUTNAMGAP_COMMIT,
                "git_tree_sha1": PUTNAMGAP_TREE,
                "dataset_git_tree_sha1": PUTNAMGAP_DATASET_TREE,
                "external_archive_locator": PUTNAMGAP_ARCHIVE_URL,
                "external_archive_sha256": PUTNAMGAP_ARCHIVE_SHA256,
                "external_archive_byte_length": PUTNAMGAP_ARCHIVE_BYTES,
                "external_archive_root": PUTNAMGAP_ARCHIVE_ROOT,
                "external_archive_file_count": PUTNAMGAP_FILE_COUNT,
                "source_row_count": 1_051,
                "prose_free_manifest_repository_path": PUTNAMGAP_MANIFEST_REL.as_posix(),
                "prose_free_manifest_sha256": sha256(pg_payload),
                "prose_free_manifest_byte_length": len(pg_payload),
                "archive_embedded_in_repository": False,
                "raw_problem_or_solution_text_redistributed": False,
            },
            "kedlaya_2025": {
                "source_snapshot_id": f"kedlaya-putnam-archive:{KEDLAYA_REVISION}",
                "canonical_origin": KEDLAYA_CANONICAL_ROOT,
                "canonical_statement_url": KEDLAYA_CANONICAL_STATEMENT_URL,
                "canonical_solution_url": KEDLAYA_CANONICAL_SOLUTION_URL,
                "immutable_statement_capture_url": KEDLAYA_STATEMENT_CAPTURE_URL,
                "immutable_solution_capture_url": KEDLAYA_SOLUTION_CAPTURE_URL,
                "mirror_repository": KEDLAYA_MIRROR_REPOSITORY,
                "immutable_revision": KEDLAYA_REVISION,
                "git_tree_sha1": KEDLAYA_TREE,
                "external_archive_locator": KEDLAYA_ARCHIVE_URL,
                "external_archive_sha256": KEDLAYA_ARCHIVE_SHA256,
                "external_archive_byte_length": KEDLAYA_ARCHIVE_BYTES,
                "external_archive_root": KEDLAYA_ARCHIVE_ROOT,
                "external_archive_file_count": KEDLAYA_FILE_COUNT,
                "statement_file": source_file_binding(kedlaya_archive.files[KEDLAYA_STATEMENT_PATH]),
                "solution_file": source_file_binding(kedlaya_archive.files[KEDLAYA_SOLUTION_PATH]),
                "canonical_bytes_match_immutable_mirror": True,
                "source_row_count": 12,
                "year": 2025,
                "prose_free_manifest_repository_path": KEDLAYA_MANIFEST_REL.as_posix(),
                "prose_free_manifest_sha256": sha256(kedlaya_payload),
                "prose_free_manifest_byte_length": len(kedlaya_payload),
                "archive_embedded_in_repository": False,
                "raw_problem_or_solution_text_redistributed": False,
            },
        },
        "coordinate_policy": {
            "competition": "William Lowell Putnam Mathematical Competition",
            "first_year": 1962,
            "last_year": 2025,
            "sections": ["A", "B"],
            "problems_per_section": [1, 2, 3, 4, 5, 6],
            "putnamgap_source_years": [1962, 2024],
            "kedlaya_source_year": 2025,
            "coordinate_existence_alone_grants_claim_credit": False,
            "source_statement_and_solution_hash_policy": "exact_decoded_UTF-8_field_bytes_for_PutnamGAP; exact_ASCII-trimmed_labeled_item_body_bytes_for_Kedlaya",
        },
        "rights": build_rights(),
        "outputs": {
            "putnamgap_prose_free_manifest": {
                "path": PUTNAMGAP_MANIFEST_REL.as_posix(),
                "media_type": "application/x-ndjson",
                "row_count": len(pg_rows),
                "sha256": sha256(pg_payload),
            },
            "kedlaya_2025_prose_free_manifest": {
                "path": KEDLAYA_MANIFEST_REL.as_posix(),
                "media_type": "application/x-ndjson",
                "row_count": len(kedlaya_rows),
                "sha256": sha256(kedlaya_payload),
            },
            "full_source_candidates": {
                "path": CANDIDATES_REL.as_posix(),
                "media_type": "application/x-ndjson",
                "row_count": len(candidates),
                "sha256": sha256(candidates_payload),
            },
            "full_source_problems": {
                "path": PROBLEMS_REL.as_posix(),
                "media_type": "application/x-ndjson",
                "row_count": len(problems),
                "sha256": sha256(problems_payload),
            },
        },
        "counts": {
            "full_grid_problem_keys": 768,
            "putnambench_subset_problem_keys": 675,
            "outside_putnambench_problem_keys": 93,
            "putnamgap_source_candidates": 1_051,
            "kedlaya_2025_source_candidates": 12,
            "putnamgap_grid_problem_keys": 756,
            "kedlaya_2025_grid_problem_keys": 12,
            "putnamgap_out_of_scope_pre_1962_candidates": 295,
            "mapped_source_candidates": 768,
            "alternate_or_duplicate_source_candidates": 0,
            "rejected_malformed_source_candidates": 0,
        },
        "set_digests": {
            "full_grid_problem_key_set_sha256": set_digest(grid),
            "putnambench_problem_key_set_sha256": set_digest(pb_keys),
            "supplemental_problem_key_set_sha256": set_digest(grid - pb_keys),
            "source_candidate_id_set_sha256": set_digest(str(row["source_candidate_id"]) for row in candidates),
            "putnamgap_candidate_id_set_sha256": set_digest(str(row["source_candidate_id"]) for row in pg_rows),
            "mapped_putnamgap_candidate_id_set_sha256": set_digest(str(row["source_candidate_id"]) for row in pg_rows if row["disposition"] == "mapped_in_scope_coordinate"),
            "pre_1962_putnamgap_candidate_id_set_sha256": set_digest(str(row["source_candidate_id"]) for row in pg_rows if row["disposition"] == "out_of_scope_pre_1962"),
            "problem_row_set_sha256": set_digest(str(row["row_sha256"]) for row in problems),
            "candidate_row_set_sha256": set_digest(str(row["row_sha256"]) for row in candidates),
            "putnamgap_manifest_row_set_sha256": set_digest(str(row["row_sha256"]) for row in pg_rows),
            "kedlaya_manifest_row_set_sha256": set_digest(str(row["row_sha256"]) for row in kedlaya_rows),
        },
    }
    inventory["authority_sha256"] = hash_without(inventory, "authority_sha256")
    return inventory, candidates, problems, pg_rows, kedlaya_rows


def output_payloads(
    inventory: Mapping[str, Any],
    candidates: Sequence[Mapping[str, Any]],
    problems: Sequence[Mapping[str, Any]],
    pg_rows: Sequence[Mapping[str, Any]],
    kedlaya_rows: Sequence[Mapping[str, Any]],
) -> dict[Path, bytes]:
    return {
        INVENTORY_REL: encoded_json(inventory),
        CANDIDATES_REL: encoded_jsonl(candidates),
        PROBLEMS_REL: encoded_jsonl(problems),
        PUTNAMGAP_MANIFEST_REL: encoded_jsonl(pg_rows),
        KEDLAYA_MANIFEST_REL: encoded_jsonl(kedlaya_rows),
    }


def exact_keys(value: Any, keys: set[str], label: str) -> Mapping[str, Any]:
    require(isinstance(value, dict), f"{label} is not an object")
    require(set(value) == keys, f"{label} field set drifted: missing={sorted(keys - set(value))} extra={sorted(set(value) - keys)}")
    return value


PG_MANIFEST_KEYS = {
    "schema_version", "source_candidate_id", "native_index", "source_row_index",
    "index_order", "source_file_binding", "record_locator", "disposition",
    "target_problem_key", "rights_id", "anomaly_codes",
    "exact_statement_or_solution_text_embedded", "row_sha256",
}
KEDLAYA_MANIFEST_KEYS = {
    "schema_version", "source_candidate_id", "native_index", "source_row_index",
    "coordinate", "statement_binding", "solution_binding", "disposition",
    "target_problem_key", "rights_id", "anomaly_codes",
    "exact_statement_or_solution_text_embedded", "row_sha256",
}
CANDIDATE_KEYS = {
    "schema_version", "source_candidate_id", "source_branch", "source_binding",
    "source_statement_sha256", "source_solution_sha256", "source_problem_key",
    "source_year", "disposition", "target_problem_key", "rights_id", "row_sha256",
}
PROBLEM_KEYS = {
    "schema_version", "problem_key", "coordinate", "source_branch",
    "source_candidate_ids", "source_statement_sha256", "source_solution_sha256",
    "putnambench_problem_row_sha256", "formal_variant_ids", "rights_id",
    "anomaly_codes", "row_sha256",
}


def validate_hash(value: Any, label: str) -> str:
    require(isinstance(value, str) and SHA_RE.fullmatch(value) is not None, f"{label} is not SHA-256")
    return value


def validate_repo_only(repository_root: Path) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    inventory_path = repository_root / INVENTORY_REL
    require(inventory_path.is_file(), f"full source inventory missing: {INVENTORY_REL}")
    inventory_payload = inventory_path.read_bytes()
    inventory = strict_json_loads(inventory_payload, str(INVENTORY_REL))
    require(isinstance(inventory, dict) and encoded_json(inventory) == inventory_payload, "full source inventory is not canonical JSON")
    exact_keys(inventory, {"schema_version", "putnambench_source_inventory_authority_sha256", "source_snapshots", "coordinate_policy", "rights", "outputs", "counts", "set_digests", "authority_sha256"}, "inventory")
    require(inventory["schema_version"] == "awesome-theorems/full-putnam-source-inventory/5.6", "inventory schema drifted")
    require(inventory["authority_sha256"] == hash_without(inventory, "authority_sha256"), "inventory authority mismatch")
    require(inventory["authority_sha256"] == FULL_SOURCE_AUTHORITY, "inventory frozen authority drifted")
    require(inventory["putnambench_source_inventory_authority_sha256"] == PB_AUTHORITY, "inventory PB authority drifted")
    _pb_inventory, pb_by_key = load_pb(repository_root)

    pg_rows, pg_payload = load_jsonl(repository_root / PUTNAMGAP_MANIFEST_REL, "PutnamGAP locator manifest")
    kedlaya_rows, kedlaya_payload = load_jsonl(repository_root / KEDLAYA_MANIFEST_REL, "Kedlaya locator manifest")
    candidates, candidates_payload = load_jsonl(repository_root / CANDIDATES_REL, "full source candidates")
    problems, problems_payload = load_jsonl(repository_root / PROBLEMS_REL, "full source problems")
    require((len(pg_rows), len(kedlaya_rows), len(candidates), len(problems)) == (1051, 12, 1063, 768), "full source repository denominators drifted")

    outputs = inventory["outputs"]
    expected_outputs = {
        "putnamgap_prose_free_manifest": (PUTNAMGAP_MANIFEST_REL, pg_rows, pg_payload),
        "kedlaya_2025_prose_free_manifest": (KEDLAYA_MANIFEST_REL, kedlaya_rows, kedlaya_payload),
        "full_source_candidates": (CANDIDATES_REL, candidates, candidates_payload),
        "full_source_problems": (PROBLEMS_REL, problems, problems_payload),
    }
    require(isinstance(outputs, dict) and set(outputs) == set(expected_outputs), "inventory output set drifted")
    for name, (relative, rows, payload) in expected_outputs.items():
        descriptor = exact_keys(outputs[name], {"path", "media_type", "row_count", "sha256"}, f"outputs.{name}")
        require(descriptor == {"path": relative.as_posix(), "media_type": "application/x-ndjson", "row_count": len(rows), "sha256": sha256(payload)}, f"output binding drifted: {name}")

    snapshots = inventory["source_snapshots"]
    require(isinstance(snapshots, dict) and set(snapshots) == {"putnamgap", "kedlaya_2025"}, "snapshot set drifted")
    pg_snapshot = snapshots["putnamgap"]
    kedlaya_snapshot = snapshots["kedlaya_2025"]
    require(pg_snapshot["repository"] == PUTNAMGAP_REPOSITORY and pg_snapshot["commit"] == PUTNAMGAP_COMMIT and pg_snapshot["git_tree_sha1"] == PUTNAMGAP_TREE, "PutnamGAP snapshot identity drifted")
    require(pg_snapshot["external_archive_sha256"] == PUTNAMGAP_ARCHIVE_SHA256 and pg_snapshot["external_archive_byte_length"] == PUTNAMGAP_ARCHIVE_BYTES, "PutnamGAP archive pin drifted")
    require(pg_snapshot["prose_free_manifest_repository_path"] == PUTNAMGAP_MANIFEST_REL.as_posix() and pg_snapshot["prose_free_manifest_sha256"] == sha256(pg_payload) and pg_snapshot["prose_free_manifest_byte_length"] == len(pg_payload), "PutnamGAP manifest snapshot drifted")
    require(kedlaya_snapshot["immutable_revision"] == KEDLAYA_REVISION and kedlaya_snapshot["git_tree_sha1"] == KEDLAYA_TREE and kedlaya_snapshot["canonical_origin"] == KEDLAYA_CANONICAL_ROOT, "Kedlaya snapshot identity drifted")
    require(kedlaya_snapshot["external_archive_sha256"] == KEDLAYA_ARCHIVE_SHA256 and kedlaya_snapshot["external_archive_byte_length"] == KEDLAYA_ARCHIVE_BYTES, "Kedlaya archive pin drifted")
    require(kedlaya_snapshot["prose_free_manifest_repository_path"] == KEDLAYA_MANIFEST_REL.as_posix() and kedlaya_snapshot["prose_free_manifest_sha256"] == sha256(kedlaya_payload) and kedlaya_snapshot["prose_free_manifest_byte_length"] == len(kedlaya_payload), "Kedlaya manifest snapshot drifted")
    for snapshot in (pg_snapshot, kedlaya_snapshot):
        require(snapshot["archive_embedded_in_repository"] is False and snapshot["raw_problem_or_solution_text_redistributed"] is False, "source redistribution boundary drifted")

    rights = inventory["rights"]
    require(isinstance(rights, dict) and set(rights) == {"registry", "catalog_release_policy"}, "rights registry malformed")
    require(set(rights["registry"]) == {PUTNAMGAP_RIGHTS_ID, KEDLAYA_RIGHTS_ID}, "rights IDs drifted")
    policy = rights["catalog_release_policy"]
    require(policy == build_rights()["catalog_release_policy"], "catalog release rights policy drifted")
    require(rights["registry"][PUTNAMGAP_RIGHTS_ID]["putnamgap_cc_by_4_0_applies_to_original_problem_or_solution_text"] is False, "PutnamGAP CC-BY scope expanded")
    require(rights["registry"][KEDLAYA_RIGHTS_ID]["mirror_mit_license_applies_to_problem_or_solution_text"] is False, "mirror MIT scope expanded")

    pg_by_id: dict[str, Mapping[str, Any]] = {}
    expected_pg_order: list[tuple[int, int, int, int]] = []
    for index, raw_row in enumerate(pg_rows):
        row = exact_keys(raw_row, PG_MANIFEST_KEYS, f"PutnamGAP manifest[{index}]")
        require(row["schema_version"] == "awesome-theorems/putnamgap-source-locator/5.6", f"PutnamGAP manifest schema drifted: {index}")
        require(row["row_sha256"] == hash_without(row, "row_sha256"), f"PutnamGAP manifest seal drifted: {index}")
        require(row["source_row_index"] == index and row["exact_statement_or_solution_text_embedded"] is False, f"PutnamGAP manifest ordinal/embedding drifted: {index}")
        native = row["native_index"]
        parsed = parse_pg_index(native)
        expected_pg_order.append((parsed[0], parsed[1], 0 if parsed[2] == "A" else 1, parsed[3]))
        candidate_id = f"putnamgap/{PUTNAMGAP_COMMIT}/{native}"
        require(row["source_candidate_id"] == candidate_id and candidate_id not in pg_by_id, f"PutnamGAP candidate ID drifted: {index}")
        require(row["index_order"] == {"year": parsed[0], "edition": parsed[1], "section": parsed[2], "problem_number": parsed[3]}, f"PutnamGAP index projection drifted: {native}")
        locator = row["record_locator"]
        for field in ("record_raw_sha256", "record_canonical_sha256", "native_index_value_sha256", "statement_value_sha256", "solution_value_sha256"):
            validate_hash(locator[field], f"PutnamGAP {native}/{field}")
        require(locator["native_index_value_sha256"] == sha256(native.encode("utf-8")), f"PutnamGAP native index hash drifted: {native}")
        if parsed[0] >= 1962:
            require(row["disposition"] == "mapped_in_scope_coordinate" and row["target_problem_key"] == target_key(parsed[0], parsed[2], parsed[3]), f"PutnamGAP mapped disposition drifted: {native}")
        else:
            require(row["disposition"] == "out_of_scope_pre_1962" and row["target_problem_key"] is None, f"PutnamGAP pre-1962 disposition drifted: {native}")
        require(row["rights_id"] == PUTNAMGAP_RIGHTS_ID and isinstance(row["anomaly_codes"], list), f"PutnamGAP rights/anomalies drifted: {native}")
        pg_by_id[candidate_id] = row
    require(expected_pg_order == sorted(expected_pg_order), "PutnamGAP source row order drifted")
    require(Counter(row["disposition"] for row in pg_rows) == Counter({"mapped_in_scope_coordinate": 756, "out_of_scope_pre_1962": 295}), "PutnamGAP repository disposition denominator drifted")

    kedlaya_by_id: dict[str, Mapping[str, Any]] = {}
    labels = [f"{section}{number}" for section in ("A", "B") for number in range(1, 7)]
    for index, (raw_row, label) in enumerate(zip(kedlaya_rows, labels, strict=True)):
        row = exact_keys(raw_row, KEDLAYA_MANIFEST_KEYS, f"Kedlaya manifest[{index}]")
        require(row["schema_version"] == "awesome-theorems/kedlaya-putnam-source-locator/5.6" and row["row_sha256"] == hash_without(row, "row_sha256"), f"Kedlaya manifest schema/seal drifted: {index}")
        native = f"2025-{label[0]}-{label[1]}"
        candidate_id = f"kedlaya/{KEDLAYA_REVISION}/{native}"
        require(row["source_row_index"] == index and row["native_index"] == native and row["source_candidate_id"] == candidate_id, f"Kedlaya identity drifted: {index}")
        require(row["coordinate"] == {"year": 2025, "section": label[0], "problem_number": int(label[1])}, f"Kedlaya coordinate drifted: {label}")
        require(row["target_problem_key"] == target_key(2025, label[0], int(label[1])) and row["disposition"] == "mapped_in_scope_coordinate", f"Kedlaya target drifted: {label}")
        require(row["rights_id"] == KEDLAYA_RIGHTS_ID and row["exact_statement_or_solution_text_embedded"] is False, f"Kedlaya rights/embedding drifted: {label}")
        expected_statement, expected_solution = KEDLAYA_EXPECTED_HASHES[label]
        require(row["statement_binding"]["item_body_sha256"] == expected_statement and row["solution_binding"]["item_body_sha256"] == expected_solution, f"Kedlaya item hash drifted: {label}")
        kedlaya_by_id[candidate_id] = row

    candidate_by_id: dict[str, Mapping[str, Any]] = {}
    by_target: dict[str, list[str]] = defaultdict(list)
    for index, raw_row in enumerate(candidates):
        row = exact_keys(raw_row, CANDIDATE_KEYS, f"candidate[{index}]")
        require(row["schema_version"] == "awesome-theorems/full-putnam-source-candidate/5.6" and row["row_sha256"] == hash_without(row, "row_sha256"), f"candidate schema/seal drifted: {index}")
        candidate_id = row["source_candidate_id"]
        require(isinstance(candidate_id, str) and candidate_id not in candidate_by_id, f"duplicate candidate ID: {candidate_id}")
        validate_hash(row["source_statement_sha256"], f"candidate statement hash: {candidate_id}")
        validate_hash(row["source_solution_sha256"], f"candidate solution hash: {candidate_id}")
        if row["source_branch"] == "putnamgap":
            manifest = pg_by_id.get(candidate_id)
            manifest_path, manifest_sha, rights_id = PUTNAMGAP_MANIFEST_REL, sha256(pg_payload), PUTNAMGAP_RIGHTS_ID
            require(manifest is not None and row["source_problem_key"] == manifest["native_index"] and row["source_year"] == manifest["index_order"]["year"], f"candidate/PutnamGAP join drifted: {candidate_id}")
            require(row["source_statement_sha256"] == manifest["record_locator"]["statement_value_sha256"] and row["source_solution_sha256"] == manifest["record_locator"]["solution_value_sha256"], f"candidate/PutnamGAP field hash drifted: {candidate_id}")
        elif row["source_branch"] == "kedlaya_2025":
            manifest = kedlaya_by_id.get(candidate_id)
            manifest_path, manifest_sha, rights_id = KEDLAYA_MANIFEST_REL, sha256(kedlaya_payload), KEDLAYA_RIGHTS_ID
            require(manifest is not None and row["source_problem_key"] == manifest["native_index"] and row["source_year"] == 2025, f"candidate/Kedlaya join drifted: {candidate_id}")
            require(row["source_statement_sha256"] == manifest["statement_binding"]["item_body_sha256"] and row["source_solution_sha256"] == manifest["solution_binding"]["item_body_sha256"], f"candidate/Kedlaya field hash drifted: {candidate_id}")
        else:
            raise FreezeError(f"candidate branch invalid: {candidate_id}")
        binding = exact_keys(row["source_binding"], {"source_id", "path", "file_sha256", "locator", "evidence_sha256", "rights_id"}, f"candidate binding: {candidate_id}")
        locator = exact_keys(binding["locator"], {"manifest_row_index", "manifest_row_sha256", "native_index"}, f"candidate locator: {candidate_id}")
        require(binding["path"] == manifest_path.as_posix() and binding["file_sha256"] == manifest_sha and binding["rights_id"] == rights_id and row["rights_id"] == rights_id, f"candidate source/rights binding drifted: {candidate_id}")
        require(locator["manifest_row_sha256"] == manifest["row_sha256"] and locator["native_index"] == manifest["native_index"] and binding["evidence_sha256"] == manifest["row_sha256"], f"candidate manifest evidence drifted: {candidate_id}")
        require(row["disposition"] == manifest["disposition"] and row["target_problem_key"] == manifest["target_problem_key"], f"candidate disposition drifted from manifest: {candidate_id}")
        if row["target_problem_key"] is not None:
            by_target[row["target_problem_key"]].append(candidate_id)
        candidate_by_id[candidate_id] = row
    require(Counter(row["source_branch"] for row in candidates) == Counter({"putnamgap": 1051, "kedlaya_2025": 12}), "candidate branch denominator drifted")
    require(set(by_target) == full_grid_keys() and all(len(ids) == 1 for ids in by_target.values()), "candidate target projection drifted")

    problem_by_key: dict[str, Mapping[str, Any]] = {}
    for index, raw_row in enumerate(problems):
        row = exact_keys(raw_row, PROBLEM_KEYS, f"problem[{index}]")
        require(row["schema_version"] == "awesome-theorems/full-putnam-source-problem/5.6" and row["row_sha256"] == hash_without(row, "row_sha256"), f"problem schema/seal drifted: {index}")
        key = row["problem_key"]
        require(isinstance(key, str) and key not in problem_by_key and row["coordinate"] == coordinate(key), f"problem key/coordinate drifted: {index}")
        require(row["source_candidate_ids"] == sorted(set(by_target[key])) and len(row["source_candidate_ids"]) == 1, f"problem candidate projection drifted: {key}")
        candidate = candidate_by_id[row["source_candidate_ids"][0]]
        require(row["source_branch"] == candidate["source_branch"] and row["source_statement_sha256"] == candidate["source_statement_sha256"] and row["source_solution_sha256"] == candidate["source_solution_sha256"] and row["rights_id"] == candidate["rights_id"], f"problem primary candidate binding drifted: {key}")
        pb = pb_by_key.get(key)
        require(row["putnambench_problem_row_sha256"] == (pb["row_sha256"] if pb else None) and row["formal_variant_ids"] == (pb["formal_variant_ids"] if pb else []), f"problem PutnamBench binding drifted: {key}")
        require(isinstance(row["anomaly_codes"], list), f"problem anomaly ledger malformed: {key}")
        problem_by_key[key] = row
    grid = full_grid_keys()
    require(set(problem_by_key) == grid, "problem grid coverage drifted")
    require(Counter(row["source_branch"] for row in problems) == Counter({"putnamgap": 756, "kedlaya_2025": 12}), "problem branch denominator drifted")

    counts = inventory["counts"]
    require(counts == {
        "full_grid_problem_keys": 768,
        "putnambench_subset_problem_keys": 675,
        "outside_putnambench_problem_keys": 93,
        "putnamgap_source_candidates": 1051,
        "kedlaya_2025_source_candidates": 12,
        "putnamgap_grid_problem_keys": 756,
        "kedlaya_2025_grid_problem_keys": 12,
        "putnamgap_out_of_scope_pre_1962_candidates": 295,
        "mapped_source_candidates": 768,
        "alternate_or_duplicate_source_candidates": 0,
        "rejected_malformed_source_candidates": 0,
    }, "inventory counts drifted")
    digests = inventory["set_digests"]
    expected_digests = {
        "full_grid_problem_key_set_sha256": set_digest(grid),
        "putnambench_problem_key_set_sha256": set_digest(pb_by_key),
        "supplemental_problem_key_set_sha256": set_digest(grid - set(pb_by_key)),
        "source_candidate_id_set_sha256": set_digest(candidate_by_id),
        "putnamgap_candidate_id_set_sha256": set_digest(pg_by_id),
        "mapped_putnamgap_candidate_id_set_sha256": set_digest(row["source_candidate_id"] for row in pg_rows if row["disposition"] == "mapped_in_scope_coordinate"),
        "pre_1962_putnamgap_candidate_id_set_sha256": set_digest(row["source_candidate_id"] for row in pg_rows if row["disposition"] == "out_of_scope_pre_1962"),
        "problem_row_set_sha256": set_digest(row["row_sha256"] for row in problems),
        "candidate_row_set_sha256": set_digest(row["row_sha256"] for row in candidates),
        "putnamgap_manifest_row_set_sha256": set_digest(row["row_sha256"] for row in pg_rows),
        "kedlaya_manifest_row_set_sha256": set_digest(row["row_sha256"] for row in kedlaya_rows),
    }
    require(digests == expected_digests, "inventory set digests drifted")

    output_dir = repository_root / OUTPUT_DIR_REL
    for path in output_dir.iterdir():
        lower = path.name.lower()
        require(not (path.is_file() and (lower.endswith(".tar") or lower.endswith(".tar.gz") or lower.endswith(".tgz"))), f"raw source archive embedded beside frozen outputs: {path.name}")
    return inventory, candidates, problems, pg_rows, kedlaya_rows


def atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fchmod(stream.fileno(), 0o644)
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def compare_full_rebuild(repository_root: Path, putnamgap_archive: Path, kedlaya_archive: Path) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    built = build(repository_root, putnamgap_archive, kedlaya_archive)
    for relative, payload in output_payloads(*built).items():
        path = repository_root / relative
        require(path.is_file() and path.read_bytes() == payload, f"frozen output differs from external-source replay: {relative}")
    validate_repo_only(repository_root)
    return built


def run(args: argparse.Namespace) -> int:
    repository_root = args.repo_root.resolve()
    if args.write:
        require(args.putnamgap_source_archive is not None and args.kedlaya_source_archive is not None, "--write requires both source archives")
        built = build(repository_root, args.putnamgap_source_archive.resolve(), args.kedlaya_source_archive.resolve())
        for relative, payload in output_payloads(*built).items():
            atomic_write(repository_root / relative, payload)
        result = validate_repo_only(repository_root)
        action = "WROTE"
    elif args.check:
        require(args.putnamgap_source_archive is None and args.kedlaya_source_archive is None, "--check is repository-only")
        result = validate_repo_only(repository_root)
        action = "PASS"
    else:
        require(args.putnamgap_source_archive is not None and args.kedlaya_source_archive is not None, "--audit-source-archives requires both source archives")
        result = compare_full_rebuild(repository_root, args.putnamgap_source_archive.resolve(), args.kedlaya_source_archive.resolve())
        action = "AUDIT PASS"
    inventory, candidates, problems, pg_rows, kedlaya_rows = result
    print(
        f"{action} full Putnam source freeze candidates={len(candidates)} "
        f"putnamgap={len(pg_rows)} kedlaya_2025={len(kedlaya_rows)} "
        f"grid={len(problems)} pb_subset=675 complement=93 "
        f"authority={inventory['authority_sha256']}"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--audit-source-archives", action="store_true")
    parser.add_argument("--putnamgap-source-archive", type=Path)
    parser.add_argument("--kedlaya-source-archive", type=Path)
    parser.add_argument("--repo-root", type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        return run(args)
    except (FreezeError, OSError, ValueError, KeyError, TypeError) as error:
        print(f"FAIL full Putnam source freeze: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
