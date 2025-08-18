import type { AIResponseProps } from "../types";
import Flashcard from "./Flashcard";

const AIResponse = (props: AIResponseProps) => {
    const { flashcards } = props;
    
    return <div className="ai-response-content">
        {flashcards.map((flashcard, index) => (
            <Flashcard
                question={flashcard.question}
                answer={flashcard.answer}
                index={index}
            />
        ))}
    </div>;
};

export default AIResponse;
