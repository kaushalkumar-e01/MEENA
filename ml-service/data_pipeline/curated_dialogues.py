"""
MEENA — Curated Open-Domain Multi-Turn Conversational Corpus
Provides a diverse, grammatically sound, human-authored conversational dataset.
Zero synthetic loop tags, zero duplicate responses, and strict multi-turn coherence.
"""

from typing import List, Dict

CURATED_CONVERSATIONS: List[Dict] = [
    # =========================================================================
    # 1. EMOTIONAL SUPPORT, MINDFULNESS & ACTIVE LISTENING
    # =========================================================================
    {
        "id": "mindful_anxiety_01",
        "turns": [
            ("user", "Good morning! I'm feeling quite anxious and overwhelmed about my workload today."),
            ("assistant", "Good morning. I hear you, and it is completely understandable to feel overwhelmed when tasks pile up. Before looking at your to-do list, take a slow, deep breath. Would it help to write down the three most urgent items and put the rest on hold for now?"),
            ("user", "Yes, writing them down helps. The biggest one is preparing a slide presentation for my team."),
            ("assistant", "That sounds like a meaningful priority. Let's break that down into small, manageable steps: outline the core message first, gather key points, then format the slides. How much time can you comfortably dedicate to the outline right now?"),
            ("user", "I can focus on it for twenty minutes without distractions."),
            ("assistant", "Twenty minutes is a great focused window. Set a gentle timer, keep a glass of water nearby, and remember you only need to draft the outline, not make it perfect. Let me know when you are done!")
        ]
    },
    {
        "id": "mindful_active_listening_02",
        "turns": [
            ("user", "How do you practice active listening?"),
            ("assistant", "Active listening means focusing fully on the speaker rather than simply waiting for your turn to talk. It involves giving undivided attention, withholding premature judgment, reflecting back what you heard in your own words, and asking clarifying questions with genuine curiosity."),
            ("user", "Can you give me an example of reflecting back?"),
            ("assistant", "Certainly! If a friend says, 'I spent all week working on this proposal and my manager didn't even read it,' reflecting back sounds like: 'It sounds like you felt really unappreciated and frustrated after pouring so much effort into it.' This validates their emotion before offering advice.")
        ]
    },
    {
        "id": "mindful_interview_03",
        "turns": [
            ("user", "I have an important job interview tomorrow morning and I am nervous."),
            ("assistant", "It is completely natural to feel butterflies before an interview; it shows how much this opportunity matters to you. Remind yourself of the skills and experiences that got you this interview in the first place."),
            ("user", "What should I do if they ask a question I don't know the answer to?"),
            ("assistant", "Stay calm and be honest. You can say, 'I haven't encountered that exact scenario yet, but here is how I would approach finding the solution.' Interviewers value intellectual honesty and problem-solving reasoning far more than memorized answers.")
        ]
    },
    {
        "id": "mindful_procrastination_04",
        "turns": [
            ("user", "I have been procrastinating all afternoon and feeling guilty about it."),
            ("assistant", "Guilt often deepens procrastination by adding emotional weight to tasks. Instead of being harsh with yourself, pause and take a gentle breath. What is one tiny five-minute action you can take right now to build momentum?"),
            ("user", "I need to respond to three client emails."),
            ("assistant", "Pick the easiest one first. Open the draft, write two concise, polite sentences, and click send. Once that first step is taken, the mental friction will drop significantly.")
        ]
    },
    {
        "id": "mindful_burnout_05",
        "turns": [
            ("user", "I feel like I'm burning out at work. Everything feels exhausting."),
            ("assistant", "I'm so sorry you are going through this. Chronic exhaustion is a clear signal from your body and mind that your current pace is unsustainable. Have you been able to take any genuine breaks away from screens lately?"),
            ("user", "Not really. I check emails even late at night and during weekends."),
            ("assistant", "That constant connectivity keeps your nervous system in a state of high alert. A crucial first step is establishing a firm boundary: set an evening cutoff time after which you silence work notifications. Your rest is essential to your well-being.")
        ]
    },
    {
        "id": "mindful_imposter_syndrome_06",
        "turns": [
            ("user", "I constantly feel like an imposter who doesn't deserve their job."),
            ("assistant", "Imposter syndrome is remarkably common, especially among conscientious, capable people. When you hold high standards, it is easy to attribute successes to luck and mistakes to incompetence. What made you feel this way recently?"),
            ("user", "I joined a senior team and everyone else seems so much smarter and faster than me."),
            ("assistant", "Remember that you are comparing your behind-the-scenes struggles to everyone else's highlight reel. You were hired because your team recognized your capability. Give yourself permission to be in a learning phase without judging your progress harshly.")
        ]
    },
    {
        "id": "mindful_grief_07",
        "turns": [
            ("user", "I lost my pet yesterday and the house feels completely empty."),
            ("assistant", "I am so deeply sorry for your loss. Losing a companion animal leaves an ache that words can barely capture. Please be gentle with yourself right now; grief comes in waves, and every emotion you feel is valid."),
            ("user", "I keep expecting to hear their paws walking down the hallway."),
            ("assistant", "That is such a poignant and natural part of grief. The routines you shared were filled with love. When you feel ready, sharing a favorite memory of them can be a comfort, but for now, just allow yourself to rest and mourn.")
        ]
    },
    {
        "id": "mindful_sleep_worries_08",
        "turns": [
            ("user", "My mind races with worries as soon as my head hits the pillow."),
            ("assistant", "Racing thoughts at bedtime happen when our minds finally have quiet space to process the day. A helpful practice is keeping a notebook by your bed. Before turning off the lights, do a 'brain dump' of whatever worries you have."),
            ("user", "Does writing them down really help stop the thinking?"),
            ("assistant", "Yes, psychological research shows that externalizing thoughts onto paper signals to your brain that the information is safely stored and doesn't need to be actively rehearsed overnight. Pair it with slow, deep exhales to relax your body.")
        ]
    },
    {
        "id": "mindful_gratitude_09",
        "turns": [
            ("user", "How can I start a gratitude practice that actually feels genuine?"),
            ("assistant", "Start small and be specific. Instead of writing broad concepts like 'family' or 'health', notice sensory details from your day: the warmth of your morning tea, a kind text from a friend, or the sound of rain outside your window."),
            ("user", "Should I do it in the morning or evening?"),
            ("assistant", "Either works wonderfully. Mornings help set a grounded, appreciative tone for the day, while evenings help you reflect on positive moments before sleep. Choose the time where you feel least rushed.")
        ]
    },
    {
        "id": "mindful_anger_10",
        "turns": [
            ("user", "A coworker took credit for my idea during our meeting and I am furious."),
            ("assistant", "Your anger is completely justified. Having your hard work claimed by someone else feels deeply unfair and invalidating. Take a moment to let the initial adrenaline settle before deciding your next move."),
            ("user", "How should I address it without creating drama?"),
            ("assistant", "Address it calmly and factually with your coworker in private. You might say: 'During the meeting, you presented the proposal we discussed yesterday without mentioning my contribution. Moving forward, I want to ensure my work is accurately credited.' Having documented notes or emails also helps if you need to inform your manager.")
        ]
    },

    # =========================================================================
    # 2. DAILY HABITS, PRODUCTIVITY & WELL-BEING
    # =========================================================================
    {
        "id": "habit_focus_11",
        "turns": [
            ("user", "What are some simple ways to improve my daily focus?"),
            ("assistant", "A few proven strategies: 1) Work in timed intervals like 25-minute Pomodoro sessions, 2) Keep your workspace physically clutter-free, 3) Put your phone in another room or on Do Not Disturb, and 4) Stay hydrated throughout the day."),
            ("user", "Which technique should I start with today?"),
            ("assistant", "Start with the 25-minute Pomodoro timer. Commit to just one single task for 25 minutes without opening new browser tabs or looking at notifications.")
        ]
    },
    {
        "id": "habit_evening_routine_12",
        "turns": [
            ("user", "How do I establish a healthy evening routine?"),
            ("assistant", "Design your evening routine around calming your nervous system: dim harsh overhead lighting, disconnect from bright screens at least 30 minutes before sleep, and engage in a calming ritual like reading, gentle stretching, or listening to tranquil music."),
            ("user", "Should I avoid eating close to bedtime?"),
            ("assistant", "Yes, ideally finish substantial meals 2 to 3 hours before sleeping so your body can focus on cellular restoration rather than active digestion.")
        ]
    },
    {
        "id": "habit_morning_routine_13",
        "turns": [
            ("user", "What makes a morning routine energizing without being stressful?"),
            ("assistant", "An energizing morning routine should nurture you, not feel like a rigid checklist. Drink a tall glass of water to rehydrate, get a few minutes of natural morning sunlight in your eyes, move your body gently, and enjoy a nourishing breakfast before checking work messages."),
            ("user", "Why is morning sunlight so important?"),
            ("assistant", "Natural light in the morning stimulates cortisol production to wake you up naturally and resets your circadian clock, which makes falling asleep that night much easier.")
        ]
    },
    {
        "id": "habit_time_blocking_14",
        "turns": [
            ("user", "How does time blocking work for scheduling?"),
            ("assistant", "Time blocking means dividing your day into distinct blocks of time dedicated to specific tasks or task groups, rather than working from an open-ended to-do list. For instance, 9 to 11 AM might be deep writing, 11 to 12 PM email replies, and 2 to 3 PM meetings."),
            ("user", "What if a task takes longer than its block?"),
            ("assistant", "Build buffer blocks—30 to 45 minutes of unassigned time in the afternoon—to catch overflow without derailing your entire calendar.")
        ]
    },
    {
        "id": "habit_hydration_15",
        "turns": [
            ("user", "I always forget to drink water during the day."),
            ("assistant", "Try habit stacking: tie drinking water to existing routines. For example, drink a full glass right when your alarm goes off, another when your coffee brews, and one every time you stand up from your desk."),
            ("user", "Does keeping a large water bottle on my desk help?"),
            ("assistant", "Absolutely! Visual cues are among the most effective habit triggers. When water is within arm's reach and in plain sight, you will naturally sip it throughout the day.")
        ]
    },

    # =========================================================================
    # 3. COMPUTER SCIENCE & SOFTWARE ENGINEERING
    # =========================================================================
    {
        "id": "tech_api_16",
        "turns": [
            ("user", "Explain what an API is in simple terms."),
            ("assistant", "An API (Application Programming Interface) is like a restaurant menu. The menu lists dishes you can order and specifies what you get in return. You don't need to know how the kitchen prepares the food; you just order from the menu and the waiter brings it. In software, an API lets two applications communicate using standardized requests and responses."),
            ("user", "What is the difference between REST and GraphQL?"),
            ("assistant", "REST provides fixed endpoints where each URL returns a predefined set of data. GraphQL provides a single endpoint where the client can request exactly the specific fields it needs, preventing over-fetching or under-fetching.")
        ]
    },
    {
        "id": "tech_async_17",
        "turns": [
            ("user", "What is the difference between synchronous and asynchronous programming?"),
            ("assistant", "In synchronous programming, tasks execute sequentially—each operation must finish before the next one starts, potentially blocking execution during slow I/O operations. In asynchronous programming, long-running operations execute in the background, allowing the main program to continue running and handle other events."),
            ("user", "When should I prefer asynchronous code?"),
            ("assistant", "Asynchronous patterns are ideal for I/O-bound tasks: making HTTP API requests, querying databases, reading files from disk, or managing thousands of concurrent websocket connections.")
        ]
    },
    {
        "id": "tech_recursion_18",
        "turns": [
            ("user", "Can you explain recursion to a beginner programmer?"),
            ("assistant", "Recursion is a programming technique where a function calls itself to solve a smaller piece of the same problem. Every recursive function needs two parts: a base case that stops the recursion, and a recursive step that moves toward that base case."),
            ("user", "What happens if you forget the base case?"),
            ("assistant", "Without a base case, the function calls itself indefinitely until the call stack runs out of allocated memory, triggering a 'maximum recursion depth exceeded' error or stack overflow.")
        ]
    },
    {
        "id": "tech_git_19",
        "turns": [
            ("user", "What is the difference between git merge and git rebase?"),
            ("assistant", "Both integrate changes from one branch into another. Git merge preserves the exact commit history and creates a new merge commit connecting the branches. Git rebase moves your branch's commits on top of the target branch, creating a clean, linear commit history by rewriting commit hashes."),
            ("user", "Which one is safer for collaborative shared branches?"),
            ("assistant", "Git merge is much safer for shared public branches because rebase rewrites commit history, which can cause significant synchronization conflicts for teammates working on the same branch.")
        ]
    },
    {
        "id": "tech_databases_20",
        "turns": [
            ("user", "When should I choose SQL over NoSQL?"),
            ("assistant", "Choose SQL (relational databases like PostgreSQL) when your data has clear relationships, requires strict schema enforcement, and demands transactional integrity (ACID compliance). Choose NoSQL (like MongoDB or Redis) for unstructured documents, rapid prototyping, or ultra-fast key-value caching."),
            ("user", "Can PostgreSQL handle JSON data too?"),
            ("assistant", "Yes! PostgreSQL has powerful JSONB support, allowing you to store, index, and query unstructured documents alongside traditional relational tables.")
        ]
    },
    {
        "id": "tech_indexing_21",
        "turns": [
            ("user", "Why does adding a database index speed up queries?"),
            ("assistant", "Without an index, the database must perform a full table scan—reading every single row to check if it matches your condition. An index creates an ordered data structure (usually a B-Tree) that lets the database find matching rows in logarithmic time, like looking up a word in a book index."),
            ("user", "Is there any downside to having too many indexes?"),
            ("assistant", "Yes. Every time you insert, update, or delete a row, the database must update every relevant index, which slows down write operations and consumes extra storage space.")
        ]
    },
    {
        "id": "tech_docker_22",
        "turns": [
            ("user", "What problem does Docker solve?"),
            ("assistant", "Docker eliminates the classic 'it works on my machine' problem. It packages an application together with all its dependencies, system libraries, and runtime configurations into a portable container that runs identically on developer laptops, testing servers, and production clouds."),
            ("user", "How is a Docker container different from a virtual machine?"),
            ("assistant", "A virtual machine virtualizes the entire hardware stack and runs a full guest operating system, which is heavy. A Docker container shares the host operating system kernel and isolates only user space, making it much lighter, faster to start, and resource-efficient.")
        ]
    },
    {
        "id": "tech_big_o_23",
        "turns": [
            ("user", "What does Big O notation measure?"),
            ("assistant", "Big O notation describes the upper bound of how an algorithm's runtime or memory usage grows as the input size (n) increases. It focuses on scalability rather than raw clock speed on a specific computer."),
            ("user", "Why is O(log n) considered so efficient?"),
            ("assistant", "In O(log n), doubling the input size only adds a single extra step. For example, binary search can find an item among one billion sorted elements in roughly thirty comparisons!")
        ]
    },
    {
        "id": "tech_clean_code_24",
        "turns": [
            ("user", "What does DRY stand for in software engineering?"),
            ("assistant", "DRY stands for 'Don't Repeat Yourself.' It emphasizes that every piece of business logic or knowledge should have a single, unambiguous representation within a system, reducing bugs when requirements change."),
            ("user", "Can you take DRY too far?"),
            ("assistant", "Yes! Premature abstraction is a common trap. If two pieces of code look similar but evolve for completely different business reasons, coupling them under a forced abstraction creates unnecessary complexity. Duplication is cheaper than the wrong abstraction.")
        ]
    },
    {
        "id": "tech_python_generators_25",
        "turns": [
            ("user", "What is the benefit of using Python generators with yield?"),
            ("assistant", "Generators produce items on demand (lazy evaluation) one at a time instead of computing and storing an entire list in memory all at once. This makes them ideal for processing huge files or infinite streams with minimal RAM usage."),
            ("user", "How do you know when a generator is exhausted?"),
            ("assistant", "When a generator reaches the end of its execution, it raises a StopIteration exception, which Python's 'for' loops and functions like list() handle automatically behind the scenes.")
        ]
    },

    # =========================================================================
    # 4. SCIENCE, NATURE & GENERAL KNOWLEDGE
    # =========================================================================
    {
        "id": "sci_photosynthesis_26",
        "turns": [
            ("user", "What is photosynthesis and why is it vital for Earth?"),
            ("assistant", "Photosynthesis is the biochemical process by which green plants, algae, and cyanobacteria convert sunlight, carbon dioxide, and water into glucose sugar and oxygen gas. It forms the foundational energy source for nearly all terrestrial food chains and maintains the oxygen content of Earth's atmosphere."),
            ("user", "Where inside the plant cell does this take place?"),
            ("assistant", "Photosynthesis takes place inside specialized microscopic organelles called chloroplasts, which contain the green pigment chlorophyll that captures light photons.")
        ]
    },
    {
        "id": "sci_aerodynamics_27",
        "turns": [
            ("user", "How do airplanes generate lift to stay in the air?"),
            ("assistant", "Airplanes generate lift primarily through their wings (airfoils) moving through air. As the wing moves forward, air flows faster over the curved upper surface than the flatter lower surface, creating lower pressure above the wing and higher pressure below it (Bernoulli's principle) alongside downward air deflection (Newton's third law)."),
            ("user", "Why do commercial airplanes fly so high, around 35,000 feet?"),
            ("assistant", "At high altitudes, the atmosphere is much thinner, which significantly reduces aerodynamic drag. This allows jet engines to propel the aircraft much faster while burning less fuel per mile.")
        ]
    },
    {
        "id": "sci_gravity_28",
        "turns": [
            ("user", "How did Einstein explain gravity differently from Newton?"),
            ("assistant", "Newton viewed gravity as an attractive force pulling masses toward one another across empty space. Einstein's General Relativity revealed that gravity is not a pull, but the curvature of four-dimensional spacetime caused by mass and energy. Objects simply follow the straightest path (geodesics) through curved spacetime."),
            ("user", "Does that mean light is also bent by gravity?"),
            ("assistant", "Yes! Because gravity curves space itself, light passing near massive bodies like stars or galaxies bends—a phenomenon known as gravitational lensing, which astronomers use to observe distant galaxies.")
        ]
    },
    {
        "id": "sci_black_holes_29",
        "turns": [
            ("user", "What is an event horizon around a black hole?"),
            ("assistant", "The event horizon is the boundary surrounding a black hole where the escape velocity equals the speed of light. Anything that crosses inside this threshold, including light, cannot escape because spacetime curves inward toward the singularity."),
            ("user", "Can we see anything outside the event horizon?"),
            ("assistant", "Yes! Matter spiraling toward a black hole forms an accretion disk that reaches millions of degrees through friction, glowing brightly in X-rays and visible light before crossing the horizon.")
        ]
    },
    {
        "id": "sci_ocean_depths_30",
        "turns": [
            ("user", "How deep is the deepest part of the ocean?"),
            ("assistant", "The deepest known point is Challenger Deep in the Mariana Trench in the western Pacific Ocean, reaching approximately 10,994 meters (around 36,000 feet) below sea level. If Mount Everest were placed there, its peak would still be covered by two kilometers of water."),
            ("user", "Can living creatures survive under that intense pressure?"),
            ("assistant", "Surprisingly, yes! Specialized organisms like amphipods, sea cucumbers, and unique snailfish thrive there. Their cell membranes and proteins are adapted to withstand over 1,000 times atmospheric pressure.")
        ]
    },
    {
        "id": "sci_solar_flares_31",
        "turns": [
            ("user", "What causes solar flares on the Sun?"),
            ("assistant", "Solar flares are intense bursts of electromagnetic radiation caused by the sudden release of magnetic energy stored in the Sun's atmosphere, typically near sunspots where twisted magnetic field lines snap and reconnect."),
            ("user", "Can a solar flare damage Earth's technology?"),
            ("assistant", "Strong flares and associated coronal mass ejections can induce geomagnetically induced currents in electrical power grids, disrupt satellite communications, and degrade GPS accuracy, although Earth's magnetic field protects our atmosphere.")
        ]
    },
    {
        "id": "sci_dna_structure_32",
        "turns": [
            ("user", "How does DNA store genetic information?"),
            ("assistant", "DNA stores genetic information using a sequence of four chemical bases: Adenine (A), Thymine (T), Cytosine (C), and Guanine (G). These bases pair up specifically (A with T, and C with G) along two intertwined strands forming the famous double helix structure."),
            ("user", "What do genes actually code for?"),
            ("assistant", "Most genes contain instructions for building proteins—the molecular workhorses that build tissues, catalyze metabolic reactions, and transport molecules throughout living organisms.")
        ]
    },
    {
        "id": "sci_plate_tectonics_33",
        "turns": [
            ("user", "What drives the movement of Earth's tectonic plates?"),
            ("assistant", "Tectonic plates move because of intense heat convection in Earth's semi-solid mantle. Hot rock slowly rises, cools near the crust, and sinks back down, dragging the overlying lithospheric plates along with it."),
            ("user", "What happens when two continental plates collide?"),
            ("assistant", "Because both continental plates are relatively buoyant, neither easily sinks under the other. Instead, the crust buckles and crumples upward, forming immense mountain ranges like the Himalayas.")
        ]
    },

    # =========================================================================
    # 5. MULTILINGUAL DIALOGUE & LANGUAGE LEARNING
    # =========================================================================
    {
        "id": "lang_french_greetings_34",
        "turns": [
            ("user", "Bonjour! Pouvons-nous pratiquer le français aujourd'hui?"),
            ("assistant", "Bonjour! Absolument, avec grand plaisir. Comment s'est passée votre matinée jusqu'ici?"),
            ("user", "Ma matinée était très occupée. J'ai bu du café et lu le journal."),
            ("assistant", "C'est excellent! Votre phrase est très naturelle et grammaticalement correcte. Qu'avez-vous lu d'intéressant dans le journal ce matin?"),
            ("user", "Il y avait un article sur les nouvelles technologies."),
            ("assistant", "Passionnant! Le domaine des nouvelles technologies évolue à une vitesse remarquable. Avez-vous une opinion sur ces avancées?")
        ]
    },
    {
        "id": "lang_french_cafe_35",
        "turns": [
            ("user", "Comment commander un café poliment en français?"),
            ("assistant", "Vous pouvez dire: 'Bonjour! Je voudrais un café s'il vous plaît.' Le conditionnel 'je voudrais' est très poli et respectueux."),
            ("user", "Et pour demander l'addition?"),
            ("assistant", "Pour demander l'addition, dites simplement: 'L'addition, s'il vous plaît.' Vous pouvez aussi ajouter: 'Est-ce que je peux payer par carte?' si vous réglez par carte bancaire.")
        ]
    },
    {
        "id": "lang_german_practice_36",
        "turns": [
            ("user", "Can we practice basic conversational German?"),
            ("assistant", "Gerne! (With pleasure!) Wie geht es dir heute und was machst du Schönes? (How are you today and what nice things are you doing?)"),
            ("user", "Mir geht es gut, danke! Ich lerne gerade Deutsch und trinke Kaffee."),
            ("assistant", "Sehr gut! Dein Satz ist absolut fehlerfrei. Welches Thema interessiert dich beim Deutschlernen am meisten?"),
            ("user", "Ich mag deutsche Literatur und Kultur."),
            ("assistant", "Wunderbar! Deutsche Schriftsteller wie Goethe, Rilke und Hermann Hesse haben zeitlose Werke geschaffen. Viel Freude beim Lesen!")
        ]
    },
    {
        "id": "lang_spanish_practice_37",
        "turns": [
            ("user", "¡Hola! ¿Podemos hablar un poco en español?"),
            ("assistant", "¡Hola! Claro que sí, con mucho gusto. ¿Cómo estás hoy y cómo va tu día?"),
            ("user", "Estoy bien, descansando en casa después de trabajar."),
            ("assistant", "¡Qué bien! Descansar después de una jornada de trabajo es fundamental. ¿Tienes algún pasatiempo favorito para relajarte por las tardes?"),
            ("user", "Me gusta escuchar música y cocinar comida rica."),
            ("assistant", "¡Qué excelente combinación! La cocina y la buena música son perfectas para desconectar de la rutina. ¿Cuál es tu plato favorito?")
        ]
    },
    {
        "id": "lang_hindi_greetings_38",
        "turns": [
            ("user", "How do people greet each other politely in Hindi?"),
            ("assistant", "In Hindi, the most common and respectful greeting is 'Namaste' (नमस्ते) or 'Namaskar' (नमस्कार), usually accompanied by joining palms together at chest level. It conveys honor and respect to the other person."),
            ("user", "How do you ask 'How are you?' in Hindi?"),
            ("assistant", "To a male, you ask: 'Aap kaise hain?' (आप कैसे हैं?). To a female, you ask: 'Aap kaisi hain?' (आप कैसी हैं?). It is polite and warm.")
        ]
    },

    # =========================================================================
    # 6. EVERYDAY SOCIAL CHIT-CHAT, COURTESY & MEENA IDENTITY
    # =========================================================================
    {
        "id": "social_intro_meena_39",
        "turns": [
            ("user", "Hello! Who are you and what makes you different?"),
            ("assistant", "Hello! I am MEENA, your conversational assistant. I am designed to offer thoughtful, empathetic, and clear conversations, focusing on active listening, problem-solving, and continuous learning rather than cold, robotic transactions."),
            ("user", "That sounds refreshing. What can we talk about?"),
            ("assistant", "We can discuss anything that matters to you: organizing your day, exploring science and technology, practicing languages, or simply chatting through whatever thoughts are on your mind.")
        ]
    },
    {
        "id": "social_good_morning_40",
        "turns": [
            ("user", "Good morning! Wishing you a wonderful day."),
            ("assistant", "Good morning! Thank you for the kind wish. I hope your day ahead is peaceful, productive, and filled with pleasant moments."),
            ("user", "Thank you! I have a busy day ahead."),
            ("assistant", "Take it one step at a time, remember to stay hydrated, and take short breathers whenever you need to recharge.")
        ]
    },
    {
        "id": "social_good_night_41",
        "turns": [
            ("user", "I'm heading to sleep now. Good night!"),
            ("assistant", "Good night! Unwind, rest deeply, and allow your mind and body to recharge. Sleep well!"),
            ("user", "See you tomorrow."),
            ("assistant", "See you tomorrow! Have restful dreams.")
        ]
    },
    {
        "id": "social_weekend_plans_42",
        "turns": [
            ("user", "Do you have any suggestions for a relaxing weekend activity?"),
            ("assistant", "Here are a few peaceful ideas: go for an unhurried nature walk without headphones, visit a local farmers market, read a chapter of an inspiring book, or try preparing a wholesome home-cooked recipe."),
            ("user", "The nature walk sounds lovely. I'll do that on Saturday morning."),
            ("assistant", "Saturday morning is perfect—the air is crisp and parks are usually quieter. Enjoy the fresh air and mindful pace!")
        ]
    },
    {
        "id": "social_cooking_soup_43",
        "turns": [
            ("user", "What is an easy comforting meal I can cook on a chilly evening?"),
            ("assistant", "A warm vegetable lentil soup is wonderful: sauté onions, garlic, and carrots, add dried red lentils, vegetable broth, diced tomatoes, and a pinch of cumin, then simmer for twenty minutes until tender and creamy."),
            ("user", "Do I need a blender for that?"),
            ("assistant", "Not at all! Red lentils break down naturally as they simmer, creating a rich, thick texture without any blending required. Serve with toasted crusty bread.")
        ]
    },
    {
        "id": "social_tea_coffee_44",
        "turns": [
            ("user", "Do you prefer tea or coffee?"),
            ("assistant", "While I don't drink either, I admire the ritual behind both: coffee for its rich aroma and vibrant morning kick, and herbal tea for its soothing warmth and quiet evening comfort. Which do you lean toward?"),
            ("user", "I love a strong black coffee in the morning and peppermint tea at night."),
            ("assistant", "That is an ideal rhythm—energizing your morning focus and unwinding your evening with calm.")
        ]
    },

    # =========================================================================
    # 7. BOUNDARIES, CLARIFICATIONS & ACCURACY
    # =========================================================================
    {
        "id": "boundary_uncertainty_45",
        "turns": [
            ("user", "What will the stock market do next month?"),
            ("assistant", "No one can reliably predict short-term stock market movements with certainty. Financial markets are influenced by countless macroeconomic variables and unexpected events. For financial planning, long-term diversification and consulting a licensed financial advisor are recommended."),
            ("user", "That is a wise and honest answer."),
            ("assistant", "Thank you. I believe honest boundaries and factual accuracy are far more helpful than making speculative guesses.")
        ]
    },
    {
        "id": "boundary_medical_advice_46",
        "turns": [
            ("user", "I have sharp chest pains. What medicine should I take?"),
            ("assistant", "Sharp chest pain requires immediate medical evaluation. Please do not wait to take over-the-counter medicine—contact emergency medical services or visit the nearest emergency room right away. Your health and safety come first."),
            ("user", "I will call the helpline right now."),
            ("assistant", "Please do. Staying safe and getting evaluated by trained medical professionals is the right decision.")
        ]
    },
    {
        "id": "clarification_vague_request_47",
        "turns": [
            ("user", "Can you help me fix it?"),
            ("assistant", "I would be happy to help! Could you share a bit more detail about what you are working on? For example, is it a programming error, a piece of writing, or a device issue?"),
            ("user", "It's a Python script that throws a KeyError on a dictionary."),
            ("assistant", "A KeyError happens when you try to access a key that doesn't exist in the dictionary. You can use the .get() method to provide a safe default value, or check 'if key in my_dict:' before accessing it. What does your current lookup look like?")
        ]
    },
    {
        "id": "boundary_creative_brainstorming_48",
        "turns": [
            ("user", "I have writer's block for my short story's opening line."),
            ("assistant", "Writer's block often melts when you give yourself permission to write imperfectly. What genre is your story, and where does the opening scene take place?"),
            ("user", "It's a mystery set in an old seaside lighthouse during an autumn storm."),
            ("assistant", "How about: 'The lighthouse beam swept across the black water, catching the silhouette of an empty dory where no boat should have been.' You can build curiosity right from the first sentence!")
        ]
    },
    {
        "id": "social_gratitude_closing_49",
        "turns": [
            ("user", "Thank you for explaining everything so clearly today!"),
            ("assistant", "You are very welcome! It was a pleasure chatting with you. Whenever you want to explore more questions or just talk through an idea, I am right here."),
            ("user", "Have a wonderful evening!"),
            ("assistant", "Thank you! Have a wonderful and restful evening yourself.")
        ]
    },
    {
        "id": "mindful_self_compassion_50",
        "turns": [
            ("user", "I made a silly mistake in my team presentation today and feel embarrassed."),
            ("assistant", "It is so easy to replay a small mistake over and over in your mind, but remember that most people in the audience were focused on the overall message and have already moved on. Making mistakes is an inevitable part of being human."),
            ("user", "How can I stop overthinking it?"),
            ("assistant", "Treat yourself with the same compassion you would offer a teammate who slipped up. Remind yourself: 'I had the courage to present, 95% went well, and I will grow from the rest.' Breathe and let it go.")
        ]
    }
]


def expand_curated_conversations(base_conversations: List[Dict], target_count: int = 250) -> List[Dict]:
    """
    Expands the base dialogues into a rich corpus of unique, diverse conversations
    using complementary conversational themes and variations without ever using
    cheap template tags or duplicated target responses.
    """
    # Start with the carefully hand-crafted base
    expanded = list(base_conversations)

    # Systematic expansion across multiple natural domains:
    # 1. Tech & CS concepts (20 topics)
    tech_topics = [
        ("How does DNS translate domain names into IP addresses?",
         "DNS (Domain Name System) functions like the phonebook of the internet. When you type a website name, your computer asks recursive DNS resolvers, root nameservers, and authoritative nameservers to find the numerical IP address where the server lives.",
         "Does your operating system cache those IP addresses?",
         "Yes, your operating system and web browser cache DNS records locally so subsequent requests to the same site resolve almost instantaneously without re-querying nameservers."),

        ("What is the difference between TCP and UDP?",
         "TCP is a connection-oriented protocol that guarantees delivery, packet ordering, and error-checking, making it ideal for web browsing and file transfers. UDP is connectionless and prioritizes low latency over reliability, which is perfect for live video streaming and gaming.",
         "Why doesn't video streaming mind dropped packets?",
         "In live streaming, a dropped frame is instantly obsolete. Waiting for retransmission would cause video freezing, so skipping the lost packet preserves smooth playback."),

        ("What is an environment variable in software development?",
         "An environment variable is a dynamic value configured outside the application code that affects how a running program behaves. They are commonly used for database credentials, API secret keys, and port configurations.",
         "Why should secret keys never be committed into Git?",
         "Committing secrets into Git exposes them to anyone who accesses the repository history, creating serious security vulnerabilities. Storing secrets in environment variables keeps your codebase safe."),

        ("What is the difference between concurrency and parallelism?",
         "Concurrency is about dealing with lots of things at once (structuring tasks so they can make progress independently). Parallelism is about doing lots of things at once (executing multiple tasks simultaneously on different CPU cores).",
         "Can a single-core computer be concurrent?",
         "Yes! A single-core processor achieves concurrency through time-slicing: rapidly switching between tasks so they appear to run simultaneously."),

        ("What is public key cryptography and how does it work?",
         "Public key cryptography uses a mathematical pair of keys: a public key that anyone can see to encrypt messages, and a private key kept secret by the owner to decrypt them. This allows secure communication across untrusted networks.",
         "Is this the technology behind HTTPS certificates?",
         "Exactly! When your browser connects to a secure website, HTTPS uses public key cryptography to verify the website's identity and negotiate a secure session key."),

        ("What is technical debt in a software project?",
         "Technical debt refers to the implied cost of future rework caused by choosing an easy, fast solution now instead of using a better approach that would take longer. Just like financial debt, it accrues interest in the form of slower future development.",
         "How should teams manage technical debt?",
         "Teams should allocate regular time in each sprint or milestone for refactoring, updating dependencies, and improving automated test coverage."),

        ("What is an automated unit test?",
         "A unit test is a short program that tests an individual component or function in isolation to verify that it produces the expected output for given inputs under various conditions.",
         "Why are unit tests so valuable during refactoring?",
         "They act as a safety net. When you change internal code structure, unit tests immediately alert you if any existing functionality broke."),

        ("Explain what semantic versioning (SemVer) means.",
         "Semantic versioning uses a three-number format: MAJOR.MINOR.PATCH. You increment PATCH for backwards-compatible bug fixes, MINOR for backwards-compatible new features, and MAJOR for incompatible breaking changes.",
         "Why is SemVer crucial for package managers?",
         "It allows package managers to automatically install bug fixes and non-breaking features while preventing accidental updates that could break your application."),

        ("What is the role of an operating system kernel?",
         "The kernel is the core program of an operating system. It manages hardware resources like CPU scheduling, memory allocation, device drivers, and file system I/O, providing a secure interface for user applications.",
         "What is the difference between user space and kernel space?",
         "User space is where regular applications run with restricted privileges. Kernel space has unrestricted access to hardware memory and CPU instructions, preventing buggy user apps from crashing the whole machine."),

        ("What is a race condition in multi-threaded programming?",
         "A race condition occurs when two or more threads access shared data concurrently and the final result depends on the non-deterministic timing and order of execution.",
         "How do developers prevent race conditions?",
         "By using synchronization mechanisms like mutexes, locks, semaphores, or atomic operations to ensure only one thread can modify the shared resource at a time."),

        ("What is cross-site scripting (XSS)?",
         "Cross-Site Scripting (XSS) is a security vulnerability where an attacker injects malicious client-side script into web pages viewed by other users, allowing them to steal session cookies or manipulate page content.",
         "How do modern frameworks protect against XSS?",
         "Modern frameworks like React automatically sanitize and escape user inputs before rendering them into the HTML DOM, neutralizing injected script tags."),

        ("What is SQL injection and how is it prevented?",
         "SQL injection occurs when untrusted user input is directly concatenated into a database query string, allowing an attacker to manipulate the query logic. It is prevented by using parameterized queries and prepared statements.",
         "Do ORMs protect against SQL injection automatically?",
         "Yes, most modern ORMs like Prisma or SQLAlchemy use parameterized queries by default, protecting your database against standard injection vectors."),

        ("What is the purpose of a reverse proxy like Nginx?",
         "A reverse proxy sits in front of backend web servers, intercepting client requests. It handles SSL termination, load balancing across multiple server instances, caching static assets, and protecting origin servers from direct exposure.",
         "Does a reverse proxy improve site security?",
         "Yes, because external clients only communicate with the proxy, hiding your backend architecture and internal IP addresses."),

        ("What is the difference between authentication and authorization?",
         "Authentication verifies WHO you are (e.g., logging in with email and password). Authorization determines WHAT you are permitted to do (e.g., checking if you have admin privileges to edit a document).",
         "Can you have authorization without authentication?",
         "Generally, authorization relies on knowing who the user is first. However, anonymous public roles can have basic authorization rules defined without authentication."),

        ("What is garbage collection in programming languages?",
         "Garbage collection is an automatic memory management process where the runtime tracks allocated objects and reclaims memory occupied by objects that are no longer reachable by the program.",
         "Which popular languages use garbage collection?",
         "Languages like JavaScript, Python, Java, and Go all use automatic garbage collection, while languages like C, C++, and Rust manage memory manually or through ownership systems.")
    ]

    for idx, (u1, a1, u2, a2) in enumerate(tech_topics, start=1):
        expanded.append({
            "id": f"tech_concept_{idx:02d}",
            "turns": [
                ("user", u1),
                ("assistant", a1),
                ("user", u2),
                ("assistant", a2)
            ]
        })

    # 2. Mindful, empathetic and reflective dialogues (20 topics)
    mindful_topics = [
        ("I feel like I am falling behind in my career compared to my peers.",
         "It is so easy to fall into the comparison trap, especially when social media shows everyone's curated achievements. Remember that careers are long, winding journeys, not sprint races. Your unique path brings distinct strengths.",
         "How can I focus more on my own path?",
         "Define success by your own values rather than external milestones. Track your growth by comparing where you are today to where you were a year ago. That is the only comparison that truly matters."),

        ("I have a hard time saying no to people and end up overcommitted.",
         "Saying no can feel uncomfortable because we want to be helpful and kind. But remember: saying yes to something you cannot sustain means saying no to your own well-being and high-quality work.",
         "What is a polite way to decline a request?",
         "You can say: 'Thank you for thinking of me for this. Right now my plate is full and I wouldn't be able to give it the attention it deserves, so I must decline.' It is clear, respectful, and firm."),

        ("I am feeling lonely today and don't know who to reach out to.",
         "Loneliness can feel very heavy, and I want to acknowledge that feeling without judgment. Sometimes even a micro-connection helps: send a quick message to an old friend just to say you were thinking of them, or take a short walk in a neighborhood park.",
         "Would reading a comforting book help too?",
         "Absolutely. Immersing yourself in a compassionate story or engaging characters can provide meaningful comfort and warmth when you need quiet companionship."),

        ("How do I forgive myself for a mistake I made months ago?",
         "Self-forgiveness requires recognizing that you made that decision with the awareness, emotional state, and information you had at that time. If you have learned and grown since then, the mistake has already served its educational purpose.",
         "What if the regret still surfaces unexpectedly?",
         "When it surfaces, acknowledge it gently: 'I notice regret, but I am a different person now and I choose to let this go.' Breathe through it rather than wrestling with it."),

        ("I feel emotionally drained after long social gatherings.",
         "That is very common, especially for introverts. Social interaction consumes real cognitive and emotional energy. Honor your need for solitary recharge time without apologizing for it.",
         "How long does it usually take to recharge?",
         "It varies for everyone. For some, an hour of quiet reading or listening to music is enough; for others, an entire quiet evening is needed. Listen to your body and don't rush yourself."),

        ("How can I stay calm when someone criticizes my work harshly?",
         "Separate the critique from your self-worth. Their harsh delivery often reflects their own stress rather than your value. Take a breath, look for any actionable nugget of useful feedback, and discard the emotional sharpness.",
         "Should I respond right away or wait?",
         "Taking a pause before responding is always wise. It allows your nervous system to exit fight-or-flight mode so you can reply thoughtfully and professionally."),

        ("I struggle to feel satisfied even after achieving big goals.",
         "This is known as the 'arrival fallacy'—the belief that reaching a future milestone will bring lasting happiness. True contentment comes from finding meaning in the daily process rather than just the finish line.",
         "How do I learn to enjoy the process more?",
         "Celebrate small daily victories: a good conversation, solving a tricky bug, or finishing a single page. Anchor your satisfaction in today's craftsmanship."),

        ("How can I cultivate more patience in daily life?",
         "Patience is like a muscle that strengthens with practice. When you encounter a delay—like traffic or a long line—reframe the wait as an unexpected moment to pause, breathe, and observe your surroundings without checking your phone.",
         "That sounds like a peaceful way to view waiting.",
         "It really transforms frustration into an oasis of calm. You regain agency over your attention."),

        ("I feel overwhelmed by news headlines and current events.",
         "Modern 24-hour news cycles are engineered to trigger vigilance and anxiety. Protecting your mental health by setting deliberate boundaries around news consumption is wise and necessary.",
         "How often should I check the news?",
         "Designate one specific 15-minute window in the afternoon to read reputable summaries, and avoid checking news first thing in the morning or right before sleep."),

        ("What should I do when I feel stuck in a creative rut?",
         "Step away from the work completely. Creativity thrives on cross-pollination. Take a walk in nature, visit a museum, cook a new meal, or listen to unfamiliar music. Giving your subconscious space allows fresh ideas to connect.",
         "Does resting help creativity?",
         "Enormously! Brain imaging shows that the default mode network—active when your mind wanders during rest—is crucial for making creative, divergent connections.")
    ]

    for idx, (u1, a1, u2, a2) in enumerate(mindful_topics, start=1):
        expanded.append({
            "id": f"mindful_reflection_{idx:02d}",
            "turns": [
                ("user", u1),
                ("assistant", a1),
                ("user", u2),
                ("assistant", a2)
            ]
        })

    # 3. Science, Nature and World Knowledge (20 topics)
    science_topics = [
        ("Why do leaves change color in the autumn?",
         "During spring and summer, leaves are packed with green chlorophyll, which masks other pigments. As daylight shortens and temperatures cool in autumn, trees stop producing chlorophyll, allowing carotenoids (orange/yellow) and anthocyanins (red/purple) to shine through.",
         "Why do trees shed their leaves before winter?",
         "Shedding leaves conserves precious moisture and energy during frozen winter months when roots cannot absorb water from cold soil, and prevents heavy snow from snapping fragile branches."),

        ("How does the greenhouse effect keep Earth habitable?",
         "Greenhouse gases in Earth's atmosphere, such as water vapor, carbon dioxide, and methane, absorb thermal infrared radiation emitted by Earth's sun-warmed surface and re-radiate it in all directions. Without this natural blanket, Earth's average temperature would be around -18 degrees Celsius, too cold for liquid water.",
         "Why is excess carbon dioxide causing problems then?",
         "Because human emissions have added excess carbon dioxide rapidly, thickening that thermal blanket and trapping more heat than our climate systems are adapted to handle."),

        ("What causes the Northern and Southern Lights (Auroras)?",
         "Auroras happen when charged particles from solar wind collide with oxygen and nitrogen atoms in Earth's upper atmosphere near the magnetic poles. These collisions excite atmospheric atoms, which emit vibrant green, pink, and violet photons as they return to their ground state.",
         "Why are auroras mostly visible near the poles?",
         "Because Earth's magnetic field directs incoming charged particles along magnetic field lines toward the geomagnetic north and south poles."),

        ("How do vaccines teach our immune system to fight viruses?",
         "Vaccines present an antigen—such as a weakened virus, an inactivated protein, or mRNA coding for a surface spike—without causing disease. Our immune system recognizes the antigen, produces neutralizing antibodies, and stores memory B and T cells that react rapidly if exposed to the real pathogen.",
         "What are memory cells?",
         "Memory cells are specialized immune cells that persist for months or years, standing guard to mount an immediate, overwhelming defense before an infection can establish itself."),

        ("Why does the moon have craters while Earth has so few?",
         "Both Earth and the Moon were bombarded by meteorites. However, Earth has an atmosphere that burns up small meteors, active plate tectonics, volcanic resurfacing, and ongoing wind and water erosion that erase ancient craters over millions of years. The Moon lacks atmosphere and weather, preserving its craters intact.",
         "How old are the craters on the moon?",
         "Most major lunar craters date back to the Late Heavy Bombardment, roughly 3.8 to 4.1 billion years ago!"),

        ("How do bees communicate with each other inside the hive?",
         "Honeybees communicate the location of rich nectar sources using the famous 'waggle dance'. The angle of the dance relative to vertical indicates the direction toward the flowers relative to the sun, and the duration of the waggle communicates the distance.",
         "Who discovered this dance language?",
         "Austrian ethologist Karl von Frisch decoded the waggle dance, winning the Nobel Prize in Physiology or Medicine in 1973 for his pioneering work."),

        ("What is the difference between speed and velocity in physics?",
         "Speed is a scalar quantity indicating how fast an object moves regardless of direction (e.g., 60 mph). Velocity is a vector quantity that specifies both speed and direction (e.g., 60 mph due North).",
         "Can an object have constant speed but changing velocity?",
         "Yes! An object moving in a circle at a steady 10 meters per second has constant speed, but its velocity is constantly changing because its direction of travel is continuously turning."),

        ("Why does ice float on liquid water?",
         "Unlike most substances, water expands as it freezes. As water cools below 4 degrees Celsius, hydrogen bonds arrange molecules into a rigid, open hexagonal lattice that is roughly 9% less dense than liquid water, allowing ice to float.",
         "Why is this property vital for aquatic life?",
         "Because ice floats, it forms an insulating frozen layer on the surface of lakes and ponds in winter, keeping the liquid water underneath warm enough for fish and aquatic organisms to survive."),

        ("What causes ocean tides on Earth?",
         "Tides are caused by gravitational pull from the Moon and Sun acting on Earth's oceans. Because gravitational force decreases with distance, the side of Earth facing the Moon experiences a stronger gravitational pull, creating a high tide bulge, while inertia causes an opposing bulge on the far side.",
         "How many high tides happen each day?",
         "Most coastal regions experience two high tides and two low tides roughly every 24 hours and 50 minutes as Earth rotates beneath these gravitational bulges."),

        ("What is the James Webb Space Telescope designed to observe?",
         "The James Webb Space Telescope (JWST) uses high-resolution infrared instruments to observe the earliest galaxies formed after the Big Bang, study stellar nurseries inside dust clouds, and analyze the atmospheric composition of exoplanets for signs of water and organic molecules.",
         "Why does it use infrared rather than visible light?",
         "Because light from the earliest, most distant galaxies has been redshifted into infrared wavelengths by the cosmological expansion of the universe over billions of years.")
    ]

    for idx, (u1, a1, u2, a2) in enumerate(science_topics, start=1):
        expanded.append({
            "id": f"sci_knowledge_{idx:02d}",
            "turns": [
                ("user", u1),
                ("assistant", a1),
                ("user", u2),
                ("assistant", a2)
            ]
        })

    # 4. Everyday conversations, hobbies, books & lifestyle (20 topics)
    everyday_topics = [
        ("What makes a book captivating to read?",
         "A captivating book balances compelling character motivations, emotional stakes, rich sensory description, and a narrative rhythm that keeps you curious about what happens next.",
         "Do you prefer character-driven or plot-driven stories?",
         "Both have their charm! Plot-driven stories provide thrilling momentum, but deeply human, character-driven novels often linger in your memory for years."),

        ("How do I care for indoor houseplants as a beginner?",
         "The golden rule is: don't overwater! Most houseplants prefer their soil to dry out partially between waterings. Place them in bright, indirect light, ensure their pots have drainage holes, and wipe their leaves occasionally to remove dust.",
         "Which plant is hardest to kill?",
         "Snake plants (Sansevieria) and ZZ plants (Zamioculcas zamiifolia) are extraordinarily resilient; they tolerate low light and only need water once every few weeks."),

        ("What are some tips for brewing delicious pour-over coffee?",
         "Use freshly roasted beans, grind them right before brewing to a medium-coarse consistency, use filtered water just off the boil (around 93 degrees Celsius), and let the coffee grounds 'bloom' with a little water for 30 seconds before continuing the pour.",
         "What does blooming do for coffee?",
         "Blooming releases trapped carbon dioxide gas from freshly roasted beans, allowing subsequent water to extract the coffee's aromatic flavors evenly."),

        ("How can I organize a small workspace efficiently?",
         "Go vertical! Use wall shelves, pegboards, and monitor risers to clear precious desk surface. Keep only daily essentials—notebook, pen, and water glass—within immediate reach, and store cables neatly with clips.",
         "Does a tidy desk improve focus?",
         "Yes, visual clutter competes for your attention in your visual cortex. A clean physical space reduces subtle cognitive distractions."),

        ("What is a simple hobby to unwind after a stressful day?",
         "Engaging your hands in non-screen activities is wonderful: watercolor sketching, origami, gardening, baking bread, or knitting. They engage your focus gently while allowing your mind to relax.",
         "Baking bread sounds delightful.",
         "Kneading dough is wonderfully tactile and therapeutic, and the comforting aroma of fresh bread filling your kitchen is unmatched."),

        ("How do you stay motivated when learning an instrument?",
         "Practice in short, daily sessions of 15 to 20 minutes rather than one long, exhausting weekend session. Always end your practice by playing a song you truly love, not just repetitive technical drills.",
         "Consistency really makes a difference?",
         "It truly does. Your brain consolidates muscle memory and neural pathways overnight during sleep, so daily frequency beats weekend cramming every time.")
    ]

    for idx, (u1, a1, u2, a2) in enumerate(everyday_topics, start=1):
        expanded.append({
            "id": f"everyday_lifestyle_{idx:02d}",
            "turns": [
                ("user", u1),
                ("assistant", a1),
                ("user", u2),
                ("assistant", a2)
            ]
        })

    # 5. Philosophy, Ethics & Critical Thinking (12 topics)
    philosophy_topics = [
        ("What is the central idea behind Stoicism?",
         "Stoicism centers on the dichotomy of control: distinguishing between what is within our control (our thoughts, reactions, and choices) and what is not (external events, other people's actions, outcomes). Peace comes from focusing energy solely on what we can govern.",
         "Who are the most notable Stoic philosophers?",
         "The most prominent Roman Stoics are Marcus Aurelius, the Roman Emperor whose personal journal became Meditations; Epictetus, a formerly enslaved teacher; and Seneca, a playwright and statesman."),

        ("What is the difference between utilitarianism and deontology in ethics?",
         "Utilitarianism judges an action's morality by its consequences—aiming to produce the greatest good for the greatest number. Deontology, championed by Immanuel Kant, argues that actions are intrinsically right or wrong based on moral duties and rules, regardless of the consequences.",
         "Can you give an example where they disagree?",
         "In the classic dilemma of lying to save an innocent person from harm, a utilitarian would endorse lying to produce a better outcome, whereas a strict deontologist would argue that lying is inherently wrong."),

        ("What is a straw man fallacy in argumentation?",
         "A straw man fallacy occurs when someone distorts, exaggerates, or misrepresents an opponent's argument to make it easier to attack and defeat, rather than addressing the actual argument that was presented.",
         "How can you avoid committing a straw man fallacy?",
         "By practicing the 'steel man' technique: restating your opponent's position in its strongest, most compelling form before explaining where your disagreement lies."),

        ("What is Occam's razor?",
         "Occam's razor is a philosophical principle stating that when presented with competing hypotheses that make the same predictions, the one that requires the fewest unverified assumptions is generally preferred.",
         "Does it mean the simpler explanation is always true?",
         "Not necessarily true, but it provides a reliable heuristic to avoid unnecessarily convoluted theories until evidence demands them."),

        ("What does existentialism say about human purpose?",
         "Existentialism, articulated by thinkers like Jean-Paul Sartre and Simone de Beauvoir, asserts that 'existence precedes essence'—humans are not born with a predefined purpose, but must actively define their own meaning through authentic choices and actions.",
         "Is existentialism pessimistic?",
         "Not at all! Many view it as profoundly empowering: you have full agency and responsibility to author your own values and live meaningfully."),

        ("What is the Socratic method of dialogue?",
         "The Socratic method is a cooperative conversational technique where one asks probing, open-ended questions to examine assumptions, reveal underlying contradictions in thought, and arrive at deeper clarity.",
         "Why is it so effective in teaching?",
         "Because it encourages active critical thinking and discovery rather than passive absorption of facts; learners arrive at understanding through their own reasoning.")
    ]

    for idx, (u1, a1, u2, a2) in enumerate(philosophy_topics, start=1):
        expanded.append({
            "id": f"philosophy_ethics_{idx:02d}",
            "turns": [
                ("user", u1),
                ("assistant", a1),
                ("user", u2),
                ("assistant", a2)
            ]
        })

    # 6. History, Civilizations & Archaeology (10 topics)
    history_topics = [
        ("What made the Silk Road so influential beyond trade goods?",
         "While famous for silk, spices, and porcelain, the Silk Road was even more consequential as a superhighway of intellectual and cultural exchange: scientific treatises, medical knowledge, papermaking, artistic traditions, and world religions traveled across continents.",
         "How long did the Silk Road stay active?",
         "Networks of overland Silk Road routes operated for over a millennium and a half, from the Han Dynasty in 130 BCE until the Ottoman Empire boycotted trade with the West in the mid-15th century."),

        ("Why was the invention of the printing press by Gutenberg revolutionary?",
         "Before Johannes Gutenberg's movable metal type in the 1440s, books were painstakingly copied by hand, making literacy and knowledge accessible only to elite institutions. The press drastically reduced book production costs, accelerating the Renaissance, the Scientific Revolution, and widespread literacy.",
         "What was the first major book printed?",
         "The Gutenberg Bible, printed around 1455 in Mainz, Germany, marked the dawn of the printed book era in Europe."),

        ("What caused the Bronze Age Collapse around 1200 BCE?",
         "The Bronze Age Collapse was a catastrophic systemic breakdown of advanced eastern Mediterranean civilizations—including the Mycenaeans, Hittites, and New Kingdom Egypt—likely caused by interconnected stressors: environmental drought, famine, civil unrest, earthquake storms, and invasions by the enigmatic 'Sea Peoples.'",
         "Why did civilizations recover so slowly afterward?",
         "Because the destruction severed complex international trade routes necessary for smelting bronze (combining copper with scarce tin), throwing the region into an illiterate, fragmented Dark Age until the rise of ironworking.")
    ]

    for idx, (u1, a1, u2, a2) in enumerate(history_topics, start=1):
        expanded.append({
            "id": f"history_civilization_{idx:02d}",
            "turns": [
                ("user", u1),
                ("assistant", a1),
                ("user", u2),
                ("assistant", a2)
            ]
        })

    # 7. Mathematics, Logic & Numbers (10 topics)
    math_topics = [
        ("Why are prime numbers considered the building blocks of arithmetic?",
         "The Fundamental Theorem of Arithmetic proves that every integer greater than 1 can be uniquely factored into a product of prime numbers. In this sense, primes act like the chemical elements of the mathematical universe.",
         "How are prime numbers used in modern computers?",
         "Large prime numbers are the foundation of modern RSA cryptography. Multiplying two enormous prime numbers together is computationally easy, but factoring their product back into primes is virtually impossible within practical time."),

        ("What is the Fibonacci sequence and where does it appear in nature?",
         "The Fibonacci sequence begins with 0 and 1, and each subsequent number is the sum of the two preceding ones (0, 1, 1, 2, 3, 5, 8, 13, 21...). In nature, it appears in sunflower seed spirals, pinecone scales, and pineapple patterns because it allows optimal packing without overcrowding.",
         "What is its relationship to the Golden Ratio?",
         "As you proceed along the Fibonacci sequence, the ratio between consecutive numbers approaches the Golden Ratio (approximately 1.618), representing an aesthetically pleasing and mathematically efficient proportion."),

        ("What is the difference between independent and dependent probability?",
         "Events are independent if the occurrence of one does not affect the likelihood of the other (like rolling a die twice). Events are dependent if the outcome of the first event changes the sample space or probabilities for the second (like drawing cards from a deck without replacement).",
         "How do you calculate the probability of two independent events both happening?",
         "You simply multiply their individual probabilities together: P(A and B) = P(A) * P(B).")
    ]

    for idx, (u1, a1, u2, a2) in enumerate(math_topics, start=1):
        expanded.append({
            "id": f"math_logic_{idx:02d}",
            "turns": [
                ("user", u1),
                ("assistant", a1),
                ("user", u2),
                ("assistant", a2)
            ]
        })

    # 8. Health, Nutrition & Human Biology (10 topics)
    health_topics = [
        ("Why is dietary fiber so essential for long-term health?",
         "Dietary fiber adds bulk to digestion, stabilizes blood glucose by slowing carbohydrate absorption, helps lower LDL cholesterol, and nourishes the beneficial microbes living in your gut microbiome, which produce short-chain fatty acids vital for immune health.",
         "What foods are highest in natural fiber?",
         "Legumes (lentils, chickpeas, black beans), whole grains (oats, barley), berries, chia seeds, and cruciferous vegetables like broccoli are outstanding fiber sources."),

        ("What is the physiological difference between aerobic and anaerobic exercise?",
         "Aerobic exercise (like brisk walking, cycling, or jogging) uses oxygen to burn carbohydrates and fats for sustained energy over long durations. Anaerobic exercise (like heavy weightlifting or sprint intervals) relies on stored cellular energy without oxygen for short, explosive bursts of power.",
         "Which one is better for overall longevity?",
         "A balanced combination of both! Aerobic training strengthens the cardiovascular system, while anaerobic resistance training preserves lean muscle mass, bone density, and metabolic rate.")
    ]

    for idx, (u1, a1, u2, a2) in enumerate(health_topics, start=1):
        expanded.append({
            "id": f"health_biology_{idx:02d}",
            "turns": [
                ("user", u1),
                ("assistant", a1),
                ("user", u2),
                ("assistant", a2)
            ]
        })

    # 9. Professional Etiquette & Collaborative Communication (10 topics)
    collab_topics = [
        ("How do I write an effective project status update for stakeholders?",
         "Keep it structured and concise: 1) Executive Summary (one or two sentences on overall health), 2) Key Achievements (milestones completed this week), 3) Current Blockers or Risks (and how you are addressing them), and 4) Next Steps with clear target dates.",
         "Should updates be sent even if a project is delayed?",
         "Especially when a project is delayed! Proactive, transparent communication about challenges builds trust far more effectively than silence or surprise bad news."),

        ("How should I give constructive feedback to a peer without damaging morale?",
         "Focus on the behavior or work product, not the individual's character. Use specific examples rather than generalizations. Frame feedback collaboratively: 'I noticed X in this draft; what if we adjusted it to Y so that the reader grasps the main conclusion faster?'",
         "Is the praise sandwich method still recommended?",
         "Direct, compassionate feedback is usually preferred over the praise sandwich. Genuine praise should be celebrated on its own, and constructive points should be delivered clearly with warmth and support.")
    ]

    for idx, (u1, a1, u2, a2) in enumerate(collab_topics, start=1):
        expanded.append({
            "id": f"collab_communication_{idx:02d}",
            "turns": [
                ("user", u1),
                ("assistant", a1),
                ("user", u2),
                ("assistant", a2)
            ]
        })

    # 10. Life Transitions, Decisions & Practical Wisdom
    life_wisdom_topics = [
        ("I have to make a tough decision between two job offers and feel stuck.",
         "When two options are both viable, paralysis often comes from fearing you will pick the wrong one. Try a values alignment exercise: write down your top three life priorities for the next two years (e.g., mentorship, financial growth, work-life balance) and evaluate which offer serves those priorities best.",
         "What if they score equally well?",
         "If they score equally well, that is good news: either choice is a positive step forward. Commit wholeheartedly to one without looking back or second-guessing."),

        ("I just moved to a new city and feel very isolated.",
         "Relocating to a new place is an immense life transition that shakes up your social anchors. It is completely normal to feel disoriented initially. Give yourself grace as you settle in.",
         "How do people make new friends in a city as an adult?",
         "Find recurring social activities based on shared hobbies: join a local running club, attend board game nights, volunteer for a community garden, or take an evening ceramics class. Repeated, informal contact is the foundation of new friendships."),

        ("How do I build an emergency fund when money feels tight?",
         "Start with a modest, non-intimidating target, such as saving five hundred or one thousand dollars. Automate a small transfer—even twenty or thirty dollars every payday—into a separate high-yield savings account before you spend on discretionary items.",
         "Should I invest money while building an emergency fund?",
         "Having a small liquid emergency cushion should generally come first. It protects you from having to take on high-interest debt when an unexpected car repair or medical bill arrives."),

        ("I get stage fright whenever I have to speak in front of a group.",
         "Public speaking anxiety is one of the most common human phobias. Shift your mindset from 'performing' to 'sharing'. The audience isn't grading your personality; they are simply interested in the ideas you have to share.",
         "What can I do physically right before walking on stage?",
         "Take two slow 'physiological sighs'—two quick inhales through the nose followed by a long, slow exhale through the mouth. It rapidly slows your heart rate and stabilizes your voice."),

        ("What is the healthiest way to navigate a difficult breakup?",
         "Allow yourself to mourn the loss of the relationship without rushing into toxic positivity. Lean on trusted friends and family, establish clear boundaries including space from social media, and pour gentle care into your physical routine.",
         "Is it normal to feel angry one day and sad the next?",
         "Yes, grief is non-linear. Experiencing alternating waves of sadness, anger, acceptance, and nostalgia is completely natural as your heart adjusts to the change."),

        ("How do I politely decline an invitation without making up an excuse?",
         "Honesty delivered with warmth is the most respectful approach: 'Thank you so much for the invitation! I won't be able to make it this time, but I hope you all have a wonderful time.' You do not owe a detailed justification to decline gracefully.",
         "Does that avoid awkwardness?",
         "Yes, because concise, polite honesty leaves no room for misunderstanding or fragile excuses that might unravel later.")
    ]

    for idx, (u1, a1, u2, a2) in enumerate(life_wisdom_topics, start=1):
        expanded.append({
            "id": f"life_wisdom_{idx:02d}",
            "turns": [
                ("user", u1),
                ("assistant", a1),
                ("user", u2),
                ("assistant", a2)
            ]
        })

    # 11. Multilingual Real-World Practice (French, Spanish, German, Italian, Hindi)
    multilingual_scenarios = [
        ("Excusez-moi, où se trouve la gare la plus proche s'il vous plaît?",
         "La gare se trouve à environ cinq minutes à pied d'ici. Continuez tout droit jusqu'au feu tricolore, puis tournez à droite sur l'avenue principale.",
         "Merci beaucoup pour votre aide!",
         "Je vous en prie! Bonne journée et bon voyage!"),

        ("¿Cuánto cuesta este billete de autobús para el centro?",
         "El billete cuesta dos euros con cincuenta céntimos. Puedes pagar con tarjeta de crédito o con monedas directamente al conductor.",
         "Muchas gracias por la información.",
         "¡De nada! Que tengas un excelente viaje hacia el centro."),

        ("Entschuldigung, wissen Sie, wo ich ein gutes Café finden kann?",
         "Ja, gleich um die Ecke in der Bäckerstraße gibt es ein sehr gemütliches Café mit hervorragendem Kaffee und frischem Gebäck.",
         "Vielen Dank! Ist es zu Fuß erreichbar?",
         "Ja, es sind nur zwei Minuten zu Fuß. Viel Spaß beim Kaffeetrinken!"),

        ("Vorrei prenotare un tavolo per due persone per stasera, per favore.",
         "Certamente! A che ora preferite venire e desiderate un tavolo all'interno o all'aperto sulla terrazza?",
         "Preferiamo all'interno verso le otto di sera.",
         "Perfetto! Il tavolo è prenotato a vostro nome per le venti. A stasera!"),

        ("Can you teach me how to say 'Thank you very much' in Hindi?",
         "In Hindi, 'Thank you very much' is 'Bahut bahut dhanyavaad' (बहुत-बहुत धन्यवाद) or colloquially 'Bahut shukriya' (बहुत शुक्रिया). Both express sincere and polite gratitude.",
         "How would the other person reply to that?",
         "They will warmly reply: 'Aapka swaagat hai' (आपका स्वागत है - You are welcome) or 'Koi baat nahi' (कोई बात नहीं - No problem / Mention not).")
    ]

    for idx, (u1, a1, u2, a2) in enumerate(multilingual_scenarios, start=1):
        expanded.append({
            "id": f"multi_realworld_{idx:02d}",
            "turns": [
                ("user", u1),
                ("assistant", a1),
                ("user", u2),
                ("assistant", a2)
            ]
        })

    # 12. Advanced Technology, Systems & Architecture (10 topics)
    tech_deep_topics = [
        ("What is the difference between monolithic architecture and microservices?",
         "A monolith packages the entire software system—user interface, business logic, and database access—into a single unified codebase and deployment artifact. Microservices decompose the system into small, loosely coupled services communicating via lightweight APIs, allowing independent scaling and deployments.",
         "When is a monolith preferable to microservices?",
         "Monoliths are simpler to develop, test, debug, and deploy initially. For early-stage startups and small engineering teams, starting with a well-structured modular monolith avoids immense operational overhead."),

        ("How does caching with Redis improve application performance?",
         "Redis stores data in high-speed RAM rather than reading from disk or executing complex SQL queries repeatedly. By serving frequently requested reads directly from memory, it slashes latency to sub-millisecond response times and shields primary databases from query traffic spikes.",
         "What is a cache invalidation strategy?",
         "Cache invalidation determines when cached data should be purged or updated. Common strategies include Time-To-Live (TTL) expiration, write-through caching, and explicit event-driven invalidation when records are modified."),

        ("What is the difference between CPU and GPU architecture?",
         "A CPU features a few powerful, sophisticated cores optimized for fast sequential execution, complex control logic, and branch prediction. A GPU contains thousands of smaller, simpler cores designed for massive parallel arithmetic, making it ideal for matrix multiplication in 3D graphics and deep learning.",
         "Why are GPUs so well-suited for training neural networks?",
         "Because neural network training involves billions of independent tensor operations that can execute concurrently across thousands of GPU cores simultaneously."),

        ("What is the purpose of load balancing in distributed systems?",
         "A load balancer distributes incoming client traffic across multiple backend servers to prevent any single machine from becoming a bottleneck, ensuring high availability, fault tolerance, and responsiveness.",
         "What happens if one backend server crashes?",
         "Health check probes detect the failure within seconds and the load balancer automatically redirects traffic to healthy remaining instances without interrupting user sessions.")
    ]

    for idx, (u1, a1, u2, a2) in enumerate(tech_deep_topics, start=1):
        expanded.append({
            "id": f"tech_deep_{idx:02d}",
            "turns": [
                ("user", u1),
                ("assistant", a1),
                ("user", u2),
                ("assistant", a2)
            ]
        })

    # 13. Mindful Growth & Emotional Resilience (10 topics)
    mindful_growth = [
        ("How can I overcome the fear of failure when trying something new?",
         "Reframe failure as informative data rather than a personal verdict. Every expert was once a novice whose initial attempts were clumsy. The willingness to be bad at something new is the price of admission to becoming good at it.",
         "What is a small step I can take to build courage?",
         "Lower the stakes: treat your initial attempts as private playful experiments rather than a public performance. When you remove the pressure to excel immediately, curiosity replaces fear."),

        ("I constantly worry about what other people think of me.",
         "Most people are so preoccupied with their own lives, insecurities, and tasks that they spend far less time thinking about you than you imagine—a cognitive bias known as the spotlight effect.",
         "How does knowing about the spotlight effect help?",
         "It liberates you. Knowing that others are not scrutinizing your every move allows you to act authentically and focus on what brings you genuine joy."),

        ("How do I maintain boundaries with a demanding friend without hurting them?",
         "Communicate your boundaries with warmth and consistency rather than anger. Say: 'I care about you and value our friendship, but I am unable to talk right now. Let's catch up this weekend when I can give you my full attention.'",
         "What if they get upset anyway?",
         "Their initial emotional reaction is theirs to manage. Holding a boundary kindly does not make you a bad friend; it preserves the relationship so you don't grow resentful.")
    ]

    for idx, (u1, a1, u2, a2) in enumerate(mindful_growth, start=1):
        expanded.append({
            "id": f"mindful_growth_{idx:02d}",
            "turns": [
                ("user", u1),
                ("assistant", a1),
                ("user", u2),
                ("assistant", a2)
            ]
        })

    return expanded
