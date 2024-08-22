import zarr
from hdf5zarr import HDF5Zarr

file_name = '/home/v-wenhuitan/diffusion_policy/octo/difpol/data/merged_dataset.h5'
hdf5_zarr = HDF5Zarr(filename = file_name, store_mode='w', max_chunksize=2*2**20)
zgroup = hdf5_zarr.consolidate_metadata(metadata_key = '.zmetadata')
# 创建一个新的 Zarr 存储并保存数据
zarr_store = zarr.DirectoryStore('converted_data.zarr')
root = zarr.group(store=zarr_store, overwrite=True)

# 将转换后的 Zarr 数据保存到新文件中
for key, value in zgroup.items():
    root[key] = value

print("Zarr data has been saved to 'converted_data.zarr'")

