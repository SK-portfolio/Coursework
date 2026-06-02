import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.colors import ListedColormap
from sklearn.model_selection import cross_val_score, KFold

file = pd.read_csv('week4.1.csv', header=None)      #(i) - dataset1
#file = pd.read_csv('week4.2.csv', header=None)     #(ii) - dataset2

X = file.iloc[:, 0:2].values  #col1(X[0]->feat1)=x-axis, col2(X[1]->feat2)=y-axis,
y = file.iloc[:, 2].values    #col3(X[2]->target(y)

#:::(for(a)&(b)):::
    #X vals separated for y predictions
X1 = file.iloc[:,0]
X2 = file.iloc[:,1]
    #5 folds for cross validation
kf = KFold(n_splits=5, shuffle=True, random_state=42)
    #meshgrid for better dec boundary visual
x1_min, x1_max = X1.min() - 0.5, X1.max() + 0.5
x2_min, x2_max = X2.min() - 0.5, X2.max() + 0.5
xx, yy = np.meshgrid(np.linspace(x1_min, x1_max, 400),
                     np.linspace(x2_min, x2_max, 400))
#::::::::::::::::::

#traning data plot
plt.figure(figsize=(6,6))
    #training data
plt.scatter(X[y == 1, 0], X[y == 1, 1], color='blue', edgecolor='k', label='Class +1')
plt.scatter(X[y == -1, 0], X[y == -1, 1], color='red', edgecolor='k', label='Class -1')
    #lables & legend 
plt.xlabel("Feature 1 (X1)")
plt.ylabel("Feature 2 (X2)")
plt.title("Training Data Visualisation")
plt.legend(title="Target Class", loc='upper right', bbox_to_anchor=(1.20, 1))
plt.tight_layout()
plt.show()
    #see count of each train data class(for(c))
print(np.unique(y, return_counts=True))

#'''
#--------------------(a)--------------------
#'''
#---polynomial logistic regression---
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LogisticRegression

degrees = [2, 4, 6]
C_vals = [0.001, 0.01, 0.1, 1, 10, 100, 1000]

mean_scores = np.zeros((len(degrees), len(C_vals)))
std_scores = np.zeros((len(degrees), len(C_vals)))

for i, d in enumerate(degrees):
    poly = PolynomialFeatures(degree=d)
    X_poly = poly.fit_transform(X)

    for j, c in enumerate(C_vals):
            #train log reg
        model = LogisticRegression(C=c, penalty='l2', solver='lbfgs', max_iter=10000)
            #5F cross val
        scores = cross_val_score(model, X_poly, y, cv=kf, scoring='accuracy')
        mean_scores[i, j] = scores.mean()   #cross validation accuracy
        std_scores[i, j] = scores.std()     #accuracy error

#print(mean_scores.round(5))        

fig, axes = plt.subplots(1, 3, figsize=(15, 4), sharey=True)  # 1x3 grid for 3 degree subplots
axes = axes.ravel()  #flatten to index with [i]

for i, d in enumerate(degrees):
    ax = axes[i]
        #for std.dev of cross val accuracy
    ax.errorbar(C_vals, mean_scores[i], yerr=std_scores[i], fmt='-o', capsize=3)
        #labels
    ax.set_xscale('log')
    ax.set_title(f"Degree = [{d}]")
    ax.set_xlabel("C (log scale)")
    ax.set_ylabel("Cross-Validation Accuracy")
    ax.grid(True, linestyle='--', alpha=0.6)
        #find max (best) accuracy for each degree
    best_idx = np.argmax(mean_scores[i])
    print(f"Degree = [{d}]     C = {C_vals[best_idx]}")
    print(f"CV Accuracy: {mean_scores[i, best_idx].round(5)}")
        #use to find+highlight best C val in plot
    ax.scatter(C_vals[best_idx], mean_scores[i, best_idx], color='red', zorder=5, label=f"Best C = {C_vals[best_idx]}")
    ax.legend()

#auto pick best deg & C val out of all plots made
best_deg_idx, best_c_idx = np.unravel_index(np.argmax(mean_scores), mean_scores.shape)
best_degree = degrees[best_deg_idx]
best_C = C_vals[best_c_idx]
print("best degree :", best_degree)
print("best C :", best_C)

plt.suptitle("Cross-Validation Results per Polynomial Degree", y=1.0, fontsize=14)
plt.tight_layout()
plt.show()


#---BEST polynom log reg---
poly = PolynomialFeatures(degree=best_degree)
X_poly = poly.fit_transform(X)
    #train log reg
model = LogisticRegression(C=best_C, penalty='l2', solver='lbfgs', max_iter=10000)
model.fit(X_poly, y)
y_pred = model.predict(X_poly)

#plot
plt.figure(figsize=(7,7))
    #trainning data
plt.scatter(X1[y == 1], X2[y == 1], s=40, marker='o', color='b', zorder=5, label='Class +1')
plt.scatter(X1[y == -1], X2[y == -1], s=40, marker='o', color='r', zorder=5, label='Class -1')
    #predictions
plt.scatter(X1[y_pred == 1], X2[y_pred == 1], marker='+', color='y', zorder=5, label='Predicted +1')
plt.scatter(X1[y_pred == -1], X2[y_pred == -1], s=12.5, marker='x', color='k', zorder=5, label='Predicted -1')
    #prediction regions on meshgrid
Z = model.predict(poly.transform(np.c_[xx.ravel(), yy.ravel()]))
Z = Z.reshape(xx.shape)
    #dec boundary
plt.contourf(xx, yy, Z, alpha=0.3, cmap=ListedColormap(['red', 'blue']))
    #labels&legend
plt.xlabel("Feature 1 (X1)")
plt.ylabel("Feature 2 (X2)")
plt.title(f"Polynomial Logistic Regression Decision Boundary (Degree={best_degree}, C={best_C})")
plt.legend(title="Target Class", loc='upper right', bbox_to_anchor=(1.20, 1))

plt.tight_layout()
plt.show()
#'''
#--------------------(b)--------------------
#'''
#---------kNN---------
from sklearn.neighbors import KNeighborsClassifier

#range of k values to test
k_values = np.arange(1, 45)
#reset acc & err
mean_scores = []
std_scores = []

for k in k_values:
    #train kNN
    knn = KNeighborsClassifier(n_neighbors=k)
    #5F cross val
    scores = cross_val_score(knn, X, y, cv=kf, scoring='accuracy')
    mean_scores.append(scores.mean())
    std_scores.append(scores.std())

mean_scores = np.array(mean_scores)
std_scores = np.array(std_scores)

#print(mean_scores.round(5))
#print(std_scores.round(5))

#plot
plt.figure(figsize=(8,5))
    #for std.dev of cross val accuracy
plt.errorbar(k_values, mean_scores, yerr=std_scores, fmt='-o', capsize=4, zorder=1)
    #lables
plt.xlabel("Number of Neighbors (k)")
plt.ylabel("Cross-Validation Accuracy")
plt.title("kNN Classifier Cross-Validation Performance")
plt.grid(True, linestyle='--', alpha=0.6)
    #find max (best) accuracy for each k val
best_k = k_values[np.argmax(mean_scores)]
print(f"Best k = {best_k}, Mean CV Accuracy = {np.max(mean_scores):.4f}")
    #use to find+highlight best k in plot
plt.scatter(best_k, np.max(mean_scores), color='red', zorder=2, label=f"Best k = {best_k}")
plt.legend()
plt.tight_layout()
plt.show()


#---------BEST kNN---------
    #train kNN
knn_best = KNeighborsClassifier(n_neighbors=best_k).fit(X, y)
y_pred_knn = knn_best.predict(X)
    #prediction regions on meshgrid
Z = knn_best.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

#plot
plt.figure(figsize=(7,7))
    #dec boundary
plt.contourf(xx, yy, Z, alpha=0.3, cmap=ListedColormap(['red', 'blue']))
    #training data
plt.scatter(X[y==1,0], X[y==1,1], color='blue', label='Class +1')
plt.scatter(X[y==-1,0], X[y==-1,1], color='red', label='Class -1')
    #predictions
plt.scatter(X1[y_pred_knn == 1], X2[y_pred_knn == 1], marker='+', color='y', zorder=5, label='Predicted +1')
plt.scatter(X1[y_pred_knn == -1], X2[y_pred_knn == -1], s=12.5, marker='x', color='k', zorder=5, label='Predicted -1')
    #legend&labels
plt.title(f"kNN Decision Boundary (k={best_k})")
plt.xlabel("Feature 1 (X1)")
plt.ylabel("Feature 2 (X2)")
plt.legend(title="Target Class", loc='upper left')

plt.tight_layout()
plt.show()
#'''
#--------------------(c)--------------------
#'''
#------confusion matrix------
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.dummy import DummyClassifier

#polynom Log Reg predictions
y_pred_logreg = model.predict(X_poly)
    #see count of each data class
print(np.unique(y_pred_logreg, return_counts=True))

#kNN predictions
y_pred_knn = knn_best.predict(X)
    #see count of each data class
print(np.unique(y_pred_knn, return_counts=True))

#baseline models
    #most frequent
baseline_mostfreq = DummyClassifier(strategy='most_frequent').fit(X, y)
y_pred_mostfreq = baseline_mostfreq.predict(X)
    #random
baseline_random = DummyClassifier(strategy='uniform', random_state=42).fit(X, y)
y_pred_random = baseline_random.predict(X)

#func to create labeled confusion matrix
def confuseMtrx_df(y_true, y_pred, labels=[1, -1]):
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    return pd.DataFrame(
        cm,
        index=[f"True {l}" for l in labels],
        columns=[f"Pred {l}" for l in labels]
    )

#build+print dataframes
    #plynm log reg
cm_logreg_df = confuseMtrx_df(y, y_pred_logreg)
print("\n--- Confusion Matrix: Logistic Regression ---")
print(cm_logreg_df)
    #kNN
cm_knn_df = confuseMtrx_df(y, y_pred_knn)
print(f"\n--- Confusion Matrix: kNN (k={best_k}) ---")
print(cm_knn_df)
    #freq
cm_mostfreq_df = confuseMtrx_df(y, y_pred_mostfreq)
print("\n--- Confusion Matrix: Baseline (Most Frequent) ---")
print(cm_mostfreq_df)
    #rand
cm_random_df = confuseMtrx_df(y, y_pred_random)
print("\n--- Confusion Matrix: Baseline (Random) ---")
print(cm_random_df)


#'''
#--------------------(d)--------------------
#'''
#------ROC Curve------
from sklearn.metrics import roc_curve, auc
# plynm log reg probs
    #(.predict(...)-> get class prediction|||.predict_proba(...) -> get prob value)
y_score_logreg = model.predict_proba(X_poly)[:, 1]

# kNN probs
y_score_knn = knn_best.predict_proba(X)[:, 1]

# baseln probs
y_score_mostfreq = baseline_mostfreq.predict_proba(X)[:, 1]
y_score_random = baseline_random.predict_proba(X)[:, 1]

#get false pos & true pos rates - logreg
fpr_logreg, tpr_logreg, _ = roc_curve(y, y_score_logreg, pos_label=1)
    #use to find AUC
roc_auc_logreg = auc(fpr_logreg, tpr_logreg)

#get false pos & true pos rates - kNN
fpr_knn, tpr_knn, _ = roc_curve(y, y_score_knn, pos_label=1)
roc_auc_knn = auc(fpr_knn, tpr_knn)

#get false pos & true pos rates - baselns
fpr_mostfreq, tpr_mostfreq, _ = roc_curve(y, y_score_mostfreq, pos_label=1)
fpr_random, tpr_random, _ = roc_curve(y, y_score_random, pos_label=1)

#plot
plt.figure(figsize=(7,7))
    #ROC curves
plt.plot(fpr_logreg, tpr_logreg, label=f"Logistic Regression (AUC = {roc_auc_logreg:.4f})")
plt.plot(fpr_knn, tpr_knn, label=f"kNN (AUC = {roc_auc_knn:.4f})")
    #freq baseln 
plt.plot(fpr_mostfreq, tpr_mostfreq, c='g', marker='.', label='Most Frequent classifier')
    #diagonal (rand Baseln)
plt.plot(fpr_random, tpr_random, 'k--', label='Random classifier')
    #lables&legend
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curves for Logistic Regression and kNN Classifiers")
plt.legend(loc="lower right")
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
#'''


