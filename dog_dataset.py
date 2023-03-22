import os
import requests
import fiftyone as fo
import tarfile
def download_and_prepare(dataset_dir=None, scratch_dir=None, split=None):
    url = 'http://vision.stanford.edu/aditya86/ImageNetDogs/images.tar'

    target_dir = os.path.join(fo.config.dataset_zoo_dir
                              , "temp-dataset")
    if not scratch_dir:
        scratch_dir = target_dir
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    target_path = os.path.join(target_dir,
                               "aditya86/ImageNetDogs/images.tar".replace("/",
                                                                          "-"))
    if not os.path.exists(target_path):

        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(target_path, 'wb') as f:
                f.write(response.raw.read())

    # with tarfile.open(target_path, "r") as tf:
    #     print(tf.getmembers())
    if not dataset_dir:
        dataset_dir = os.path.join(fo.config.dataset_zoo_dir, target_path.split(
                '/')[-1].split(".")[0])
    if not os.path.exists(dataset_dir):
        os.makedirs(dataset_dir)

    with tarfile.open(target_path, "r") as tf:
        dataset_dir = os.path.join(fo.config.dataset_zoo_dir, target_path.split(
                '/')[-1].split(".")[0])
        if not os.path.exists(dataset_dir):
            os.makedirs(dataset_dir)
        tf.extractall(path=dataset_dir)

    samples =[]
    for path, subdirs, files in os.walk(dataset_dir):
        for name in files:
            filepath = (os.path.join(path, name))
            sample = fo.Sample(filepath=filepath)
            samples.append(sample)

    # Create dataset
    dataset = fo.Dataset("ImageNet-Dogs")
    dataset.add_samples(samples)
    return dataset