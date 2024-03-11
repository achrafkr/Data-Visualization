# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 2024

@author: Achrafkr
"""

import numpy as np

class Radar(object):
    
    """
    Radar class creates a radar plot using the polar projection based 
    matplotlib framework
    """
    
    def __init__(self, fig, titles, labels, n_sep=11, rect=None):
        if rect is None:
            rect = [0.05, 0.05, 0.5, 0.5]
        color="w" #"#EAEAF2"
        self.n = len(titles)
        self.angles = np.arange(0, 360, 360.0/self.n)
        self.axes = [fig.add_axes(rect, projection="polar", label="axes%d" % i) 
                         for i in range(self.n)]
    
        self.ax = self.axes[0]
        self.ax.set_facecolor(color)
        l, text = self.ax.set_thetagrids(self.angles, labels=titles, fontsize=8)
        [txt.set_position((np.deg2rad(angle),-0.06)) for txt, angle in zip(text, self.angles)]
        [txt.set_rotation(90-angle) for txt, angle in zip(text, self.angles)]
        
        for ax in self.axes[1:]:
            ax.patch.set_visible(False)
            ax.grid("off")
            ax.xaxis.set_visible(False)
            ax.yaxis.grid(False)
            
        for ax, angle, label in zip(self.axes, self.angles, labels):
            l, text = ax.set_rgrids(np.linspace(0, 1, n_sep), angle=angle, labels=label, fontsize=6)
            ax.spines[["polar", "inner", "end", "start"]].set_visible(False)
            ax.set_ylim(np.round(-1/n_sep, 2), 1)

    def scale_data(self, values, overall_values):
        scaled = []
        for i in range(len(values)):
            min, max = np.min(overall_values[i]), np.max(overall_values[i])
            scaled.append((values[i]-min)/(max-min))
        return scaled

    def plot(self, values, overall_values, *args, **kw):
        values = self.scale_data(values, overall_values)
        angle = np.deg2rad(np.r_[self.angles, self.angles[0]])
        values = np.r_[values, values[0]]
        self.ax.plot(angle, values, *args, **kw)
        
    def fill(self, values, overall_values, *args, **kw):
        values = self.scale_data(values, overall_values)
        angle = np.deg2rad(np.r_[self.angles, self.angles[0]])
        values = np.r_[values, values[0]]
        self.ax.fill(angle, values, *args, **kw)