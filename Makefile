# Makefile
SHELL = /bin/bash

artifacts:
	wget https://dl.fbaipublicfiles.com/inversecooking/ingr_vocab.pkl -P app/artifacts/
	wget https://dl.fbaipublicfiles.com/inversecooking/instr_vocab.pkl -P app/artifacts
	wget https://dl.fbaipublicfiles.com/inversecooking/modelbest.ckpt -P app/artifacts