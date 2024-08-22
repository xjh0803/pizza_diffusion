import tensorflow as tf
import tensorflow_datasets as tfds
import h5py
import os
import numpy as np

rlds_dataset_dir = '/home/v-wenhuitan/tensorflow_datasets/pizza_dataset_dataset/pizza_dataset/1.0.0'
h5_dataset_dir = '/home/v-wenhuitan/diffusion_policy/octo/difpol/data'
output_filename = os.path.join(h5_dataset_dir, 'merged_dataset.h5')

def process_data(episode):
    act_data_dict = {
        '/observations/image': [],
        '/action': [],
    }

    for step in episode['steps']:
        action = step['action']
        observation = step['observation']  

        act_data_dict['/observations/image'].append(observation['image'])
        act_data_dict['/action'].append(action)

    # 将数据转换为 NumPy 数组
    act_data_dict['/observations/image'] = np.array(act_data_dict['/observations/image'])
    act_data_dict['/action'] = np.array(act_data_dict['/action'])

    # 确保长度一致
    assert len(act_data_dict['/action']) == len(act_data_dict['/observations/image'])

    return act_data_dict

def save_merged_data_to_h5(episodes_data, episode_ends, output_filename):
    with h5py.File(output_filename, 'w', rdcc_nbytes=1024 ** 2 * 2) as root:
        root.attrs['sim'] = False

        # merge all eposide
        merged_image_data = np.concatenate([ep['/observations/image'] for ep in episodes_data], axis=0)
        merged_action_data = np.concatenate([ep['/action'] for ep in episodes_data], axis=0)

        # creat//chunk中100可改动，但img和action需一致
        root.create_dataset('img', data=merged_image_data, dtype='uint8', chunks=(100, 224, 224, 3))
        root.create_dataset('action', data=merged_action_data, dtype='float32',chunks=(100, 7))
        root.create_dataset('episode_ends', data=episode_ends, dtype='int64')

    print(f'Saved to {output_filename}')

def rlds2h5(rlds_dataset_dir, output_filename):
    builder = tfds.builder_from_directory(builder_dir=rlds_dataset_dir)
    ds = builder.as_dataset(split='train')

    episodes_data = []
    episode_ends = []
    total_steps = 0

    for i, episode in enumerate(ds):
        processed_episode = process_data(episode)
        episodes_data.append(processed_episode)
        total_steps += len(processed_episode['/action'])
        episode_ends.append(total_steps)

    save_merged_data_to_h5(episodes_data, np.array(episode_ends), output_filename)

def main():
    if not os.path.exists(h5_dataset_dir):
        os.makedirs(h5_dataset_dir)

    if not os.path.exists(rlds_dataset_dir):
        raise ValueError(f"The RLDS directory '{rlds_dataset_dir}' does not exist.")

    rlds2h5(rlds_dataset_dir, output_filename)

if __name__ == '__main__':
    main()