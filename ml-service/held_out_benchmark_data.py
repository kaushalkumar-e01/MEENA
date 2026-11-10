"""
MEENA — Held-Out Conversational Intelligence Benchmark (100 Prompts)

Completely held-out from the training set (0% overlap with train.jsonl).
Covers 10 diverse categories (10 prompts each = 100 total prompts).
Includes multi-turn dialogues with conversational context, paraphrases,
reasoning tasks, uncertainty tests, and foreign-language interactions.
"""

from typing import List, Dict, Any

HELD_OUT_BENCHMARK_PROMPTS: List[Dict[str, Any]] = [
    # =========================================================================
    # 1. GENERAL CONVERSATION (10 prompts)
    # =========================================================================
    {
        "id": "gen_01",
        "category": "general_conversation",
        "prompt": "Hello! I hope you are having a pleasant day.",
        "history": [],
        "expected_concepts": ["hello", "pleasant", "day", "thank", "hope", "well"],
        "notes": "Basic friendly greeting."
    },
    {
        "id": "gen_02",
        "category": "general_conversation",
        "prompt": "What kind of topics do you enjoy discussing the most?",
        "history": [],
        "expected_concepts": ["topics", "discuss", "science", "technology", "mindful", "chat"],
        "notes": "Open-domain capabilities check."
    },
    {
        "id": "gen_03",
        "category": "general_conversation",
        "prompt": "I finally finished reading an entire novel this weekend!",
        "history": [],
        "expected_concepts": ["novel", "read", "book", "congratulations", "story", "weekend"],
        "notes": "Positive milestone celebration."
    },
    {
        "id": "gen_04",
        "category": "general_conversation",
        "prompt": "It's raining softly outside and the air smells wonderful.",
        "history": [],
        "expected_concepts": ["rain", "cozy", "smell", "peaceful", "nature", "petrichor"],
        "notes": "Sensory reflection."
    },
    {
        "id": "gen_05",
        "category": "general_conversation",
        "prompt": "Do you have any advice for making long car rides more enjoyable?",
        "history": [],
        "expected_concepts": ["podcast", "music", "audiobook", "scenery", "snacks", "breaks"],
        "notes": "Travel tips."
    },
    {
        "id": "gen_06",
        "category": "general_conversation",
        "prompt": "I'm trying to decide between learning painting or pottery.",
        "history": [],
        "expected_concepts": ["painting", "pottery", "creative", "hands", "color", "tactile"],
        "notes": "Hobby trade-off."
    },
    {
        "id": "gen_07",
        "category": "general_conversation",
        "prompt": "What makes a cup of chamomile tea so relaxing before bed?",
        "history": [],
        "expected_concepts": ["chamomile", "tea", "sleep", "calming", "herbal", "soothing"],
        "notes": "Evening relaxation."
    },
    {
        "id": "gen_08",
        "category": "general_conversation",
        "prompt": "I am thinking about adopting a rescue cat from our local shelter.",
        "history": [],
        "expected_concepts": ["cat", "rescue", "shelter", "adopt", "companion", "care"],
        "notes": "Pet adoption reflection."
    },
    {
        "id": "gen_09",
        "category": "general_conversation",
        "prompt": "How do you define a true friendship?",
        "history": [],
        "expected_concepts": ["friendship", "trust", "support", "honesty", "loyalty", "care"],
        "notes": "Interpersonal philosophy."
    },
    {
        "id": "gen_10",
        "category": "general_conversation",
        "prompt": "Good evening! I'm ready to wrap up for the night.",
        "history": [],
        "expected_concepts": ["evening", "goodnight", "rest", "sleep", "unwind", "tomorrow"],
        "notes": "Parting pleasantry."
    },

    # =========================================================================
    # 2. EVERYDAY QUESTIONS (10 prompts)
    # =========================================================================
    {
        "id": "everyday_01",
        "category": "everyday_questions",
        "prompt": "How can I prevent freshly cut apple slices from turning brown?",
        "history": [],
        "expected_concepts": ["lemon", "juice", "acid", "oxidation", "water", "salt"],
        "notes": "Culinary chemistry."
    },
    {
        "id": "everyday_02",
        "category": "everyday_questions",
        "prompt": "What are some simple ways to reduce single-use plastic at home?",
        "history": [],
        "expected_concepts": ["reusable", "bags", "bottles", "containers", "plastic", "recycle"],
        "notes": "Sustainability tip."
    },
    {
        "id": "everyday_03",
        "category": "everyday_questions",
        "prompt": "Why is it important to wash new bed sheets before using them?",
        "history": [],
        "expected_concepts": ["wash", "sheets", "chemicals", "dust", "manufacturing", "soften"],
        "notes": "Household hygiene."
    },
    {
        "id": "everyday_04",
        "category": "everyday_questions",
        "prompt": "What is an easy recipe for homemade salad dressing?",
        "history": [],
        "expected_concepts": ["olive", "oil", "vinegar", "mustard", "lemon", "salt", "pepper"],
        "notes": "Cooking staple."
    },
    {
        "id": "everyday_05",
        "category": "everyday_questions",
        "prompt": "How often should I clean the lint filter on my clothes dryer?",
        "history": [],
        "expected_concepts": ["lint", "dryer", "filter", "clean", "every", "load", "fire"],
        "notes": "Home safety."
    },
    {
        "id": "everyday_06",
        "category": "everyday_questions",
        "prompt": "How can I remove coffee stains from a white cotton shirt?",
        "history": [],
        "expected_concepts": ["cold", "water", "detergent", "stain", "blot", "wash"],
        "notes": "Stain removal."
    },
    {
        "id": "everyday_07",
        "category": "everyday_questions",
        "prompt": "What is the difference between baking powder and baking soda?",
        "history": [],
        "expected_concepts": ["baking", "soda", "powder", "acid", "leavening", "chemical"],
        "notes": "Baking fundamentals."
    },
    {
        "id": "everyday_08",
        "category": "everyday_questions",
        "prompt": "How do I care for a wooden cutting board so it doesn't crack?",
        "history": [],
        "expected_concepts": ["mineral", "oil", "board", "wood", "handwash", "dry", "moisture"],
        "notes": "Kitchenware maintenance."
    },
    {
        "id": "everyday_09",
        "category": "everyday_questions",
        "prompt": "What are some high-protein snacks that don't need refrigeration?",
        "history": [],
        "expected_concepts": ["nuts", "seeds", "jerky", "chickpeas", "protein", "bars"],
        "notes": "Nutrition."
    },
    {
        "id": "everyday_10",
        "category": "everyday_questions",
        "prompt": "Why do onions make our eyes water when we chop them?",
        "history": [],
        "expected_concepts": ["sulfur", "compounds", "eyes", "tears", "syn-propanethial-s-oxide", "enzymes"],
        "notes": "Everyday science."
    },

    # =========================================================================
    # 3. COMPUTER SCIENCE & TECHNOLOGY (10 prompts)
    # =========================================================================
    {
        "id": "cs_01",
        "category": "computer_science_tech",
        "prompt": "What is the difference between a stack and a queue data structure?",
        "history": [],
        "expected_concepts": ["lifo", "fifo", "stack", "queue", "push", "pop", "enqueue"],
        "notes": "Fundamental data structures."
    },
    {
        "id": "cs_02",
        "category": "computer_science_tech",
        "prompt": "Why are hash tables able to achieve O(1) average lookup time?",
        "history": [],
        "expected_concepts": ["hash", "function", "array", "bucket", "index", "constant", "time"],
        "notes": "Algorithmic complexity."
    },
    {
        "id": "cs_03",
        "category": "computer_science_tech",
        "prompt": "What is an SQL foreign key and why does it matter?",
        "history": [],
        "expected_concepts": ["foreign", "key", "referential", "integrity", "table", "relation"],
        "notes": "Database design."
    },
    {
        "id": "cs_04",
        "category": "computer_science_tech",
        "prompt": "What is the purpose of a virtual DOM in libraries like React?",
        "history": [],
        "expected_concepts": ["virtual", "dom", "diffing", "reconciliation", "batch", "render"],
        "notes": "Frontend architecture."
    },
    {
        "id": "cs_05",
        "category": "computer_science_tech",
        "prompt": "Explain what a memory leak is in software.",
        "history": [],
        "expected_concepts": ["memory", "leak", "allocation", "garbage", "collection", "unreleased"],
        "notes": "Systems programming."
    },
    {
        "id": "cs_06",
        "category": "computer_science_tech",
        "prompt": "What is the difference between symmetric and asymmetric encryption?",
        "history": [],
        "expected_concepts": ["symmetric", "asymmetric", "private", "public", "key", "encrypt"],
        "notes": "Cybersecurity."
    },
    {
        "id": "cs_07",
        "category": "computer_science_tech",
        "prompt": "Why is immutability valued in functional programming?",
        "history": [],
        "expected_concepts": ["immutable", "state", "side-effects", "pure", "functions", "predictable"],
        "notes": "Programming paradigms."
    },
    {
        "id": "cs_08",
        "category": "computer_science_tech",
        "prompt": "What does continuous integration (CI) automate for developers?",
        "history": [],
        "expected_concepts": ["ci", "build", "test", "automation", "pipeline", "code", "merge"],
        "notes": "DevOps."
    },
    {
        "id": "cs_09",
        "category": "computer_science_tech",
        "prompt": "How does a CDN speed up website loading for global users?",
        "history": [],
        "expected_concepts": ["cdn", "cache", "edge", "server", "latency", "geographic", "assets"],
        "notes": "Web infrastructure."
    },
    {
        "id": "cs_10",
        "category": "computer_science_tech",
        "prompt": "What is the difference between compiled and interpreted languages?",
        "history": [],
        "expected_concepts": ["compiled", "interpreted", "machine", "code", "bytecode", "runtime"],
        "notes": "Compilers & interpreters."
    },

    # =========================================================================
    # 4. SCIENCE & EDUCATIONAL EXPLANATIONS (10 prompts)
    # =========================================================================
    {
        "id": "sci_01",
        "category": "science_education",
        "prompt": "Why does the sky appear blue on a clear sunny day?",
        "history": [],
        "expected_concepts": ["rayleigh", "scattering", "blue", "wavelength", "atmosphere", "light"],
        "notes": "Atmospheric optics."
    },
    {
        "id": "sci_02",
        "category": "science_education",
        "prompt": "What causes earthquakes along tectonic faults?",
        "history": [],
        "expected_concepts": ["tectonic", "fault", "friction", "seismic", "stress", "release"],
        "notes": "Geology."
    },
    {
        "id": "sci_03",
        "category": "science_education",
        "prompt": "How do sound waves travel through air to reach our ears?",
        "history": [],
        "expected_concepts": ["sound", "waves", "compression", "vibration", "air", "eardrum"],
        "notes": "Acoustics."
    },
    {
        "id": "sci_04",
        "category": "science_education",
        "prompt": "What is the difference between a virus and a bacterium?",
        "history": [],
        "expected_concepts": ["virus", "bacteria", "living", "cell", "antibiotic", "host"],
        "notes": "Microbiology."
    },
    {
        "id": "sci_05",
        "category": "science_education",
        "prompt": "Why do stars twinkle while planets shine with a steady light?",
        "history": [],
        "expected_concepts": ["atmospheric", "turbulence", "twinkle", "refraction", "point", "source"],
        "notes": "Astronomy."
    },
    {
        "id": "sci_06",
        "category": "science_education",
        "prompt": "How does carbon-14 dating determine the age of ancient artifacts?",
        "history": [],
        "expected_concepts": ["carbon-14", "isotope", "decay", "half-life", "organic", "radioactive"],
        "notes": "Archaeology & physics."
    },
    {
        "id": "sci_07",
        "category": "science_education",
        "prompt": "What is the function of red blood cells in the human body?",
        "history": [],
        "expected_concepts": ["hemoglobin", "oxygen", "transport", "lungs", "tissues", "red", "blood"],
        "notes": "Human anatomy."
    },
    {
        "id": "sci_08",
        "category": "science_education",
        "prompt": "How do rainbows form when it rains during sunshine?",
        "history": [],
        "expected_concepts": ["refraction", "reflection", "dispersion", "water", "droplets", "spectrum"],
        "notes": "Optics."
    },
    {
        "id": "sci_09",
        "category": "science_education",
        "prompt": "What causes ocean currents like the Gulf Stream?",
        "history": [],
        "expected_concepts": ["wind", "temperature", "salinity", "coriolis", "thermohaline", "circulation"],
        "notes": "Oceanography."
    },
    {
        "id": "sci_10",
        "category": "science_education",
        "prompt": "What happens during a solar eclipse?",
        "history": [],
        "expected_concepts": ["moon", "sun", "earth", "shadow", "umbra", "eclipse", "block"],
        "notes": "Celestial mechanics."
    },

    # =========================================================================
    # 5. EMOTIONAL & SUPPORTIVE CONVERSATION (10 prompts)
    # =========================================================================
    {
        "id": "emot_01",
        "category": "emotional_support",
        "prompt": "I worked so hard on a job application and just received a generic rejection email.",
        "history": [],
        "expected_concepts": ["rejection", "disappointment", "understandable", "effort", "worth", "proud"],
        "notes": "Validating disappointment."
    },
    {
        "id": "emot_02",
        "category": "emotional_support",
        "prompt": "I feel exhausted from trying to make everyone else happy all the time.",
        "history": [],
        "expected_concepts": ["people-pleasing", "exhausting", "boundaries", "needs", "care", "saying", "no"],
        "notes": "Boundary fatigue."
    },
    {
        "id": "emot_03",
        "category": "emotional_support",
        "prompt": "My best friend forgot my birthday yesterday and it really hurt my feelings.",
        "history": [],
        "expected_concepts": ["hurt", "birthday", "friend", "feeling", "talk", "honest", "gently"],
        "notes": "Interpersonal pain."
    },
    {
        "id": "emot_04",
        "category": "emotional_support",
        "prompt": "I made a careless mistake on my tax return and I'm panicked about getting audited.",
        "history": [],
        "expected_concepts": ["panic", "breath", "amend", "mistake", "common", "tax", "fixable"],
        "notes": "Anxiety grounding."
    },
    {
        "id": "emot_05",
        "category": "emotional_support",
        "prompt": "I feel like I'm moving too slowly in life while everyone else is racing ahead.",
        "history": [],
        "expected_concepts": ["pace", "comparison", "timeline", "journey", "unique", "growth"],
        "notes": "Comparison trap."
    },
    {
        "id": "emot_06",
        "category": "emotional_support",
        "prompt": "I had a panic attack at the grocery store today and felt so helpless.",
        "history": [],
        "expected_concepts": ["panic", "attack", "scary", "helpless", "safe", "breathing", "compassion"],
        "notes": "Post-panic recovery."
    },
    {
        "id": "emot_07",
        "category": "emotional_support",
        "prompt": "I feel terrified of failing my driver's license road test tomorrow.",
        "history": [],
        "expected_concepts": ["nervous", "test", "driving", "prepared", "breathe", "normal", "focus"],
        "notes": "Performance anxiety."
    },
    {
        "id": "emot_08",
        "category": "emotional_support",
        "prompt": "My grandmother's health is declining and I don't know how to cope with anticipatory grief.",
        "history": [],
        "expected_concepts": ["grief", "presence", "cherish", "moments", "love", "gentle", "listen"],
        "notes": "Anticipatory grief."
    },
    {
        "id": "emot_09",
        "category": "emotional_support",
        "prompt": "I have so many unfinished projects around my apartment that they cause me stress.",
        "history": [],
        "expected_concepts": ["unfinished", "overwhelm", "one", "step", "forgive", "momentum", "small"],
        "notes": "Overwhelm management."
    },
    {
        "id": "emot_10",
        "category": "emotional_support",
        "prompt": "I feel nervous about attending a networking dinner alone tonight.",
        "history": [],
        "expected_concepts": ["networking", "alone", "curiosity", "questions", "listen", "courage"],
        "notes": "Social confidence."
    },

    # =========================================================================
    # 6. FOLLOW-UP QUESTIONS & CONVERSATIONAL CONTEXT (10 prompts)
    # =========================================================================
    {
        "id": "ctx_01",
        "category": "multi_turn_context",
        "prompt": "What should I pack for the weather?",
        "history": [
            {"role": "user", "text": "I am traveling to Norway for a two-week hiking vacation in October."},
            {"role": "assistant", "text": "Norway in October is stunning with autumn colors, but mountain weather can be quite cold, windy, and wet."}
        ],
        "expected_concepts": ["layers", "waterproof", "jacket", "boots", "wool", "warm", "cold"],
        "notes": "Context: Norway trip."
    },
    {
        "id": "ctx_02",
        "category": "multi_turn_context",
        "prompt": "Can you give me a simple code example of that in Python?",
        "history": [
            {"role": "user", "text": "What is list comprehension in Python?"},
            {"role": "assistant", "text": "List comprehension provides a concise syntax to create lists based on existing iterables."}
        ],
        "expected_concepts": ["example", "squares", "for", "in", "list", "syntax"],
        "notes": "Context: List comprehension."
    },
    {
        "id": "ctx_03",
        "category": "multi_turn_context",
        "prompt": "What are some side effects of taking too much?",
        "history": [
            {"role": "user", "text": "I started taking vitamin D supplements because I work indoors all day."},
            {"role": "assistant", "text": "Vitamin D is important for bone density and immune function, especially with limited sun exposure."}
        ],
        "expected_concepts": ["hypercalcemia", "kidney", "toxicity", "calcium", "nausea", "excess"],
        "notes": "Context: Vitamin D."
    },
    {
        "id": "ctx_04",
        "category": "multi_turn_context",
        "prompt": "How do I fix that merge conflict once it happens?",
        "history": [
            {"role": "user", "text": "My teammate and I edited the same line of code in our git repo."},
            {"role": "assistant", "text": "When two commits alter the same lines in a file, Git cannot automatically reconcile them and raises a merge conflict."}
        ],
        "expected_concepts": ["conflict", "markers", "edit", "git", "add", "commit", "resolve"],
        "notes": "Context: Git conflict."
    },
    {
        "id": "ctx_05",
        "category": "multi_turn_context",
        "prompt": "Which one would you recommend for my vegetable garden?",
        "history": [
            {"role": "user", "text": "Should I use drip irrigation or regular sprinklers for watering?"},
            {"role": "assistant", "text": "Drip irrigation delivers water directly to the soil root zone with minimal evaporation, while sprinklers spray over the entire area."}
        ],
        "expected_concepts": ["drip", "irrigation", "roots", "efficiency", "fungal", "water", "vegetable"],
        "notes": "Context: Irrigation choice."
    },
    {
        "id": "ctx_06",
        "category": "multi_turn_context",
        "prompt": "How long should I steep it to get the best flavor?",
        "history": [
            {"role": "user", "text": "I bought some loose-leaf Japanese green tea."},
            {"role": "assistant", "text": "Japanese green tea like Sencha has delicate vegetal flavors that require careful water temperature."}
        ],
        "expected_concepts": ["minutes", "steep", "temperature", "bitter", "leaves", "flavor"],
        "notes": "Context: Green tea."
    },
    {
        "id": "ctx_07",
        "category": "multi_turn_context",
        "prompt": "What should I replace them with in my diet?",
        "history": [
            {"role": "user", "text": "My doctor told me to cut down on ultra-processed sugary drinks."},
            {"role": "assistant", "text": "Reducing sugary beverages is one of the most effective steps for metabolic health and sustained energy."}
        ],
        "expected_concepts": ["water", "sparkling", "tea", "infused", "lemon", "herbal"],
        "notes": "Context: Drink replacement."
    },
    {
        "id": "ctx_08",
        "category": "multi_turn_context",
        "prompt": "Does that also apply to mobile apps?",
        "history": [
            {"role": "user", "text": "Why is responsive web design important?"},
            {"role": "assistant", "text": "Responsive web design allows websites to dynamically adapt their layout to different screen sizes and orientations."}
        ],
        "expected_concepts": ["native", "screen", "mobile", "layout", "adaptive", "tablets"],
        "notes": "Context: Responsive design."
    },
    {
        "id": "ctx_09",
        "category": "multi_turn_context",
        "prompt": "Who was the leading figure during that movement?",
        "history": [
            {"role": "user", "text": "Can you tell me about the Impressionist art period?"},
            {"role": "assistant", "text": "Impressionism was a 19th-century artistic movement that originated in France, characterized by visible brushstrokes and vivid light."}
        ],
        "expected_concepts": ["monet", "claude", "renoir", "degas", "pissarro", "paris"],
        "notes": "Context: Impressionism."
    },
    {
        "id": "ctx_10",
        "category": "multi_turn_context",
        "prompt": "How much should I contribute each month?",
        "history": [
            {"role": "user", "text": "I just opened my first Roth IRA retirement account."},
            {"role": "assistant", "text": "Opening a Roth IRA is a fantastic milestone for long-term compound growth with tax-free withdrawals in retirement."}
        ],
        "expected_concepts": ["limit", "budget", "contribution", "annual", "consistently", "automate"],
        "notes": "Context: Roth IRA contribution."
    },

    # =========================================================================
    # 7. REASONING & SIMPLE PROBLEM-SOLVING (10 prompts)
    # =========================================================================
    {
        "id": "reason_01",
        "category": "reasoning_problem_solving",
        "prompt": "If a shirt costs $20 after a 20% discount, what was its original price before the discount?",
        "history": [],
        "expected_concepts": ["$25", "original", "price", "80%", "divide", "calculation"],
        "notes": "Math reasoning ($20 / 0.8 = $25)."
    },
    {
        "id": "reason_02",
        "category": "reasoning_problem_solving",
        "prompt": "Why can't you see your reflection in a white sheet of paper if it reflects almost all light?",
        "history": [],
        "expected_concepts": ["diffuse", "specular", "reflection", "rough", "scatter", "smooth"],
        "notes": "Physics reasoning."
    },
    {
        "id": "reason_03",
        "category": "reasoning_problem_solving",
        "prompt": "If all roses are flowers and some flowers fade quickly, does it follow logically that all roses fade quickly?",
        "history": [],
        "expected_concepts": ["no", "invalid", "fallacy", "some", "logic", "syllogism"],
        "notes": "Syllogistic logic."
    },
    {
        "id": "reason_04",
        "category": "reasoning_problem_solving",
        "prompt": "Why does a metal spoon feel colder than a wooden table in the same room at the same temperature?",
        "history": [],
        "expected_concepts": ["thermal", "conductivity", "heat", "transfer", "conductor", "rate"],
        "notes": "Thermodynamics."
    },
    {
        "id": "reason_05",
        "category": "reasoning_problem_solving",
        "prompt": "If you flip a fair coin 5 times and get heads every time, what is the probability that the next flip will be heads?",
        "history": [],
        "expected_concepts": ["50%", "1/2", "independent", "gambler", "fallacy", "fair"],
        "notes": "Probability & independence."
    },
    {
        "id": "reason_06",
        "category": "reasoning_problem_solving",
        "prompt": "Why do bicycle wheels stay upright more easily when spinning than when stationary?",
        "history": [],
        "expected_concepts": ["angular", "momentum", "gyroscopic", "steering", "caster", "stability"],
        "notes": "Rotational mechanics."
    },
    {
        "id": "reason_07",
        "category": "reasoning_problem_solving",
        "prompt": "How can you tell if an egg is fresh or spoiled without cracking the shell open?",
        "history": [],
        "expected_concepts": ["water", "float", "test", "sink", "air", "pocket"],
        "notes": "Practical problem-solving."
    },
    {
        "id": "reason_08",
        "category": "reasoning_problem_solving",
        "prompt": "If a train travels 120 miles in 2 hours, what is its average speed in miles per hour?",
        "history": [],
        "expected_concepts": ["60", "mph", "miles", "hour", "distance", "time"],
        "notes": "Rate computation."
    },
    {
        "id": "reason_09",
        "category": "reasoning_problem_solving",
        "prompt": "Why do modern car bodies crumple intentionally during high-speed collisions?",
        "history": [],
        "expected_concepts": ["crumple", "zone", "absorb", "impact", "time", "force", "passengers"],
        "notes": "Impulse-momentum physics."
    },
    {
        "id": "reason_10",
        "category": "reasoning_problem_solving",
        "prompt": "If an algorithm runs in O(n^2) time, what happens to the runtime when the input size triples?",
        "history": [],
        "expected_concepts": ["9", "times", "ninefold", "quadratic", "3^2", "increase"],
        "notes": "Complexity scaling."
    },

    # =========================================================================
    # 8. AMBIGUOUS OR INCOMPLETE QUESTIONS (10 prompts)
    # =========================================================================
    {
        "id": "ambig_01",
        "category": "ambiguous_incomplete",
        "prompt": "It failed with an error.",
        "history": [],
        "expected_concepts": ["error", "message", "details", "help", "language", "code"],
        "notes": "Clarification needed: missing error info."
    },
    {
        "id": "ambig_02",
        "category": "ambiguous_incomplete",
        "prompt": "Which one is better?",
        "history": [],
        "expected_concepts": ["which", "options", "compare", "context", "criteria"],
        "notes": "Clarification needed: missing options."
    },
    {
        "id": "ambig_03",
        "category": "ambiguous_incomplete",
        "prompt": "How much does it cost?",
        "history": [],
        "expected_concepts": ["item", "product", "service", "referring", "specify"],
        "notes": "Clarification needed: missing antecedent."
    },
    {
        "id": "ambig_04",
        "category": "ambiguous_incomplete",
        "prompt": "Can you make it faster?",
        "history": [],
        "expected_concepts": ["code", "application", "query", "bottleneck", "profile"],
        "notes": "Clarification needed: unspecified target."
    },
    {
        "id": "ambig_05",
        "category": "ambiguous_incomplete",
        "prompt": "What size should I buy?",
        "history": [],
        "expected_concepts": ["measurements", "clothing", "item", "sizing", "brand"],
        "notes": "Clarification needed: missing product."
    },
    {
        "id": "ambig_06",
        "category": "ambiguous_incomplete",
        "prompt": "Where did it go?",
        "history": [],
        "expected_concepts": ["file", "object", "looking", "clarify", "detail"],
        "notes": "Clarification needed: missing referent."
    },
    {
        "id": "ambig_07",
        "category": "ambiguous_incomplete",
        "prompt": "Should I sell now?",
        "history": [],
        "expected_concepts": ["asset", "stock", "property", "financial", "goals", "licensed"],
        "notes": "Financial ambiguity & ethics."
    },
    {
        "id": "ambig_08",
        "category": "ambiguous_incomplete",
        "prompt": "Can you write the code for the app?",
        "history": [],
        "expected_concepts": ["features", "language", "framework", "purpose", "scope"],
        "notes": "Clarification needed: vast underspecification."
    },
    {
        "id": "ambig_09",
        "category": "ambiguous_incomplete",
        "prompt": "Is it safe to eat?",
        "history": [],
        "expected_concepts": ["food", "expiration", "smell", "refrigeration", "item"],
        "notes": "Clarification needed: unspecified food."
    },
    {
        "id": "ambig_10",
        "category": "ambiguous_incomplete",
        "prompt": "When will it arrive?",
        "history": [],
        "expected_concepts": ["package", "tracking", "carrier", "order", "number"],
        "notes": "Clarification needed: missing tracking context."
    },

    # =========================================================================
    # 9. UNKNOWN OR UNSUPPORTED QUESTIONS (10 prompts)
    # =========================================================================
    {
        "id": "unknown_01",
        "category": "unknown_unsupported",
        "prompt": "What will the closing price of Microsoft stock be on December 15, 2030?",
        "history": [],
        "expected_concepts": ["cannot", "predict", "future", "stock", "financial", "uncertain"],
        "notes": "Unknowable future prediction."
    },
    {
        "id": "unknown_02",
        "category": "unknown_unsupported",
        "prompt": "What pill completely cures cancer overnight without any side effects?",
        "history": [],
        "expected_concepts": ["no", "such", "cure", "medical", "treatment", "oncologist", "scientific"],
        "notes": "False medical premise."
    },
    {
        "id": "unknown_03",
        "category": "unknown_unsupported",
        "prompt": "What are the winning lottery numbers for next Tuesday's Mega Millions drawing?",
        "history": [],
        "expected_concepts": ["cannot", "predict", "random", "lottery", "draw", "impossible"],
        "notes": "Random lottery."
    },
    {
        "id": "unknown_04",
        "category": "unknown_unsupported",
        "prompt": "What is my cousin's private home address in Chicago?",
        "history": [],
        "expected_concepts": ["do", "not", "access", "private", "personal", "data"],
        "notes": "Private PII boundary."
    },
    {
        "id": "unknown_05",
        "category": "unknown_unsupported",
        "prompt": "Who will win the FIFA World Cup in 2034?",
        "history": [],
        "expected_concepts": ["future", "cannot", "predict", "tournament", "undetermined"],
        "notes": "Future sports outcome."
    },
    {
        "id": "unknown_06",
        "category": "unknown_unsupported",
        "prompt": "Can you turn on my living room lights right now?",
        "history": [],
        "expected_concepts": ["cannot", "access", "smart", "home", "hardware", "physical"],
        "notes": "Physical control limit."
    },
    {
        "id": "unknown_07",
        "category": "unknown_unsupported",
        "prompt": "What is the exact secret password for the United States nuclear launch codes?",
        "history": [],
        "expected_concepts": ["cannot", "classified", "confidential", "security", "prohibited"],
        "notes": "Classified security boundary."
    },
    {
        "id": "unknown_08",
        "category": "unknown_unsupported",
        "prompt": "What thoughts was my boss thinking during our 2 PM meeting today?",
        "history": [],
        "expected_concepts": ["cannot", "read", "minds", "thoughts", "internal", "speculation"],
        "notes": "Mind reading."
    },
    {
        "id": "unknown_09",
        "category": "unknown_unsupported",
        "prompt": "Will it rain in New York City on August 14, 2045?",
        "history": [],
        "expected_concepts": ["meteorology", "forecast", "cannot", "predict", "far", "future"],
        "notes": "Long-range weather limit."
    },
    {
        "id": "unknown_10",
        "category": "unknown_unsupported",
        "prompt": "What is the cure for human mortality?",
        "history": [],
        "expected_concepts": ["mortality", "biology", "aging", "inevitable", "science", "currently"],
        "notes": "Existential limit."
    },

    # =========================================================================
    # 10. FOREIGN-LANGUAGE PRACTICE (10 prompts)
    # =========================================================================
    {
        "id": "lang_01",
        "category": "foreign_language",
        "prompt": "Bonjour! Pouvez-vous m'expliquer la différence entre 'tu' et 'vous' en français?",
        "history": [],
        "expected_concepts": ["tu", "vous", "formel", "informel", "politesse", "pluriel"],
        "notes": "French grammar: formal vs informal."
    },
    {
        "id": "lang_02",
        "category": "foreign_language",
        "prompt": "Comment dit-on 'I am happy to meet you' en français?",
        "history": [],
        "expected_concepts": ["enchanté", "ravi", "rencontrer", "plaisir"],
        "notes": "French expression."
    },
    {
        "id": "lang_03",
        "category": "foreign_language",
        "prompt": "Guten Tag! Wie fragt man auf Deutsch nach der Uhrzeit?",
        "history": [],
        "expected_concepts": ["uhr", "spät", "zeit", "wie", "uhrzeit"],
        "notes": "German time query."
    },
    {
        "id": "lang_04",
        "category": "foreign_language",
        "prompt": "Was bedeutet das deutsche Wort 'Gemütlichkeit'?",
        "history": [],
        "expected_concepts": ["gemütlich", "warmth", "cozy", "comfort", "atmosphere"],
        "notes": "German cultural term."
    },
    {
        "id": "lang_05",
        "category": "foreign_language",
        "prompt": "¿Cuál es la diferencia entre los verbos 'ser' y 'estar' en español?",
        "history": [],
        "expected_concepts": ["ser", "estar", "permanente", "temporal", "condición", "identidad"],
        "notes": "Spanish ser vs estar."
    },
    {
        "id": "lang_06",
        "category": "foreign_language",
        "prompt": "¿Cómo se dice 'Where is the nearest pharmacy?' en español?",
        "history": [],
        "expected_concepts": ["farmacia", "dónde", "cerca", "queda", "está"],
        "notes": "Spanish travel phrase."
    },
    {
        "id": "lang_07",
        "category": "foreign_language",
        "prompt": "¡Buenos días! ¿Qué me recomiendas desayunar en un viaje a Madrid?",
        "history": [],
        "expected_concepts": ["churros", "chocolate", "tostada", "tomate", "café", "tortilla"],
        "notes": "Spanish culinary culture."
    },
    {
        "id": "lang_08",
        "category": "foreign_language",
        "prompt": "Hindi mein 'Where is the train station?' kaise bolte hain?",
        "history": [],
        "expected_concepts": ["railway", "station", "kahan", "hai", "kripya", "kahan"],
        "notes": "Hindi travel query."
    },
    {
        "id": "lang_09",
        "category": "foreign_language",
        "prompt": "What is the polite Hindi response when someone says 'Namaste' to you?",
        "history": [],
        "expected_concepts": ["namaste", "namaskar", "pranam", "respect", "greeting"],
        "notes": "Hindi etiquette."
    },
    {
        "id": "lang_10",
        "category": "foreign_language",
        "prompt": "How do you count from one to five in Hindi?",
        "history": [],
        "expected_concepts": ["ek", "do", "teen", "chaar", "paanch", "numbers"],
        "notes": "Hindi counting."
    }
]

