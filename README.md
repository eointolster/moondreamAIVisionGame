You are going to want to do go here first
    https://github.com/vikhyat/moondream
by git clone https://github.com/vikhyat/moondream

Then this, you will have to wait awhile
      pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu121

then this but inside of there are also torch and torchvision, we dont need them as we downloaded the better ones above for gpu
  You can do this first and maybe it is recommended, ill tell you why in a sec
      pip install -r requirements.txt

So once that is done you will want to do something like this 
    python sample.py --image "D:\moondream1Test\moondream\assets\background7.jpg" --prompt "describe this picture"

give the directory of your image. This will initiate the download for the model so you do not have to worry.

-------------------------------------------------------------------------------------------------------------------------------

copy the files in this github into the folder as shown in the image attached below
![image](https://github.com/eointolster/moondreamAIVisionGame/assets/64816111/b777348b-8b66-40e9-ba2e-71ebf29534c4)
next you will 
  python app.py
it will load the index.html in the templates folder
use the main.js in the static folder
and the images in the static\images\ folder
127.0.0.1:5000
That should all work for you. At least I hope so :)
