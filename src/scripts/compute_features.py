import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import settings
from dataset import CUB_200_2011
from storage import datastore
from deep_extractor import CNN_Features_CAFFE_REFERENCE
import pyprind
import click


@click.command()
@click.argument('sname')
@click.argument('iteration', type=click.INT)
@click.argument('cropped', type=click.BOOL)
@click.option('--full', type=click.BOOL, default=False)
@click.option('--flipped', type=click.BOOL, default=False)
@click.option('--force', type=click.BOOL, default=False)
def main(sname, iteration, cropped, full, flipped, force):
    new_name = '%s-%d' % (sname, iteration)
    cub = CUB_200_2011(settings.CUB_ROOT, full=full)
    ft_storage = datastore(settings.storage(new_name))
    ft_extractor = CNN_Features_CAFFE_REFERENCE(ft_storage, model_file=settings.model(new_name), pretrained_file=settings.pretrained(new_name), full=full)
    number_of_images_in_dataset = sum(1 for _ in cub.get_all_images())
    bar = pyprind.ProgBar(number_of_images_in_dataset, width=80)
    for t, des in ft_extractor.extract_all(cub.get_all_images(), flip=flipped, crop=cropped, bbox=cub.get_bbox(), force=force):
        bar.update()
    print 'DONE'

if __name__ == '__main__':
    main()
