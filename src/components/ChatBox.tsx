import type { ChatMessage, ChatBoxProps } from '../types';
import { SYSTEM_PROMPTS } from '../constants/prompts';
import { zodToJsonSchema } from 'zod-to-json-schema';
import { useEffect, useState } from "react";
import { z } from 'zod';

const Flashcard = z.object({
    question: z.string().describe('The question for this flashcard.'),
    answer: z.string().describe('The answer for this flashcard.')
});

const StudySet = z.object({
    flashcards: z.array(Flashcard).describe('A list of flashcard objects containing questions and answers.')
});

const ChatBox = ({ onSendMessage }: ChatBoxProps) => {
    const [availableModels, setAvailableModels] = useState<string[]>([]);
    const [selectedModel, setSelectedModel] = useState('');
    const [text, setText] = useState('');

    useEffect(() => {
        fetch('http://localhost:11434/api/tags')
            .then(response => response.json())
            .then(data => {
                const models = data.models.map((model: any) => model.name);
                setAvailableModels(models);

                if (models.length > 0) {
                    setSelectedModel(models[0]);
                }
            })
            .catch(error => {
                console.error('Failed to fetch models: ', error);
                setAvailableModels([]);
                setSelectedModel('');
            })
    }, []);

    const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendUserQuery();
        }
    };

    async function sendUserQuery() {
        if(!text.trim() || !selectedModel) { 
            return
        }

        const userMessage: ChatMessage = {
            id: Date.now().toString(),
            type: 'user',
            content: text
        };
        onSendMessage(userMessage);
        const queryText = text;
        setText('');

        try {
            const response = await fetch('http://localhost:11434/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json'},
                body: JSON.stringify({
                    model: selectedModel,
                    messages: [
                        { role: 'system', content: SYSTEM_PROMPTS.FLASHCARD_GENERATION },
                        { role: 'user', content: queryText }],
                    format: zodToJsonSchema(StudySet),
                    stream: false
                }),
            });
            const data = await response.json();
            const parsedContent = JSON.parse(data.message.content);
            const aiMessage: ChatMessage = {
                id: (Date.now() + 1).toString(),
                type: 'ai',
                content: data.message.content,
                flashcards: parsedContent.flashcards
            };
            onSendMessage(aiMessage);
        } catch (error) {
            console.error('Failed to send message: ', error)
        }
    };

    return <div className="relative left-1/2 -translate-x-1/2 flex flex-col gap-[10px] w-full max-w-[750px] h-fit max-h-[200px] p-[10px] pt-0 box-border bg-[var(--accent)] border border-[var(--secondary)] rounded-[20px]">
        <textarea
            placeholder="Forge your studies..."
            value={text}
            onChange={(e) => setText(
                (e.target as HTMLTextAreaElement).value
            )}
            onKeyDown={handleKeyDown}
            className="flex-1 min-h-[75px] px-[5px] pt-[15px] bg-transparent text-[var(--primary)] font-[Satoshi-Medium] text-[1.05rem] box-border rounded-t-[10px] border-none resize-none focus:outline-none"
        ></textarea>
        <div className="flex justify-between">
            <div className="flex flex-row gap-[10px]">
                <button className="font-[Satoshi-Medium] text-[0.85rem] text-[var(--primary)] flex items-center w-[35px] h-[35px] bg-transparent border border-[var(--secondary)] rounded-[10px] box-border hover:bg-[var(--secondary)]" id="file-button">
                    <svg fill="currentColor" height="24" viewBox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg">
                        <path d="M15.9999 2C19.3136 2 21.9999 4.68629 21.9999 8C21.9999 9.5373 21.4178 10.9843 20.396 12.0835L20.2061 12.2784L11.479 21.0053L11.4259 21.0548L11.3702 21.0997C10.7009 21.6759 9.84594 22 8.9429 22C6.88779 22 5.22179 20.334 5.22179 18.2789C5.22179 17.3775 5.54481 16.5248 6.11735 15.8574L6.26564 15.6945L6.28072 15.6826L13.5717 8.37879C13.9619 7.98793 14.5951 7.98737 14.986 8.37755C15.3768 8.76774 15.3774 9.4009 14.9872 9.79177L7.69618 17.0956L7.68524 17.1039C7.38894 17.4208 7.22179 17.8354 7.22179 18.2789C7.22179 19.2294 7.99236 20 8.9429 20C9.32185 20 9.67979 19.8781 9.97412 19.6571L10.0962 19.5564L10.097 19.558L18.7994 10.8571L18.958 10.6927C19.6231 9.96299 19.9999 9.0125 19.9999 8C19.9999 5.79086 18.2091 4 15.9999 4C14.9383 4 13.9453 4.4146 13.2048 5.13858L13.0501 5.29842L13.0316 5.31139L3.70629 14.6403C3.31585 15.0309 2.68269 15.031 2.29207 14.6406C1.90146 14.2501 1.90132 13.617 2.29176 13.2264L11.6007 3.91324L11.6473 3.87021C12.7712 2.68577 14.3316 2 15.9999 2Z"/>
                    </svg>
                </button>
                <button className="font-[Satoshi-Medium] text-[0.85rem] text-[var(--primary)] flex items-center w-fit h-[35px] bg-transparent border border-[var(--secondary)] rounded-[10px] box-border hover:bg-[var(--secondary)] px-[10px] gap-[5px]" id="export-button">
                    <svg fill="currentColor" height="24" viewBox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg">
                        <path d="M2.75 4.50388C3.1297 4.50388 3.44349 4.78604 3.49315 5.15211L3.5 5.25388V18.7525C3.5 19.1667 3.16421 19.5025 2.75 19.5025C2.3703 19.5025 2.05651 19.2204 2.00685 18.8543L2 18.7525V5.25388C2 4.83967 2.33579 4.50388 2.75 4.50388ZM15.2098 6.38702L15.293 6.29282C15.6535 5.93237 16.2207 5.9047 16.613 6.20977L16.7072 6.29297L21.7038 11.2906C22.064 11.6509 22.0919 12.2178 21.7873 12.6101L21.7042 12.7043L16.7076 17.7077C16.3173 18.0985 15.6842 18.0989 15.2934 17.7087C14.9326 17.3484 14.9045 16.7812 15.2093 16.3887L15.2924 16.2945L18.581 12.9999L6 13C5.48716 13 5.06449 12.614 5.00673 12.1166L5 12C5 11.4872 5.38604 11.0645 5.88338 11.0067L6 11L18.584 10.9999L15.2928 7.70703C14.9324 7.34651 14.9047 6.77928 15.2098 6.38702L15.293 6.29282L15.2098 6.38702Z"/>
                    </svg>
                    Export
                </button>
            </div>
            <div className="flex flex-row gap-[10px]">
                <select
                    value={selectedModel}
                    onChange={(e) => setSelectedModel(e.target.value)}
                    className="font-[Satoshi-Medium] text-[0.85rem] bg-transparent text-[var(--primary)] border border-[var(--secondary)] rounded-[10px] w-[125px] pl-[10px] pr-[25px] box-border appearance-none transition-colors hover:bg-[var(--secondary)]"
                    style={{
                        backgroundImage: "url('/src/assets/dropdown_arrow.svg')",
                        backgroundRepeat: 'no-repeat',
                        backgroundPosition: 'right 5px center',
                        backgroundSize: '15px'
                    }}
                >
                    {availableModels.map(model => (
                        <option key={model} value={model}>
                            {model}
                        </option>
                    ))}
                </select>
                <button onClick={sendUserQuery} className="font-[Satoshi-Medium] text-[0.85rem] flex items-center w-[35px] h-[35px] bg-[var(--secondary)] text-[var(--primary)] border border-[var(--secondary)] rounded-[10px] hover:bg-[var(--primary)] hover:text-[var(--neutral)]">
                    <svg fill="currentColor" height="24" viewBox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg">
                        <path d="M4.28401 10.2959C3.89639 10.6893 3.90108 11.3225 4.29449 11.7101C4.68789 12.0977 5.32104 12.093 5.70866 11.6996L11 6.32931V20.0004C11 20.5527 11.4477 21.0004 12 21.0004C12.5523 21.0004 13 20.5527 13 20.0004V6.33579L18.2849 11.6996C18.6726 12.093 19.3057 12.0977 19.6991 11.7101C20.0925 11.3225 20.0972 10.6893 19.7096 10.2959L12.8872 3.37171C12.3976 2.8748 11.596 2.87479 11.1064 3.37171L4.28401 10.2959Z"/>
                    </svg>
                </button>
            </div>
        </div>
    </div>;
};

export default ChatBox;
