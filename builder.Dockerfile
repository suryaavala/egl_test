FROM python:3.9.10

RUN pip install --upgrade pip

# Install gcloud cli
COPY assests/google-cloud-sdk-373.0.0-linux-x86_64.tar.gz google-cloud-sdk-373.0.0-linux-x86_64.tar.gz
RUN tar xvf google-cloud-sdk-373.0.0-linux-x86_64.tar.gz &&\
    ./google-cloud-sdk/install.sh --usage-reporting false --path-update true --bash-completion false --rc-path false --quiet &&\
    rm -rf google-cloud-sdk-373.0.0-linux-x86_64.tar.gz google-cloud-sdk-371.0.0-linux-x86_64 &&\
    ln -s /google-cloud-sdk/bin/* /usr/local/bin/

WORKDIR /app

COPY Makefile /app/Makefile

COPY Pipfile Pipfile.lock /app/

RUN make install-pipenv &&\
    make install-py-dev-as-sys &&\
    rm -rf /app/*
