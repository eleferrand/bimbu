install:
	pip install praatio
	git clone https://github.com/xinjli/allosaurus.git
	sed -i "s/https:\/\/github.com\/xinjli\/allosaurus\/releases\/download\/v1.0\/' + model_name + '.tar.gz'/https:\/\/github.com\/eleferrand\/bimbu\/raw\/main\/big_kun.tar.gz'/g" allosaurus/allosaurus/bin/download_model.py
	cd allosaurus && python setup.py install
	python -m allosaurus.bin.download_model
	cd ..
test:
	cd allosaurus && python -m allosaurus.run -i sample.wav