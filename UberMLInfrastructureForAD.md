title: Uber ATG's ML Infrastructure and Version Control Platform Architecture
original post link: https://eng.uber.com/machine-learning-model-life-cycle-version-control/
Chinese version: https://mp.weixin.qq.com/s/yJzW3-RLC0d05vW2EqjY0w
Uber ATG: Advanced Technologies Group, developing self-driving vehicles technology.

General introduction of contents: ML components, development life cycle, automating tool (VerCD - Ver continuous delivery)

## Self-driving vehicle ML model components
Software components (tasks) that contains one or more ML models
- Perception: Object identification (types: vehicle, pedestrian, bicycle, etc.) and 3D localization.
- Prediction: Combine object detection results (type + localization) with HD maps, to perform object trajectory prediction in future n seconds in a given scene. The Prediction component allows the self-driving vehicle to anticipate where actors will most likely be located at various points in the future.
- Motion Planning:
  - Input:
    - self-driving vehicle’s destination
    - the predicted trajectories of all actors in the scene
    - the high definition map
    - other mechanisms
  - Output: plan the path of the vehicle.
- Control: Path following for motion planned path by controlling steering, brakes and accelerator.

## ML model life cycle.
Training data source: sensor-equipped vehicles(Lidar, cameras, radar) in a wide variety of traffic situations.
Labeling work: location, shape, other attributes like object type, etc.
Model training: sufficient labeled training data + HD map
ML Model different layers: highest layer: ML applications, middle layer: common ML libraries such as TF and PyTorch, GPU acceleration.
Five-step life cycle for training and deployment of ML models:
[ATG_ML_platform_figure-lifecycle.png]

### Data ingestion
Data ingestion process: Select the logs intended to use and extract data from them.

1. Data log selection and dividing: 75% training data, 15% testing data, 10% validation data. The pipeline used to select logs and split the data into 3 groups based on geographical location: GeoSplit.

2. Data extraction from logs (Using Petastorm, Uber ATG's open source data accesss library for DL):
Data contents:
- Images from the vehicle’s cameras
- LiDAR 3D point information
- Radar information
- The state of the vehicle, including location, speed, acceleration and heading
- Map information, such as the vehicle’s route and lanes it used
- Ground truth labels
Extraction process:
- extract data from multiple logs in parallel using Apache Spark (this way keeps the data in an optimized format by storing all info needed in GPUs memory after load from HDFS, so the training is efficient)
- save data log-by-log on HDFS
[ATG_ML_platform_figure-extraction.png] shows the extraction process running on CPU cluster.

### Data validation
1. Run queries to pull: 1) the number of frames in a scene 2) the number of occurrences of the different label types.
2. Compare results to previous data sets to see how conditions have changed. Further analysis needed if not as expected.

### Model training
Distributed ML training system used: Horovod!
1. Spread the training process on different GPUs with data parallelism as shown in figure below (same model trained on different GPUs with different parts of data). Each process performs forward and backword propagation independently.
[ATG_ML_platform_figure-modeltraining.png]
2. Combine the parallel-trained model(knowledge distributing as I understand): using Horovod's ring-allreduce algorithm to average gradients and disperse them to all work nodes without requiring a parameter server.
3. Training verification: through TensorBoard, leveraging ML frameworks like TensorFlow and PyTorch.

ML computing with hybrid approach: both in on-premise data centers powered by GPU and CPU clusters as well as in the cloud.
- on-premise data center: orchestrate training jobs using Peloton (https://eng.uber.com/resource-scheduler-cluster-management-peloton/), to scales jobs to GPUs and CPUs.
- cloud-based training: using Kubernetes (https://kubernetes.io/) to deploy and scale application containers across clusters.

### Model evaluation
Evaluate the performance on model itself (with model-specific metrics) and on entire system (with system metrics). Also use hardware metrics to evaluate the model running speed on hardware.
1. Model-specific metrics
For example, Perception model: precision(correct detection rate) and recall(the proportion of the ground truth objects that model identified correctly).
For not performing well metrics, we adjust data pipeline by including similar cases(https://eng.uber.com/searchable-ground-truth-atg/) (data augmentation). But prevent overfitting.
2. System metrics
Mainly safety and comfort measurement on overall vehicle motion, with large test set. Performed after model-specific metrics are well enough. Due to ML model dependencies, the system evaluation will give a comprehensive overview between components.
3. Hardware metrics
Using ATG's internal benchmarking system to profile a certain part of software, and evaluate how quick it will run on vehicle hardware.

### Model serving
Deploy the model on an inference engine in vehicle with continuous iteration, focusing on the part need to be improved learnt from model evaluation part.

## Accelerating ML research with CI and CD
Continuous integration and delivery (VerCD platform) will wrap and automate the 5-step ML model developing process to an end-to-end workflow, reduce errors and boost the speed.

The VerCD platform is such a system that tracks dependencies between code, datasets and models throughout the workflow, starts with the dataset extraction stage, cover model training, and conclude with computing metrics.
