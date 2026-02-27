# Hugging Face Spaces Deployment Guide

## Quick Start

### Option 1: Docker Deployment (Recommended)

1. **Create a new Space on Hugging Face:**
   - Go to https://huggingface.co/spaces
   - Click "Create new Space"
   - Choose a name (e.g., `ticket-classifier`)
   - Select **Docker** as the space type
   - Choose **Docker** as the runtime

2. **Upload files to your Space:**
   
   Required files to upload:
   ```
   Dockerfile          (root level)
   api/main.py
   api/__init__.py
   frontend/index.html
   models/model (2).pkl  (or your model file)
   requirements.txt
   ```

3. **File Structure on HF Spaces:**
   ```
   Dockerfile
   requirements.txt
   api/
     __init__.py
     main.py
   frontend/
     index.html
   models/
     model (2).pkl
   ```

4. **Update requirements.txt** if needed to ensure all dependencies are included:
   ```
   fastapi==0.95.2
   uvicorn==0.22.0
   joblib
   mlflow
   pandas
   scikit-learn
   ```

### Option 2: Using Git (Recommended for Version Control)

1. Initialize a git repo:
   ```bash
   git init
   ```

2. Add HF Spaces as a remote:
   ```bash
   git remote add spaces https://huggingface.co/spaces/<your-username>/<space-name>
   ```

3. Commit and push:
   ```bash
   git add .
   git commit -m "Initial deployment"
   git push spaces main
   ```

## Configuration

### Port
- The Dockerfile exposes port **7860** (Hugging Face Spaces default)
- The app is configured to run on `0.0.0.0:7860`

### Model Path
- The app expects the model at: `models/model (2).pkl`
- Make sure this file is included when uploading to HF Spaces

### Frontend
- The frontend (`index.html`) is served from the root `/` endpoint
- Static files are served from `/static`

## API Endpoints

Once deployed, you'll have:

- **Frontend:** `https://<your-hf-username>-<space-name>.hf.space/`
- **API Docs:** `https://<your-hf-username>-<space-name>.hf.space/docs`
- **Prediction:** `POST https://<your-hf-username>-<space-name>.hf.space/predict`

## Testing Locally Before Deployment

Build and run locally:

```bash
docker build -t ticket-classifier .
docker run -p 8000:7860 ticket-classifier
```

Then visit: `http://localhost:8000`

## Troubleshooting

- **Model not found:** Ensure `models/model (2).pkl` is uploaded
- **Port issues:** HF Spaces always uses port 7860; the Dockerfile handles this
- **Missing dependencies:** Check `requirements.txt` includes all imports from `api/main.py`
- **Frontend not loading:** Verify `frontend/index.html` is in the correct path

## Full Project Structure

```
your-project/
├── Dockerfile
├── requirements.txt
├── api/
│   ├── __init__.py
│   └── main.py
├── frontend/
│   └── index.html
└── models/
    └── model (2).pkl
```

## Next Steps

1. Create a Space: https://huggingface.co/spaces
2. Upload the files or use git
3. HF will automatically build the Docker image
4. Your space will be live in ~2-5 minutes
5. Share the URL!
