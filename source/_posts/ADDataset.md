---
title: Autonomous Driving Dataset Summary
date: 2020-03-05 20:33:18
categories:
- Dataset
- AD Dataset
tags:
- Dataset
toc: true
---
Useful dataset collected for autonomous vehicle algorithm (perception, path planning and control). Mainly sensor raw dataset, some with labels.
Used for research, benchmarking, tranining, etc.
<!--more-->
# Overview
- KITTI Dataset
- Argoai Dataset
- Waymo Open Dataset
## Dataset Attributes Comparison
| Dataset        | Scene for object tracking | Map data          |
| -------------- |:-------------------------:| -----------------:|
| KITTI          | 22                        | Nan               |
| Argoai         | 113 (3D annotated)        | **HD map (2 cities)** |
| Waymo          | are neat                  | Nan               |

``` bash
$ git clone ...
```
```python
def fun():
  return ok
```

# Argoai Dataset
Official website: <https://www.argoverse.org/data.html>
Github: <https://github.com/argoai/argoverse-api>

Obviously the most unique part for Argoai dataset is the HD map data. It not only provides large amount of 3D annotated, well synced camera and lidar data, but also emphasis the importance of using HD map data in AD algorithm, and provides APIs to connect sensor perception data with the map data.

Argoai also provides two baseline for [3D object tracking](https://github.com/alliecc/argoverse_baselinetracker) and [trajectory forecasting](https://github.com/jagjeet-singh/argoverse-forecasting).
![](argoaisensorset.png)
