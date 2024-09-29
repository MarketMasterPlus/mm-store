```
PUC-Rio
Especialização em Desenvolvimento Fullstack
Disciplina: Desenvolvimento Back-end Avançado

Aluno: Rodrigo Alves Costa
```

## Market Master: Store Management Service

The `mm-store` service is part of the Market Master project, a suite of microservices designed to manage various aspects of a supermarket e-commerce platform. This service handles store registration, updates, and management, along with integration with the `mm-address` service for address handling.

### Related Market Master Microservices:
- [mm-inventory](https://github.com/MarketMasterPlus/mm-inventory) — Inventory (available items) Management
- [mm-product](https://github.com/MarketMasterPlus/mm-product) — Product (item registry) Management
- [mm-shopping-cart](https://github.com/MarketMasterPlus/mm-shopping-cart) — Shopping Cart Management
- [mm-address](https://github.com/MarketMasterPlus/mm-address) — Address Management with ViaCEP API integration
- [mm-customer](https://github.com/MarketMasterPlus/mm-customer) — Customer/User Management
- [mm-pact-broker](https://github.com/MarketMasterPlus/mm-pact-broker) — Pact Broker for Contract tests
- [mm-ui](https://github.com/MarketMasterPlus/mm-ui) — User Interface for Market Master

---

## Quick Start

### Prerequisites
- **Docker** and **Docker Compose** are required to run this service.

### Steps to Run the Service
1. Clone the repository:  
   git clone https://github.com/MarketMasterPlus/mm-store

2. Navigate to the project directory:  
   cd mm-store

3. Start the services with Docker Compose:  
   docker-compose up -d

4. Access the Store Management API at:  
   http://localhost:5703/

---

## Project Description

The `mm-store` service is responsible for managing store data, including registering stores, updating store details, and deleting stores. It also integrates with the `mm-address` service to handle the storage and retrieval of store address data.

### Key Features
- **Store Registration**: Allows owners to register their stores by providing store information and address details.
- **Store Information Management**: Enables updating and deleting store records.
- **Integration with Address Service**: Communicates with the `mm-address` service to store address data based on the store's postal code (CEP).

---

## Docker Setup

The `docker-compose.yml` file configures the `mm-store` service and a PostgreSQL database for data storage.

### Docker Compose Configuration:

version: '3.8'

services:
  db:
    image: postgres:latest
    container_name: mm-store-db
    environment:
      POSTGRES_DB: postgres
      POSTGRES_USER: marketmaster
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./db/mm-store.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - 5434:5432
    networks:
      - marketmaster-network

  store_service:
    build: .
    container_name: mm-store
    ports:
      - 5703:5703
    depends_on:
      - db
    environment:
      FLASK_APP: app.py
      FLASK_ENV: development
    volumes:
      - .:/app
    networks:
      - marketmaster-network

volumes:
  postgres_data:

networks:
  marketmaster-network:
    external: true

To start the service using Docker, run:

docker-compose up -d

---

## API Endpoints

### Store Registration:
- **POST /mm-store/**  
  Allows store owners to register their stores by providing store information such as name, CNPJ, and address.  
  Example:  
  curl -X POST http://localhost:5703/mm-store/ -d '{"ownerid": "12345678900", "cnpj": "12345678000199", "name": "Supermarket XYZ", "cep": "58700123", "street": "Rua A", "neighborhood": "Centro", "state": "PB", "city": "Patos"}'

### Store Information:
- **GET /mm-store/**  
  Retrieves a list of all stores, or searches for stores by name or CNPJ using a query parameter (`q`).  
  Example:  
  curl http://localhost:5703/mm-store/?q=Supermarket

- **GET /mm-store/{id}**  
  Retrieves detailed information for a store by its unique identifier.  
  Example:  
  curl http://localhost:5703/mm-store/1

- **PUT /mm-store/{id}**  
  Updates store information based on the unique identifier. Fields like name, CNPJ, and address can be updated.  
  Example:  
  curl -X PUT http://localhost:5703/mm-store/1 -d '{"name": "Supermarket ABC", "cnpj": "98765432000188"}'

- **DELETE /mm-store/{id}**  
  Deletes a store record based on its unique identifier.  
  Example:  
  curl -X DELETE http://localhost:5703/mm-store/1

### Store Search by City:
- **GET /mm-store/city/{city}**  
  Fetches stores based on the city name.  
  Example:  
  curl http://localhost:5703/mm-store/city/Patos

---

## Running the Flask Application Locally

If you prefer to run the service without Docker, follow the steps below.

### Step 1: Install Dependencies

Make sure you have Python 3 and `pip` installed. Then, install the required dependencies:

pip install -r requirements.txt

### Step 2: Configure Environment Variables

Create a `.env` file in the root of the project with the following content:

FLASK_APP=app.py  
FLASK_ENV=development  
DATABASE_URL=postgresql://marketmaster:password@localhost:5434/postgres

### Step 3: Run the Application

With the environment variables set, you can run the Flask application:

flask run

By default, the service will be accessible at `http://localhost:5703`.

---

## Additional Information

This microservice is part of the Market Master system, providing store management features that are essential for supermarket owners. It is closely integrated with other services in the system, such as the `mm-address` service for managing store addresses.

For more details about the Market Master project and to explore other microservices, visit the respective repositories:

- [mm-inventory](https://github.com/MarketMasterPlus/mm-inventory)
- [mm-product](https://github.com/MarketMasterPlus/mm-product)
- [mm-shopping-cart](https://github.com/MarketMasterPlus/mm-shopping-cart)
- [mm-address](https://github.com/MarketMasterPlus/mm-address)
- [mm-customer](https://github.com/MarketMasterPlus/mm-customer)
- [mm-pact-broker](https://github.com/MarketMasterPlus/mm-pact-broker)
- [mm-ui](https://github.com/MarketMasterPlus/mm-ui)

For any further questions, feel free to open an issue on GitHub or consult the provided documentation within each repository.
