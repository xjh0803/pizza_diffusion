# pizza_diffusion

convert rlds to zarr
```
pip install zarr
pip install h5py
```
1. rlds to hdf5(rlds2hdf5.py)
2. hdf5 to zarr(hdf52zarr.py)

这时converted_data.zarr目录结构为
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
主要改动文件：
```
├── diffusion_policy
    ├── dataset
      └── pizza_dataset.py
    ├── env_runner
      └── pizza_image_runner.py
    ├── env
      └── pizza_env.py
      └── pizza_image_env.py
├── pizza_diffusion_policy.yaml
```

run
```
python train.py --config-dir=. --config-name=pizza_diffusion_policy.yaml training.seed=42 training.device=cuda:0 hydra.run.dir='data/outputs/${now:%Y.%m.%d}/${now:%H.%M.%S}_${name}_${task_name}'
```
