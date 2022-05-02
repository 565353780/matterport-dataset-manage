#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import numpy as np
from plyfile import PlyData

from Data.object import HouseObject

def getHouseObjectList(house_file_basepath):
    house_object_list = []

    house_ply_file_path = house_file_basepath + ".ply"
    plydata = PlyData.read(house_ply_file_path)

    point_list = []
    color_list = []
    for vertex in plydata['vertex']:
        point_list.append([vertex['x'], vertex['y'], vertex['z']])
        color_list.append([vertex['red'], vertex['green'], vertex['blue']])
    point_array = np.array(point_list)
    color_array = np.array(color_list) / 255.0

    face_list = []
    for face in plydata['face']:
        face_list.append(face['vertex_indices'])
    face_point_idx_array = np.array(face_list)

    house_fsegs_file_path = house_file_basepath + ".fsegs.json"
    fsegs_json = None
    with open(house_fsegs_file_path, "r") as f:
        fsegs_json = json.load(f)
    face_seg_array = np.array(fsegs_json["segIndices"])

    semseg_file_path = house_file_basepath + ".semseg.json"
    semseg_json = None
    with open(semseg_file_path, "r") as f:
        semseg_json = json.load(f)
    for seg_group in semseg_json["segGroups"]:
        object_id = seg_group["id"]
        object_label_index = int(seg_group["label_index"])

        object_seg_array = np.array(seg_group["segments"])
        object_face_idx_array = \
            np.where(np.isin(face_seg_array, object_seg_array) == True)
        object_point_idx_array = \
            np.unique(face_point_idx_array[object_face_idx_array].flatten())
        object_point_array = point_array[object_point_idx_array]
        object_color_array = color_array[object_point_idx_array]

        new_house_object = HouseObject()
        new_house_object.id = object_id
        new_house_object.label_index = object_label_index
        new_house_object.point_array = object_point_array
        new_house_object.color_array = object_color_array
        house_object_list.append(new_house_object)
    return house_object_list

