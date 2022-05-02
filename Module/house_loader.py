#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import numpy as np
import open3d as o3d

from Data.color import COLOR_MAP

from Method.house_solver import getHouseObjectList
from Method.pointcloud_solver import \
    getObjectPointCloud, getMergePointCloud

class HouseLoader(object):
    def __init__(self):
        self.house_folder_path = None

        self.house_file_basename = None
        self.house_object_list = None
        return

    def updateHouseFileBasename(self):
        house_filename_list = \
            os.listdir(self.house_folder_path)
        self.house_file_basename_list = []
        for house_filename in house_filename_list:
            if house_filename[-4:] != ".ply":
                continue
            self.house_file_basename = house_filename.split(".")[0]
            return True
        print("[ERROR][HouseLoader::updateHouseFileBasename]")
        print("\t update house file basename failed!")
        return False

    def setHousePath(self, house_folder_path):
        if not os.path.exists(house_folder_path):
            print("[ERROR][HouseLoader::setHousePath]")
            print("\t house_folder_path not exist!")
            return False

        self.house_folder_path = house_folder_path
        if self.house_folder_path[-1] != "/":
            self.house_folder_path += "/"

        if not self.updateHouseFileBasename():
            print("[ERROR][HouseLoader::setHousePath]")
            print("\t updateHouseFileBasename failed!")
            return False
        return True

    def getHouseObjectList(self):
        house_file_basepath = \
            self.house_folder_path + self.house_file_basename

        house_object_list = getHouseObjectList(house_file_basepath)
        return house_object_list

    def loadHouseObject(self):
        self.house_object_list = self.getHouseObjectList()
        return True

    def isLabelIdxValid(self, label_index):
        unused_object_label_idx_list = []
        if label_index in unused_object_label_idx_list:
            return False
        return True

    def saveHouseObjectPointCloud(self, save_folder_path):
        if save_folder_path[-1] != "/":
            save_folder_path += "/"

        if not os.path.exists(save_folder_path):
            os.makedirs(save_folder_path)

        house_pointcloud_list = []

        for house_object in self.house_object_list:
            house_pointcloud = getObjectPointCloud(house_object)
            house_pointcloud_list.append(house_pointcloud)

        for i in range(len(house_pointcloud_list)):
            house_pointcloud_label_idx = house_object_list[i].label_index
            if not self.isLabelIdxValid(house_pointcloud_label_idx):
                continue
            house_pointcloud = house_pointcloud_list[i]
            house_pointcloud_save_filename = "house_" + \
                str(i) + "_" + str(house_pointcloud_label_idx) + ".ply"
            o3d.io.write_point_cloud(
                save_folder_path + house_pointcloud_save_filename,
                house_pointcloud,
                write_ascii=True)
        return True

    def visualHouseObject(self, use_color_map=True):
        house_pointcloud_list = []

        valid_label_idx_list = []

        tmp_idx_ = 0
        for house_object in self.house_object_list:
            if not self.isLabelIdxValid(house_object.label_index):
                continue
            if house_object.label_index not in valid_label_idx_list:
                valid_label_idx_list.append(house_object.label_index)
            tmp_idx_ += 1
            house_pointcloud = getObjectPointCloud(house_object)
            if use_color_map:
                colors = np.zeros(house_object.point_array.shape)
                colors[:] = COLOR_MAP[tmp_idx_%40]/255.0
                house_pointcloud.colors = o3d.utility.Vector3dVector(colors)
            house_pointcloud_list.append(house_pointcloud)

        print(valid_label_idx_list)

        merge_pointcloud = getMergePointCloud(house_pointcloud_list)

        o3d.visualization.draw_geometries([merge_pointcloud])
        return True

def demo():
    house_folder_path = \
        "/home/chli/.ros/COSCAN/MatterPort/01/ARNzJeq3xxb/house_segmentations/"
    save_folder_path = "/home/chli/.ros/COSCAN/MatterPort/01/objects/"
    use_color_map = True

    house_loader = HouseLoader()
    house_loader.setHousePath(house_folder_path)
    house_loader.loadHouseObject()
    #  house_loader.saveHouseObjectPointCloud(save_folder_path)
    house_loader.visualHouseObject(use_color_map)
    return True

if __name__ == "__main__":
    demo()

