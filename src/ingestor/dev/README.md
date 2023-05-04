# Ingestor to receive telemetry from runelite clients

## Helper during dev

```sh
sudo docker rm -f ingestortest; sudo docker build . -t ingestortest && sudo docker run --rm -d -p 8000:8000 --name ingestortest ingestortest
```
