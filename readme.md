# Introduction

This repository contains one of the
approach in order to addressed categories to a product.

# Repository structure
## Category Service
It contains the category's prediction service.
## Data
All data created and needed are stored in this directory.
This include the original input data, training data set.
## Data Analysis
Notebook in which I performed a simple data analysis.
## Model
It contains one data structure (Product) and some helper functions. 

## Pseudo pipeline
It contains the controller and the category client in order
to run a local data pipeline.

## Research and development 
Most of the experiments whose have been
conducted in order to find out the best model to solve
this task happened here.

# Solution explanation
Immediately I chose a BERT language model (https://arxiv.org/pdf/1706.03762.pdf). With the library Farm
is it very easy to train a german model for text classification.
Also all the pre-processing 
steps are done by the library (tokenization etc). 
This is a plus in order to avoid 
code duplicate.


I did not want to go for a regex one, because it is too much maintenance.


A solution based on hand made features could have solved this problem better.
Nevertheless I did want to pick up this solution, because:

    1. It would have been long to create rules for hundreds of categories
    2. It is hard to maintain
    3. It is not convenient to adapt (e.g. new category)

To fake the Google cloud service you wanted,
I decided to create a docker image container. 
The pseudo_pipeline is a tiny version of a pipeline Media Markt could have.
In this pipeline it is possible to send requests to get the product's categories.


## Pre processing steps
I did not perform a lot of pre-processing steps. Because it will be duplicate code,
it will make the model less universal. If we train the model with a data set 
respecting the 4V. Pre-processing steps should be required.

We could implement a translation service because media markt data base
may contain a lot of different language. by translation to german we could save us
the creation of some models.

By creating the training data and by creating the input string which will be feed to the 
model I just concatenated all the strings I have. Please see `utils/utils.py`

# How to run
Generate the training data.
Then train the model.
Put the model into the image's storage.
Run the docker container.
Finally you can send to the docker container requests in order to get
the categories of a product.

## Create training data

`utils/create_training_data_multi_class_multi_label.py`


## Train the model

`research_and_development/train_model/train_multi_label_multi_class.py`
## Move model to category directory
When your model will be trained, put the files contained 
in  `research_and_development/trained_model/category_multi_class_multi_label_name_description 
into `category_service/service/category_model`.


## Run docker image
Go to the image directory and run the following commands:
`docker-ompose up`

## Send request to service
You have 2 possibilities.

Use the pseudo pipleine 
Or send a `curl request to the serivce curl -s 127.0.0.1:8810/api/inference   -d '{"name": article.name,
                "short_description": "This is good short description",
                "short_description_mm": "NO_TEXT",
                "long_description": "NO_TEXT",
                "long_description_mn": "NO_TEXT",
                "marketing_text_mm": "Marketing teams made this product awsome"
                }'   -H 'content-type: application/json' | jq`

# Data Analysis
Please have a look at the notebook for more insights.

it looks like some categories are just there when the article is blocked or deleted.

By performing simple data analytics, I was able to see that
the short_description is the only column always fulfilled.

sometimes the article has no label (3 times)

all data is not complete. sometimes only one article is completed
but the other ones (e.g. other colors) are not.

so i will do 1 data with all info and another one without.
I will then predict on this data to get more training data.

it happens also that the short_description is a smaller version of the name. 
By seeing that, a sentence comparison could be implemented in order to create a better data
set by avoiding very similar sentences.

also it looks like that with just the name, one could find out the categories of a product.

## Conclusion of data analysis
The data is highly unbalanced. This should be solved. also some labels present in the 
labeld product are not in my hash tabel id-label.

# Train the model
To train the model please run `research_and_development/train_model/train_multi_label_multi_class.py`
## Architecture
It is BERT language model (for german). The last layer is the classification layer.
## Results analysis

do some plots here

## Possible experiments 

I tried to train a multi-class model. The performances are much better.
We could use this kind of model as back up, if the multi-class multi-label model
does not find any category for the the given product.

# Docker image

The docker performs the prediction of a product category(ies).

# Pipeline explanation

## Pseudo pipeline
In this script we get all the products contains in our fake data base (csv file).
After we send them one after the other to the service in order to get their predicted
category.
After getting the category, the methode get_parent is called in order to get the product
parent's categories.

Finally we could save the enhanced product to a data base.

# Ideas for a better solution and outlook

## Model

The model architecture is good. Maybe too slow for this tasks.

## Training data
With only 1k samples in train,dev and test sets, the model is able to learn
enough features. There are 530 different labels. So it means some label have few samples.
A more balanced training data should be used.

by generating the training data, if a product has just a number id, we could 
send a request to another retailer in order to get more information about (e.g. in other
mediamarkt market place and then translate).

## Pipeline

In my solution, we are getting the product from a csv file.
Getting the product data from a data base will be better.
After enriching the product data we should also save
the enhance product into the data base.

## Service

On the service side, we are predicting on batch size of 1.
Use the predict on my batch in a better way. 
We could implement a wait function, that gather an optimal amount of data 
to be predicted and then send the data to service. 

to encounter the fact that sometimes the model does not find any category
we could a another model to assign 1 category.

## Data Analytic
I performed a short data analytics. This could have be done deeper.
With the basic information I get, I thought I could train a good model.
It showed that the trained model is barely acceptable. 
A deeper data analytic should help to increase the model f1 macro score.


## General
Use a source-code, bug and quality checker (e.g. Pylint).
Implemenation of mock-ups and unittests. 
