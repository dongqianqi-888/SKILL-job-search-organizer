#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
prepare_table_payload.py — 将岗位核查结果按"批次升序 + 批次内适配等级降序"排序，
输出可直接写入飞书表格的 CSV（含表头，9列）。

用法:
  python3 prepare_table_payload.py <输入.csv|json> [输出.csv]

输入格式:
  CSV : 表头含 批次/公司/.../适配等级 9列（列名含"批次"与"适配等级"即可，其余列按顺序）
  JSON: 数组，每项为 dict 或数组；dict 键支持中文列名与英文别名
        （batch/company/website/status/roles/evidence/location/notes/level），
        键可只写部分字段，缺失列自动留空；数值键自动转字符串。

排序规则:
  1. 批次升序（1→2→3…）
  2. 批次内适配等级降序: 高适配 > 中高适配 > 中适配 > 低适配 > 未确认
  3. 同等级保持原顺序（稳定排序）

输出:
  默认 stdout；给出输出路径时写文件。表头取自输入（9列固定顺序：
  批次/公司/官网/校招状态/目标职能岗/证据说明/地点/备注/适配等级，
  名称缺失时以输入为准）。
"""
import csv
import io
import json
import sys

HEADER = ["批次", "公司", "官网/招聘入口", "校招状态", "目标职能岗",
          "证据说明", "地点/可投性", "备注", "适配等级"]

LEVEL_ORDER = {"高适配": 4, "中高适配": 3, "中适配": 2, "低适配": 1, "未确认": 0}

# JSON dict 输入的英文别名（键可全用英文，如 {"batch":1,"company":"A","level":"高适配"}）
ALIAS = {
    "批次": "batch",
    "公司": "company",
    "官网/招聘入口": "website",
    "校招状态": "status",
    "目标职能岗": "roles",
    "证据说明": "evidence",
    "地点/可投性": "location",
    "备注": "notes",
    "适配等级": "level",
}


def load_rows(path):
    text = open(path, encoding="utf-8-sig").read()
    if path.endswith(".json") or text.lstrip().startswith("["):
        data = json.loads(text)
        rows = []
        for item in data:
            if isinstance(item, dict):
                rows.append([_lookup(item, c) for c in HEADER])
            else:
                rows.append(list(item)[:9])
        return HEADER, rows
    reader = csv.reader(io.StringIO(text))
    lines = [r for r in reader if any(c.strip() for c in r)]
    header = lines[0]
    if len(header) < 2:
        raise SystemExit("CSV 表头不完整")
    return header, lines[1:]


def _lookup(item, col):
    """dict 中取列值：优先中文键，其次英文别名；数字转字符串。"""
    for key in (col, ALIAS[col]):
        if key in item and item[key] is not None:
            v = item[key]
            return str(v) if not isinstance(v, str) else v
    return ""


def sort_rows(rows):
    def key(r):
        batch = ""
        level = ""
        if r:
            v0 = r[0]
            batch = str(v0).strip() if v0 is not None else ""
        if len(r) > 8:
            v8 = r[8]
            level = str(v8).strip() if v8 is not None else ""
        try:
            b = int(batch)
        except ValueError:
            b = 99
        return (b, -LEVEL_ORDER.get(level, 0))
    return sorted(rows, key=key)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    header, rows = load_rows(sys.argv[1])
    rows = sort_rows(rows)
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(header)
    for r in rows:
        w.writerow(r[:9] if len(r) >= 9 else r + [""] * (9 - len(r)))
    out = sys.argv[2] if len(sys.argv) > 2 else None
    if out:
        open(out, "w", encoding="utf-8").write(buf.getvalue())
        print(f"已写入 {out}（{len(rows)} 行数据 + 表头）")
    else:
        sys.stdout.write(buf.getvalue())


if __name__ == "__main__":
    main()
