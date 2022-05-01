#!/usr/bin/env python
# -*- coding: utf-8 -*-

import open3d as o3d

def getObjectPointCloud(obj):
    pointcloud = o3d.geometry.PointCloud()
    pointcloud.points = o3d.utility.Vector3dVector(obj.point_array)
    return pointcloud

