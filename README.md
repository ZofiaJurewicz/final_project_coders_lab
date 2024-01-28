# Final Project: Work, World & Travel

## Application Description
The "Work, World & Travel" application is designed to assist in finding various types of jobs in different locations around the world. It serves not only as a job search tool but also as a platform focused on building new connections. The application not only enables users to browse job offers but also allows travelers to delegate tasks or find work in their current location, fostering a community where individuals can share skills and help each other.

## Opis Aplikacji
Aplikacja "Work, World & Travel" została stworzona w celu pomocy w znalezieniu różnorodnych ofert pracy w różnych miejscach na świecie. Jest nie tylko narzędziem do poszukiwania pracy, ale także platformą skupioną na budowaniu nowych relacji. Aplikacja umożliwia użytkownikom przeglądanie ofert pracy, a także podróżującym delegowanie zadań lub szukanie pracy w ich obecnej lokalizacji, wspierając społeczność, w której jednostki mogą dzielić się umiejętnościami i pomagać sobie nawzajem.

## Dependencies
Sample list:
- Django
- psycopg2-binary

## Zależności
Przykładowa lista:
- Django
- psycopg2-binary

## Migrations
After installing the application and configuring the Docker environment, connect to the database using the information in settings.py. Additionally, run the following commands to apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Migrations
Po zainstalowaniu aplikacji i skonfigurowaniu środowiska Docker, połącz się z bazą danych, korzystając z informacji zawartych w pliku settings.py. Dodatkowo, uruchom poniższe polecenia, aby zastosować migracje:

```bash
python manage.py makemigrations
python manage.py migrate
```
## Management Scripts
- **views.py:** Contains views handling various HTTP requests.
- **urls.py:** Defines URL routes for individual views.
- **models.py:** Contains the data models for the application.
- **forms.py:** Templates for application forms.
- HTML Files: 

## Skrypty Zarządzające
- **views.py:** Zawiera widoki obsługujące różne żądania HTTP.
- **urls.py:** Definiuje trasy URL dla poszczególnych widoków.
- **models.py:** Zawiera modele danych dla aplikacji.
- **forms.py:** Szablony formularzy aplikacyjnych.
- **HTML Files:** Szablony dla poszczególnych stron.

## Extensibility
There are plans to expand the application by adding a location-based API.

## Rozszerzalność
W planach jest rozbudowa aplikacji poprzez dodanie interfejsu API opartego na lokalizacji.


