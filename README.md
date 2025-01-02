# ScoreDraft

ScoreDraft is a desktop application for freehand music note-taking on an infinite canvas. It aims to combine the flexibility of traditional pen-and-paper methods with the convenience of digital tools. The project is focused on creating a lightweight, responsive, and open solution for personal use, with extensibility in mind for potential future development.

---

## Overview

### Goals
- Provide a digital alternative to pen-and-paper for music note-taking.
- Ensure the application feels responsive and snappy, even on older systems.
- Store user-created content in open formats (e.g., SVG) to ensure compatibility with external tools.
- Support freehand drawing, with potential for text and line annotations in future versions.

### Features
- Infinite canvas for music notation.
- Freehand drawing with smooth rendering.
- Interactive CLI (TUI) for navigating canvases and linking related documents.
- SVG-based storage to maintain openness and portability of user content.

---

## Anticipated Challenges

### Real-Time Rendering
- **Problem**: SVG rendering engines typically re-render the entire SVG on updates, which can make real-time drawing sluggish.
- **Solution**: Use Kivy for real-time rendering while translating user input to SVG in the background.

### Line Smoothing
- **Problem**: Raw input data from freehand drawing may appear jagged or unpolished.
- **Solution**: Apply smoothing algorithms (e.g., Bézier curves or splines) to generate clean paths.

### Consistent Rendering
- **Problem**: The appearance of SVGs rendered in the app may differ from those viewed in external tools.
- **Solution**: Utilize Cairo for precise SVG creation and configure consistent styling properties (e.g., stroke-width, linecap, filters).

---

## Libraries

### Core Libraries
1. **Kivy**
   - **Purpose**: GUI rendering and interactive canvas functionality.
   - **Rationale**: Lightweight, cross-platform, and optimized for real-time user interaction.

2. **Cairo**
   - **Purpose**: SVG creation and rendering.
   - **Rationale**: High-quality vector graphics generation with precise control over paths, styles, and export.

3. **RSVG**
   - **Purpose**: Parsing and handling SVG files.
   - **Rationale**: Ensures compatibility for loading, saving, and rendering externally created SVGs.

---

## Design Decisions

1. **Open Formats**
   - User content will be stored in SVG to ensure compatibility with external programs and long-term accessibility.

2. **Rendering Workflow**
   - Use Kivy's real-time drawing capabilities for input responsiveness.
   - Translate finished strokes into SVG paths asynchronously to minimize delays.

3. **Lightweight Application**
   - Focus on performance optimizations to keep the app responsive on older hardware.
   - Avoid web-based technologies to reduce overhead.

---

## Future Considerations
- Add support for text annotations and structured elements like arrows and lines.
- Explore cross-platform packaging options for broader distribution.
- Investigate more advanced rendering engines or technologies if needed for scaling.
- Implement linked canvases to allow users to connect different notes (e.g., linking sections of a composition or transitions).
- Support sub-canvases within a canvas to enable versioning and iteration over specific sections.

---

## Usage
- **Initial Setup**: Install the required libraries (detailed instructions will be added as development progresses).
- **Drawing**: Use the infinite canvas for freehand notes.
- **Navigation**: Leverage the interactive CLI for managing linked canvases.

---

## Contributing
This is a personal project aimed at experimentation and solving a specific problem. Contributions are welcome as the project evolves. For feedback or feature requests, please open an issue.

---

## License
[MIT License](LICENSE)

