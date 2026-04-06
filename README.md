# 🏥 Hospital Management System API (HMS Backend)

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0-092E20?style=for-the-badge&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Google Cloud](https://img.shields.io/badge/Google_Cloud-Run-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)

A robust, cloud-native backend REST API designed to streamline hospital operations, patient management, and automated billing. Built with modern Django and fully containerized for highly available, serverless deployment.

## 🚀 Live Production Environment
This API is continuously deployed via Google Cloud Build and hosted on Google Cloud Run. 
* **Live Base URL:** `https://hospital-managemnet-api-409389836892.europe-west1.run.app`
* **Admin Portal:** `https://hospital-managemnet-api-409389836892.europe-west1.run.app/admin/`

---

## 🏗️ Cloud & System Architecture
This project goes beyond standard local development, featuring a fully automated, production-grade cloud infrastructure:

* **Serverless Compute:** Containerized with Docker and deployed to **Google Cloud Run** for auto-scaling and high availability.
* **Continuous Deployment (CI/CD):** Integrated with **Google Cloud Build** to automatically trigger, build, and deploy new Docker images upon pushing to the `master` branch.
* **Managed Database:** Powered by a serverless **Neon PostgreSQL** database for decoupled, resilient data storage.
* **Static File Management:** Optimized with **WhiteNoise** to serve production assets directly from the Gunicorn WSGI server.
* **System-Level PDF Rendering:** Configured custom Linux dependencies (Cairo, Pango) within the Dockerfile to support **WeasyPrint** for automated, high-fidelity PDF invoice generation.

---

## ✨ Key Features

* **🩺 Clinical Management:** Securely handle patient records, doctor assignments, and medical histories.
* **💳 Automated Billing & Invoicing:** Generate professional, downloadable PDF invoices dynamically using HTML-to-PDF rendering via WeasyPrint.
* **🔐 Secure Authentication:** Configured with robust CSRF protections, allowed host routing, and secure proxy trusting for seamless admin access in the cloud.
* **🌐 RESTful Architecture:** Clean, predictable endpoints built for seamless integration with modern frontend frameworks or mobile apps.

---

## 🛠️ Technology Stack

**Core Application:**
* Python 3.12
* Django 6.0
* Django REST Framework

**Infrastructure & DevOps:**
* Docker & Dockerfile scripting
* Google Cloud Platform (Cloud Run, Cloud Build)
* Gunicorn (WSGI HTTP Server)

**Database & Utilities:**
* PostgreSQL (Neon)
* WeasyPrint (PDF Generation)
* dj-database-url (Environment variable parsing)

---

## 💻 Local Development Setup

Want to run this project locally? Follow these steps:

**1. Clone the repository**
```bash
git clone [https://github.com/333IAN/Hospital-Managemnet-API.git](https://github.com/333IAN/Hospital-Managemnet-API.git)
cd Hospital-Managemnet-API
```
### **2. Create and Activate Virtual Environment**

```bash
python3 -m venv venv
```

#### Activate the virtual environment:

**Linux / Mac:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```
### **3. Install Dependencies**

```bash
pip install -r requirements.txt
```
### **4. Set Up Environment Variables**

Create a `.env` file in the root directory:

```bash
touch .env
```

Add your environment variables:

```env
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url
```
### **5. Apply Migrations**

```bash
python manage.py migrate
```
### **6. Create Superuser**

```bash
python manage.py createsuperuser
```
### **7. Run Development Server**

```bash
python manage.py runserver
```

Visit:

```
http://127.0.0.1:8000/
```