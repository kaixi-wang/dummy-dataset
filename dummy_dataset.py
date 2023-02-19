import fiftyone as fo
import fiftyone.zoo.datasets.base as fozb

def download_and_prepare(dataset_dir, scratch_dir, split=None):
    zoo_dataset = fozb.QuickstartDataset()
    dataset_type, _, _ = zoo_dataset._download_and_prepare(
        dataset_dir, scratch_dir, split
    )

    return fo.Dataset.from_dir(
        dataset_dir=dataset_dir, dataset_type=dataset_type
    )
