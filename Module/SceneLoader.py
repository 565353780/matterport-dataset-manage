#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import numpy as np
import open3d as o3d
from tqdm import tqdm
from plyfile import PlyData

from Data.Color import COLOR_MAP

class SceneLoader(object):
    def __init__(self):
        self.scene_root_folder_path = None

        self.scene_id = None

        self.house_segmentations_folder_path = None

        self.region_segmentations_folder_path = None
        self.region_file_basename_list = []

        self.region_object_dict = {}
        return

    def updateSceneID(self):
        if self.scene_root_folder_path is None:
            print("[ERROR][SceneLoader::updateSceneID]")
            print("\t scene_root_folder_path is None!")
            return False

        scene_root_folder_path_split_list = self.scene_root_folder_path.split("/")
        self.scene_id = scene_root_folder_path_split_list[-2]
        return True

    def setScenePath(self, scene_root_folder_path):
        if not os.path.exists(scene_root_folder_path):
            print("[ERROR][SceneLoader::setScenePath]")
            print("\t scene_root_folder_path not exist!")
            return False

        self.scene_root_folder_path = scene_root_folder_path
        if self.scene_root_folder_path[-1] != "/":
            self.scene_root_folder_path += "/"

        self.house_segmentations_folder_path = \
            self.scene_root_folder_path + "house_segmentations/"
        if not os.path.exists(self.house_segmentations_folder_path):
            print("[ERROR][SceneLoader::setScenePath]")
            print("\t house_segmentations folder not exist!")
            return False

        if not self.updateSceneID():
            print("[ERROR][SceneLoader::setScenePath]")
            print("\t updateSceneID failed!")
            return False
        return True

    def loadScene(self, scene_root_folder_path):
        if not self.setScenePath(scene_root_folder_path):
            print("[ERROR][SceneLoader::loadScene]")
            print("\t setScenePath failed!")
            return False
        return True

    def visualRegionObject(self, region_file_basename):
        pcd = o3d.geometry.PointCloud()
        points = np.concatenate(
            [object_vertex_array for object_vertex_array in object_vertex_array_list])
        colors = np.concatenate(
            [[COLOR_MAP[i]/255.0 for _ in range(len(object_vertex_array_list[i]))] for i in range(len(object_vertex_array_list))])
        pcd.points = o3d.utility.Vector3dVector(points)
        pcd.colors = o3d.utility.Vector3dVector(colors)

        o3d.visualization.draw_geometries([pcd])
        return True

    def visualSceneObject(self):
        return True

def demo():
    scene_root_folder_path = "/home/chli/.ros/COSCAN/MatterPort/01/ARNzJeq3xxb/"

    scene_loader = SceneLoader()
    scene_loader.loadScene(scene_root_folder_path)
    return True

if __name__ == "__main__":
    demo()

