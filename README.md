# Spring 2022 Bass Connections Code Files - Akhil & Jasmine
## Python scripts for voxel-based analyses and R scripts for running statistical tests. 

### mouseinfo_latest.R --> latest R script for conducting region-based statistical analyses on 5xFAD/WT mouse dataset

Necessary Files to Run This Program: 
- MouseInfo2.xlsx: contains the info for MRI dataset, with proportional brain volumes of the mice, sorted by genotype, treatment, and timepoint. 

The general methodology undertaken by this region-based statistical analysis script is as follows: 

Retrieve dataset with proportional brain volumes of all the mice in the study. Omit the columns of data that are not wanted/not needed for analysis. Initialize matrices for p-values and significant regions with the appropriate sizes. Perform a two-way repeated measures ANOVA within a loop to go through all 332 brain regions. The ANOVA should take into account genotype and treatment, within timepoint. The resultant p-values are then loaded into the matrix defined earlier for the regions with statistically significant results and have an FDR correction performed on them. Next, Tukey HSD post-hoc testing is performed to obtain specific comparisons within the treatment and genotype that are statistically significant. These p-values are also loaded into a table, so that the comparisons with statistically significant results can be visualized. 

Instructions for Code Usage: 
- Ensure that the mouseinfo_latest.R file and the MouseInfo2.xlsx files are located within the same folder on the computer. 
- Run the script line-by-line to ensure that the files load and initialize properly. 
- Any time a new file is defined in the variable explorer, be sure to inspect its contents to ensure it contains what is wanted. 



### secondleveladapt_latest.py --> latest Python script for conducting voxel-based analyses on 5xFAD/WT mouse dataset

Necessary Files to Run this Program: 
- MouseInfo.xlsx: contains the info for the MRI dataset, with proportional brain volumes of the mice, sorted by genotype, treatment, and timepoint. 
- MDT_mask.nii.gz: contains the mask for the mouse brains, used for plotting the statistical parametric map. 

The general methodology undertaken by the second-level analysis script is as follows: 

Retrieve dataset with variables and image filenames in a dataframe. Obtain the desired mask to be used for the images. Resample the images so their resolution matches that of the mask. Create a design matrix with rows corresponding to each mouse, with columns for their corresponding genotypes, treatments, and/or timepoints. Fit and calibrate the data in the images and the design matrix with the second-level general linear model (GLM). Compute second-level contrast for each of the variables of interest and obtain a statistical map showing the relationship between the variable and the grey matter density in the different regions of the brain. Generate a threshold for the second-level analysis using an FDR-corrected p-value, which is then translated into a z-scale threshold. Plot the statistical map that displays the effect sizes in various regions of the mouse brains, which is thresholded at the prescribed cluster and voxel levels. A report is generated with relevant statistical maps, contrast plots, and cluster tables.

Instructions for Code Usage: 
- Ensure that the secondleveladapt_latest.py and the MouseInfo.xlsx files are located within the same folder on the computer. 
- Adjust the treatment_subset, genotype_subset, and intercept_subset variables to obtain the desired amount of mouse data to make comparisons. If utilizing the entire dataset, simply comment out these variables and use the variables treatment, genotype, and intercept in their place. Be sure to make these changes in the design_matrix variable as well or errors will result. 
- For the significance level, adjust the alpha variable to obtain the desired significance level (default is 0.05). The FDR-corrected threshold is also contained in the threshold variable, but this can be manually adjusted as well. 

