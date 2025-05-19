import kagglehub

# Download latest version
path = kagglehub.dataset_download("neelghoshal/therapist-patient-conversation-dataset")

print("Path to dataset files:", path)