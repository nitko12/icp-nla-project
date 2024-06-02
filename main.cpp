
#include <Eigen/Dense>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>

// https://github.com/crvs/KDTree/tree/master
#include "KDTree.hpp"

// https://github.com/sreiter/stl_reader/tree/master
#include "reader.h"

using namespace std;
using namespace Eigen;

vector<point_t> read_stl(string filename) {
  vector<point_t> points;

  try {
    stl_reader::StlMesh<float, unsigned int> mesh(filename);

    for (size_t itri = 0; itri < mesh.num_tris(); ++itri) {
      for (size_t icorner = 0; icorner < 3; ++icorner) {
        const float *c = mesh.tri_corner_coords(itri, icorner);
        points.push_back({c[0], c[1], c[2]});
      }
    }
  } catch (std::exception &e) {
    std::cout << e.what() << std::endl;
    exit(1);
  }

  return points;
}

int main(int argc, char *argv[]) {
  if (argc != 3) {
    std::cerr << "Usage: " << argv[0] << " <stl file 1>"
              << " <stl file 2>" << std::endl;
    return 1;
  }

  string filename1 = argv[1];
  string filename2 = argv[2];

  auto points1 = read_stl(filename1);
  auto points2 = read_stl(filename2);

  MatrixXd m1(points1.size(), 3);
  for (size_t i = 0; i < points1.size(); ++i) {
    m1.row(i) = Map<Vector3d>(points1[i].data());
  }
}