#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Module.region_loader import RegionLoader
from Module.house_loader import HouseLoader

def demo_load_region():
    region_folder_path = \
        "/home/chli/.ros/COSCAN/MatterPort/01/ARNzJeq3xxb/region_segmentations/"
    processes = 12
    save_folder_path = "/home/chli/.ros/COSCAN/MatterPort/01/region_objects/"
    select_valid_label = False
    use_color_map = True

    region_loader = RegionLoader()
    region_loader.setRegionPath(region_folder_path)
    region_loader.loadAllRegionObjectWithPool(processes)
    #  region_loader.saveAllRegionObjectPointCloud(save_folder_path, select_valid_label)
    region_loader.visualAllRegionObject(use_color_map, select_valid_label)
    return True

def demo_load_house():
    house_folder_path = \
        "/home/chli/.ros/COSCAN/MatterPort/01/ARNzJeq3xxb/house_segmentations/"
    save_folder_path = "/home/chli/.ros/COSCAN/MatterPort/01/house_objects/"
    select_valid_label_index = False
    use_color_map = True

    house_loader = HouseLoader()
    house_loader.setHousePath(house_folder_path)
    house_loader.loadHouseObject()
    #  house_loader.saveHouseObjectPointCloud(save_folder_path, select_valid_label_index)
    house_loader.visualHouseObject(use_color_map, select_valid_label_index)
    return True

def demo_load_all_region():
    region_folder_path_list = [
        "/home/chli/.ros/COSCAN/MatterPort/01/ARNzJeq3xxb/region_segmentations/",
        "/home/chli/.ros/COSCAN/MatterPort/02/q9vSo1VnCiC/region_segmentations/",
        "/home/chli/.ros/COSCAN/MatterPort/03/zsNo4HB9uLZ/region_segmentations/",
        "/home/chli/.ros/COSCAN/MatterPort/04/8WUmhLawc2A/region_segmentations/",
        "/home/chli/.ros/COSCAN/MatterPort/05/JeFG25nYj2p/region_segmentations/",
        "/home/chli/.ros/COSCAN/MatterPort/06/yqstnuAEVhm/region_segmentations/"
    ]
    processes = 12
    save_folder_path_list = [
        "/home/chli/.ros/COSCAN/MatterPort/01/region_objects/",
        "/home/chli/.ros/COSCAN/MatterPort/02/region_objects/",
        "/home/chli/.ros/COSCAN/MatterPort/03/region_objects/",
        "/home/chli/.ros/COSCAN/MatterPort/04/region_objects/",
        "/home/chli/.ros/COSCAN/MatterPort/05/region_objects/",
        "/home/chli/.ros/COSCAN/MatterPort/06/region_objects/"
    ]
    valid_save_folder_path_list = [
        "/home/chli/.ros/COSCAN/MatterPort/01/valid_region_objects/",
        "/home/chli/.ros/COSCAN/MatterPort/02/valid_region_objects/",
        "/home/chli/.ros/COSCAN/MatterPort/03/valid_region_objects/",
        "/home/chli/.ros/COSCAN/MatterPort/04/valid_region_objects/",
        "/home/chli/.ros/COSCAN/MatterPort/05/valid_region_objects/",
        "/home/chli/.ros/COSCAN/MatterPort/06/valid_region_objects/"
    ]

    for i in range(len(region_folder_path_list)):
        print("[INFO][get_object::demo_load_all_region]")
        print("\t start load scene " + str(i) + " ...")
        region_folder_path = region_folder_path_list[i]
        save_folder_path = save_folder_path_list[i]
        valid_save_folder_path = valid_save_folder_path_list[i]

        region_loader = RegionLoader()
        region_loader.setRegionPath(region_folder_path)
        region_loader.loadAllRegionObjectWithPool(processes)
        region_loader.saveAllRegionObjectPointCloud(save_folder_path, False)
        region_loader.saveAllRegionObjectPointCloud(valid_save_folder_path, True)

if __name__ == "__main__":
    #  demo_load_region()
    #  demo_load_house()
    demo_load_all_region()

