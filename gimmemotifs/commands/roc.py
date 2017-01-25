#!/usr/bin/python -W ignore
# Copyright (c) 2009-2016 Simon van Heeringen <simon.vanheeringen@gmail.com>
#
# This module is free software. You can redistribute it and/or modify it under 
# the terms of the MIT License, see the file COPYING included with this 
# distribution.
import sys
import os

from gimmemotifs.motif import read_motifs
from gimmemotifs.plot import roc_plot
from gimmemotifs.stats import calc_stats

def roc(args):
    """ Calculate ROC_AUC and other metrics and optionally plot ROC curve.
    """
    pwmfile = args.pwmfile
    fg_file = args.sample
    bg_file = args.background
    outputfile = args.outfile
    # Default extension for image
    if outputfile and   not outputfile.endswith(".png"):
        outputfile += ".png"
    
    motifs = read_motifs(open(pwmfile), fmt="pwm")

    ids = []
    if args.ids:
        ids = args.ids.split(",")
    else:
        ids = [m.id for m in motifs]
    motifs = [m for m in motifs if (m.id in ids)]
    
    stats = [
            "roc_auc", 
            "mncp", 
            "enr_at_fdr",
            "max_enrichment", 
            "recall_at_fdr", 
            "roc_values"
            ]
    
    motif_stats = calc_stats(motifs, fg_file, bg_file, stats)

    plot_x = []
    plot_y = []
    # Print the metrics
    print "Motif\tROC AUC\tMNCP\tEnr. at 5% FDR\tMax enr.\tRecall at 10% FDR"
    for i,motif_id in enumerate(ids):
        if outputfile:
            x, y = motif_stats[motif_id]["roc_values"]
            plot_x.append(x)
            plot_y.append(y)
        print "{}\t{:.3f}\t{:.3f}\t{:.2f}\t{:0.2f}\t{:0.4f}".format(
              motif_id, 
              motif_stats[motif_id]["roc_auc"], 
              motif_stats[motif_id]["mncp"], 
              motif_stats[motif_id]["enr_at_fdr"], 
              motif_stats[motif_id]["max_enrichment"][0], 
              motif_stats[motif_id]["recall_at_fdr"],
              )
    
    # Plot the ROC curve
    if outputfile:
        roc_plot(outputfile, plot_x, plot_y, ids=ids)
