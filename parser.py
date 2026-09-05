import sys
import re
import json
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTextEdit, QLineEdit, QPushButton, QTreeWidget, QTreeWidgetItem,
    QSplitter, QFrame, QSpinBox, QFileDialog, QStatusBar,
    QToolBar, QSizePolicy, QMessageBox, QGroupBox, QDialog,
    QDialogButtonBox, QHeaderView, QAbstractItemView, QTabWidget,
    QPlainTextEdit, QComboBox, QCheckBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import (
    QFont, QColor, QPalette, QTextCharFormat,
    QSyntaxHighlighter, QBrush
)

# ─────────────────────────────────────────────
#  PALETTE & STYLE
# ─────────────────────────────────────────────
DARK_BG        = "#0D1117"
PANEL_BG       = "#161B22"
BORDER         = "#30363D"
ACCENT         = "#FEFEFE"
ACCENT_HOVER   = "#FFFFFF"
SUCCESS        = "#FFFFFF"
WARNING        = "#D29922"
ERROR_COLOR    = "#FFFFFF"
TEXT_PRIMARY   = "#E6EDF3"
TEXT_SECONDARY = "#8B949E"
TAG_COLOR      = "#FF7B72"
LEN_COLOR      = "#FFFFFF"
VAL_COLOR      = "#FFFFFF"
LEN_ERROR_C    = "#D29922"
DELETE_RED        = "#F85149"
ADD_GREEN         = "#3FB950"
SEARCH_HIGHLIGHT  = "#2D4A1E"   # dark green background for matched rows
SEARCH_MATCH_FORE = "#7EE787"   # bright green text for matched rows
SEARCH_CURRENT    = "#1C3452"   # blue tint for the focused match

GLOBAL_STYLE = f"""
QMainWindow, QWidget {{
    background-color: {DARK_BG};
    color: {TEXT_PRIMARY};
    font-family: 'Segoe UI', 'Inter', 'Helvetica Neue', Arial, sans-serif;
    font-size: 13px;
}}
QSplitter::handle {{
    background-color: {BORDER};
    width: 2px;
    height: 2px;
}}
QGroupBox {{
    border: 1px solid {BORDER};
    border-radius: 8px;
    margin-top: 12px;
    padding: 10px;
    font-weight: 600;
    color: {TEXT_SECONDARY};
    font-size: 11px;
    letter-spacing: 0.8px;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
}}
QTextEdit, QLineEdit, QPlainTextEdit {{
    background-color: {PANEL_BG};
    border: 1px solid {BORDER};
    border-radius: 6px;
    color: {TEXT_PRIMARY};
    padding: 8px 10px;
    font-family: 'Cascadia Code', 'Fira Code', 'JetBrains Mono', 'Consolas', monospace;
    font-size: 12px;
    selection-background-color: {ACCENT};
}}
QTextEdit:focus, QLineEdit:focus, QPlainTextEdit:focus {{
    border-color: {ACCENT};
}}
QPushButton {{
    background-color: {PANEL_BG};
    border: 1px solid {BORDER};
    border-radius: 6px;
    color: {TEXT_PRIMARY};
    padding: 7px 16px;
    font-weight: 600;
    font-size: 12px;
    min-height: 32px;
}}
QPushButton:hover {{
    border-color: {ACCENT};
    color: {ACCENT};
}}
QPushButton:pressed {{
    background-color: #21262D;
}}
QPushButton#primary {{
    background-color: {ACCENT};
    border-color: {ACCENT};
    color: #000000;
}}
QPushButton#primary:hover {{
    background-color: {ACCENT_HOVER};
    border-color: {ACCENT_HOVER};
    color: #000000;
}}
QPushButton#success {{
    background-color: {SUCCESS};
    border-color: {SUCCESS};
    color: #000000;
}}
QPushButton#danger {{
    background-color: transparent;
    border: 1px solid {ERROR_COLOR};
    color: {ERROR_COLOR};
}}
QPushButton#danger:hover {{
    background-color: {ERROR_COLOR};
    color: #ffffff;
}}
QPushButton#delete_tag {{
    background-color: transparent;
    border: 1px solid {DELETE_RED};
    color: {DELETE_RED};
    font-size: 12px;
    min-height: 28px;
    padding: 4px 12px;
}}
QPushButton#delete_tag:hover {{
    background-color: {DELETE_RED};
    color: #ffffff;
}}
QPushButton#add_tag {{
    background-color: transparent;
    border: 1px solid {ADD_GREEN};
    color: {ADD_GREEN};
    font-size: 12px;
    min-height: 28px;
    padding: 4px 12px;
}}
QPushButton#add_tag:hover {{
    background-color: {ADD_GREEN};
    color: #000000;
}}
QTreeWidget {{
    background-color: {PANEL_BG};
    border: 1px solid {BORDER};
    border-radius: 8px;
    color: {TEXT_PRIMARY};
    alternate-background-color: #1C2128;
    outline: none;
    font-family: 'Cascadia Code', 'Fira Code', 'Consolas', monospace;
    font-size: 12px;
}}
QTreeWidget::item {{
    padding: 4px 6px;
    border-bottom: 1px solid #21262D;
    min-height: 24px;
}}
QTreeWidget::item:selected {{
    background-color: #1C3452;
    color: {TEXT_PRIMARY};
    border-left: 2px solid {ACCENT};
}}
QTreeWidget::item:hover {{
    background-color: #21262D;
}}
QHeaderView::section {{
    background-color: #21262D;
    border: none;
    border-bottom: 1px solid {BORDER};
    padding: 6px 10px;
    font-weight: 700;
    font-size: 11px;
    color: {TEXT_SECONDARY};
    letter-spacing: 0.5px;
}}
QStatusBar {{
    background-color: {PANEL_BG};
    border-top: 1px solid {BORDER};
    color: {TEXT_SECONDARY};
    font-size: 11px;
    padding: 2px 10px;
}}
QToolBar {{
    background-color: {PANEL_BG};
    border-bottom: 1px solid {BORDER};
    spacing: 4px;
    padding: 4px 8px;
}}
QScrollBar:vertical {{
    background-color: {PANEL_BG};
    width: 8px;
    border-radius: 4px;
}}
QScrollBar::handle:vertical {{
    background-color: {BORDER};
    border-radius: 4px;
    min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{
    background-color: {TEXT_SECONDARY};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
QScrollBar:horizontal {{
    background-color: {PANEL_BG};
    height: 8px;
    border-radius: 4px;
}}
QScrollBar::handle:horizontal {{
    background-color: {BORDER};
    border-radius: 4px;
    min-width: 30px;
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0; }}
QSpinBox {{
    background-color: {PANEL_BG};
    border: 1px solid {BORDER};
    border-radius: 6px;
    color: {TEXT_PRIMARY};
    padding: 4px 8px;
    font-size: 12px;
    min-height: 28px;
}}
QSpinBox::up-button, QSpinBox::down-button {{
    background-color: {BORDER};
    border-radius: 3px;
    width: 16px;
}}
QTabWidget::pane {{
    border: 1px solid {BORDER};
    border-radius: 6px;
    background-color: {PANEL_BG};
}}
QTabBar::tab {{
    background-color: {DARK_BG};
    border: 1px solid {BORDER};
    border-bottom: none;
    border-radius: 6px 6px 0 0;
    padding: 6px 16px;
    color: {TEXT_SECONDARY};
    font-size: 12px;
    font-weight: 600;
}}
QTabBar::tab:selected {{
    background-color: {PANEL_BG};
    color: {TEXT_PRIMARY};
    border-bottom: 2px solid {ACCENT};
}}
QTabBar::tab:hover {{
    color: {TEXT_PRIMARY};
}}
QComboBox {{
    background-color: {PANEL_BG};
    border: 1px solid {BORDER};
    border-radius: 6px;
    color: {TEXT_PRIMARY};
    padding: 4px 10px;
    font-size: 12px;
    min-height: 28px;
}}
QComboBox:focus {{
    border-color: {ACCENT};
}}
QComboBox::drop-down {{
    border: none;
    width: 20px;
}}
QComboBox QAbstractItemView {{
    background-color: {PANEL_BG};
    border: 1px solid {BORDER};
    color: {TEXT_PRIMARY};
    selection-background-color: #1C3452;
}}
"""

# ─────────────────────────────────────────────
#  TAG DICTIONARY — chargé depuis tags.json
# ─────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TAGS_JSON  = os.path.join(SCRIPT_DIR, "tags.json")
BITS_JSON  = os.path.join(SCRIPT_DIR, "BIT_DEFINITIONS_WITH_POSITIONS.json")


def load_tag_dictionary(path: str) -> dict:
    print(f"[TLV Parser] Chargement dictionnaire : {path}")
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        result = {}
        for k, v in raw.items():
            key = k.strip().upper()
            if isinstance(v, list):
                result[key] = v
            else:
                result[key] = [{"name": str(v).strip(), "length_rule": {"type": "any"},
                                 "length_raw": "", "templates": []}]
        print(f"[TLV Parser] {len(result)} tags chargés depuis tags.json") 
        return result
    except FileNotFoundError:
        print(f"[TLV Parser] AVERTISSEMENT : tags.json introuvable.")
        return {}
    except json.JSONDecodeError as e:
        print(f"[TLV Parser] ERREUR : tags.json invalide — {e}")
        return {}


def load_bit_definitions(path: str) -> tuple[dict, dict]:
    print(f"[TLV Parser] Chargement bit definitions : {path}")
    bit_defs: dict = {}
    pos_defs: dict = {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)

        for entry in raw.get("BIT_DEFINITIONS", []):
            tag = entry["Tag"].strip().upper()
            bit_defs.setdefault(tag, []).append(entry)

        for entry in raw.get("POSITION_DEFINITIONS", []):
            tag = entry["Tag"].strip().upper()
            pos  = entry["Position"]
            nv   = entry["Nibble Value"]
            meaning = entry["Meaning"]
            pos_label = entry.get("Position Label", f"Position {pos}")

            pos_defs.setdefault(tag, {})
            pos_defs[tag].setdefault(pos, {"label": pos_label, "values": {}})
            pos_defs[tag][pos]["values"][nv] = meaning

        print(f"[TLV Parser] {len(bit_defs)} tags avec BIT_DEFINITIONS, "
              f"{len(pos_defs)} tags avec POSITION_DEFINITIONS")
        return bit_defs, pos_defs

    except FileNotFoundError:
        print(f"[TLV Parser] AVERTISSEMENT : {path} introuvable.")
        return {}, {}
    except json.JSONDecodeError as e:
        print(f"[TLV Parser] ERREUR JSON : {e}")
        return {}, {}


TAG_DICT: dict = load_tag_dictionary(TAGS_JSON)
BIT_DEFS: dict = {}
POS_DEFS: dict = {}
BIT_DEFS, POS_DEFS = load_bit_definitions(BITS_JSON)


# ─────────────────────────────────────────────
#  BIT / POSITION DECODING HELPERS
# ─────────────────────────────────────────────

def decode_bits(tag_hex: str, value_hex: str) -> list[dict]:
    tag = tag_hex.upper()
    entries = BIT_DEFS.get(tag)
    if not entries:
        return []

    try:
        value_bytes = bytes.fromhex(value_hex)
    except ValueError:
        return []

    byte_groups: dict[str, dict] = {}
    byte_order: list[str] = []
    for e in entries:
        bl = e["Byte"]
        if bl not in byte_groups:
            byte_groups[bl] = {"byte_label": bl, "byte_index": None, "byte_val": None, "bits": []}
            byte_order.append(bl)
        byte_groups[bl]["bits"].append(e)

    for bl, grp in byte_groups.items():
        m = re.match(r"Byte\s+(\d+)", bl)
        if m:
            grp["byte_index"] = int(m.group(1)) - 1

    result = []
    for bl in byte_order:
        grp = byte_groups[bl]
        idx = grp["byte_index"]
        if idx is None or idx >= len(value_bytes):
            continue
        bval = value_bytes[idx]
        active = []
        for e in grp["bits"]:
            try:
                mask_val = e.get("Mask")
                if mask_val is None:
                    continue
                mask = int(mask_val, 16) if isinstance(mask_val, str) else int(mask_val)
            except (ValueError, KeyError, TypeError):
                continue
            if bval & mask:
                bit_lbl = e["Bit"]
                desc    = e["Description"]
                active.append(f" {bit_lbl} (Mask {e['Mask']}, value 0x{bval & mask:02X}) --> {desc}")
        result.append({
            "byte_label": bl,
            "byte_val":   bval,
            "active_bits": active,
        })
    return result


def decode_positions(tag_hex: str, value_hex: str) -> list[dict]:
    tag = tag_hex.upper()
    pos_map = POS_DEFS.get(tag)
    if not pos_map:
        return []

    try:
        value_hex_clean = value_hex.upper().replace(" ", "")
    except Exception:
        return []

    decoded = []
    for pos_idx in sorted(pos_map.keys()):
        entry = pos_map[pos_idx]
        char_idx = pos_idx - 1
        if char_idx >= len(value_hex_clean):
            continue
        nibble_char = value_hex_clean[char_idx]
        try:
            nibble_val = int(nibble_char, 16)
        except ValueError:
            continue
        meaning = entry["values"].get(nibble_val, f"Unknown (0x{nibble_char})")
        decoded.append({
            "position": pos_idx,
            "label":    entry["label"],
            "nibble":   nibble_val,
            "meaning":  meaning,
        })
    return decoded


def render_bit_decode_text(tag_hex: str, value_hex: str) -> str:
    lines = []

    byte_groups = decode_bits(tag_hex, value_hex)
    if byte_groups:
        for grp in byte_groups:
            bval = grp["byte_val"]
            byte_short = grp["byte_label"].split("–")[0].strip()
            lines.append(f"  +--+ {byte_short} ({bval:02X})")
            for bit_line in grp["active_bits"]:
                lines.append(f"  |  +--+ {bit_line.strip()}")

    pos_decoded = decode_positions(tag_hex, value_hex)
    if pos_decoded:
        for p in pos_decoded:
            lines.append(f"  +--+ Position {p['position']} — {p['label']}")
            lines.append(f"  |  +--+ Nibble {p['nibble']} → {p['meaning']}")

    return "\n".join(lines)


def render_bit_decode_html(tag_hex: str, value_hex: str) -> str:
    parts = []

    byte_groups = decode_bits(tag_hex, value_hex)
    if byte_groups:
        parts.append(
            f"<div style='margin-top:8px; color:{TEXT_SECONDARY}; "
            f"font-size:11px; letter-spacing:0.5px;'>BIT DECODE</div>"
        )
        for grp in byte_groups:
            bval = grp["byte_val"]
            byte_short = re.sub(r"\s*–.*", "", grp["byte_label"]).strip()
            byte_title = grp["byte_label"]
            parts.append(
                f"<div style='margin-top:6px;'>"
                f"<span style='color:{WARNING}; font-weight:700;'>{byte_short}</span>"
                f" <span style='color:{TEXT_SECONDARY}; font-size:11px;'>"
                f"(0x{bval:02X} = {bval})</span>"
                f" <span style='color:{TEXT_SECONDARY}; font-size:10px; font-style:italic;'>"
                f"{byte_title}</span>"
                f"</div>"
            )
            if grp["active_bits"]:
                for bit_line in grp["active_bits"]:
                    m = re.match(r"\s*(Bit[s]?\s+[\d\-]+)\s+\(([^)]+)\)\s+-->\s+(.*)", bit_line)
                    if m:
                        bit_lbl, bit_detail, bit_desc = m.group(1), m.group(2), m.group(3)
                        parts.append(
                            f"<div style='margin-left:16px; margin-top:2px;'>"
                            f"<span style='color:{TAG_COLOR};'>✓ {bit_lbl}</span>"
                            f" <span style='color:{TEXT_SECONDARY}; font-size:10px;'>({bit_detail})</span>"
                            f" <span style='color:{TEXT_PRIMARY};'>→ {bit_desc}</span>"
                            f"</div>"
                        )
                    else:
                        parts.append(
                            f"<div style='margin-left:16px; color:{TEXT_PRIMARY};'>{bit_line.strip()}</div>"
                        )
            else:
                parts.append(
                    f"<div style='margin-left:16px; color:{TEXT_SECONDARY}; font-size:11px;'>"
                    f"(no active bits)</div>"
                )

    pos_decoded = decode_positions(tag_hex, value_hex)
    if pos_decoded:
        parts.append(
            f"<div style='margin-top:10px; color:{TEXT_SECONDARY}; "
            f"font-size:11px; letter-spacing:0.5px;'>NIBBLE / POSITION DECODE</div>"
        )
        for p in pos_decoded:
            parts.append(
                f"<div style='margin-top:4px;'>"
                f"<span style='color:{WARNING}; font-weight:700;'>Pos {p['position']}</span>"
                f" <span style='color:{TEXT_SECONDARY}; font-size:11px;'>— {p['label']}</span>"
                f" : <span style='color:{TEXT_PRIMARY};'>"
                f"nibble=<b>{p['nibble']}</b> → {p['meaning']}</span>"
                f"</div>"
            )

    return "".join(parts)


# ─────────────────────────────────────────────
#  TAG RESOLUTION HELPERS
# ─────────────────────────────────────────────

def length_matches(length_bytes: int, rule: dict) -> bool:
    rtype = rule.get("type", "any")
    if rtype == "any":
        return True
    if rtype == "exact":
        return length_bytes == rule.get("value")
    if rtype == "range":
        return rule.get("min", 0) <= length_bytes <= rule.get("max", float("inf"))
    if rtype == "max":
        return length_bytes <= rule.get("value", float("inf"))
    if rtype == "choice":
        return length_bytes in rule.get("values", [])
    return True


def format_length_rule(rule: dict, raw: str = "") -> str:
    if raw:
        return raw
    rtype = rule.get("type", "any")
    if rtype == "exact":
        return f"{rule.get('value')} byte(s)"
    if rtype == "range":
        return f"{rule.get('min')}–{rule.get('max')} bytes"
    if rtype == "max":
        return f"variable (max. {rule.get('value')})"
    if rtype == "choice":
        return " or ".join(str(v) for v in rule.get("values", [])) + " bytes"
    return "variable"


def resolve_tag(tag_hex: str, length_bytes: int) -> dict:
    entries = TAG_DICT.get(tag_hex.upper())
    if not entries:
        return {
            "name": "Unknown Tag",
            "length_ok": True,
            "expected_length": "",
            "ambiguous": False,
            "templates": [],
        }
    ambiguous = len(entries) > 1
    for entry in entries:
        if length_matches(length_bytes, entry["length_rule"]):
            return {
                "name": entry["name"],
                "length_ok": True,
                "expected_length": format_length_rule(entry["length_rule"], entry.get("length_raw", "")),
                "ambiguous": ambiguous,
                "templates": entry.get("templates", []),
            }
    first = entries[0]
    return {
        "name": first["name"],
        "length_ok": False,
        "expected_length": format_length_rule(first["length_rule"], first.get("length_raw", "")),
        "ambiguous": ambiguous,
        "templates": first.get("templates", []),
    }


def tag_name(tag_hex: str) -> str:
    entries = TAG_DICT.get(tag_hex.upper())
    if not entries:
        return "Unknown Tag"
    return entries[0]["name"]


# ─────────────────────────────────────────────
#  TLV CORE LOGIC
# ─────────────────────────────────────────────
def clean_hex(raw: str) -> str:
    return re.sub(r"[^0-9A-Fa-f]", "", raw).upper()


def parse_tlv(hex_str: str, level: int = 0, max_level: int = 15) -> list:
    data = bytes.fromhex(hex_str)
    nodes, _ = _parse_bytes(data, 0, len(data), level, max_level)
    return nodes


def _parse_bytes(data: bytes, start: int, end: int, level: int, max_level: int):
    nodes = []
    pos = start
    while pos < end:
        node_start = pos
        first_byte = data[pos]
        tag_bytes = bytearray([first_byte])
        pos += 1
        if (first_byte & 0x1F) == 0x1F:
            while pos < end:
                b = data[pos]
                tag_bytes.append(b)
                pos += 1
                if (b & 0x80) == 0:
                    break
        tag_hex = tag_bytes.hex().upper()
        is_constructed = (first_byte & 0x20) == 0x20
        if pos >= end:
            break
        len_byte = data[pos]
        pos += 1
        if len_byte & 0x80:
            num_len_bytes = len_byte & 0x7F
            if num_len_bytes == 0 or pos + num_len_bytes > end:
                break
            length = int.from_bytes(data[pos:pos + num_len_bytes], "big")
            pos += num_len_bytes
        else:
            length = len_byte
        value_start = pos
        value_end   = value_start + length
        if value_end > end:
            value_end = end
        value_bytes = data[value_start:value_end]
        pos = value_end

        resolved = resolve_tag(tag_hex, length)
        node = {
            "tag":             tag_hex,
            "name":            resolved["name"],
            "length":          length,
            "value":           value_bytes.hex().upper(),
            "is_constructed":  is_constructed,
            "level":           level,
            "children":        [],
            "raw_start":       node_start,
            "raw_end":         pos,
            "length_ok":       resolved["length_ok"],
            "expected_length": resolved["expected_length"],
            "ambiguous":       resolved["ambiguous"],
            "templates":       resolved["templates"],
        }
        if is_constructed and level < max_level and length > 0:
            children, _ = _parse_bytes(value_bytes, 0, len(value_bytes), level + 1, max_level)
            node["children"] = children
        nodes.append(node)
    return nodes, pos


def encode_length(length: int) -> bytes:
    if length < 0x80:
        return bytes([length])
    len_bytes = []
    tmp = length
    while tmp > 0:
        len_bytes.insert(0, tmp & 0xFF)
        tmp >>= 8
    return bytes([0x80 | len(len_bytes)]) + bytes(len_bytes)


def rebuild_tlv(nodes: list) -> str:
    result = b""
    for node in nodes:
        tag_bytes = bytes.fromhex(node["tag"])
        if node["is_constructed"] and node["children"]:
            value_hex   = rebuild_tlv(node["children"])
            value_bytes = bytes.fromhex(value_hex)
        else:
            value_hex   = clean_hex(node["value"])
            value_bytes = bytes.fromhex(value_hex) if value_hex else b""
        result += tag_bytes + encode_length(len(value_bytes)) + value_bytes
    return result.hex().upper()


def update_constructed_values(nodes: list):
    for node in nodes:
        if node["is_constructed"] and node["children"]:
            update_constructed_values(node["children"])
            child_hex = rebuild_tlv(node["children"])
            node["value"] = child_hex
            node["length"] = len(child_hex) // 2
        resolved = resolve_tag(node["tag"], node["length"])
        node["name"]            = resolved["name"]
        node["length_ok"]       = resolved["length_ok"]
        node["expected_length"] = resolved["expected_length"]
        node["ambiguous"]       = resolved["ambiguous"]
        node["templates"]       = resolved["templates"]


def collect_length_warnings(nodes: list, warnings: list = None) -> list:
    if warnings is None:
        warnings = []
    for node in nodes:
        if not node.get("length_ok", True):
            warnings.append(
                f"{node['tag']} ({node['name']}) : longueur {node['length']} octet(s) "
                f"≠ attendu {node.get('expected_length', '?')}"
            )
        if node["children"]:
            collect_length_warnings(node["children"], warnings)
    return warnings


def count_nodes(nodes: list) -> int:
    total = 0
    for n in nodes:
        total += 1 + count_nodes(n["children"])
    return total


def calc_max_depth(nodes: list, current: int = 0) -> int:
    if not nodes:
        return current
    return max(calc_max_depth(n["children"], current + 1) for n in nodes)


# ─────────────────────────────────────────────
#  TREE NODE HELPERS  (delete / find parent)
# ─────────────────────────────────────────────

def _find_and_remove_node(nodes: list, target_id: int) -> bool:
    """
    Recursively search `nodes` for the node with id(node)==target_id.
    Remove it in-place and return True if found.
    """
    for i, node in enumerate(nodes):
        if id(node) == target_id:
            nodes.pop(i)
            return True
        if node["children"] and _find_and_remove_node(node["children"], target_id):
            return True
    return False


def _find_node_parent(nodes: list, target_id: int, parent: list = None):
    """
    Returns the parent list that contains the node with id==target_id.
    Returns None if target is a root node (parent == top-level nodes list).
    We return (parent_list, index).
    """
    for i, node in enumerate(nodes):
        if id(node) == target_id:
            return nodes, i
        if node["children"]:
            result = _find_node_parent(node["children"], target_id, node["children"])
            if result is not None:
                return result
    return None


def _find_node_by_id(nodes: list, target_id: int):
    """Return the node dict whose id() == target_id."""
    for node in nodes:
        if id(node) == target_id:
            return node
        if node["children"]:
            found = _find_node_by_id(node["children"], target_id)
            if found is not None:
                return found
    return None


def _collect_all_constructed(nodes: list) -> list:
    """Return list of (display_path, node) for all constructed nodes (containers)."""
    result = []
    def _walk(nodelist, prefix):
        for n in nodelist:
            if n["is_constructed"]:
                label = f"{prefix}{n['tag']}  ({n['name']})"
                result.append((label, n))
                _walk(n["children"], prefix + "  › ")
    _walk(nodes, "")
    return result


def _collect_all_nodes_flat(nodes: list) -> list[dict]:
    """Return every node in DFS order as a flat list."""
    result = []
    def _walk(nodelist):
        for n in nodelist:
            result.append(n)
            _walk(n["children"])
    _walk(nodes)
    return result


def _node_matches_query(node: dict, query: str) -> bool:
    """
    Return True if `query` (already stripped/uppercased) matches this node by:
      - tag hex  (e.g. "9F26")
      - tag name (e.g. "transaction")
      - value hex (e.g. "0A2B")
    """
    q = query.upper()
    if q in node["tag"].upper():
        return True
    if q in node["name"].upper():
        return True
    if q in node["value"].upper():
        return True
    return False


# ─────────────────────────────────────────────
#  TEXT TREE RENDERER  (with bit decode)
# ─────────────────────────────────────────────
def render_text_tree(nodes: list, indent: str = "") -> str:
    lines = []
    for i, node in enumerate(nodes):
        tag     = node["tag"]
        name    = node["name"]
        ln      = node["length"]
        is_last = (i == len(nodes) - 1)

        connector = f"{indent}+--+ " if indent else ""
        keyword   = f'value="{node["value"]}"'
        flag      = "" if node.get("length_ok", True) else "  [!] longueur invalide"
        lines.append(f"{connector}{tag} ({name}, len=0x{ln:02X}) {keyword}{flag}")

        if not node["is_constructed"]:
            bit_text = render_bit_decode_text(tag, node["value"])
            if bit_text:
                for bl in bit_text.splitlines():
                    lines.append(f"{indent}{bl}")

        if indent and not is_last:
            lines.append(f"{indent}|")

        if node["is_constructed"] and node["children"]:
            child_indent = indent + "  "
            lines.append(render_text_tree(node["children"], indent=child_indent))

    return "\n".join(lines)


# ─────────────────────────────────────────────
#  ADD TAG DIALOG
# ─────────────────────────────────────────────
class AddTagDialog(QDialog):
    def __init__(self, parsed_tree: list, parent=None):
        super().__init__(parent)
        self.parsed_tree = parsed_tree
        self.setWindowTitle("Add Tag")
        self.setMinimumWidth(620)
        self.setStyleSheet(GLOBAL_STYLE)

        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        # ── Tag hex ──────────────────────────────
        tag_row = QHBoxLayout()
        tag_lbl = QLabel("Tag (hex) :")
        tag_lbl.setFixedWidth(120)
        tag_lbl.setStyleSheet(f"color:{TEXT_SECONDARY};")
        self.tag_input = QLineEdit()
        self.tag_input.setPlaceholderText("e.g.  9F26  or  DF1B")
        self.tag_name_lbl = QLabel("")
        self.tag_name_lbl.setStyleSheet(f"color:{TAG_COLOR}; font-size:11px; min-width:180px;")
        self.tag_input.textChanged.connect(self._on_tag_changed)
        tag_row.addWidget(tag_lbl)
        tag_row.addWidget(self.tag_input)
        tag_row.addWidget(self.tag_name_lbl)
        layout.addLayout(tag_row)

        # ── Value hex (primitive) ─────────────────
        val_row = QHBoxLayout()
        val_lbl = QLabel("Value (hex) :")
        val_lbl.setFixedWidth(120)
        val_lbl.setStyleSheet(f"color:{TEXT_SECONDARY};")
        self.val_input = QLineEdit()
        self.val_input.setPlaceholderText("e.g.  0A2B3C …  (leave empty for a container)")
        self.val_input.textChanged.connect(self._on_val_changed)
        val_row.addWidget(val_lbl)
        val_row.addWidget(self.val_input)
        layout.addLayout(val_row)

        self.len_lbl = QLabel("Length : 0 bytes")
        self.len_lbl.setStyleSheet(f"color:{TEXT_SECONDARY}; font-size:11px; margin-left:124px;")
        layout.addWidget(self.len_lbl)

        # ── Constructed checkbox ──────────────────
        constr_row = QHBoxLayout()
        constr_lbl = QLabel("Constructed :")
        constr_lbl.setFixedWidth(120)
        constr_lbl.setStyleSheet(f"color:{TEXT_SECONDARY};")
        self.constr_check = QCheckBox("Yes  (container / template tag)")
        self.constr_check.setStyleSheet(f"color:{TEXT_PRIMARY};")
        self.constr_check.toggled.connect(self._on_constr_changed)
        constr_row.addWidget(constr_lbl)
        constr_row.addWidget(self.constr_check)
        layout.addLayout(constr_row)

        # ── Insert position ───────────────────────
        pos_row = QHBoxLayout()
        pos_lbl = QLabel("Insert into :")
        pos_lbl.setFixedWidth(120)
        pos_lbl.setStyleSheet(f"color:{TEXT_SECONDARY};")
        self.parent_combo = QComboBox()
        self.parent_combo.setMinimumWidth(340)
        pos_row.addWidget(pos_lbl)
        pos_row.addWidget(self.parent_combo)
        layout.addLayout(pos_row)

        # Populate combo
        self.parent_combo.addItem("▸  Root  (top level)", None)
        for label, node in _collect_all_constructed(parsed_tree):
            self.parent_combo.addItem(label, id(node))

        # ── Buttons ───────────────────────────────
        btns = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        btns.button(QDialogButtonBox.StandardButton.Ok).setText("Add Tag")
        btns.button(QDialogButtonBox.StandardButton.Ok).setObjectName("add_tag")
        btns.accepted.connect(self._validate_and_accept)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)

    def _on_tag_changed(self, text):
        tag = clean_hex(text)
        if tag:
            name = tag_name(tag)
            self.tag_name_lbl.setText(f"  →  {name}")
        else:
            self.tag_name_lbl.setText("")

    def _on_val_changed(self, text):
        n = len(clean_hex(text)) // 2
        self.len_lbl.setText(f"Length : {n} bytes")

    def _on_constr_changed(self, checked):
        self.val_input.setEnabled(not checked)
        if checked:
            self.val_input.clear()
            self.val_input.setPlaceholderText("(children will be added after)")
        else:
            self.val_input.setPlaceholderText("e.g.  0A2B3C …")

    def _validate_and_accept(self):
        tag = clean_hex(self.tag_input.text())
        if not tag:
            QMessageBox.warning(self, "Missing Tag", "Please enter a tag hex value.")
            return
        if len(tag) % 2 != 0:
            QMessageBox.warning(self, "Invalid Tag", "Tag must have an even number of hex digits.")
            return
        val = clean_hex(self.val_input.text()) if not self.constr_check.isChecked() else ""
        if val and len(val) % 2 != 0:
            QMessageBox.warning(self, "Invalid Value", "Value must have an even number of hex digits.")
            return
        self.accept()

    def get_new_node(self) -> dict:
        tag = clean_hex(self.tag_input.text())
        is_constructed = self.constr_check.isChecked()
        val = "" if is_constructed else clean_hex(self.val_input.text())
        length = len(val) // 2

        # Determine the constructed bit from tag byte
        first_tag_byte = int(tag[:2], 16)
        if is_constructed:
            first_tag_byte = first_tag_byte | 0x20
        else:
            first_tag_byte = first_tag_byte & ~0x20

        # Rebuild tag hex with correct constructed bit
        tag_corrected = f"{first_tag_byte:02X}" + tag[2:]

        resolved = resolve_tag(tag_corrected, length)
        return {
            "tag":             tag_corrected,
            "name":            resolved["name"],
            "length":          length,
            "value":           val,
            "is_constructed":  is_constructed,
            "level":           0,
            "children":        [],
            "raw_start":       0,
            "raw_end":         0,
            "length_ok":       resolved["length_ok"],
            "expected_length": resolved["expected_length"],
            "ambiguous":       resolved["ambiguous"],
            "templates":       resolved["templates"],
        }

    def get_parent_node_id(self):
        """Returns id of parent node, or None for root."""
        return self.parent_combo.currentData()


# ─────────────────────────────────────────────
#  CUSTOM WIDGETS
# ─────────────────────────────────────────────
class StatCard(QFrame):
    def __init__(self, label: str, value: str = "—", color: str = ACCENT):
        super().__init__()
        self.setFixedHeight(70)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {PANEL_BG};
                border: 1px solid {BORDER};
                border-radius: 8px;
            }}
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(2)
        self.val_label = QLabel(value)
        self.val_label.setStyleSheet(
            f"font-size: 22px; font-weight: 700; color: {color};"
            f" border: none; background: transparent;"
        )
        self.lbl_label = QLabel(label.upper())
        self.lbl_label.setStyleSheet(
            f"font-size: 10px; color: {TEXT_SECONDARY}; letter-spacing: 0.8px;"
            f" font-weight: 600; border: none; background: transparent;"
        )
        layout.addWidget(self.val_label)
        layout.addWidget(self.lbl_label)

    def set_value(self, v: str):
        self.val_label.setText(v)


class SectionHeader(QWidget):
    def __init__(self, title: str, subtitle: str = ""):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 8)
        layout.setSpacing(2)
        t = QLabel(title)
        t.setStyleSheet(f"font-size: 15px; font-weight: 700; color: {TEXT_PRIMARY};")
        layout.addWidget(t)
        if subtitle:
            s = QLabel(subtitle)
            s.setStyleSheet(f"font-size: 11px; color: {TEXT_SECONDARY};")
            layout.addWidget(s)


class TLVTreeWidget(QTreeWidget):
    node_selected = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.setColumnCount(4)
        self.setHeaderLabels(["Tag", "Name", "Length", "Value"])
        self.setAlternatingRowColors(True)
        self.setRootIsDecorated(True)
        self.setAnimated(True)
        self.setExpandsOnDoubleClick(True)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        h = self.header()
        h.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        h.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        h.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        h.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.itemSelectionChanged.connect(self._on_selection)
        self._node_map: dict = {}

    def _on_selection(self):
        items = self.selectedItems()
        if items:
            node = self._node_map.get(id(items[0]))
            if node:
                self.node_selected.emit(node)

    def load_tree(self, nodes: list):
        self.clear()
        self._node_map.clear()
        self._add_nodes(nodes, self.invisibleRootItem())
        self.expandAll()

    def _add_nodes(self, nodes: list, parent):
        bold_mono = QFont("Cascadia Code, Fira Code, Consolas", 11)
        bold_mono.setBold(True)
        for node in nodes:
            item = QTreeWidgetItem(parent)
            length_ok = node.get("length_ok", True)

            item.setText(0, node["tag"])
            item.setForeground(0, QBrush(QColor(TAG_COLOR)))
            item.setFont(0, bold_mono)

            name_display = node["name"]
            if not length_ok:
                name_display += "  ⚠"
            item.setText(1, name_display)
            item.setForeground(1, QBrush(QColor(LEN_ERROR_C if not length_ok else TEXT_SECONDARY)))

            item.setText(2, f"0x{node['length']:02X}  ({node['length']})")
            item.setForeground(2, QBrush(QColor(LEN_ERROR_C if not length_ok else LEN_COLOR)))

            display = node["value"][:80] + ("…" if len(node["value"]) > 80 else "")
            item.setText(3, display)
            item.setForeground(3, QBrush(QColor(VAL_COLOR)))

            self._node_map[id(item)] = node
            if node["children"]:
                self._add_nodes(node["children"], item)

    def get_selected_node(self) -> dict | None:
        items = self.selectedItems()
        if items:
            return self._node_map.get(id(items[0]))
        return None


# ─────────────────────────────────────────────
#  EDIT NODE DIALOG
# ─────────────────────────────────────────────
class EditNodeDialog(QDialog):
    def __init__(self, node: dict, parent=None):
        super().__init__(parent)
        self.node = node
        self.setWindowTitle(f"Edit  ·  Tag {node['tag']}")
        self.setMinimumWidth(600)
        self.setStyleSheet(GLOBAL_STYLE)
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        if not node["is_constructed"]:
            layout.addWidget(QLabel("Hex Value  (modifiable) :"))
            self.value_edit = QTextEdit()
            self.value_edit.setPlainText(node["value"])
            self.value_edit.setMinimumHeight(100)
            self.value_edit.setStyleSheet(
                f"font-family:'Cascadia Code','Fira Code',monospace;"
                f"font-size:13px; background:{PANEL_BG};"
                f"border:1px solid {BORDER}; border-radius:6px; color:{VAL_COLOR};"
            )
            layout.addWidget(self.value_edit)
            self.len_indicator = QLabel(f"Longueur après édition : {node['length']} octets")
            self.len_indicator.setStyleSheet(f"color:{TEXT_SECONDARY}; font-size:11px;")
            layout.addWidget(self.len_indicator)
            self.value_edit.textChanged.connect(self._update_length)
        else:
            note = QLabel("ne peut pas être édité directement.")
            note.setStyleSheet(
                f"color:{TEXT_SECONDARY}; font-size:12px; padding:12px;"
                f"background:#21262D; border-radius:6px;"
            )
            layout.addWidget(note)

        btns = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)

    def _update_length(self):
        n = len(clean_hex(self.value_edit.toPlainText())) // 2
        self.len_indicator.setText(f"Longueur après édition : {n} octets")

    def get_new_value(self) -> str:
        if hasattr(self, "value_edit"):
            return clean_hex(self.value_edit.toPlainText())
        return self.node["value"]


# ─────────────────────────────────────────────
#  MAIN WINDOW
# ─────────────────────────────────────────────
class TLVMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.parsed_tree = None
        self._search_matches: list = []
        self._search_cursor: int   = -1
        self.setWindowTitle("TLV / EMV Parser")
        self.setMinimumSize(1200, 750)
        self.resize(1500, 900)
        self.setStyleSheet(GLOBAL_STYLE)
        self._build_ui()

    def _build_ui(self):
        self._build_toolbar()

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(16, 12, 16, 12)
        root.setSpacing(12)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(2)
        root.addWidget(splitter)

        # ── LEFT PANEL ──────────────────────────
        left = QWidget()
        left.setMaximumWidth(400)
        left.setMinimumWidth(280)
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(0, 0, 8, 0)
        left_layout.setSpacing(12)

        input_grp = QGroupBox("Input — TLV Hex String")
        ig = QVBoxLayout(input_grp)
        ig.setSpacing(8)
        self.hex_input = QTextEdit()
        self.hex_input.setPlaceholderText(
            "E081A29F1A020280DF1B020978DF1C01029F3501229F330360F8C8…"
        )
        self.hex_input.setMinimumHeight(180)
        self.hex_input.setStyleSheet(
            self.hex_input.styleSheet() + f" color: {ACCENT};"
        )
        ig.addWidget(self.hex_input)

        btn_row = QHBoxLayout()
        self.parse_btn = QPushButton("▶  Parse")
        self.parse_btn.setObjectName("primary")
        self.parse_btn.setFixedHeight(36)
        self.parse_btn.clicked.connect(self.do_parse)
        self.clear_btn = QPushButton("⌫  Clear")
        self.clear_btn.setObjectName("danger")
        self.clear_btn.setFixedHeight(36)
        self.clear_btn.clicked.connect(self.do_clear)
        btn_row.addWidget(self.parse_btn)
        btn_row.addWidget(self.clear_btn)
        ig.addLayout(btn_row)
        left_layout.addWidget(input_grp)

        left_layout.addStretch()
        splitter.addWidget(left)

        # ── RIGHT PANEL ─────────────────────────
        right = QWidget()
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(8, 0, 0, 0)
        right_layout.setSpacing(12)

        hdr_row = QHBoxLayout()
        hdr_row.addWidget(SectionHeader("Parse Tree", "Double-clic → éditer · Sélection → détails"))
        hdr_row.addStretch()

        # ── New: Delete & Add tag buttons ────────
        self.delete_tag_btn = QPushButton("🗑  Delete Tag")
        self.delete_tag_btn.setObjectName("delete_tag")
        self.delete_tag_btn.setFixedHeight(28)
        self.delete_tag_btn.setToolTip("Delete the selected tag (and its children) from the tree")
        self.delete_tag_btn.clicked.connect(self.do_delete_tag)

        self.add_tag_btn = QPushButton("＋  Add Tag")
        self.add_tag_btn.setObjectName("add_tag")
        self.add_tag_btn.setFixedHeight(28)
        self.add_tag_btn.setToolTip("Add a new tag anywhere in the tree")
        self.add_tag_btn.clicked.connect(self.do_add_tag)

        for label, slot in [
            ("⊞ Expand All",    lambda: self.tree.expandAll()),
            ("⊟ Collapse All",  lambda: self.tree.collapseAll()),
            ("⧉ Copy Rebuilt",  self.copy_rebuilt),
        ]:
            b = QPushButton(label)
            b.setFixedHeight(28)
            b.clicked.connect(slot)
            hdr_row.addWidget(b)

        hdr_row.addWidget(self.delete_tag_btn)
        hdr_row.addWidget(self.add_tag_btn)
        right_layout.addLayout(hdr_row)

        self.tabs = QTabWidget()

        # ── Search bar (live search across tag/name/value) ────────
        search_frame = QWidget()
        search_frame.setStyleSheet(
            f"background-color:{PANEL_BG}; border:1px solid {BORDER};"
            f" border-radius:6px; padding:2px;"
        )
        search_layout = QHBoxLayout(search_frame)
        search_layout.setContentsMargins(8, 4, 8, 4)
        search_layout.setSpacing(6)

        search_icon = QLabel("🔍")
        search_icon.setStyleSheet("border:none; background:transparent; font-size:13px;")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Search tag hex, name, or value…  (Enter = next,  Shift+Enter = prev)"
        )
        self.search_input.setStyleSheet(
            f"background:transparent; border:none; color:{TEXT_PRIMARY};"
            f" font-size:12px; font-family:'Cascadia Code','Fira Code',monospace;"
        )
        self.search_input.textChanged.connect(self._on_search_changed)
        self.search_input.returnPressed.connect(self._search_next)
        self.search_input.installEventFilter(self)

        self.search_count_lbl = QLabel("")
        self.search_count_lbl.setStyleSheet(
            f"color:{TEXT_SECONDARY}; font-size:11px; min-width:80px;"
            f" border:none; background:transparent;"
        )

        search_prev_btn = QPushButton("↑")
        search_prev_btn.setFixedSize(26, 26)
        search_prev_btn.setStyleSheet(
            f"QPushButton{{background:{PANEL_BG};border:1px solid {BORDER};"
            f"border-radius:4px;color:{TEXT_PRIMARY};font-weight:700;padding:0;}}"
            f"QPushButton:hover{{border-color:{ACCENT};color:{ACCENT};}}"
        )
        search_prev_btn.setToolTip("Previous match  (Shift+Enter)")
        search_prev_btn.clicked.connect(self._search_prev)

        search_next_btn = QPushButton("↓")
        search_next_btn.setFixedSize(26, 26)
        search_next_btn.setStyleSheet(
            f"QPushButton{{background:{PANEL_BG};border:1px solid {BORDER};"
            f"border-radius:4px;color:{TEXT_PRIMARY};font-weight:700;padding:0;}}"
            f"QPushButton:hover{{border-color:{ACCENT};color:{ACCENT};}}"
        )
        search_next_btn.setToolTip("Next match  (Enter)")
        search_next_btn.clicked.connect(self._search_next)

        search_clear_btn = QPushButton("✕")
        search_clear_btn.setFixedSize(26, 26)
        search_clear_btn.setStyleSheet(
            f"QPushButton{{background:{PANEL_BG};border:1px solid {BORDER};"
            f"border-radius:4px;color:{TEXT_SECONDARY};font-weight:700;padding:0;}}"
            f"QPushButton:hover{{border-color:{DELETE_RED};color:{DELETE_RED};}}"
        )
        search_clear_btn.setToolTip("Clear search")
        search_clear_btn.clicked.connect(self._search_clear)

        search_layout.addWidget(search_icon)
        search_layout.addWidget(self.search_input, stretch=1)
        search_layout.addWidget(self.search_count_lbl)
        search_layout.addWidget(search_prev_btn)
        search_layout.addWidget(search_next_btn)
        search_layout.addWidget(search_clear_btn)

        right_layout.addWidget(search_frame)

        # Tree tab
        tree_tab = QWidget()
        tree_tab_layout = QVBoxLayout(tree_tab)
        tree_tab_layout.setContentsMargins(0, 8, 0, 0)
        self.tree = TLVTreeWidget()
        self.tree.node_selected.connect(self._show_node_detail)
        self.tree.itemDoubleClicked.connect(self._edit_node_from_item)
        tree_tab_layout.addWidget(self.tree)
        self.tabs.addTab(tree_tab, "Tree View")

        # Text tab
        text_tab = QWidget()
        text_tab_layout = QVBoxLayout(text_tab)
        text_tab_layout.setContentsMargins(0, 8, 0, 0)
        self.text_tree_output = QPlainTextEdit()
        self.text_tree_output.setReadOnly(True)
        self.text_tree_output.setStyleSheet(
            f"font-family:'Cascadia Code','Fira Code','Consolas',monospace;"
            f"font-size:12px; color:{TEXT_PRIMARY}; line-height:1.5;"
        )
        copy_text_btn = QPushButton("⧉  Copier le texte")
        copy_text_btn.setFixedHeight(28)
        copy_text_btn.clicked.connect(
            lambda: QApplication.clipboard().setText(self.text_tree_output.toPlainText())
        )
        text_tab_layout.addWidget(self.text_tree_output)
        text_btn_row = QHBoxLayout()
        text_btn_row.addStretch()
        text_btn_row.addWidget(copy_text_btn)
        text_tab_layout.addLayout(text_btn_row)
        self.tabs.addTab(text_tab, "📄  Text View")

        right_layout.addWidget(self.tabs, stretch=3)

        bot = QSplitter(Qt.Orientation.Horizontal)

        # Node Detail panel
        detail_frame = QGroupBox("Node Detail  +  Bit Decode")
        dl = QVBoxLayout(detail_frame)
        self.detail_text = QTextEdit()
        self.detail_text.setReadOnly(True)
        self.detail_text.setMinimumHeight(160)
        dl.addWidget(self.detail_text)
        bot.addWidget(detail_frame)

        # Rebuilt HEX output
        rebuilt_frame = QGroupBox("Rebuilt HEX Output")
        rl = QVBoxLayout(rebuilt_frame)
        rb_btn_row = QHBoxLayout()
        self.rebuild_btn = QPushButton("🔄  Rebuild TLV")
        self.rebuild_btn.setObjectName("success")
        self.rebuild_btn.clicked.connect(self.do_rebuild)
        rb_btn_row.addWidget(self.rebuild_btn)
        rb_btn_row.addStretch()
        rl.addLayout(rb_btn_row)
        self.rebuilt_output = QTextEdit()
        self.rebuilt_output.setReadOnly(True)
        self.rebuilt_output.setStyleSheet(
            self.rebuilt_output.styleSheet() + f" color:{SUCCESS};"
        )
        rl.addWidget(self.rebuilt_output)
        bot.addWidget(rebuilt_frame)

        right_layout.addWidget(bot, stretch=1)
        splitter.addWidget(right)
        splitter.setSizes([340, 1160])

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def _build_toolbar(self):
        tb = self.addToolBar("Main")
        tb.setMovable(False)
        tb.setIconSize(QSize(16, 16))
        brand = QLabel("  🔍  TLV / EMV Parser  —  with Bit Decode")
        brand.setStyleSheet(
            f"font-size:14px; font-weight:700; color:{TEXT_PRIMARY}; padding:0 12px;"
        )
        tb.addWidget(brand)
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        tb.addWidget(spacer)

    # ── Actions ──────────────────────────────
    def _status(self, msg: str, color: str = TEXT_SECONDARY):
        self.status_bar.showMessage(msg)

    def do_parse(self):
        raw     = self.hex_input.toPlainText()
        cleaned = clean_hex(raw)
        if not cleaned:
            self._show_error("Aucune donnée hexadécimale valide détectée.")
            return
        if len(cleaned) % 2 != 0:
            self._show_error("La chaîne hex doit contenir un nombre pair de caractères.")
            return
        try:
            self.parsed_tree = parse_tlv(cleaned)
            self._refresh_tree_views()

            nb = len(cleaned) // 2
            nt = count_nodes(self.parsed_tree)
            nd = calc_max_depth(self.parsed_tree)

            self.rebuilt_output.clear()
            self.detail_text.clear()

            warnings = collect_length_warnings(self.parsed_tree)
            if warnings:
                preview = " · ".join(warnings[:3])
                more = f"  (+{len(warnings) - 3} autres)" if len(warnings) > 3 else ""
                self._status(
                    f"⚠  Parsed {nb} bytes · {nt} tags · profondeur {nd}  —  "
                    f"longueur(s) invalide(s) : {preview}{more}",
                    LEN_ERROR_C,
                )
            else:
                self._status(f"✓  Parsed {nb} bytes · {nt} tags · profondeur {nd}", SUCCESS)
        except Exception as e:
            self._show_error(f"Erreur de parsing : {e}")

    def do_clear(self):
        self.hex_input.clear()
        self.tree.clear()
        self.text_tree_output.clear()
        self.detail_text.clear()
        self.rebuilt_output.clear()
        self.parsed_tree = None
        self._status("Effacé")

    def do_rebuild(self):
        if not self.parsed_tree:
            self._show_error("Rien à reconstruire. Parsez d'abord.")
            return
        try:
            rebuilt = rebuild_tlv(self.parsed_tree)
            self.rebuilt_output.setPlainText(rebuilt)
            self._status(f"TLV reconstruit — {len(rebuilt)//2} bytes", SUCCESS)
        except Exception as e:
            self._show_error(f"Erreur de reconstruction : {e}")

    def copy_rebuilt(self):
        text = self.rebuilt_output.toPlainText()
        if text:
            QApplication.clipboard().setText(text)
            self._status("✓  Copié dans le presse-papiers", SUCCESS)
        else:
            self._status("Rien à copier — reconstruisez d'abord.")

    # ── DELETE TAG ────────────────────────────
    def do_delete_tag(self):
        if not self.parsed_tree:
            self._show_error("Aucun arbre parsé.")
            return

        node = self.tree.get_selected_node()
        if node is None:
            self._show_error("Sélectionnez d'abord un tag dans l'arbre.")
            return

        tag_display = f"{node['tag']}  ({node['name']})"
        child_count = count_nodes(node["children"])
        msg = f"Supprimer le tag  {tag_display} ?"
        if child_count:
            msg += f"\n\nCe tag contient {child_count} enfant(s) qui seront également supprimés."
        msg += "\n\nLe TLV reconstruit ne contiendra plus ce tag."

        reply = QMessageBox.question(
            self, "Confirmer la suppression", msg,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Cancel,
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        node_id = id(node)
        removed = _find_and_remove_node(self.parsed_tree, node_id)
        if not removed:
            self._show_error("Impossible de localiser le tag dans l'arbre interne.")
            return

        # Propagate length changes up through any parent containers
        update_constructed_values(self.parsed_tree)
        self._refresh_tree_views()
        self.detail_text.clear()
        self.rebuilt_output.clear()

        nt = count_nodes(self.parsed_tree)
        self._status(
            f"✓  Tag {node['tag']} supprimé — {nt} tag(s) restant(s) · "
            f"Cliquez Rebuild pour mettre à jour la sortie HEX.",
            SUCCESS,
        )

    # ── ADD TAG ───────────────────────────────
    def do_add_tag(self):
        if self.parsed_tree is None:
            # Allow adding to an empty tree
            self.parsed_tree = []

        dlg = AddTagDialog(self.parsed_tree, self)
        if dlg.exec() != QDialog.DialogCode.Accepted:
            return

        new_node    = dlg.get_new_node()
        parent_id   = dlg.get_parent_node_id()

        if parent_id is None:
            # Insert at root level
            self.parsed_tree.append(new_node)
        else:
            # Insert into the selected constructed node
            parent_node = _find_node_by_id(self.parsed_tree, parent_id)
            if parent_node is None:
                self._show_error("Parent node not found — inserting at root.")
                self.parsed_tree.append(new_node)
            else:
                parent_node["children"].append(new_node)

        # Update all constructed lengths
        update_constructed_values(self.parsed_tree)
        self._refresh_tree_views()
        self.rebuilt_output.clear()

        nt = count_nodes(self.parsed_tree)
        self._status(
            f"✓  Tag {new_node['tag']} ({new_node['name']}) ajouté — "
            f"{nt} tag(s) total · Cliquez Rebuild pour la sortie HEX.",
            SUCCESS,
        )

    # ── SHARED TREE REFRESH ───────────────────
    def _refresh_tree_views(self):
        """Reload both the QTreeWidget and the plain-text view."""
        self.tree.load_tree(self.parsed_tree)
        self.text_tree_output.setPlainText(render_text_tree(self.parsed_tree))
        # Re-apply any active search so highlights stay correct after edits
        current_query = self.search_input.text().strip()
        if current_query:
            self._on_search_changed(current_query)
        else:
            self._search_matches = []
            self._search_cursor  = -1
            self.search_count_lbl.setText("")

    def _show_node_detail(self, node: dict):
        """Show tag info + bit/position decode in the detail panel."""
        length_ok = node.get("length_ok", True)
        len_color = LEN_ERROR_C if not length_ok else LEN_COLOR

        lines = [
            f"<span style='color:{TAG_COLOR}; font-weight:700; font-size:15px'>"
            f"{node['tag']}</span>",

            f"<span style='color:{TEXT_SECONDARY}'>Name :</span>  "
            f"<span style='color:{TEXT_PRIMARY}'>{node['name']}</span>"
            + (f"  <span style='color:{TEXT_SECONDARY}; font-size:11px;'>"
               f"(multiple interpretations)</span>" if node.get("ambiguous") else ""),

            f"<span style='color:{TEXT_SECONDARY}'>Length :</span> "
            f"<span style='color:{len_color}'>{node['length']} bytes  "
            f"(0x{node['length']:02X})</span>"
            + (f"  <span style='color:{LEN_ERROR_C}'>⚠ expected : "
               f"{node.get('expected_length', '?')}</span>" if not length_ok else ""),
        ]

        if node.get("templates"):
            lines.append(
                f"<span style='color:{TEXT_SECONDARY}'>Template :</span> "
                f"<span style='color:{TEXT_PRIMARY}'>"
                f"{', '.join(node['templates'])}</span>"
            )

        val   = node["value"]
        label = "Container :" if node["is_constructed"] else "Value :"
        lines.append(
            f"<span style='color:{TEXT_SECONDARY}'>{label}</span><br>"
            f"<span style='color:{VAL_COLOR}; font-family:monospace; "
            f"font-size:11px;'>{val}</span>"
        )

        if not node["is_constructed"]:
            bit_html = render_bit_decode_html(node["tag"], node["value"])
            if bit_html:
                lines.append(
                    f"<hr style='border:none; border-top:1px solid {BORDER}; "
                    f"margin:8px 0;'>"
                )
                lines.append(bit_html)

        self.detail_text.setHtml(
            f"<div style='font-family:\"Cascadia Code\",monospace; font-size:12px;'>"
            + "<br>".join(lines)
            + "</div>"
        )

    def _edit_node_from_item(self, item, _column):
        node = self.tree._node_map.get(id(item))
        if not node:
            return
        dlg = EditNodeDialog(node, self)
        if dlg.exec() == QDialog.DialogCode.Accepted and not node["is_constructed"]:
            new_value  = dlg.get_new_value()
            new_length = len(new_value) // 2

            entries = TAG_DICT.get(node["tag"].upper())
            if entries:
                length_valid = any(
                    length_matches(new_length, entry["length_rule"])
                    for entry in entries
                )
                if not length_valid:
                    rules_desc = " / ".join(
                        format_length_rule(e["length_rule"], e.get("length_raw", ""))
                        for e in entries
                    )
                    QMessageBox.warning(
                        self,
                        "Longueur invalide — Modification refusée",
                        f"Le tag  {node['tag']}  ({node['name']})\n"
                        f"n'accepte pas une valeur de  {new_length}  octet(s).\n\n"
                        f"Longueur(s) attendue(s) :  {rules_desc}\n\n"
                        f"Corrigez la valeur et réessayez."
                    )
                    return

            node["value"]  = new_value
            node["length"] = new_length

            update_constructed_values(self.parsed_tree)
            self._refresh_tree_views()

            warnings = collect_length_warnings(self.parsed_tree)
            if warnings:
                preview = " · ".join(warnings[:3])
                more = f"  (+{len(warnings) - 3} autres)" if len(warnings) > 3 else ""
                self._status(
                    f"⚠  Tag {node['tag']} mis à jour — longueur(s) invalide(s) : {preview}{more}",
                    LEN_ERROR_C,
                )
            else:
                self._status(f"✓  Tag {node['tag']} mis à jour", SUCCESS)

    # ── SEARCH ────────────────────────────────
    def eventFilter(self, obj, event):
        from PyQt6.QtCore import QEvent
        if obj is self.search_input and event.type() == QEvent.Type.KeyPress:
            if (event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter)):
                if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                    self._search_prev()
                    return True
        return super().eventFilter(obj, event)

    def _on_search_changed(self, text: str):
        """Live search: highlight all matches, jump to first."""
        query = text.strip()
        self._search_matches = []
        self._search_cursor  = -1
        self.search_count_lbl.setText("")
        self._clear_search_highlights()

        if not query or not self.parsed_tree:
            return

        self._search_matches = self._collect_matching_items(query)

        if not self._search_matches:
            self.search_count_lbl.setText("0 results")
            self.search_count_lbl.setStyleSheet(
                f"color:{DELETE_RED}; font-size:11px; min-width:80px;"
                f" border:none; background:transparent;"
            )
            return

        # Highlight every match with a distinct background
        for item in self._search_matches:
            for col in range(4):
                item.setBackground(col, QBrush(QColor(SEARCH_HIGHLIGHT)))
            item.setForeground(1, QBrush(QColor(SEARCH_MATCH_FORE)))

        n = len(self._search_matches)
        self._search_cursor = 0
        self._jump_to_match(0)
        self.search_count_lbl.setText(f"1 / {n}")
        self.search_count_lbl.setStyleSheet(
            f"color:{ADD_GREEN}; font-size:11px; min-width:80px;"
            f" border:none; background:transparent;"
        )

    def _collect_matching_items(self, query: str) -> list:
        results = []
        self._walk_items_for_search(self.tree.invisibleRootItem(), query, results)
        return results

    def _walk_items_for_search(self, parent_item, query: str, results: list):
        for i in range(parent_item.childCount()):
            item = parent_item.child(i)
            node = self.tree._node_map.get(id(item))
            if node and _node_matches_query(node, query):
                results.append(item)
            self._walk_items_for_search(item, query, results)

    def _clear_search_highlights(self):
        transparent = QBrush(Qt.BrushStyle.NoBrush)
        self._walk_items_clear(self.tree.invisibleRootItem(), transparent)

    def _walk_items_clear(self, parent_item, transparent):
        for i in range(parent_item.childCount()):
            item = parent_item.child(i)
            for col in range(4):
                item.setBackground(col, transparent)
            node = self.tree._node_map.get(id(item))
            if node:
                length_ok = node.get("length_ok", True)
                item.setForeground(1, QBrush(QColor(
                    LEN_ERROR_C if not length_ok else TEXT_SECONDARY
                )))
            self._walk_items_clear(item, transparent)

    def _jump_to_match(self, index: int):
        """Select + scroll the tree to the match at `index`, update detail panel."""
        if not self._search_matches:
            return
        item = self._search_matches[index]
        # Expand all ancestors so the item is visible
        parent = item.parent()
        while parent:
            parent.setExpanded(True)
            parent = parent.parent()
        self.tree.setCurrentItem(item)
        self.tree.scrollToItem(item, QAbstractItemView.ScrollHint.PositionAtCenter)
        # Show node detail immediately
        node = self.tree._node_map.get(id(item))
        if node:
            self._show_node_detail(node)
        # Switch to Tree View tab so the user sees it
        self.tabs.setCurrentIndex(0)

    def _search_next(self):
        if not self._search_matches:
            return
        self._search_cursor = (self._search_cursor + 1) % len(self._search_matches)
        self._jump_to_match(self._search_cursor)
        self.search_count_lbl.setText(
            f"{self._search_cursor + 1} / {len(self._search_matches)}"
        )

    def _search_prev(self):
        if not self._search_matches:
            return
        self._search_cursor = (self._search_cursor - 1) % len(self._search_matches)
        self._jump_to_match(self._search_cursor)
        self.search_count_lbl.setText(
            f"{self._search_cursor + 1} / {len(self._search_matches)}"
        )

    def _search_clear(self):
        self.search_input.clear()
        self._clear_search_highlights()
        self._search_matches = []
        self._search_cursor  = -1
        self.search_count_lbl.setText("")

    def _show_error(self, msg: str):
        self._status(f"✗  {msg}", ERROR_COLOR)
        QMessageBox.critical(self, "Erreur", msg)


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────
def main():
    app = QApplication(sys.argv)
    app.setApplicationName("TLV / EMV Parser")
    app.setStyle("Fusion")

    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window,          QColor(DARK_BG))
    palette.setColor(QPalette.ColorRole.WindowText,      QColor(TEXT_PRIMARY))
    palette.setColor(QPalette.ColorRole.Base,            QColor(PANEL_BG))
    palette.setColor(QPalette.ColorRole.AlternateBase,   QColor("#1C2128"))
    palette.setColor(QPalette.ColorRole.Text,            QColor(TEXT_PRIMARY))
    palette.setColor(QPalette.ColorRole.Button,          QColor(PANEL_BG))
    palette.setColor(QPalette.ColorRole.ButtonText,      QColor(TEXT_PRIMARY))
    palette.setColor(QPalette.ColorRole.Highlight,       QColor(ACCENT))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#000000"))
    app.setPalette(palette)

    window = TLVMainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()