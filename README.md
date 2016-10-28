#Scaner
## Getting Started

Scaner, Social Context Analysis aNd Emotion Recognition is a platform to collect and analyse social context, i.e context of users and content in social media. In particular, Scaner detects possible influencers and assess their relevance and impact capabilities in a given topic.

Scaner uses data from Twitter to do several tasks as:

- Rank most influential users in Twitter according to topics
- Find the network of an user
- Analyze data from tweets studying its impact or relevance.

To do so, Scaner provides an API REST to easily manage data and periodically calculate metrics of users and tweets.

##Arquitecture
![alt tag](https://raw.githubusercontent.com/gsi-upm/scaner/newdata/overview.png?token=AKvRCZVCM46LZWHwF_50RvQPtwBSjtzaks5X389rwA%3D%3D)

## Installation
Firstly you have to install [Docker](https://docs.docker.com/engine/installation/) and Docker Compose. This can be easily installed with [pip](https://pip.pypa.io/en/stable/installing/):
```
$ pip install docker-compose
```

Now, clone the repository into your local system
```
$ git clone http://github.com/gsi-upm/scaner
```
Use Docker Compose to build the application:

```
$ cd scaner
$ docker-compose build
```
Then, it is necessary to run **OrientDB**
```
$ ./populate_schema.sh
```
Finally, we run the application
```
$ docker-compose up
```
Scaner application it is now available on port **5000**

More
----

For more information visit: http://scaner.readthedocs.io/en/latest/

Acknowledgement
---------------
This development has been partially funded by the European Union through the MixedEmotions Project (project number H2020 644632), as part of the `RIA ICT 15 Big data and Open Data Innovation and take-up` programme.


.. image:: img/me.png
    :target: http://mixedemotions-project.eu
    :height: 100px
    :alt: MixedEmotions Logo

.. image:: img/eu-flag.jpg
    :height: 100px
    :target: http://ec.europa.eu/research/participants/portal/desktop/en/opportunities/index.html


![GSI Logo](http://vps161.cesvima.upm.es/images/stories/logos/gsi.png)
