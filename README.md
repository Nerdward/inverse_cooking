## FoodAI 

## Table of contents
1. [Installation guide](#installation)
2. [Backend](#backend-server)
3. [Frontend](#frontend)

### Installation

This code uses Python 3.6 and PyTorch 0.4.1 cuda version 9.0.
- Packages setup
```bash
$ pip install --editable .
```

- Creating virtual environment:
```bash
conda create -n inv_cooking
```
- Activate the virtual environment
```bash
conda activate inv_cooking
```

- Installing PyTorch:
```bash
$ conda install pytorch=0.4.1 cuda90 -c pytorch
```

- Install dependencies
```bash
$ pip install -r requirements.txt
```

### Pretrained model
- To download the Ingredient, Instruction vocabularies and pretrained model weights. Run:
```bash
$ make artifacts
```

### Backend Server
- To start up the fast api and uvicorn server
```bash
$ cd app
```
```bash
$ uvicorn app.api:app \       # location of app (`app` directory >`api.py` script > `app` object)
    --host 0.0.0.0 \        # localhost
    --port 8000 \           # port 8000
    --reload \              # reload every time we update
    --reload-dir tagifai \  # only reload on updates to `tagifai` directory
    --reload-dir app        # and the `app` directory
```

### Frontend
- To start up the streamlit frontend server, run
```bash
$ cd frontend
```

```bash
$ streamlit run home.py
```


Code supporting the paper:

*Amaia Salvador, Michal Drozdzal, Xavier Giro-i-Nieto, Adriana Romero.
[Inverse Cooking: Recipe Generation from Food Images. ](https://arxiv.org/abs/1812.06164)
CVPR 2019*

```
@InProceedings{Salvador2019inversecooking,
author = {Salvador, Amaia and Drozdzal, Michal and Giro-i-Nieto, Xavier and Romero, Adriana},
title = {Inverse Cooking: Recipe Generation From Food Images},
booktitle = {The IEEE Conference on Computer Vision and Pattern Recognition (CVPR)},
month = {June},
year = {2019}
}
```