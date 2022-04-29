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
        return

    def setSceneRootFolderPath(self, scene_root_folder_path):
        if not os.path.exists(scene_root_folder_path):
            print("[ERROR][SceneLoader::setSceneRootFolderPath]")
            print("\t scene_root_folder_path not exist!")
            return False

        self.scene_root_folder_path = scene_root_folder_path
        if self.scene_root_folder_path[-1] != "/":
            self.scene_root_folder_path += "/"
        return True

    def loadScene(self, scene_root_folder_path):
        if not self.setSceneRootFolderPath(scene_root_folder_path):
            print("[ERROR][SceneLoader::loadScene]")
            print("\t setSceneRootFolderPath failed!")
            return False
        return True

    def run_demo(self):

        matterport_foldername = None
        scene_pointcloud_folder_filename_list = os.listdir(scene_pointcloud_folder_path)
        for scene_pointcloud_folder_filename in scene_pointcloud_folder_filename_list:
            if os.path.isfile(scene_pointcloud_folder_filename):
                continue
            matterport_foldername = scene_pointcloud_folder_filename
            break

        scene_pointcloud_file_path = scene_pointcloud_folder_path + \
            matterport_foldername + "/house_segmentations/" + \
            matterport_foldername + ".ply"
        object_pointcloud_folder_path = scene_pointcloud_folder_path + \
            matterport_foldername + "/region_segmentations/"

        #  pointcloud = o3d.io.read_point_cloud(scene_pointcloud_file_path)

        test_file_path = object_pointcloud_folder_path + "region0.ply"
        plydata = PlyData.read(test_file_path)

        vertex_list = []
        for vertex in tqdm(plydata['vertex']):
            vertex_list.append([vertex['x'], vertex['y'], vertex['z']])
        vertex_array = np.array(vertex_list)

        vertex_category_array = np.zeros(vertex_array.shape)
        vertex_category_array[:] = -1
        for face in tqdm(plydata['face']):
            vertex_index_array = np.array(face['vertex_indices'])
            catrgory_id = face['category_id']
            vertex_category_array[vertex_index_array] = catrgory_id

        vsegs_file_path = object_pointcloud_folder_path + "region0.vsegs.json"
        vsegs_json = None
        with open(vsegs_file_path, "r") as f:
            vsegs_json = json.load(f)
        vertex_seg_array = np.array(vsegs_json["segIndices"])

        semseg_file_path = object_pointcloud_folder_path + "region0.semseg.json"
        semseg_json = None
        with open(semseg_file_path, "r") as f:
            semseg_json = json.load(f)
        object_seg_array_list = []
        for seg_group in semseg_json["segGroups"]:
            object_seg_array_list.append(np.array(seg_group["segments"]))

        object_vertex_idx_array_list = []
        for object_seg_array in object_seg_array_list:
            object_vertex_array = np.where(np.isin(vertex_seg_array, object_seg_array) == True)
            object_vertex_idx_array_list.append(object_vertex_array)

        object_vertex_array_list = []
        for object_vertex_idx_array in object_vertex_idx_array_list:
            object_vertex_array_list.append(vertex_array[object_vertex_idx_array])

        for object_vertex_array in object_vertex_array_list:
            pcd = o3d.geometry.PointCloud()
            colors = [COLOR_MAP[0] / 255.0 for _ in range(len(object_vertex_array))]
            pcd.points = o3d.utility.Vector3dVector(object_vertex_array)
            pcd.colors = o3d.utility.Vector3dVector(colors)
            o3d.visualization.draw_geometries([pcd])

        pcd = o3d.geometry.PointCloud()
        points = np.concatenate(
            [object_vertex_array for object_vertex_array in object_vertex_array_list])
        colors = np.concatenate(
            [[COLOR_MAP[i]/255.0 for _ in range(len(object_vertex_array_list[i]))] for i in range(len(object_vertex_array_list))])
        pcd.points = o3d.utility.Vector3dVector(points)
        pcd.colors = o3d.utility.Vector3dVector(colors)

        o3d.visualization.draw_geometries([pcd])
        return True

def demo():
    scene_root_folder_path = "/home/chli/.ros/COSCAN/MatterPort/01/ARNzJeq3xxb/"

    scene_loader = SceneLoader()
    scene_loader.loadScene(scene_root_folder_path)
    return True

if __name__ == "__main__":
    demo()

