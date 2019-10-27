# scan2mail
> scan2mail – 100% organic, free-range scanner toolchain for lazy people

## Basic process

- Take a picture with the smartphone and upload it to Nextcloud
- Load images from Nextcloud folder to server
- Apply image rotation and strip metadata
- Convert images to TIFF and use deskewing, normalization etc.
- Convert TIFF to PDF
- Bundle PDFs according to timestamps
- Send out new PDFs via mail
- Update Nextcloud folder

## Installation

The following steps assume that you run a modern Linux-based distribution.

- Make sure you have docker installed.
- Copy `scan2mail-config.json.default` to `scan2mail-config.json` and change properties according to your environment.
- Run `docker-run.sh`

The latter script creates a lock file in the project folder. This is beneficial if you just want to put the call to the docker container into crontab.

## License 

This project is licensed under [GPLv3](LICENSE).

## To-Do

- [x] Add a loop-like procedure to make sure to load all new images from a batch

  - Not sure yet, how to do this best, but the current loop with sleep does a fair job, even though sleeps are generally a bad idea. Maybe the owncloud API has something.

- [x] Add appropriate logging to inspect the container while running

  - There is `docker logs`, so actually there is no need to do sth. genuine

- [x] Put convert step into separate folder
- [x] Refactor code after switching to python
- [x] Create a more robust packaging algorithm to determine related documents
- [x] Add multi-configuration/user support
- [x] Allow sending to different recipients
- [ ] Switch to an alpine-based docker image

