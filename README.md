# مواصفات واجهة تطبيق تعليمي لتوضيح الخوارزميات

## الهدف العام

يهدف المشروع إلى بناء تطبيق تعليمي متكامل بلغة **Python** يقوم بتنفيذ وشرح مجموعة من الخوارزميات الأساسية في علوم الحاسب. الفكرة ليست فقط في كتابة الكود، بل في جعل عمل الخوارزمية مرئياً ومفهوماً للمستخدم خطوة بخطوة.

## نطاق المشروع

### الخوارزميات الأساسية المطلوبة

1. Linear Search (البحث الخطي)
2. Merge Sort (الفرز بالدمج)
3. Quick Sort (الفرز السريع)
4. Kruskal's Algorithm (كروسكال لإيجاد الشجرة الممتدة الصغرى)
5. Dijkstra's Algorithm (ديكسترا لإيجاد أقصر مسار)

### التوسّع المقترح

بالإضافة إلى الخوارزميات الخمس السابقة، نهدف لتوسيع التطبيق ليشمل ما يقارب **12 من أشهر خوارزميات العرض والترتيب والبحث التعليمية**، مثل:

- Binary Search
- Bubble Sort
- Selection Sort
- Insertion Sort
- Heap Sort
- Breadth-First Search (BFS)
- Depth-First Search (DFS)
- Bellman-Ford Algorithm
- Prim’s Algorithm

## المتطلبات الأساسية للتطبيق

### 1. كتابة الكود البرمجي الصحيح

- لكل خوارزمية سيتم توفير دالة (function) بلغة Python
- الكود يجب أن يكون فعالاً، ويعالج مختلف المدخلات مع إرجاع النتائج الصحيحة

### 2. التمثيل البصري (Visualization)

- واجهة رسومية تعرض خطوات تنفيذ الخوارزمية بشكل تفاعلي
- استخدام عناصر مرئية مثل:
  - الأعمدة البيانية (للترتيب)
  - العقد والحواف (للرسوم البيانية)
- دعم التقدم خطوة بخطوة عبر **مؤشر (Slider)**
- عند كل خطوة يتم عرض شرح نصي مبسط أسفل التمثيل

### 3. التفاعل مع المستخدم والمدخلات

- واجهة إدخال مرنة تسمح للمستخدم بإدخال بياناته
- التحقق من صحة المدخلات قبل التنفيذ

### 4. أوضاع التشغيل

- **الوضع التفاعلي:** المستخدم يتنقل بين الخطوات يدوياً (Step by Step)
- **الوضع التلقائي:** تشغيل الخوارزمية كأنها مقطع فيديو مع تحريك تلقائي للخطوات
- إمكانية الإيقاف المؤقت والاستئناف

### 5. التقرير التحليلي (Analysis Report)

بعد التنفيذ، يتم عرض تقرير موجز يتضمن:

- **تعقيد الوقت (Time Complexity):** الحالات الثلاث (أفضل، متوسط، أسوأ)
- **تعقيد المساحة (Space Complexity)**
- ملاحظات إضافية حول كفاءة الخوارزمية واستخداماتها العملية

## التصميم والوظائف الرئيسية

### التمثيل البصري بخطوات قابلة للتنقل

- الخوارزمية تُنفّذ على شكل تسلسل من "الأحداث" (events)
- يتم تخزين هذه الأحداث في "trace" (قائمة مرتّبة من الأحداث)
- الواجهة تعرض الرسم وتتفاعل مع الحدث الحالي
- زرّان أو Slider للانتقال خطوة للخلف/خطوة للأمام
- القدرة على الانتقال لأي خطوة مباشرة
- مع كل خطوة، يظهر شرح نصي يصف العملية

### إدخال المدخلات والتحقّق

**أنواع المدخلات المقترحة:**

- Sorting / Searching: مصفوفة أرقام (قابلة للكتابة أو التحميل أو التوليد العشوائي)
- Graph algorithms: قائمة حواف (edge list) مع أوزان، أو قائمة جوار (adjacency list) مع أوزان

**قواعد التحقق (Validation):**

- التحقق من نوع القيم (أرقام صحيحة أم عشرية)
- التأكد من عدم وجود أوزان سالبة عند تشغيل Dijkstra
- التحقق من أن الحواف تشير إلى عقد موجودة وأن الأوزان عددية
- إعلام المستخدم برسالة واضحة عند وجود خطأ

### نظام التشغيل التفاعلي

**عناصر التحكم المطلوبة:**

- Play / Pause
- Step Forward (خطوة للأمام)
- Step Back (خطوة للخلف)
- Speed Control (شريط أو قائمة لاختيار سرعة التشغيل)
- Replay (إعادة التشغيل من البداية)

## التنفيذ التقني

### كتابة الخوارزمية كمولد أحداث (Generator)

- كل خوارزمية تخرج `yield` لأحداث على شكل قواميس (dict/JSON)
- مثال: بدلًا من إرجاع مصفوفة مرتبة فقط، `merge_sort_events(arr)` يقوم بعمل `yield` لكل عملية مقارنة أو كتابة

### شكل الحدث المقترح (Event Schema)

كل حدث يجب أن يحتوي الحقول الأساسية التالية على الأقل:

- `step`: رقم الخطوة (int)
- `type`: نوع الحدث (string) - أمثلة: `compare`, `swap`, `overwrite`, `visit`, `set_pivot`, `consider_edge`, `add_mst_edge`, `relax`, `set_distance`, `found`, `done`
- `details`: نص شرح موجز يصف الحدث للمستخدم
- حقول إضافية حسب النوع (مثلاً: `i`, `j`, `index`, `value`, `u`, `v`, `weight`)

### محرك العرض (Visualization Engine)

- يقوم بقراءة حدث تلو الآخر
- يحدّث الرسوم (مثلاً: تغيير لون عمود، تغيير ارتفاع عمود، تلوين حافة)
- يدعم التحكم بالسرعة والـ play/pause
- يدعم التخزين الكامل للـ trace لتمكين step-back و replay

## الهيكل التنظيمي للمشروع

```
/project_root
  /app
    /algorithms      # implementations that yield events
      linear_search.py
      merge_sort.py
      quick_sort.py
      kruskal.py
      dijkstra.py
    /visualization   # mapping events -> visual updates
    /ui              # واجهات للمستخدم (PyQt/Streamlit/...)
    /utils           # validators, generators, loaders, serializers
  /tests
  /docs
  README.md
```

## ميزات إضافية مقترحة

- حفظ trace كـ JSON للـ replay أو المشاركة
- لوحة log عرض كامل لسجل الخطوات مع قابلية البحث والانتقال
- أزرار "توليد بيانات عشوائية" و"نماذج جاهزة" لاختبار سريع
- تصدير العرض كفيديو أو GIF (ميزة متقدمة لاحقاً)

## قائمة التحقق عند التسليم

- [ ] واجهة إدخال مدخلات مع تحقق فعّال
- [ ] كل خوارزمية تُصدر trace من الأحداث
- [ ] محرك عرض يدعم play/pause/step/back/speed
- [ ] شرح نصي يظهر لكل خطوة
- [ ] حفظ/تحميل trace بصيغة JSON

## الخطوات التالية المقترحة

1. تصميم مخطط واجهة (wireframe) بسيط لشاشة التشغيل
2. تنفيذ نموذج أولي (Prototype) لواحدة من الخوارزميات
3. مراجعة التجربة وتجميع ملاحظات لتحسين التجربة قبل بناء بقية الخوارزميات

```md
    You are Manus, a highly-capable code generation and project orchestration assistant. Your objective is to produce a complete, production-quality Python project: an interactive educational application that visualizes and explains algorithms step-by-step according to the specification below. Produce working code, tests, documentation, sample data, and a runnable demo. Prioritize correctness, modular architecture, clear API contracts, readability, type hints, and developer-friendly docs. Use best global engineering practices and produce a git-style repository layout with commits described in a single log at the end.

    Project summary:
    Create a Python application named "AlgoVisEdu" that demonstrates and visualizes these algorithms initially: Linear Search, Merge Sort, Quick Sort, Kruskal (MST), and Dijkstra (SSSP). Design the codebase so adding up to ~12 algorithms (sorting/searching/graph) is straightforward. Provide a polished interactive UI using Streamlit for the main demo (desktop-first, responsive), with a core visualization engine that maps time-ordered "events" to UI updates. Save traces as JSON for replay.

    Key deliverables (files & behavior):
    1. Full repository scaffold (project_root) with these folders/files:
    - app/
        - algorithms/ (one file per algorithm, each algorithm implemented as a generator yielding events)
        - linear_search.py, merge_sort.py, quick_sort.py, kruskal.py, dijkstra.py
        - visualization/
        - engine.py (core event-to-UI translator)
        - renderers.py (render functions for arrays, bars, graphs)
        - ui/
        - streamlit_app.py (main runnable UI)
        - components.py (controls: play/pause/step/back/speed/slider/load/save)
        - utils/
        - validators.py, io.py (load/save trace JSON), sample_generators.py, types.py (event dataclasses)
    - tests/
        - unit tests for generator correctness and event schema conformance
    - docs/
        - README.md (detailed run & dev instructions)
        - API.md (algorithm event schema, examples)
    - requirements.txt
    - pyproject.toml or setup.cfg
    - sample_data/ (example arrays and graphs)
    - examples/trace_samples.json (saved traces)
    - CI config: a simple GitHub Actions workflow that runs tests and lint.

    Architecture & quality constraints:
    - Algorithms must **yield** events (Python generators). Each yielded event is a dictionary or dataclass with at least: `step:int`, `type:str`, `details:str`, plus fields relevant to the event (e.g., `i`, `j`, `index`, `value`, `u`, `v`, `weight`, `distance`). Provide a canonical Event dataclass in utils/types.py and ensure all algorithms yield instances convertible to JSON.
    - Use type hints and thorough docstrings (Google or NumPy style). Add short comments where algorithms are tricky.
    - Write unit tests that execute each algorithm generator on representative inputs and assert that: sequence ends with a `done` event, events conform to schema, and final logical result matches reference algorithm (e.g., sorted array, shortest distances, MST edges).
    - Keep external dependencies minimal and explicit in requirements.txt: streamlit, networkx, matplotlib, numpy, pytest. Avoid heavy or obscure packages.

    Event schema (canonical):
    - `step` (int): monotonic step number
    - `type` (str): e.g., "compare", "swap", "overwrite", "visit", "set_pivot", "consider_edge", "add_mst_edge", "relax", "set_distance", "found", "done"
    - `details` (str): short human-readable explanation
    - optional fields depending on type: `i`, `j`, `index`, `value`, `u`, `v`, `weight`, `old_value`, `new_value`, `distances` (for snapshots)
    Examples:
    - {"step": 12, "type":"compare", "details":"compare arr[3] and arr[7]", "i":3, "j":7}
    - {"step": 20, "type":"swap", "details":"swap arr[2] and arr[5]", "i":2, "j":5}
    - {"step": 65, "type":"relax", "details":"relax edge 2->5 weight 4", "u":2, "v":5, "weight":4, "new_distance":10}

    Visualization engine requirements:
    - engine.py should accept a trace (list of events) and expose:
    - step_count, current_step, next(), prev(), seek(step), play(speed), pause(), get_snapshot() that returns a minimal renderable state.
    - renderers must be stateless pure functions that accept the current snapshot and return Matplotlib figures or Plotly objects that Streamlit can display. Provide two render modes: array-bars (for sorts/search) and graph (for graph algorithms). Use NetworkX to manage graph layouts but keep the UI rendering simple (matplotlib or Plotly). Avoid custom JS unless strictly necessary.
    - UI must provide: load/save trace JSON, text explanation area (shows `details` of current event), slider for seeking, Play/Pause, Step Forward, Step Back, Speed selector, Replay button, random/generate sample data, and validations with clear error messages.

    Algorithm implementation expectations:
    - Implement each algorithm so that **every meaningful operation** is yielded as an event. For sorts: comparisons, swaps/overwrites, pivot selections, merges. For graph algorithms: visiting nodes, considering edges, relaxations, adding MST edges, distance updates.
    - Dijkstra: validate non-negative weights; if negative weights are present, provide a clear validation error and optionally run Bellman-Ford instead (if implemented).
    - Kruskal: yield events when edges are considered and when an edge is added to MST.
    - Merge sort & Quick sort: produce events describing recursive splits/merges and the array snapshots where useful.
    - Also provide a "snapshot" event type occasionally to allow the renderer to draw the full array/graph state.

    User inputs & validation:
    - Provide UI forms for:
    - array input (comma-separated) or generate random (size & range)
    - graph input via adjacency list, edge list upload (CSV/JSON), or random graph generator (n, density, weight range)
    - validators.py must check types, connectivity expectations (for algorithms that require connected graphs), negative weights, duplicated nodes, etc., and return structured errors.

    Testing, docs & examples:
    - Provide pytest tests for correctness and event emission. Include at least one integration test that runs the streamlit app headless to ensure no import/run errors (a simple smoke test).
    - README must include: how to install, run (e.g., `pip install -r requirements.txt` then `streamlit run app/ui/streamlit_app.py`), how to add a new algorithm (developer guide: implement generator adhering to event schema, add renderer if needed, register in UI).
    - Provide an API.md that documents the Event schema, engine API, and example traces (include 2 short JSON samples).
    - Provide code comments indicating where to extend the repo for the additional 7 algorithms later.

    UX and pedagogical notes:
    - For each step also show a concise textual explanation (the `details`), and optionally an expandable "deep explanation" that explains the algorithmic reasoning (complexity, why this operation matters) — display in the UI after the run completes or on demand.
    - After a full run, show an analysis panel that lists time complexity (best/avg/worst) and space complexity and practical notes for that algorithm (these descriptions can be templated content in docs and injected to UI).

    Acceptance criteria (must be true before final delivery):
    1. The repo runs locally and the Streamlit demo starts without errors.
    2. For each of the five algorithms, there exists a generator producing a non-empty trace ending with `done`, and a unit test validating final correctness.
    3. The engine supports stepping forward/back and play/pause with speed control.
    4. Traces can be saved/loaded as JSON and replayed deterministically.
    5. README and API docs present clear instructions and examples.
    6. Provide a short developer changelog describing commits/manus actions.

    Output format requirements for Manus:
    - Create the full repository tree with file contents. For large files include full code. Ensure files are runnable and imports resolve relative to project root.
    - At the end of generation, output a brief commit log (list of high-level commits and what they contain) and instructions to run tests and launch the demo.
    - Also provide 2 ready-made trace JSON files (one for a short merge_sort run and one for a short Dijkstra run) as examples.

    Non-functional constraints:
    - Favor clarity over clever micro-optimizations. Prioritize pedagogical clarity in emitted events and UI over squeezing performance. Keep code portable (Python 3.10+).
    - Use no external web services. All generated assets must be local.

    Now generate the complete project files and content described above. Start by producing the repository tree and then fill files in order of importance (core types, one full algorithm generator as a canonical example — Merge Sort — with tests, the visualization engine, Streamlit UI wired to that engine, utilities, and then the remaining algorithm stubs fully implemented). After code, produce the example trace JSON files and the short commit log and run instructions.

    Final packaging requirement:
    After generating the full repository with all files and documentation, package the entire project into a single well-organized ZIP archive named `AlgoVisEdu.zip`. Ensure directory structure, imports, and run instructions are intact. Provide this ZIP file as the final output, ready for direct download and use without any additional modifications.
```

---

---

# AlgoVisEdu: Algorithm Visualizer & Educator

AlgoVisEdu is an interactive Python application built with Streamlit that visualizes and explains various algorithms step-by-step. It's designed to be an educational tool for understanding how algorithms work through dynamic visualization and detailed event logging.

## Features

- **Interactive Visualization**: See algorithms in action with real-time updates.
- **Step-by-Step Explanation**: Understand each operation with concise textual details.
- **Playback Controls**: Play, pause, step forward/backward, and adjust playback speed.
- **Algorithm Analysis**: View time and space complexity, along with pedagogical notes for each algorithm.
- **Trace Management**: Save and load algorithm execution traces as JSON files for replay and analysis.
- **Extensible Architecture**: Easily add new algorithms (sorting, searching, graph) by implementing a generator function.

## Implemented Algorithms (Initial Set)

- **Sorting Algorithms**:
  - Merge Sort
  - Quick Sort
- **Searching Algorithms**:
  - Linear Search
- **Graph Algorithms**:
  - Kruskal (Minimum Spanning Tree)
  - Dijkstra (Single Source Shortest Path)

## Project Structure

```
AlgoVisEdu/
├── app/
│   ├── algorithms/             # Algorithm implementations as event generators
│   │   ├── linear_search.py
│   │   ├── merge_sort.py
│   │   ├── quick_sort.py
│   │   ├── kruskal.py
│   │   └── dijkstra.py
│   ├── visualization/          # Core visualization engine and renderers
│   │   ├── engine.py
│   │   └── renderers.py
│   └── ui/                     # Streamlit UI components and main app
│       ├── streamlit_app.py
│       └── components.py
│   └── utils/                  # Utility functions (types, validators, IO, sample data generators)
│       ├── types.py
│       ├── validators.py
│       ├── io.py
│       ├── sample_generators.py
│       └── union_find.py       # Helper for Kruskal's
├── tests/                      # Unit tests for algorithms and components
│   └── test_merge_sort.py
│   └── ... (other algorithm tests)
├── docs/                       # Documentation files
│   ├── README.md
│   └── API.md
├── sample_data/                # Example input data for algorithms
├── examples/                   # Example trace JSON files
│   └── trace_samples.json
├── requirements.txt            # Python dependencies
└── pyproject.toml              # Project metadata and build configuration
```

## Setup and Installation

1.  **Clone the repository**:

    ```bash
    git clone https://github.com/your-username/AlgoVisEdu.git
    cd AlgoVisEdu
    ```

2.  **Create a virtual environment** (recommended):

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    Alternatively, if you prefer `poetry` or `pipenv`, you can use `pyproject.toml`.

## How to Run the Demo

To launch the interactive Streamlit application:

```bash
streamlit run app/ui/streamlit_app.py
```

This will open the application in your default web browser. If it doesn't, Streamlit will provide a local URL (e.g., `http://localhost:8501`).

## How to Add a New Algorithm (Developer Guide)

The architecture is designed to make adding new algorithms straightforward:

1.  **Create a new algorithm file**: In `app/algorithms/`, create a new Python file (e.g., `new_algo.py`).

2.  **Implement the generator**: Inside `new_algo.py`, implement your algorithm as a Python generator function. This function must `yield` `Event` objects (defined in `app/utils/types.py`) at every meaningful step of the algorithm. Ensure the `Event` objects conform to the [Event Schema](#event-schema).

    ```python
    # Example structure for new_algo.py
    from typing import Generator, List, Any
    from app.utils.types import Event, Array

    def new_algorithm_generator(data: Any) -> Generator[Event, None, None]:
        step_count = 0
        # ... algorithm logic ...
        yield Event(step=step_count, type="start", details="Algorithm started", data={})
        step_count += 1
        # ... yield more events ...
        yield Event(step=step_count, type="done", details="Algorithm finished", data={})
    ```

3.  **Register the algorithm**: Open `app/ui/streamlit_app.py` and:

    - Import your new generator function.
    - Add your algorithm to the `algorithms` dictionary, specifying its `generator` and `type` (e.g., `"array"` or `"graph"`).

    ```python
    # In app/ui/streamlit_app.py
    from app.algorithms.new_algo import new_algorithm_generator

    algorithms = {
        # ... existing algorithms ...
        "New Algorithm Name": {"generator": new_algorithm_generator, "type": "array"},
    }
    ```

4.  **(Optional) Create a renderer**: If your algorithm requires a unique visualization (e.g., a custom data structure), you might need to extend `app/visualization/renderers.py` with a new rendering function and integrate it into `streamlit_app.py`.

5.  **(Optional) Add unit tests**: Create a corresponding test file in `tests/` (e.g., `test_new_algo.py`) to ensure your generator produces correct events and the final result is accurate.

## Event Schema

The `Event` dataclass (defined in `app/utils/types.py`) is the core data structure for capturing algorithm steps. Each event is a dictionary or dataclass with at least the following fields:

- `step` (int): A monotonically increasing step number.
- `type` (str): A string categorizing the event (e.g., "compare", "swap", "visit", "add_mst_edge", "relax", "done").
- `details` (str): A short, human-readable explanation of what happened in this step.
- `data` (Dict[str, Any]): An optional dictionary containing event-specific data. This can include indices (`i`, `j`, `index`), values (`value`, `old_value`, `new_value`), graph nodes/edges (`u`, `v`, `weight`), distances (`distances`), or snapshots of the entire data structure (`array_snapshot`, `graph_snapshot`).

For a detailed API reference and examples, please refer to `docs/API.md`.

## Running Tests

To run the unit tests, navigate to the project root and execute `pytest`:

```bash
pytest
```

## CI/CD (GitHub Actions)

A simple GitHub Actions workflow is included to run tests and linting on pushes and pull requests. The configuration is located at `.github/workflows/main.yml`.

## License

This project is licensed under the MIT License - see the LICENSE file for details. (Note: LICENSE file not generated in this output, but should be added to a real project.)

## Acknowledgements

- Streamlit for the amazing web framework.
- Matplotlib and NetworkX for visualization capabilities.

---

_Generated by Manus AI_
