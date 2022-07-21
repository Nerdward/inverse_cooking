## Inverse Cooking: Recipe Generation from Food Images

### Installation

This code uses Python 3.6 and PyTorch 0.4.1 cuda version 9.0.

- Creating virtual environment:
```bash
conda create -n inv_cooking python=3.6
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

### Demo

You can use our pretrained model to get recipes for your images.

Download the required files (listed above), place them under the ```data``` directory, and try our demo notebook ```src/demo.ipynb```.

Note: The demo will run on GPU if a device is found, else it will use CPU.

### Data

- Download [Recipe1M](http://im2recipe.csail.mit.edu/dataset/download) (registration required)
- Extract files somewhere (we refer to this path as ```path_to_dataset```).
- The contents of ```path_to_dataset``` should be the following:
```
det_ingrs.json
layer1.json
layer2.json
images/
images/train
images/val
images/test
```

*Note: all python calls below must be run from ```./src```*

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