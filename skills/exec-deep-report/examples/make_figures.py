# -*- coding: utf-8 -*-
"""生成样例图 fig_weights.png（全部数字为虚构）。用法：python3 make_figures.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
from chart_style import weights_cumulative

core = [18.9, 15.7, 14.0]                                    # 三家核心，合计 48.6%
raw = [3.2 - 2.5 * i / 26 for i in range(27)]                # 27 只卫星，线性递减
sat = [round(w * 51.4 / sum(raw), 2) for w in raw]           # 归一到 51.4%
sat[-1] = round(51.4 - sum(sat[:-1]), 2)                     # 修正四舍五入误差
names = ["核心A", "核心B", "核心C"] + [f"卫星{i+1:02d}" for i in range(27)]
groups = ["核心"] * 3 + ["卫星"] * 27
print(weights_cumulative(names, core + sat, groups, os.path.join(HERE, "fig_weights.png"), marks=(3, 10)))
