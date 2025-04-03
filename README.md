# Project Technical Decisions and Architecture
## 1. Web Scraping
Frameworks/Libraries Used:

Selenium: Chosen to interact with websites that rely on JavaScript for rendering dynamic content. Selenium allows for automation of web browsers, ensuring the website's JavaScript executes fully before scraping.

BeautifulSoup: Used to parse the static HTML content once Selenium has rendered the page. BeautifulSoup makes it easier to extract structured data from the HTML.

Selenium is selected over traditional scraping methods (like requests or urllib) because the target website uses JavaScript for dynamic content loading. By using Selenium, we can interact with the website as a user would, ensuring that all dynamic content is rendered. BeautifulSoup is then utilized to extract the necessary data from the resulting static HTML content after rendering, ensuring accurate and structured scraping.

## 2. Data Synchronization
Functionality: A synchronization function ensures that data entered into the database is not redundant and maintains consistency between scraping sessions. This function is crucial to prevent unnecessary duplicate entries and maintain data integrity.

The sync function ensures that when the script is rerun, only updated or new data is inserted into the database, ensuring the database contains the most up-to-date information without redundancies.

## 3. Database - PostgreSQL

While there are no specific technical requirements to use PostgreSQL, it was chosen due to familiarity and ease of use. PostgreSQL is a robust, open-source relational database that can scale to more complex systems, should the need arise. Given the simplicity of the database for this project, PostgreSQL serves as a reliable solution for managing data effectively.

### Entitiy Relationship Diagram (ERD) :

The database design in the attached ERD is intentionally simple and might not represent a real-world system's design for scalability. The design has been tailored to ensure consistency for the LLM (text-to-SQL bot) integration, with minor configuration. While not necessarily optimal for larger, production-level systems, it suffices for the scope and requirements of the current project.

## 4. FastAPI
These endpoints serve as the bridge between the frontend and backend. The fetchoutlet endpoint handles retrieval of outlet data, while the chatbot endpoint leverages the LLM to ensure consistent SQL query generation for complex data retrieval tasks.
Programming Language: Python 3.11

Endpoints:

fetchoutlet: This endpoint retrieves data about outlets, based on the provided parameters.

chatbot: This endpoint interacts with the LLM (text-to-SQL bot) to generate SQL queries based on user inputs, ensuring a smooth backend for the static frontend.

## 5. Text-to-SQL Bot - OpenAI GPT-4 ("gpt-4o-2024-08-06")

The choice to implement a text-to-SQL bot was driven by the need for consistent and accurate query generation. While retrieval-augmented generation (RAG) models excel in providing contextually relevant responses, they can be imprecise when it comes to generating consistent SQL queries based on factors like address, facility, and branch name. The GPT-4 model, used here, is trained to handle such tasks, ensuring more precise control over SQL query formation, particularly for WHERE clauses.

## 6. Frontend Framework - React (JavaScript)

Despite me being relatively new to React, the framework was chosen for its ability to create responsive user interfaces. React’s component-based architecture is well-suited for building interactive and dynamic web applications, which aligns well with the project’s goal of providing a responsive and user-friendly frontend for the web application.

## 7. Hosting
