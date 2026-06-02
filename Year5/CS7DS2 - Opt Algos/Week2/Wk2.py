import sympy as sp
import sympy.plotting as plt
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema

def center_axes(ax):
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_label_coords(1.0, 0.45)
    ax.yaxis.set_label_coords(0.45, 0.95)

#'''
#-----------------Q1-----------------------
print("----------Q1----------")
###a###
x = sp.symbols('x')
f = x**4
dfdx = sp.diff(f, x)
print("df/dx = " + str(dfdx))

###b###
def f(x):
    return x**4

def df_exact(x):
    return 4*x**3

def df_forward(x, delta):
    return (f(x + delta) - f(x)) / delta

# range
x_vals = np.linspace(-2, 2, 400)
delta = 0.01

exact = df_exact(x_vals)
approx = df_forward(x_vals, delta)

# plot
plt.figure()
plt.plot(x_vals, exact, label="Exact derivative")
plt.plot(x_vals, approx, linestyle="--", label="Forward finite difference (δ=0.01)")
plt.xlabel("x")
plt.ylabel("f'(x)")
plt.legend(loc=	'lower right')
plt.title("Exact vs Finite Difference Derivative")
ax = plt.gca()
center_axes(ax)
plt.show()

###c###
deltas = [0.001, 0.01, 0.1, 1]
mae = []

print("Delta\t\tMAE")
print("-" * 25)

for delta in deltas:
    approx = df_forward(x_vals, delta)
    error = np.mean(np.abs(exact - approx))
    mae.append(error)
    print(f"{delta:.3f}\t\t{error:.3f}")

plt.figure()
plt.plot(deltas, mae, marker='o')
plt.xscale("log")
plt.yscale("log")
plt.xlabel("δ")
plt.ylabel("Mean Absolute Error")
plt.title("MAE vs δ (Forward Finite Difference)")
plt.grid(True, which="both", linestyle="--", alpha=0.5)
plt.show()

###d###
def gradient_descent(alpha, x0=1.0, n_iters=10):
    x = x0
    xs = [x]
    fs = [f(x)]
    
    for _ in range(n_iters):
        x = x - alpha * df_exact(x)

        if abs(x) > 1e6: #divergence occurs
            print(f"Divergence detected for alpha = {alpha}")
            break

        xs.append(x)
        fs.append(f(x))
        print(f"{x:.3f}   \t   {f(x):.3f}")

    print('\n')
    return np.array(xs), np.array(fs)

alphas = [0.05, 0.5, 1.2]
results = {}

for alpha in alphas:
    print(f"learning rate: {alpha}")
    print("x   \t\t   f(x)")
    print("-" * 25)
    results[alpha] = gradient_descent(alpha)


###e###
plt.figure(figsize=(12, 4))

# x_k plot
plt.subplot(1, 2, 1)
for alpha in alphas:
    xs, _ = results[alpha]
    plt.plot(xs, label=f"α={alpha}")
plt.xlabel("Iteration")
plt.ylabel("$x_k$")
plt.title("$x_k$ vs Iteration")
plt.legend()

# f(x_k) plot
plt.subplot(1, 2, 2)
for alpha in alphas:
    _, fs = results[alpha]
    plt.plot(fs, label=f"α={alpha}")
plt.xlabel("Iteration")
plt.ylabel("f($x_k$)")
plt.title("f($x_k$) vs Iteration")
plt.legend()

plt.tight_layout()
plt.show()
#'''
#'''
#-----------------Q2-----------------------
print("----------Q2----------")
###(i)###
###a###

def f2(x0, x1):
    return 0.5 * (x0**2 + 10*x1**2)

# grid
x0 = np.linspace(-2, 2, 400)
x1 = np.linspace(-2, 2, 400)
X0, X1 = np.meshgrid(x0, x1)

Z = f2(X0, X1)

plt.figure()
plt.contour(X0, X1, Z, levels=20)
plt.xlabel("$x_0$")
plt.ylabel("$x_1$")
plt.title("Contour Plot of f($x_0, x_1$)")
plt.show()

###b###
def grad_f(x):
    return np.array([x[0], 10*x[1]])

def gradient_descent_2d(alpha, x0, n_iters=20):
    x = np.array(x0, dtype=float)
    path = [x.copy()]
    
    for _ in range(n_iters):
        x = x - alpha * grad_f(x)
        path.append(x.copy())
    
    return np.array(path)

x_init = [1.5, 1.5]

path1 = gradient_descent_2d(0.05, x_init)
path2 = gradient_descent_2d(0.2, x_init)

plt.figure()
plt.contour(X0, X1, Z, levels=20)

plt.plot(path1[:,0], path1[:,1], 'o-', label="α=0.05")
plt.plot(path2[:,0], path2[:,1], 'o-', label="α=0.2")

plt.legend()
plt.xlabel("$x_0$")
plt.ylabel("$x_1$")
plt.title("Gradient Descent Paths")
plt.show()

###(ii)###
###a###
def f3(x):
    return x**4 - 2*x**2 + 0.1*x

x_vals = np.linspace(-2, 2, 400)
y_vals = f3(x_vals)

max_indices = argrelextrema(y_vals, np.greater)[0]
min_indices = argrelextrema(y_vals, np.less)[0]

plt.figure()
plt.plot(x_vals, y_vals, label="f(x) = $x^4 - 2x^2 + 0.1x$")
plt.scatter(x_vals[max_indices], y_vals[max_indices], 
            color='red', marker='o', s=25, label='Local Maxima', zorder=5)
plt.scatter(x_vals[min_indices], y_vals[min_indices], 
            color='blue', marker='o', s=25, label='Local Minima', zorder=5)
plt.xlabel("x")
plt.ylabel("f(x)")
plt.title("Plot of f(x)")
plt.legend(loc=	'upper left')
plt.grid(True)
plt.axhline(0, color='black',linewidth=0.5)
plt.axvline(0, color='black',linewidth=0.5)
ax = plt.gca()
center_axes(ax)
plt.show()

###b###
def df3(x):
    return 4*x**3 - 4*x + 0.1

def gradient_descent_1d(alpha, x0, n_iters=50):
    x = x0
    path = [x]
    
    for _ in range(n_iters):
        x = x - alpha * df3(x)
        path.append(x)
    
    return np.array(path)

path_neg = gradient_descent_1d(0.05, -1.5)
path_pos = gradient_descent_1d(0.05, 1.5)

print("Final from -1.5:", path_neg[-1])
print("Final from 1.5:", path_pos[-1])

#'''
#'''
#-----------------Q3-----------------------
print("----------Q3----------")
###(i)###
###a###
def f_quad(x):
    return x**2

def df_quad(x):
    return 2*x

def gradient_descent_1d(alpha, x0=1, n_iters=30):
    x = x0
    xs = [x]
    fs = [f_quad(x)]
    
    for _ in range(n_iters):
        x = x - alpha * df_quad(x)
        xs.append(x)
        fs.append(f_quad(x))
    
    return np.array(xs), np.array(fs)

alphas = [0.1, 0.01, 1.01]
results = {}

for alpha in alphas:
    results[alpha] = gradient_descent_1d(alpha)

###b###
plt.figure(figsize=(12,4))

# x_k
plt.subplot(1,2,1)
for alpha in alphas:
    xs, _ = results[alpha]
    plt.plot(xs, label=f"α={alpha}")
plt.xlabel("Iteration")
plt.ylabel("$x_k$")
plt.legend()
plt.title("$x_k$ vs Iteration")

# f(x_k)
plt.subplot(1,2,2)
for alpha in alphas:
    _, fs = results[alpha]
    plt.plot(fs, label=f"α={alpha}")
plt.xlabel("Iteration")
plt.ylabel("f($x_k$)")
plt.legend()
plt.title("f($x_k$) vs Iteration")

plt.tight_layout()
plt.show()

plt.figure()
for alpha in alphas:
    _, fs = results[alpha]
    plt.plot(fs, label=f"α={alpha}")

plt.yscale("log")
plt.xlabel("Iteration")
plt.ylabel("f($x_k$)")
plt.legend()
plt.title("Log-scale: f($x_k$)")
plt.show()

###(ii)###
###a###
gammas = [0.5, 1, 2, 5]

def f_gamma(x, gamma):
    return gamma * x**2

def gradient_descent_gamma(alpha, gamma, x0=1, n_iters=30):
    x = x0
    fs = [f_gamma(x, gamma)]
    
    for _ in range(n_iters):
        x = x * (1 - (2*alpha*gamma))
        fs.append(f_gamma(x, gamma))
    
    return np.array(fs)

results_gamma = {}

for gamma in gammas:
    results_gamma[gamma] = gradient_descent_gamma(0.1, gamma)

###b###
plt.figure()
for gamma in gammas:
    plt.plot(results_gamma[gamma], label=f"γ={gamma}")

plt.yscale("log")
plt.xlabel("Iteration")
plt.ylabel("f($x_k$)")
plt.legend()
plt.title("Log-scale: Effect of γ")
plt.show()

###(iii)###
###a###
def subgrad(x):  #sign(x) func
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:        #x=0
        return 0

def gradient_descent_abs(alpha, x0=1, n_iters=60):
    x = x0
    xs = [x]
    fs = [abs(x)]
    
    for _ in range(n_iters):
        x = x - alpha * subgrad(x)
        xs.append(x)
        fs.append(abs(x))
    
    return np.array(xs), np.array(fs)

xs_abs, fs_abs = gradient_descent_abs(0.1)

###b###
plt.figure(figsize=(12,4))

plt.subplot(1,2,1)
plt.plot(xs_abs)
plt.title("$x_k$ vs iteration")
plt.xlabel("Iteration")
plt.ylabel("$x_k$")

plt.subplot(1,2,2)
plt.plot(fs_abs)
plt.title("f($x_k$) vs iteration")
plt.xlabel("Iteration")
plt.ylabel("$f(x_k)$")

plt.tight_layout()
plt.show()
#'''
#'''
#-----------------Q4-----------------------
print("----------Q4----------")
###a###
def f_q4(x1, x2, gamma):
    return x1**2 + gamma * x2**2

x1 = np.linspace(-1.5, 1.5, 400)
x2 = np.linspace(-1.5, 1.5, 400)
X1, X2 = np.meshgrid(x1, x2)
gammas = [1, 4]
plt.figure(figsize=(12,5))

for i, gamma in enumerate(gammas):
    plt.subplot(1,2,i+1)
    Z = f_q4(X1, X2, gamma)
    plt.contour(X1, X2, Z, levels=20)
    plt.title(f"Contours (γ = {gamma})")
    plt.xlabel("$x_1$")
    plt.ylabel("$x_2$")

plt.tight_layout()
plt.show()


###b###
def grad_q4(x, gamma):
    return np.array([2*x[0], 2*gamma*x[1]])

def gradient_descent_q4(alpha, gamma, x0, n_iters=20):
    x = np.array(x0, dtype=float)
    path = [x.copy()]
    
    for _ in range(n_iters):
        x = x - alpha * grad_q4(x, gamma)
        path.append(x.copy())
    
    return np.array(path)

x_init = [1, 1]
alpha = 0.1

paths = {}

for gamma in [1, 4]:
    paths[gamma] = gradient_descent_q4(alpha, gamma, x_init)

plt.figure(figsize=(12,5))

for i, gamma in enumerate([1,4]):
    plt.subplot(1,2,i+1)
    Z = f_q4(X1, X2, gamma)
    plt.contour(X1, X2, Z, levels=20)
    
    path = paths[gamma]
    plt.plot(path[:,0], path[:,1], 'o-', color='red', label='Gradient Decent Path')
    
    plt.title(f"GD Path (γ = {gamma})")
    plt.xlabel("$x_1$")
    plt.ylabel("$x_2$")
    plt.legend(loc = 'lower left')

plt.tight_layout()
plt.show()

###c###
def rosenbrock(x1, x2):
    return (1 - x1)**2 + 100*(x2 - x1**2)**2

x1 = np.linspace(-2, 2, 400)
x2 = np.linspace(-1, 3, 400)
X1, X2 = np.meshgrid(x1, x2)

Z = rosenbrock(X1, X2)

plt.figure()
plt.contour(X1, X2, Z, levels=50)
plt.title("Rosenbrock Function Contours")
plt.xlabel("$x_1$")
plt.ylabel("$x_2$")
plt.show()

###d###
def grad_rosenbrock(x):
    x1, x2 = x
    df_dx1 = -2*(1 - x1) - 400*x1*(x2 - x1**2)
    df_dx2 = 200*(x2 - x1**2)
    return np.array([df_dx1, df_dx2])

def gradient_descent_rosen(alpha, x0, n_iters=2000):
    x = np.array(x0, dtype=float)
    path = [x.copy()]
    
    for _ in range(n_iters):
        x = x - alpha * grad_rosenbrock(x)
        path.append(x.copy())
    
    return np.array(path)

x_init = [-1.25, 0.5]

path1 = gradient_descent_rosen(0.001, x_init)
path2 = gradient_descent_rosen(0.005, x_init)

plt.figure()
plt.contour(X1, X2, Z, levels=50)

plt.plot(path1[:,0], path1[:,1], label="α=0.001")
plt.plot(path2[:,0], path2[:,1], label="α=0.005")

plt.legend()
plt.title("GD on Rosenbrock")
plt.xlabel("$x_1$")
plt.ylabel("$x_2$")
plt.show()
#'''
