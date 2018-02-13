# Unoconv-MAESC
A repo for building an Unoconv microservice Docker image

## Build

Build the image with `build.sh`. Pass in your hostname as an argument (i.e. HOSTNAME/unoconv)

## Running

You can run the image with the following command (replace HOST_PORT,HOST_DIR,HOST_NAME):

`docker run -itd -p HOST_PORT:80 -v HOST_DIR:/var/www/tmp HOST_NAME/unoconv`

## Usage

/upload/(.+) - send original files here

/service - this will run your unoconv conversion commands and respond with the converted file
```
{
  "cmd": array, the unoconv commands. Should include "INPUT" and "OUTPUT" as separate elements.
  "input": string, the file name to convert. It will be inserted into the "INPUT" location of your commands.
}
```
