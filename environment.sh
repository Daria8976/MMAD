conda create -n mmad python=3.10 -y
conda activate mmad
pip install --upgrade pip  # enable PEP 660 support
cd VideoCaption
pip install -e .
pip install -e ".[train]"
pip install flash-attn --no-build-isolation
pip install decord opencv-python git+https://github.com/facebookresearch/pytorchvideo.git@28fe037d212663c6a24f373b94cc5d478c8c1a1d
cd ..
pip install -r requirements.txt