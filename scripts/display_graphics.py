# Graphics for Exploratory Analysis Script
# ==============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# ^^^ pyforest auto-imports - don't write above this line
# ==============================================================================
# Auto Import Dependencies
# ==============================================================================
# pyforest imports dependencies according to use in the notebook
# ==============================================================================

# Dependencies not Included in Auto Import*
# ==============================================================================
import matplotlib.ticker as ticker

# Disribution of Target Variable
# ==============================================================================

def Target_Distribution(df, target):

    
    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(15, 10))
    sns.distplot(
        df[target],
        hist    = False,
        rug     = True,
        color   = "navy",
        kde_kws = {'shade': True, 'linewidth': 1},
        ax      = axes[0]
    )
    axes[0].set_title("Original layout", fontsize = 'medium')
    axes[0].set_xlabel(f'{target}', fontsize='small') 
    axes[0].tick_params(labelsize = 6)

    sns.distplot(
        np.sqrt(df[target]),
        hist    = False,
        rug     = True,
        color   = "purple",
        kde_kws = {'shade': True, 'linewidth': 1},
        ax      = axes[1]
    )
    axes[1].set_title("Square root transformation", fontsize = 'medium')
    axes[1].set_xlabel(f'sqrt(var)', fontsize='small') 
    axes[1].tick_params(labelsize = 6)

    """sns.distplot(
        np.log(df[target]),
        hist    = False,
        rug     = True,
        color   = "coral",
        kde_kws = {'shade': True, 'linewidth': 1},
        ax      = axes[2]
    )
    axes[2].set_title("Logarithmic transformation", fontsize = 'medium')
    axes[2].set_xlabel(f'log({target})', fontsize='small') 
    axes[2].tick_params(labelsize = 6)
"""
    fig.suptitle(f'Distribution of the {target} Variable', fontsize = 30, fontweight = "bold")
    fig.tight_layout()
    plt.savefig(f"../reports/figures/{target}_Distribution_Variable.png")


# Distribution graph for each numerical variable
# ==============================================================================
# Adjust number of subplots based on the number of columns

def Numerical_Distribution(df, var, name, cols, rows):

    fig, axes = plt.subplots(ncols=cols, nrows=rows, figsize=(cols*5, rows*5))
    axes = axes.flat
    columnas_numeric = df.select_dtypes(include=['float64', 'int']).columns
    columnas_numeric = columnas_numeric.drop(f'{var}')

    for i, colum in enumerate(columnas_numeric):
        sns.histplot(
            data    = df,
            x       = colum,
            stat    = "count",
            kde     = True,
            color   = (list(plt.rcParams['axes.prop_cycle'])*2)[i]["color"],
            line_kws= {'linewidth': 2},
            alpha   = 0.3,
            ax      = axes[i]
        )
        axes[i].set_title(colum, fontsize = 16, fontweight = "bold")
        axes[i].tick_params(labelsize = 16)
        axes[i].set_xlabel("")
    
    
    fig.tight_layout()
    plt.subplots_adjust(top = 0.9)
    fig.suptitle(f'Distribution Numerical Variable {name}' , fontsize = cols*4, fontweight = "bold")
    plt.savefig(f'../reports/figures/Distribution_Numerical_Variable_{name}.png')


# Correlation & Distribution graph for each numerical variable
# ==============================================================================
# Adjust number of subplots based on the number of columns

def Numerical_Correlation(df, target, drop ,cols, rows):
    fig, axes = plt.subplots(ncols=cols, nrows=rows,  figsize=(cols*5, rows*5))
    axes = axes.flat
    columnas_numeric = df.select_dtypes(include=['float64', 'int']).columns
    columnas_numeric = columnas_numeric.drop(drop)

    for i, colum in enumerate(columnas_numeric):
        sns.regplot(
            x           = df[colum],
            y           = df[target],
            color       = "navy",
            marker      = '.',
            scatter_kws = {"alpha":0.4},
            line_kws    = {"color":"r","alpha":0.7},
            ax          = axes[i]
        )
        axes[i].set_title(f"{target} vs {colum}", fontsize = 16, fontweight = "bold")
        #axes[i].ticklabel_format(style='sci', scilimits=(-4,4), axis='both')
        axes[i].yaxis.set_major_formatter(ticker.EngFormatter())
        axes[i].xaxis.set_major_formatter(ticker.EngFormatter())
        axes[i].tick_params(labelsize = 16)
        axes[i].set_xlabel("")
        axes[i].set_ylabel("")

        #if (i-1 >= len(columnas_numeric)-1): break

    # Empty axes are removed
    """for i in [8]:
            fig.delaxes(axes[i])"""
    
    fig.tight_layout()
    plt.subplots_adjust(top=0.9)
    fig.suptitle(f'Correlation with {target}', fontsize = cols*4, fontweight = "bold")
    plt.savefig(f"../reports/figures/Correlation_Each_Numerical_Variable_with_{target}.png")

# Correlation between numeric columns
# ==============================================================================

def tidy_corr_matrix(df):
    
    # Function to convert a pandas correlation matrix to tidy format
    #df.drop(drop)

    corr_mat = df.select_dtypes(include=['float64', 'int']).corr(method='pearson')
    corr_mat = corr_mat.stack().reset_index()
    corr_mat.columns = ['variable_1','variable_2','r']
    corr_mat = corr_mat.loc[corr_mat['variable_1'] != corr_mat['variable_2'], :]
    corr_mat['abs_r'] = np.abs(corr_mat['r'])
    corr_mat = corr_mat.sort_values('abs_r', ascending=False)
    
    return corr_mat

# Heatmap matrix of correlations
# ==============================================================================

def heat_map(df, name):

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 15))
    
    #df.drop(drop)
    
    corr= df.select_dtypes(include=['float64', 'int']).corr(method='pearson').corr()

    # Getting the Upper Triangle of the co-relation matrix

    matrix = np.triu(corr)

    # using the upper triangle matrix as mask 
    sns.heatmap(corr, 
            annot=True, 
            mask=matrix, 
            cmap=sns.diverging_palette(150, 275, s=80, l=55, n=9),
            annot_kws = {"size": 10})

    ax.set_xticklabels(
        ax.get_xticklabels(),
        rotation = 45,
        horizontalalignment = 'right',
    )
    ax.set_yticklabels(
    ax.get_yticklabels(),
    rotation = 0,
    horizontalalignment = 'right',
    )
    ax.tick_params(labelsize = 15)

    fig.suptitle(f'Heatmap Correlation Matrix {name}', fontsize = 30, fontweight = "bold")
    plt.savefig(f"../reports/figures/Heatmap_Matrix_Correlations_{name}.png")
    

# Graph for each qualitative variable
# ==============================================================================
# Adjust number of subplots based on the number of columns

def Qualitative_Distribution(df, name, rows, cols):

    fig, axes = plt.subplots(nrows=rows, ncols=cols, figsize=(rows*10, rows*50))
    axes = axes.flat
    columnas_object = df.select_dtypes(include=['object']).columns

    for i, colum in enumerate(columnas_object):
        df[colum].value_counts().plot.barh(ax = axes[i])
        axes[i].set_title(colum, fontsize = 16, fontweight = "bold")
        axes[i].tick_params(labelsize = 11)
        axes[i].set_xlabel("")

    # Empty axes are removed
    #for i in [7, 8]:
        #fig.delaxes(axes[i])
    
    fig.tight_layout()
    plt.subplots_adjust(top=0.9)
    fig.suptitle(f'Qualitative variable distribution {name}',
             fontsize = 30, fontweight = "bold")
    plt.savefig(f"../reports/figures/Each_Qualtitative_Variable_{name}.png")
    

# Graph relationship between the Target and each qualitative variables
# ==============================================================================
# Adjust number of subplots based on the number of columns

def Qualitative_Relationship(df, var, rows, cols):

    fig, axes = plt.subplots(nrows=rows, ncols=cols, figsize=(100, 60))
    axes = axes.flat
    columnas_object = df.select_dtypes(include=['object']).columns

    for i, colum in enumerate(columnas_object):
        sns.violinplot(
            x     = colum,
            y     = var,
            data  = df,
            color = "coral",
            ax    = axes[i]
        )
        axes[i].set_title(f"{colum} vs {var}", fontsize = 30, fontweight = "bold")
        axes[i].yaxis.set_major_formatter(ticker.EngFormatter())
        axes[i].tick_params(labelsize = 22)
        axes[i].set_xticklabels(axes[i].get_xticklabels(),rotation = 45, horizontalalignment = 'right')
        axes[i].set_xlabel("")
        axes[i].set_ylabel("")
    
    # Empty axes are removed
    #for i in [7, 8]:
        #fig.delaxes(axes[i])

    fig.tight_layout()
    plt.subplots_adjust(top=0.9)
    fig.suptitle(f'{var} distribution by group', fontsize = 60, fontweight = "bold")
    plt.savefig(f"../reports/figures/Target_vs_Qualitative_Variable_{var}.png")
    

# Graph adjusted intertia BestK for KMeans
# ==============================================================================
def inertia(results):

    # plot the results
    plt.figure(figsize=(14,8))
    plt.plot(results,'-o')
    plt.title('Adjusted Inertia for each K')
    plt.xlabel('K')
    plt.ylabel('Adjusted Inertia')
    plt.xticks(range(2,len(results),1))
    plt.savefig("../../reports/figures/BestK_for_KMeans.png");
    
# Graph PCA
# ==============================================================================
def pca(pca):
    PC = range(1, pca.n_components_+1)
    
    plt.figure(figsize=(12,6))
    plt.bar(PC, pca.explained_variance_ratio_, color=('navy','b','g','r','coral','c','m','y','k','gray'))
    plt.xlabel('Principal Components')
    plt.ylabel('Variance %')
    plt.title('Principal Components Variance')
    plt.xticks(PC);
    plt.savefig(f"../../reports/figures/Principal_Components{pca.n_components}.png");