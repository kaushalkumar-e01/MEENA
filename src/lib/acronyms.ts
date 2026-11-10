/**
 * Comprehensive Knowledge Base & Acronym Dictionary for MEENA
 * Maps common technical, academic, medical, and scientific terms & acronyms directly.
 */

export const ACRONYM_DICTIONARY: Record<string, { fullName: string; explanation: string; details?: string }> = {
  DBMS: {
    fullName: 'Database Management System',
    explanation: 'A **Database Management System (DBMS)** is system software used for creating, managing, storing, organizing, and retrieving data from databases. It serves as an interface between end-users or application programs and the underlying database, ensuring that data is consistently organized and easily accessible.',
    details: `### Key Advantages of a DBMS:
1. **Data Redundancy Control**: Minimizes unnecessary duplication of data across multiple files.
2. **Data Consistency & Integrity**: Enforces business constraints and rules so data remains accurate and valid.
3. **Data Security**: Restricts unauthorized access through role-based access permissions.
4. **Multi-User Access & Concurrency Control**: Allows multiple users to read and update data simultaneously without conflicts.
5. **Backup & Recovery**: Provides automated routines to recover data in the event of hardware or system failures.

### Popular Examples:
- **Relational DBMS (RDBMS)**: PostgreSQL, MySQL, Oracle Database, Microsoft SQL Server, SQLite.
- **NoSQL DBMS**: MongoDB, Apache Cassandra, Redis, DynamoDB.`
  },
  RDBMS: {
    fullName: 'Relational Database Management System',
    explanation: 'A **Relational Database Management System (RDBMS)** is a DBMS based on the relational model introduced by E.F. Codd, where data is organized into tables (relations) consisting of rows (tuples) and columns (attributes), queried using SQL (Structured Query Language).'
  },
  SQL: {
    fullName: 'Structured Query Language',
    explanation: 'A standardized programming language used to manage, query, and manipulate relational databases.'
  },
  API: {
    fullName: 'Application Programming Interface',
    explanation: 'A set of rules, protocols, and definitions that allows different software applications to communicate and transfer data with one another.'
  },
  CPU: {
    fullName: 'Central Processing Unit',
    explanation: 'The primary component of a computer that performs arithmetic, logic, controlling, and input/output operations specified by instructions in a program.'
  },
  RAM: {
    fullName: 'Random Access Memory',
    explanation: 'High-speed volatile computer memory that temporarily stores data and machine code currently being used by the operating system and running programs.'
  },
  HTTP: {
    fullName: 'Hypertext Transfer Protocol',
    explanation: 'An application-layer protocol for transmitting hypermedia documents, such as HTML, forming the foundation of data communication on the World Wide Web.'
  },
  HTTPS: {
    fullName: 'Hypertext Transfer Protocol Secure',
    explanation: 'An extension of HTTP that uses Transport Layer Security (TLS) or Secure Sockets Layer (SSL) encryption to secure communication over computer networks.'
  },
  URL: {
    fullName: 'Uniform Resource Locator',
    explanation: 'A reference to a web resource that specifies its location on a computer network and a mechanism for retrieving it.'
  },
  HTML: {
    fullName: 'HyperText Markup Language',
    explanation: 'The standard markup language used for creating and structuring web pages and web applications.'
  },
  CSS: {
    fullName: 'Cascading Style Sheets',
    explanation: 'A stylesheet language used for describing the presentation, formatting, and layout of a document written in HTML.'
  },
  OOP: {
    fullName: 'Object-Oriented Programming',
    explanation: 'A programming paradigm based on the concept of "objects", which contain data (fields/attributes) and code (methods/behaviors).'
  },
  AI: {
    fullName: 'Artificial Intelligence',
    explanation: 'The simulation of human intelligence processes by machines and computer systems, including learning, reasoning, and self-correction.'
  },
  ML: {
    fullName: 'Machine Learning',
    explanation: 'A branch of artificial intelligence focused on building applications that learn from data and improve their accuracy over time without being explicitly programmed.'
  },
  NLP: {
    fullName: 'Natural Language Processing',
    explanation: 'A subfield of computer science, artificial intelligence, and linguistics concerned with the interactions between computers and human natural language.'
  },
  LLM: {
    fullName: 'Large Language Model',
    explanation: 'A computational model capable of language generation and other natural language processing tasks, trained on vast amounts of text data.'
  },
  IoT: {
    fullName: 'Internet of Things',
    explanation: 'A network of physical devices and objects embedded with sensors, software, and connectivity technologies to exchange data with other devices over the internet.'
  },
  GUI: {
    fullName: 'Graphical User Interface',
    explanation: 'A user interface that allows users to interact with electronic devices through graphical icons and visual indicators rather than text-based command interfaces.'
  },
  CLI: {
    fullName: 'Command Line Interface',
    explanation: 'A text-based interface used to run programs, manage computer files, and interact with the operating system by typing commands.'
  },
  JSON: {
    fullName: 'JavaScript Object Notation',
    explanation: 'A lightweight, text-based data-interchange format that is easy for humans to read and write and easy for machines to parse and generate.'
  },
  REST: {
    fullName: 'Representational State Transfer',
    explanation: 'A software architectural style for providing standards between computer systems on the web, typically using HTTP verbs (GET, POST, PUT, DELETE).'
  },
  ACID: {
    fullName: 'Atomicity, Consistency, Isolation, Durability',
    explanation: 'A set of standard properties of database transactions intended to guarantee validity even in the event of errors, power failures, or crashes.'
  }
};
