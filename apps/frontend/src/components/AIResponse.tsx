import type { AIResponseProps } from "../types";
import Flashcard from "./Flashcard";

const AIResponse = ({ flashcards }: AIResponseProps) => {
    return <div className="flex flex-col gap-[10px]">
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
