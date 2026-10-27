
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import sys

from config import CONFIG

metadata = CONFIG.metadata
colors = CONFIG.colors
models = CONFIG.topics.models
SwendsenWang = CONFIG.topics.models.SwendsenWang

data = SwendsenWang.data("meglTower")

metadata.initialize(plt)

fig, ax = plt.subplots(**models.plots.defaults.subplots)
bigs = np.empty(0)

for branch, shortname in SwendsenWang.branches.items():
	dat = data[branch]
	if dat.empty: continue

	bigs = dat["scale"] if len(dat["scale"]) > len(bigs) else bigs
	ax.plot(dat["scale"], dat["ttc"], label=shortname)

ax.set_xscale("log", base=np.sqrt(2))
ax.set_xlim(min(bigs)-1/2, max(bigs)+1/2)
ax.set_xticks(bigs)
ax.set_xticklabels([f"{int(t)}" for t in bigs])

for i in bigs:
	ax.text(
		i, -0.075, #-0.075 if i%2 else -0.1,
		# rf"$(2^{{{int(np.log2(metadata.cells[dimension][xticks[i]]))}}})$",
		f"{metadata.cells[4][i]:,}",
		transform=ax.get_xaxis_transform(),
		ha="center",
		fontsize=4
	)


ax.legend(loc="lower right")

CONFIG._defaults.yaxis.logTime(ax)

plt.savefig(f"profiling/reduction.jpeg", dpi=1200, bbox_inches="tight")

