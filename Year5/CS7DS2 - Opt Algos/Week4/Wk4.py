import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema

#'''
#-----------------Q1-----------------------
print("----------Q1----------")
###I###
def f(x):
    return x[0]**2 + 100*x[1]**2

def grad_f(x):
    return np.array([2*x[0], 200*x[1]])

#init point
x0 = np.array([2.0, 2.0])
T = 200

#--------------------------
########Polyak########
def polyak(x0):
    x = x0.copy()
    values = []
    f_star = 0      #min val

    for k in range(T):
        g = grad_f(x)
        alpha = (f(x) - f_star) / (np.dot(g, g) + 1e-8)
        x = x - alpha * g
        values.append(f(x))
    return values

########RMSProp########
def rmsprop(x0, alpha=0.2, beta=0.9, eps=1e-8):
    x = x0.copy()
    v = np.zeros_like(x)
    values = []

    for k in range(T):
        g = grad_f(x)
        v = beta*v + (1-beta)*(g**2)
        x = x - alpha * g / (np.sqrt(v) + eps)
        values.append(f(x))
    return values

########Heavy Ball########
def heavy_ball(x0, alpha=0.01, beta=0.9):
    x = x0.copy()
    v = np.zeros_like(x)
    values = []

    for k in range(T):
        g = grad_f(x)
        v = beta*v - alpha*g
        x = x + v
        values.append(f(x))
    return values

########Adam########
def adam(x0, alpha=0.1, beta1=0.9, beta2=0.999, eps=1e-8):
    x = x0.copy()
    m = np.zeros_like(x)
    v = np.zeros_like(x)
    values = []

    for k in range(1, T+1):
        g = grad_f(x)
        m = beta1*m + (1-beta1)*g
        v = beta2*v + (1-beta2)*(g**2)

        m_hat = m / (1 - beta1**k)
        v_hat = v / (1 - beta2**k)

        x = x - alpha*m_hat / (np.sqrt(v_hat) + eps)
        values.append(f(x))
    return values
#--------------------------

polyak_vals = polyak(x0)
rms_vals = rmsprop(x0)
hb_vals = heavy_ball(x0)
adam_vals = adam(x0)

#plot
plt.figure()
plt.plot(polyak_vals, label="Polyak")
plt.plot(rms_vals, label="RMSProp")
plt.plot(hb_vals, label="Heavy Ball")
plt.plot(adam_vals, label="Adam")
plt.yscale("log")
plt.xlabel("Iteration")
plt.ylabel("f(x,y)")
plt.legend()
plt.title("Function Value vs Iteration")
plt.show()

###II###
def heavy_ball_track(x0, alpha, beta=0.9):
    x = x0.copy()
    v = np.zeros_like(x)
    x_values = []

    for k in range(T):
        g = grad_f(x)
        v = beta*v - alpha*g
        x = x + v
        x_values.append(x[0])
    return x_values

alphas = [0.006, 0.01, 0.02]

plt.figure()
for a in alphas:
    x_vals = heavy_ball_track(x0, a)
    plt.plot(x_vals, label=f"alpha={a}")

plt.xlabel("Iteration")
plt.ylabel("x-coordinate")
plt.legend()
plt.title("Heavy Ball Stability (β=0.9)")
plt.show()


###III###
def trajectory(algo):
    x = x0.copy()
    traj = [x.copy()]

    if algo == "hb":
        v = np.zeros_like(x)
        alpha=0.01; beta=0.9
        for _ in range(T):
            g = grad_f(x)
            v = beta*v - alpha*g
            x = x + v
            traj.append(x.copy())

    elif algo == "rms":
        v = np.zeros_like(x)
        alpha=0.2; beta=0.9; eps=1e-8
        for _ in range(T):
            g = grad_f(x)
            v = beta*v + (1-beta)*(g**2)
            x = x - alpha*g/(np.sqrt(v)+eps)
            traj.append(x.copy())

    elif algo == "adam":
        m = np.zeros_like(x)
        v = np.zeros_like(x)
        alpha=0.1; b1=0.9; b2=0.999; eps=1e-8
        for k in range(1,T+1):
            g = grad_f(x)
            m = b1*m + (1-b1)*g
            v = b2*v + (1-b2)*(g**2)
            m_hat = m/(1-b1**k)
            v_hat = v/(1-b2**k)
            x = x - alpha*m_hat/(np.sqrt(v_hat)+eps)
            traj.append(x.copy())

    return np.array(traj)

#grid for plot
x_vals = np.linspace(-2.5,2.5,400)
y_vals = np.linspace(-2.5,2.5,400)
X, Y = np.meshgrid(x_vals, y_vals)
Z = X**2 + 100*Y**2

plt.figure()
plt.contour(X, Y, Z, levels=30)

hb_traj = trajectory("hb")
rms_traj = trajectory("rms")
adam_traj = trajectory("adam")

plt.plot(hb_traj[:,0], hb_traj[:,1], label="Heavy Ball")
plt.plot(rms_traj[:,0], rms_traj[:,1], label="RMSProp")
plt.plot(adam_traj[:,0], adam_traj[:,1], linestyle="--", label="Adam")

plt.legend()
plt.title("Trajectories on Contour Plot")
plt.xlabel("x")
plt.ylabel("y")
plt.show()

#'''
#-----------------Q2-----------------------
print("----------Q2----------")
###I###
#rosenbrock function
def f(x):
    return (1 - x[0])**2 + 100*(x[1] - x[0]**2)**2

def grad_f(x):
    dfdx = -2*(1 - x[0]) - 400*x[0]*(x[1] - x[0]**2)
    dfdy = 200*(x[1] - x[0]**2)
    return np.array([dfdx, dfdy])

x0 = np.array([-1.25, 0.5])
T = 3000

#--------------------------
########Polyak########
def polyak(x0, alpha_max=0.1):
    x = x0.copy()
    values = []
    f_star = 0

    for k in range(T):
        g = grad_f(x)
        alpha = (f(x) - f_star) / (np.dot(g,g) + 1e-8)
        alpha = min(alpha, alpha_max)
        x = x - alpha * g
        values.append(f(x))
    return values

########RMSProp########
def rmsprop(x0, alpha=0.01, beta=0.9, eps=1e-8):
    x = x0.copy()
    v = np.zeros_like(x)
    values = []

    for k in range(T):
        g = grad_f(x)
        v = beta*v + (1-beta)*(g**2)
        x = x - alpha*g/(np.sqrt(v)+eps)
        values.append(f(x))
    return values

########Heavy Ball########
def heavy_ball(x0, alpha=2e-4, beta=0.9):
    x = x0.copy()
    v = np.zeros_like(x)
    values = []

    for k in range(T):
        g = grad_f(x)
        v = beta*v - alpha*g
        x = x + v
        values.append(f(x))
    return values

########Adam########
def adam(x0, alpha=0.05, beta1=0.9, beta2=0.999, eps=1e-8):
    x = x0.copy()
    m = np.zeros_like(x)
    v = np.zeros_like(x)
    values = []

    for k in range(1, T+1):
        g = grad_f(x)
        m = beta1*m + (1-beta1)*g
        v = beta2*v + (1-beta2)*(g**2)

        m_hat = m/(1-beta1**k)
        v_hat = v/(1-beta2**k)

        x = x - alpha*m_hat/(np.sqrt(v_hat)+eps)
        values.append(f(x))
    return values
#--------------------------

polyak_vals = polyak(x0)
rms_vals = rmsprop(x0)
hb_vals = heavy_ball(x0)
adam_vals = adam(x0)

#plot
plt.figure()
plt.plot(polyak_vals, label="Polyak")
plt.plot(rms_vals, label="RMSProp")
plt.plot(hb_vals, label="Heavy Ball")
plt.plot(adam_vals, label="Adam")
plt.yscale("log")
plt.xlabel("Iteration")
plt.ylabel("f(x,y)")
plt.legend()
plt.title("Rosenbrock: Function Value vs Iteration")
plt.show()

###II###
def adam_track(x0, alpha):
    x = x0.copy()
    m = np.zeros_like(x)
    v = np.zeros_like(x)
    x_vals = []

    beta1 = 0.9
    beta2 = 0.999
    eps = 1e-8

    for k in range(1, T+1):
        g = grad_f(x)
        m = beta1*m + (1-beta1)*g
        v = beta2*v + (1-beta2)*(g**2)

        m_hat = m/(1-beta1**k)
        v_hat = v/(1-beta2**k)

        x = x - alpha*m_hat/(np.sqrt(v_hat)+eps)
        x_vals.append(x[0])

    return x_vals

alphas = [0.02, 0.05, 0.12]

plt.figure()
for a in alphas:
    x_vals = adam_track(x0, a)
    plt.plot(x_vals, label=f"alpha={a}")

plt.xlabel("Iteration")
plt.ylabel("x-coordinate")
plt.legend()
plt.title("Adam Stability on Rosenbrock")
plt.show()

###III###
def trajectory(algo):
    x = x0.copy()
    traj = [x.copy()]

    if algo == "hb":
        v = np.zeros_like(x)
        for _ in range(T):
            g = grad_f(x)
            v = 0.9*v - 2e-4*g
            x = x + v
            traj.append(x.copy())

    elif algo == "rms":
        v = np.zeros_like(x)
        for _ in range(T):
            g = grad_f(x)
            v = 0.9*v + 0.1*(g**2)
            x = x - 0.01*g/(np.sqrt(v)+1e-8)
            traj.append(x.copy())

    elif algo == "adam":
        m = np.zeros_like(x)
        v = np.zeros_like(x)
        for k in range(1,T+1):
            g = grad_f(x)
            m = 0.9*m + 0.1*g
            v = 0.999*v + 0.001*(g**2)
            m_hat = m/(1-0.9**k)
            v_hat = v/(1-0.999**k)
            x = x - 0.05*m_hat/(np.sqrt(v_hat)+1e-8)
            traj.append(x.copy())

    return np.array(traj)

#grid for plot
x_vals = np.linspace(-2,2,400)
y_vals = np.linspace(-1,3,400)
X, Y = np.meshgrid(x_vals, y_vals)
Z = (1-X)**2 + 100*(Y-X**2)**2

plt.figure()
plt.contour(X,Y,Z,levels=50)

hb_traj = trajectory("hb")
rms_traj = trajectory("rms")
adam_traj = trajectory("adam")

plt.plot(hb_traj[:,0], hb_traj[:,1], label="Heavy Ball")
plt.plot(rms_traj[:,0], rms_traj[:,1], label="RMSProp")
plt.plot(adam_traj[:,0], adam_traj[:,1], linestyle="--", label="Adam")

plt.legend()
plt.title("Rosenbrock Trajectories")
plt.xlabel("x")
plt.ylabel("y")
plt.show()
#'''
