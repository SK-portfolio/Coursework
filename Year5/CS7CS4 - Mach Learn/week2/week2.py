import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
file = pd.read_csv('week2.csv', header=None)
X1 = file.iloc[:,0] #select all rows in col1
X2 = file.iloc[:,1] #col2
y = file.iloc[:, 2] #col3
'''-------------------------a(i-iii)------------------------'''
#logistic regression model
from sklearn.linear_model import LogisticRegression
Xtrain = file.iloc[:,0:2] #col1&2
model = LogisticRegression().fit(Xtrain, y)
y_pred = model.predict(Xtrain)
print("Intercept (θ0):", model.intercept_)
print("Coeffs (θ1, θ2):", model.coef_)
#print("(θ1, θ2): (", model.coef_[0,0], ", ", model.coef_[0,1], ")")
theta0 = model.intercept_[0]
theta1, theta2 = model.coef_[0]

#param vals for decision boundary
x1_vals = np.linspace(Xtrain.iloc[:,0].min(), Xtrain.iloc[:,0].max(), 100)
x2_vals = -(theta0 + theta1 * x1_vals) / theta2

#plot
plt.figure(figsize=(7,7))
    #training data
plt.scatter(X1[y == 1], X2[y == 1], s=40, marker='o', color='b', label='Class +1')
plt.scatter(X1[y == -1], X2[y == -1], s=40, marker='o', color='r', label='Class -1')
    #predictions
plt.scatter(Xtrain[y_pred==1].iloc[:,0], Xtrain[y_pred==1].iloc[:,1],  marker='+', color='y', label='Predicted +1')
plt.scatter(Xtrain[y_pred==-1].iloc[:,0], Xtrain[y_pred==-1].iloc[:,1], s=12.5, marker='x', color='k', label='Predicted -1')
    #dec boundary
plt.plot(x1_vals, x2_vals, 'k--', label='Decision boundary')
    #lables & legend 
plt.xlabel('Feature 1 (X1)')
plt.ylabel('Feature 2 (X2)')
plt.title('2D Feature Value Scatter Plot')
plt.legend(title="Target Class", loc = 'upper right', bbox_to_anchor=(1.20, 1))

plt.tight_layout()
plt.show()

'''-------------------------b(i-iii)------------------------'''
#SVC
from sklearn.svm import LinearSVC
C_values = [0.001, 0.01, 0.1, 1, 10, 100, 1000]

#subplot grid (7 plots, 3x3 grid)
fig, axes = plt.subplots(3, 3, figsize=(9, 9))
axes = axes.ravel()  #flatten to index with [i]

    #logistic regression accuracy b(iv)
log_acc = model.score(Xtrain, y)
print("Logistic Regression Training Accuracy:", log_acc)

#SVM plot per C loop
for i, C in enumerate(C_values):
    svm_model = LinearSVC(C=C, max_iter=10000).fit(Xtrain, y)
    svm_y_pred = svm_model.predict(Xtrain)
    
        #SVM accuracies across C values (b(iv))
    svm_acc = svm_model.score(Xtrain, y)
    print(f"SVM Training Accuracy (C={C}): {svm_acc}")
    
    #print(f"\nC = {C}")
    #print("Intercept (θ0):", svm_model.intercept_)
    #print("Coeffs (θ1, θ2):", svm_model.coef_)
    svm_theta0 = svm_model.intercept_[0]
    svm_theta1, svm_theta2 = svm_model.coef_[0]
        #param vals for SVM Decision boundary
    x1_vals = np.linspace(Xtrain.iloc[:,0].min(), Xtrain.iloc[:,0].max(), 100)
    x2_vals = -(svm_theta0 + svm_theta1 * x1_vals) / svm_theta2

    #subplots
    ax = axes[i]
        #training data
    ax.scatter(X1[y == 1], X2[y == 1], s=15, marker='o', color='b', label='Class +1')
    ax.scatter(X1[y == -1], X2[y == -1], s=15, marker='o', color='r', label='Class -1')
        #predictions
    ax.scatter(Xtrain[svm_y_pred == 1].iloc[:,0], Xtrain[svm_y_pred == 1].iloc[:,1], 
               marker='+', color='y', label='Predicted +1')
    ax.scatter(Xtrain[svm_y_pred == -1].iloc[:,0], Xtrain[svm_y_pred == -1].iloc[:,1], 
               s=7.5, marker='x', color='k', label='Predicted -1')
        #dec boundary
    ax.plot(x1_vals, x2_vals, 'c-', linewidth = 3.5, label='Decision boundary')
        #lables
    ax.set_xlabel('X1')
    ax.set_ylabel('X2')
    ax.set_title(f'SVM, C = {C}')
        #legend added to the last subplot only
    if i == len(C_values) - 1:
        ax.legend(title="Classes & Predictions", loc='lower right',  bbox_to_anchor=(1.65, 0))

#hide unused subplots (since only use 7/9)
for j in range(len(C_values), len(axes)):
    fig.delaxes(axes[j])

plt.tight_layout()
plt.show()

'''-------------------------c(i-iv)------------------------'''
#poly features
X1_sq = X1**2
X2_sq = X2**2

#combine feats & poly feats into 4 column matrix
X_poly = np.column_stack((X1, X2, X1_sq, X2_sq))

#quadratic logistic regression model
model_poly = LogisticRegression().fit(X_poly, y)
y_poly_pred = model_poly.predict(X_poly)

#parameters
theta0_poly = model_poly.intercept_[0]
theta_poly = model_poly.coef_[0]

print("Logistic Regression with Quadratic Features")
print("Intercept (θ0):", theta0_poly)
print("Coefficients (θ1, θ2, θ3, θ4):", theta_poly)

#plot
plt.figure(figsize=(7,7))
    #trainning data
plt.scatter(X1[y == 1], X2[y == 1], s=40, marker='o', color='b', label='Class +1')
plt.scatter(X1[y == -1], X2[y == -1], s=40, marker='o', color='r', label='Class -1')
    #predictions
plt.scatter(X1[y_poly_pred == 1], X2[y_poly_pred == 1], marker='+', color='y', label='Predicted +1')
plt.scatter(X1[y_poly_pred == -1], X2[y_poly_pred == -1], s=12.5, marker='x', color='k', label='Predicted -1')

#quadratic logistic regression accuracy
quad_acc = model_poly.score(X_poly, y)
print("Quadratic Logistic Regression Training Accuracy:", quad_acc)
#baseline classifier (predicts most common class in dataset) 
most_common_class = y.mode()[0]
baseline_pred = np.full_like(y, fill_value=most_common_class)
    #since there's no trained model for bsln pred
from sklearn.metrics import accuracy_score
baseline_acc = accuracy_score(baseline_pred, y)
print("Baseline Predictor Accuracy:", baseline_acc)

#quad logistic regression dec boundary(quadratic EQ)

#discriminant (b^2-4ac)
disc = theta_poly[1]**2 - 4*theta_poly[3]*(theta0_poly + theta_poly[0]*x1_vals + theta_poly[2]*x1_vals**2)

#keep only valid discriminants(disc >= 0)
valid = disc >= 0
x1_valid = x1_vals[valid]
disc_valid = np.sqrt(disc[valid])

#(+/-) x2 curves
#x2_pos = (-theta_poly[1] + disc_valid) / (2*theta_poly[3])   #doesn't fit data
x2_neg = (-theta_poly[1] - disc_valid) / (2*theta_poly[3])

#plot
#plt.plot(x1_valid, x2_pos, 'g--', label='Decision boundary')   #doesn't fit data
plt.plot(x1_valid, x2_neg, 'g--', label='Decision boundary')
    #lables & legend
plt.xlabel('Feature 1 (X1)')
plt.ylabel('Feature 2 (X2)')
plt.title('Quadratic Logistic Regression Decision Boundary')
plt.legend(title="Classes & Predictions", loc='upper right', bbox_to_anchor=(1.25, 1))

plt.tight_layout()
plt.show()


