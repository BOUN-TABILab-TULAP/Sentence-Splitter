## How to run using Docker
1. Clone the repo
```bash
git clone https://github.com/BOUN-TABILab-TULAP/Sentence-Splitter.git
```
2. Launch a terminal in the root directory of the repo and build the Docker image where
- `-t` is the tag for the Docker image. You can provide any name you want
- `.` is the relative path to the Dockerfile 
```bash
docker build -t sentence-splitter .
```
3. Run the Docker image where
- `-d` indicates "detach", let the container run in the background
- `-p 5000:5000` indicates mapping port 5000 of the container to the port 5000 of the host.
```bash
docker run -d -p 5000:5000 sentence-splitter
```
4. Send a POST request
- via curl
    ```bash
    curl -X POST http://localhost:5000/evaluate 
   -H 'Content-Type: application/json' 
   -d '{"text":"Filmde kamburunu çıkarmış eski Yugoslav lideri, iki kişinin arasında elleri önden bağlı, cezaevi avlusunda yürüyor.Sabahları hiçbir şey yemeden içmeden, paldür küldür çıkıyorum evden"}'

   > {'sentences': ['Filmde kamburunu çıkarmış eski Yugoslav lideri, iki kişinin arasında elleri önden bağlı, cezaevi avlusunda yürüyor.', 'Sabahları hiçbir şey yemeden içmeden, paldür küldür çıkıyorum evden.']}
    ```
- via Python's requests library
    ```python
    import requests
    res = requests.post('http://localhost:5000/evaluate', json={'text':"Filmde kamburunu çıkarmış eski Yugoslav lideri, iki kişinin arasında elleri önden bağlı, cezaevi avlusunda yürüyor.Sabahları hiçbir şey yemeden içmeden, paldür küldür çıkıyorum evden."})
    print(res.json())

    > {'sentences': ['Filmde kamburunu çıkarmış eski Yugoslav lideri, iki kişinin arasında elleri önden bağlı, cezaevi avlusunda yürüyor.', 'Sabahları hiçbir şey yemeden içmeden, paldür küldür çıkıyorum evden.']}
    ```