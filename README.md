# Audiovisual User Experience for Music Streaming Platforms
Capstone project for Rochester Institute of Technology Master's Program


### Project Description Abstract:

The current music industry has already made its massive move to online streaming
platforms which now dominate the online audio space. Within its move, the online streaming
field now also encapsulates other content such as talk shows and music videos, showing the
industry’s interest and evolution to investing into a more audio-visual space. This Capstone
Project will utilize AI technology to address the current lack of visual content on popular streaming platforms coupling
its audio content that will help push them closer to the audiovisual space that the online music
streaming industry is moving towards in the future. The completion of the project will involve
my working to research, collect data, and develop a product from January to April 2025. This
project will result in a working software product that will demonstrate the technology that could
be used to provide more visual content to music streaming platforms, along with a project report
and documentation that will give insight into the project development as well as data on whether
the product will enhance the overall user experience of popular streaming platforms. The project
aims to enhance the user’s enjoyment of music through popular streaming platforms and be a
contribution in the evolution of the online music industry.


### Run Instructions (Developed on MacOS): <br/>
-Install requirements : `pip install -r requirements.txt` <br/>
-Pull and run ollama model gemma3:4b : `ollama run gemma3:4b` (If using a different model, change `model` parameter in AudioVisualizer.py to the model name) <br/>
-Download Stable Diffusion model ([Stable Diffusion 1.5-pruned-emaonly](https://huggingface.co/stable-diffusion-v1-5/stable-diffusion-v1-5) was used in development). <br/>
-Install [AUTOMATIC1111 Stable Diffusion WebUI](https://github.com/AUTOMATIC1111/stable-diffusion-webui). <br/>
-Run Stable Diffusion WebUI as an API using terminal `./webui.sh --api` on Mac, or `/webui.sh --api` on Linux. <br/>
-Run program within preferred IDE (this project used PyCharm), or in terminal with `python AudioVisualizer.py`, along with both Ollama and Stable Diffusion models running at the same time<br/>

### Screenshots <br/>

Starting screen: <br/>
<img width="1280" alt="Program GUI on loadup" src="https://github.com/user-attachments/assets/2a9b60e3-b2fd-482a-b5e6-091efe665095" /> <br/>

Running: <br/>
<img width="1267" alt="Screenshot 2025-04-27 at 6 58 36 PM" src="https://github.com/user-attachments/assets/fb8fdd09-7e2d-4fda-8e31-7f27823613b5" /> <br/>

### Credit <br/>

AUTOMATIC1111 WebUI
Stable Diffusion
Ollama
Gemma 3

