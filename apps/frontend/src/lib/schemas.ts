import { z } from 'zod';

export const Flashcard = z.object({
    question: z.string().describe('The question for this flashcard.'),
    answer: z.string().describe('The answer for this flashcard.')
});

export const StudySet = z.object({
    flashcards: z.array(Flashcard).describe('A list of flashcard objects containing questions and answers.')
});
