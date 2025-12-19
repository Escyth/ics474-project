# ICS474 - Term Project
**Prepared by:**
- Usama Bakkar (202263960)
- Naif Alenazi (202163490)
- Anas Alhanaya (201967330)

**Demo:** < INSERT LINK HERE >

Access the original repository [here](https://github.com/abeltavares/real-time-data-pipeline).

## Use Case
The use case of this project is **real-time clickstream analysis** for a web-based application. The system continuously captures user interaction events, such as page visits and clicks, and analyzes them as they occur. This enables real-time monitoring of user behavior, allowing stakeholders to observe activity trends, identify popular content, and detect unusual patterns in user interactions.

Such a use case is commonly applied in scenarios including user behavior analytics, traffic monitoring, and operational dashboards for large-scale web platforms, where timely insights from high-volume event streams are critical for informed decision-making.

## Architecture
The technologies used are: [Kafka](https://kafka.apache.org/) and [ZooKeeper](https://zookeeper.apache.org/) for **Data Ingestion**, [Flink](https://flink.apache.org/) for **Stream Processing**, [MinIO](https://www.min.io/) for **Storage**, [Iceberg](https://iceberg.apache.org/) for **Data Lake Table Format**, [Trino](https://trino.io/) for **Query Engine**, and [Superset](https://superset.apache.org/) for **Visualization**.

Kafka receives data from either real or simulated sources, while ZooKeeper is used for distributed coordination and metadata management. Then the data is streamed to Flink for processing. After being processed, it is stored in MinIO using the Iceberg table format, which is then queried by Trino based on visualization requests from Superset. All services are containerized with Docker for easy deployment and higher reproducibility.

Visual Representation:

![Architecture](https://i.imgur.com/eSOQlEU.png)

As an additional step in this pipeline, [Faker](https://faker.readthedocs.io/) (a Python library) is used to generate synthetic clickstream data, serving as the data source for the ingestion layer. The data structure and example events are described in Appendix B, and the corresponding implementation can be found in `producer/producer.py`.

| Technology | Why |
|:----------:|-----|
| Kafka | Provides a high-throughput, fault-tolerant messaging layer to ingest streaming data and decouple producers from consumers. |
| ZooKeeper | Handles distributed coordination and metadata management required by Kafka in this setup. |
| Flink | Enables low-latency, stateful stream processing for real-time data transformation and filtering. |
| MinIO | Acts as scalable object storage. |
| Iceberg | Provides a table format on top of object storage with schema evolution and reliable reads/writes. |
| Trino | Enables fast, interactive SQL queries over Iceberg tables without moving data. |
| Superset | Provides visualization and dashboarding capabilities for querying and exploring processed data. |
| Faker | Generates realistic synthetic data to simulate real-world event streams for testing the pipeline. |

This architecture represents a modern lakehouse-style streaming analytics pipeline commonly used in industry.

## Installation
This project, as per the original repository, has a recommended minimum of 16GB memory.

1. Ensure [Docker](https://docs.docker.com/) is installed (with Compose).
2. Clone this repository:
```sh
git clone https://github.com/Escyth/ics474-project
cd ics474-project
```
3. Start the services with `docker-compose up -d`.
4. Done! You may now access the services, refer to Appendix A for ports and login credentials.
5. Run `docker-compose down -v` or `Ctrl+C` to kill all services.

## Data Visualization
The component that is concerned with visualization in this pipeline is Superset. To start visualization, follow these steps:
1. Access Superset at [http://localhost:8088](http://localhost:8088).
2. Login with credentials in Appendix A.
3. Connect Superset to Trino with the SQLAlchemy URI `trino://trino@trino:8080/iceberg/db`.
4. Create dashboards.

You may refer to Appendix C for a complete step-by-step guide with images and example dashboard.

## Challenges & Fixes
Although the original repository had a solid, ready pipeline, we faced a few challenges:
1. **Windows volume path fixes:** The repository used `${PWD}` in its configuration which would not resolve properly on our Windows machine, so we had to replace all instances of `${PWD}` with `./` to refer to the current directory.
2. **Superset and Trino integration fixes:** Initially, the Superset service could not find the Trino driver due to Python environment mismatches, so we modified `superset/Dockerfile` to ensure the Trino SQLAlchemy driver was installed in the correct Python environment used by Superset.
3. **Outdated MinIO mc command:** The configuration of mc (MinIO client) used an outdated command, which was changed in later versions, so we had to update that in `docker-compose.yaml`.

## Appendices
### A
| Service | URL | Credentials |
|:------:|:---:|:-----------:|
| Kafka Control Center | http://localhost:9021 | No Auth |
| Flink | http://localhost:18081 | No Auth |
| MinIO | http://localhost:9001 | admin / password |
| Trino | http://localhost:8080/ui | No Auth |
| Superset | http://localhost:8088 | admin / admin |

### B
Structure:
```python
{
  "event_id": fake.uuid4(),
  "user_id": fake.uuid4(),
  "event_type": fake.random_element(elements=("page_view",        "add_to_cart", "purchase", "logout")),
  "url": fake.uri_path(),
  "session_id": fake.uuid4(),
  "device": fake.random_element(elements=("mobile", "desktop", "tablet")),
  "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
  "geo_location": {
      "lat": float(fake.latitude()),
      "lon": float(fake.longitude())
  },
  "purchase_amount": float(random.uniform(0.0, 500.0)) if fake.boolean(chance_of_getting_true=30) else None
}
```
Examples (`add_to_cart` and `purchase` events):

![Faker example](https://i.imgur.com/eXe86w1.png)
![Faker example](https://i.imgur.com/UTtQRku.png)

### C
To establish a connection to the database:
1. Access Superset.
![C-1-1](https://i.imgur.com/GQjOUXG.png)
2. Login and connect database.
![C-1-2](https://i.imgur.com/gvf0D20.png)
3. Select database type, Trino, from the dropdown list.
![C-1-3](https://i.imgur.com/yGUVUmL.png)
4. Enter the SQLAlchemy URI, test the connection, and connect.
![C-1-4](https://i.imgur.com/ptt07Rs.png)
5. Now, the connection to the database is established.

To create a dashboard:
1. Go to the Dashboards page and click on "+ Dashboard".
![C-2-1](https://i.imgur.com/t8RQQrl.png)
2. Click on "+ Create a new chart" and (optionally) set a name for the dashboard.
![C-2-2](https://i.imgur.com/12EkVWO.png)
3. Click on "Add a dataset".
![C-2-3](https://i.imgur.com/XxeJ3ES.png)
4. Configure the dataset information and click on "Create dataset".
![C-2-4](https://i.imgur.com/dwH5xKp.png)
5. Go back to the chart page, select the dataset, and Big Number type, then click on "Create new chart".
![C-2-5](https://i.imgur.com/UiSOhuD.png)
6. Choose Metric and fill in the fields as shown then Save. Finally, click on "Create chart".
![C-2-6](https://i.imgur.com/YHglSyC.png)
7. Now, you have a working live dashboard showing the total revenue.