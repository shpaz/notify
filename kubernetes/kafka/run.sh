#! /bin/bash 
kubectl create namespace kafka && \
kubectl apply -k github.com/Yolean/kubernetes-kafka/variants/dev-small/?ref=v6.0.3
