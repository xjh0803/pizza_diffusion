# pizza_diffusion

convert rlds to zarr
1. rlds to hdf5

2. hdf5 to zarr

这时目录结构为
```
├── action
├── img
├── episode_ends

```
需要手动调整为类似pusht_cchi_v7_replay.zarr样式
```
├── data
│ ├── action
│ └── img
├── meta
│ ├── episode_ends
```
