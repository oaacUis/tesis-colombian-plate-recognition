import torch

print("Torch cuda version: ", torch.version.cuda), print()

if torch.cuda.is_available():
    print("CUDA is available. Device count:", torch.cuda.device_count()), print()
    print("CUDA device name:", torch.cuda.get_device_name(0))
else:
    print("CUDA is not available.")
