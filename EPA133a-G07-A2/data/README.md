# Data for Model Generation of Simple Transport Model Demo in MESA

Created by:
Yilin HUANG

Email:
y.huang@tudelft.nl

Version:
1.0

## Introduction

The simple transport model demo, see [../model/model.py](../model/model.py) for EPA133a Advanced Simulation course Assignment 2, takes a `csv` input data file that specifies the infrastructure model components to be generated. The data format used **by the demo model** is described here.

## Format

|     Column | Description                                              |
| ---------: | :------------------------------------------------------- |
|       road | On which road does the component belong to               |
|         id | **Unique ID** of the component                           |
| model_type | Type (i.e. class) of the model component to be generated |
|       name | Name of the object                                       |
|        lat | Latitude in Decimal Degrees                              |
|        lon | Longitude in Decimal Degrees                             |
|     length | Length of the object in meters                           |

The column `road` is used by the model generation to classify model components by roads, i.e., on which road does a component belong to. The model generation assumes that the infrastructure model components of the same road is ordered sequentially. This means, e.g. in `demo-1.csv`, component `100000` is connected to component `100001`, that is connected to component `100002`, that is connected to component `100003`, etc., all of which are on road `N1`.

The column `model_type` is used by the model generation to identify which class of components to be generated. The `model_type` labels used in this column must be consistent with the labels in the `generate_model` routine.

The rest of the information is used to instantiate the components (objects).

You may change the data format and structure if the model generation (`generate_model`) routine is adapted accordingly.

All data files contained in this directory are used as demonstration for model generation. They are not based on real data.
