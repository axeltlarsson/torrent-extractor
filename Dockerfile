FROM python:3-onbuild

ENTRYPOINT ["python", "./run_torrent_extractor.py"]

CMD ["-h"]
