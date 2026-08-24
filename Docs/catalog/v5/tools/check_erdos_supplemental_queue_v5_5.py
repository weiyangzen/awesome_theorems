#!/usr/bin/env python3
"""Independent checker for the fixed 167-row Erdős supplemental queue."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
BASE = Path("Docs/catalog/v5/curation/erdos_parent_join_v5_5")
SOURCE_REL = BASE / "resolved-theorem-rows.jsonl"
SELECTED_REL = BASE / "resolved-theorem-max2-selected.jsonl"
QUEUE_REL = BASE / "resolved-theorem-supplemental.jsonl"
RECEIPT_REL = BASE / "resolved-theorem-supplemental-receipt.json"

EXPECTED_SOURCE_SHA = "5bf64315db3eca7aba7111bf234ec913bb7b5d4b00b0f2693676cc7d9aa99e2b"
EXPECTED_SELECTED_SHA = "a65f8e9841dd415894cbfc5f032283fa05e4bd1161c6bd4c8a4ae3e9e0e64cae"
EXPECTED_QUEUE_SHA = "6d31bf21d1182e3d1dd908fa27d552340fcb6169636541b04fbf26ea1a7e65a7"
EXPECTED_RECEIPT_FILE_SHA = "c6568c36e99a45eac8bac1f4a575cefecf22d33ba783031f1c4165f47b8f29fb"
EXPECTED_RECEIPT_AUTHORITY = "9d46834e999f20d013650ccea1e1731d705676243155ececf727aae0613b218a"


class CheckError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckError(message)


def file_sha(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def canonical_sha(value: object) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return sha256(raw).hexdigest()


def parse_jsonl(raw: bytes, label: str) -> tuple[list[bytes], list[dict]]:
    lines = raw.splitlines(keepends=True)
    require(all(line.endswith(b"\n") for line in lines), f"{label} must use one LF-terminated JSON object per row")
    try:
        rows = [json.loads(line) for line in lines]
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise CheckError(f"{label} is not valid UTF-8 JSONL: {error}") from error
    return lines, rows


def exact_key(row: dict) -> tuple[str, str]:
    try:
        stage = row["parent"]["stage_claim_id"]
        variant = row["parent"]["variant_id"]
    except (KeyError, TypeError) as error:
        raise CheckError(f"row lacks exact parent identity: {error}") from error
    require(isinstance(stage, str) and isinstance(variant, str), "exact parent identity fields must be strings")
    return stage, variant


def pair_object(pair: tuple[str, str]) -> dict[str, str]:
    return {"stage_claim_id": pair[0], "variant_id": pair[1]}


def main() -> None:
    source_path = ROOT / SOURCE_REL
    selected_path = ROOT / SELECTED_REL
    queue_path = ROOT / QUEUE_REL
    receipt_path = ROOT / RECEIPT_REL
    for path in (source_path, selected_path, queue_path, receipt_path):
        require(path.is_file(), f"missing required artifact: {path.relative_to(ROOT)}")

    require(file_sha(source_path) == EXPECTED_SOURCE_SHA, "resolved-theorem-rows parent hash drifted")
    require(file_sha(selected_path) == EXPECTED_SELECTED_SHA, "max2-selected parent hash drifted")
    require(file_sha(queue_path) == EXPECTED_QUEUE_SHA, "supplemental queue hash drifted")
    require(file_sha(receipt_path) == EXPECTED_RECEIPT_FILE_SHA, "supplemental receipt file hash drifted")

    source_lines, source_rows = parse_jsonl(source_path.read_bytes(), "resolved source")
    selected_lines, selected_rows = parse_jsonl(selected_path.read_bytes(), "max2 selection")
    queue_lines, queue_rows = parse_jsonl(queue_path.read_bytes(), "supplemental queue")
    require(len(source_rows) == 546, "resolved source row count is not 546")
    require(len(selected_rows) == 379, "max2 selection row count is not 379")
    require(len(queue_rows) == 167, "supplemental queue row count is not 167")

    source_keys = [exact_key(row) for row in source_rows]
    selected_keys = [exact_key(row) for row in selected_rows]
    queue_keys = [exact_key(row) for row in queue_rows]
    require(len(set(source_keys)) == 546, "resolved exact keys are not unique")
    require(len(set(selected_keys)) == 379, "selected exact keys are not unique")
    require(len(set(queue_keys)) == 167, "supplemental exact keys are not unique")
    source_set = set(source_keys)
    selected_set = set(selected_keys)
    queue_set = set(queue_keys)
    require(selected_set <= source_set, "selected key is absent from resolved source")
    require(selected_set.isdisjoint(queue_set), "selected and supplemental key sets overlap")
    require(selected_set | queue_set == source_set, "selected plus supplemental does not exactly partition resolved keys")

    expected_line_pairs = [
        (line, pair) for line, pair in zip(source_lines, source_keys) if pair not in selected_set
    ]
    expected_lines = [line for line, _ in expected_line_pairs]
    expected_keys = [pair for _, pair in expected_line_pairs]
    require(queue_lines == expected_lines, "queue is not the byte-identical ordered source difference")
    require(queue_keys == expected_keys, "queue keys do not preserve resolved source order")

    try:
        receipt = json.loads(receipt_path.read_bytes())
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise CheckError(f"receipt is invalid JSON: {error}") from error
    require(receipt.get("schema_version") == "awesome-theorems/erdos-supplemental-queue-receipt/5.5", "receipt schema drifted")
    authority = receipt.get("authority_sha256")
    require(authority == EXPECTED_RECEIPT_AUTHORITY, "receipt authority constant drifted")
    unsigned = dict(receipt)
    unsigned.pop("authority_sha256", None)
    require(canonical_sha(unsigned) == authority, "receipt canonical authority is invalid")

    resolved_binding = receipt["source_bindings"]["resolved_theorem_rows"]
    selected_binding = receipt["source_bindings"]["max2_selected"]
    queue_binding = receipt["supplemental_queue"]
    require(
        resolved_binding == {
            "path": str(SOURCE_REL), "sha256": EXPECTED_SOURCE_SHA,
            "bytes": source_path.stat().st_size, "rows": 546,
        },
        "resolved source receipt binding drifted",
    )
    require(
        selected_binding == {
            "path": str(SELECTED_REL), "sha256": EXPECTED_SELECTED_SHA,
            "bytes": selected_path.stat().st_size, "rows": 379,
        },
        "max2 receipt binding drifted",
    )
    require(
        queue_binding == {
            "path": str(QUEUE_REL), "sha256": EXPECTED_QUEUE_SHA,
            "bytes": queue_path.stat().st_size, "rows": 167,
            "zero_based_first": 0, "zero_based_last": 166,
        },
        "queue receipt binding drifted",
    )
    require(receipt["construction"]["exclusion_key"] == ["parent.stage_claim_id", "parent.variant_id"], "exclusion key drifted")
    require(receipt["counts"] == {
        "resolved_rows": 546,
        "max2_selected_rows": 379,
        "supplemental_rows": 167,
        "arithmetic_difference": 167,
        "unique_resolved_keys": 546,
        "unique_selected_keys": 379,
        "unique_supplemental_keys": 167,
    }, "receipt counts drifted")

    pair_sort = lambda pair: (pair[0].encode(), pair[1].encode())
    expected_digests = {
        "resolved_key_set_sha256": canonical_sha([pair_object(x) for x in sorted(source_keys, key=pair_sort)]),
        "selected_key_set_sha256": canonical_sha([pair_object(x) for x in sorted(selected_keys, key=pair_sort)]),
        "supplemental_key_set_sha256": canonical_sha([pair_object(x) for x in sorted(queue_keys, key=pair_sort)]),
        "supplemental_ordered_keys_sha256": canonical_sha([pair_object(x) for x in queue_keys]),
        "supplemental_ordered_source_identity_payload_sha256_values_sha256": canonical_sha(
            [row["identity"]["identity_payload_sha256"] for row in queue_rows]
        ),
    }
    require(receipt["set_digests"] == expected_digests, "receipt set digest changed")
    require(all(receipt["invariants"].values()), "receipt reports a failed invariant")
    require(receipt["credit_boundary"] == {
        "frontier_theorem_credit_granted": 0,
        "new_theorem_credit_granted": 0,
        "release_modified": False,
        "queue_membership_grants_credit": False,
    }, "queue improperly grants credit or modifies the release")

    print(
        "PASS erdos supplemental queue "
        f"resolved={len(source_rows)} selected={len(selected_rows)} supplemental={len(queue_rows)} "
        f"queue_sha256={EXPECTED_QUEUE_SHA} authority_sha256={EXPECTED_RECEIPT_AUTHORITY}"
    )


if __name__ == "__main__":
    try:
        main()
    except CheckError as error:
        raise SystemExit(f"FAIL: {error}")
