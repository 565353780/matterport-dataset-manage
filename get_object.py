#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Module.region_loader import RegionLoader
from Module.house_loader import HouseLoader

def demo_load_region():
    region_folder_path = \
        "/home/chli/.ros/COSCAN/MatterPort/01/ARNzJeq3xxb/region_segmentations/"
    processes = 12
    save_folder_path = "/home/chli/.ros/COSCAN/MatterPort/01/valid_region_objects/"
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

if __name__ == "__main__":
    demo_load_region()
    #  demo_load_house()

