import xarray

from .xarray import DatasetAdapter


def read_netcdf(filepath):
    ds = xarray.open_dataset(filepath)
    return DatasetAdapter.from_dataset(ds)
