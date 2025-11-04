# DataSoluTech: Conteneurisation via Docker d'une BDD MongoDB et son script import Python

Ce projet automatise la **migration d’un dataset CSV vers MongoDB**. Ce dernier inclue des tests pytest automatique afin de vérifier l'import des données.
Le tout est conteneurisé grâce à **Docker** pour garantir la portabilité et la scalabilité.

## Contexte de la mission

Nous venons de recevoir un dataset de données médicales de patients d'un de nos clients. Ils commencent à avoir des soucis de scalabilité avec leurs tâches quotidiennes et ont besoin de notre aide.

Pour les aider à mieux gérer leurs données, nous leur avons proposé une solution Big Data scalable horizontalement.

## Sources de Données
Le monde médical est un monde où les données sont soumises à des réglementations sur la confidentialité (RGPD, secret médical), ce qui rend leur accès difficle à des fins d'apprentissage. Afin de s'affranchir de ce problème, ce dataset a été généré pour reproduire la structure et les attributs généralement présents dans les dossiers médicaux. 
Ces données sont au format csv: healthcare_data.csv
Ce csv contient 55500 lignes et 15 colonnes. 

## Structure du Projet

```
.
├── mongo-init  
├──────── init-bdd.js                   # Création des rôles et utilisateurs de la BDD

├── script_import                       
├──────── data
├────────────── hcare_dataset_test.csv  # CSV créé avec seulement 5 lignes et 3 colonnes pour le développement
├────────────── healthcare_dataset.csv  # CSV source des données
├──────── src
├────────────── csv_info.py             # Fonctions sur le CSV utilisées dans le test pytest
├────────────── db_info.py              # Fonctions sur la BDD utilisées dans le test pytest
├────────────── script_import_fct.py    # Fonctions utilisées dans le script d'insertion du CSV dans la bDD
├──────── tests
├────────────── test_insert_script.py   # Contient les tests de validation
├──────── Dockerfile                    # Définition de l'image: script_import dans Docker
├──────── pytest.ini                    # Configure pytest
├──────── requirements.txt              # Liste des dépendances Python à installer dans le conteneur
├──────── script_import.py              # Script python d'import du csv dans mongoDB

├── docker-compose.yml                  # Docker Compose: Connecte les différentes images nécessaires (script_import + mongoDB)
├── poetry.lock                         # Généré automatiquement par poetry
├── pyproject.toml                      # Indique ce qu'il faut installer pour faire tourner le code (hors conteneur)
└── README.md                           # Read me
```
## Schéma JSON de la BDD mongoDB

{
  "Name": str
  "Age": int
  "Gender": str
  "Blood_Type": str
  "Insurance_Provider": str
  "Admission": {
    "Date_of_Admission": date
    "Discharge_Date": date
    "Admission_Type": str
    "Hospital":str
    "Room_Number": str
    "Doctor": str
    "Billing_Amount": float
  },
  "Diagnostic": {
    "Medical_Condition": str
    "Medication": str
    "Test_Results": str
  }
}

## Logique de migration / Tests - Python

La migration fonctionne comme suit: 
1- Connection à MongoDB
    1.1- Lecture des variables d'environnement pour construire l'**URI MONGO DB**
    1.2- Tentative de connexion répétées dans le temps (afin d'attendre que la bdd dans le conteneur mongodb est opérationnelle)
2- Lecture du csv et création d'un dataframe grâce à **Pandas**
3- Création de la bdd 'hcare_db' et collection 'traitement'
4- Création des documents à partir de chaque lignes du csv (en suivant le **schéma JSON décrit ci-dessus**) 
5- Insertion de l'ensemble des documents
6- Tests pytest sont lancés automatiquement dans le conteneur script_import
    6.1- Vérification du nombre de ligne entre le CSV et le nomdre de documents dans la collection
    6.2- Vérification des noms des champs de la collection: {'_id', 'Name', 'Age', 'Gender', 'Blood_Type', 'Insurance_Provider', 'Admission', 'Diagnostic'}
    6.3- Vérification des valeurs dans le champs Admission.Admission_Type: ['Elective','Emergency','Urgent']
    6.4- Vérification de l'âge (positif, et inférieur à 120)

Ces tests ont été choisis en mettant en place différentes approches de lecture de la bdd. De nombreux tests supplémentaires peuvent être mis en place.

## Conteneurisation par Docker
Le Dockerfile décrit comment créer l'image script_import, celui qui contient les CSV et le code d'insertion Python.
Dans ce fichier, nous demandons l'installation des différentes librairies nécessaires, et l'éxécution du script, et des tests pytest.

Le Docker Compose décrit le lancement du docker script_import et celui de mongodb qui provient de l'image (mongodb/mongodb-community-server:latest).
Il décrit un volume qui va garder les données MongoDB et le réseau de communication entre les deux conteneurs.

## Rôles/Utilisateurs créés
Le script init-bdd.js défini les rôles et les utilisateurs créés pour la gestion de base de données MongoDB.
Nous devons démarrer sur la base **admin** afin de décrire les trois rôles créés:
    - reader 
    - writer 
    - admin 

Le **reader** accède seulement en lecture à la bdd **hcare_db**.
Le **writer** accède en lecture, écriture à la bdd **hcare_db**.
L' **admin** accède en lecture, écriture à la bdd **hcare_db**, il gère également les rôles et utilisateurs de mongoDB.

## Utilisation du module

### Prérequis
- Python 3.9+ installé
- Docker installé

### Build de l'image / Création du réseau, volume et des deux conteneurs
Dans un terminal ouvert dans le dossier 1_Code

```bash
# Create the different images, volumes, networks and run the two containers:
docker-compose up -- build
```
Vous devriez avoir de nombreux logs correspondant à MongoDB. Regardons-ce concernant le script_import_csv, vous devriez avoir:

```bash
script_import_csv  | Connexion à Mongo réussie !
script_import_csv  | CSV file has 55500 rows.
script_import_csv  | 55500 documents insérés dans la collection 'patients'

script_import_csv  | tests/test_insert_script.py ....
script_import_csv  | 
script_import_csv  | ============================== 4 passed in 0.59s ===============================
```

Nous avons donc bien insérés les 55500 documents dans la collection et les 4 tests ont étés concluants.

### Connexion à la Base de données MongoDB via Mongosh
Dans un autre terminal, nous pouvons nous connecter à cette bdd mongoDB.

```bash
docker exec -it mongodb mongosh -u readerUser -p readerPassword --authenticationDatabase hcare_db
```
 Dans Mongosh, nous pouvons faire les actions suivantes:
```bash
test> show dbs #ne montre que la bdd hcare_db
```

```bash
test> use hcare_db #connection à la bdd hcare_db 
hcare_db> db.traitement.find() #rechercher les documents dans la collection 'traitement'
```
Nous voyons ici les 20 premiers documents.

Essayons d'insérer un nouveau document: 

```bash
hcare_db> db.traitement.insertOne({
    Name: "Thomas", 
    Age: 30, Gender: "Male",  
    Blood_Type: "B+",
    Insurance_Provider: "Cigna",  
    Admission: {
        Date_of_Admission: ISODate("2025-11-01T00:00:00Z"),
        Discharge_Date: ISODate("2025-11-03T00:00:00Z"),
        Admission_Type: "Emergency",
        Hospital: "Hammond Ltd",
        Room_Number: 301,
        Doctor: "Denise Galloway",
        Billing_Amount: 2000.00
        },
    Diagnostic: {
        Medical_Condition: "Asthma",
        Medication: "Penicillin",
        Test_Results: "Normal"
        }
    }) 
```

Vous devriez avoir le message suivant: 
```bash
MongoServerError[Unauthorized]: not authorized on hcare_db to execute command { insert: "traitement", documents: etc..
```

En revance, repartons de zéro et connectons-nous avec les crédentials suivants:
```bash
docker exec -it mongodb mongosh -u readerUser -p readerPassword --authenticationDatabase hcare_db
test> use hcare_db #connection à la bdd hcare_db 
hcare_db> db.traitement.insertOne({
    Name: "Thomas", 
    Age: 30, Gender: "Male",  
    Blood_Type: "B+",
    Insurance_Provider: "Cigna",  
    Admission: {
        Date_of_Admission: ISODate("2025-11-01T00:00:00Z"),
        Discharge_Date: ISODate("2025-11-03T00:00:00Z"),
        Admission_Type: "Emergency",
        Hospital: "Hammond Ltd",
        Room_Number: 301,
        Doctor: "Denise Galloway",
        Billing_Amount: 2000.00
        },
    Diagnostic: {
        Medical_Condition: "Asthma",
        Medication: "Penicillin",
        Test_Results: "Normal"
        }
    }) 
```
Nous avons cette réponse:
```bash
{
  acknowledged: true,
  insertedId: ObjectId('690a1233e82c2219f04f87fe')
}
```
Vérifions la présence du document: 
```bash
 db.traitement.findOne({Name:'Thomas'})

 ```
 et voilà la réponse: 
```bash
{
  _id: ObjectId('690a1233e82c2219f04f87fe'),
  Name: 'Thomas',
  Age: 30,
  Gender: 'Male',
  Blood_Type: 'B+',
  Insurance_Provider: 'Cigna',
  Admission: {
    Date_of_Admission: ISODate('2025-11-01T00:00:00.000Z'),
    Discharge_Date: ISODate('2025-11-03T00:00:00.000Z'),
    Admission_Type: 'Emergency',
    Hospital: 'Hammond Ltd',
    Room_Number: 301,
    Doctor: 'Denise Galloway',
    Billing_Amount: 2000
  },
  Diagnostic: {
    Medical_Condition: 'Asthma',
    Medication: 'Penicillin',
    Test_Results: 'Normal'
  }
}

```
Pour terminer, nous pouvons supprimer ce dernier document, car nous en avons le droit en temps que **writer**:


```bash
hcare_db> db.traitement.deleteOne({Name:'Thomas'})
```
Nous avons cette réponse:
```bash
{ acknowledged: true, deletedCount: 1 }
 ```
