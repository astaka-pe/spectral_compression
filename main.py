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

    k_list = [3, 5, 10, 50, 100, 200, 300, 500]
    for k in k_list:
        rec_mesh.vs = reconstruction(E, mesh.vs, k)
        rec_mesh.save("{}/rec_{}.obj".format(mesh_dir, k))

def eigen_decomposition(L, k=100):
    L = L.to_dense().numpy()
    csr = sp.sparse.csr_matrix(L)
    w, v = sp.sparse.linalg.eigs(csr, which="SR", k=k)
    index = np.argsort(np.real(w))
    E = np.real(v[:, index]).astype(np.float)
    return E
    

def reconstruction(E, vs, k):
    alpha = np.matmul(E.T, vs)
    new_vs = np.sum(alpha[:k][np.newaxis, :, :] * E[:, :k][:, :, np.newaxis], axis=1)
    return new_vs

if __name__ == "__main__":
    main()