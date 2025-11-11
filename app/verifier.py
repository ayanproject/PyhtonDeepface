from deepface import DeepFace

def verify_faces_by_path(probe_path: str, stored_path: str, model_name: str, distance_metric: str):
    """
    Calls DeepFace.verify with file paths. Returns the raw result dict from DeepFace.
    """
    result = DeepFace.verify(
        img1_path=probe_path,
        img2_path=stored_path,
        model_name=model_name,
        distance_metric=distance_metric,
        enforce_detection=True
    )
    return result
