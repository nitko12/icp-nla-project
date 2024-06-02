import stl
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.transform import Rotation as R
from sklearn.neighbors import KDTree


def display_meshes(ptss):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_aspect('equal', adjustable='box')

    for pts in ptss:
        ax.scatter(pts[:, 0], pts[:, 1], pts[:, 2])

    plt.show()


def random_transform(pts):
    trans = np.random.rand(3)
    pts += trans
    rot = R.random()
    pts = rot.apply(pts)

    return pts


def centroid(pts):
    return np.mean(pts, axis=0)


def icp(pts1, pts2):
    restarts = 100
    iters = 10

    min_rmse = np.inf
    best_pts2 = None

    for _ in range(restarts):
        rot = R.random()
        pts2 = rot.apply(pts2)

        for _ in range(iters):
            pts1 -= centroid(pts1)
            pts2 -= centroid(pts2)

            tree = KDTree(pts1)
            dists, idxs = tree.query(pts2)
            idxs = idxs.flatten()

            _pts1 = pts1[idxs]

            rot = optimal_rotation(_pts1, pts2)
            pts2 = np.dot(pts2, rot.T)

            rmse = np.sqrt(np.mean(dists ** 2))

            if rmse < min_rmse:
                min_rmse = rmse
                best_pts2 = pts2

    display_meshes([pts1, best_pts2])


def optimal_rotation(pts1, pts2):
    H = np.dot(pts1.T, pts2)

    U, S, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(np.dot(Vt, U.T)))
    M = np.eye(3)
    M[-1, -1] = d

    R = np.dot(U, np.dot(M, Vt))

    return R


if __name__ == '__main__':
    mesh = stl.mesh.Mesh.from_file('pikachu.stl')

    points = mesh.points
    points = points.reshape(-1, 3)

    points1 = random_transform(points)
    points2 = random_transform(points)

    icp(points1, points2)
