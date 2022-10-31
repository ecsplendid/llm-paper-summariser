## GPT-3 PDF paper summariser tool

This is a tool to summarise PDF papers using OpenAI's GPT-3 API. It is a work in progress.

It is a python function and also a REST / POST service that can be deployed on a server.

It will download a PDF paper from a URL, extract the text, summarise it using GPT-3 and return the summary.

The summarisation is can be thought of a DAG of computation i.e. it will;

* Download the PDF
* Segment the PDF into chunks
* Clean each chunk with a prompt
* Then summarise each chunk with a prompt
* Then summarise and combine adjacent chunks recursively until the summary is complete
* It will then compute an expert bullet point summary using the summary, and a high level structure of the paper

It's a little bit slow, as it will be making many calls to GPT-3. A typical paper, say 8 pages long will take about 130 seconds to summarise.

### How to use with docker

Create file `~/openai.env` with the following content:

```
OAI1="sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
OAI2="sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
OAI3="sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
OAI4="sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
OAI5="sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
```

We use all of your 5 OpenAI keys so we can get maximum parallelism. Currently there is no support for fewer keys.

OpenAI only allows 2 concurrent requests per key, so we use 5 keys to get 10 concurrent requests (in theory). Apparently OpenAI didn't have scalability in mind when they designed their API infra.

Run these commands to get it running on your machine

```
docker build -t doc-summariser . 
docker run -dp 80:5000 --env-file ~/openai.env -it doc-summariser
```

## Usage

Now that the docker container is running, goto your local browser and type `localhost` in the address bar. You should see a web page with a text box and a submit button.

This will return you back the summary in HTML format (that's what the checkbox is for).

You can alternatively use the REST API to get the summary. The REST API is a POST request to `localhost/pdf2txt` with the `url="..."` i.e. pointing to a URL of a PDF paper.

```
{
    "url": "https://arxiv.org/pdf/2005.14165.pdf",
    "html": true
}
```

## Hosting on ACI (Azure container services)

If you are building on MacOS with M1, you will need to use the `--platform linux/amd64` flag when building the docker image.

You will need to push the image to the docker hub, and then create an ACI instance with the image.

```
docker login
docker buildx build --push --tag timscarfe/doc-summariser:latest-amd64 --platform=linux/amd64 .
```

Check the deployment script for ACI in `./deploy.yml`. You might want to tweak some things in there i.e. 

- The env variables so that they container your OpenAI keys.
- The server location
- The service name and FQDN

Deploy the server onto ACI with this command (ensure you have `az` shell installed);

```
az login
az container create -g rg-intelligence-service --file ./deploy.yml
```

## Local development

To run the code locally, you will need to install the dependencies. 

This program needs `wget` to be on your path. On Ubuntu, you can install it with `sudo apt install wget`.

Then install the python dependencies with `pip install -r requirements.txt`.

There is currently no CLI interface for the programme.

## License (MIT)

You can use this code for any purpose, commercial or otherwise. You can modify it, redistribute it, etc. You can even sell it. You can't hold me liable for anything. If you do use it, I'd appreciate a shout out. If you have any questions, feel free to contact me. If you find any bugs, please let me know. 

Copyright (c) 2022 Tim Scarfe
