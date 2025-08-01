import type { AIResponseProps } from "../types"
import { Flashcard } from "./Flashcard"

export function AIResponse({ flashcards }: AIResponseProps) {
    return (
        <div className="ai-response-content">
            {flashcards.map((flashcard, index) => (
                <Flashcard
                    key={index}
                    question={flashcard.question}
                    answer={flashcard.answer}
                />
            ))}
        </div>
    )
}
