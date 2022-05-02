#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import numpy as np
from plyfile import PlyData

from Data.object import Object

def getRegionObjectList(region_file_basepath):
    region_object_list = []

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

