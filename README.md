# Nanos Machine Learning Task

This app takes the  url of webpage like: https://www.nanos.ai/ and also a list of products and extracts the most relevant words from the webpage to
the given list of products/services.


## Installation

Have Docker and Git installed in your machine.

Clone this repository by running

```bash
git clone https://github.com/NickDee96/nanos-mltest.git
```

Change directory in terminal  to the repo's folder

Build the docker image by running : 

```bash
docker build -t <YOUR IMAGE NAME> .
```

Run the image by:

```bash
docker run -p 8050:8050 -t <YOUR IMAGE NAME>
```

## Usage

Logon on to your browser at `127.0.0.1:8050` and access the webapp

You can find the approach to the task [here](https://github.com/NickDee96/nanos-mltest/blob/master/Nanos%20Machine%20Learning%20Task%20Approach_2.pdf)