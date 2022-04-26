# Spring 2022 Bass Connections Code Files - Akhil & Jasmine
## Python scripts for voxel-based analyses and R scripts for running statistical tests. 

### mouseinfo_latest.R --> latest R script for conducting region-based statistical analyses on 5xFAD/WT mouse dataset

Necessary Files to Run This Program: 
- MouseInfo2.xlsx: contains the info for MRI dataset, with proportional brain volumes of the mice, sorted by genotype, treatment, and timepoint. 
- 

The general methodology undertaken by this region-based statistical analysis script is as follows: 




### secondleveladapt_latest.py --> latest Python script for conducting voxel-based analyses on 5xFAD/WT mouse dataset

Necessary Files to Run this Program: 
- MouseInfo.xlsx: contains the info for the MRI dataset, with proportional brain volumes of the mice, sorted by genotype, treatment, and timepoint. 
- MDT_mask.nii.gz: contains the mask for the mouse brains, used for plotting the statistical parametric map. 
- 

The general methodology undertaken by the second-level analysis script is as follows: 

Retrieve dataset with variables and image filenames in a dataframe. Obtain the desired mask to be used for the images. Resample the images so their resolution matches that of the mask. Create a design matrix with rows corresponding to each mouse, with columns for their corresponding genotypes, treatments, and/or timepoints. Fit and calibrate the data in the images and the design matrix with the second-level general linear model (GLM). Compute second-level contrast for each of the variables of interest and obtain a statistical map showing the relationship between the variable and the grey matter density in the different regions of the brain. Generate a threshold for the second-level analysis using an FDR-corrected p-value, which is then translated into a z-scale threshold. Plot the statistical map that displays the effect sizes in various regions of the mouse brains, which is thresholded at the prescribed cluster and voxel levels. A report is generated with relevant statistical maps, contrast plots, and cluster tables.

Instructions for Code Usage: 
1. 


