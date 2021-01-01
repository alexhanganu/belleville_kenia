# !/usr/bin/env python
# coding: utf-8
# last update: 2020-11-13

'''
Sylvie Study Brain Reserve
'''
project = "brain_reserve"

STEP0_make_groups        = True
STEP1_prep1_fs711_dir    = False # this step was needed temporarily to clean the FS711 folder. Probably not needed anymore
STEP1_prep2_fs_processed = False
STEP3_run_stats          = False

from os import path, system
from bin import nimb_link
NIMB_HOME = nimb_link.link_with_nimb()
from setup.get_vars import Get_Vars, SetProject
all_vars = Get_Vars()
project_vars = all_vars.projects[project]
#nimb_stats = SetProject(all_vars.location_vars['local']['NIMB_PATHS']['NIMB_tmp'], all_vars.stats_vars, project).stats

if STEP0_make_groups:
    from bin.step0_prep4_make_groups import MakeGroupFile
    MakeGroupFile(project_vars)
    #step0_make_groups.make_file_groups()

if STEP1_prep1_fs711_dir:
    from bin import step1_prep1_fs711_dir
    step1_prep1_fs711_dir.CleanFS711Dir(NIMB_HOME, path_derivatives_fs7, path_derivatives_fs7_from6, path2xtrct, path_err)

if STEP1_prep2_fs_processed:
    from bin import step1_prep2_fs_processed
    step1_prep2_fs_processed.LinkIDstoProcessed(project_vars)


if STEP3_run_stats:
    chdir(NIMB_HOME)
    system('python3 nimb.py -process run-stats -project {}'.format(project))


'''
STEPS:
PRE-PROCESSING
(A) Clinical Data Extraction:
a_make_file_data_for_analysis.py:
    1) defining the groups (new script written by me)
    2) extracting the clinical data (education, sex, age, moca)
    3) extracting scanner-based MRI parameters

(B) MRI stats extraction
b_run_nimb_stats.py:
    4) extracting the MRI statistical data (script adjusted by me, but some manual adjustments are still performed)
    6) extracting 3 files (1) Subcort (2) DK, (3) DS for parameters: volumes, thickness, area, folding index
    5) checking the data for consistency, correctitude, missing values (now, one subject is missing the data for one sub-parameter, and for this one the average of the group was taken)
    ERRORS adjusted:
        CA150 missing values for: temporal_transverse_Sulc_ThickStdL_DS. Average per group was taken.
        WM_CA466_RF_T1 has no wmparc.stats, BA.stats, needs redo. Stats in table are the means.
        WM_CA323_DM_T1 frontal_orbitomedial_FoldIndL_DK is 89850850. value is changed to group mean
        WM_CA323_DM_T1 cc_subcallosal_Gyr_FoldIndL_DS is 89850807. value is changed to group mean
    MATLAB - LinAdj:
        6) correction with eTIV for subcortical and cortical volumes (matlab script, not automatized in the main pipeline yet)

TO DO:
    extract Surface to Area parameter
    extract HipCor parameter


STATISTICAL ANALYSIS
(A) FREESURFER: c_run_FreeSurfer_glm.py:
    13) perform Whole-Brain FreeSurfer GLM per group with correlations with variables

(B) GENERAL STATISTICS
    NORMALIZE ? (zscores, QuantileTransformer ?)

ANOVA for volumes
    if significant:
        put in table (avg per group)
        check if comes from th, ar, curv of fold
            if sig put in table, avg per group
do pca
    chk which regions correspond to ANOVA:
        for all
        for bac
        for high_school

for pca regions see how correlate with moca (correlations for pearson/spearman/kendall)

for pca regions do linear regression (do linear regression, check r2)

for pca regions do hierarchical regression by age (dp hierarchical regression (moderation) analysis by age, by group (v1 Asha Dixit, v2 Lynn))

for pca regions do laterality (laterality_analysis.py))



    7) do individual group distribution analysis  (script adjusted by me, some manual adjustments are still performed)

    do PCA, extract feature for threshold (defined in definitions.prediction_defs['pca_threshold'])
    for all
    per group

TO DO:
    for PCA regions:
        compute the average values (Vol, Area, Thick, ThickStd, CurvInd, FoldInd) for all participants
        plot correlation average with MoCA
        plot correlation average with education
        compute the average for each group
        plot the averages of each group


    make image for PCA regions for all and for each group
    do logistic regression, check r2 (using first script but adjusted by me, d_predict_logreg)


    8) do general group-based statistical analysis (using first version of the script written by me)
    9) do anova group-based analysis (using first version of the script, written by me)


    do polynomial regression, chk r2 (https://www.w3schools.com/python/python_ml_polynomial_regression.asp)
    do multiple regression (https://www.w3schools.com/python/python_ml_multiple_regression.asp)
    evaluate interactions via partial correl (stats sig diff determined by bootstrap testing) (Lefort-Besnard 2018

(C) PREDICTION STATISTICS
    14) do prediction analysis SKF and LOO cross validation (script written by me, Asha and Van Tien with input and
verifications from Ethan, d_predict_ml.py, d_predict_step2_make_sig_feat_db.py: (10fold CrossValidation)
    analyze weights assigned by the classifier
    18) create polar-plot for the significant results (script written by Ethan for matlab)  (deadline: december 30, 2020)

MANUSCRIPT
    19) write the results (require adjustments) (deadline: january 1, 2020)
    20) make the tables (require adjustments) (deadline: january 1, 2020)
    21) make the images for the manuscript (will adjust the linear regression and logistic regression images) (deadline: january 2, 2020)
    22) write introduction (written by will add more paragraphs, since results have changed a little bit) (deadline: january 6, 2020)
    23) write discussion (needs more to be written) (deadline: january 10, 2020)

FS QA
Maclaren et al 2014, estimatio of long subcort rois
slope was used to classify pre-HD vs. HC
poster: Eduardo Castro, Guillermo Cecchi, Watson IBM Research Lab, Yorktown NY, USSA;)

KMeans for extracting a middle group - had limitations, method not used. Unclear what information this method could bring to the manuscript.


chk if pca file present, if not -> send pca features to file
read the file to create the working file
send the new file with pca features to logistic regression


pca regions and regions with significant diff are not the same.
extract pca, extrac reg with sig diff between groups.


do PCA for BACC and HS for DK and DS
see regions based on lobes for DK and DS
see if PCA variance is similar in the 2 groups

use PCA to predict group
use PCA to predict education
use PCA to predict group without 15 and 16 years (the middle)

3 direction: DK+Subcort; DS+Subcort; DS+DK+Subcort
analysis: HS vs. Bacc, All, HS, Bacc, HS vs. Bacc without middle ones

PCA for each direction => extract reg with variance => send feat to RF-LOO => predict group, get accuracy => predict ed$extract features, use them for Lin Regression and ANOVA

=> are there regions in DK that would benefit from the DS atlas
=> take those regions and analyse age influence on them
=> regions that explain the variance in the HS group are similar as in the Bacc ?
DK-based PCA results: 32 regions explain the variance in everyone.

LOO - shouldn't nr of iterations be similar to nr of participants ?, i.e. 163

chk the results of the redone DS step1 that showed 82% accuracy, redoing with 100 iterations.

add DecissionTreeClassifier - to show the tree ?

make the image showing the education level and the predicted education using the features ?


# 7 males high school are needed.
loo final results:
=> classify the regions with highest accuracy.
=> find out which participants were not classified based on the criteria
=> depict what is common between participants regarding the criteria depicted for prediction accuracy
=> logistic regression - can this bring any answers ?

'''







'''
OLD VERSION = all was sent to nimb
# TABLES get for stats start ===============================================
df_clin = db_processing.get_df(path.join(paths['materials_DIR'][1], paths['GLM_file_group']),
                                    usecols=[paths['id_col'], paths['group_col'], 'education', 'age', 'moca'],
                                    index_col = paths['id_col'])
groups = preprocessing.get_groups(df_clin, paths['group_col'], groups_all)
df_sub_and_cort, ls_cols_X_atlas = preprocessing.get_df(f_subcort, f_atlas_DK, f_atlas_DS,
                                                         atlas, paths['id_col'])
df_clin_atlas = db_processing.join_dfs(df_clin, df_sub_and_cort, how='outer')
# TABLES get for stats  end ===============================================


# stats = predict.get_stats_df(len(ls_cols_X_atlas), atlas,
#                             prediction_vars['nr_threads'], 
#                             definitions.sys.platform,
#                             time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))

def get_X_data_per_group_all_groups(group):
    # extract X_scaled values for the brain parameters for and use them to extract PCA-based features

    # print('group is: ',group)
    if group == 'all':
        df_clin_group = df_clin
        df_X = df_sub_and_cort
        y_labeled = preprocessing.label_y(df_clin, prediction_vars['target'])
        X_scaled = preprocessing.scale_X(df_X)
    else:
        df_group      = db_processing.get_df_per_parameter(df_clin_atlas, paths['group_col'], group)
        df_clin_group = db_processing.rm_cols_from_df(df_group, ls_cols_X_atlas)
        df_X          = db_processing.rm_cols_from_df(df_group, [i for i in df_group.columns.tolist() if i not in ls_cols_X_atlas])
        y_labeled     = preprocessing.label_y(df_group, prediction_vars['target'])
        X_scaled      = preprocessing.scale_X(df_X)
    return df_X, y_labeled, X_scaled, df_clin_group


# analyses per GROUP and for ALL participants


for group in groups + ['all',]: #'all' stands for all participants
    df_X, y_labeled, X_scaled, df_clin_group = get_X_data_per_group_all_groups(group)
    if feature_algo == 'PCA':# using PCA
        features = predict.get_features_based_on_pca(varia.get_dir(path.join(nimb_stats['STATS_HOME'], nimb_stats['features'])),
                                                    prediction_vars['pca_threshold'],
                                                    X_scaled, ls_cols_X_atlas,
                                                    group, atlas)
    elif feature_algo == 'RFE': # using RFE
        features, features_rfe_and_rank_df = predict.feature_ranking(X_scaled,
                                                                    y_labeled,
                                                                    ls_cols_X_atlas)
        print("number of features extracted by RFE: ",len(features_rfe_and_rank_df.feature))
    # print(features)
    df_with_features = db_processing.get_df_from_df(df_X, usecols = features)
    df_with_features_lhrh = db_processing.get_df_from_df(df_X, usecols = sorted(stats_laterality.RReplace(features).lhrh_list))

    # STEP run Linear Regression Moderation
    if STEP_LinRegModeration:
        linear_regression_moderation.linreg_moderation_results(db_processing.join_dfs(df_clin_group, df_with_features),
                        features, params['group_param'], params['regression_param'],
                        varia.get_dir(path.join(nimb_stats['STATS_HOME'], nimb_stats['linreg_moderation_dir'])),
                        atlas, group)
    if STEP_Laterality:
        stats_laterality.run_laterality(db_processing.join_dfs(df_clin_group, df_with_features_lhrh), paths["group_col"],
                        varia.get_dir(path.join(nimb_stats['STATS_HOME'], nimb_stats['laterality_dir']+'_'+group)))
    if group == 'all':
        # STEP run ANOVA and Simple Linear Regression
        if STEP_Anova_SimpLinReg:
            RUN_GroupAnalysis_ANOVA_SimpleLinearRegression(db_processing.join_dfs(df_clin_group, df_with_features),
                                                            groups,
                                                            params['y'],
                                                            params['other_params'],
                                                            varia.get_dir(path.join(nimb_stats['STATS_HOME'], nimb_stats['anova']+'_'+group)),
                                                            paths['group_col'],
                                                            features)
        # STEP run ANOVA and Simple Logistic Regression
        if STEP_LogisticRegression:
            stats_LogisticRegression.Logistic_Regression(X_scaled, y_labeled, paths['group_col'],
                                                        varia.get_dir(path.join(nimb_stats['STATS_HOME'], nimb_stats['logistic_regression_dir']+'_'+group)))


'''



'''
STEPS:
a_make_file_data_for_analysis.py:
	1) defining the groups (new script written by me)
	2) extracting the clinical data (education, sex, age, moca)
	3) extracting scanner-based MRI parameters
b_run_nimb_stats.py:
	4) extracting the MRI statistical data (script adjusted by me, but some manual adjustments are still performed)
	6) extracting 3 files (1) Subcort (2) DK, (3) DS for parameters: volumes, thickness, area, folding index
	5) checking the data for consistency, correctitude, missing values (now, one subject is missing the data for one sub-parameter, and for this one the average of the group was taken)
	ERRORS adjusted:
		CA150 missing values for: temporal_transverse_Sulc_ThickStdL_DS. Average per group was taken.
		WM_CA466_RF_T1 has no wmparc.stats, BA.stats, needs redo. Stats in table are the means.

		WM_CA323_DM_T1 frontal_orbitomedial_FoldIndL_DK is 89850850. value is changed to group mean
		WM_CA323_DM_T1 cc_subcallosal_Gyr_FoldIndL_DS is 89850807. value is changed to group mean
	MATLAB - LinAdj:
		6) correction with eTIV for subcortical and cortical volumes (matlab script, not automatized in the main pipeline yet)
		
	chk values, error WM_CA323, folding index
	NORMALIZE ? (zsocres, QuantileTransformer ?)
	Surface to Area parameter ?
	HipCor parameter ?
	
c_run_FreeSurfer_glm.py:
	13) perform Whole-Brain FreeSurfer GLM per group with correlations with variables

	7) perform individual group distribution analysis  (script adjusted by me, some manual adjustments are still performed)
	8) do general group-based statistical analysis (using first version of the script written by me)
	9) do anova group-based analysis (using first version of the script, written by me)
	12) do correlations for pearson/spearman/kendall (script written by Lynn)
	evaluate interactions via partial correl (stats sig diff determined by bootstrap testing) (Lefort-Besnard 2018
	10) do linear regresion analysis, on groups (script written by me, first version)
	
	for the regions with 0.94:
		compute the average values (Vol, Area, Thick, ThickStd, CurvInf, FoldInd) for all participants
		plot correlation average with MoCA
		plot correlation average with education
		compute the average for each group
		plot the averages of each group

d_predict_logreg
	11) do logistic regression (using first script but adjusted by me)
d_predict_ml.py, d_predict_step2_make_sig_feat_db.py: (10fold CrossValidation)
	14) do prediction analysis leave-one-out cross validation (script written by me, Asha and Van Tien with input and verifications from Ethan)
	analyze weights assigned by the classifier
e_laterality_analysis.py:
	16) do laterality analysis (initially script written by Ethan ior matlab, re-written by me for python to add to the pipeline)
Lynn R script:
	17) hierarchical regression (moderation) analysis by age, by group (initially, script written by Asha for python, second version by Lynn for SPSS) (deadline: december 30, 2020)
Matlab Ethan:
	18) create polar-plot for the significant results (script written by Ethan for matlab)  (deadline: december 30, 2020)
Manuscript:
	19) write the results (require adjustments) (deadline: january 1, 2020) 
	20) make the tables (require adjustments) (deadline: january 1, 2020)
	21) make the images for the manuscript (will adjust the linear regression and logistic regression images) (deadline: january 2, 2020)
	22) write introduction (written by will add more paragraphs, since results have changed a little bit) (deadline: january 6, 2020)
	23) write discussion (needs more to be written) (deadline: january 10, 2020)

FS QA
Maclaren et al 2014, estimatio of long subcort rois
slope was used to classify pre-HD vs. HC
poster: Eduardo Castro, Guillermo Cecchi, Watson IBM Research Lab, Yorktown NY, USSA;)
'''

