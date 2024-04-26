import http.server
import urllib.parse
import socketserver
import os
import json
import random
import requests

# import base64
import base64

PORT = 8080
STUDENT_ID = "24012943"


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)

        if parsed_url.path == '/':
            if not self.authenticate():
                return
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            with open('templates/index.html', 'rb') as f:
                self.copyfile(f, self.wfile)

        elif parsed_url.path == '/form':
            if not self.authenticate():
                return
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('templates/psycho.html', 'rb') as f:
                self.copyfile(f, self.wfile)

        elif parsed_url.path == '/view/input':
            if not self.authenticate():
                return
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            with open('input_data.json', 'rb') as f:
                self.copyfile(f, self.wfile)

        elif parsed_url.path == '/view/profile':
            if not self.authenticate():
                return
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            with open('profile_data.json', 'rb') as f:
                self.copyfile(f, self.wfile)

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('templates/404.html', 'rb') as f:
                self.copyfile(f, self.wfile)

    def do_HEAD(self):
        self.do_GET()

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Psycho Profile\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def authenticate(self):
        auth_header = self.headers.get('Authorization')
        if auth_header is None or not auth_header.startswith('Basic '):
            self.do_AUTHHEAD()
            self.wfile.write(bytes('Unauthorized access.', 'utf-8'))
            return False
        auth_decoded = base64.b64decode(
            auth_header.split()[1]).decode('utf-8').split(':')
        username = auth_decoded[0]
        password = auth_decoded[1]
        if username == STUDENT_ID and password == STUDENT_ID:
            return True
        else:
            self.do_AUTHHEAD()
            self.wfile.write(bytes('Unauthorized access.', 'utf-8'))
            return False

    def do_POST(self):
        if self.path == '/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_data = post_data.decode('utf-8')
            credentials = post_data.split('&')
            username = credentials[0].split('=')[1]
            password = credentials[1].split('=')[1]

            if username == STUDENT_ID and password == STUDENT_ID:
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(bytes("Login successful!", 'utf-8'))
            else:
                self.do_AUTHHEAD()
                self.wfile.write(bytes('Unauthorized access.', 'utf-8'))

        elif self.path == '/analysis':
            if not self.authenticate():
                return
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            parsed_data = urllib.parse.parse_qs(post_data.decode('utf-8'))
            # Parse and store form data
            profile_data = self.parse_form_data(parsed_data)
            # Analyze data and generate psychological profile
            psychological_profile = self.analyze_data(profile_data)

            # delete if there are any exisiting images
            imgs = ['dog_image.jpg', 'cat_image.jpg', 'duck_image.jpg']
            for img in imgs:
                if os.path.exists(img):
                    os.remove(img)

            # Store profile data and images at server side
            for pet in profile_data['pets']:
                if pet == 'dog':
                    dog_image_url = "https://dog.ceo/api/breeds/image/random"
                    response = requests.get(dog_image_url)
                    dog_image_url = response.json()['message']
                    self.fetch_and_store_image(dog_image_url, 'dog_image.jpg')
                    profile_data['pets'] += [dog_image_url]
                elif pet == 'cat':
                    cat_image_url = "https://api.thecatapi.com/v1/images/search"
                    response = requests.get(cat_image_url)
                    cat_image_url = response.json()[0]['url']
                    profile_data['pets'] += [cat_image_url]
                    self.fetch_and_store_image(cat_image_url, 'cat_image.jpg')
                elif pet == 'duck':
                    duck_image_url = "https://random-d.uk/api/v2/random"
                    response = requests.get(duck_image_url)
                    duck_image_url = response.json()['url']
                    self.fetch_and_store_image(
                        duck_image_url, 'duck_image.jpg')
                    profile_data['pets'] += [duck_image_url]

            # remove dogs, cats and ducks from pets
            profile_data['pets'] = [pet for pet in profile_data['pets']
                                    if pet != 'dog' and pet != 'cat' and pet != 'duck']
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(bytes(
                "Analysis complete. Psychological profile data and images stored at server side.", 'utf-8'))

            # serialize the psychological profile to be used in /view/profile store on the server in a properly serialized format (json)
            with open('profile_data.json', 'w') as f:
                json.dump(psychological_profile, f, indent=4)

            # serialize the psychological profile to be used in /view/input store on the server in a properly serialized format (json)
            with open('input_data.json', 'w') as f:
                json.dump(profile_data, f, indent=4)

        else:
            self.send_error(404, 'Not Found')

    def parse_form_data(self, data):
        profile_data = {}
        profile_data['name'] = data.get('name', [''])[0]
        profile_data['gender'] = data.get('gender', [''])[0]
        profile_data['birthyear'] = data.get('birthyear', [''])[0]
        profile_data['birthplace'] = data.get('birthplace', [''])[0]
        profile_data['residence'] = data.get('residence', [''])[0]
        profile_data['job'] = data.get('job', [''])[0]
        profile_data['pets'] = data.get('pets', [])
        profile_data['message'] = data.get('message', [''])[0]

        # handle the logic for all the radio buttons
        for key, value in data.items():
            if key.startswith("question["):
                question_id = int(key.split("[")[1][:-1])
                profile_data[question_id] = int(value[0])

        return profile_data

    def analyze_data(self, data):
        psychological_profile = {}

        print(data)
        # Calculate the total score based on user responses
        total_score = sum([int(data[i]) for i in range(1, 21)])
        print(total_score)
        # Determine career assessment based on the total score
        if total_score <= 40:
            career_susceptibility = 'low'
        elif total_score <= 70:
            career_susceptibility = 'mid'
        else:
            career_susceptibility = 'high'

        print(career_susceptibility)
        # Add career assessment to the psychological profile
        psychological_profile['career_susceptibility'] = career_susceptibility

        movie_recommendation = self.fetch_movie_recommendation()
        psychological_profile['movie_recommendation'] = movie_recommendation

        return psychological_profile

    def fetch_movie_recommendation(self):
        # Placeholder logic to fetch movie recommendation from a third-party API
        # Here's an example using a mock recommendation
        mock_recommendations = [
            "The Shawshank Redemption",
            "Inception",
            "The Dark Knight",
            "Pulp Fiction",
            "The Godfather",
            "Fight Club",
            "Forrest Gump",
            "The Matrix",
            "Goodfellas",
            "The Silence of the Lambs",
            "The Avengers",
            "Interstellar",
            "The Lion King",
            "The Departed",
            "Gladiator",
            "The Green Mile",
            "The Prestige",
            "The Usual Suspects"
        ]
        return random.choice(mock_recommendations)

    def fetch_and_store_image(self, url, filename):
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)


handler = MyHttpRequestHandler

with socketserver.TCPServer(("", PORT), handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
