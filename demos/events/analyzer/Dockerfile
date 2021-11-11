FROM python:3.8

ENV SPARK_VERSION=3.1.2
ENV HADOOP_VERSION=3.2

RUN apt-get update && apt-get install -y openjdk-11-jre-headless

RUN mkdir -p /opt && \
  cd /opt && \
  curl https://downloads.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz | tar -zx && \
  ln -s spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} spark

RUN cd /opt/spark/jars && \
  curl -O https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.63/aws-java-sdk-bundle-1.12.63.jar && \
  curl -O https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.2.0/hadoop-aws-3.2.0.jar

ENV PATH=$PATH:/opt/spark/bin
ENV SPARK_HOME=/opt/spark

COPY requirements.txt  .
RUN  pip3 install -r requirements.txt

COPY analyzer.py .

ENTRYPOINT ["spark-submit", "analyzer.py"]
