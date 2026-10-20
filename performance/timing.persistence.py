
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import sys

from config import CONFIG

metadata = CONFIG.metadata
persistence = CONFIG.topics.persistence
colors = CONFIG.colors

# Specify available data.
persistence.trials = 100
persistence.fields = [3]
persistence.dimensions = [2, 3, 4, 6]
persistence.hosts = ["pangolin"]
persistence.variants = ["JIT", "stagger", "twist", "split"]

sizes = {
	2: 3,
	3: 3
}

defaults = persistence.plots.defaults

# Initialize the plot.
metadata.initialize(plt)

for host in persistence.hosts:
	for field in persistence.fields:
		for dimension in persistence.dimensions:

			fig, ax = plt.subplots(**persistence.plots.defaults.subplots)
			positions = persistence.plots.defaults.boxplot.positions(len(persistence.variants), spacing=1.5)

			xticks = np.array([])
			Boxes = []

			for i, (color, pos, name) in enumerate(zip(persistence.colors, positions, persistence.variants)):
				try: data = persistence.data(host, name)
				except: break
 
				subset = data[(data.DIMENSION == dimension) & (data.FIELD == field)]
				scales = subset.SCALE.unique()
				scales = [L for L in scales if L >= sizes[dimension]]

				boxes = [
					subset[subset.SCALE == scale].TTC for scale in scales
				]

				Boxes.append(boxes)

				# Plot boxes.
				if not len(boxes): continue
				if len(boxes) >= len(xticks): xticks = scales

				posns = np.arange(1, len(boxes)+1) + pos
				ax.boxplot(boxes, positions=posns, **persistence.plots.defaults.boxplot.props(color))

				# Plot medians.
				medians = np.array([
					np.median(box) for box in boxes
				])

				ax.scatter(posns, medians, **persistence.plots.defaults.boxplot.medians(color))

			# Get the 100th percentile over all boxes, then label at that point.
			if not len(Boxes[0]): continue
			pt = max([np.percentile(Boxes[k][0], 100) for k in range(len(Boxes))])
			pt *= 1.1

			for posn, name in zip(positions, persistence.variants):
				ax.text(
					1+posn, pt,
					name,
					fontsize=3,
					rotation=90,
					ha="center",
					va="bottom"
				)

			defaults.boxplot.pinstripes(len(xticks), ax)

			ticks = range(1,len(xticks)+1)
			ax.set_xticks(ticks)
			ax.set_xticklabels([
				f"{t}" if i > 0 else rf"$L={t}$" for i, t in enumerate(xticks)
			], fontsize=7)
			# ax.set_xticklabels([f"{t}\n({metadata.cells[dimension][t]:,})" for t in xticks], fontsize=7)
			ax.set_xlim(1/2, len(xticks)+1/2)
			# ax.set_xlabel(r"$k$")
			# ax.set_xlabel(r"torus scale $L$")
			# ax.set_ylabel(r"$\mu$s/iteration")

			# ax.set_title(rf"$\mathbb T^{{{dimension}}}_L$, $\mathbb Z/{{{field}}}\mathbb Z$", fontsize=8)
			# ax.set_title(rf"{host}, $\mathbb T^{{{dimension}}}_k$, $\mathbb Z/{{{field}}}\mathbb Z$", fontsize=8)

			CONFIG._defaults.yaxis.logTime(ax)
			
			plt.savefig(f"./timing/{host}.{dimension}.{field}.cached.jpeg", **CONFIG._defaults.savefig)
			plt.close()
			plt.clf()

