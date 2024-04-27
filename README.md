# Telecom Customer Management System

Welcome to the Telecom Customer Management System! This application provides a RESTful API for managing telecom customers.

## Prerequisites

Before running the application, make sure you have the following prerequisites installed:

- Python 3.x
- pip
- virtualenv (optional but recommended)

## Getting Started

To get started with the Telecom Customer Management System, follow these steps:

1. Clone the repository:
2. Create and activate a virtual environment (optional but recommended):
3. Install the required dependencies:
4. Set up the database:
5. Start the application: `python3 main.py`
6. Open your browser and visit `http://localhost:8000/docs` to access the API documentation.

## API Documentation

The Telecom Customer Management System provides the following API endpoints:

- `/customers`: Manage telecom customers.
- `GET /customers`: Retrieve a list of customers.
- `POST /customers`: Create a new customer.
- `GET /customers/{customer_id}`: Retrieve details of a specific customer.
- `PUT /customers/{customer_id}`: Update the details of a specific customer.
- `DELETE /customers/{customer_id}`: Delete a specific customer.
- `PUT /change_plan`: Update the plan of a specific customer.

For more detailed information about each endpoint, refer to the API documentation at `http://localhost:8000/docs`.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
