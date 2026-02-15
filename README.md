# FlashForge

AI-powered flashcard generator that transforms course documents into study sets in seconds.

## Tech Stack

- **Runtime**: Bun
- **Framework**: React 19
- **Styling**: Tailwind CSS 4
- **Deployment**: Vercel

## Project Structure

```
src/
├── components/        # React components
│   ├── FileUpload.tsx    # File upload with drag & drop
│   └── FlashcardView.tsx # Flashcard display
├── types/            # TypeScript type definitions
│   └── flashcard.ts
├── utils/            # Utility functions
├── App.tsx           # Main application component
├── index.ts          # Server entry point
├── index.html        # HTML template
└── index.css         # Global styles
```

## Development

Install dependencies:
```bash
bun install
```

Start the development server:
```bash
bun dev
```

The app will be available at `http://localhost:3000`

## Building for Production

Build the project:
```bash
bun run build
```

The built files will be in the `dist/` directory.

## Environment Variables

Copy `.env.example` to `.env.local` and fill in your values:

```bash
cp .env.example .env.local
```

Required variables:
- `VITE_AI_API_KEY`: Your AI API key (OpenAI, Anthropic, etc.)
- `VITE_AI_API_URL`: AI API endpoint URL
