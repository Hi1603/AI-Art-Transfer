**On the SERVER-SIDE for backend:**



---Extract the files and folders from AI Project server-side.zip file



---Open a terminal and run the following commands



**Install Python and Conda**



conda create -n ai-server-env python=3.11

conda activate ai-server-env



**Install the packages**



pip install -r requirements.txt



**Install ngrok**



wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip

unzip ngrok-stable-linux-amd64.zip

sudo mv ngrok /usr/local/bin







---OR if you can’t use sudo, just run ngrok from your project folder.



---Sign up at ngrok.com to get your auth token

&nbsp;

---after signing up do the following 







ngrok config add-authtoken <YOUR\_AUTHTOKEN>







**Start your ngrok tunnel**



---open a new terminal and run:

ngrok http 5001





---once you see the URL been published run the following command



python remote\_server.py







**VIOLA! you have the backend set up running make sure to use the terminal in the directory where you have the files for the backend. Now let us move on to the frontend**





**For the FRONTEND**

Extract the front files from AI\_Project\_frontend.zip


---in a new terminal



pip install -r requirements.txt





---after that paste the link you have copied from ngrok terminal in the app.py file



---there you go now you can run the frontend





python app.py







