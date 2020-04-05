# Dashboard OCR

Python OCR integral frame for Industry Dashboards

## Usage

1. Get the code from Github clone or download zip by clicking [this](https://github.com/zolars/dashboard-ocr/archive/master.zip).

   ```
   $ git clone https://github.com/zolars/dashboard-ocr.git
   ```

2. You need to install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) and [SQLite](https://sqlite.org) on your computer.

   ```
   $ conda -V
   conda 4.7.11
   ```

3. Create the environment and install dependencies.

   ```
   $ cd dashboard-ocr
   $ conda env create -f environment.yml
   $ conda activate dashboard-ocr
   $ python -V
   Python 3.6.8 :: Anaconda, Inc. 
   $ python -m pip install -r requirements.txt
   ```

   If you want to edit or update your environment, use:
   
   ```
   $ conda env update -f environment.yml
   ```

4. Install packages. See [PyTorch-YOLOv3](https://github.com/eriklindernoren/PyTorch-YOLOv3).

   * PyTorch-YOLOv3 : A minimal PyTorch implementation of YOLOv3, with support for training, inference and evaluation. Download pretrained weights

     ```
     $ cd ./packages/yolov3/weights/
     $ bash download_weights.sh
     ```

5. Run the app.
   ```
   $ conda activate dashboard-ocr
   $ export FLASK_APP=app
   $ export FLASK_ENV=development
   $ flask run
   ```