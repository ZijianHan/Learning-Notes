---
title: SLAM with Deep Learning - Summary
date: 2020-03-06 22:52:40
categories:
- SLAM
- Vision SLAM
tags:
- machine learning
- SLAM
- VSLAM
toc: true
---
A brief study list of some deep-learning-based vision SLAM methods.

<!--more-->

# Ideas of using deep neural network in SLAM
- Use CNN for image depth estimation
- DNN to replace some traditional optimization problem, end to end solution, trained to perform better without loop closure, or reduce the load on loop closure part
- Online learning and adaptation: how to generalize network power to unseen view
- Self-tuning SLAM

# Semantic stereo visual odometry (Weiming’s thesis)
Use CNN classification to recognize feature points as objects, and build a geometric map with semantic meanings for certain landmarks / objects.

Inspiration: semantic 3D reconstruction for map building, use classified objects as feature points

# DeepVO
## 1. Introduction
  End-to-end learning with deep Recurrent Convolutional Neural Networks
  Raw RGB image -> pose
  CNN for image feature representation, RNN for pose learning

  Limits for traditional methods: need lots of engineering efforts to tune, scaling problem requires extra or prior knowledge

  Why need sequential data learning: VO is heavily rely on geometric features, dynamic motions among changes of images, rather than a single frame, so CNN is not enough

  How to generalise to new environment: using geometric feature representation learnt by CNN

## 2. Related work
Two main types: geometry based and learning based
- Geometry based:
  - Sparse feature based: outliers, noises cause drifts over time. Computational expensive. Keyframe based: PTAM, ORBSLAM.
  - Direct methods: photometric consistency, DTAM, SVO,
- Learning based: Using optical flow to train KNN (K nearest neighbour), GP (gaussian process) and SVM (support vector machines) for monocular VO [15,16,17].
  - DL based methods: handle large scale, big data, non-linear high dimensional data

## 3. RCNN method
