# Robot Behavior Classification Using ConvLSTM

A vision‑based deep learning system for detecting **robotic behavior anomalies** from video sequences.  
This project uses a **custom ConvLSTM architecture** to jointly learn spatial and temporal patterns in video frames, enabling detection of subtle anomalies beyond simple success/failure checks.

---

## 📌 Project Overview
- **Goal:** Classify robot task executions as **Positive** (correct or minimal deviation) or **Negative** (anomalous execution) from recorded video sequences.
- **Key Features:**
  - Custom ConvLSTM model capturing spatio‑temporal features.
  - Automated frame extraction and preprocessing pipeline.
  - Targeted data augmentation to address class imbalance.
  - Evaluation on unseen videos with qualitative and quantitative comparisons.

---

## 📂 Dataset
- **Raw Data:** 170+ robot activity videos.
- **Metadata:** `.xlsx` file containing instructions, ground truths (with timestamps), and anomaly descriptions.
- **Processing:**
  - Cleaned and restructured metadata for binary classification.
  - Manually annotated missing entries by reviewing videos.
  - Synchronized video files with updated metadata.

---

## 🛠 Step‑by‑Step Approach
1. **Data Preparation**
   - Removed redundant metadata columns.
   - Added binary label column: `1` → Positive, `0` → Negative.
   - Filled missing annotations manually.

2. **Frame Extraction**
   - Extracted 20 evenly spaced frames per video.
   - Resized frames to `64×64`, normalized pixel values.
   - Organized into Positive/Negative directories.

3. **Data Augmentation**
   - Applied transformations (rotation, shift, flip, brightness) to the Negative class to balance the dataset.

4. **Train–Test Split**
   - 70–30 stratified split to preserve class ratios.
   - Computed class weights to reduce bias.

5. **Model Development**
   - Custom ConvLSTM2D architecture with 3D max pooling, batch normalization, dropout, and dense layers.
   - Compiled with Adam optimizer, binary cross‑entropy loss.
   - Used EarlyStopping, ReduceLROnPlateau, and LearningRateScheduler.

6. **Evaluation**
   - Metrics: Accuracy, AUC, F1‑score, balanced accuracy.
   - Tested on unseen videos, compared predictions with ground truth.

---

## 📊 Results

| Metric                | Value    |
|-----------------------|----------|
| **Training Accuracy** | ~81.4%   |
| **Validation Accuracy** | ~79.0% |
| **AUC Score**         | 0.853    |
| **Positive Class Recall** | 100% |
| **Negative Class Accuracy** | 62.9% |


---

**Full Dataset** – *https://drive.google.com/drive/folders/1DHuYOJqtoWb1CvYQnGXXFKIbG6721HkC?usp=sharing*
