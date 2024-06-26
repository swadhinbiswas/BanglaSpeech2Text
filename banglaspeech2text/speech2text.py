from typing import Optional, Union
from banglaspeech2text.utils import app_name, logger, get_app_path
from banglaspeech2text.utils.extras import get_hash, ShortTermMemory
from banglaspeech2text.utils.download_models import ModelType, get_model, available_models, ModelDict
import os
# import torch
from speech_recognition import AudioData
from uuid import uuid4
from threading import Thread
from transformers import pipeline
from banglaspeech2text.utils.install_packages import check_git_exists
import subprocess
import warnings
warnings.filterwarnings("ignore")

def initialize_git_lfs():
    if not check_git_exists():
        raise ValueError("Git is not installed. Please install Git and try again")
    
    cmd = "git lfs install"
    try:
        subprocess.check_output(cmd, shell=True)
    except:
        pass
    


class Model:
    def __init__(self, model: Union[str, ModelType, ModelDict] = ModelType.base, cache_path=None, device: Optional[Union[int, str, "torch.device"]] = None, force=False, verbose=True, **kwargs):  # type: ignore
        """
        Args:
            model_name_or_type (str or ModelType): Model name or type 
            download_path (str): Path to download model (default: home directory)
            device (str): Device to use for inference (cpu, cuda, cuda:0, cuda:1, etc.)
            force (bool): Force download model
            verbose (bool): Verbose mode

        **kwargs are passed to transformers.pipeline
        See more at https://huggingface.co/transformers/main_classes/pipelines.html#transformers.pipeline
        """

        if verbose:
            logger.setLevel("INFO")
        else:
            logger.setLevel("ERROR")

        initialize_git_lfs()
        
        if cache_path is not None:
            if not os.path.exists(cache_path):
                raise ValueError(f"{cache_path} does not exist")
            os.environ[app_name] = cache_path

        self.model: ModelDict = None  # type: ignore
        if isinstance(model, ModelDict):
            self.model = model
        else:
            self.model = get_model(model, force=force)

        self.device = device
        self.kwargs = kwargs

        self.task = "automatic-speech-recognition"
        self.pipe = None
        
        self.from_audio_data = False
        
        self.cache_file = True
        
        if self.cache_file:
            self.cache = ShortTermMemory(20)

    def load(self):
        logger.info("Loading model")
        if not self.model.is_downloaded():
            self.model.download()

        self.pipe = pipeline(self.task, model=self.model.path,device=self.device, **self.kwargs)  # type: ignore

    @property
    def available_models(self):
        return available_models()

    def __get_wav_from_audiodata(self, data: AudioData):
        temp_audio_file = f"{uuid4()}.wav"
        path = os.path.join(get_app_path(app_name), temp_audio_file)

        with open(path, "wb") as f:
            f.write(data.get_wav_data())

        return path

    def transcribe(self, audio_file) -> dict:
        hash = None
        if self.cache_file:
            hash = get_hash(audio_file)
            hash = f"{self.model.name}_{hash}"
            if hash in self.cache:
                return self.cache[hash] # type: ignore
        
        data: dict = self.pipe(audio_file)  # type: ignore
        if self.from_audio_data:
            Thread(target=os.remove, args=(audio_file,)).start()
            self.from_audio_data = False
        
        if self.cache_file:
            self.cache[hash] = data # type: ignore
        return data

    def recognize(self, audio) -> dict:
        if isinstance(audio, AudioData):
            audio = self.__get_wav_from_audiodata(audio)
            self.from_audio_data = True
        return self.transcribe(audio)  # type: ignore

    def __call__(self, audio) -> dict:
        return self.recognize(audio)

    def __repr__(self):
        return f"Model(name={self.model.name}, type={self.model.type})"

    def __str__(self):
        return self.__repr__()


__all__ = [
    "Model",
    "available_models",
    "ModelType",
]

if __name__ == "__main__":
    model = Model()
    model.load()
    print(model.available_models)
    print(model)

    # audio_file = "data/audios/0.wav"
