#!/bin/sh
./quantize.py trained/ai85-cifar100-qat8.pth.tar trained/ai85-cifar100-qat8-q.pth.tar --device MAX78000 -v "$@"
