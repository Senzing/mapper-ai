#!/usr/bin/env python3
"""
Senzing JSON Linter (no third-party deps)

Checks that JSON/JSONL documents follow the recommended structure:
- Root has DATA_SOURCE (string) and FEATURES (array of objects); RECORD_ID optional (string)
- Root payload attributes (any other keys) must be scalars (no arrays/objects)
- FEATURES is the only array at root
- Each FEATURES item is a flat object of one feature family (no nested arrays/objects)
- RECORD_TYPE is optional but recommended; include when known to prevent cross-type resolution
- Warn on unknown/likely-mistyped attribute names; error on mixed feature families

Usage:
  python tools/lint_senzing_json.py path
  - path can be a file (.json or .jsonl) or a directory (recurses *.json, *.jsonl)

Exit codes:
  0 = all files passed
  1 = one or more files had errors
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any, Dict, List, Tuple

SCALAR_TYPES = (str, int, float, bool, type(None))

ALLOWED_ROOT_KEYS = {"DATA_SOURCE", "RECORD_ID", "FEATURES"}

# Canonical allowed attributes per feature family (from the spec)
ALLOWED_ATTRS: Dict[str, set] = {
    # Record typing
    "RECORD_TYPE": {"RECORD_TYPE"},
    # Names
    "NAME": {
        "NAME_TYPE",
        "NAME_LAST",
        "NAME_FIRST",
        "NAME_MIDDLE",
        "NAME_PREFIX",
        "NAME_SUFFIX",
        "NAME_ORG",
        "NAME_FULL",
    },
    # Addresses
    "ADDRESS": {
        "ADDR_TYPE",
        "ADDR_LINE1",
        "ADDR_LINE2",
        "ADDR_LINE3",
        "ADDR_LINE4",
        "ADDR_LINE5",
        "ADDR_LINE6",
        "ADDR_CITY",
        "ADDR_STATE",
        "ADDR_POSTAL_CODE",
        "ADDR_COUNTRY",
        "ADDR_FULL",
    },
    # Contact
    "PHONE": {"PHONE_TYPE", "PHONE_NUMBER"},
    "EMAIL": {"EMAIL_ADDRESS"},
    "WEBSITE": {"WEBSITE_ADDRESS"},
    # Physical/other
    "GENDER": {"GENDER"},
    "DOB": {"DATE_OF_BIRTH"},
    "DOD": {"DATE_OF_DEATH"},
    "NATIONALITY": {"NATIONALITY"},
    "CITIZENSHIP": {"CITIZENSHIP"},
    "POB": {"PLACE_OF_BIRTH"},
    "REGISTRATION_DATE": {"REGISTRATION_DATE"},
    "REGISTRATION_COUNTRY": {"REGISTRATION_COUNTRY"},
    # Identifiers
    "PASSPORT": {"PASSPORT_NUMBER", "PASSPORT_COUNTRY"},
    "DRLIC": {"DRIVERS_LICENSE_NUMBER", "DRIVERS_LICENSE_STATE"},
    "SSN": {"SSN_NUMBER"},
    "NATIONAL_ID": {"NATIONAL_ID_TYPE", "NATIONAL_ID_NUMBER", "NATIONAL_ID_COUNTRY"},
    "TAX_ID": {"TAX_ID_TYPE", "TAX_ID_NUMBER", "TAX_ID_COUNTRY"},
    "OTHER_ID": {"OTHER_ID_TYPE", "OTHER_ID_NUMBER", "OTHER_ID_COUNTRY"},
    "TRUSTED_ID": {"TRUSTED_ID_TYPE", "TRUSTED_ID_NUMBER"},
    "ACCOUNT": {"ACCOUNT_NUMBER", "ACCOUNT_DOMAIN"},
    "DUNS_NUMBER": {"DUNS_NUMBER"},
    "NPI_NUMBER": {"NPI_NUMBER"},
    "LEI_NUMBER": {"LEI_NUMBER"},
    # Groups & employment
    "EMPLOYER": {"EMPLOYER"},
    "GROUP_ASSOCIATION": {"GROUP_ASSOCIATION_TYPE", "GROUP_ASSOCIATION_ORG_NAME"},
    "GROUP_ASSN_ID": {"GROUP_ASSN_ID_TYPE", "GROUP_ASSN_ID_NUMBER"},
    # Relationships
    "REL_ANCHOR": {"REL_ANCHOR_DOMAIN", "REL_ANCHOR_KEY"},
    "REL_POINTER": {"REL_POINTER_DOMAIN", "REL_POINTER_KEY", "REL_POINTER_ROLE"},
    # Social handles (attribute name equals feature)
    "LINKEDIN": {"LINKEDIN"},
    "FACEBOOK": {"FACEBOOK"},
    "TWITTER": {"TWITTER"},
    "SKYPE": {"SKYPE"},
    "ZOOMROOM": {"ZOOMROOM"},
    "INSTAGRAM": {"INSTAGRAM"},
    "WHATSAPP": {"WHATSAPP"},
    "SIGNAL": {"SIGNAL"},
    "TELEGRAM": {"TELEGRAM"},
    "TANGO": {"TANGO"},
    "VIBER": {"VIBER"},
    "WECHAT": {"WECHAT"},
}

# Map attribute key to family for fast lookup
KEY_TO_FAMILY: Dict[str, str] = {}
for fam, keys in ALLOWED_ATTRS.items():
    for k in keys:
        KEY_TO_FAMILY[k] = fam

ALLOWED_RECORD_TYPES = {"PERSON", "ORGANIZATION", "VESSEL", "AIRCRAFT"}


def is_scalar(value: Any) -> bool:
    return isinstance(value, SCALAR_TYPES)


def detect_family(key: str) -> str | None:
    return KEY_TO_FAMILY.get(key)


def feature_families(obj: Dict[str, Any]) -> Tuple[List[str], List[str]]:
    families: List[str] = []
    unknown: List[str] = []
    for k in obj.keys():
        fam = detect_family(k)
        if fam is None and k.isupper():
            unknown.append(k)
        elif fam is not None:
            if fam not in families:
                families.append(fam)
    return families, unknown


def lint_record(doc: Any, where: str, *, strict: bool = True) -> List[str]:
    errors: List[str] = []
    warnings: List[str] = []

    if not isinstance(doc, dict):
        return [f"{where}: Root must be an object"]

    # Root keys
    if "DATA_SOURCE" not in doc or not isinstance(doc.get("DATA_SOURCE"), str):
        errors.append(f"{where}: Missing or non-string DATA_SOURCE at root")
    if "FEATURES" not in doc or not isinstance(doc.get("FEATURES"), list):
        errors.append(f"{where}: Missing or non-array FEATURES at root")

    if "RECORD_ID" in doc and not isinstance(doc.get("RECORD_ID"), str):
        errors.append(f"{where}: RECORD_ID must be a string when present")

    # Root payload types (no arrays/objects besides FEATURES)
    for k, v in doc.items():
        if k in ALLOWED_ROOT_KEYS:
            continue
        # Check if this is a feature attribute that should not be at root level
        if k in KEY_TO_FAMILY:
            errors.append(
                f"{where}: Feature attribute '{k}' must be inside FEATURES array, not at root level"
            )
            continue
        if not is_scalar(v):
            errors.append(
                f"{where}: Root attribute '{k}' must be a scalar (string/number/boolean/null); no objects/arrays at root"
            )

    # FEATURES content
    features = doc.get("FEATURES") if isinstance(doc.get("FEATURES"), list) else []
    seen_rel_anchor = False
    has_record_type = False
    for idx, item in enumerate(features):
        loc = f"{where}#FEATURES[{idx}]"
        if not isinstance(item, dict):
            errors.append(f"{loc}: Must be an object")
            continue
        # No nested arrays/objects
        for kk, vv in item.items():
            if not is_scalar(vv):
                errors.append(f"{loc}: Attribute '{kk}' must be scalar; found {type(vv).__name__}")
        if "RECORD_TYPE" in item and isinstance(item.get("RECORD_TYPE"), str):
            has_record_type = True
            if item["RECORD_TYPE"] not in ALLOWED_RECORD_TYPES:
                errors.append(
                    f"{loc}: RECORD_TYPE '{item['RECORD_TYPE']}' is not allowed; "
                    f"must be one of {sorted(ALLOWED_RECORD_TYPES)}"
                )
        fams, unknown = feature_families(item)
        # --- Address Rule ---
        if "ADDR_FULL" in item:
            addr_parts = {
                "ADDR_LINE1",
                "ADDR_LINE2",
                "ADDR_LINE3",
                "ADDR_LINE4",
                "ADDR_LINE5",
                "ADDR_LINE6",
                "ADDR_CITY",
                "ADDR_STATE",
                "ADDR_POSTAL_CODE",
                "ADDR_COUNTRY",
            }
            bad_mix = addr_parts & set(item.keys())
            if bad_mix:
                errors.append(
                    f"{loc}: Invalid address mix: ADDR_FULL cannot be combined with parsed fields {sorted(bad_mix)}"
                )

        # --- Name Rule ---
        if "NAME_FULL" in item:
            name_parts = {"NAME_ORG", "NAME_LAST", "NAME_FIRST", "NAME_MIDDLE", "NAME_SUFFIX", "NAME_PREFIX"}
            bad_mix = name_parts & set(item.keys())
            if bad_mix:
                errors.append(
                    f"{loc}: Invalid name mix: NAME_FULL cannot be combined with parsed fields {sorted(bad_mix)}"
                )

        # --- Relationship Rules ---
        if "REL_ANCHOR" in fams:
            if "REL_ANCHOR_DOMAIN" not in item or "REL_ANCHOR_KEY" not in item:
                errors.append(f"{loc}: REL_ANCHOR missing REL_ANCHOR_DOMAIN or REL_ANCHOR_KEY")
            if seen_rel_anchor:
                errors.append(f"{loc}: Multiple REL_ANCHOR features not allowed")
            seen_rel_anchor = True

        if "REL_POINTER" in fams:
            if "REL_POINTER_DOMAIN" not in item or "REL_POINTER_KEY" not in item:
                errors.append(f"{loc}: REL_POINTER missing REL_POINTER_DOMAIN or REL_POINTER_KEY")

        if ("REL_ANCHOR_DOMAIN" in item or "REL_ANCHOR_KEY" in item) and (
            "REL_POINTER_DOMAIN" in item or "REL_POINTER_KEY" in item
        ):
            errors.append(f"{loc}: Cannot mix REL_ANCHOR and REL_POINTER in same feature")

        # Unknown uppercase keys handling
        for u in unknown:
            msg = f"{loc}: Unrecognized attribute '{u}' — verify against spec"
            if strict:
                errors.append(msg)
            else:
                print(f"WARN: {msg}", file=sys.stderr)
        if len(fams) == 0:
            warnings.append(f"{loc}: No recognized feature attributes; check attribute names")
        elif len(fams) > 1:
            errors.append(f"{loc}: Mixed feature families {fams}; split into separate feature objects")
        else:
            fam = fams[0]
            allowed = ALLOWED_ATTRS.get(fam, set())
            for kk in item.keys():
                # allow RECORD_TYPE-only objects
                if fam == "RECORD_TYPE" and kk == "RECORD_TYPE":
                    continue
                # If key maps to a different family, it's mixed (already handled)
                # Enforce allowed attributes within family
                if kk not in allowed:
                    errors.append(f"{loc}: Attribute '{kk}' not allowed for family {fam}")

    # --- Cross-feature validation: NAME_ORG and NAME_LAST conflict ---
    has_name_org = False
    has_name_last = False
    for item in features:
        if isinstance(item, dict):
            if "NAME_ORG" in item:
                has_name_org = True
            if "NAME_LAST" in item:
                has_name_last = True
    
    if has_name_org and has_name_last:
        errors.append(f"{where}: Cannot have both NAME_ORG and NAME_LAST in FEATURES array; indicates confusion between person and organization")

    if not has_record_type:
        warnings.append(f"{where}: Missing RECORD_TYPE; include when known to prevent cross-type resolution")

    # Report warnings as notes but do not fail build; print to stderr
    for w in warnings:
        print(f"WARN: {w}", file=sys.stderr)

    return errors


def iter_paths(root: str) -> List[str]:
    if os.path.isdir(root):
        out: List[str] = []
        for d, _, files in os.walk(root):
            for fn in files:
                if fn.lower().endswith((".json", ".jsonl")):
                    out.append(os.path.join(d, fn))
        return sorted(out)
    return [root]


def load_file(path: str) -> List[Tuple[Any, str]]:
    items: List[Tuple[Any, str]] = []
    with open(path, "r", encoding="utf-8") as f:
        if path.lower().endswith(".jsonl"):
            for i, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    items.append((json.loads(line), f"{path}:{i}"))
                except json.JSONDecodeError as e:
                    items.append((None, f"{path}:{i} (invalid JSON: {e})"))
        else:
            try:
                items.append((json.load(f), path))
            except json.JSONDecodeError as e:
                items.append((None, f"{path} (invalid JSON: {e})"))
    return items


def main(argv: List[str]) -> int:
    if len(argv) < 2:
        print(__doc__.strip())
        return 2

    target = argv[1]
    strict = True
    if len(argv) >= 3 and argv[2] == "--no-strict":
        strict = False
    paths = iter_paths(target)
    if not paths:
        print(f"No JSON/JSONL files found in {target}")
        return 2

    total_errors = 0
    for p in paths:
        for obj, where in load_file(p):
            if obj is None:
                print(f"ERROR: {where}")
                total_errors += 1
                continue
            errs = lint_record(obj, where, strict=strict)
            if errs:
                total_errors += len(errs)
                for e in errs:
                    print(f"ERROR: {e}")

    if total_errors:
        print(f"\nFAIL: {total_errors} error(s) found", file=sys.stderr)
        return 1
    print("OK: All files passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
