import time
import cv2
import numpy as np
import torch
from torchvision.transforms import transforms
from resmasking import resmasking_dropout1

transform = transforms.Compose([transforms.ToPILImage(), transforms.ToTensor()])


FER_2013_EMO_DICT = {
    0: "angry",
    1: "disgust",
    2: "fear",
    3: "happy",
    4: "sad",
    5: "surprise",
    6: "neutral",
}

state = torch.load(
    "./checkpoints/Z_resmasking_dropout1_rot30_2019Nov30_13.32"
)

model = resmasking_dropout1()
model.cuda()

model.load_state_dict(state["net"])
model.eval()

def ensure_color(image):
    if len(image.shape) == 2:
        return np.dstack([image] * 3)
    elif image.shape[2] == 1:
        return np.dstack([image] * 3)
    return image

def ensure_size(image):
    if image.shape[0] != 224 or image.shape[1] != 224:
        return cv2.resize(image, (224, 224))
    return image

def recognize_face(face):
    with torch.no_grad():
        face = ensure_color(face)
        face = ensure_size(face)
        face = transform(face).cuda()
        face = torch.unsqueeze(face, dim=0)

        start = time.time()
        out = model(face)
        end = time.time()
        print(f"Time to recognize emotion: {(end - start)*1000} ms")

        output = torch.squeeze(out, 0)
        proba = torch.softmax(output, 0)

        emo_proba, emo_idx = torch.max(proba, dim=0)
        emo_idx = emo_idx.item()
        emo_proba = emo_proba.item()

        emo_label = FER_2013_EMO_DICT[emo_idx]

        return emo_proba, emo_label

