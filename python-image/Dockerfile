FROM python

WORKDIR /app

COPY . /app/

RUN pip3 install -user fluigent_sdk -21.0.0.zip
RUN pip3 install -r requirements.txt

CMD ["python3", "app.py"]
# Need to add the commands to install 
# SLS
# SALEAE
# FLUIGENT
# the