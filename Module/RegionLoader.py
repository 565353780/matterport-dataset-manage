#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import numpy as np
import open3d as o3d
from tqdm import tqdm
from plyfile import PlyData

from Data.Color import COLOR_MAP
from Data.Object import Object

from Method.ObjectToPointCloud import getObjectPointCloud

class RegionLoader(object):
    def __init__(self):
        self.region_folder_path = None

        self.region_file_basename_list = []
        self.region_object_list_dict = {}
        return

    def updateRegionFileBasenameList(self):
        region_filename_list = \
            os.listdir(self.region_folder_path)
        self.region_file_basename_list = []
        for region_filename in region_filename_list:
            if region_filename[-4:] != ".ply":
                continue
            self.region_file_basename_list.append(
                region_filename.split(".")[0])
        return True

    def setRegionPath(self, region_folder_path):
        if not os.path.exists(region_folder_path):
            print("[ERROR][RegionLoader::setRegionPath]")
            print("\t region_folder_path not exist!")
            return False

        self.region_folder_path = region_folder_path
        if self.region_folder_path[-1] != "/":
            self.region_folder_path += "/"

        if not self.updateRegionFileBasenameList():
            print("[ERROR][RegionLoader::setRegionPath]")
            print("\t updateRegionFileBasenameList failed!")
            return False
        return True

    def loadRegionObject(self, region_file_basename):
        self.region_object_list_dict[region_file_basename] = []
        region_file_basepath = \
            self.region_folder_path + region_file_basename

        region_ply_file_path = region_file_basepath + ".ply"
        plydata = PlyData.read(region_ply_file_path)

        vertex_list = []
        for vertex in plydata['vertex']:
            vertex_list.append([vertex['x'], vertex['y'], vertex['z']])
        vertex_array = np.array(vertex_list)

        vertex_category_array = np.zeros(vertex_array.shape)
        vertex_category_array[:] = -1
        for face in plydata['face']:
            vertex_index_array = np.array(face['vertex_indices'])
            catrgory_id = face['category_id']
            vertex_category_array[vertex_index_array] = catrgory_id

        region_vsegs_file_path = region_file_basepath + ".vsegs.json"
        vsegs_json = None
        with open(region_vsegs_file_path, "r") as f:
            vsegs_json = json.load(f)
        vertex_seg_array = np.array(vsegs_json["segIndices"])

        semseg_file_path = region_file_basepath + ".semseg.json"
        semseg_json = None
        with open(semseg_file_path, "r") as f:
            semseg_json = json.load(f)
        for seg_group in semseg_json["segGroups"]:
            object_label = seg_group["label"]

            object_seg_array = np.array(seg_group["segments"])
            object_vertex_idx_array = \
                np.where(np.isin(vertex_seg_array, object_seg_array) == True)
            object_vertex_array = vertex_array[object_vertex_idx_array]

            new_object = Object()
            new_object.label = object_label
            new_object.point_array = object_vertex_array
            self.region_object_list_dict[region_file_basename].append(new_object)
        return True

    def loadAllRegionObject(self):
        print("[INFO][RegionLoader::loadAllRegionObject]")
        print("\t start loading objects in all regions...")
        for region_file_basename in tqdm(self.region_file_basename_list):
            if not self.loadRegionObject(region_file_basename):
                print("[ERROR][RegionLoader::loadAllRegionObject]")
                print("\t loadRegionObject failed!")
                return False
        return True

    def visualRegionObject(self, region_file_basename):
        region_object_list = \
            self.region_object_list_dict[region_file_basename]

        region_pointcloud_list = []
        tmp_idx_ = 0
        for region_object in region_object_list:
            tmp_idx_ += 1
            region_pointcloud = getObjectPointCloud(region_object_list)
            colors = np.zeros(region_object.point_array.shape)
            colors[:] = COLOR_MAP[tmp_idx_%40]/255.0
            region_pointcloud.colors = o3d.utility.Vector3dVector(colors)
            region_pointcloud_list.append(region_pointcloud)

        o3d.visualization.draw_geometries(region_pointcloud_list)
        return True

    def visualAllRegionObject(self):
        unused_object_label_list = [
            "floor", "wall"
        ]

        region_pointcloud_list = []

        for region_file_basename in self.region_file_basename_list:
            region_object_list = \
                self.region_object_list_dict[region_file_basename]

            tmp_idx_ = 0
            for region_object in region_object_list:
                if region_object.label in unused_object_label_list:
                    continue
                tmp_idx_ += 1
                region_pointcloud = getObjectPointCloud(region_object)
                colors = np.zeros(region_object.point_array.shape)
                colors[:] = COLOR_MAP[tmp_idx_%40]/255.0
                region_pointcloud.colors = o3d.utility.Vector3dVector(colors)
                region_pointcloud_list.append(region_pointcloud)

        o3d.visualization.draw_geometries(region_pointcloud_list)
        return True

def demo():
    region_folder_path = \
        "/home/chli/.ros/COSCAN/MatterPort/01/ARNzJeq3xxb/region_segmentations/"

    region_loader = RegionLoader()
    region_loader.setRegionPath(region_folder_path)
    region_loader.loadAllRegionObject()
    region_loader.visualAllRegionObject()
    return True

if __name__ == "__main__":
    demo()

