import type { Flashcard } from "@/types/flashcard";

interface FlashcardViewProps {
  cards: Flashcard[];
}

export function FlashcardView({ cards }: FlashcardViewProps) {
  if (cards.length === 0) {
    return null;
  }

  return (
    <div className="mt-8">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold">Generated Flashcards</h2>
        <span className="text-gray-600">{cards.length} cards</span>
      </div>
      <div className="space-y-4">
        {cards.map((card) => (
          <div
            key={card.id}
            className="border rounded-lg p-6 bg-white shadow-sm hover:shadow-md transition-shadow"
          >
            <div className="mb-4">
              <span className="text-xs font-semibold text-gray-500 uppercase">
                Question
              </span>
              <p className="text-lg font-medium mt-1">{card.question}</p>
            </div>
            <div>
              <span className="text-xs font-semibold text-gray-500 uppercase">
                Answer
              </span>
              <p className="text-gray-700 mt-1">{card.answer}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
