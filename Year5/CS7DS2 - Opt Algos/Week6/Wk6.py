import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)
m = 1000

#'''
#-----------------Q1-----------------------
print("----------Q1----------")
###a###
print("----------(a)----------")
d = 2
sigma = 1

# true param
theta_star = np.array([3,4])

# data
X = np.random.randn(m,d)
epsilon = sigma*np.random.randn(m)
y = X @ theta_star + epsilon

# initial theta
theta0 = np.array([1.,1.])

def loss(theta):
    return (1/(2*m))*np.linalg.norm(X@theta - y)**2

def grad(theta):
    return (1/m)*X.T@(X@theta - y)

#---(i)---

alpha = 0.5
T = 80

theta = theta0.copy()

losses_gd = []
traj_gd = [theta.copy()]

for t in range(T):
    
    losses_gd.append(loss(theta))
    
    theta = theta - alpha*grad(theta)
    
    traj_gd.append(theta.copy())

traj_gd = np.array(traj_gd)

#'''
print("\nGD vals:")
print("initial loss:", losses_gd[0])
print("final loss:", losses_gd[-1])
print("true theta:", theta_star)
print("est theta:", traj_gd[-1])
print("param error:", np.linalg.norm(traj_gd[-1]-theta_star))
print("\nfirst 5 losses:", losses_gd[:5])
print("last 5 losses:", losses_gd[-5:])
#'''

plt.figure()
plt.plot(losses_gd)
plt.yscale("log")
plt.xlabel("Iteration")
plt.ylabel("Loss $L(theta_t)$")
plt.title("Full Batch GD Loss")
plt.show()

#---(ii)---

theta1 = np.linspace(-1,6,100)
theta2 = np.linspace(-1,7,100)

T1,T2 = np.meshgrid(theta1,theta2)

Z = np.zeros_like(T1)

for i in range(T1.shape[0]):
    for j in range(T1.shape[1]):
        th = np.array([T1[i,j],T2[i,j]])
        Z[i,j] = loss(th)

plt.figure()

plt.contour(T1,T2,Z,levels=30)

plt.plot(traj_gd[:,0],traj_gd[:,1],'ro-')

plt.xlabel("$theta_1$")
plt.ylabel("$theta_2$")

plt.title("GD Trajectory")

plt.show()

###b###
print("----------(b)----------")

def SGD(batch_size, updates, alpha):
    
    theta = theta0.copy()
    
    traj = [theta.copy()]
    losses = []
    
    idx = np.arange(m)
    
    for t in range(updates):
        
        if t % (m//batch_size) == 0:
            np.random.shuffle(idx)
        
        batch = idx[(t*batch_size)%m : (t*batch_size)%m + batch_size]
        
        Xb = X[batch]
        yb = y[batch]
        
        g = (1/batch_size)*Xb.T@(Xb@theta - yb)
        
        theta = theta - alpha*g
        
        losses.append(loss(theta))
        traj.append(theta.copy())
    
    return np.array(losses), np.array(traj)

#---(i)---

loss_sgd5, traj_sgd5 = SGD(5,400,0.5)
loss_sgd20, traj_sgd20 = SGD(20,400,0.5)

#'''
print("\nSGD vals:")
print("\nSGD b=5 final theta:", traj_sgd5[-1])
print("SGD b=5 final loss:", loss_sgd5[-1])
print("\nSGD b=20 final theta:", traj_sgd20[-1])
print("SGD b=20 final loss:", loss_sgd20[-1])
print("\nGD final theta:", traj_gd[-1])
print("GD final loss:", losses_gd[-1])
#'''

plt.figure()

plt.plot(losses_gd,label="GD", color="r")
plt.plot(loss_sgd5,label="SGD b=5")
plt.plot(loss_sgd20,label="SGD b=20", color="y")

plt.yscale("log")

plt.xlabel("Iteration")
plt.ylabel("Loss")


plt.legend()
plt.title("GD vs SGD")

plt.show()

#---(ii)---

plt.figure()

plt.contour(T1,T2,Z,levels=30)

plt.plot(traj_gd[:,0],traj_gd[:,1],label="GD", color="r")
plt.plot(traj_sgd5[:,0],traj_sgd5[:,1],label="SGD b=5")
plt.plot(traj_sgd20[:,0],traj_sgd20[:,1],label="SGD b=20", color="y")

plt.legend()

plt.xlabel("$theta_1$")
plt.ylabel("$theta_2$")

plt.title("Optimisation Trajectories")

plt.show()

###c###
print("----------(c)----------")

def NAG(batch_size,updates,alpha,beta=0.9):
    
    theta = theta0.copy()
    v = np.zeros_like(theta)
    
    traj=[theta.copy()]
    losses=[]
    
    idx=np.arange(m)
    
    for t in range(updates):
        
        if t%(m//batch_size)==0:
            np.random.shuffle(idx)
            
        batch=idx[(t*batch_size)%m:(t*batch_size)%m+batch_size]
        
        Xb=X[batch]
        yb=y[batch]
        
        lookahead = theta - beta*v
        
        g=(1/batch_size)*Xb.T@(Xb@lookahead - yb)
        
        v = beta*v + alpha*g
        
        theta = theta - v
        
        losses.append(loss(theta))
        traj.append(theta.copy())
        
    return np.array(losses), np.array(traj)

def Adagrad(batch_size,updates,alpha,eps=1e-8):
    
    theta = theta0.copy()
    
    G = np.zeros_like(theta)
    
    traj=[theta.copy()]
    losses=[]
    
    idx=np.arange(m)
    
    for t in range(updates):
        
        if t%(m//batch_size)==0:
            np.random.shuffle(idx)
            
        batch=idx[(t*batch_size)%m:(t*batch_size)%m+batch_size]
        
        Xb=X[batch]
        yb=y[batch]
        
        g=(1/batch_size)*Xb.T@(Xb@theta - yb)
        
        G += g**2
        
        theta = theta - alpha/(np.sqrt(G)+eps)*g
        
        losses.append(loss(theta))
        traj.append(theta.copy())
        
    return np.array(losses), np.array(traj)

#---(i)---

loss_nag,traj_nag = NAG(10,400,0.5)
loss_ada,traj_ada = Adagrad(10,400,0.5)
loss_sgd10,traj_sgd10 = SGD(10,400,0.5)

#'''
print("\noptimiser comparison:")
print("\nSGD final loss:", loss_sgd10[-1])
print("SGD final theta:", traj_sgd10[-1])
print("\nNAG final loss:", loss_nag[-1])
print("NAG final theta:", traj_nag[-1])
print("\nAdag final loss:", loss_ada[-1])
print("Adag final theta:", traj_ada[-1])
#'''

plt.figure()

plt.plot(loss_sgd10,label="SGD", color="r")
plt.plot(loss_nag,label="NAG")
plt.plot(loss_ada,label="Adagrad", color="y")

plt.yscale("log")

plt.legend()

plt.title("Optimiser Comparison")

plt.xlabel("Iteration")
plt.ylabel("Loss")

plt.show()

#---(ii)---

plt.figure()

plt.contour(T1,T2,Z,levels=30)

plt.plot(traj_sgd10[:,0],traj_sgd10[:,1],label="SGD", color="r")
plt.plot(traj_nag[:,0],traj_nag[:,1],label="NAG")
plt.plot(traj_ada[:,0],traj_ada[:,1],label="Adagrad", color="y")

plt.legend()

plt.xlabel("$theta_1$")
plt.ylabel("$theta_2$")

plt.title("Optimiser Trajectories")

plt.show()

##Q1##'''


#'''
#-----------------Q2-----------------------
print("----------Q2----------")
###a###
print("----------(a)----------")

# true params
x_star = np.array([1,3])

# input
u = np.random.uniform(-2,2,m)

# noise
epsilon = 0.05*np.random.randn(m)

def model(u,x):
    return x[1]*np.tanh(x[0]*u)

# labels
y = model(u,x_star) + epsilon

# initial parameters
x0 = np.array([1.,1.])

def loss(x):
    yhat = model(u,x)
    return (1/(2*m))*np.sum((yhat-y)**2)

def grad(x):

    yhat = model(u,x)
    e = yhat - y
    
    tanh_term = np.tanh(x[0]*u)
    
    g2 = (1/m)*np.sum(e * tanh_term)
    
    g1 = (1/m)*np.sum(e * x[1] * (1 - tanh_term**2) * u)
    
    return np.array([g1,g2])

#---(i)---
alpha = 0.75
T = 500

x = x0.copy()

losses_gd = []
traj_gd = [x.copy()]

for t in range(T):

    losses_gd.append(loss(x))

    x = x - alpha*grad(x)

    traj_gd.append(x.copy())

traj_gd = np.array(traj_gd)

#'''
print("\nQ2GD vals:")
print("initial loss:", losses_gd[0])
print("final loss:", losses_gd[-1])
print("true param:", x_star)
print("est params:", traj_gd[-1])
print("param error:", np.linalg.norm(traj_gd[-1]-x_star))
#'''

plt.figure()

plt.plot(losses_gd)
plt.yscale("log")

plt.xlabel("Iteration")
plt.ylabel("$J(x_t)$")

plt.title("GD Loss")

plt.show()

#---(ii)---

x1 = np.linspace(-1,3,100)
x2 = np.linspace(0,5,100)

X1,X2 = np.meshgrid(x1,x2)

Z = np.zeros_like(X1)

for i in range(X1.shape[0]):
    for j in range(X1.shape[1]):
        x_temp = np.array([X1[i,j],X2[i,j]])
        Z[i,j] = loss(x_temp)

plt.figure()

plt.contour(X1,X2,Z,levels=30)

plt.plot(traj_gd[:,0],traj_gd[:,1],'ro-')

plt.xlabel("$x_1$")
plt.ylabel("$x_2$")

plt.title("GD Trajectory")

plt.show()

###b###
print("----------(b)----------")

def SGD(batch_size,updates,alpha):

    x = x0.copy()
    
    traj=[x.copy()]
    losses=[]
    
    idx=np.arange(m)
    
    for t in range(updates):
        
        if t%(m//batch_size)==0:
            np.random.shuffle(idx)
            
        batch=idx[(t*batch_size)%m:(t*batch_size)%m+batch_size]
        
        ub=u[batch]
        yb=y[batch]
        
        yhat = x[1]*np.tanh(x[0]*ub)
        e = yhat - yb
        
        tanh_term = np.tanh(x[0]*ub)
        
        g2 = (1/batch_size)*np.sum(e*tanh_term)
        g1 = (1/batch_size)*np.sum(e*x[1]*(1-tanh_term**2)*ub)
        
        g = np.array([g1,g2])
        
        x = x - alpha*g
        
        losses.append(loss(x))
        traj.append(x.copy())
        
    return np.array(losses),np.array(traj)

#---(i)---

loss_sgd5,traj_sgd5 = SGD(5,500,0.75)
loss_sgd20,traj_sgd20 = SGD(20,500,0.75)

#'''
print("\nQ2 SGD vals:")
print("SGD b=5 final loss:", loss_sgd5[-1])
print("SGD b=5 final x:", traj_sgd5[-1])
print("SGD b=20 final loss:", loss_sgd20[-1])
print("SGD b=20 final x:", traj_sgd20[-1])
print("GD final x:", traj_gd[-1])
#'''

plt.figure()

plt.plot(losses_gd,label="GD", color="r")
plt.plot(loss_sgd5,label="SGD b=5")
plt.plot(loss_sgd20,label="SGD b=20", color="y")

plt.yscale("log")

plt.xlabel("Iteration")
plt.ylabel("Loss")

plt.legend()
plt.title("GD vs SGD")

plt.show()

#---(ii)---

plt.figure()

plt.contour(X1,X2,Z,levels=30)

plt.plot(traj_gd[:,0],traj_gd[:,1],label="GD", color="r")
plt.plot(traj_sgd5[:,0],traj_sgd5[:,1],label="SGD b=5")
plt.plot(traj_sgd20[:,0],traj_sgd20[:,1],label="SGD b=20", linestyle="--", color="y")

plt.legend()

plt.xlabel("$x_1$")
plt.ylabel("$x_2$")

plt.title("Optimisation Trajectories")

plt.show()

###c###
print("----------(c)----------")
def NAG(batch_size,updates,alpha,beta=0.9):

    x = x0.copy()
    v = np.zeros_like(x)
    
    traj=[x.copy()]
    losses=[]
    
    idx=np.arange(m)
    
    for t in range(updates):
        
        if t%(m//batch_size)==0:
            np.random.shuffle(idx)
            
        batch=idx[(t*batch_size)%m:(t*batch_size)%m+batch_size]
        
        ub=u[batch]
        yb=y[batch]
        
        lookahead = x - beta*v
        
        yhat = lookahead[1]*np.tanh(lookahead[0]*ub)
        e = yhat - yb
        
        tanh_term = np.tanh(lookahead[0]*ub)
        
        g2 = (1/batch_size)*np.sum(e*tanh_term)
        g1 = (1/batch_size)*np.sum(e*lookahead[1]*(1-tanh_term**2)*ub)
        
        g=np.array([g1,g2])
        
        v = beta*v + alpha*g
        
        x = x - v
        
        losses.append(loss(x))
        traj.append(x.copy())
        
    return np.array(losses),np.array(traj)

def Adagrad(batch_size,updates,alpha,eps=1e-8):

    x = x0.copy()
    G = np.zeros_like(x)
    
    traj=[x.copy()]
    losses=[]
    
    idx=np.arange(m)
    
    for t in range(updates):
        
        if t%(m//batch_size)==0:
            np.random.shuffle(idx)
            
        batch=idx[(t*batch_size)%m:(t*batch_size)%m+batch_size]
        
        ub=u[batch]
        yb=y[batch]
        
        yhat = x[1]*np.tanh(x[0]*ub)
        e = yhat - yb
        
        tanh_term = np.tanh(x[0]*ub)
        
        g2 = (1/batch_size)*np.sum(e*tanh_term)
        g1 = (1/batch_size)*np.sum(e*x[1]*(1-tanh_term**2)*ub)
        
        g=np.array([g1,g2])
        
        G += g**2
        
        x = x - alpha/(np.sqrt(G)+eps)*g
        
        losses.append(loss(x))
        traj.append(x.copy())
        
    return np.array(losses),np.array(traj)

#---(i)---

loss_nag,traj_nag = NAG(10,400,0.5)
loss_ada,traj_ada = Adagrad(10,400,0.5)
loss_sgd10,traj_sgd10 = SGD(10,400,0.5)

#'''
print("\nQ2 optimiser comparison:")
print("SGD final loss:", loss_sgd10[-1])
print("NAG final loss:", loss_nag[-1])
print("Adag final loss:", loss_ada[-1])
print("\nfinal params:")
print("SGD:", traj_sgd10[-1])
print("NAG:", traj_nag[-1])
print("Adag:", traj_ada[-1])
#'''

plt.figure()

plt.plot(loss_sgd10,label="SGD", color="r")
plt.plot(loss_nag,label="NAG")
plt.plot(loss_ada,label="Adagrad", color="y")

plt.yscale("log")

plt.legend()

plt.title("Optimiser Comparison")

plt.xlabel("Iteration")
plt.ylabel("Loss")

plt.show()

#---(ii)---

plt.figure()

plt.contour(X1,X2,Z,levels=30)

plt.plot(traj_sgd10[:,0],traj_sgd10[:,1],label="SGD", color="r")
plt.plot(traj_nag[:,0],traj_nag[:,1],label="NAG")
plt.plot(traj_ada[:,0],traj_ada[:,1],label="Adagrad", color="y")

plt.legend()

plt.xlabel("$X_1$")
plt.ylabel("$X_2$")

plt.title("Optimiser Trajectories")

plt.show()

##Q2##'''


#'''
#-----------------Q3-----------------------
print("----------Q3----------")

def f(x):
    x1, x2 = x
    return (1-x1)**2 + 100*(x2 - x1**2)**2

x0 = np.array([-1.,1.])

def grad_fd(x,h=1e-5):

    g = np.zeros(2)

    for i in range(2):
        xp = x.copy()
        xm = x.copy()

        xp[i] += h
        xm[i] -= h

        g[i] = (f(xp)-f(xm))/(2*h)

    return g

def hessian_fd(x,h=1e-4):

    H = np.zeros((2,2))

    for i in range(2):
        for j in range(2):

            xp = x.copy()
            xm = x.copy()
            xpp = x.copy()
            xmm = x.copy()

            xp[i]+=h; xp[j]+=h
            xm[i]+=h; xm[j]-=h
            xpp[i]-=h; xpp[j]+=h
            xmm[i]-=h; xmm[j]-=h

            H[i,j]=(f(xp)-f(xm)-f(xpp)+f(xmm))/(4*h*h)

    return H

###a###
print("----------(a)----------")

alpha = 1e-3
T = 200

x = x0.copy()

loss_gd = []
traj_gd = [x.copy()]

for t in range(T):

    loss_gd.append(f(x))

    g = grad_fd(x)

    x = x - alpha*g

    traj_gd.append(x.copy())

traj_gd = np.array(traj_gd)

#'''
print("\nQ3 GD vals:")
print("initial f(x):", loss_gd[0])
print("final f(x):", loss_gd[-1])
print("final point:", traj_gd[-1])
print("dist to optimum (1,1):", np.linalg.norm(traj_gd[-1]-np.array([1,1])))
#'''

plt.figure()

plt.plot(loss_gd)
plt.yscale("log")

plt.xlabel("Iteration")
plt.ylabel("$f(x)$")

plt.title("Gradient Descent")

plt.show()

###b###
print("----------(b)----------")

alpha = 0.7
T = 200

x = x0.copy()

loss_newton=[]
traj_newton=[x.copy()]

for t in range(T):

    loss_newton.append(f(x))

    g = grad_fd(x)
    H = hessian_fd(x)

    p = np.linalg.solve(H,g)

    x = x - alpha*p

    traj_newton.append(x.copy())

traj_newton=np.array(traj_newton)

#'''
print("\nQ3 newton vals:")
print("initial f(x):", loss_newton[0])
print("final f(x):", loss_newton[-1])
print("final point:", traj_newton[-1])
print("dist to optimum:", np.linalg.norm(traj_newton[-1]-np.array([1,1])))
#'''

plt.figure()

plt.plot(loss_newton)
plt.yscale("log")

plt.xlabel("Iteration")
plt.ylabel("$f(x)$")

plt.title("GD - Newton Method & Hessian")

plt.show()



###c###
print("----------(c)----------")
#---(i)---

T=200
alpha0=1
rho=0.5
K=20

x=x0.copy()

loss_dn=[]
traj_dn=[x.copy()]

for t in range(T):

    ft=f(x)
    loss_dn.append(ft)

    g=grad_fd(x)
    H=hessian_fd(x)

    p=np.linalg.solve(H,g)

    alpha=alpha0
    accepted=False

    for k in range(K):

        x_new=x-alpha*p

        if f(x_new)<ft:
            accepted=True
            break

        alpha*=rho

    if not accepted:
        x_new=x-1e-4*g

    x=x_new

    traj_dn.append(x.copy())

traj_dn=np.array(traj_dn)

#'''
print("\nQ3 damped newton vals:")
print("Final f(x):", loss_dn[-1])
print("Final point:", traj_dn[-1])
print("dist to optimum:", np.linalg.norm(traj_dn[-1]-np.array([1,1])))
#'''

plt.figure()

plt.plot(loss_gd,label="GD", color="r")
plt.plot(loss_newton,label="Newton")
plt.plot(loss_dn,label="Damped Newton", linestyle="--", color="y")

plt.yscale("log")

plt.xlabel("Iteration")
plt.ylabel("$f(x)$")

plt.legend()

plt.title("Optimiser Comparison")

plt.show()

#---(ii)---

x1 = np.linspace(-2,2,200)
x2 = np.linspace(-1,3,200)

X1,X2 = np.meshgrid(x1,x2)

Z = (1-X1)**2 + 100*(X2-X1**2)**2

plt.figure()

plt.contour(X1,X2,Z,levels=50)

plt.plot(traj_dn[:,0],traj_dn[:,1],label="Damped Newton", color="y")
plt.plot(traj_newton[:,0],traj_newton[:,1],label="Newton")
plt.plot(traj_gd[::5,0],traj_gd[::5,1],label="GD", color="r")

plt.legend()

plt.xlabel("$x_1$")
plt.ylabel("$x_2$")

plt.title("Optimisation Trajectories")

plt.show()

##Q3##'''

