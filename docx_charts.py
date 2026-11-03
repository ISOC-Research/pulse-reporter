"""
docx_charts.py
==============
Renders the Mermaid charts that the LLM emits (pie / xychart-beta) as static
PNGs in the ISOC palette so they can be embedded in the Word report
(Word cannot execute Mermaid.js).
"""
import os
import re
import tempfile

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from isoc_theme import CHART_PALETTE, DARK_NAVY, DEEP_INDIGO  # noqa: E402

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.edgecolor": "#9AA8B8",
    "axes.labelcolor": f"#{DARK_NAVY}",
    "xtick.color": f"#{DARK_NAVY}",
    "ytick.color": f"#{DARK_NAVY}",
    "axes.spines.top": False,
    "axes.spines.right": False,
})


def _num(s):
    m = re.search(r"-?\d+(?:\.\d+)?", s)
    return float(m.group(0)) if m else None


def _pie_colors(labels):
    """DNSSEC pies use semantic colours (Secure=teal, Insecure=coral, Other=gold, Invalid=plum)."""
    semantic = {"secure": "#40B2A4", "insecure": "#D25238", "other": "#EECA4A", "invalid": "#7E245C"}
    keys = [re.sub(r"\s*\(.*$", "", l).strip().lower() for l in labels]
    if "secure" in keys and "insecure" in keys:
        pal = ["#" + c for c in CHART_PALETTE]
        return [semantic.get(k, pal[i % len(pal)]) for i, k in enumerate(keys)]
    return ["#" + c for c in (CHART_PALETTE * 3)[:len(labels)]]


def _parse_pie(text):
    labels, values = [], []
    for line in text.splitlines():
        m = re.match(r'\s*"(.+?)"\s*:\s*(-?[\d.]+)', line)
        if m:
            labels.append(m.group(1))
            values.append(float(m.group(2)))
    return labels, values


def _parse_xy(text):
    xs = re.search(r"x-axis[^\[\n]*\[(.*?)\]", text, re.S)
    ys = re.search(r'y-axis\s*(?:"(.*?)")?\s*([\d.\-]+)?\s*(?:-->\s*([\d.\-]+))?', text)
    series = []
    for kind in ("bar", "line"):
        for m in re.finditer(rf"^\s*{kind}\s*\[(.*?)\]", text, re.M):
            vals = [_num(v) for v in m.group(1).split(",")]
            series.append((kind, [v for v in vals if v is not None]))
    labels = [x.strip().strip('"\'') for x in xs.group(1).split(",")] if xs else []
    ylabel = ys.group(1) if ys and ys.group(1) else ""
    ymax = float(ys.group(3)) if ys and ys.group(3) else None
    return labels, series, ylabel, ymax


def render_mermaid(mermaid_text, title=""):
    """Return a temp PNG path for the chart, or None if it can't be parsed."""
    text = mermaid_text.strip()
    fd, path = tempfile.mkstemp(suffix=".png")
    os.close(fd)
    try:
        if text.startswith("pie"):
            labels, values = _parse_pie(text)
            if not values:
                raise ValueError("empty pie")
            # strip "(xx%)" suffixes the generator adds to labels
            labels = [re.sub(r"\s*\([\d.]+\s*%?\)\s*$", "", l) for l in labels]
            fig, ax = plt.subplots(figsize=(6.4, 3.4))
            wedges, _, autotexts = ax.pie(
                values, colors=_pie_colors(labels), startangle=90, counterclock=False,
                autopct=lambda p: f"{p:.1f}%" if p >= 4 else "",
                pctdistance=0.78, wedgeprops=dict(width=0.45, edgecolor="white", linewidth=1.5),
                textprops=dict(color="white", fontsize=8, fontweight="bold"))
            ax.legend(wedges, [f"{l} ({v:g}%)" for l, v in zip(labels, values)],
                      loc="center left", bbox_to_anchor=(1.0, 0.5), frameon=False, fontsize=8)
            ax.set_aspect("equal")
        elif text.startswith("xychart"):
            labels, series, ylabel, ymax = _parse_xy(text)
            if not series or all(v == 0 for _, vals in series for v in vals):
                raise ValueError("no data")
            fig, ax = plt.subplots(figsize=(6.4, 3.2))
            n = len(series[0][1])
            xs = list(range(n))
            labels = (labels + [""] * n)[:n]
            for i, (kind, vals) in enumerate(series):
                color = "#" + CHART_PALETTE[i % len(CHART_PALETTE)]
                vals = vals[:n]
                if kind == "bar":
                    bars = ax.bar(xs[:len(vals)], vals, color=color, width=0.6)
                    for b, v in zip(bars, vals):
                        ax.text(b.get_x() + b.get_width() / 2, b.get_height(), f"{v:g}",
                                ha="center", va="bottom", fontsize=7.5, color=f"#{DEEP_INDIGO}")
                else:
                    ax.plot(xs[:len(vals)], vals, marker="o", color=color, linewidth=2)
            ax.set_xticks(xs)
            ax.set_xticklabels(labels, fontsize=8, rotation=0 if n <= 6 else 30,
                               ha="center" if n <= 6 else "right")
            if ylabel:
                ax.set_ylabel(ylabel, fontsize=8.5)
            if ymax:
                ax.set_ylim(0, ymax)
            ax.grid(axis="y", color="#E3E8EF", linewidth=0.8)
            ax.set_axisbelow(True)
        else:
            raise ValueError("unsupported chart type")
        fig.tight_layout()
        fig.savefig(path, dpi=200, facecolor="white")
        plt.close(fig)
        return path
    except Exception as exc:
        plt.close("all")
        print(f"   [warn] Chart skipped in Word export ({exc})".encode("ascii", "replace").decode())
        try:
            os.remove(path)
        except OSError:
            pass
        return None


# ═══════════════════════════════════════════════════════════════════════
# Structured chart renderer (used for BOTH the Word report and the HTML brief)
# The LLM emits  <div class="isoc-chart">{json}</div>  blocks; this turns the
# JSON into a PNG in the ISOC style.  Types: donut | bar | line | matrix
# ═══════════════════════════════════════════════════════════════════════
import json  # noqa: E402
import textwrap  # noqa: E402

BENCH_COLOR = "#c0392b"
BLUE, INDIGO, TEAL, CORAL, GOLD = "#3A82E4", "#24366E", "#40B2A4", "#D25238", "#EECA4A"


def parse_chart_json(raw):
    """Tolerant JSON loader for LLM output (strict=False allows raw newlines in strings)."""
    raw = (raw or "").strip()
    raw = re.sub(r"^```(?:json)?|```$", "", raw, flags=re.M).strip()
    return json.loads(raw, strict=False)


def _title(fig, title):
    if title:
        fig.suptitle(textwrap.fill(title, 78), x=0.01, y=0.99, ha="left", va="top",
                     fontsize=10.5, fontweight="bold", color=INDIGO)


def _fmt(v, suffix=""):
    return f"{v:g}{suffix}"


def _donut(spec, path):
    labels = [str(l) for l in spec["labels"]]
    values = [float(v) for v in spec["values"]]
    suffix = spec.get("suffix", "%")
    n = len(values)
    fig, ax = plt.subplots(figsize=(6.6, 3.5))
    cols = _pie_colors(labels)
    wedges, _ = ax.pie(values, colors=cols, startangle=90, counterclock=False,
                       wedgeprops=dict(width=0.42, edgecolor="white", linewidth=1.5))
    total = sum(values) or 1
    # direct percentage labels on large segments
    import math
    for w, v in zip(wedges, values):
        if v / total >= 0.06:
            ang = math.radians((w.theta1 + w.theta2) / 2)
            ax.text(0.79 * math.cos(ang), 0.79 * math.sin(ang), _fmt(v, suffix),
                    ha="center", va="center", fontsize=8, fontweight="bold", color="white")
    center = str(spec.get("center", "")).replace("\\n", "\n")
    if center:
        head, _, rest = center.partition("\n")
        ax.text(0, 0.07 if rest else 0, head, ha="center", va="center",
                fontsize=17, fontweight="bold", color="#0F2A47")
        if rest:
            ax.text(0, -0.17, textwrap.fill(rest, 14), ha="center", va="top",
                    fontsize=8, color="#44566a")
    ax.legend(wedges, [f"{textwrap.fill(l, 34)}  ({_fmt(v, suffix)})" for l, v in zip(labels, values)],
              loc="center left", bbox_to_anchor=(1.02, 0.5), frameon=False, fontsize=8,
              labelspacing=0.8)
    ax.set_aspect("equal")
    _title(fig, spec.get("title", ""))
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    fig.savefig(path, dpi=200, facecolor="white", bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)


def _bar(spec, path):
    labels = [str(l) for l in spec["labels"]]
    values = [float(v) for v in spec["values"]]
    suffix = spec.get("suffix", "%")
    bench = spec.get("benchmark")
    n = len(values)
    horizontal = spec.get("horizontal")
    if horizontal is None:
        horizontal = n > 6 or max(len(l) for l in labels) > 14
    colors = ["#" + CHART_PALETTE[0]] * n
    top = max(values + ([float(bench["value"])] if bench else []))
    pct = suffix == "%" and top <= 100
    lim = 100 if pct else top * 1.18
    if horizontal:
        fig, ax = plt.subplots(figsize=(6.6, max(2.4, 0.42 * n + 1.5)))
        ys = list(range(n))[::-1]
        bars = ax.barh(ys, values, color=colors, height=0.62)
        ax.set_yticks(ys)
        ax.set_yticklabels([textwrap.fill(l, 30) for l in labels], fontsize=8)
        for b, v in zip(bars, values):
            ax.text(b.get_width() + lim * 0.01, b.get_y() + b.get_height() / 2, _fmt(v, suffix),
                    va="center", fontsize=7.5, color=INDIGO)
        ax.set_xlim(0, lim * (1.08 if pct else 1))
        if spec.get("ylabel"):
            ax.set_xlabel(spec["ylabel"], fontsize=8.5)
        ax.grid(axis="x", color="#E3E8EF", linewidth=0.8)
        if bench:
            ax.axvline(float(bench["value"]), color=BENCH_COLOR, linestyle="--", linewidth=1.4,
                       label=f'{bench.get("label", "Benchmark")} ({_fmt(float(bench["value"]), suffix)})')
    else:
        fig, ax = plt.subplots(figsize=(6.6, 3.5))
        xs = list(range(n))
        bars = ax.bar(xs, values, color=colors, width=0.58)
        ax.set_xticks(xs)
        ax.set_xticklabels([textwrap.fill(l, 14) for l in labels], fontsize=8)
        for b, v in zip(bars, values):
            ax.text(b.get_x() + b.get_width() / 2, b.get_height() + lim * 0.012, _fmt(v, suffix),
                    ha="center", va="bottom", fontsize=8, color=INDIGO)
        ax.set_ylim(0, lim)
        if spec.get("ylabel"):
            ax.set_ylabel(spec["ylabel"], fontsize=8.5)
        ax.grid(axis="y", color="#E3E8EF", linewidth=0.8)
        if bench:
            ax.axhline(float(bench["value"]), color=BENCH_COLOR, linestyle="--", linewidth=1.4,
                       label=f'{bench.get("label", "Benchmark")} ({_fmt(float(bench["value"]), suffix)})')
    ax.set_axisbelow(True)
    if bench:
        ax.legend(loc="lower right" if horizontal else "upper right", frameon=False, fontsize=8)
    _title(fig, spec.get("title", ""))
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig(path, dpi=200, facecolor="white", bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)


def _line(spec, path):
    labels = [str(l) for l in spec["labels"]]
    values = [float(v) for v in spec["values"]]
    suffix = spec.get("suffix", "%")
    bench = spec.get("benchmark")
    fig, ax = plt.subplots(figsize=(6.6, 3.3))
    xs = list(range(len(values)))
    ax.plot(xs, values, marker="o", color=BLUE, linewidth=2.2, label=spec.get("series", "Country"))
    for x, v in zip(xs, values):
        ax.annotate(_fmt(v, suffix), (x, v), textcoords="offset points", xytext=(0, 8),
                    ha="center", fontsize=8, color=INDIGO)
    if bench:
        ax.axhline(float(bench["value"]), color=BENCH_COLOR, linestyle="--", linewidth=1.4,
                   label=f'{bench.get("label", "Benchmark")} ({_fmt(float(bench["value"]), suffix)})')
    top = max(values + ([float(bench["value"])] if bench else []))
    ax.set_ylim(0, 100 if suffix == "%" and top <= 100 else top * 1.2)
    ax.set_xticks(xs)
    ax.set_xticklabels([textwrap.fill(l, 12) for l in labels], fontsize=8)
    if spec.get("ylabel"):
        ax.set_ylabel(spec["ylabel"], fontsize=8.5)
    ax.grid(axis="y", color="#E3E8EF", linewidth=0.8)
    ax.set_axisbelow(True)
    if bench or spec.get("series"):
        ax.legend(loc="best", frameon=False, fontsize=8)
    _title(fig, spec.get("title", ""))
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig(path, dpi=200, facecolor="white", bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)


def _matrix(spec, path):
    items = spec["items"]
    fig, ax = plt.subplots(figsize=(6.6, 4.0))
    ax.set_xlim(0, 10)
    ax.set_ylim(5, 10.4)
    ax.axvline(4.5, color="#7a8aa0", linestyle="--", linewidth=1.2)
    ax.axvspan(0, 4.5, color="#EAF4F2", zorder=0)
    ax.axvspan(4.5, 10, color="#FBF3E2", zorder=0)
    ax.text(2.25, 10.18, "QUICK WINS", ha="center", va="center", fontsize=9, fontweight="bold", color="#26867A")
    ax.text(7.25, 10.18, "STRUCTURAL INVESTMENT", ha="center", va="center", fontsize=9,
            fontweight="bold", color="#A9402B")
    seen = {}
    for it in items:
        x = min(max(float(it.get("effort", 5)), 0.4), 9.6)
        y = min(max(float(it.get("impact", 7)), 5.3), 9.7)
        k = (round(x, 1), round(y, 1))
        seen[k] = seen.get(k, 0) + 1
        off = (seen[k] - 1) * 0.42  # nudge overlapping circles apart
        x += off
        quick = x < 4.5
        high = y >= 8
        col = (TEAL if high else BLUE) if quick else (CORAL if high else GOLD)
        ax.scatter([x], [y], s=460, color=col, edgecolor="white", linewidth=1.5, zorder=3)
        ax.text(x, y, str(it.get("n", "")), ha="center", va="center", fontsize=8.5,
                fontweight="bold", color="white" if col != GOLD else "#3a2f00", zorder=4)
    ax.set_xlabel("Effort / cost / time to deliver  \u2192", fontsize=9)
    ax.set_ylabel("Resilience impact  \u2192", fontsize=9)
    ax.set_xticks(range(0, 11, 2))
    ax.set_yticks(range(5, 11))
    ax.grid(color="#FFFFFF", linewidth=0.8)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    _title(fig, spec.get("title", ""))
    fig.tight_layout(rect=(0, 0.24, 1, 0.93))
    # numbered legend under the plot, two columns in figure coordinates
    half = (len(items) + 1) // 2
    cols = [items[:half], items[half:]]
    for ci, col_items in enumerate(cols):
        y = 0.21
        for it in col_items:
            txt = textwrap.fill(f'{it.get("n", "")}.  {it.get("label", "")}', 48,
                                subsequent_indent="     ")
            fig.text(0.08 + ci * 0.46, y, txt, ha="left", va="top",
                     fontsize=7.6, color="#22303C")
            y -= 0.036 * (txt.count("\n") + 1) + 0.008
    fig.savefig(path, dpi=200, facecolor="white", bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)


_RENDERERS = {"donut": _donut, "pie": _donut, "bar": _bar, "line": _line, "matrix": _matrix}


def render_chart(spec_or_raw):
    """Render an isoc-chart spec (dict or raw JSON string) -> temp PNG path, or None on failure."""
    fd, path = tempfile.mkstemp(suffix=".png")
    os.close(fd)
    try:
        spec = spec_or_raw if isinstance(spec_or_raw, dict) else parse_chart_json(spec_or_raw)
        fn = _RENDERERS.get(str(spec.get("type", "")).lower())
        if fn is None:
            raise ValueError(f"unknown chart type {spec.get('type')!r}")
        if spec["type"] != "matrix":
            vals = [float(v) for v in spec.get("values", [])]
            if not vals or all(v == 0 for v in vals):
                raise ValueError("no data")
        fn(spec, path)
        return path
    except Exception as exc:
        plt.close("all")
        print(f"   [warn] Chart skipped ({exc})".encode("ascii", "replace").decode())
        try:
            os.remove(path)
        except OSError:
            pass
        return None
