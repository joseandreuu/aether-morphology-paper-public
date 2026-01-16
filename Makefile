.PHONY: all figures clean \
        fig1 fig2 fig3 fig4 fig5 fig6 \
        fetch_fig2 fetch_fig3 fetch_fig4 fetch_fig5 fetch_fig6

PYTHON := python3
ifneq ("$(wildcard .venv/bin/python)","")
PYTHON := .venv/bin/python
endif
OUTDIRS := outputs/figures outputs/tables data/processed

dirs:
	mkdir -p $(OUTDIRS)

all: figures

figures: dirs fig1 fig2 fig3 fig4 fig5 fig6

fig1: 
	$(PYTHON) -m src.fig1 \
		--out-pdf paper/figures/Fig1.pdf \
		--out-png outputs/figures/Fig1.png

fetch_fig2:
	bash scripts/fetch_fig2_ims_data.sh

fig2: fetch_fig2
	$(PYTHON) -m src.fig2_ims

fetch_fig3:
	bash scripts/fetch_fig3_data.sh

fig3: fetch_fig3
	$(PYTHON) -m src.fig3 \
		--cwru data/processed/fig3/cwru_scored_windows.parquet \
		--vsb  data/processed/fig3/vsb_scored_windows.parquet \
		--out-pdf paper/figures/Fig3.pdf \
		--out-png outputs/figures/Fig3.png

fetch_fig4:
	bash scripts/fetch_fig4_data.sh

fig4: fetch_fig4
	$(PYTHON) -m src.fig4 \
		--csv data/processed/fig4/morphology_destruction.csv \
		--out-pdf paper/figures/Fig4.pdf \
		--out-png outputs/figures/Fig4.png \
		--raw-baseline 0.90

fetch_fig5:
	bash scripts/fetch_fig5_data.sh

fig5: fetch_fig5
	$(PYTHON) -m src.fig5 \
		--aether data/processed/fig5/aether_physical_correlation.csv \
		--convae data/processed/fig5/convae_physical_correlation.csv \
		--out-pdf paper/figures/Fig5.pdf \
		--out-png outputs/figures/Fig5.png \
		--no-title

fetch_fig6:
	bash scripts/fetch_fig6_data.sh

fig6: fetch_fig6
	$(PYTHON) -m src.fig6 \
		--scores-csv data/processed/fig6/reverb_L1_scores_by_file.csv \
		--metrics-json data/processed/fig6/cwru_auc_metrics.json \
		--out-pdf paper/figures/Fig6.pdf \
		--out-png outputs/figures/Fig6.png

clean:
	rm -f outputs/figures/* outputs/tables/*
