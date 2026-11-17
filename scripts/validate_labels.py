"""Kiá»ƒm tra file nhĂ£n COCO (export tá»« CVAT) TRÆ¯á»C KHI ná»™p.

    python scripts/validate_labels.py --all
    python scripts/validate_labels.py submission/labels/123_NguyenVanA.json

Kiá»ƒm: tĂªn file, tĂªn lá»›p, giĂ¡ trá»‹ thuá»™c tĂ­nh, box trong áº£nh, box quĂ¡ nhá», áº£nh Ä‘á»§/thá»«a so vá»›i danh sĂ¡ch Ä‘Æ°á»£c giao.
Exit code 1 náº¿u cĂ³ ERROR.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

from common import IMAGES_DIR, ROOT, Taxonomy, list_label_files, load_assignment, load_coco, load_taxonomy, rel

NAME_RE = re.compile(r"^(2A\d{9})_([A-Za-z0-9_\-]+)\.json$")


def validate(path: Path, tax: Taxonomy, assignment) -> tuple:
    errs, warns = [], []
    m = NAME_RE.match(path.name)
    if not m:
        errs.append("TĂªn file pháº£i dáº¡ng <MSHV>_<HoTen>.json, MSHV lĂ  sá»‘, HoTen viáº¿t liá»n khĂ´ng dáº¥u "
                    "(VD: 20001_NguyenVanA.json). HĂ£y Ä‘á»•i tĂªn file.")
    try:
        lf = load_coco(path, tax)
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        return [f"KhĂ´ng Ä‘á»c Ä‘Æ°á»£c file nhÆ° COCO JSON ({e}). Export láº¡i tá»« CVAT: Actions -> Export task dataset -> COCO 1.0."], [], Counter()
    warns += [f"{p}" for p in lf.problems]
    counts = Counter()
    missing_attr = Counter()
    for img, objs in lf.objects.items():
        w, h = lf.images[img]
        if not (IMAGES_DIR / img).exists():
            errs.append(f"{img}: khĂ´ng cĂ³ trong data/images/ (tĂªn áº£nh trong file khĂ´ng khá»›p áº£nh gá»‘c).")
        for o in objs:
            tag = f"{img} (annotation id={o.id}, lá»›p {o.cls})"
            if o.cls not in tax.classes:
                errs.append(f"{tag}: lá»›p '{o.cls}' KHĂ”NG thuá»™c taxonomy {tax.classes}. Sá»­a tĂªn lá»›p trong CVAT.")
                continue
            counts[o.cls] += 1
            x1, y1, x2, y2 = o.box
            if x2 - x1 <= 0 or y2 - y1 <= 0:
                errs.append(f"{tag}: box cĂ³ chiá»u rá»™ng/cao <= 0.")
                continue
            if w and h and (x1 < -1 or y1 < -1 or x2 > w + 1 or y2 > h + 1):
                errs.append(f"{tag}: box [{x1:.0f},{y1:.0f},{x2:.0f},{y2:.0f}] vÆ°á»£t ra ngoĂ i áº£nh {w}x{h}.")
            if o.cls != tax.ignore and (y2 - y1) < tax.rules["min_box_height_px"]:
                warns.append(f"{tag}: cao {y2 - y1:.0f}px < {tax.rules['min_box_height_px']}px -> theo quy táº¯c nĂªn "
                             f"gá»™p vĂ o má»™t vĂ¹ng {tax.ignore}.")
            if o.cls != tax.ignore:
                for n in tax.attrs:
                    if n not in o.raw_attrs:
                        missing_attr[n] += 1
                    elif not tax.valid(n, o.attrs[n]):
                        errs.append(f"{tag}: thuá»™c tĂ­nh {n}='{o.raw_attrs[n]}' khĂ´ng há»£p lá»‡ "
                                    f"(chá»‰ nháº­n {tax.attrs[n].get('values') or 'true/false'}).")
    for n, c in missing_attr.items():
        warns.append(f"{c} Ä‘á»‘i tÆ°á»£ng thiáº¿u thuá»™c tĂ­nh '{n}' (coi nhÆ° giĂ¡ trá»‹ máº·c Ä‘á»‹nh '{tax.attrs[n].get('default')}'). "
                     f"Kiá»ƒm tra láº¡i khi export / Ä‘Ă£ khai bĂ¡o thuá»™c tĂ­nh trong CVAT chÆ°a.")
    if assignment is not None and m:
        mshv = m.group(1)
        mine = {i for i, a in assignment.items() if mshv in a}
        if not mine:
            errs.append(f"MSHV {mshv} khĂ´ng cĂ³ trong assignment.csv. Kiá»ƒm tra láº¡i tĂªn file / danh sĂ¡ch --members.")
        else:
            have = set(lf.images)
            miss, extra = sorted(mine - have), sorted(have - mine)
            if miss:
                errs.append(f"Thiáº¿u {len(miss)} áº£nh Ä‘Æ°á»£c giao: {', '.join(miss[:8])}{' ...' if len(miss) > 8 else ''}. "
                            "GĂ¡n ná»‘t rá»“i export láº¡i (áº£nh khĂ´ng cĂ³ váº­t váº«n pháº£i náº±m trong task).")
            if extra:
                warns.append(f"CĂ³ {len(extra)} áº£nh KHĂ”NG Ä‘Æ°á»£c giao cho báº¡n: {', '.join(extra[:8])}"
                             f"{' ...' if len(extra) > 8 else ''} (sáº½ bá»‹ bá» qua khi QC).")
    return errs, warns, counts


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="*", help="File nhĂ£n cáº§n kiá»ƒm")
    ap.add_argument("--all", action="store_true", help="Kiá»ƒm má»i file trong submission/labels/")
    args = ap.parse_args()
    tax = load_taxonomy()
    files = [Path(f) for f in args.files] or (list_label_files() if args.all else [])
    if not files:
        ap.error("ChÆ°a chá»‰ Ä‘á»‹nh file. DĂ¹ng --all hoáº·c truyá»n Ä‘Æ°á»ng dáº«n file nhĂ£n.")
    assignment = load_assignment()
    if assignment is None:
        print("(ChÆ°a cĂ³ submission/qc/assignment.csv -> bá» qua kiá»ƒm áº£nh Ä‘á»§/thá»«a. Cháº¡y split_assign.py trÆ°á»›c.)\n")
    total_err = 0
    for p in files:
        errs, warns, counts = validate(p, tax, assignment)
        total_err += len(errs)
        print(f"=== {rel(p.resolve())}: {len(errs)} lá»—i, {len(warns)} cáº£nh bĂ¡o")
        for e in errs:
            print(f"  [ERROR] {e}")
        for w in warns:
            print(f"  [WARN]  {w}")
        if counts:
            print("  Sá»‘ box theo lá»›p: " + ", ".join(f"{c}={n}" for c, n in sorted(counts.items())))
    print("\n" + ("Káº¾T QUáº¢: cĂ³ lá»—i, hĂ£y sá»­a vĂ  export láº¡i trÆ°á»›c khi ná»™p." if total_err else "Káº¾T QUáº¢: khĂ´ng cĂ³ ERROR."))
    print("LÆ¯U Ă: script nĂ y chá»‰ kiá»ƒm Ä‘á»‹nh dáº¡ng/quy táº¯c mĂ¡y kiá»ƒm Ä‘Æ°á»£c. Script KHĂ”NG biáº¿t box cĂ³ Ă´m sĂ¡t váº­t hay khĂ´ng, "
          "lá»›p cĂ³ Ä‘Ăºng thá»±c táº¿ khĂ´ng, cĂ³ bá» sĂ³t váº­t hay khĂ´ng - pháº§n Ä‘Ă³ cáº§n máº¯t ngÆ°á»i (QC).")
    sys.exit(1 if total_err else 0)


if __name__ == "__main__":
    main()

