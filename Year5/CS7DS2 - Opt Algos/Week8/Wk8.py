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

def print_q1_feasibility(traj, region):
    x_final = traj[-1]
    x1, x2 = x_final
    print(f"\nFinal feasibility check for {region}:")
    if region == 'X1':
        print(f"x1 - 0.5 = {x1 - 0.5:.6f}")
        print(f"2.5 - x1 = {2.5 - x1:.6f}")
        print(f"x2 - 0.5 = {x2 - 0.5:.6f}")
        print(f"3.5 - x2 = {x2 if False else 3.5 - x2:.6f}")
        if (x1 > 0.5 and x1 < 2.5 and x2 > 0.5 and x2 < 3.5):
            print("Final iterate is in the interior of X1.")
        else:
            print("Final iterate is on the boundary of X1.")
    elif region == 'X2':
        print(f"x1 - 0.5 = {x1 - 0.5:.6f}")
        print(f"x2 - 0.5 = {x2 - 0.5:.6f}")
        print(f"x2 - x1  = {x2 - x1:.6f}")
        if (x1 > 0.5 and x2 > 0.5 and x1 < x2):
            print("Final iterate is in the interior of X2.")
        else:
            print("Final iterate is on the boundary of X2.")

def print_constraint_summary(g1_vals, g2_vals, label):
    print(f"\n--- {label} constraint summary ---")
    print(f"g1 initial: {g1_vals[0]:.6f}, final: {g1_vals[-1]:.6f}, max violation: {np.max(g1_vals):.6f}")
    print(f"g2 initial: {g2_vals[0]:.6f}, final: {g2_vals[-1]:.6f}, max violation: {np.max(g2_vals):.6f}")
    print_head_tail(g1_vals, "g1 values")
    print_head_tail(g2_vals, "g2 values")

def print_lambda_summary(lam_hist, label):
    print(f"\n--- {label} multiplier summary ---")
    print_vector("Initial lambda", lam_hist[0])
    print_vector("Final lambda", lam_hist[-1])
    print(f"lambda1 min/max: {lam_hist[:,0].min():.6f} / {lam_hist[:,0].max():.6f}")
    print(f"lambda2 min/max: {lam_hist[:,1].min():.6f} / {lam_hist[:,1].max():.6f}")
    print_head_tail(lam_hist[:, 0], "lambda1 values")
    print_head_tail(lam_hist[:, 1], "lambda2 values")

def print_fw_summary(traj, zs, vals, beta_label):
    print(f"\n--- Frank-Wolfe summary ({beta_label}) ---")
    print_vector("Initial iterate", traj[0])
    print_vector("Final iterate", traj[-1])
    print(f"Initial objective: {vals[0]:.6f}")
    print(f"Final objective:   {vals[-1]:.6f}")
    print_head_tail(vals, "Objective values")
    print_head_tail(traj[:, 0], "x1 values")
    print_head_tail(traj[:, 1], "x2 values")
    print_head_tail(zs[:, 0], "z1 values")
    print_head_tail(zs[:, 1], "z2 values")

    unique_z, counts = np.unique(zs, axis=0, return_counts=True)
    print("Selected vertices and counts:")
    for z, c in zip(unique_z, counts):
        print(f"  vertex {np.round(z,6)} chosen {c} times")
#'''

#'''
#-----------------Q1-----------------------
print("----------Q1----------")
#a(Objective and gradient)#
def f(x):
    x1, x2 = x
    return (x1 - 1.2)**2 + 2*(x2 - 2.5)**2 + 0.4*x1*x2

def grad_f(x):
    x1, x2 = x
    return np.array([
        2*x1 + 0.4*x2 - 2.4,
        0.4*x1 + 4*x2 - 10
    ])

# projected gradient descent
def pgd(x0, alpha, proj, n_iters=60):
    xs = [x0.copy()]
    fs = [f(x0)]
    x = x0.copy()

    for _ in range(n_iters):
        x = proj(x - alpha * grad_f(x))
        xs.append(x.copy())
        fs.append(f(x))

    return np.array(xs), np.array(fs)

##b(project onto X1 by elementwise clipping)##
# X1 = {0.5 <= x1 <= 2.5, 0.5 <= x2 <= 3.5}
def proj_X1(x):
    return np.array([
        np.clip(x[0], 0.5, 2.5),
        np.clip(x[1], 0.5, 3.5)
    ])


###c(projections for X2)###
# X2 = {x1 >= 0.5, x2 >= 0.5, x1 <= x2}
def proj_c1(x):
    # project onto x1 >= 0.5
    y = x.copy()
    y[0] = max(y[0], 0.5)
    return y

def proj_c2(x):
    # project onto x2 >= 0.5
    y = x.copy()
    y[1] = max(y[1], 0.5)
    return y

def proj_c3(x):
    # project onto x1 <= x2
    y = x.copy()
    if y[0] > y[1]:     # if gt (NOT leq), project orthogonally on line x1 = x2
        avg = 0.5 * (y[0] + y[1])
        y[0] = avg
        y[1] = avg
    return y

def proj_X2_repeat(x, num_iters=20):
    y = x.copy()
    for _ in range(num_iters):
        y = proj_c1(y)
        y = proj_c2(y)
        y = proj_c3(y)
    return y

# Params
alpha = 0.2
n_iters = 60
x0 = np.array([2.4, 0.7])

traj_X1, vals_X1 = pgd(x0, alpha, proj_X1, n_iters=n_iters)

x0_X2 = proj_X2_repeat(x0)
traj_X2, vals_X2 = pgd(x0_X2, alpha, proj_X2_repeat, n_iters=n_iters)

print("Final iterate for X1:", traj_X1[-1])
print("Final objective for X1:", vals_X1[-1])

print("Initial projected point for X2:", x0_X2)
print("Final iterate for X2:", traj_X2[-1])
print("Final objective for X2:", vals_X2[-1])

print_iterate_summary(traj_X1, vals_X1, "Q1: PGD on X1")
print_q1_feasibility(traj_X1, "X1")

print_iterate_summary(traj_X2, vals_X2, "Q1: PGD on X2")
print_q1_feasibility(traj_X2, "X2")

print("\nQ1 contour-plot points:")
print_vector("X1 start", traj_X1[0])
print_vector("X1 end", traj_X1[-1])
print_vector("X2 start", traj_X2[0])
print_vector("X2 end", traj_X2[-1])

####d&e(Plots)####
# Plotting helper
def plot_results(traj, vals, title, region='X1'):
    # contour grid
    x1_grid = np.linspace(0.0, 3.0, 300)
    x2_grid = np.linspace(0.0, 4.0, 300)
    X1g, X2g = np.meshgrid(x1_grid, x2_grid)
    Z = (X1g - 1.2)**2 + 2*(X2g - 2.5)**2 + 0.4*X1g*X2g

    # (I) contour plot
    plt.figure(figsize=(6, 5))
    cs = plt.contour(X1g, X2g, Z, levels=25)
    plt.clabel(cs, inline=True, fontsize=8)

    if region == 'X1':
        # rectangle boundary
        plt.plot([0.5, 2.5, 2.5, 0.5, 0.5],
                 [0.5, 0.5, 3.5, 3.5, 0.5], 'k-', linewidth=2, label='Feasible region')
    elif region == 'X2':
        # show the region boundary x1=0.5, x2=0.5, x1=x2
        xx = np.linspace(0.5, 3.0, 200)
        plt.plot([0.5, 0.5], [0.5, 4.0], 'k-', linewidth=2)
        plt.plot([0.0, 4.0], [0.5, 0.5], 'k-', linewidth=2)
        plt.plot(xx, xx, 'k-', linewidth=2, label='Boundary x1 = x2')

    plt.plot(traj[:, 0], traj[:, 1], 'ro-', markersize=3, linewidth=1.5, label='Trajectory')
    plt.xlabel(r'$x_1$')
    plt.ylabel(r'$x_2$')
    plt.title(f'{title}: contour + trajectory')
    plt.legend()
    plt.grid(True)
    plt.show()

    # (II) objective value vs iteration
    plt.figure(figsize=(6, 4))
    plt.plot(vals, 'o-', markersize=3)
    plt.xlabel('Iteration')
    plt.ylabel(r'$f(x^{(t)})$')
    plt.title(f'{title}: objective vs iteration')
    plt.grid(True)
    plt.show()

    # (III) x1 and x2 vs iteration
    plt.figure(figsize=(6, 4))
    plt.plot(traj[:, 0], 'o-', markersize=3, label=r'$x_1^{(t)}$')
    plt.plot(traj[:, 1], 's-', markersize=3, label=r'$x_2^{(t)}$')
    plt.xlabel('Iteration')
    plt.ylabel('Value')
    plt.title(f'{title}: coordinates vs iteration')
    plt.legend()
    plt.grid(True)
    plt.show()

#d
plot_results(traj_X1, vals_X1, 'PGD on X1', region='X1')
#e
plot_results(traj_X2, vals_X2, 'PGD on X2', region='X2')
#'''

#'''
#-----------------Q2-----------------------
print("----------Q2----------")
#a(Objective and constraints)#
def f(x):
    x1, x2 = x
    return (x1 - 0.2)**2 + (x2 - 2.0)**2

def g1(x):
    x1, x2 = x
    return 0.5 - x1

def g2(x):
    x1, x2 = x
    return 1.0 - x1*x2

def grad_f(x):
    x1, x2 = x
    return np.array([
        2*(x1 - 0.2),
        2*(x2 - 2.0)
    ])

def grad_g1(x):
    return np.array([-1.0, 0.0])

def grad_g2(x):
    x1, x2 = x
    return np.array([-x2, -x1])

#a(Penalised objective F = f + Q)
def penalty(x, lam1, lam2):
    return lam1 * max(0.0, g1(x)) + lam2 * max(0.0, g2(x))

def F(x, lam1, lam2):
    return f(x) + penalty(x, lam1, lam2)

def subgrad_F(x, lam1, lam2):
    grad = grad_f(x).copy()

    if g1(x) > 0:
        grad += lam1 * grad_g1(x)

    if g2(x) > 0:
        grad += lam2 * grad_g2(x)

    return grad

##b(Fixed-penalty gradient descent)##
def gradient_descent_penalty(x0, alpha, lam1, lam2, n_iters=100):
    x = x0.copy()
    xs = [x.copy()]
    vals = [F(x, lam1, lam2)]
    g1_vals = [g1(x)]
    g2_vals = [g2(x)]

    for _ in range(n_iters):
        x = x - alpha * subgrad_F(x, lam1, lam2)
        xs.append(x.copy())
        vals.append(F(x, lam1, lam2))
        g1_vals.append(g1(x))
        g2_vals.append(g2(x))

    return np.array(xs), np.array(vals), np.array(g1_vals), np.array(g2_vals)

###c(Primal-dual iteration)###
def primal_dual(x0, alpha=0.06, beta=0.08, n_iters=100):
    x = x0.copy()
    lam = np.array([0.0, 0.0])  # [lam1, lam2]

    xs = [x.copy()]
    lam_hist = [lam.copy()]
    vals = [f(x)]
    g1_vals = [g1(x)]
    g2_vals = [g2(x)]

    for _ in range(n_iters):
        # primal step
        grad_L = grad_f(x) + lam[0]*grad_g1(x) + lam[1]*grad_g2(x)
        x = x - alpha * grad_L

        # dual step
        lam[0] = max(0.0, lam[0] + beta * g1(x))
        lam[1] = max(0.0, lam[1] + beta * g2(x))

        xs.append(x.copy())
        lam_hist.append(lam.copy())
        vals.append(f(x))
        g1_vals.append(g1(x))
        g2_vals.append(g2(x))

    return np.array(xs), np.array(lam_hist), np.array(vals), np.array(g1_vals), np.array(g2_vals)

#b&c(Params
x0 = np.array([1.4, 0.6])
alpha_pen = 0.08
n_iters_pen = 100

##b(Fixed-penalty cases)##
traj_small, vals_small, g1_small, g2_small = gradient_descent_penalty(
    x0, alpha_pen, lam1=0.5, lam2=0.5, n_iters=n_iters_pen
)

traj_large, vals_large, g1_large, g2_large = gradient_descent_penalty(
    x0, alpha_pen, lam1=4.0, lam2=4.0, n_iters=n_iters_pen
)

print("Final iterate (small penalty):", traj_small[-1])
print("Final g1, g2:", g1_small[-1], g2_small[-1])

print("Final iterate (large penalty):", traj_large[-1])
print("Final g1, g2:", g1_large[-1], g2_large[-1])

###c(Primal-dual)###
traj_pd, lam_pd, vals_pd, g1_pd, g2_pd = primal_dual(
    x0, alpha=0.06, beta=0.08, n_iters=100
)

print("Final iterate (primal-dual):", traj_pd[-1])
print("Final lambdas:", lam_pd[-1])
print("Final g1, g2:", g1_pd[-1], g2_pd[-1])

print_iterate_summary(traj_small, vals_small, "Q2: fixed penalty, small weights")
print_constraint_summary(g1_small, g2_small, "Q2: fixed penalty, small weights")

print_iterate_summary(traj_large, vals_large, "Q2: fixed penalty, large weights")
print_constraint_summary(g1_large, g2_large, "Q2: fixed penalty, large weights")

print_iterate_summary(traj_pd, vals_pd, "Q2: primal-dual")
print_constraint_summary(g1_pd, g2_pd, "Q2: primal-dual")
print_lambda_summary(lam_pd, "Q2: primal-dual")

def print_q2_feasibility(x, label):
    print(f"\nFinal feasibility check for {label}:")
    print_vector("Final iterate", x)
    print(f"g1(final) = {g1(x):.6f}")
    print(f"g2(final) = {g2(x):.6f}")
    if g1(x) <= 0 and g2(x) <= 0:
        print("Final iterate is feasible.")
    else:
        print("Final iterate is NOT feasible.")

print_q2_feasibility(traj_small[-1], "Q2 small penalty")
print_q2_feasibility(traj_large[-1], "Q2 large penalty")
print_q2_feasibility(traj_pd[-1], "Q2 primal-dual")

####d&e(Plots)####
# helper funcs
def contour_background():
    x1 = np.linspace(0.0, 2.2, 400)
    x2 = np.linspace(0.0, 3.0, 400)
    X1, X2 = np.meshgrid(x1, x2)
    Z = (X1 - 0.2)**2 + (X2 - 2.0)**2
    return X1, X2, Z

def feasible_boundary():
    # boundary x1 = 0.5 and x2 = 1/x1
    x1_curve = np.linspace(0.5, 2.2, 400)
    x2_curve = 1.0 / x1_curve
    return x1_curve, x2_curve

def plot_contour_with_trajectory(traj, title):
    X1, X2, Z = contour_background()
    x1_curve, x2_curve = feasible_boundary()

    plt.figure(figsize=(6, 5))
    cs = plt.contour(X1, X2, Z, levels=25)
    plt.clabel(cs, inline=True, fontsize=8)

    # feasible region shading
    plt.fill_between(x1_curve, x2_curve, 3.0, alpha=0.15)
    plt.plot([0.5, 0.5], [0.0, 3.0], 'k-', linewidth=2, label=r'$x_1=0.5$')
    plt.plot(x1_curve, x2_curve, 'k--', linewidth=2, label=r'$x_1x_2=1$')

    plt.plot(traj[:, 0], traj[:, 1], 'ro-', markersize=3, linewidth=1.5, label='Trajectory')
    plt.xlabel(r'$x_1$')
    plt.ylabel(r'$x_2$')
    plt.xlim(0.0, 2.2)
    plt.ylim(0.0, 3.0)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()

####d(Fixed-penalty plots)####
#(I) s-penalty contour + trajectory
plot_contour_with_trajectory(traj_small, 'Fixed penalty (small weights)')

#(II) l-penalty contour + trajectory
plot_contour_with_trajectory(traj_large, 'Fixed penalty (large weights)')

#(III) constraint violations vs iteration
plt.figure(figsize=(7, 4))
plt.plot(g1_small, label='g1 small penalty')
plt.plot(g2_small, label='g2 small penalty')
plt.plot(g1_large, '--', label='g1 large penalty')
plt.plot(g2_large, '--', label='g2 large penalty')
plt.axhline(0.0, linewidth=1)
plt.xlabel('Iteration')
plt.ylabel('Constraint value')
plt.title('Constraint violations for fixed-penalty method')
plt.legend()
plt.grid(True)
plt.show()

#####e(Primal-dual plots)#####
#(I) contour + trajectory
plot_contour_with_trajectory(traj_pd, 'Primal-dual method')

#(II) x1 and x2 vs iters
plt.figure(figsize=(7, 4))
plt.plot(traj_pd[:, 0], label=r'$x_1^{(t)}$')
plt.plot(traj_pd[:, 1], label=r'$x_2^{(t)}$')
plt.xlabel('Iteration')
plt.ylabel('Value')
plt.title('Primal-dual: primal variables')
plt.legend()
plt.grid(True)
plt.show()

#(III) lam1 and lam2 vs iters
plt.figure(figsize=(7, 4))
plt.plot(lam_pd[:, 0], label=r'$\lambda_1^{(t)}$')
plt.plot(lam_pd[:, 1], label=r'$\lambda_2^{(t)}$')
plt.xlabel('Iteration')
plt.ylabel('Value')
plt.title('Primal-dual: multipliers')
plt.legend()
plt.grid(True)
plt.show()

#'''


#'''
#-----------------Q3-----------------------
print("----------Q3----------")
# -------------------------------------------------
# Objective and gradient
# -------------------------------------------------
def f(x):
    x1, x2 = x
    return (x1 - 1.5)**2 + (x2 - 1.2)**2

##b##
def grad_f(x):
    x1, x2 = x
    return np.array([
        2*(x1 - 1.5),
        2*(x2 - 1.2)
    ])

#a(easible set vertices)#
vertices = np.array([
    [0.5, 0.5],
    [3.0, 0.5],
    [3.0, 1.0],
    [1.0, 3.0],
    [0.5, 3.0]
])

###c(Frank-Wolfe linear subproblem: min_{x in X} grad^T x)###
def linear_subproblem(grad):
    vals = vertices @ grad
    idx = np.argmin(vals)
    return vertices[idx].copy()

# Frank-Wolfe algorithm: gamma_t = beta^t
def frank_wolfe(x0, beta=0.8, n_iters=60):
    x = x0.copy()
    xs = [x.copy()]
    zs = []
    vals = [f(x)]

    for t in range(n_iters):
        g = grad_f(x)
        z = linear_subproblem(g)
        gamma = beta**t
        x = (1 - gamma) * x + gamma * z

        zs.append(z.copy())
        xs.append(x.copy())
        vals.append(f(x))

    return np.array(xs), np.array(zs), np.array(vals)

#####e(Projection operators for PGD)#####
def proj_c1(x):
    y = x.copy()
    y[0] = max(y[0], 0.5)
    return y

def proj_c2(x):
    y = x.copy()
    y[1] = max(y[1], 0.5)
    return y

def proj_c3(x):
    # x1 + x2 <= 4
    y = x.copy()
    if y[0] + y[1] > 4:
        # orthogonal projection onto line x1+x2=4
        s = (y[0] + y[1] - 4) / 2.0
        y[0] -= s
        y[1] -= s
    return y

def proj_c4(x):
    y = x.copy()
    y[0] = min(y[0], 3.0)
    return y

def proj_c5(x):
    y = x.copy()
    y[1] = min(y[1], 3.0)
    return y

def proj_X_repeat(x, iters=20):
    y = x.copy()
    for _ in range(iters):
        y = proj_c1(y)
        y = proj_c2(y)
        y = proj_c3(y)
        y = proj_c4(y)
        y = proj_c5(y)
    return y

# projected gradient descent func
def pgd(x0, alpha=0.2, n_iters=60):
    x = x0.copy()
    xs = [x.copy()]
    vals = [f(x)]

    for _ in range(n_iters):
        x = proj_X_repeat(x - alpha * grad_f(x))
        xs.append(x.copy())
        vals.append(f(x))

    return np.array(xs), np.array(vals)

# initial point
x0 = np.array([2.8, 0.8])

# Frank-Wolfe for two beta values
traj_fw_08, z_fw_08, vals_fw_08 = frank_wolfe(x0, beta=0.8, n_iters=60)
traj_fw_095, z_fw_095, vals_fw_095 = frank_wolfe(x0, beta=0.95, n_iters=60)

# Projected gradient descent
traj_pgd, vals_pgd = pgd(x0, alpha=0.2, n_iters=60)

print("Final FW iterate (beta=0.8):", traj_fw_08[-1], "f =", vals_fw_08[-1])
print("Final FW iterate (beta=0.95):", traj_fw_095[-1], "f =", vals_fw_095[-1])
print("Final PGD iterate:", traj_pgd[-1], "f =", vals_pgd[-1])

print_fw_summary(traj_fw_08, z_fw_08, vals_fw_08, "beta = 0.8")
print_fw_summary(traj_fw_095, z_fw_095, vals_fw_095, "beta = 0.95")
print_iterate_summary(traj_pgd, vals_pgd, "Q3: projected gradient descent")

def print_q3_feasibility(x, label):
    x1, x2 = x
    print(f"\nFinal feasibility/boundary check for {label}:")
    print_vector("Final iterate", x)
    print(f"x1 - 0.5   = {x1 - 0.5:.6f}")
    print(f"x2 - 0.5   = {x2 - 0.5:.6f}")
    print(f"4 - x1-x2  = {4 - x1 - x2:.6f}")
    print(f"3 - x1     = {3 - x1:.6f}")
    print(f"3 - x2     = {3 - x2:.6f}")
    if (x1 > 0.5 and x2 > 0.5 and x1 + x2 < 4 and x1 < 3 and x2 < 3):
        print("Final iterate is in the interior of X.")
    else:
        print("Final iterate is on the boundary of X.")

print_q3_feasibility(traj_fw_08[-1], "Q3 FW beta=0.8")
print_q3_feasibility(traj_fw_095[-1], "Q3 FW beta=0.95")
print_q3_feasibility(traj_pgd[-1], "Q3 PGD")

# Plot helper func
def plot_contour_and_trajectory(traj, title, z_traj=None):
    x1 = np.linspace(0.0, 3.4, 400)
    x2 = np.linspace(0.0, 3.4, 400)
    X1, X2 = np.meshgrid(x1, x2)
    Z = (X1 - 1.5)**2 + (X2 - 1.2)**2

    plt.figure(figsize=(6, 5))
    cs = plt.contour(X1, X2, Z, levels=25)
    plt.clabel(cs, inline=True, fontsize=8)

    # feasible polygon
    poly = np.array([
        [0.5, 0.5],
        [3.0, 0.5],
        [3.0, 1.0],
        [1.0, 3.0],
        [0.5, 3.0],
        [0.5, 0.5]
    ])
    plt.plot(poly[:, 0], poly[:, 1], 'k-', linewidth=2, label='Feasible region')
    plt.scatter(vertices[:, 0], vertices[:, 1], s=60, marker='s', label='Vertices')

    plt.plot(traj[:, 0], traj[:, 1], 'ro-', markersize=3, linewidth=1.5, label='x trajectory')

    if z_traj is not None:
        plt.scatter(z_traj[:, 0], z_traj[:, 1], marker='x', s=40, label='z points')

    plt.xlabel(r'$x_1$')
    plt.ylabel(r'$x_2$')
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.xlim(0.0, 3.4)
    plt.ylim(0.0, 3.4)
    plt.show()


#d(Frank-Wolfe plots for beta=0.8)
plot_contour_and_trajectory(traj_fw_08, 'Frank-Wolfe (beta = 0.8)', z_traj=z_fw_08)

plt.figure(figsize=(6, 4))
plt.plot(vals_fw_08, 'o-', markersize=3)
plt.xlabel('Iteration')
plt.ylabel(r'$f(x^{(t)})$')
plt.title('FW (beta = 0.8): objective vs iteration')
plt.grid(True)
plt.show()

plt.figure(figsize=(7, 4))
plt.plot(traj_fw_08[:, 0], label=r'$x_1^{(t)}$')
plt.plot(traj_fw_08[:, 1], label=r'$x_2^{(t)}$')
plt.plot(np.arange(len(z_fw_08)), z_fw_08[:, 0], '--', label=r'$z_1^{(t)}$')
plt.plot(np.arange(len(z_fw_08)), z_fw_08[:, 1], '--', label=r'$z_2^{(t)}$')
plt.xlabel('Iteration')
plt.ylabel('Value')
plt.title('FW (beta = 0.8): x and z coordinates')
plt.legend()
plt.grid(True)
plt.show()

#d(Frank-Wolfe plots for beta=0.95)
plot_contour_and_trajectory(traj_fw_095, 'Frank-Wolfe (beta = 0.95)', z_traj=z_fw_095)

plt.figure(figsize=(6, 4))
plt.plot(vals_fw_095, 'o-', markersize=3)
plt.xlabel('Iteration')
plt.ylabel(r'$f(x^{(t)})$')
plt.title('FW (beta = 0.95): objective vs iteration')
plt.grid(True)
plt.show()

plt.figure(figsize=(7, 4))
plt.plot(traj_fw_095[:, 0], label=r'$x_1^{(t)}$')
plt.plot(traj_fw_095[:, 1], label=r'$x_2^{(t)}$')
plt.plot(np.arange(len(z_fw_095)), z_fw_095[:, 0], '--', label=r'$z_1^{(t)}$')
plt.plot(np.arange(len(z_fw_095)), z_fw_095[:, 1], '--', label=r'$z_2^{(t)}$')
plt.xlabel('Iteration')
plt.ylabel('Value')
plt.title('FW (beta = 0.95): x and z coordinates')
plt.legend()
plt.grid(True)
plt.show()

#e(PGD plots)
plot_contour_and_trajectory(traj_pgd, 'Projected Gradient Descent')

plt.figure(figsize=(6, 4))
plt.plot(vals_pgd, 'o-', markersize=3)
plt.xlabel('Iteration')
plt.ylabel(r'$f(x^{(t)})$')
plt.title('PGD: objective vs iteration')
plt.grid(True)
plt.show()

plt.figure(figsize=(7, 4))
plt.plot(traj_pgd[:, 0], label=r'$x_1^{(t)}$')
plt.plot(traj_pgd[:, 1], label=r'$x_2^{(t)}$')
plt.xlabel('Iteration')
plt.ylabel('Value')
plt.title('PGD: coordinates vs iteration')
plt.legend()
plt.grid(True)
plt.show()
#'''
