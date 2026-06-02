import numpy as np
import matplotlib.pyplot as plt

#'''
# numerical output helper funcs
def print_vector(name, v):
    print(f"{name}: [{v[0]:.6f}, {v[1]:.6f}]")

def print_head_tail(arr, name, k=5):
    arr = np.asarray(arr)
    print(f"{name} first {k}: {np.round(arr[:k], 6)}")
    print(f"{name} last  {k}: {np.round(arr[-k:], 6)}")

def print_iterate_summary(traj, vals, label):
    print(f"\n--- {label} summary ---")
    print(f"Number of iterates stored: {len(traj)}")
    print_vector("Initial iterate", traj[0])
    print_vector("Final iterate", traj[-1])
    print(f"Initial objective: {vals[0]:.6f}")
    print(f"Final objective:   {vals[-1]:.6f}")
    print(f"Min objective:     {np.min(vals):.6f}")
    print(f"Max objective:     {np.max(vals):.6f}")
    print_head_tail(vals, "Objective values")
    print_head_tail(traj[:, 0], "x1 values")
    print_head_tail(traj[:, 1], "x2 values")

def print_stepsize_summary(step_hist, label):
    print(f"\n--- {label} step-size summary ---")
    if step_hist.ndim == 1:
        print(f"Initial step size: {step_hist[0]:.6f}")
        print(f"Final step size:   {step_hist[-1]:.6f}")
        print(f"Min step size:     {np.min(step_hist):.6f}")
        print(f"Max step size:     {np.max(step_hist):.6f}")
        print_head_tail(step_hist, "Step sizes")
    else:
        print_vector("Initial effective step", step_hist[0])
        print_vector("Final effective step", step_hist[-1])
        print(f"step1 min/max: {step_hist[:,0].min():.6f} / {step_hist[:,0].max():.6f}")
        print(f"step2 min/max: {step_hist[:,1].min():.6f} / {step_hist[:,1].max():.6f}")
        print_head_tail(step_hist[:, 0], "step1 values")
        print_head_tail(step_hist[:, 1], "step2 values")

def print_method_comparison(method_dict, benchmark_name):
    print(f"\n========== {benchmark_name}: final objective comparison ==========")
    for method_name, result in method_dict.items():
        print(f"{method_name:18s} final objective = {result['vals'][-1]:.6f}")

def safe_log_values(vals, floor=1e-12):
    vals = np.asarray(vals)
    return np.maximum(vals, floor)
#'''

#'''
#--------------Benchmarks------------------------

#Benchmark A: linear regression quadratic loss#
def make_benchmark_A(m=1000, seed=7, noise_std=0.35):
    rng = np.random.default_rng(seed)
    theta_star = np.array([3.0, 4.0])
    X = rng.normal(size=(m, 2))
    eps = rng.normal(loc=0.0, scale=noise_std, size=m)
    y = X @ theta_star + eps
    return X, y, theta_star

def f_A(theta, X, y):
    r = X @ theta - y
    m = X.shape[0]
    return 0.5 / m * np.dot(r, r)

def grad_A(theta, X, y):
    m = X.shape[0]
    return (X.T @ (X @ theta - y)) / m

#(Benchmark B: toy neural network quadratic loss)#
def f_B(x):
    x1, x2 = x
    return (x1 - 1.0)**2 + 5.0*(x2 - 2.0)**2 + np.sin(x1)

def grad_B(x):
    x1, x2 = x
    return np.array([
        2.0*(x1 - 1.0) + np.cos(x1),
        10.0*(x2 - 2.0)
    ])

#Benchmark C: Rosenbrock#
def f_C(x):
    x1, x2 = x
    return (1.0 - x1)**2 + 100.0*(x2 - x1**2)**2

def grad_C(x):
    x1, x2 = x
    return np.array([
        -2.0*(1.0 - x1) - 400.0*x1*(x2 - x1**2),
        200.0*(x2 - x1**2)
    ])

#-----------------Q1-----------------------
print("----------Q1----------")
#a(implement opt. methods)#
# constant-step gradient descent
def gradient_descent_constant(f, grad_f, x0, alpha, n_iters=120):
    x = x0.copy()
    xs = [x.copy()]
    vals = [f(x)]

    for _ in range(n_iters):
        g = grad_f(x)
        x = x - alpha * g
        xs.append(x.copy())
        vals.append(f(x))

    return np.array(xs), np.array(vals)

# Polyak step size
def gradient_descent_polyak(f, grad_f, x0, f_star=0.0, eps=1e-4, n_iters=120):
    x = x0.copy()
    xs = [x.copy()]
    vals = [f(x)]
    step_hist = []

    for _ in range(n_iters):
        g = grad_f(x)
        g2 = np.dot(g, g)
        alpha = (f(x) - f_star) / (g2 + eps)
        step_hist.append(alpha)

        x = x - alpha * g
        xs.append(x.copy())
        vals.append(f(x))

    return np.array(xs), np.array(vals), np.array(step_hist)

# Adagrad
def adagrad(f, grad_f, x0, alpha0, eps=1e-5, n_iters=120):
    x = x0.copy()
    s = np.zeros_like(x)

    xs = [x.copy()]
    vals = [f(x)]
    step_hist = []

    for _ in range(n_iters):
        g = grad_f(x)
        s = s + g**2
        eff_step = alpha0 / (np.sqrt(s) + eps)
        step_hist.append(eff_step.copy())

        x = x - eff_step * g
        xs.append(x.copy())
        vals.append(f(x))

    return np.array(xs), np.array(vals), np.array(step_hist)

# RMSprop
def rmsprop(f, grad_f, x0, alpha0, beta=0.9, eps=1e-5, n_iters=120):
    x = x0.copy()
    s = np.zeros_like(x)

    xs = [x.copy()]
    vals = [f(x)]
    step_hist = []

    for _ in range(n_iters):
        g = grad_f(x)
        s = beta * s + (1.0 - beta) * (g**2)
        eff_step = alpha0 / (np.sqrt(s) + eps)
        step_hist.append(eff_step.copy())

        x = x - eff_step * g
        xs.append(x.copy())
        vals.append(f(x))

    return np.array(xs), np.array(vals), np.array(step_hist)

# Polyak momentum / heavy ball
def heavy_ball(f, grad_f, x0, alpha, beta, n_iters=120):
    x = x0.copy()
    z = np.zeros_like(x)

    xs = [x.copy()]
    vals = [f(x)]

    for _ in range(n_iters):
        g = grad_f(x)
        z = beta * z + alpha * g
        x = x - z
        xs.append(x.copy())
        vals.append(f(x))

    return np.array(xs), np.array(vals)

#-------------------plot helper funcs-------------------#

##b(objective value vs iteration)##
def plot_objective_2x3(results, title):
    method_names = list(results.keys())
    fig, axes = plt.subplots(2, 3, figsize=(14, 8))
    axes = axes.flatten()

    for i, method_name in enumerate(method_names):
        ax = axes[i]
        vals = results[method_name]['vals']
        ax.plot(vals, linewidth=1.8)
        ax.set_title(method_name)
        ax.set_xlabel('Iteration')
        ax.set_ylabel('Objective value')
        ax.grid(True)

    axes[-1].axis('off')

    fig.suptitle(title, fontsize=14)
    plt.tight_layout()
    plt.show()


###c(contour + trajectory)###
def plot_contour_trajectory_2x3(f, results, x1_range, x2_range, title, levels=30):
    method_names = list(results.keys())

    x1 = np.linspace(x1_range[0], x1_range[1], 400)
    x2 = np.linspace(x2_range[0], x2_range[1], 400)
    X1, X2 = np.meshgrid(x1, x2)
    Z = np.zeros_like(X1)

    for i in range(X1.shape[0]):
        for j in range(X1.shape[1]):
            Z[i, j] = f(np.array([X1[i, j], X2[i, j]]))

    fig, axes = plt.subplots(2, 3, figsize=(14, 10))
    axes = axes.flatten()

    for i, method_name in enumerate(method_names):
        ax = axes[i]
        traj = results[method_name]['traj']

        cs = ax.contour(X1, X2, Z, levels=levels)
        ax.clabel(cs, inline=True, fontsize=7)
        ax.plot(traj[:, 0], traj[:, 1], 'ro-', markersize=2.5, linewidth=1.2)

        ax.set_title(method_name)
        ax.set_xlabel(r'$x_1$')
        ax.set_ylabel(r'$x_2$')
        ax.grid(True)

    axes[-1].axis('off')

    fig.suptitle(title, fontsize=14)
    plt.tight_layout()
    plt.show()

####d(adaptive step-size)####
def plot_adaptive_stepsize(polyak_steps, adagrad_steps, rmsprop_steps, title):
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

    step1 = r'$x_1$ step'
    step2 = r'$x_2$ step'
    
    if (title == 'Benchmark A: Adaptive Step-Size Evolution'):
        step1 = r'$\theta_1$ step'
        step2 = r'$\theta_2$ step'
    
    # Polyak
    axes[0].plot(polyak_steps, linewidth=1.8)
    axes[0].set_title('Polyak')
    axes[0].set_xlabel('Iteration')
    axes[0].set_ylabel('Step size')
    axes[0].grid(True)

    # Adagrad
    axes[1].plot(adagrad_steps[:, 0], label=step1, linewidth=1.8)
    axes[1].plot(adagrad_steps[:, 1], label=step2, linewidth=1.8)
    axes[1].set_title('Adagrad')
    axes[1].set_xlabel('Iteration')
    axes[1].set_ylabel('Effective step size')
    axes[1].legend()
    axes[1].grid(True)

    # RMSprop
    axes[2].plot(rmsprop_steps[:, 0], label=step1, linewidth=1.8)
    axes[2].plot(rmsprop_steps[:, 1], label=step2, linewidth=1.8)

    axes[2].set_title('RMSprop')
    axes[2].set_xlabel('Iteration')
    axes[2].set_ylabel('Effective step size')
    axes[2].legend()
    axes[2].grid(True)

    fig.suptitle(title, fontsize=14)
    plt.tight_layout()
    plt.show()

#-----------------Q1: run all benchmark experiments-----------------------
print("\n===== Benchmark A: Linear Regression Quadratic Loss =====")
X_A, y_A, theta_star_A = make_benchmark_A(m=1000, seed=7, noise_std=0.35)

def fA_wrap(x):
    return f_A(x, X_A, y_A)

def gA_wrap(x):
    return grad_A(x, X_A, y_A)

x0_A = np.array([-4.0, 6.0])

traj_A_gd, vals_A_gd = gradient_descent_constant(
    fA_wrap, gA_wrap, x0_A, alpha=0.08, n_iters=120
)
traj_A_poly, vals_A_poly, steps_A_poly = gradient_descent_polyak(
    fA_wrap, gA_wrap, x0_A, f_star=0.0, eps=1e-4, n_iters=120
)
traj_A_ada, vals_A_ada, steps_A_ada = adagrad(
    fA_wrap, gA_wrap, x0_A, alpha0=1.8, eps=1e-5, n_iters=120
)
traj_A_rms, vals_A_rms, steps_A_rms = rmsprop(
    fA_wrap, gA_wrap, x0_A, alpha0=0.22, beta=0.9, eps=1e-5, n_iters=120
)
traj_A_hb, vals_A_hb = heavy_ball(
    fA_wrap, gA_wrap, x0_A, alpha=0.045, beta=0.88, n_iters=120
)

results_A = {
    'GD baseline': {'traj': traj_A_gd, 'vals': vals_A_gd},
    'Polyak': {'traj': traj_A_poly, 'vals': vals_A_poly},
    'Adagrad': {'traj': traj_A_ada, 'vals': vals_A_ada},
    'RMSprop': {'traj': traj_A_rms, 'vals': vals_A_rms},
    'Heavy Ball': {'traj': traj_A_hb, 'vals': vals_A_hb}
}

#'''
print_vector("True theta*", theta_star_A)
print_iterate_summary(traj_A_gd, vals_A_gd, "Benchmark A: GD baseline")
print_iterate_summary(traj_A_poly, vals_A_poly, "Benchmark A: Polyak")
print_iterate_summary(traj_A_ada, vals_A_ada, "Benchmark A: Adagrad")
print_iterate_summary(traj_A_rms, vals_A_rms, "Benchmark A: RMSprop")
print_iterate_summary(traj_A_hb, vals_A_hb, "Benchmark A: Heavy Ball")

print_stepsize_summary(steps_A_poly, "Benchmark A: Polyak")
print_stepsize_summary(steps_A_ada, "Benchmark A: Adagrad")
print_stepsize_summary(steps_A_rms, "Benchmark A: RMSprop")

print_method_comparison(results_A, "Benchmark A")
#'''

print("\n===== Benchmark B: Toy Neural Network Quadratic Loss =====")
x0_B = np.array([-1.5, 4.5])

traj_B_gd, vals_B_gd = gradient_descent_constant(
    f_B, grad_B, x0_B, alpha=0.06, n_iters=120
)
traj_B_poly, vals_B_poly, steps_B_poly = gradient_descent_polyak(
    f_B, grad_B, x0_B, f_star=0.0, eps=1e-4, n_iters=120
)
traj_B_ada, vals_B_ada, steps_B_ada = adagrad(
    f_B, grad_B, x0_B, alpha0=1.2, eps=1e-5, n_iters=120
)
traj_B_rms, vals_B_rms, steps_B_rms = rmsprop(
    f_B, grad_B, x0_B, alpha0=0.14, beta=0.9, eps=1e-5, n_iters=120
)
traj_B_hb, vals_B_hb = heavy_ball(
    f_B, grad_B, x0_B, alpha=0.035, beta=0.90, n_iters=120
)

results_B = {
    'GD baseline': {'traj': traj_B_gd, 'vals': vals_B_gd},
    'Polyak': {'traj': traj_B_poly, 'vals': vals_B_poly},
    'Adagrad': {'traj': traj_B_ada, 'vals': vals_B_ada},
    'RMSprop': {'traj': traj_B_rms, 'vals': vals_B_rms},
    'Heavy Ball': {'traj': traj_B_hb, 'vals': vals_B_hb}
}

#'''
print_iterate_summary(traj_B_gd, vals_B_gd, "Benchmark B: GD baseline")
print_iterate_summary(traj_B_poly, vals_B_poly, "Benchmark B: Polyak")
print_iterate_summary(traj_B_ada, vals_B_ada, "Benchmark B: Adagrad")
print_iterate_summary(traj_B_rms, vals_B_rms, "Benchmark B: RMSprop")
print_iterate_summary(traj_B_hb, vals_B_hb, "Benchmark B: Heavy Ball")

print_stepsize_summary(steps_B_poly, "Benchmark B: Polyak")
print_stepsize_summary(steps_B_ada, "Benchmark B: Adagrad")
print_stepsize_summary(steps_B_rms, "Benchmark B: RMSprop")

print_method_comparison(results_B, "Benchmark B")
#'''

print("\n===== Benchmark C: Rosenbrock Function =====")
x0_C = np.array([-1.2, 1.0])

traj_C_gd, vals_C_gd = gradient_descent_constant(
    f_C, grad_C, x0_C, alpha=0.0012, n_iters=120
)
traj_C_poly, vals_C_poly, steps_C_poly = gradient_descent_polyak(
    f_C, grad_C, x0_C, f_star=0.0, eps=1e-3, n_iters=120
)
traj_C_ada, vals_C_ada, steps_C_ada = adagrad(
    f_C, grad_C, x0_C, alpha0=0.45, eps=1e-5, n_iters=120
)
traj_C_rms, vals_C_rms, steps_C_rms = rmsprop(
    f_C, grad_C, x0_C, alpha0=0.0035, beta=0.9, eps=1e-5, n_iters=120
)
traj_C_hb, vals_C_hb = heavy_ball(
    f_C, grad_C, x0_C, alpha=0.0008, beta=0.86, n_iters=120
)

results_C = {
    'GD baseline': {'traj': traj_C_gd, 'vals': vals_C_gd},
    'Polyak': {'traj': traj_C_poly, 'vals': vals_C_poly},
    'Adagrad': {'traj': traj_C_ada, 'vals': vals_C_ada},
    'RMSprop': {'traj': traj_C_rms, 'vals': vals_C_rms},
    'Heavy Ball': {'traj': traj_C_hb, 'vals': vals_C_hb}
}

#'''
print_iterate_summary(traj_C_gd, vals_C_gd, "Benchmark C: GD baseline")
print_iterate_summary(traj_C_poly, vals_C_poly, "Benchmark C: Polyak")
print_iterate_summary(traj_C_ada, vals_C_ada, "Benchmark C: Adagrad")
print_iterate_summary(traj_C_rms, vals_C_rms, "Benchmark C: RMSprop")
print_iterate_summary(traj_C_hb, vals_C_hb, "Benchmark C: Heavy Ball")

print_stepsize_summary(steps_C_poly, "Benchmark C: Polyak")
print_stepsize_summary(steps_C_ada, "Benchmark C: Adagrad")
print_stepsize_summary(steps_C_rms, "Benchmark C: RMSprop")

print_method_comparison(results_C, "Benchmark C")
#'''
#--------------------------------------------------------------------------

#-PLOT-#
#'''
##b(objective vs iteration)##
plot_objective_2x3(results_A, 'Benchmark A: Objective vs Iteration')
plot_objective_2x3(results_B, 'Benchmark B: Objective vs Iteration')
plot_objective_2x3(results_C, 'Benchmark C: Objective vs Iteration')

###c(contour plots + opt. traj.)###
plot_contour_trajectory_2x3(
    f_B,
    results_B,
    x1_range=(-2.0, 2.5),
    x2_range=(0.5, 4.5),
    title='Benchmark B: Contour & Optimisation Trajectories',
    levels=25
)

plot_contour_trajectory_2x3(
    f_C,
    results_C,
    x1_range=(-1.8, 1.8),
    x2_range=(-0.5, 2.0),
    title='Benchmark C: Contour & Optimisation Trajectories',
    levels=30
)

####d(adaptive step-size evolution)####
plot_adaptive_stepsize(
    steps_A_poly, steps_A_ada, steps_A_rms,
    'Benchmark A: Adaptive Step-Size Evolution'
)

plot_adaptive_stepsize(
    steps_B_poly, steps_B_ada, steps_B_rms,
    'Benchmark B: Adaptive Step-Size Evolution'
)

plot_adaptive_stepsize(
    steps_C_poly, steps_C_ada, steps_C_rms,
    'Benchmark C: Adaptive Step-Size Evolution'
)
#'''

#'''
#-----------------Q2-----------------------
print("\n----------Q2----------")

#a(implement Nesterov, Adam, minibatch SGD, noisy SGD)#

# Nesterov momentum / acceleration
def nesterov_momentum(f, grad_f, x0, alpha, beta_max, n_iters=150):
    x = x0.copy()
    z = np.zeros_like(x)

    xs = [x.copy()]
    vals = [f(x)]

    for k in range(1, n_iters + 1):
        beta_k = min((k - 1) / (k + 2), beta_max)

        lookahead = x + beta_k * z
        g = grad_f(lookahead)

        z = beta_k * z - alpha * g
        x = x + z

        xs.append(x.copy())
        vals.append(f(x))

    return np.array(xs), np.array(vals)

# Adam
def adam(f, grad_f, x0, alpha, beta1, beta2, eps=1e-8, n_iters=150):
    x = x0.copy()
    m = np.zeros_like(x)
    v = np.zeros_like(x)

    xs = [x.copy()]
    vals = [f(x)]

    for t in range(1, n_iters + 1):
        g = grad_f(x)

        m = beta1 * m + (1.0 - beta1) * g
        v = beta2 * v + (1.0 - beta2) * (g**2)

        m_hat = m / (1.0 - beta1**t)
        v_hat = v / (1.0 - beta2**t)

        x = x - alpha * m_hat / (np.sqrt(v_hat) + eps)

        xs.append(x.copy())
        vals.append(f(x))

    return np.array(xs), np.array(vals)

# minibatch SGD for Benchmark A
def minibatch_sgd_A(X, y, x0, alpha=0.06, batch_size=5, epochs=50, seed=123):
    rng = np.random.default_rng(seed)

    x = x0.copy()
    xs = [x.copy()]
    vals = [f_A(x, X, y)]

    m = X.shape[0]

    for _ in range(epochs):
        perm = rng.permutation(m)
        X_shuf = X[perm]
        y_shuf = y[perm]

        for start in range(0, m, batch_size):
            end = min(start + batch_size, m)

            Xb = X_shuf[start:end]
            yb = y_shuf[start:end]

            g = (Xb.T @ (Xb @ x - yb)) / Xb.shape[0]
            x = x - alpha * g

        xs.append(x.copy())
        vals.append(f_A(x, X, y))

    return np.array(xs), np.array(vals)

#-------------------plot helper funcs-------------------#

##b(objective value vs iteration for Q2 full-batch methods)##
def plot_objective_1x3(results, title):
    method_names = list(results.keys())
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

    for i, method_name in enumerate(method_names):
        ax = axes[i]
        vals = results[method_name]['vals']
        ax.plot(vals, linewidth=1.8)
        ax.set_title(method_name)
        ax.set_xlabel('Iteration')
        ax.set_ylabel('Objective value')
        ax.grid(True)

    fig.suptitle(title, fontsize=14)
    plt.tight_layout()
    plt.show()

###c(contour + trajectory for full-batch methods)###
def plot_contour_trajectory_1x3(f, results, x1_range, x2_range, title, levels=30):
    method_names = list(results.keys())

    x1 = np.linspace(x1_range[0], x1_range[1], 400)
    x2 = np.linspace(x2_range[0], x2_range[1], 400)
    X1, X2 = np.meshgrid(x1, x2)
    Z = np.zeros_like(X1)

    for i in range(X1.shape[0]):
        for j in range(X1.shape[1]):
            Z[i, j] = f(np.array([X1[i, j], X2[i, j]]))

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

    for i, method_name in enumerate(method_names):
        ax = axes[i]
        traj = results[method_name]['traj']

        cs = ax.contour(X1, X2, Z, levels=levels)
        ax.clabel(cs, inline=True, fontsize=7)
        ax.plot(traj[:, 0], traj[:, 1], 'ro-', markersize=2.5, linewidth=1.2)

        ax.set_title(method_name)
        ax.set_xlabel(r'$x_1$')
        ax.set_ylabel(r'$x_2$')
        ax.grid(True)

    fig.suptitle(title, fontsize=14)
    plt.tight_layout()
    plt.show()

####d(SGD batch-size comparison plots)####
def plot_sgd_batch_comparison(vals_b5, vals_b40, title):
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    axes[0].plot(vals_b5, 'o-', markersize=3, label='batch size = 5')
    axes[0].plot(vals_b40, 's-', markersize=3, label='batch size = 40')
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Objective value')
    axes[0].set_title('Objective vs epoch')
    axes[0].legend()
    axes[0].grid(True)

    axes[1].plot(vals_b5, 'o-', markersize=3, label='batch size = 5')
    axes[1].plot(vals_b40, 's-', markersize=3, label='batch size = 40')
    axes[1].set_yscale('log')
    axes[1].set_xlabel('Epoch')
    axes[1].set_ylabel('Objective value (log scale)')
    axes[1].set_title('Objective vs epoch (log scale)')
    axes[1].legend()
    axes[1].grid(True)

    fig.suptitle(title, fontsize=14)
    plt.tight_layout()
    plt.show()

#####e(noisy SGD comparison plot)#####
def plot_noisy_sgd_comparison(vals_clean_b5, vals_noisy_b5, vals_clean_b40, vals_noisy_b40, title):
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    axes[0].plot(vals_clean_b5, 'o-', markersize=3, label='clean, b = 5')
    axes[0].plot(vals_noisy_b5, 'o--', markersize=3, label='noisy, b = 5')
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Objective value')
    axes[0].set_title('Batch size 5')
    axes[0].legend()
    axes[0].grid(True)

    axes[1].plot(vals_clean_b40, 's-', markersize=3, label='clean, b = 40')
    axes[1].plot(vals_noisy_b40, 's--', markersize=3, label='noisy, b = 40')
    axes[1].set_xlabel('Epoch')
    axes[1].set_ylabel('Objective value')
    axes[1].set_title('Batch size 40')
    axes[1].legend()
    axes[1].grid(True)

    fig.suptitle(title, fontsize=14)
    plt.tight_layout()
    plt.show()

#-----------------Q2: prepare benchmark A data-----------------------
print("\n===== Benchmark A: Linear Regression Quadratic Loss =====")
X_A_q2, y_A_q2, theta_star_A_q2 = make_benchmark_A(m=1000, seed=7, noise_std=0.35)
X_A_q2_noisy, y_A_q2_noisy, _ = make_benchmark_A(m=1000, seed=7, noise_std=0.35 * 6.0)

def fA_q2(x):
    return f_A(x, X_A_q2, y_A_q2)

def gA_q2(x):
    return grad_A(x, X_A_q2, y_A_q2)

def fA_q2_noisy(x):
    return f_A(x, X_A_q2_noisy, y_A_q2_noisy)

#-----------------Q2: Benchmark A full-batch methods-----------------------
x0_A_q2 = np.array([-4.0, 6.0])

traj_A_q2_gd, vals_A_q2_gd = gradient_descent_constant(
    fA_q2, gA_q2, x0_A_q2, alpha=0.08, n_iters=150
)

traj_A_q2_nes, vals_A_q2_nes = nesterov_momentum(
    fA_q2, gA_q2, x0_A_q2, alpha=0.06, beta_max=0.90, n_iters=150
)

traj_A_q2_adam, vals_A_q2_adam = adam(
    fA_q2, gA_q2, x0_A_q2, alpha=0.12, beta1=0.82, beta2=0.999, eps=1e-8, n_iters=150
)

results_A_q2 = {
    'GD baseline': {'traj': traj_A_q2_gd, 'vals': vals_A_q2_gd},
    'Nesterov': {'traj': traj_A_q2_nes, 'vals': vals_A_q2_nes},
    'Adam': {'traj': traj_A_q2_adam, 'vals': vals_A_q2_adam}
}

#'''
print_vector("True theta*", theta_star_A_q2)
print_iterate_summary(traj_A_q2_gd, vals_A_q2_gd, "Q2 Benchmark A: GD baseline")
print_iterate_summary(traj_A_q2_nes, vals_A_q2_nes, "Q2 Benchmark A: Nesterov")
print_iterate_summary(traj_A_q2_adam, vals_A_q2_adam, "Q2 Benchmark A: Adam")
print_method_comparison(results_A_q2, "Q2 Benchmark A")
#'''

#-----------------Q2: Benchmark B full-batch methods-----------------------
print("\n===== Benchmark B: Toy Neural Network Quadratic Loss =====")
x0_B_q2 = np.array([-1.5, 4.5])

traj_B_q2_gd, vals_B_q2_gd = gradient_descent_constant(
    f_B, grad_B, x0_B_q2, alpha=0.06, n_iters=150
)

traj_B_q2_nes, vals_B_q2_nes = nesterov_momentum(
    f_B, grad_B, x0_B_q2, alpha=0.035, beta_max=0.92, n_iters=150
)

traj_B_q2_adam, vals_B_q2_adam = adam(
    f_B, grad_B, x0_B_q2, alpha=0.08, beta1=0.80, beta2=0.999, eps=1e-8, n_iters=150
)

results_B_q2 = {
    'GD baseline': {'traj': traj_B_q2_gd, 'vals': vals_B_q2_gd},
    'Nesterov': {'traj': traj_B_q2_nes, 'vals': vals_B_q2_nes},
    'Adam': {'traj': traj_B_q2_adam, 'vals': vals_B_q2_adam}
}

#'''
print_iterate_summary(traj_B_q2_gd, vals_B_q2_gd, "Q2 Benchmark B: GD baseline")
print_iterate_summary(traj_B_q2_nes, vals_B_q2_nes, "Q2 Benchmark B: Nesterov")
print_iterate_summary(traj_B_q2_adam, vals_B_q2_adam, "Q2 Benchmark B: Adam")
print_method_comparison(results_B_q2, "Q2 Benchmark B")
#'''

#-----------------Q2: Benchmark C full-batch methods-----------------------
print("\n===== Benchmark C: Rosenbrock Function =====")
x0_C_q2 = np.array([-1.2, 1.0])

traj_C_q2_gd, vals_C_q2_gd = gradient_descent_constant(
    f_C, grad_C, x0_C_q2, alpha=0.0012, n_iters=150
)

traj_C_q2_nes, vals_C_q2_nes = nesterov_momentum(
    f_C, grad_C, x0_C_q2, alpha=0.0007, beta_max=0.90, n_iters=150
)

traj_C_q2_adam, vals_C_q2_adam = adam(
    f_C, grad_C, x0_C_q2, alpha=0.006, beta1=0.80, beta2=0.999, eps=1e-8, n_iters=150
)

results_C_q2 = {
    'GD baseline': {'traj': traj_C_q2_gd, 'vals': vals_C_q2_gd},
    'Nesterov': {'traj': traj_C_q2_nes, 'vals': vals_C_q2_nes},
    'Adam': {'traj': traj_C_q2_adam, 'vals': vals_C_q2_adam}
}

#'''
print_iterate_summary(traj_C_q2_gd, vals_C_q2_gd, "Q2 Benchmark C: GD baseline")
print_iterate_summary(traj_C_q2_nes, vals_C_q2_nes, "Q2 Benchmark C: Nesterov")
print_iterate_summary(traj_C_q2_adam, vals_C_q2_adam, "Q2 Benchmark C: Adam")
print_method_comparison(results_C_q2, "Q2 Benchmark C")
#'''

#-----------------Q2: SGD on Benchmark A-----------------------
print("\n===== Benchmark A: Mini-Batch SGD =====")

traj_sgd_b5, vals_sgd_b5 = minibatch_sgd_A(
    X_A_q2, y_A_q2, x0_A_q2, alpha=0.06, batch_size=5, epochs=50, seed=321
)

traj_sgd_b40, vals_sgd_b40 = minibatch_sgd_A(
    X_A_q2, y_A_q2, x0_A_q2, alpha=0.06, batch_size=40, epochs=50, seed=321
)

traj_sgd_noisy_b5, vals_sgd_noisy_b5 = minibatch_sgd_A(
    X_A_q2_noisy, y_A_q2_noisy, x0_A_q2, alpha=0.06, batch_size=5, epochs=50, seed=321
)

traj_sgd_noisy_b40, vals_sgd_noisy_b40 = minibatch_sgd_A(
    X_A_q2_noisy, y_A_q2_noisy, x0_A_q2, alpha=0.06, batch_size=40, epochs=50, seed=321
)

#'''
print_iterate_summary(traj_sgd_b5, vals_sgd_b5, "Q2 SGD clean: batch size 5")
print_iterate_summary(traj_sgd_b40, vals_sgd_b40, "Q2 SGD clean: batch size 40")
print_iterate_summary(traj_sgd_noisy_b5, vals_sgd_noisy_b5, "Q2 SGD noisy: batch size 5")
print_iterate_summary(traj_sgd_noisy_b40, vals_sgd_noisy_b40, "Q2 SGD noisy: batch size 40")
#'''

#-PLOT-#
#'''
##b(objective value vs iteration)##
plot_objective_1x3(results_A_q2, 'Benchmark A: Objective vs Iteration')
plot_objective_1x3(results_B_q2, 'Benchmark B: Objective vs Iteration')
plot_objective_1x3(results_C_q2, 'Benchmark C: Objective vs Iteration')

###c(contour plots + opt traj.)###
plot_contour_trajectory_1x3(
    f_B,
    results_B_q2,
    x1_range=(-2.0, 2.5),
    x2_range=(0.5, 4.5),
    title='Benchmark B: Contour & Optimisation Trajectories',
    levels=25
)

plot_contour_trajectory_1x3(
    f_C,
    results_C_q2,
    x1_range=(-1.8, 1.8),
    x2_range=(-0.5, 2.0),
    title='Benchmark C: Contour & Optimisation Trajectories',
    levels=30
)

####d(compare SGD batch sizes)####
plot_sgd_batch_comparison(
    vals_sgd_b5, vals_sgd_b40,
    'Benchmark A: SGD Batch-Size Comparison'
)

#####e( noisy SGD comparison)#####
plot_noisy_sgd_comparison(
    vals_sgd_b5, vals_sgd_noisy_b5,
    vals_sgd_b40, vals_sgd_noisy_b40,
    'Benchmark A: Effect of Additional Noise on SGD'
)
#'''


#'''
#-----------------Q3-----------------------
print("----------Q3----------")

#a(1D local approx + Newtons method)#

# 1D test function g(x) = x^4
def g_1d(x):
    return x**4

def g1_1d(x):
    return 4.0 * x**3

def g2_1d(x):
    return 12.0 * x**2

# first-order local approx around x0
def g_first_order(x, x0=0.25):
    return g_1d(x0) + g1_1d(x0) * (x - x0)

# second-order local approx around x0
def g_second_order(x, x0=0.25):
    return g_1d(x0) + g1_1d(x0) * (x - x0) + 0.5 * g2_1d(x0) * (x - x0)**2

# Newton update for 1D
def newton_update_1d(x):
    return x - g1_1d(x) / g2_1d(x)

# Hessians for benchmark problems
def hess_A(theta, X, y):
    m = X.shape[0]
    return (X.T @ X) / m

def hess_B(x):
    x1, x2 = x
    return np.array([
        [2.0 - np.sin(x1), 0.0],
        [0.0, 10.0]
    ])

def hess_C(x):
    x1, x2 = x
    return np.array([
        [2.0 - 400.0*x2 + 1200.0*x1**2, -400.0*x1],
        [-400.0*x1, 200.0]
    ])

# Newtons method with damping
def newton_method(f, grad_f, hess_f, x0, alpha=1.0, damping=1e-8, n_iters=20):
    x = x0.copy()

    xs = [x.copy()]
    vals = [f(x)]
    update_norms = []

    for _ in range(n_iters):
        g = grad_f(x)
        H = hess_f(x)

        H_damped = H + damping * np.eye(len(x))
        step = np.linalg.solve(H_damped, g)

        x = x - alpha * step

        xs.append(x.copy())
        vals.append(f(x))
        update_norms.append(np.linalg.norm(alpha * step))

    return np.array(xs), np.array(vals), np.array(update_norms)

# GD with update magnitudes
def gradient_descent_with_updates(f, grad_f, x0, alpha, n_iters=80):
    x = x0.copy()

    xs = [x.copy()]
    vals = [f(x)]
    update_norms = []

    for _ in range(n_iters):
        g = grad_f(x)
        step = alpha * g
        x = x - step

        xs.append(x.copy())
        vals.append(f(x))
        update_norms.append(np.linalg.norm(step))

    return np.array(xs), np.array(vals), np.array(update_norms)

#-------------------plot helper funcs-------------------#
#a(plot 1D function + local approxs)#
def plot_local_approxs(x_grid, g_vals, g_lin, g_quad, x0):
    plt.figure(figsize=(7, 5))
    plt.plot(x_grid, g_vals, label=r'$g(x)=x^4$')
    plt.plot(x_grid, g_lin, '--', label='First-order approximation')
    plt.plot(x_grid, g_quad, '-.', label='Second-order approximation')
    plt.axvline(x0, linestyle=':', label=fr'$x_0={x0}$')
    plt.xlabel('x')
    plt.ylabel('Value')
    plt.title('1D local approximations')
    plt.legend()
    plt.grid(True)
    plt.show()

###c(objective value vs iteration for GD and Newton)###
def plot_objective_1x2(results, title):
    method_names = list(results.keys())
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    for i, method_name in enumerate(method_names):
        ax = axes[i]
        vals = results[method_name]['vals']
        ax.plot(vals, linewidth=1.8)
        ax.set_title(method_name)
        ax.set_xlabel('Iteration')
        ax.set_ylabel('Objective value')
        ax.grid(True)

    fig.suptitle(title, fontsize=14)
    plt.tight_layout()
    plt.show()

####d(contour plots + trajectory for GD and Newton)####
def plot_contour_trajectory_1x2(f, results, x1_range, x2_range, title, levels=30):
    method_names = list(results.keys())

    x1 = np.linspace(x1_range[0], x1_range[1], 400)
    x2 = np.linspace(x2_range[0], x2_range[1], 400)
    X1, X2 = np.meshgrid(x1, x2)
    Z = np.zeros_like(X1)

    for i in range(X1.shape[0]):
        for j in range(X1.shape[1]):
            Z[i, j] = f(np.array([X1[i, j], X2[i, j]]))

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))

    for i, method_name in enumerate(method_names):
        ax = axes[i]
        traj = results[method_name]['traj']

        cs = ax.contour(X1, X2, Z, levels=levels)
        ax.clabel(cs, inline=True, fontsize=7)
        ax.plot(traj[:, 0], traj[:, 1], 'ro-', markersize=2.5, linewidth=1.2)

        ax.set_title(method_name)
        ax.set_xlabel(r'$x_1$')
        ax.set_ylabel(r'$x_2$')
        ax.grid(True)

    fig.suptitle(title, fontsize=14)
    plt.tight_layout()
    plt.show()

#####e(update magnitude vs iteration)#####
def plot_update_magnitude(gd_updates, newton_updates, title):
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    axes[0].plot(gd_updates, linewidth=1.8)
    axes[0].set_title('Gradient Descent')
    axes[0].set_xlabel('Iteration')
    axes[0].set_ylabel('Update magnitude')
    axes[0].grid(True)

    axes[1].plot(newton_updates, linewidth=1.8)
    axes[1].set_title("Newton's Method")
    axes[1].set_xlabel('Iteration')
    axes[1].set_ylabel('Update magnitude')
    axes[1].grid(True)

    fig.suptitle(title, fontsize=14)
    plt.tight_layout()
    plt.show()

#-----------------1D local approxs-----------------------
print("\n=====First-order and Second-order Local Approximation =====")

x0_1d = 0.25
x_grid_1d = np.linspace(-0.5, 0.8, 500)

g_vals_1d = g_1d(x_grid_1d)
g_lin_1d = g_first_order(x_grid_1d, x0=x0_1d)
g_quad_1d = g_second_order(x_grid_1d, x0=x0_1d)

x1d_newton_next = newton_update_1d(x0_1d)

#'''
print(f"g(x0) at x0 = {x0_1d:.6f}: {g_1d(x0_1d):.6f}")
print(f"g'(x0) at x0 = {x0_1d:.6f}: {g1_1d(x0_1d):.6f}")
print(f"g''(x0) at x0 = {x0_1d:.6f}: {g2_1d(x0_1d):.6f}")
print(f"Newton update from x0 = {x0_1d:.6f}: x1 = {x1d_newton_next:.6f}")
#'''

#-----------------Benchmark A-----------------------
print("\n===== Benchmark A: Linear Regression Quadratic Loss =====")

X_A_q3, y_A_q3, theta_star_A_q3 = make_benchmark_A(m=1000, seed=7, noise_std=0.35)

def fA_q3(x):
    return f_A(x, X_A_q3, y_A_q3)

def gA_q3(x):
    return grad_A(x, X_A_q3, y_A_q3)

def hA_q3(x):
    return hess_A(x, X_A_q3, y_A_q3)

x0_A_q3 = np.array([-4.0, 6.0])

traj_A_q3_gd, vals_A_q3_gd, upd_A_q3_gd = gradient_descent_with_updates(
    fA_q3, gA_q3, x0_A_q3, alpha=0.08, n_iters=80
)

traj_A_q3_newton, vals_A_q3_newton, upd_A_q3_newton = newton_method(
    fA_q3, gA_q3, hA_q3, x0_A_q3, alpha=1.0, damping=1e-8, n_iters=20
)

results_A_q3 = {
    'GD baseline': {'traj': traj_A_q3_gd, 'vals': vals_A_q3_gd},
    "Newton's method": {'traj': traj_A_q3_newton, 'vals': vals_A_q3_newton}
}

#'''
print_vector("True theta*", theta_star_A_q3)
print_iterate_summary(traj_A_q3_gd, vals_A_q3_gd, "Benchmark A: GD baseline")
print_iterate_summary(traj_A_q3_newton, vals_A_q3_newton, "Benchmark A: Newton")
print_method_comparison(results_A_q3, "Benchmark A")
print_head_tail(upd_A_q3_gd, "GD update magnitudes")
print_head_tail(upd_A_q3_newton, "Newton update magnitudes")
#'''

#-----------------Benchmark B-----------------------
print("\n===== Benchmark B: Toy Neural Network Quadratic Loss =====")

x0_B_q3 = np.array([-1.5, 4.5])

traj_B_q3_gd, vals_B_q3_gd, upd_B_q3_gd = gradient_descent_with_updates(
    f_B, grad_B, x0_B_q3, alpha=0.06, n_iters=80
)

traj_B_q3_newton, vals_B_q3_newton, upd_B_q3_newton = newton_method(
    f_B, grad_B, hess_B, x0_B_q3, alpha=0.85, damping=1e-8, n_iters=20
)

results_B_q3 = {
    'GD baseline': {'traj': traj_B_q3_gd, 'vals': vals_B_q3_gd},
    "Newton's method": {'traj': traj_B_q3_newton, 'vals': vals_B_q3_newton}
}

#'''
print_iterate_summary(traj_B_q3_gd, vals_B_q3_gd, "Benchmark B: GD baseline")
print_iterate_summary(traj_B_q3_newton, vals_B_q3_newton, "Benchmark B: Newton")
print_method_comparison(results_B_q3, "Benchmark B")
print_head_tail(upd_B_q3_gd, "GD update magnitudes")
print_head_tail(upd_B_q3_newton, "Newton update magnitudes")
#'''

#-----------------Benchmark C-----------------------
print("\n===== Benchmark C: Rosenbrock Function =====")

x0_C_q3 = np.array([-1.2, 1.0])

traj_C_q3_gd, vals_C_q3_gd, upd_C_q3_gd = gradient_descent_with_updates(
    f_C, grad_C, x0_C_q3, alpha=0.001, n_iters=80
)

traj_C_q3_newton, vals_C_q3_newton, upd_C_q3_newton = newton_method(
    f_C, grad_C, hess_C, x0_C_q3, alpha=0.22, damping=1e-8, n_iters=20
)

results_C_q3 = {
    'GD baseline': {'traj': traj_C_q3_gd, 'vals': vals_C_q3_gd},
    "Newton's method": {'traj': traj_C_q3_newton, 'vals': vals_C_q3_newton}
}

#'''
print_iterate_summary(traj_C_q3_gd, vals_C_q3_gd, "Benchmark C: GD baseline")
print_iterate_summary(traj_C_q3_newton, vals_C_q3_newton, "Benchmark C: Newton")
print_method_comparison(results_C_q3, "Benchmark C")
print_head_tail(upd_C_q3_gd, "GD update magnitudes")
print_head_tail(upd_C_q3_newton, "Newton update magnitudes")
#'''

#-PLOT-#
#'''
#a(1D local approxs)#
plot_local_approxs(x_grid_1d, g_vals_1d, g_lin_1d, g_quad_1d, x0_1d)

###c(objective value vs iteration)###
plot_objective_1x2(results_A_q3, 'Benchmark A: Objective vs Iteration')
plot_objective_1x2(results_B_q3, 'Benchmark B: Objective vs Iteration')
plot_objective_1x2(results_C_q3, 'Benchmark C: Objective vs Iteration')

####d(contour plots + opt traj.)####
plot_contour_trajectory_1x2(
    f_B,
    results_B_q3,
    x1_range=(-2.0, 2.5),
    x2_range=(0.5, 4.5),
    title='Benchmark B: Contour & Optimisation Trajectories',
    levels=25
)

plot_contour_trajectory_1x2(
    f_C,
    results_C_q3,
    x1_range=(-1.8, 1.8),
    x2_range=(-0.5, 2.0),
    title='Benchmark C: Contour & Optimisation Trajectories',
    levels=30
)

#####e(update magnitude vs iteration)#####
plot_update_magnitude(
    upd_A_q3_gd, upd_A_q3_newton,
    'Benchmark A: Update Magnitude vs Iteration'
)

plot_update_magnitude(
    upd_B_q3_gd, upd_B_q3_newton,
    'Benchmark B: Update Magnitude vs Iteration'
)

plot_update_magnitude(
    upd_C_q3_gd, upd_C_q3_newton,
    'Benchmark C: Update Magnitude vs Iteration'
)
#'''

#'''
#-----------------Q4-----------------------
print("----------Q4----------")

#a(derivative approximation + derivative-free optimisation)#

# forward finite-difference gradient approximation
def grad_finite_diff(f, x, delta):
    n = len(x)
    g = np.zeros(n)
    fx = f(x)

    for i in range(n):
        e = np.zeros(n)
        e[i] = 1.0
        g[i] = (f(x + delta * e) - fx) / delta

    return g

# finite-difference gradient descent
def finite_diff_gd(f, x0, alpha, delta, n_iters=120):
    x = x0.copy()

    xs = [x.copy()]
    vals = [f(x)]

    for _ in range(n_iters):
        g = grad_finite_diff(f, x, delta)
        x = x - alpha * g

        xs.append(x.copy())
        vals.append(f(x))

    return np.array(xs), np.array(vals)

# Nesterov random search
def nesterov_random_search(f, x0, alpha, delta, n_iters=220, seed=123):
    rng = np.random.default_rng(seed)

    x = x0.copy()
    xs = [x.copy()]
    vals = [f(x)]

    for _ in range(n_iters):
        u = rng.normal(size=len(x))
        u = u / np.linalg.norm(u)

        directional_est = (f(x + delta * u) - f(x)) / delta
        x = x - alpha * directional_est * u

        xs.append(x.copy())
        vals.append(f(x))

    return np.array(xs), np.array(vals)

# Nelder-Mead simplex method for 2D
def nelder_mead_2d(f, x0, step=0.35, n_iters=160, alpha=1.0, gamma=2.0, rho=0.5, sigma=0.5):
    x0 = x0.copy()

    simplex = np.array([
        x0,
        x0 + np.array([step, 0.0]),
        x0 + np.array([0.0, step])
    ])

    traj_best = []
    vals_best = []
    simplex_hist = []

    for _ in range(n_iters):
        fvals = np.array([f(p) for p in simplex])
        idx = np.argsort(fvals)

        simplex = simplex[idx]
        fvals = fvals[idx]

        best = simplex[0].copy()
        worst = simplex[-1].copy()
        second_worst = simplex[-2].copy()

        traj_best.append(best.copy())
        vals_best.append(fvals[0])
        simplex_hist.append(simplex.copy())

        centroid = 0.5 * (simplex[0] + simplex[1])

        # reflection
        xr = centroid + alpha * (centroid - worst)
        fr = f(xr)

        if fvals[0] <= fr < fvals[1]:
            simplex[-1] = xr
            continue

        # expansion
        if fr < fvals[0]:
            xe = centroid + gamma * (xr - centroid)
            fe = f(xe)

            if fe < fr:
                simplex[-1] = xe
            else:
                simplex[-1] = xr
            continue

        # contraction
        if fr < fvals[2]:
            xc = centroid + rho * (xr - centroid)
            fc = f(xc)
            if fc <= fr:
                simplex[-1] = xc
                continue
        else:
            xc = centroid + rho * (worst - centroid)
            fc = f(xc)
            if fc < fvals[2]:
                simplex[-1] = xc
                continue

        # shrink
        simplex[1] = simplex[0] + sigma * (simplex[1] - simplex[0])
        simplex[2] = simplex[0] + sigma * (simplex[2] - simplex[0])

    # store final best point after last update
    fvals = np.array([f(p) for p in simplex])
    idx = np.argsort(fvals)
    simplex = simplex[idx]
    fvals = fvals[idx]

    traj_best.append(simplex[0].copy())
    vals_best.append(fvals[0])
    simplex_hist.append(simplex.copy())

    return np.array(traj_best), np.array(vals_best), simplex_hist

# brute-force grid search on Benchmark C
def grid_search_2d(f, x1_range=(-2, 2), x2_range=(-1, 3), grid_n=55):
    x1_vals = np.linspace(x1_range[0], x1_range[1], grid_n)
    x2_vals = np.linspace(x2_range[0], x2_range[1], grid_n)

    sampled_points = []
    sampled_vals = []
    best_so_far = []

    best_val = np.inf
    best_point = None

    for x1 in x1_vals:
        for x2 in x2_vals:
            p = np.array([x1, x2])
            val = f(p)

            sampled_points.append(p.copy())
            sampled_vals.append(val)

            if val < best_val:
                best_val = val
                best_point = p.copy()

            best_so_far.append(best_val)

    return (
        np.array(sampled_points),
        np.array(sampled_vals),
        np.array(best_so_far),
        best_point,
        best_val
    )

#-------------------plot helper funcs-------------------#

##b(objective value vs iteration for Benchmark B methods)##
def plot_objective_2x2(results, title):
    method_names = list(results.keys())
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    axes = axes.flatten()

    for i, method_name in enumerate(method_names):
        ax = axes[i]
        vals = results[method_name]['vals']
        ax.plot(vals, linewidth=1.8)
        ax.set_title(method_name)
        ax.set_xlabel('Iteration')
        ax.set_ylabel('Objective value')
        ax.grid(True)

    fig.suptitle(title, fontsize=14)
    plt.tight_layout()
    plt.show()

###c(contour plots + trajectories for Benchmark B methods)###
def plot_contour_trajectory_2x2(f, results, x1_range, x2_range, title, levels=30):
    method_names = list(results.keys())

    x1 = np.linspace(x1_range[0], x1_range[1], 400)
    x2 = np.linspace(x2_range[0], x2_range[1], 400)
    X1, X2 = np.meshgrid(x1, x2)
    Z = np.zeros_like(X1)

    for i in range(X1.shape[0]):
        for j in range(X1.shape[1]):
            Z[i, j] = f(np.array([X1[i, j], X2[i, j]]))

    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    axes = axes.flatten()

    for i, method_name in enumerate(method_names):
        ax = axes[i]
        traj = results[method_name]['traj']

        cs = ax.contour(X1, X2, Z, levels=levels)
        ax.clabel(cs, inline=True, fontsize=7)
        ax.plot(traj[:, 0], traj[:, 1], 'ro-', markersize=2.5, linewidth=1.2)

        ax.set_title(method_name)
        ax.set_xlabel(r'$x_1$')
        ax.set_ylabel(r'$x_2$')
        ax.grid(True)

    fig.suptitle(title, fontsize=14)
    plt.tight_layout()
    plt.show()

####d(Nelder-Mead trajectory on Benchmark C)####
def plot_nelder_mead_trajectory(f, traj, x1_range, x2_range, title, levels=30):
    x1 = np.linspace(x1_range[0], x1_range[1], 400)
    x2 = np.linspace(x2_range[0], x2_range[1], 400)
    X1, X2 = np.meshgrid(x1, x2)
    Z = np.zeros_like(X1)

    for i in range(X1.shape[0]):
        for j in range(X1.shape[1]):
            Z[i, j] = f(np.array([X1[i, j], X2[i, j]]))

    plt.figure(figsize=(7, 5.5))
    cs = plt.contour(X1, X2, Z, levels=levels)
    plt.clabel(cs, inline=True, fontsize=7)

    plt.plot(traj[:, 0], traj[:, 1], 'ro-', markersize=2.5, linewidth=1.2, label='Best point trajectory')
    plt.xlabel(r'$x_1$')
    plt.ylabel(r'$x_2$')
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()

#####e(grid-search sampling pattern + best-so-far value)#####
def plot_grid_search_results(sampled_points, best_so_far, best_point, title):
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))

    axes[0].scatter(sampled_points[:, 0], sampled_points[:, 1], s=8)
    axes[0].scatter(best_point[0], best_point[1], s=60, marker='x', label='Best point')
    axes[0].set_xlabel(r'$x_1$')
    axes[0].set_ylabel(r'$x_2$')
    axes[0].set_title('Sampling pattern')
    axes[0].legend()
    axes[0].grid(True)

    axes[1].plot(best_so_far, linewidth=1.8)
    axes[1].set_xlabel('Sample index')
    axes[1].set_ylabel('Best-so-far objective')
    axes[1].set_title('Best-so-far value')
    axes[1].grid(True)

    fig.suptitle(title, fontsize=14)
    plt.tight_layout()
    plt.show()

#-----------------Q4 Part A: Benchmark B-----------------------
print("\n===== Benchmark B: Finite Differences and Random Search =====")

x0_B_q4 = np.array([-1.5, 4.5])

# exact GD baseline
traj_B_q4_gd, vals_B_q4_gd = gradient_descent_constant(
    f_B, grad_B, x0_B_q4, alpha=0.06, n_iters=120
)

# finite-difference GD (good delta)
traj_B_q4_fd_good, vals_B_q4_fd_good = finite_diff_gd(
    f_B, x0_B_q4, alpha=0.08, delta=0.05, n_iters=120
)

# finite-difference GD (poor delta)
traj_B_q4_fd_poor, vals_B_q4_fd_poor = finite_diff_gd(
    f_B, x0_B_q4, alpha=0.08, delta=0.8, n_iters=120
)

# Nesterov random search
traj_B_q4_nrs, vals_B_q4_nrs = nesterov_random_search(
    f_B, x0_B_q4, alpha=0.025, delta=0.08, n_iters=220, seed=321
)

results_B_q4 = {
    'Exact GD': {'traj': traj_B_q4_gd, 'vals': vals_B_q4_gd},
    'FD GD (good)': {'traj': traj_B_q4_fd_good, 'vals': vals_B_q4_fd_good},
    'FD GD (poor)': {'traj': traj_B_q4_fd_poor, 'vals': vals_B_q4_fd_poor},
    'Random search': {'traj': traj_B_q4_nrs, 'vals': vals_B_q4_nrs}
}

#'''
print_iterate_summary(traj_B_q4_gd, vals_B_q4_gd, "Q4 Benchmark B: exact GD")
print_iterate_summary(traj_B_q4_fd_good, vals_B_q4_fd_good, "Q4 Benchmark B: FD GD good delta")
print_iterate_summary(traj_B_q4_fd_poor, vals_B_q4_fd_poor, "Q4 Benchmark B: FD GD poor delta")
print_iterate_summary(traj_B_q4_nrs, vals_B_q4_nrs, "Q4 Benchmark B: Nesterov random search")
print_method_comparison(results_B_q4, "Q4 Benchmark B")
#'''

#-----------------Q4 Part B: Benchmark C-----------------------
print("\n===== Benchmark C: Nelder-Mead and Grid Search =====")

x0_C_q4_nm = np.array([-1.2, 1.0])

traj_C_q4_nm, vals_C_q4_nm, simplex_hist_C_q4 = nelder_mead_2d(
    f_C, x0_C_q4_nm, step=0.35, n_iters=160
)

grid_points_C_q4, grid_vals_C_q4, grid_best_so_far_C_q4, best_point_C_q4, best_val_C_q4 = grid_search_2d(
    f_C, x1_range=(-2, 2), x2_range=(-1, 3), grid_n=55
)

#'''
print_iterate_summary(traj_C_q4_nm, vals_C_q4_nm, "Q4 Benchmark C: Nelder-Mead")
print_vector("Grid-search best point", best_point_C_q4)
print(f"Grid-search best value: {best_val_C_q4:.6f}")
print_head_tail(grid_best_so_far_C_q4, "Grid-search best-so-far values")
#'''

#-PLOT-#
#'''
##b(objective value vs iteration)##
plot_objective_2x2(results_B_q4, 'Benchmark B: Objective vs Iteration')

###c(contour plots + opt. traj.)###
plot_contour_trajectory_2x2(
    f_B,
    results_B_q4,
    x1_range=(-2.0, 2.5),
    x2_range=(0.5, 4.5),
    title='Benchmark B: Contour & Optimisation Trajectories',
    levels=25
)

####d(Nelder-Mead trajectory on Benchmark C)####
plot_nelder_mead_trajectory(
    f_C,
    traj_C_q4_nm,
    x1_range=(-2.0, 2.0),
    x2_range=(-1.0, 3.0),
    title='Benchmark C: Nelder-Mead Trajectory',
    levels=30
)

#####e(grid-search sampling pattern + best-so-far value)#####
plot_grid_search_results(
    grid_points_C_q4,
    grid_best_so_far_C_q4,
    best_point_C_q4,
    'Benchmark C: Grid Search Results'
)
#'''


#'''
#-----------------Q5-----------------------
print("----------Q5----------")

#1(unconstrained GD, projected GD, and penalty GD)#

# projection onto feasible set x1 >= 0.5
def proj_x1_ge_05(x):
    y = x.copy()
    y[0] = max(0.5, y[0])
    return y

# projected gradient descent
def projected_gradient_descent(f, grad_f, x0, alpha, proj, n_iters=100):
    x = x0.copy()

    xs = [x.copy()]
    vals = [f(x)]

    for _ in range(n_iters):
        x = proj(x - alpha * grad_f(x))
        xs.append(x.copy())
        vals.append(f(x))

    return np.array(xs), np.array(vals)

# penalised objective for x1 >= 0.5
def penalty_q5(x, lam):
    x1 = x[0]
    return lam * max(0.0, 0.5 - x1)

def F_q5(x, lam):
    return f_B(x) + penalty_q5(x, lam)

# subgradient of penalised objective
def subgrad_F_q5(x, lam):
    g = grad_B(x).copy()

    if x[0] < 0.5:
        g += np.array([-lam, 0.0])

    return g

# penalty method GD
def penalty_gradient_descent(x0, alpha, lam, n_iters=100):
    x = x0.copy()

    xs = [x.copy()]
    vals = [F_q5(x, lam)]
    orig_vals = [f_B(x)]
    violations = [max(0.0, 0.5 - x[0])]

    for _ in range(n_iters):
        x = x - alpha * subgrad_F_q5(x, lam)

        xs.append(x.copy())
        vals.append(F_q5(x, lam))
        orig_vals.append(f_B(x))
        violations.append(max(0.0, 0.5 - x[0]))

    return np.array(xs), np.array(vals), np.array(orig_vals), np.array(violations)

# helper to store violation
def build_violation_hist(traj):
    return np.maximum(0.0, 0.5 - traj[:, 0])

#-------------------plot helper funcs-------------------#

##2(objective or penalised objective vs iteration)##
def plot_q5_objectives(results, title):
    method_names = list(results.keys())
    fig, axes = plt.subplots(2, 3, figsize=(14, 8))
    axes = axes.flatten()

    for i, method_name in enumerate(method_names):
        ax = axes[i]
        vals = results[method_name]['vals']
        ax.plot(vals, linewidth=1.8)
        ax.set_title(method_name)
        ax.set_xlabel('Iteration')
        ax.set_ylabel('Objective / penalised objective')
        ax.grid(True)

    axes[-1].axis('off')

    fig.suptitle(title, fontsize=14)
    plt.tight_layout()
    plt.show()

###3(contour plot w boundary + optimisation paths)###
def plot_q5_contour_paths(f, results, x1_range, x2_range, title, levels=30):
    x1 = np.linspace(x1_range[0], x1_range[1], 400)
    x2 = np.linspace(x2_range[0], x2_range[1], 400)
    X1, X2 = np.meshgrid(x1, x2)
    Z = np.zeros_like(X1)

    for i in range(X1.shape[0]):
        for j in range(X1.shape[1]):
            Z[i, j] = f(np.array([X1[i, j], X2[i, j]]))

    plt.figure(figsize=(8, 6))
    cs = plt.contour(X1, X2, Z, levels=levels)
    plt.clabel(cs, inline=True, fontsize=7)

    # feasible boundary x1 = 0.5
    plt.axvline(0.5, color='k', linewidth=2, linestyle='--', label=r'Feasible boundary $x_1=0.5$')

    for method_name, result in results.items():
        traj = result['traj']
        plt.plot(traj[:, 0], traj[:, 1], marker='o', markersize=2.2, linewidth=1.2, label=method_name)

    plt.xlabel(r'$x_1$')
    plt.ylabel(r'$x_2$')
    plt.title(title)
    plt.legend(fontsize=8)
    plt.grid(True)
    plt.show()

####4(constraint violation(log scale))####
def plot_q5_constraint_violation(results, title):
    plt.figure(figsize=(8, 5))

    for method_name, result in results.items():
        viol = np.maximum(result['violation'], 1e-12)
        plt.plot(viol, linewidth=1.8, label=method_name)

    plt.yscale('log')
    plt.xlabel('Iteration')
    plt.ylabel(r'Constraint violation $\max(0,\,0.5-x_1)$')
    plt.title(title)
    plt.legend(fontsize=8)
    plt.grid(True)
    plt.show()

#####5(same constraint violation(0-30 iters))#####
def plot_q5_constraint_violation_zoom(results, title, k=30):
    plt.figure(figsize=(8, 5))

    for method_name, result in results.items():
        viol = np.maximum(result['violation'], 1e-12)
        plt.plot(np.arange(min(k, len(viol))), viol[:k], linewidth=1.8, label=method_name)

    plt.yscale('log')
    plt.xlabel('Iteration')
    plt.ylabel(r'Constraint violation $\max(0,\,0.5-x_1)$')
    plt.title(title)
    plt.legend(fontsize=8)
    plt.grid(True)
    plt.show()

#-----------------Q5: run all methods-----------------------
print("\n===== Benchmark B with constraint x1 >= 0.5 =====")

x0_q5 = np.array([0.2, 4.0])

# unconstrained GD baseline
traj_q5_unc, vals_q5_unc = gradient_descent_constant(
    f_B, grad_B, x0_q5, alpha=0.07, n_iters=100
)
viol_q5_unc = build_violation_hist(traj_q5_unc)

# projected GD
traj_q5_proj, vals_q5_proj = projected_gradient_descent(
    f_B, grad_B, x0_q5, alpha=0.08, proj=proj_x1_ge_05, n_iters=100
)
viol_q5_proj = build_violation_hist(traj_q5_proj)

# penalty GD: lambda = 0.15
traj_q5_pen015, vals_q5_pen015, orig_q5_pen015, viol_q5_pen015 = penalty_gradient_descent(
    x0_q5, alpha=0.05, lam=0.15, n_iters=100
)

# penalty GD: lambda = 1.8
traj_q5_pen18, vals_q5_pen18, orig_q5_pen18, viol_q5_pen18 = penalty_gradient_descent(
    x0_q5, alpha=0.05, lam=1.8, n_iters=100
)

# penalty GD: lambda = 4.5
traj_q5_pen45, vals_q5_pen45, orig_q5_pen45, viol_q5_pen45 = penalty_gradient_descent(
    x0_q5, alpha=0.03, lam=4.5, n_iters=100
)

results_q5 = {
    'Unconstrained GD': {'traj': traj_q5_unc, 'vals': vals_q5_unc, 'violation': viol_q5_unc},
    'Projected GD': {'traj': traj_q5_proj, 'vals': vals_q5_proj, 'violation': viol_q5_proj},
    r'Penalty GD ($\lambda=0.15$)': {'traj': traj_q5_pen015, 'vals': vals_q5_pen015, 'violation': viol_q5_pen015},
    r'Penalty GD ($\lambda=1.8$)': {'traj': traj_q5_pen18, 'vals': vals_q5_pen18, 'violation': viol_q5_pen18},
    r'Penalty GD ($\lambda=4.5$)': {'traj': traj_q5_pen45, 'vals': vals_q5_pen45, 'violation': viol_q5_pen45}
}

#'''
print_iterate_summary(traj_q5_unc, vals_q5_unc, "Q5 unconstrained GD")
print_iterate_summary(traj_q5_proj, vals_q5_proj, "Q5 projected GD")
print_iterate_summary(traj_q5_pen015, vals_q5_pen015, "Q5 penalty GD lambda=0.15")
print_iterate_summary(traj_q5_pen18, vals_q5_pen18, "Q5 penalty GD lambda=1.8")
print_iterate_summary(traj_q5_pen45, vals_q5_pen45, "Q5 penalty GD lambda=4.5")

print(f"\nFinal constraint violation (unconstrained GD): {viol_q5_unc[-1]:.6f}")
print(f"Final constraint violation (projected GD):     {viol_q5_proj[-1]:.6f}")
print(f"Final constraint violation (penalty GD, 0.15): {viol_q5_pen015[-1]:.6f}")
print(f"Final constraint violation (penalty GD, 1.8):  {viol_q5_pen18[-1]:.6f}")
print(f"Final constraint violation (penalty GD, 4.5):  {viol_q5_pen45[-1]:.6f}")
#'''

#-PLOT-#
#'''

##2(objective or penalised objective vs iteration)##
plot_q5_objectives(results_q5, 'Benchmark B with constraint: Objective / Penalised Objective vs Iteration')

###3(contour plot w boundary + optimisation paths)###
plot_q5_contour_paths(
    f_B,
    results_q5,
    x1_range=(-0.5, 2.0),
    x2_range=(1.0, 4.5),
    title='Benchmark B with constraint: Contour Plot and Optimisation Paths',
    levels=25
)

####4(constraint violation(log scale))####
plot_q5_constraint_violation(
    results_q5,
    'Benchmark B with constraint: Constraint Violation (log scale)'
)

#####5(same constraint violation(0-30 iters))#####
plot_q5_constraint_violation_zoom(
    results_q5,
    'Benchmark B with constraint: Constraint Violation, First 30 Iterations',
    k=30
)
#'''


#'''
#-----------------Q6-----------------------
print("----------Q6----------")

#a(linear programme + Frank-Wolfe)# 

# feasible set X = {x in R^2 : 0.5 <= x1 <= 5, -5 <= x2 <= 10}
vertices_X = np.array([
    [0.5, -5.0],
    [5.0, -5.0],
    [5.0, 10.0],
    [0.5, 10.0]
])

# linear objective for LP
a_q6 = np.array([1.0, 2.0])

def f_q6_linear(x):
    return np.dot(a_q6, x)

# interior-optimum objective
def f_q6_interior(x):
    x1, x2 = x
    return (x1 - 1.0)**2 + (x2 - 5.0)**2

def grad_q6_interior(x):
    x1, x2 = x
    return np.array([
        2.0 * (x1 - 1.0),
        2.0 * (x2 - 5.0)
    ])

# boundary-optimum objective
def f_q6_boundary(x):
    x1, x2 = x
    return x1**2 + x2**2

def grad_q6_boundary(x):
    x1, x2 = x
    return np.array([
        2.0 * x1,
        2.0 * x2
    ])

# solve linear subproblem over box X
def linear_subproblem_box(grad):
    z = np.zeros(2)

    # minimise grad[0] * x1 over [0.5, 5]
    if grad[0] >= 0:
        z[0] = 0.5
    else:
        z[0] = 5.0

    # minimise grad[1] * x2 over [-5, 10]
    if grad[1] >= 0:
        z[1] = -5.0
    else:
        z[1] = 10.0

    return z

# brute-force LP solution using vertices
def solve_linear_programme_over_X():
    vals = np.array([f_q6_linear(v) for v in vertices_X])
    idx = np.argmin(vals)
    return vertices_X[idx].copy(), vals[idx], vals

# Frank-Wolfe with x_{k+1} = beta x_k + (1-beta) z_k
def frank_wolfe_box(f, grad_f, x0, beta, n_iters):
    x = x0.copy()

    xs = [x.copy()]
    zs = []
    vals = [f(x)]

    for _ in range(n_iters):
        g = grad_f(x)
        z = linear_subproblem_box(g)

        x = beta * x + (1.0 - beta) * z

        zs.append(z.copy())
        xs.append(x.copy())
        vals.append(f(x))

    return np.array(xs), np.array(zs), np.array(vals)

#-------------------plot helper funcs-------------------#

#1(plot feasible region and contours of linear objective)#
def plot_q6_linear_programme():
    x1 = np.linspace(0.0, 5.5, 300)
    x2 = np.linspace(-5.5, 10.5, 300)
    X1, X2 = np.meshgrid(x1, x2)
    Z = a_q6[0] * X1 + a_q6[1] * X2

    plt.figure(figsize=(7, 5.5))
    cs = plt.contour(X1, X2, Z, levels=20)
    plt.clabel(cs, inline=True, fontsize=7)

    poly = np.array([
        [0.5, -5.0],
        [5.0, -5.0],
        [5.0, 10.0],
        [0.5, 10.0],
        [0.5, -5.0]
    ])
    plt.plot(poly[:, 0], poly[:, 1], 'k-', linewidth=2, label='Feasible region')
    plt.scatter(vertices_X[:, 0], vertices_X[:, 1], s=60, marker='s', label='Vertices')

    lp_sol, lp_val, _ = solve_linear_programme_over_X()
    plt.scatter(lp_sol[0], lp_sol[1], s=80, marker='x', label='LP minimiser')

    plt.xlabel(r'$x_1$')
    plt.ylabel(r'$x_2$')
    plt.title('Linear Programme on Feasible Set')
    plt.legend()
    plt.grid(True)
    plt.show()

##2(Frank-Wolfe convergence curves for interior-optimum case)##
def plot_q6_fw_convergence(vals_beta1, vals_beta2, title):
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    axes[0].plot(vals_beta1, linewidth=1.8, label=r'$\beta=0.90$')
    axes[0].plot(vals_beta2, linewidth=1.8, label=r'$\beta=0.985$')
    axes[0].set_xlabel('Iteration')
    axes[0].set_ylabel('Objective value')
    axes[0].set_title('Objective vs iteration')
    axes[0].legend()
    axes[0].grid(True)

    axes[1].plot(vals_beta1, linewidth=1.8, label=r'$\beta=0.90$')
    axes[1].plot(vals_beta2, linewidth=1.8, label=r'$\beta=0.985$')
    axes[1].set_yscale('log')
    axes[1].set_xlabel('Iteration')
    axes[1].set_ylabel('Objective value (log scale)')
    axes[1].set_title('Objective vs iteration (log scale)')
    axes[1].legend()
    axes[1].grid(True)

    fig.suptitle(title, fontsize=14)
    plt.tight_layout()
    plt.show()

###3(contour plots showing Frank-Wolfe trajectories)###
def plot_q6_fw_trajectory_subplots(f, results, x1_range, x2_range, title, levels=30):
    method_names = list(results.keys())

    x1 = np.linspace(x1_range[0], x1_range[1], 400)
    x2 = np.linspace(x2_range[0], x2_range[1], 400)
    X1, X2 = np.meshgrid(x1, x2)
    Z = np.zeros_like(X1)

    for i in range(X1.shape[0]):
        for j in range(X1.shape[1]):
            Z[i, j] = f(np.array([X1[i, j], X2[i, j]]))

    fig, axes = plt.subplots(1, len(method_names), figsize=(6 * len(method_names), 4.8))
    if len(method_names) == 1:
        axes = [axes]

    poly = np.array([
        [0.5, -5.0],
        [5.0, -5.0],
        [5.0, 10.0],
        [0.5, 10.0],
        [0.5, -5.0]
    ])

    for i, method_name in enumerate(method_names):
        ax = axes[i]
        traj = results[method_name]['traj']

        cs = ax.contour(X1, X2, Z, levels=levels)
        ax.clabel(cs, inline=True, fontsize=7)
        ax.plot(poly[:, 0], poly[:, 1], 'k-', linewidth=2)
        ax.plot(traj[:, 0], traj[:, 1], 'ro-', markersize=2.5, linewidth=1.2)

        ax.set_title(method_name)
        ax.set_xlabel(r'$x_1$')
        ax.set_ylabel(r'$x_2$')
        ax.grid(True)

    fig.suptitle(title, fontsize=14)
    plt.tight_layout()
    plt.show()

####4(plot evolution of xk and zk versus iteration)####
def plot_q6_xz_evolution(traj, zs, title):
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    axes[0].plot(traj[:, 0], label=r'$x_{1}^{(k)}$')
    axes[0].plot(traj[:, 1], label=r'$x_{2}^{(k)}$')
    axes[0].set_xlabel('Iteration')
    axes[0].set_ylabel('Value')
    axes[0].set_title(r'Evolution of $x_k$')
    axes[0].legend()
    axes[0].grid(True)

    axes[1].plot(zs[:, 0], label=r'$z_{1}^{(k)}$')
    axes[1].plot(zs[:, 1], label=r'$z_{2}^{(k)}$')
    axes[1].set_xlabel('Iteration')
    axes[1].set_ylabel('Value')
    axes[1].set_title(r'Evolution of $z_k$')
    axes[1].legend()
    axes[1].grid(True)

    fig.suptitle(title, fontsize=14)
    plt.tight_layout()
    plt.show()

#-----------------Q6 Part I: linear programme-----------------------
print("\n===== Linear Programme over X =====")

lp_sol_q6, lp_val_q6, lp_vertex_vals_q6 = solve_linear_programme_over_X()

print_vector("LP minimiser", lp_sol_q6)
print(f"LP minimum value: {lp_val_q6:.6f}")
print("Vertex objective values:")
for v, val in zip(vertices_X, lp_vertex_vals_q6):
    print(f"  vertex {np.round(v, 6)} -> {val:.6f}")

#-----------------Q6 Part II: Frank-Wolfe for interior optimum-----------------------
print("\n===== Frank-Wolfe: Interior Optimum Case =====")

x0_q6_interior = np.array([1.0, 1.0])

traj_q6_int_090, z_q6_int_090, vals_q6_int_090 = frank_wolfe_box(
    f_q6_interior, grad_q6_interior, x0_q6_interior, beta=0.90, n_iters=180
)

traj_q6_int_0985, z_q6_int_0985, vals_q6_int_0985 = frank_wolfe_box(
    f_q6_interior, grad_q6_interior, x0_q6_interior, beta=0.985, n_iters=180
)

results_q6_interior = {
    r'FW interior ($\beta=0.90$)': {'traj': traj_q6_int_090, 'vals': vals_q6_int_090},
    r'FW interior ($\beta=0.985$)': {'traj': traj_q6_int_0985, 'vals': vals_q6_int_0985}
}

#'''
print_iterate_summary(traj_q6_int_090, vals_q6_int_090, "Q6 interior FW beta=0.90")
print_iterate_summary(traj_q6_int_0985, vals_q6_int_0985, "Q6 interior FW beta=0.985")
#'''

#-----------------Q6 Part III: Frank-Wolfe for boundary optimum-----------------------
print("\n===== Frank-Wolfe: Boundary Optimum Case =====")

x0_q6_boundary = np.array([3.0, 3.0])

traj_q6_bdry, z_q6_bdry, vals_q6_bdry = frank_wolfe_box(
    f_q6_boundary, grad_q6_boundary, x0_q6_boundary, beta=0.93, n_iters=140
)

results_q6_boundary = {
    r'FW boundary ($\beta=0.93$)': {'traj': traj_q6_bdry, 'vals': vals_q6_bdry}
}

#'''
print_iterate_summary(traj_q6_bdry, vals_q6_bdry, "Boundary FW beta=0.93")
#'''

#-PLOT-#
#'''

#1(plot feasible region and contours of linear objective)#
plot_q6_linear_programme()

##2(Frank-Wolfe convergence curves for interior-optimum case)##
plot_q6_fw_convergence(
    vals_q6_int_090, vals_q6_int_0985,
    'Interior Optimum Case: Frank-Wolfe Convergence'
)

###3(contour plots showing Frank-Wolfe trajectories)###
plot_q6_fw_trajectory_subplots(
    f_q6_interior,
    results_q6_interior,
    x1_range=(0.0, 5.5),
    x2_range=(-1.0, 10.5),
    title='Interior Optimum Case: Frank-Wolfe Trajectories',
    levels=25
)

plot_q6_fw_trajectory_subplots(
    f_q6_boundary,
    results_q6_boundary,
    x1_range=(0.0, 5.5),
    x2_range=(-5.5, 5.5),
    title='Boundary Optimum Case: Frank-Wolfe Trajectory',
    levels=25
)

####4(plot evolution of xk and zk versus iteration)####
plot_q6_xz_evolution(
    traj_q6_int_090, z_q6_int_090,
    r'Interior Optimum Case: $x_k$ and $z_k$ Evolution ($\beta=0.90$)'
)

plot_q6_xz_evolution(
    traj_q6_int_0985, z_q6_int_0985,
    r'Interior Optimum Case: $x_k$ and $z_k$ Evolution ($\beta=0.985$)'
)

plot_q6_xz_evolution(
    traj_q6_bdry, z_q6_bdry,
    r'Boundary Optimum Case: $x_k$ and $z_k$ Evolution ($\beta=0.93$)'
)
#'''
