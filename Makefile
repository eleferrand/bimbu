install:
	pip install praatio
	cd allosaurus && python setup.py install
	python -m allosaurus.bin.download_model
	cd ..
test:
	cd allosaurus && python -m allosaurus.run -i sample.wav