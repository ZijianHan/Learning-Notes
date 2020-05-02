# AI Platform

The development of AI technology is growing at an amazing pace, while to implement them from research into production (as most of the companies are doing nowadays), the barrier or bottleneck lays in between has become more clear: lacking of software infrastructure to continuously integrate, deploy, and improve the AI software.  

Why we need AI infrastructure:
As more machine learning platform released, the design and implementation of machine learning models becomes like just calling a function or using APIs. However the complete framework of an AI product should also need the AI infrastructure as the core part to scale up, which mainly focus on the DevOps that lots of AI researchers do not pay much attention to.
There are several headache issues we usually when building practical AI applications:
- computational resources are expensive
- integration is hard and un-efficient as different toolchains have different interface
- model training and turning (hyperparameter search) is difficult and time-consuming

So I will try to read upon different kind of AI platform and framework and try to make a summary of various of framework, to gain a better understanding of the entire machine learning pipeline.

## Determined AI - AI Infrastructure goes Open Source
News link: https://determined.ai/blog/ai-infrastructure-for-everyone/
Platform product webpage: https://determined.ai/
Github opensource repo: https://github.com/determined-ai/determined

Today I read about this deep learning training platform from Determined AI that helps to solve the DevOps headache for training models, share GPU resources and scale up the development.

Determined AI is a deep learning training platform that tries to bridges the gap between deep learning tools like TensorFlow and PyTorch. It tries to boost the process of DL as shown in the figure [loop.png]

The Determined Training Platform (https://determined.ai/developers/) tightly integrates following key features:
- High-performance distributed training: distrubuted training support built upon Horvod (distributed training framework), with optimization of twice the performance of Horvod. Distribute easily set-up without any additional changes to your model code, allows multiple users to seamlessly share the same GPU cluster.
- State-of-the-art hyperparameter search: based on research results [reference 12345]. 100x faster than standard search methods and 10x faster than Bayesian Optimization methods.
- DL tools for both individuals and teams: support experiment management with built-in experiment tracking, log management, metrics visualization, reproducibility, automatic fault tolerance for DL training jobs and dependency management.
- Flexible GPU scheduling: including dynamically resizing training jobs on-the-fly and automatic management of cloud resources on AWS and GCP
- Hardware-agnostic and integrated with the Open Source Ecosystem: support public cloud and on-prem infrastructure. Integrated with TensorBoard and GPU-powered Jupyter notebooks. See integrated tools diagram below:[determined-components.png]

Most of the guidance can be found at Github page
Installation guidance: https://docs.determined.ai/latest/how-to/install-main.html
Quick Start Guide: https://docs.determined.ai/latest/tutorials/quick-start.html
Documentation: https://docs.determined.ai/latest/index.html
