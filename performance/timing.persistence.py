
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
persistence.hosts = ["pangolin", "meglTower"]
persistence.variants = ["JIT", "stagger", "twist", "split"]

sizes = {
	2: 16,
	3: 3,
	4: 3
}

defaults = persistence.plots.defaults

# Initialize the plot.
metadata.initialize(plt)

for host in persistence.hosts:
	for field in persistence.fields:
		for dimension in persistence.dimensions:

			fig, ax = plt.subplots(**persistence.plots.defaults.subplots)
			positions = persistence.plots.defaults.boxplot.positions(len(persistence.variants), spacing=1.5, width=0.15)

			xticks = np.array([])
			Boxes = dict()

			for i, (color, pos, name) in enumerate(zip(persistence.colors, positions, persistence.variants)):
				try: data = persistence.data(host, name)
				except: break

				# Get the subset of the data corresponding to the dimension and field,
				# then winnow the data to some subset of scales.
				subset = data[(data.DIMENSION == dimension) & (data.FIELD == field)]
				scales = subset.SCALE.unique()
				scales = [L for L in scales if L >= sizes[dimension]]

				boxes = [
					subset[subset.SCALE == scale].TTC for scale in scales
				]

				# If there's nothing in the dataset, keep going.
				if not len(boxes): continue
				if len(boxes) >= len(xticks): xticks = scales

				# Add the data to the record.
				Boxes[name] = boxes

				# Plot the boxes.
				posns = np.arange(1, len(boxes)+1) + pos
				ax.boxplot(boxes, positions=posns, **persistence.plots.defaults.boxplot.props(color, widths=0.15))

				# Plot the medians.
				medians = np.array([
					np.median(box) for box in boxes
				])

				ax.scatter(posns, medians, **persistence.plots.defaults.boxplot.medians(color, size=3))

			if not len(Boxes): break

			# Find the points of the 99th percentiles (i.e. the point at the end
			# of the topmost whisker) of the first set of boxes and put the
			# corresponding variants' names there.
			pt = max([np.percentile(Boxes[variant][0], 99) for variant in Boxes.keys()])
			pt *= 1.1

			for posn, name in zip(positions, Boxes.keys()):
				ax.text(
					1+posn, np.percentile(Boxes[name][0], 99)*1.1,
					name,
					fontsize=5,
					rotation=90,
					ha="center",
					va="bottom"
				)

			# Draw "pinstripes" by alternately highlighting the regions of the
			# plot corresponding to each lattice scale.
			defaults.boxplot.pinstripes(len(xticks), ax, alpha=1/40)

			# Set horizontal axis ticks.
			ticks = range(1,len(xticks)+1)
			ax.set_xticks(ticks)
			
			# Set horizontal axis tick labels.
			ax.set_xticklabels([
				f"{t}" if i > 0 else rf"$L={t}$" for i, t in enumerate(xticks)
			], fontsize=7)

			# Add the number of cells in each complex (i.e. columns in each full
			# boundary matrix) and alternate the heights so they're readable.
			for i in range(0, len(xticks)):
				ax.text(
					i+1, -0.075 if i%2 else -0.1,
					# rf"$(2^{{{int(np.log2(metadata.cells[dimension][xticks[i]]))}}})$",
					f"{metadata.cells[dimension][xticks[i]]:,}",
					transform=ax.get_xaxis_transform(),
					ha="center",
					fontsize=4
				)

			# Set horizontal axis limits.
			ax.set_xlim(1/2, len(xticks)+1/2)

			# Set horizontal and vertical axis labels.
			# ax.set_xlabel(r"$k$")
			# ax.set_xlabel(r"torus scale $L$")
			# ax.set_ylabel(r"$\mu$s/iteration")

			# Set plot titles.
			# ax.set_title(rf"$\mathbb T^{{{dimension}}}_L$, $\mathbb Z/{{{field}}}\mathbb Z$", fontsize=8)
			# ax.set_title(rf"{host}, $\mathbb T^{{{dimension}}}_k$, $\mathbb Z/{{{field}}}\mathbb Z$", fontsize=8)

			# Set the avertical axis to log time (i.e. microseconds, with labels
			# to contextualize normal human time intervals).
			CONFIG._defaults.yaxis.logTime(ax)
			
			plt.savefig(f"./timing/{host}.{dimension}.{field}.cached.jpeg", **CONFIG._defaults.savefig)
			plt.close()
			plt.clf()

