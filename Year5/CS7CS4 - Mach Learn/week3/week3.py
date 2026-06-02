import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

file = pd.read_csv('week3.csv', header=None)
X = file.iloc[:, 0:2].values  #col1(X[0]->feat1)=x-axis, col2(X[1]->feat2)=y-axis,
y = file.iloc[:, 2].values    #col3(X[2]->target(y))=z-axis
'''-------------------------(i)------------------------'''
#--------------------------a--------------------------
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(X[:, 0], X[:, 1], y, marker='o', color='b', label='Training Data')
ax.set_xlabel('Feature 1 (X1)')
ax.set_ylabel('Feature 2 (X2)')
ax.set_zlabel('Target')
ax.set_title('3D Feature Value Scatter Plot')
plt.legend(loc = 'upper right', bbox_to_anchor=(1.20, 1))

plt.show()
#--------------------------b(LassoReg)&c--------------------------
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Lasso
#generate plynom feats to degree 5
poly = PolynomialFeatures(degree=5, include_bias=False)
#fit plynom feats to data
X_poly = poly.fit_transform(X)
feature_names = poly.get_feature_names_out(['x1', 'x2'])

#c#c#c
    #find training range
#print(X.min(axis=0)) [-1, -1]
#print(X.max(axis=0)) [1, 1]
    #make grid range (a bit over train rng)
x1_range = np.linspace(-1.5, 1.5, 50)
x2_range = np.linspace(-1.5, 1.5, 50)

    #create grid
    #couldn't get nested loops to work properly, used meshgrid() instead
x1_grid, x2_grid = np.meshgrid(x1_range, x2_range) 
Xtest = np.c_[x1_grid.ravel(), x2_grid.ravel()]  # shape (2500, 2)
#c#c#c

#regStrenght(C) and alpha values
C_values = [0.1, 1, 10, 100, 1000]
alphas = [1 / (2 * C) for C in C_values]

fig = plt.figure(figsize=(14, 8))

#to record results
results_lasso = []

for i, (C, alpha) in enumerate(zip(C_values, alphas)):
    #train lasso
    model = Lasso(alpha=alpha, max_iter=10000)
    model.fit(X_poly, y)
    results_lasso.append({
        'C': C,
        'Intercept': model.intercept_,
        **dict(zip(feature_names, model.coef_))
    })
    #predict on grid
    Xtest_poly = poly.transform(Xtest)
    y_pred = model.predict(Xtest_poly)
    #reshape to grid
    y_pred_grid = y_pred.reshape(x1_grid.shape)
    
    #plot
    ax = fig.add_subplot(2, 3, i + 1, projection='3d')
        #pred surface
    ax.plot_surface(x1_grid, x2_grid, y_pred_grid, cmap='viridis', alpha=0.7, label='Lasso Prediction')
        #training data
    ax.scatter(X[:, 0], X[:, 1], y, color='r', label='Training data')
        #legend&labels
    ax.set_title(f'Lasso Regression (C={C})')
    ax.set_xlabel('x1'); ax.set_ylabel('x2'); ax.set_zlabel('y')
    if i == len(C_values) - 1:
        ax.legend(loc = 'upper right', bbox_to_anchor=(1.75, 1))

plt.tight_layout()
plt.show()

#convert to csv
df_lasso = pd.DataFrame(results_lasso).round(4)
df_lasso.to_csv('lasso_poly.csv')
pd.set_option('display.max_columns', None)
print(df_lasso)

#--------------------------e(RidgeReg)--------------------------
from sklearn.linear_model import Ridge
results_ridge = []
fig = plt.figure(figsize=(12, 6))

for i, (C, alpha) in enumerate(zip(C_values, alphas)):
    #train ridge
    model = Ridge(alpha=alpha, max_iter=10000)
    model.fit(X_poly, y)
    results_ridge.append({
        'C': C,
        'Intercept': model.intercept_,
        **dict(zip(feature_names, model.coef_))
    })
    #predict on grid
    Xtest_poly = poly.transform(Xtest)
    y_pred = model.predict(Xtest_poly)
    #reshape to grid
    y_pred_grid = y_pred.reshape(x1_grid.shape)
    
    #plot
    ax = fig.add_subplot(2, 3, i + 1, projection='3d')
        #pred surface
    ax.plot_surface(x1_grid, x2_grid, y_pred_grid, cmap='viridis', alpha=0.7, label='Ridge Prediction')
        #training data
    ax.scatter(X[:, 0], X[:, 1], y, color='r', label='Training data')
        #legend&labels
    ax.set_title(f'Ridge Regression (C={C})')
    ax.set_xlabel('x1'); ax.set_ylabel('x2'); ax.set_zlabel('y')
    if i == len(C_values)-1:
        ax.legend(loc='upper right', bbox_to_anchor=(1.75, 1))

plt.tight_layout()
plt.show()

#convert to csv
df_ridge = pd.DataFrame(results_ridge).round(4)
df_ridge.to_csv('ridge_poly.csv')
pd.set_option('display.max_columns', None)
print(df_ridge)

'''-------------------------(ii)------------------------'''
#--------------------------a(Lasso)--------------------------
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error, make_scorer

C_values = [0.01, 0.1, 1, 10, 100, 1000, 10000]
#alpha(lasso) = 1 / (2C)
alphas = [1 / (2 * C) for C in C_values]

results_5FCV = []
mean_errors = []
std_errors = []

for C, alpha in zip(C_values, alphas):
    #train lasso
    model = Lasso(alpha=alpha, max_iter=10000)
    #since cross_val_score negates values
    scores = cross_val_score(model, X_poly, y, cv=5, scoring='neg_mean_squared_error')
    #convert to positive
    mse_scores = -scores
    #record mse&std.dev
    mean_errors.append(mse_scores.mean())
    std_errors.append(mse_scores.std())
    results_5FCV.append({
        "C": C,
        "Alpha": alpha,
        "Mean_MSE": mse_scores.mean(),
        "Std_MSE": mse_scores.std()
    })

#convert to csv
cv_Lasso = pd.DataFrame(results_5FCV)
cv_Lasso.to_csv('5FCV_Lasso.csv')
print(cv_Lasso)

#plot
plt.figure(figsize=(8,5))
    #for std.dev of mse
plt.errorbar(C_values, mean_errors, yerr=std_errors, fmt='-o', capsize=4)
    #labels
plt.xscale('log')
plt.xlabel('C (Regularisation Strength)')
plt.ylabel('Mean Squared Error ± Std.Deviation')
plt.title('5-fold Cross-Validation Error - Lasso Regression')

plt.grid(True)
plt.show()

#--------------------------c(Ridge)--------------------------

rdgResults_5FCV = []
rdgMean_errors = []
rdgStd_errors = []

#C vals already init(^)
#alpha(ridge) = 1 / (2C)
alphas = [1 / C for C in C_values]
for C, alpha in zip(C_values, alphas):
    #train ridge
    model = Ridge(alpha=alpha)
    #since cross_val_score negates values
    scores = cross_val_score(model, X_poly, y, cv=5, scoring='neg_mean_squared_error')
    #convert to positive
    mse_scores = -scores
    #record mse&std.dev
    rdgMean_errors.append(mse_scores.mean())
    rdgStd_errors.append(mse_scores.std())
    rdgResults_5FCV.append({
        "C": C,
        "Alpha": alpha,
        "Mean_MSE": mse_scores.mean(),
        "Std_MSE": mse_scores.std()
    })
#convert to csv
cv_Ridge = pd.DataFrame(rdgResults_5FCV)
cv_Ridge.to_csv('5FCV_Ridge.csv')
print(cv_Ridge)

#plot
plt.figure(figsize=(8,5))
    #for std.dev of mse
plt.errorbar(C_values, rdgMean_errors, yerr=rdgStd_errors, fmt='-o', capsize=4)
    #labels
plt.xscale('log')
plt.xlabel('C (Regularisation Strength)')
plt.ylabel('Mean Squared Error ± Std.Deviation')
plt.title('5-fold Cross-Validation Error - Ridge Regression')

plt.grid(True)
plt.show()
