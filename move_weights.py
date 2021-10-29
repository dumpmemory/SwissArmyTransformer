# %%
# import torch
# old = torch.load('pretrained/cogview/cogview-caption/30000/mp_rank_00_model_states.pt.sat1', map_location='cpu')

# old['module']['transformer.word_embeddings.weight'] = old['module']['word_embeddings.weight']
# del old['module']['word_embeddings.weight']

# from model.base_model import BaseModel
# import argparse
# import os
# args = argparse.Namespace(
#     num_layers=48,
#     vocab_size=58240,
#     hidden_size=2560,
#     num_attention_heads=40,
#     max_sequence_length=1089,
#     hidden_dropout=0.1,
#     attention_dropout=0.1,
#     checkpoint_activations=True,
#     checkpoint_num_layers=1,
#     sandwich_ln=True,
#     model_parallel_size=1,
#     world_size=1,
#     rank=0
#     )
# init_method = 'tcp://'
# master_ip = os.getenv('MASTER_ADDR', 'localhost')
# master_port = os.getenv('MASTER_PORT', '6000')
# init_method += master_ip + ':' + master_port
# torch.distributed.init_process_group(
#         backend='nccl',
#         world_size=args.world_size, rank=args.rank,init_method=init_method)
# import mpu
#     # Set the model-parallel / data-parallel communicators.
# mpu.initialize_model_parallel(args.model_parallel_size)
# print('bg')
# model = BaseModel(args)
# # %%
# missing_keys, unexpected_keys = model.load_state_dict(old['module'], strict=False)
# torch.save(old, 'pretrained/cogview/cogview-caption/30000/mp_rank_00_model_states.pt')



# %%
import torch
old = torch.load('/dataset/fd5061f6/english_data/checkpoints/blocklm-10b-1024/126000/mp_rank_00_model_states.pt', map_location='cpu')
# old['module']['transformer.word_embeddings.weight'] = old['module']['word_embeddings.weight']
# del old['module']['word_embeddings.weight']
#%%
import torch

from model.cuda2d_model import Cuda2dModel
import argparse
import os
args = argparse.Namespace(
    num_layers=48,
    vocab_size=58240,
    hidden_size=2560,
    num_attention_heads=40,
    max_sequence_length=1089,
    hidden_dropout=0.1,
    attention_dropout=0.1,
    checkpoint_activations=True,
    checkpoint_num_layers=1,
    sandwich_ln=True,
    model_parallel_size=1,
    world_size=1,
    rank=0,
    new_sequence_length=1089+4096,
    layout='0,64,1088,5184',
    kernel_size=9,
    kernel_size2=7
    )

init_method = 'tcp://'
master_ip = os.getenv('MASTER_ADDR', 'localhost')
master_port = os.getenv('MASTER_PORT', '6000')
init_method += master_ip + ':' + master_port
torch.distributed.init_process_group(
        backend='nccl',
        world_size=args.world_size, rank=args.rank,init_method=init_method)
import mpu
    # Set the model-parallel / data-parallel communicators.
mpu.initialize_model_parallel(args.model_parallel_size)
print('bg')
#%%
model = Cuda2dModel(args)

#%%
oldm = old['module']
for k in list(oldm.keys()):
    if k.startswith('mixins.0'):
        new_k = k.replace('mixins.0', 'mixins.extra_position_embedding')
    elif k.startswith('mixins.1'):
        new_k = k.replace('mixins.1', 'mixins.attention_plus')
    else:
        continue
    oldm[new_k] = oldm[k]
    del oldm[k]

#%%
old['module']['mixins.0.position_embeddings.weight'] = old['module']['transformer.position_embeddings_plus.weight']
del old['module']['transformer.position_embeddings_plus.weight']

for i in range(48):
    old['module'][f'mixins.1.query_key_value.{i}.weight'] = \
        old['module'][f'transformer.layers.{i}.attention.query_key_value_plus.weight']
    del old['module'][f'transformer.layers.{i}.attention.query_key_value_plus.weight']
    old['module'][f'mixins.1.query_key_value.{i}.bias'] = \
        old['module'][f'transformer.layers.{i}.attention.query_key_value_plus.bias']
    del old['module'][f'transformer.layers.{i}.attention.query_key_value_plus.bias']
    old['module'][f'mixins.1.dense.{i}.weight'] = \
        old['module'][f'transformer.layers.{i}.attention.dense_plus.weight']
    del old['module'][f'transformer.layers.{i}.attention.dense_plus.weight']
    old['module'][f'mixins.1.dense.{i}.bias'] = \
        old['module'][f'transformer.layers.{i}.attention.dense_plus.bias']
    del old['module'][f'transformer.layers.{i}.attention.dense_plus.bias']
# %%
missing_keys, unexpected_keys = model.load_state_dict(old['module'], strict=False)

# %%
torch.save(old, 'pretrained/cogview/cogview2-base/6000/mp_rank_00_model_states.pt')
# # %%
# import torch
# old = torch.load("/dataset/fd5061f6/cogview/zwd/vqgan/l1+ms-ssim+revd_percep/checkpoints/last.ckpt", map_location='cpu')

# # %%
# from collections import OrderedDict
# new_ckpt = OrderedDict()
# for k,v in old['state_dict'].items():
#     new_ckpt[k] = v.detach()
# torch.save(new_ckpt, 'pretrained/vqvae/l1+ms-ssim+revd_percep.pt')
# # %%

# %%

old['module']['transformer.word_embeddings.weight'] = old['module']['word_embeddings.weight']
del old['module']['word_embeddings.weight']
#%%
import torch

from model.glm_model import GLMModel
import argparse
import os
args = argparse.Namespace(
    num_layers=48,
    vocab_size=50304,
    hidden_size=4096,
    num_attention_heads=64,
    max_sequence_length=1025,
    hidden_dropout=0.1,
    attention_dropout=0.1,
    checkpoint_activations=True,
    checkpoint_num_layers=1,
    sandwich_ln=False,
    model_parallel_size=1,
    world_size=1,
    rank=0
    )

init_method = 'tcp://'
master_ip = os.getenv('MASTER_ADDR', 'localhost')
master_port = os.getenv('MASTER_PORT', '6000')
init_method += master_ip + ':' + master_port
torch.distributed.init_process_group(
        backend='nccl',
        world_size=args.world_size, rank=args.rank,init_method=init_method)
import mpu
    # Set the model-parallel / data-parallel communicators.
mpu.initialize_model_parallel(args.model_parallel_size)
print('bg')
# %%
model = GLMModel(args)
# %%
old['module']['mixins.block_position_embedding.block_position_embeddings.weight'] = old['module']['transformer.block_position_embeddings.weight']
del old['module']['transformer.block_position_embeddings.weight']
# %%
missing_keys, unexpected_keys = model.load_state_dict(old['module'], strict=True)

# %%
import os
os.makedirs('pretrained/glm/glm-en-10b/250000', exist_ok=True)
torch.save(old, 'pretrained/glm/glm-en-10b/250000/mp_rank_00_model_states.pt')

# %%
