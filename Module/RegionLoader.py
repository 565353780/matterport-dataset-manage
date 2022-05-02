#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import numpy as np
import open3d as o3d
from tqdm import tqdm
from plyfile import PlyData
from multiprocessing import Pool

from Data.Color import COLOR_MAP
from Data.Object import Object

from Method.ObjectToPointCloud import \
    getObjectPointCloud, getMergePointCloud

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

    def getRegionObjectList(self, region_file_basename):
        region_object_list = []

        region_file_basepath = \
            self.region_folder_path + region_file_basename

        region_ply_file_path = region_file_basepath + ".ply"
        plydata = PlyData.read(region_ply_file_path)

        point_list = []
        color_list = []
        for vertex in plydata['vertex']:
            point_list.append([vertex['x'], vertex['y'], vertex['z']])
            color_list.append([vertex['red'], vertex['green'], vertex['blue']])
        point_array = np.array(point_list)
        color_array = np.array(color_list) / 255.0

        point_category_array = np.zeros(point_array.shape)
        point_category_array[:] = -1
        for face in plydata['face']:
            point_idx_array = np.array(face['vertex_indices'])
            catrgory_id = face['category_id']
            point_category_array[point_idx_array] = catrgory_id

        region_vsegs_file_path = region_file_basepath + ".vsegs.json"
        vsegs_json = None
        with open(region_vsegs_file_path, "r") as f:
            vsegs_json = json.load(f)
        point_seg_array = np.array(vsegs_json["segIndices"])

        semseg_file_path = region_file_basepath + ".semseg.json"
        semseg_json = None
        with open(semseg_file_path, "r") as f:
            semseg_json = json.load(f)
        for seg_group in semseg_json["segGroups"]:
            object_label = seg_group["label"]

            object_seg_array = np.array(seg_group["segments"])
            object_point_idx_array = \
                np.where(np.isin(point_seg_array, object_seg_array) == True)
            object_point_array = point_array[object_point_idx_array]
            object_color_array = color_array[object_point_idx_array]

            new_object = Object()
            new_object.label = object_label
            new_object.point_array = object_point_array
            new_object.color_array = object_color_array
            region_object_list.append(new_object)
        return region_object_list

    def loadRegionObject(self, region_file_basename):
        region_object_list = self.getRegionObjectList(region_file_basename)
        self.region_object_list_dict[region_file_basename] = region_object_list
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

    def loadAllRegionObjectWithPool(self, processes):
        print("[INFO][RegionLoader::loadAllRegionObjectWithPool]")
        print("\t start loading objects in all regions...")
        pool = Pool(processes=processes)
        region_object_list = pool.map(
            self.getRegionObjectList, self.region_file_basename_list)

        for i in range(len(region_object_list)):
            self.region_object_list_dict[self.region_file_basename_list[i]] = \
                region_object_list[i]
        return True

    def isLabelValid(self, label):
        unused_object_label_list = [
            "floor", "wall", "remove", "window"
        ]
        for unused_object_label in unused_object_label_list:
            if unused_object_label in label:
                return False
        return True

    def visualRegionObject(self, region_file_basename, use_color_map=True):
        region_object_list = \
            self.region_object_list_dict[region_file_basename]

        region_pointcloud_list = []
        tmp_idx_ = 0
        for region_object in region_object_list:
            tmp_idx_ += 1
            region_pointcloud = getObjectPointCloud(region_object)
            if use_color_map:
                colors = np.zeros(region_object.point_array.shape)
                colors[:] = COLOR_MAP[tmp_idx_%40]/255.0
                region_pointcloud.colors = o3d.utility.Vector3dVector(colors)
            region_pointcloud_list.append(region_pointcloud)

        merge_pointcloud = getMergePointCloud(region_pointcloud_list)

        o3d.visualization.draw_geometries([merge_pointcloud])
        return True

    def visualAllRegionObject(self, use_color_map=True):

        region_pointcloud_list = []

        for region_file_basename in self.region_file_basename_list:
            region_object_list = \
                self.region_object_list_dict[region_file_basename]

            tmp_idx_ = 0
            for region_object in region_object_list:
                if not self.isLabelValid(region_object.label):
                    continue
                print(region_object.label, end=", ")
                tmp_idx_ += 1
                if tmp_idx_ % 10 == 0:
                    print()
                region_pointcloud = getObjectPointCloud(region_object)
                if use_color_map:
                    colors = np.zeros(region_object.point_array.shape)
                    colors[:] = COLOR_MAP[tmp_idx_%40]/255.0
                    region_pointcloud.colors = o3d.utility.Vector3dVector(colors)
                region_pointcloud_list.append(region_pointcloud)

        merge_pointcloud = getMergePointCloud(region_pointcloud_list)

        o3d.visualization.draw_geometries([merge_pointcloud])
        return True

def demo():
    region_folder_path = \
        "/home/chli/.ros/COSCAN/MatterPort/01/ARNzJeq3xxb/region_segmentations/"

    region_loader = RegionLoader()
    region_loader.setRegionPath(region_folder_path)
    region_loader.loadAllRegionObjectWithPool(12)
    region_loader.visualAllRegionObject(False)
    return True

if __name__ == "__main__":
    demo()

