#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import numpy as np
import open3d as o3d
from tqdm import tqdm
from plyfile import PlyData

from Data.Color import COLOR_MAP

class RegionLoader(object):
    def __init__(self):
        self.region_folder_path = None

        self.region_file_basename_list = []

        self.region_object_array_list_dict = {}
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
        region_file_basepath = \
            self.region_folder_path + region_file_basename

        region_ply_file_path = region_file_basepath + ".ply"
        plydata = PlyData.read(region_ply_file_path)

        print("[INFO][RegionLoader::loadRegionObject]")
        print("\t start loading vertex...")
        vertex_list = []
        for vertex in tqdm(plydata['vertex']):
            vertex_list.append([vertex['x'], vertex['y'], vertex['z']])
        vertex_array = np.array(vertex_list)

        print("[INFO][RegionLoader::loadRegionObject]")
        print("\t start loading vertex_category...")
        vertex_category_array = np.zeros(vertex_array.shape)
        vertex_category_array[:] = -1
        for face in tqdm(plydata['face']):
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
        object_seg_array_list = []
        for seg_group in semseg_json["segGroups"]:
            object_seg_array_list.append(np.array(seg_group["segments"]))

        object_vertex_idx_array_list = []
        for object_seg_array in object_seg_array_list:
            object_vertex_array = \
                np.where(np.isin(vertex_seg_array, object_seg_array) == True)
            object_vertex_idx_array_list.append(object_vertex_array)

        object_vertex_array_list = []
        for object_vertex_idx_array in object_vertex_idx_array_list:
            object_vertex_array_list.append(
                vertex_array[object_vertex_idx_array])

        self.region_object_array_list_dict[region_file_basename] = \
            object_vertex_array_list
        return True

    def loadAllRegionObject(self):
        for i in range(len(self.region_file_basename_list)):
            region_file_basename = self.region_file_basename_list[i]

            print("[INFO][RegionLoader::loadAllRegionObject]")
            print("\t start loading objects in " + \
                  region_file_basename + " : " +
                  str(i+1) + "/" + str(len(self.region_file_basename_list)) +
                  " ...")
            if not self.loadRegionObject(region_file_basename):
                print("[ERROR][RegionLoader::loadAllRegionObject]")
                print("\t loadRegionObject failed!")
                return False
        return True

    def visualRegionObject(self, region_file_basename):
        region_object_vertex_array_list = \
            self.region_object_array_list_dict[region_file_basename]

        region_pointcloud = o3d.geometry.PointCloud()
        points = np.concatenate(
            [
                object_vertex_array for
                object_vertex_array in
                region_object_vertex_array_list
            ])
        colors = np.concatenate(
            [
                [
                    COLOR_MAP[i%40]/255.0 for
                    _ in
                    range(len(region_object_vertex_array_list[i]))
                ] for
                i in
                range(len(region_object_vertex_array_list))
            ])
        region_pointcloud.points = o3d.utility.Vector3dVector(points)
        region_pointcloud.colors = o3d.utility.Vector3dVector(colors)

        o3d.visualization.draw_geometries([region_pointcloud])
        return True

    def visualAllRegionObject(self):
        region_pointcloud_list = []

        for region_file_basename in self.region_file_basename_list:
            region_object_vertex_array_list = \
                self.region_object_array_list_dict[region_file_basename]

            region_pointcloud = o3d.geometry.PointCloud()
            points = np.concatenate(
                [
                    object_vertex_array for
                    object_vertex_array in
                    region_object_vertex_array_list
                ])
            colors = np.concatenate(
                [
                    [
                        COLOR_MAP[i%40]/255.0 for
                        _ in
                        range(len(region_object_vertex_array_list[i]))
                    ] for
                    i in
                    range(len(region_object_vertex_array_list))
                ])
            region_pointcloud.points = o3d.utility.Vector3dVector(points)
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

