# python-flask-docker

### Final course project "ML in business"

**Stack:**

- ML: sklearn, pandas, numpy, matplotlib
- API: flask
- VM: docker
- Data from kaggle: [Jigsaw Toxic comment competition](https://drive.google.com/file/d/1Vdj89P-V11ipZOCFpeM3ggWVWq3O29sj/view?usp=sharing)


**Task:** 
Predict different types of of toxicity like threats, obscenity, insults, and identity-based hate. Binary classification.




Only one feature:
- comment_text (text)


Feature transform: 
- regex clean
- tfidf

Model: logreg

## Clone git and make docker image
```
$ git clone https://github.com/hildar/python-flask-docker.git
$ cd python-flask-docker/docker
$ docker build -t python-flask-docker app/
```

## Run docker container
```
$ docker run -d -p 8180:8180 -p 8181:8181 python-flask-docker
```

## Usage

Now, there are two ways: 

#### 1-st way

Go to the address [https://localhost:8180](https://localhost:8180) and use front server. You can manually type some comment at the web form.

#### 2-nd way

Use Jupiter Notebook "Clien.ipynb" and step by step check server.

