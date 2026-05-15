import torch

print("=== PyTorch & CUDA Info ===")
print(f"PyTorch version:     {torch.__version__}")
print(f"CUDA available:      {torch.cuda.is_available()}")

if torch.cuda.is_available():
    print(f"CUDA version:        {torch.version.cuda}")
    print(f"GPU name:            {torch.cuda.get_device_name(0)}")
    print(f"GPU memory total:    {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
    print(f"GPU memory free:     {torch.cuda.mem_get_info(0)[0] / 1e9:.2f} GB")

    # Actual compute test
    print("\n=== Compute Test ===")
    x = torch.randn(1000, 1000).cuda()
    y = torch.randn(1000, 1000).cuda()
    z = x @ y
    print(f"Tensor device:       {z.device}")
    print("GPU compute test:    OK")
else:
    print("\nCUDA not available. Possible reasons:")
    print("  1. No NVIDIA GPU in this machine")
    print("  2. PyTorch installed WITHOUT CUDA support (most common)")
    print("  3. NVIDIA drivers not installed or outdated")
    print("\nCheck your PyTorch build:")
    print(f"  torch.__version__ = {torch.__version__}")
    print("  If it ends in +cpu, you need to reinstall PyTorch with CUDA support.")
    print("  Go to: https://pytorch.org/get-started/locally/")