# Smart Healthcare Optimizer [🧑‍⚕️+🖥️]

It leverages predictive analytics and data to streamline patient scheduling, staffing, and resource management in healthcare facilities, enhancing efficiency and patient care.


## 📋Features

- **Time-Series Forecasting**: Predict future patient inflows using the Prophet model.
- **Staffing Recommendations**: Adjust staffing levels based on forecasted patient volumes.
- **Interactive Dashboard**: Visualize patient inflows, staffing needs, and resource utilization.
- **Advanced Chatbot**: Retrieve data-driven answers about patients, staff, and hospital resources using LangChain and Neo4j.


## 💡The Project

The proposed solution showcases originality and innovation in addressing healthcare optimization through the following methods:

- **Enhanced Data Access and Decision-Making:** The solution emphasizes easy data access, which is crucial for effective decision-making in healthcare. Users can effortlessly access and interpret complex datasets by integrating an interactive dashboard with data visualization. This real-time visualization aids data-driven decisions on patient inflows, staffing, and resource utilization, improving operational efficiency and patient care.

- **Innovative Chatbot Integration:** The RAG (Retrieval-Augmented Generation) chatbot, powered by LangChain and Neo4j, innovatively enhances data accessibility. Users can query the system as if interacting with a human, retrieving data on patients, hospital locations, and other critical aspects. Integrated with OpenAI’s API, the chatbot generates accurate, contextually relevant responses, simplifying data retrieval and providing real-time insights.

- **Application of Time-Series Forecasting:** Utilizing time-series forecasting models like Prophet for predicting patient inflows is an innovative application of predictive analytics in healthcare. This approach allows for proactive resource planning and staffing adjustments, moving beyond traditional reactive methods. It helps manage patient flow challenges before they become critical, contributing to more efficient and responsive healthcare services.

- **Staffing Recommendations:** The solution provides staffing recommendations based on forecasted patient inflows. Unlike static staffing models, this dynamic approach adjusts staffing needs according to predicted patient volumes, ensuring facilities can adapt to fluctuations in demand. This flexibility minimizes waiting times and optimizes staff deployment, significantly advancing over fixed staffing schedules.

- **Comprehensive Resource Utilization Tracking:** Tracking of resource utilization, such as bed occupancy and equipment usage, adds another layer of innovation. This feature offers a comprehensive view of resource allocation, helping administrators manage resources more effectively. Integrating this data into the dashboard enables a holistic approach to healthcare optimization, addressing both staffing and resource management simultaneously.

In summary, the solution stands out for its innovative use of predictive analytics, advanced chatbot technology, and real-time resource management. By enhancing data accessibility and leveraging technologies like Neo4j and OpenAI’s API, it offers a unique approach to optimizing healthcare operations and improving patient care.


> **_NOTE:_** The dataset used in this project is entirely synthetic, meaning it has been artificially created rather than collected from real-world sources. Additionally, some of the CSV files used in this project have been generated programmatically using Python code. This approach ensures that the data adheres to the necessary structure and patterns required for the project's objectives, while avoiding any privacy or confidentiality concerns associated with real patient data.

## ⚡Getting Started

Create a ```.env``` file in the root directory and add the following environment variables:
```
NEO4J_URI=<YOUR_NEO4J_URI>
NEO4J_USERNAME=<YOUR_NEO4J_USERNAME>
NEO4J_PASSWORD=<YOUR_NEO4J_PASSWORD>

OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>

HOSPITALS_CSV_PATH=https://raw.githubusercontent.com/ArmaanMistry/health_optimization/main/data/hospitals.csv
PAYERS_CSV_PATH=https://raw.githubusercontent.com/ArmaanMistry/health_optimization/main/data/payers.csv
PHYSICIANS_CSV_PATH=https://raw.githubusercontent.com/ArmaanMistry/health_optimization/main/data/physicians.csv
PATIENTS_CSV_PATH=https://raw.githubusercontent.com/ArmaanMistry/health_optimization/main/data/patients.csv
VISITS_CSV_PATH=https://raw.githubusercontent.com/ArmaanMistry/health_optimization/main/data/visits.csv
REVIEWS_CSV_PATH=https://raw.githubusercontent.com/ArmaanMistry/health_optimization/main/data/reviews.csv

INFLOW_CSV_PATH=https://raw.githubusercontent.com/ArmaanMistry/health_optimization/main/data/patient_inflow.csv
RESOURCE_URL=https://raw.githubusercontent.com/ArmaanMistry/health_optimization/main/data/resource_utilization.csv

CHATBOT_URL=http://host.docker.internal:8000/hospital-rag-agent

HOSPITAL_AGENT_MODEL=gpt-3.5-turbo-1106
HOSPITAL_CYPHER_MODEL=gpt-3.5-turbo-1106
HOSPITAL_QA_MODEL=gpt-3.5-turbo-0125

NEO4J_CYPHER_EXAMPLES_INDEX_NAME=questions
NEO4J_CYPHER_EXAMPLES_NODE_NAME=Question
NEO4J_CYPHER_EXAMPLES_TEXT_NODE_PROPERTY=question
NEO4J_CYPHER_EXAMPLES_METADATA_NAME=cypher
```

The ```NEO4J_``` variables are used to connect to your [Neo4j AuraDB instance](https://openai.com/index/openai-api/).

You'll need to create an [OpenAI API key](https://neo4j.com/) and store it as ```OPENAI_API_KEY```.

This is the project directory:
```
./
│
├── chatbot_api/
│   │
│   │
│   ├── src/
│   │   │
│   │   ├── agents/
│   │   │   └── hospital_rag_agent.py
│   │   │
│   │   ├── chains/
│   │   │   │
│   │   │   ├── hospital_cypher_chain.py
│   │   │   └── hospital_review_chain.py
│   │   │
│   │   ├── models/
│   │   │   └── hospital_rag_query.py
│   │   │
│   │   ├── tools/
│   │   │   └── wait_times.py
│   │   │
│   │   ├── utils/
│   │   │   └── async_utils.py
│   │   │
│   │   ├── entrypoint.sh
│   │   └── main.py
│   │
│   ├── Dockerfile
│   └── pyproject.toml
│
├── chatbot_frontend/
│   ├── predictions/
│   │   └── patient_inflow.py
│   │
│   ├── src/
│   │   ├── entrypoint.sh
│   │   └── main.py
│   │
│   ├── Dockerfile
│   └── pyproject.toml
│
├── hospital_neo4j_etl/
│   │
│   ├── src/
│   │   ├── entrypoint.sh
│   │   └── hospital_bulk_csv_write.py
│   │
│   ├── Dockerfile
│   └── pyproject.toml
│
├── data/
│   └── ...
│
├── .env
└── docker-compose.yml
```

Execute the following command in the terminal to run the code, ensuring Docker is open:
```
docker-compose up --build --remove-orphans
```
## ▶️Video

The Interface : https://youtu.be/rZDDdEg9_No

