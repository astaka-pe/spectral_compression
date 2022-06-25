import numpy as np
import torch
import scipy as sp
import copy
import os
from util.mesh import Mesh

def main():
    mesh = Mesh("data/genus3.obj")
    mesh_dir = mesh.path.split(".")[0]
    os.makedirs(mesh_dir, exist_ok=True)
    rec_mesh = copy.deepcopy(mesh)

    E = eigen_decomposition(mesh.Lap, 500)
    X = np.matmul(E.T, mesh.vs)
    
    k_list = [3, 5, 10, 50, 100, 200, 300, 500]
    for k in k_list:
        # mesh.vs = reconstruction(E, X, k)
        rec_mesh.vs[:, 0] = recon_sub(E, mesh.vs[:, 0], k)
        rec_mesh.vs[:, 1] = recon_sub(E, mesh.vs[:, 1], k)
        rec_mesh.vs[:, 2] = recon_sub(E, mesh.vs[:, 2], k)
        rec_mesh.save("{}/rec_{}.obj".format(mesh_dir, k))

def eigen_decomposition(L, k=100):
    L = L.to_dense().numpy()
    csr = sp.sparse.csr_matrix(L)
    w, v = sp.sparse.linalg.eigs(csr, which="SR", k=k)
    index = np.argsort(np.real(w))
    E = np.real(v[:, index]).astype(np.float)
    #E /= np.linalg.norm(E, axis=0, keepdims=True)
    return E
    

def reconstruction(E, X, k=100):
    # TODO: FIX THIS!
    X_all = E.reshape(E.shape[1], -1, 1) * X.reshape(X.shape[0], 1, -1)
    X_rec = np.sum(X_all[:k], axis=0)
    return X_rec

def recon_sub(E, x, k):
    x_rec = np.zeros(len(x))
    for i in range(k):
        x_rec += np.dot(E[:, i], x) * E[:, i]
    return x_rec

if __name__ == "__main__":
    main()