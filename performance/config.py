
from sklearn.utils import Bunch
from scipy.optimize import curve_fit
from pathlib import Path
import pandas as pd
import numpy as np

CONFIG = Bunch()
CONFIG.topics = Bunch()

################################################################################
## METADATA ####################################################################
################################################################################
metadata = Bunch()

metadata.hosts = ["meglTower"]
metadata.computing = ["serial", "parallel"]
metadata.statroot = Path("profiling/stat")

metadata.initialize = lambda p: p.rcParams.update({
	"text.usetex": True,
	"font.family": "Times New Roman",
	"text.latex.preamble": r"\usepackage{nicefrac}\usepackage{amsfonts}\usepackage{graphicx}\usepackage{xcolor}"
})

# Cell counts by dimension and scale.
metadata.cells = {
	2: {
		3:         36,
		4:         64,
		5:        100,
		8:        256,
		11:        484,
		16:       1024,
		22:       1936,
		32:       4096,
		45:       8100,
		64:      16384,
		90:      32400,
		128:      65536,
		181:     131044,
		256:     262144,
		362:     524176,
		512:    1048576
	},
	3: {
		3:        216,
		4:        512,
		5:       1000,
		8:       4096,
		11:      10648,
		16:      32768,
		22:      85184,
		32:     262144,
		45:     729000,
		64:    2097152,
		90:    5832000,
	},
	4: {
		3:       1296,
		4:       4096,
		5:      10000,
		8:      65536,
		11:     234256,
		16:    1048576,
		22:    3748096,
		32:   16777216,
	},
	6: {
		3:      46656,
		4:     262144,
		5:    1000000,
		8:   16777216,
	}
}

metadata.halfcells = {
	2: {
		3:         18,
		4:         32,
		5:         50,
		8:        128,
		11:        242,
		16:        512,
		22:        968,
		32:       2048,
		45:       4050,
		64:       8192,
		90:      16200,
		128:      32768,
		181:      65522,
		256:     131072,
		362:     262088,
		512:     524288,
	},
	3: {
		3:         81,
		4:        192,
		5:        375,
		8:       1536,
		11:       3993,
		16:      12288,
		22:      31944,
		32:      98304,
		45:     273375,
		64:     786432,
		90:    2187000,
	},
	4: {
		3:        486,
		4:       1536,
		5:       3750,
		8:      24576,
		11:      87846,
		16:     393216,
		22:    1405536,
		32:    6291456,
	}
}

# Boundary matrix density by dimension and scale.
metadata.density = {
	2: {
		3: 5.555556e-02,
		4: 3.125000e-02,
		5: 2.000000e-02,
		8: 7.812500e-03,
		11: 4.132231e-03,
		16: 1.953125e-03,
		22: 1.033058e-03,
		32: 4.882812e-04,
		45: 2.469136e-04,
		64: 1.220703e-04,
		90: 6.172840e-05,
		128: 3.051758e-05,
		181: 1.526205e-05,
		256: 7.629395e-06,
		362: 3.815512e-06,
		512: 1.907349e-06,
	},
	3: {
		3:    1.388889e-02,
		4:    5.859375e-03,
		5:    3.000000e-03,
		8:    7.324219e-04,
		11:    2.817431e-04,
		16:    9.155273e-05,
		22:    3.521788e-05,
		32:    1.144409e-05,
		45:    4.115226e-06,
		64:    1.430511e-06,
		90:    5.144033e-07,
	},
	4: {
		3:  3.086420e-03,
		4:  9.765625e-04,
		5:  4.000000e-04,
		8:  6.103516e-05,
		11:  1.707534e-05,
		16:  3.814697e-06,
		22:  1.067209e-06,
		32:  2.384186e-07,
	},
	6: {
		3:   1.286008e-04,
		4:   2.288818e-05,
		5:   6.000000e-06,
		8:   3.576279e-07,
	}
}

metadata.logTimeLabels = {
	1e0: "1$\mu$s",
	1e1: "10$\mu$s",
	1e2: "100$\mu$s",
	1e3: "1ms",
	# 0.5e6: r"$\nicefrac 12$s",
	1e4: "10ms",
	1e5: "100ms",
	1e6: "1s",
	3e7: "30s",
	6e7: "1m",
	9e8: "30m",
	3.6e9: "1h",
	4.32e10: "12h",
	8.64e10: "1d",
	6.048e11: "1w"
}

CONFIG.metadata = metadata

################################################################################
## COLORS ######################################################################
################################################################################

colors = Bunch()

tol = Bunch()

tol.bright = Bunch(
	blue="#4477AA",
	cyan="#66CCEE",
	green="#228833",
	yellow="#CCBB44",
	red="#EE6677",
	purple="#AA3377",
	grey="#BBBBBB"
)

tol.highcontrast = Bunch(
	yellow="#DDAA33",
	red="#BB5566",
	blue="#004488"
)

tol.vibrant = Bunch(
	blue="#0077BB",
	cyan="#33BBEE",
	teal="#009988", 
	orange="#EE7733",
	red="#CC3311",
	magenta="#EE3377",
	grey="#BBBBBB"
)

tol.muted = Bunch(
	indigo="#332288",
	cyan="#33BBEE",
	teal="#44AA99",
	green="#117733",
	olive="#999933",
	sand="#DDCC77",
	rose="#CC6677",
	wine="#882255",
	purple="#AA4499"
)

colors.tol = tol
CONFIG.colors = colors


################################################################################
## PLOT DEFAULTS ###############################################################
################################################################################

CONFIG._defaults = Bunch()
CONFIG._defaults.yaxis = Bunch()
CONFIG._defaults.xaxis = Bunch()

# Saved figure properties.
CONFIG._defaults.savefig = dict(
	dpi=1200,
	bbox_inches="tight"
)

# Fallback scatter plots.
CONFIG._defaults.scatter = dict(
	marker="o",
	color="k",
	s=2,
	linewidths=0
)

# Log-scaled time defaults.
CONFIG._defaults.yaxis.logTime = Bunch()

CONFIG._defaults.yaxis.logTime.textprops = dict(
	fontsize=6,
	ha="left",
	va="bottom",
	color="#D3D3D3",
	zorder=-1000
)

CONFIG._defaults.yaxis.logTime.lineprops = dict(
	color="#D3D3D3",
	zorder=-1001
)

CONFIG._defaults.yaxis.logTime = \
	lambda \
		ax, \
		textprops=CONFIG._defaults.yaxis.logTime.textprops, \
		lineprops=CONFIG._defaults.yaxis.logTime.lineprops: \
		_defaultLogTimeVerticalAxis(ax, textprops, lineprops)


################################################################################
## TOPIC: ADDITION #############################################################
################################################################################

CONFIG.topics.addition = Bunch()

CONFIG.topics.addition.exec = "addition"
CONFIG.topics.addition.computing = CONFIG.metadata.computing
CONFIG.topics.addition.hosts = CONFIG.metadata.hosts
CONFIG.topics.addition.trials = 1000
CONFIG.topics.addition.sep = ","
CONFIG.topics.addition.prefix = lambda host, computing: f"{host}.{CONFIG.topics.addition.exec}.{computing}.{CONFIG.topics.addition.trials}"

CONFIG.topics.addition.columns = [
	"N",
	"L",
	"OVERLAP",
	"TTC",
	"CORES"
]

CONFIG.topics.addition.dtypes = {
	"N": int,
	"L": int,
	"OVERLAP": float,
	"TTC": int,
	"CORES": int
}


CONFIG.topics.addition.data = lambda host, computing: _additionReadFile(host, computing, CONFIG.topics.addition)

################################################################################
## PLOTS #######################################################################
################################################################################

CONFIG.topics.addition.plots = Bunch()
CONFIG.topics.addition.plots.defaults = Bunch()

CONFIG.topics.addition.plots.defaults.subplots = dict(
	figsize=(5,2.5)
)

CONFIG.topics.addition.plots.defaults.scatter = CONFIG._defaults.scatter

################################################################
## ADDITION, DENSITY BY TIME ###################################
################################################################

CONFIG.topics.addition.plots.timeByOverlap = Bunch()

CONFIG.topics.addition.plots.timeByOverlap.scatter = CONFIG.topics.addition.plots.defaults.scatter


## AXES ############
CONFIG.topics.addition.plots.timeByOverlap.yaxis = lambda ax: _timeByOverlapVaxis(ax)
CONFIG.topics.addition.plots.timeByOverlap.xaxis = lambda ax, lo, hi: _timeByOverlapHaxis(ax, lo, hi)

## LSQ #############
CONFIG.topics.addition.plots.timeByOverlap.lsq = Bunch()
CONFIG.topics.addition.plots.timeByOverlap.lsq.f = lambda x, a, k: a*x**k
CONFIG.topics.addition.plots.timeByOverlap.lsq.plot = dict(
	c=CONFIG.colors.tol.vibrant.red,
	zorder=-10000
)

CONFIG.topics.addition.plots.timeByOverlap.lsq.text = dict(
	ha="right",
	va="bottom",
	fontsize=4,
	color=CONFIG.colors.tol.vibrant.red
)

## OUTPUT ##########
CONFIG.topics.addition.plots.timeByOverlap.ext = "jpeg"
CONFIG.topics.addition.plots.timeByOverlap.out = lambda host, length, computing, cores: f"./timing/{CONFIG.topics.addition.prefix(host, computing)}.{length}.{cores}.timeByOverlap.{CONFIG.topics.addition.plots.timeByOverlap.ext}"
CONFIG.topics.addition.plots.timeByOverlap.savefig = CONFIG._defaults.savefig


################################################################
## ADDITION, DENSITY BY TIME, OVERLAID #########################
################################################################

CONFIG.topics.addition.plots.timeByOverlapOverlaid = Bunch()

CONFIG.topics.addition.plots.timeByOverlapOverlaid.scatter = CONFIG.topics.addition.plots.defaults.scatter

## AXES ############
CONFIG.topics.addition.plots.timeByOverlapOverlaid.yaxis = CONFIG.topics.addition.plots.timeByOverlap.yaxis
CONFIG.topics.addition.plots.timeByOverlapOverlaid.xaxis = CONFIG.topics.addition.plots.timeByOverlap.xaxis

## LSQ #############
CONFIG.topics.addition.plots.timeByOverlapOverlaid.lsq = Bunch()
CONFIG.topics.addition.plots.timeByOverlapOverlaid.lsq.f = CONFIG.topics.addition.plots.timeByOverlap.lsq.f
CONFIG.topics.addition.plots.timeByOverlapOverlaid.lsq.plot = lambda color: dict(
	c=color,
	zorder=-10000
)

CONFIG.topics.addition.plots.timeByOverlapOverlaid.lsq.text = lambda color: dict(
	ha="right",
	va="bottom",
	fontsize=4,
	color=color
)

## OUTPUT ##########
CONFIG.topics.addition.plots.timeByOverlapOverlaid.ext = "jpeg"

CONFIG.topics.addition.plots.timeByOverlapOverlaid.out = lambda host, length, computing="overlaid": \
	f"./timing/{CONFIG.topics.addition.prefix(host, computing)}.{length}.timeByOverlap.{CONFIG.topics.addition.plots.timeByOverlapOverlaid.ext}"

CONFIG.topics.addition.plots.timeByOverlapOverlaid.savefig = CONFIG._defaults.savefig



























################################################################################
## TOPIC: PERSISTENCE ##########################################################
################################################################################

CONFIG.topics.persistence = Bunch()

CONFIG.topics.persistence.exec = "persistence"
CONFIG.topics.persistence.variants = ["twist", "split", "JIT", "stagger", "parallel", "standard"]
# CONFIG.topics.persistence.variants = ["JIT", "stagger", "twist", "split", "standard"]
CONFIG.topics.persistence.fields = [3]
CONFIG.topics.persistence.dimensions = [2]
CONFIG.topics.persistence.hosts = ["meglTower"]
CONFIG.topics.persistence.trials = 64
CONFIG.topics.persistence.sep = ","
CONFIG.topics.persistence.prefix = lambda host, computing: f"{host}.{CONFIG.topics.persistence.exec}.{computing}.{CONFIG.topics.persistence.trials}"
CONFIG.topics.persistence.minimumsize = 3

CONFIG.topics.persistence.columns = [
	"SCALE",
	"DIMENSION",
	"FIELD",
	"TTC"
]

CONFIG.topics.persistence.dtypes = {
	"SCALE": int,
	"DIMENSION": int,
	"FIELD": int,
	"TTC": int
}

CONFIG.topics.persistence.colors = [
	CONFIG.colors.tol.muted.cyan,
	CONFIG.colors.tol.muted.teal,
	CONFIG.colors.tol.muted.green,
	CONFIG.colors.tol.muted.olive,
	CONFIG.colors.tol.muted.sand,
	CONFIG.colors.tol.muted.rose
]


CONFIG.topics.persistence.data = lambda host, computing: _additionReadFile(host, computing, CONFIG.topics.persistence)


################################################################################
## PLOTS #######################################################################
################################################################################

CONFIG.topics.persistence.plots = Bunch()
CONFIG.topics.persistence.plots.defaults = Bunch()

CONFIG.topics.persistence.plots.defaults.subplots = dict(
	figsize=(4,5)
)

CONFIG.topics.persistence.plots.defaults.scatter = CONFIG._defaults.scatter


CONFIG.topics.persistence.plots.defaults.boxplot = Bunch()
CONFIG.topics.persistence.plots.defaults.boxplot.lw = 1/2
CONFIG.topics.persistence.plots.defaults.boxplot.boxwidths = 0.1
CONFIG.topics.persistence.plots.defaults.boxplot.boxspacing = 1.25

CONFIG.topics.persistence.plots.defaults.boxplot.positions = lambda k, width=CONFIG.topics.persistence.plots.defaults.boxplot.boxwidths, spacing=CONFIG.topics.persistence.plots.defaults.boxplot.boxspacing: _boxplotSpacing(k, width, spacing)

CONFIG.topics.persistence.plots.defaults.boxplot.medianprops = dict(
	lw=0,
	color="k"
)

CONFIG.topics.persistence.plots.defaults.boxplot.boxprops = lambda color: dict(
	facecolor=color,
	lw=0
)

CONFIG.topics.persistence.plots.defaults.boxplot.whiskerprops = dict(
	lw=CONFIG.topics.persistence.plots.defaults.boxplot.lw
)

CONFIG.topics.persistence.plots.defaults.boxplot.capprops = dict(
	lw=CONFIG.topics.persistence.plots.defaults.boxplot.lw
)

CONFIG.topics.persistence.plots.defaults.boxplot.medians = lambda color, size=4: dict(
	zorder=1000,
	marker="D",
	facecolor=color,
	edgecolor="k",
	s=size,
	lw=CONFIG.topics.persistence.plots.defaults.boxplot.lw
)

CONFIG.topics.persistence.plots.defaults.boxplot.props = \
	lambda color, \
	widths=CONFIG.topics.persistence.plots.defaults.boxplot.boxwidths \
	: dict(
		showfliers=False,
		widths=widths,
		whis=(1,99),
		patch_artist=True,
		boxprops=CONFIG.topics.persistence.plots.defaults.boxplot.boxprops(color),
		medianprops=CONFIG.topics.persistence.plots.defaults.boxplot.medianprops,
		whiskerprops=CONFIG.topics.persistence.plots.defaults.boxplot.whiskerprops,
		capprops=CONFIG.topics.persistence.plots.defaults.boxplot.capprops
	)

CONFIG.topics.persistence.plots.defaults.boxplot.pinstripes = lambda boxes, ax, color="black", alpha=1/20: _boxplotPinstripes(boxes, ax, color, alpha)












################################################################################
## TOPIC: MODELS ###############################################################
################################################################################

CONFIG.topics.models = Bunch()
CONFIG.topics.models.plots = Bunch()
CONFIG.topics.models.plots.defaults = Bunch()

CONFIG.topics.models.plots.defaults.subplots = dict(
	figsize=(4,5)
)



################################################################################
## SUBTOPIC: MODELS: SWENDSEN–WANG #############################################
################################################################################
CONFIG.topics.models.SwendsenWang = Bunch()
SwendsenWang = CONFIG.topics.models.SwendsenWang

SwendsenWang.computing = ["meglTower", "pangolin"]

SwendsenWang.branches = {
	"default": "default",
	"default-updated-SparseRREF": "uS",
	"default-updated-SparseRREF-pmatmul": "uSp",
	"default-updated-SparseRREF-pmatmul-blocks": "uSpb",
	"default-updated-SparseRREF-pmatmul-blocks-mimalloc": "uSpbm",
	"pmatmul": "p",
	"pmatmul-nomimalloc": "pn",
	"pmatmul-nomimalloc-openmp": "pno"
}


SwendsenWang.parameters = Bunch()
SwendsenWang.parameters.fields = [3]
SwendsenWang.parameters.scales = [8, 11, 16, 22]
SwendsenWang.parameters.dimensions = [4]
SwendsenWang.parameters.trials = 25





SwendsenWang.data = lambda remote: _readSWStats(remote, "SwendsenWang", SwendsenWang.branches, SwendsenWang.parameters, CONFIG.metadata.statroot)



def _readSWStats(computing, model, branches, parameters, root):
	allBranches = {}

	for branch in branches:
		records = []

		for field in parameters.fields:
			for scale in parameters.scales:
				for dimension in parameters.dimensions:
					try:
						with open(f"{root}/{computing}.{model}.{scale:02}.{dimension}.{field}.1.{branch}.stat") as f:
							content = f.read()
							splitt = content.split("\n")
							splitt = [s.strip() for s in splitt]
							
							_elapsed = [e for e in splitt if "seconds time elapsed" in e][0]
							if not _elapsed: continue

							elapsed = float(_elapsed.split("seconds")[0])
							records.append({
								"field": field,
								"scale": scale,
								"dimension": dimension,
								"ttc": elapsed*1000000	# convert to microseconds
							})
					except:
						pass

		# Create a dataframe from the records.
		data = pd.DataFrame.from_records(records)
		allBranches[branch] = data

	return allBranches



################################################################################
## MISCELLANEOUS FUNCTIONS #####################################################
################################################################################
def _additionReadFile(host, computing, topic):
	pref = topic.prefix(host, computing)
	data = pd.read_csv(f"./timing/{pref}.csv", sep=topic.sep, names=topic.columns)

	for column in topic.columns: data[column] = data[column].astype(topic.dtypes[column])

	return data


def _defaultLogTimeVerticalAxis(ax, textprops, lineprops):
	# Fiddle with axis limits; make it look a bit cleaner, perhaps?
	ax.set_yscale("log")
	ylo, yhi = ax.get_ylim()

	loglo = int(np.log10(ylo))
	loghi = int(np.log10(yhi))

	ax.set_yticks([10**k for k in range(loglo, loghi+2)])

	ylo = 10**loglo
	yhi = 10**(loghi+1)
	ax.set_ylim(ylo, yhi+10)

	xlo, xhi = ax.get_xlim()

	for tick, label in CONFIG.metadata.logTimeLabels.items():
		if ylo <= tick <= yhi:
			ax.text(xlo+0.05, tick, f"{label}", **textprops)
			ax.plot([xlo, xhi], [tick, tick], **lineprops)


def _timeByOverlapVaxis(ax):
	CONFIG._defaults.yaxis.logTime(ax)

def _timeByOverlapHaxis(ax, lo, hi):
	ax.set_xlim(lo+1/2, hi-1/2)
	ax.set_xticks([hi*k for k in [0, 1/4, 1/2, 3/4, 1]])

	ax.set_xticklabels([
		f"${t}$" for t in [r"0", r"\nicefrac 14", r"\nicefrac 12", r"\nicefrac 34", r"1"]
	])


def _boxplotSpacing(k, width=0.1, spacing=1.25):
	# If there are an odd number of boxes, center at 0 and add 1.25x the width
	# for (k-1)/2 repetitions on each side.
	unit = spacing*width

	if k % 2:
		lrcount = int((k-1)/2)
		right = [unit*r for r in range(1, lrcount+1)]
		left = [-unit*l for l in range(1, lrcount+1)]
		return list(sorted(left + [0] + right))
	else:
		lrcount = int(k/2)
		right = [unit*r-unit/2 for r in range(1, lrcount+1)]
		left = [-r for r in right]
		return list(sorted(left + right))


def _boxplotPinstripes(k, ax, color, alpha):
	for i in range(1, k+1, 2):
		ax.axvspan(i-1/2, i+1/2, facecolor=color, edgecolor="none", alpha=alpha, zorder=0)


