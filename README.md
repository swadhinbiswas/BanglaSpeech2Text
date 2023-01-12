# Bangla Speech to Text
BanglaSpeech2Text: An open-source offline speech-to-text package for Bangla language. Fine-tuned on the latest whisper speech to text model for optimal performance. Transcribe speech to text, convert voice to text and perform speech recognition in python with ease, even without internet connection.

## Installation
```bash
pip install banglaspeech2text
```

## Models
| Model | Size | Best(WER) |
| --- | --- | --- |
| 'tiny' | 100-200 MB | N/A |
| 'base' | 200-300 MB | 46 |
| 'small' | 900-1000 MB | 18 |

__NOTE__: "Bigger model have better accuracy but slower inference speed. Smaller wer is better."
__NOTE__: You can view the models from [here](https://github.com/shhossain/whisper_bangla_models)


## Usage

### Download a model
```python
from banglaspeech2text import Model, available_models

# Download a model
models = available_models()
print(models) # see the available models by diffrent people and diffrent sizes

model = models[0] # select a model
model.download() # download the model
```
### Use with file
```python
from banglaspeech2text import Model, available_models

# Load a model
models = available_models()
model = models[0] # select a model
model = Model(model) # load the model
model.load()

# Use with file
file_name = 'test.wav'
output = model.recognize(file_name)

print(output) # output will be a dict containing text
print(output['text'])
```

### Use with SpeechRecognition
```python
import speech_recognition as sr
from banglaspeech2text import Model, available_models

# Load a model
models = available_models()
model = models[0] # select a model
model = Model(model) # load the model
model.load()


r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)
    output = model.recognize(audio)

print(output) # output will be a dict containing text
print(output['text'])
```

### Use GPU
```python
import speech_recognition as sr
from banglaspeech2text import Model, available_models

# Load a model
models = available_models()
model = models[0] # select a model
model = Model(model,device="gpu") # load the model
model.load()


r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)
    output = model.recognize(audio)

print(output) # output will be a dict containing text
print(output['text'])
```
__NOTE__: This package uses torch as backend. So, you can use any device supported by torch. For more information, see [here](https://pytorch.org/docs/stable/tensor_attributes.html#torch.torch.device). But you need to setup torch for gpu first from [here](https://pytorch.org/get-started/locally/).


### Some Methods
```python
from banglaspeech2text import Model, available_models

models = available_models()
print(models[0]) # get first model
print(models['base']) # get base models
print(models['whisper_base_bn_sifat']) # get model by name

# set download path
model = Model(model,download_path=r"F:\Code\Python\BanglaSpeech2Text\models")
model.load()

# directly load a model
model = Model('base')
model.load()


