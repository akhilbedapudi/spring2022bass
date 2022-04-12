"""Voxel-Based Morphometry on Oasis dataset
========================================

This example uses Voxel-Based Morphometry (VBM) to study the relationship
between aging, sex and gray matter density.

The data come from the `OASIS <http://www.oasis-brains.org/>`_ project.
If you use it, you need to agree with the data usage agreement available
on the website.

It has been run through a standard VBM pipeline (using SPM8 and
NewSegment) to create VBM maps, which we study here.

VBM analysis of aging
---------------------

We run a standard GLM analysis to study the association between age
and gray matter density from the VBM data. We use only 100 subjects
from the OASIS dataset to limit the memory usage.

Note that more power would be obtained from using a larger sample of subjects.

THIS IS THE ONE YOURE WORKING ON 
"""
# Authors: Bertrand Thirion, <bertrand.thirion@inria.fr>, July 2018
#          Elvis Dhomatob, <elvis.dohmatob@inria.fr>, Apr. 2014
#          Virgile Fritsch, <virgile.fritsch@inria.fr>, Apr 2014
#          Gael Varoquaux, Apr 2014


from bunch import bunchify

############################################################################
# Load Oasis dataset
# ------------------
import numpy as np
import gzip 
import os, glob
import pandas as pd
import itertools
from nilearn.input_data import NiftiMasker
from nilearn.image import get_data
import matplotlib.pyplot as plt
import sklearn
from nilearn import plotting
from PIL import Image as img
import nibabel as nib

mouse_images = []
mouse_images_folder = ['/Users/AkhilBedapudi/Desktop/Bass_Independent_Study/All_Images/AD5x/reg_images/', '/Users/AkhilBedapudi/Desktop/Bass_Independent_Study/All_Images/AD5x/reg_images/']
mifl =list(itertools.chain.from_iterable(itertools.repeat(mouse_images_folder, 102)))
fileextension = ['_T2_to_MDT.nii.gz', '_T2_to_MDT.nii.gz']
fileextension204 = list(itertools.chain.from_iterable(itertools.repeat(fileextension, 102)))
excel_path = '/Users/AkhilBedapudi/Desktop/Bass_Independent_Study/MouseInfo.xlsx'
mouse_database = pd.read_excel(excel_path)
mouse_database = mouse_database[4:80:3]
#timepointstring = ['1', '2', '3','1', '2', '3','1', '2', '3', '1', '2', '3', '1', '2', '3', '1', '2', '3', '1', '2', '3', '1', '2', '3', '1', '2', '3', '1', '2', '3', '1', '2', '3', '1', '2', '3', '1', '2', '3', '1', '2', '3', '1', '2', '3', '1', '2', '3', '1', '2', '3', '1', '2', '3', '1', '2', '3', '1', '2', '3' ,'1', '2', '3','1', '2', '3','1', '2', '3', '1', '2', '3', '1', '2', '3', '1', '2', '3', '1', '2', '3', '1', '2', '3', '1', '2', '3', '1', '2', '3', '1', '2', '3', '1', '2', '3', '1', '2', '3', '1', '2', '3', '1', '2', '3', '1', '2', '3', '1', '2', '3', '1', '2', '3', '1', '2', '3', '1', '2', '3' , '1', '2', '3', '1', '2', '3','1', '2', '3','1', '2', '3','1', '2', '3','1', '2', '3','1', '2', '3','1', '2', '3','1', '2', '3','1', '2', '3','1', '2', '3', '1', '2', '3', '1', '2', '3', '1', '2', '3', '1', '2', '3', '1', '2', '3', '1', '2', '3', '1', '2', '3', '1', '2', '3', '1', '2', '3', '1', '2', '3', '1', '2', '3', '1', '2', '3', '1', '2', '3', '1', '2', '3', '1', '2', '3', '1', '2', '3', '1', '2', '3' ]
timepointstring = list(itertools.chain.from_iterable(itertools.repeat('2', len(mouse_database.index))))
mouse_names = list(mouse_database.Mouse)
mouse_names = mouse_names[4:80:3]
mouse_paths = []
filepathmousenames = [''.join(z) for z in zip(mifl, mouse_names)]
filepathtimepoints = [''.join(z) for z in zip(filepathmousenames, timepointstring)]
fullfilepaths = [''.join(z) for z in zip(filepathtimepoints,fileextension204)]
gray_matter_map_filenames = fullfilepaths


# from nilearn import datasets #this is the issue
# mouse_dataset = datasets.x(
#     n_subjects=n_subjects
# )
#gray_matter_map_filenames = gm_maps_masked
mouse_database['TreatmentNum'] = mouse_database['Treatment']
for j in range(0,len(np.unique(mouse_database['Treatment']))):
    a = mouse_database['Treatment'] == sorted(np.unique(mouse_database['Treatment']))[j] #0 is iron, 1 is LPS, 2 is LPS+Iron, 3 is Saline
    mouse_database['TreatmentNum'][a] = j

mouse_database['GenotypeNum'] = mouse_database['Genotype']
for k in range(0,len(np.unique(mouse_database['Genotype']))):
    b = mouse_database['Genotype'] == sorted(np.unique(mouse_database['Genotype']))[k] #0 is 5xFAD, 1 is WT
    mouse_database['GenotypeNum'][b] = k
            
treatment = mouse_database['TreatmentNum'].astype(float)
#treatment_subset = treatment[4:80:3]
#treatment = mouse_database[4]

###############################################################################
# Sex is encoded as 'M' or 'F'. Hence, we make it a binary variable.
#genotype = mouse_database['Genotype'] == b'F'
#genotype[102:504] = bool(123)
genotype = mouse_database['GenotypeNum'].astype(float)
#genotype_subset = genotype[4:80:3]


#genotypestring = genotype.to_string()
#genotypesort = genotype.iloc[0:503:3]

###############################################################################
# Print basic information on the dataset.
print('First gray-matter anatomy image (3D) is located at: %s' %
      gray_matter_map_filenames[0])  # 3D data

###############################################################################
# Get a mask image: A mask of the  cortex of the ICBM template.
gm_mask = nib.load('/Users/AkhilBedapudi/Desktop/Bass_Independent_Study/All_Images/AD5x/median_images/MDT_mask.nii.gz')

###############################################################################
# Resample the images, since this mask has a different resolution.
from nilearn.image import resample_to_img
mask_img = resample_to_img(
    gm_mask, gray_matter_map_filenames[0], interpolation='nearest')


#############################################################################
# Analyse data
# ------------
#
# First, we create an adequate design matrix with three columns: 'age',
# 'sex', 'intercept'.
import pandas as pd
import numpy as np
n_subjects = len(mouse_database) # more subjects requires more memory
intercept = np.ones(n_subjects)
intercept_subset = intercept[4:80:3]
design_matrix = pd.DataFrame(np.vstack((treatment_subset, genotype_subset, intercept_subset)).T, columns=['treatment', 'genotype', 'intercept'])

#############################################################################
# Let's plot the design matrix.
from nilearn.plotting import plot_design_matrix

ax = plot_design_matrix(design_matrix)
ax.set_title('Second level design matrix', fontsize=12)
ax.set_ylabel('maps')

##########################################################################
# Next, we specify and fit the second-level model when loading the data and
# also smooth a little bit to improve statistical behavior.

from nilearn.glm.second_level import SecondLevelModel
second_level_model = SecondLevelModel(mask_img=mask_img)
second_level_model.fit(gray_matter_map_filenames,
                       design_matrix=design_matrix)

##########################################################################
# Estimating the contrast is very simple. We can just provide the column
# name of the design matrix.
z_map = second_level_model.compute_contrast(second_level_contrast=[1, 0, 0],
                                            output_type='z_score')

###########################################################################
# We threshold the second level contrast at uncorrected p < 0.001 and plot it.
from nilearn import plotting
from nilearn.glm import threshold_stats_img
_, threshold = threshold_stats_img(
    z_map, alpha=.05, height_control='fdr')
print('The FDR=.05-corrected threshold is: %.3g' % threshold)

z_map = second_level_model.compute_contrast(second_level_contrast='treatment',
                                            output_type='z_score')
_, threshold = threshold_stats_img(
     z_map, height_control='fdr', alpha=0.05)
plotting.plot_stat_map(
    z_map, bg_img=mask_img, threshold=threshold, colorbar=True,display_mode='z',
    #cut_coords=[-1, 1, -4],
    title='Treatment effect on grey matter density (FDR = .05)')

###########################################################################
# We can also study the effect of genotype by computing the contrast, thresholding
# it and plot the resulting map.
z_map = second_level_model.compute_contrast(second_level_contrast='genotype',
                                            output_type='z_score')
_, threshold = threshold_stats_img(
     z_map, height_control='fdr', alpha=0.05)
plotting.plot_stat_map(
    z_map, bg_img=mask_img, threshold=2, colorbar=True,display_mode='z',
    #cut_coords=[-1, 1, -4],
    title='Genotype effect on grey matter density (FDR = .05)')

###########################################################################
# Note that there does not seem to be any significant effect of genotype on
# grey matter density on that dataset.

###########################################################################
# Generating a report
# -------------------
# It can be useful to quickly generate a
# portable, ready-to-view report with most of the pertinent information.
# This is easy to do if you have a fitted model and the list of contrasts,
# which we do here.

from nilearn.reporting import make_glm_report

report = make_glm_report(model=second_level_model,
                    contrasts=['treatment', 'genotype'],
                         bg_img = mask_img)

#########################################################################
# We have several ways to access the report:

# report  # This report can be viewed in a notebook
report.save_as_html('report.html')
report.open_in_browser()
