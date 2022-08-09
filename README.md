# Smile [AI]ndex

- Author: Emanuel Mariano Ravera

## Endpoint

You should get your own keys at Microsoft for cognitive API and replace then on API_KEY constant.

```
https://eastus.api.cognitive.microsoft.com/face/v1.0

```

# Installation

To install the software need to run

```bash
pip install -r requirements.txt

```

# Smile index single command

If you want to execute the program in one liner you can do the following.

```bash
python smile-index.py --analyze --path <ROOT>/test-data/videos/
```

Is recommended to use the Full path of the videos.

# Report

If is needed to generate the global report need to execute:

```bash
python smile-index.py --report --path <ROOT>/test-data/videos/
```

Is recommended to use the Full path of the videos.

### Execution of each step

The process has several steps we need to execute:

1. Process the video to get the frames. We need to use the video_frame script.

```bash
python video_frame.py --input <video_path> --out <frames_path>
```

2. Process and filter the images that contains a face on it.

```bash
python face_detector.py --raw <frames_path> --filtered <frame_faces_path>
```

3. Analize the face from the pictures and generates the csv as output

```bash
python analyze-face-from-pictures.py --path <frame_faces_path> --header <True|False> >> report.csv
```

The process is similar to a chain, one after the other.

