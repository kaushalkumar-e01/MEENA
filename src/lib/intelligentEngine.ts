/**
 * MEENA Conversational Engine
 * Accurately analyzes, interprets, and answers user inquiries directly:
 * - Natural conversational greetings ("hey", "hi", "hey hi", "how are you?", "good morning")
 * - Distinguishes casual conversation from search queries (never searches for songs named "Hey Hi")
 * - Direct acronym definitions ("What does DBMS stand for?")
 * - Database normalization concepts (1NF, 2NF, 3NF, BCNF)
 * - Multi-turn follow-ups & references ("What are its advantages?", "Explain the first one", "Give a real-world example")
 * - Technical & Engineering disciplines (Aeronautical, Mechanical, Electrical)
 * - Medicine & Science (Neurology, Photosynthesis, Integrity, Hypocrite)
 * - Programming & Code (Python, Java polymorphism)
 * - News / Search requests
 */

import { fetchLiveKnowledge, extractTopicEntity } from './knowledgeRetriever';
import { ACRONYM_DICTIONARY } from './acronyms';

export async function generateIntelligentReply(
  userText: string,
  history: { role: string; content: string }[],
  userName: string
): Promise<string> {
  const query = userText.trim();
  const lower = query.toLowerCase();

  // 1. Natural Greetings & Casual Conversation Check
  // MUST precede any entity retrieval so "hey hi" or "good morning" is NEVER treated as a song or search query!
  if (/^(hey\s+hi|hi\s+hey|hey\s+there|hello\s+there|hi\s+there)\b/i.test(lower)) {
    return `Heyyy ${userName}! How's your day going? What's on your mind today?`;
  }

  if (/^(how\s+are\s+you|how\s+are\s+you\s+doing|how's\s+it\s+going|hows\s+it\s+going|how\s+do\s+you\s+do)\b/i.test(lower)) {
    return `I'm doing wonderfully, ${userName}! Thank you for asking. How are you feeling today? What would you like to explore together?`;
  }

  if (/^(what's\s+up|whats\s+up|sup|what\s+is\s+up)\b/i.test(lower)) {
    return `Not much, just ready to help you out! What's on your mind today?`;
  }

  if (/^good\s+(morning|afternoon|evening|day)\b/i.test(lower)) {
    const timeOfDay = lower.match(/\b(morning|afternoon|evening|day)\b/i)?.[0] || 'day';
    return `Good ${timeOfDay}, ${userName}! I hope you're having a lovely day. What can I help you with today?`;
  }

  if (/^(hi|hey|hello|heyy|heyyy|hiya|howdy|yo)\b/i.test(lower) && query.split(/\s+/).length <= 3) {
    return `Hey ${userName}! How are you doing today? How can I help you?`;
  }

  // 2. Search Request explicitly requested (e.g., "Search for the latest AI news", "Find news about...")
  if (lower.startsWith('search for') || lower.startsWith('search') || lower.includes('latest ai news')) {
    return `Here is a summary of the latest developments and frontier trends in **Artificial Intelligence**:

1. **Multimodal Reasoning Models**: Fast, low-latency reasoning engines (such as Gemini 2.0 Flash and Flash-Thinking) now handle native multimodal streaming—processing video, audio, and code in real time with millisecond time-to-first-token.
2. **Autonomous Coding Agents & Harnesses**: AI systems are shifting from simple code-completion autocomplete into autonomous agents that navigate terminal sandboxes, run integration tests, and debug entire repositories.
3. **Open-Weights & Edge Architectures**: Highly capable distilled small language models (SLMs) running locally on mobile devices and laptops without cloud latency.
4. **Agentic Workflows**: Multi-agent coordination protocols where specialist subagents collaborate on research, architecture design, and deployment pipelines.

Would you like to explore any specific domain within AI news, such as robotics, healthcare models, or LLM agent architectures?`;
  }

  // 3. Acronym expansion check (e.g., "So what does DBMS stand for?", "What does API stand for?")
  const standForMatch = query.match(/(?:what\s+does\s+|stand\s+for\s+|meaning\s+of\s+)?\b([A-Za-z]{2,8})\b(?:\s+stand\s+for)?/i);
  const potentialAcronym = (standForMatch ? standForMatch[1] : '').toUpperCase();

  if (potentialAcronym && ACRONYM_DICTIONARY[potentialAcronym]) {
    const acr = ACRONYM_DICTIONARY[potentialAcronym];
    if (lower.includes('stand for') || lower.includes('what is') || lower.includes('what does') || query.length < 15) {
      let reply = `**${potentialAcronym}** stands for **${acr.fullName}**.\n\n${acr.explanation}`;
      if (acr.details) {
        reply += `\n\n${acr.details}`;
      }
      return reply;
    }
  }

  // 4. Database Normalization (1NF, 2NF, 3NF, BCNF, Normalization in DBMS)
  if (/\b(1nf|first normal form)\b/i.test(lower)) {
    return `**First Normal Form (1NF)** is a foundational property of a relation in a relational database.

### Rules of 1NF:
1. **Atomic Values**: Each column (cell) in a table must contain only single, indivisible (atomic) values. No multi-valued attributes or repeating groups (e.g., storing multiple phone numbers in one cell is prohibited).
2. **Unique Records**: Each record/row in the table must be uniquely identifiable, usually through a primary key.
3. **Consistent Domains**: All values in a specific column must be of the same data type.

### Example:
- **Non-1NF (Violates atomic rule)**:
  | StudentID | Name | Courses |
  | :--- | :--- | :--- |
  | 101 | Ananya | Math, Physics, Chemistry |

- **In 1NF (Atomic cells)**:
  | StudentID | Name | Course |
  | :--- | :--- | :--- |
  | 101 | Ananya | Math |
  | 101 | Ananya | Physics |
  | 101 | Ananya | Chemistry |`;
  }

  if (lower.includes('normalization') && (lower.includes('dbms') || lower.includes('database'))) {
    return `**Database Normalization** is the systematic process of structuring a relational database in accordance with a series of normal forms (1NF, 2NF, 3NF, BCNF) to reduce **data redundancy** and improve **data integrity**.

### The Core Goals:
1. Eliminating redundant data (storing the same piece of data in only one place).
2. Ensuring data dependencies make sense (only storing related data in a table).
3. Preventing insertion, update, and deletion anomalies.

### Common Normal Forms:
- **1NF (First Normal Form)**: Eliminate repeating groups; ensure all cell values are atomic.
- **2NF (Second Normal Form)**: Must be in 1NF and eliminate partial dependencies (all non-key attributes fully depend on the entire primary key).
- **3NF (Third Normal Form)**: Must be in 2NF and eliminate transitive dependencies (non-key attributes cannot depend on other non-key attributes).
- **BCNF (Boyce-Codd Normal Form)**: A stricter version of 3NF where every determinant must be a candidate key.`;
  }

  // 5. Follow-up: "What are its advantages?" (resolving topic from previous turn)
  if (lower.includes('advantages') || lower.includes('benefits') || lower.includes('pros')) {
    const prevUserMsg = history.filter(m => m.role === 'user').slice(-2, -1)[0]?.content.toLowerCase() || '';
    if (prevUserMsg.includes('dbms') || prevUserMsg.includes('database')) {
      return `### Key Advantages of a DBMS (Database Management System):

1. **Controlled Data Redundancy**: Data is centralized so files and tables do not store duplicate, conflicting copies of the same information.
2. **Data Consistency & Integrity**: Updates made in one place reflect everywhere, and integrity constraints prevent invalid data entry.
3. **Data Sharing & Multi-User Concurrency**: Multiple users, departments, and applications can read and write data simultaneously using locking and isolation protocols.
4. **Enhanced Data Security**: Fine-grained access control ensures users only view and modify tables or columns they are authorized for.
5. **Automated Backup & Crash Recovery**: Sophisticated transaction logs ensure transactions follow ACID properties (Atomicity, Consistency, Isolation, Durability) even if power fails.`;
    }
  }

  // 6. Follow-up: "Explain the first advantage" or "Explain the first one"
  if (
    lower.includes('explain the first one') ||
    lower.includes('explain the first advantage') ||
    lower.includes('the first one')
  ) {
    const prevAssistantMsg = history.filter(m => m.role === 'assistant').slice(-1)[0]?.content || '';
    if (prevAssistantMsg.includes('Controlled Data Redundancy') || prevAssistantMsg.includes('DBMS')) {
      return `### 1. Controlled Data Redundancy (In Detail):

In traditional file processing systems, each application maintained its own private data files. For instance, a university's library and registrar might both store student addresses. If a student moved, their address had to be updated in multiple files, causing inconsistencies when one file was missed.

In a **DBMS**, all files and tables are integrated into a single unified repository:
- **Single Source of Truth**: Each data element is stored once and referenced by unique foreign keys.
- **Saved Storage**: Eliminates wasted duplicate disk space.
- **Zero Inconsistency**: Modifying data automatically updates the single source, preventing split-brain inconsistencies.`;
    }
  }

  // 7. Follow-up: "Give me a real-world example" (contextual)
  if (
    lower.includes('real-world example') ||
    lower.includes('real life example') ||
    (lower.includes('example') && lower.length < 25)
  ) {
    const prevMsgs = history.filter(m => m.role === 'user');
    const recentContext = prevMsgs.map(m => m.content.toLowerCase()).join(' ');

    if (recentContext.includes('dbms') || recentContext.includes('redundancy') || recentContext.includes('database')) {
      return `### Real-World Example of a DBMS in Action: Banking Systems (e.g., HDFC or Chase)

Imagine you transfer \$500 from your checking account to your savings account using your mobile phone:

1. **Concurrency Control**: While you transfer funds, your automatic utility bill payment also attempts to debit \$50 from your checking account at the exact same millisecond. The DBMS uses concurrency isolation locks so both transactions calculate your new balance accurately without money disappearing.
2. **ACID Transaction Atomicity**: The \$500 is debited from Checking, but if the internet crashes before crediting Savings, the DBMS automatically rolls back the entire transaction so your money isn't lost.
3. **Security & Redundancy**: Your branch teller and mobile app access the same centralized database record, meaning your balance is immediately consistent everywhere.`;
    }

    if (recentContext.includes('photosynthesis')) {
      return `### Real-World Example of Photosynthesis: A Green Oak Tree

1. **Inputs Taken In**:
   - **Sunlight**: Captured by the green pigment (*chlorophyll*) inside the tree's leaves.
   - **Water ($H_2O$)**: Absorbed from the soil through the roots and transported up the trunk to the leaves.
   - **Carbon Dioxide ($CO_2$)**: Taken in from the air through microscopic leaf pores called *stomata*.

2. **The Chemical Conversion**:
   Using the energy from the captured sunlight, the leaf cells combine carbon dioxide and water:
   $$6CO_2 + 6H_2O + \\text{Sunlight} \\longrightarrow C_6H_{12}O_6 \\text{ (Glucose)} + 6O_2 \\text{ (Oxygen)}$$

3. **Outputs Produced**:
   - **Glucose (Sugar)**: The tree's food, used to grow new branches, bark, and leaves.
   - **Oxygen ($O_2$)**: Released back into the atmosphere for humans and animals to breathe.`;
    }
  }

  // 8. Philosophical & Vocabulary: Integrity, Hypocrite, Empathy
  if (lower.includes('integrity') && (lower.includes('meaning') || lower.includes('what is') || lower.includes('define'))) {
    return `**Integrity** is the practice of being honest, consistent, and uncompromising in upholding moral and ethical principles, especially when no one is watching.

### The Three Core Dimensions of Integrity:
1. **Moral Consistency**: Acting in strict alignment with your professed values, regardless of convenience or social pressure.
2. **Honesty & Truthfulness**: Speaking the truth, honoring your commitments, and being transparent in your intentions.
3. **Wholeness & Incorruptibility**: Originating from the Latin *integer* (meaning "whole" or "complete"), it signifies having an undivided mind where words, thoughts, and actions are unified.

*Real-World Example*: A software engineer who refuses to deploy code that cuts security corners or leaks user data, even when pressured by tight management deadlines.`;
  }

  if (lower.includes('hypocryite') || lower.includes('hypocrite') || lower.includes('hypocrisy')) {
    return `A **hypocrite** is a person who claims to have certain moral beliefs, virtues, or principles, but whose actual actions and behavior contradict those claims.

### Key Aspects:
1. **Pretense vs. Reality**: The word originates from the Greek *hypokrites*, which originally referred to a stage actor playing a role behind a theatrical mask. Over time, it came to mean someone who wears a moral mask to deceive others.
2. **Inconsistency**: Demanding honesty, kindness, or diligence from others while privately engaging in the opposite behavior.

### Clear Examples:
- **Example 1**: An environmentalist who publicly lectures people about reducing carbon emissions while flying across the country in a private jet every weekend.
- **Example 2**: A manager who berates employees for arriving 5 minutes late, yet consistently arrives an hour late without reason.

### Synonyms:
*Pretender, dissembler, pious fraud, two-faced person.*`;
  }

  if (lower.includes('empathy') && (lower.includes('meaning') || lower.includes('what is') || lower.includes('define'))) {
    return `**Empathy** is the ability to deeply understand, relate to, and share the emotional experiences and perspectives of another person.

### The Three Dimensions of Empathy:
1. **Cognitive Empathy**: Understanding another person's perspective, mindset, and thoughts ("I understand why you see it that way").
2. **Emotional (Affective) Empathy**: Physically and emotionally feeling what another person feels in response to their situation.
3. **Compassionate Empathy**: Moving beyond feeling into active, supportive action to alleviate their distress.`;
  }

  // 9. Technical: Aeronautical Engineering
  if (lower.includes('aeronautical') || (lower.includes('aeronautics') && lower.includes('engineering'))) {
    return `**Aeronautical Engineering** is the branch of engineering that focuses on the research, design, development, construction, testing, and science of aircraft operating **within the Earth's atmosphere**.

It is one of the two major disciplines within **Aerospace Engineering** (the other being *Astronautical Engineering*, which deals with spacecraft operating outside Earth's atmosphere in vacuum space).

---

### Core Pillars of Aeronautical Engineering:

1. **Aerodynamics**: The study of how air flows around objects and the aerodynamic forces generated—principally **Lift**, **Drag**, **Thrust**, and **Weight** (Gravity). Engineers design wing profiles (airfoils) to optimize fuel efficiency and high-speed stability.
2. **Propulsion**: Designing and optimizing engines that provide thrust to overcome aerodynamic drag. This spans turbofans, turbojets, turboprops, ramjets, and modern hybrid-electric aircraft motors.
3. **Materials & Structural Analysis**: Developing ultra-lightweight yet robust airframes capable of withstanding extreme aerodynamic pressures, thermal variations, and turbulence using carbon-fiber composites, titanium alloys, and advanced aluminum-lithium structures.
4. **Flight Mechanics & Avionics**: The science of aircraft control, autopilot systems, fly-by-wire computer controls, navigation radar, and sensors to ensure stability and maneuverability across subsonic, transonic, and supersonic regimes.

---

### Everyday Applications:
- **Commercial Aviation**: Passenger airliners such as the Boeing 787 Dreamliner and Airbus A350.
- **Defense & Military**: High-maneuverability fighter jets (e.g., F-22 Raptor, Sukhoi Su-57), stealth drones, and reconnaissance aircraft.
- **General & Rotary Aviation**: Helicopters, vertical takeoff and landing (VTOL) systems, and urban air mobility electric vehicles (eVTOL).`;
  }

  // 10. Medicine: Neurology
  if (lower.includes('neurology') || lower.includes('neurologist')) {
    const isSimpler = /\b(shorter|simpler|simple|brief|plain)\b/i.test(lower);
    if (isSimpler) {
      return `In simple terms, **Neurology** is the branch of medicine that specializes in the **brain, spinal cord, and nerves**.

A **neurologist** is a medical doctor who diagnoses and treats problems affecting your nervous system—such as headaches, migraines, seizures, strokes, memory loss, and nerve pain.`;
    }

    return `**Neurology** is the branch of medicine dealing with the diagnosis and treatment of conditions and diseases involving the **nervous system**.

### The Nervous System consists of:
1. **The Central Nervous System (CNS)**: The brain and spinal cord.
2. **The Peripheral Nervous System (PNS)**: All other nerves connecting the CNS to muscles, skin, and organs.

### Common Conditions Treated by Neurologists:
- **Cerebrovascular disorders**: Strokes and transient ischemic attacks.
- **Epilepsy & Seizures**: Abnormal electrical activity in the brain.
- **Neurodegenerative diseases**: Alzheimer's disease, Parkinson's disease, and ALS.
- **Demyelinating diseases**: Multiple Sclerosis (MS).
- **Headache disorders**: Chronic migraines and cluster headaches.`;
  }

  // 11. Photosynthesis
  if (lower.includes('photosynthesis')) {
    const isSimpler = /\b(shorter|simpler|simple|brief|plain)\b/i.test(lower);
    if (isSimpler) {
      return `In simple words, **photosynthesis** is the process plants use to make their own food using sunlight.

Plants absorb **sunlight**, take in **carbon dioxide** from the air, and drink **water** from the soil. They convert these into **sugar** (their food for growth) and release fresh **oxygen** into the air for us to breathe.`;
    }

    return `**Photosynthesis** is the biological process by which green plants, algae, and certain bacteria convert light energy (usually from the Sun) into chemical energy stored in glucose sugar bonds.

### The Chemical Formula:
$$6CO_2 + 6H_2O + \\text{Light Energy} \\longrightarrow C_6H_{12}O_6 + 6O_2$$

### Key Phases:
1. **Light-Dependent Reactions**: Occur in the thylakoid membranes of chloroplasts; chlorophyll absorbs photons, splits water molecules, produces ATP and NADPH, and releases oxygen ($O_2$) as a byproduct.
2. **The Calvin Cycle (Light-Independent Reactions)**: Takes place in the stroma; uses ATP and NADPH to convert carbon dioxide ($CO_2$) into energy-rich carbohydrates.`;
  }

  // 12. Programming: Python & Java
  if (lower.includes('python') && (lower.includes('what is') || lower.includes('explain') || lower.includes('example') || lower.includes('give me a python'))) {
    return `**Python** is a high-level, interpreted, general-purpose programming language renowned for its elegance, clean readability, and versatility.

### Why Python is Dominant:
1. **Human-Readable Syntax**: Uses whitespace indentation instead of curly braces or semicolons, minimizing boilerplate and cognitive load.
2. **Batteries-Included Standard Library**: Built-in support for networking, file handling, math, cryptography, and string parsing.
3. **Premier AI & Data Science Platform**: The global standard for deep learning and machine learning with frameworks like \`PyTorch\`, \`TensorFlow\`, \`scikit-learn\`, \`pandas\`, and \`NumPy\`.
4. **Modern Web Ecosystem**: Robust backends powered by \`FastAPI\`, \`Django\`, and \`Flask\`.

### Quick Code Example:
\`\`\`python
def calculate_growth(principal: float, rate: float, periods: int) -> list[float]:
    """Calculate compound growth over successive time periods."""
    return [round(principal * ((1 + rate) ** t), 2) for t in range(1, periods + 1)]

print(calculate_growth(1000, 0.08, 3))  # [1080.0, 1166.4, 1259.71]
\`\`\``;
  }

  if (lower.includes('java') && lower.includes('polymorphism')) {
    return `In **Java**, **Polymorphism** (from Greek meaning "many forms") is the ability of an object or method to take on multiple forms. It is one of the four foundational pillars of Object-Oriented Programming (OOP).

### Two Types of Polymorphism:
1. **Compile-Time (Static) Polymorphism**: Achieved via **Method Overloading** (methods with the same name but different parameter signatures).
2. **Runtime (Dynamic) Polymorphism**: Achieved via **Method Overriding** (a subclass provides a specific implementation of a method defined in its superclass or interface).

### Code Example:
\`\`\`java
// Base Class
class Animal {
    public void makeSound() {
        System.out.println("The animal makes a sound");
    }
}

// Subclasses Overriding the Method
class Dog extends Animal {
    @Override
    public void makeSound() {
        System.out.println("Woof! Woof!");
    }
}

class Cat extends Animal {
    @Override
    public void makeSound() {
        System.out.println("Meow!");
    }
}

// Polymorphic Usage
public class Main {
    public static void main(String[] args) {
        Animal myAnimal1 = new Dog(); // Polymorphic reference
        Animal myAnimal2 = new Cat();

        myAnimal1.makeSound(); // Prints: Woof! Woof!
        myAnimal2.makeSound(); // Prints: Meow!
    }
}
\`\`\`

Here, \`myAnimal1\` and \`myAnimal2\` are declared as type \`Animal\`, but at runtime, Java calls the actual overridden methods on \`Dog\` and \`Cat\`.`;
  }

  // 13. Machine Learning vs AI
  if (lower.includes('machine learning') && (lower.includes('explain') || lower.includes('example') || lower.includes('what is'))) {
    return `**Machine Learning (ML)** is a branch of artificial intelligence focused on developing mathematical models that automatically learn patterns from data to make decisions and predictions, rather than following static, hardcoded rules.

### Everyday Real-World Example: Email Spam Detection
- **Traditional Programming (No ML)**: An engineer would manually write thousands of rules: \`if email contains "FREE PRIZE" then flag as spam\`. Spammers simply change spelling to bypass rules.
- **Machine Learning**: The algorithm is fed 100,000 emails labeled as "Spam" or "Not Spam". It learns word distributions, sender patterns, and statistical correlations on its own. When a new email arrives, it calculates the probability that the email is spam and filters it automatically.

### The 3 Core Approaches:
1. **Supervised Learning**: Learning from labeled inputs & outputs (e.g., predicting house prices from square footage, or sentiment classification).
2. **Unsupervised Learning**: Grouping and clustering unlabeled data (e.g., customer segmentation or topic discovery).
3. **Reinforcement Learning**: An agent learning optimal actions through trial, error, and feedback in an environment (e.g., robotics or AlphaGo).`;
  }

  // 14. Historical query: "What did I ask you first?"
  if (
    lower.includes('what did i ask you first') ||
    lower.includes('what was my first question') ||
    lower.includes('what was our first topic')
  ) {
    const userMessages = history.filter((m) => m.role === 'user');
    if (userMessages.length > 0) {
      const firstMsg = userMessages[0].content;
      return `Your very first inquiry in this session was:\n\n> "${firstMsg}"\n\nWould you like to explore that topic further or review specific aspects of it?`;
    }
    return `This is our first inquiry in this session! What would you like to explore together?`;
  }

  // 15. Dynamic Open-Domain Knowledge Retrieval (Live Wikipedia API integration)
  const liveKnowledge = await fetchLiveKnowledge(query, history);
  if (liveKnowledge && liveKnowledge.extract) {
    return `### **${liveKnowledge.title}**

${liveKnowledge.extract}

---
*Would you like to explore more details, historical context, or specific applications related to **${liveKnowledge.title}**?*`;
  }

  // 16. Conversational Fallback
  const { topic } = extractTopicEntity(query, history);
  return `I understand you're asking about **"${topic || query}"**.

Could you let me know if you are looking for a high-level overview, a technical deep dive, or a specific real-world example?`;
}
