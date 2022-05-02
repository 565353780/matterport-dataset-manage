#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import open3d as o3d

def getObjectPointCloud(obj):
    pointcloud = o3d.geometry.PointCloud()
    pointcloud.points = o3d.utility.Vector3dVector(obj.point_array)
    pointcloud.colors = o3d.utility.Vector3dVector(obj.color_array)
    return pointcloud

def getMergePointCloud(pointcloud_list):
    points_list = []
    colors_list = []
    for pointcloud in pointcloud_list:
        points_list.append(np.array(pointcloud.points))
        colors_list.append(np.array(pointcloud.colors))

    merge_points = np.concatenate(points_list, axis=0)
    merge_colors = np.concatenate(colors_list, axis=0)
    merge_pointcloud = o3d.geometry.PointCloud()
    merge_pointcloud.points = o3d.utility.Vector3dVector(merge_points)
    merge_pointcloud.colors = o3d.utility.Vector3dVector(merge_colors)
    return merge_pointcloud

