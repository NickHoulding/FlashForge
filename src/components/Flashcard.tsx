import type { FlashcardProps } from '../types';

const Flashcard = ({ question, answer, index }: FlashcardProps) => {
    return <div
        className="flex flex-row gap-0 border border-transparent rounded-[20px] opacity-0 transition-[gap] duration-200 ease-linear hover:gap-[10px]"
        style={{ animation: 'fadeInUp .3s ease-out forwards', animationDelay: `${index * 0.1}s` }}
    >
        <textarea
            placeholder="Forge a question..."
            rows={1}
            defaultValue={question}
            className="flex-1 font-[Satoshi-Medium] text-[1.05rem] bg-[var(--neutral)] text-[var(--primary)] p-[10px] border border-[var(--secondary)] rounded-[10px] box-border resize-none"
        ></textarea>
        <textarea
            placeholder="Forge an answer..."
            rows={1}
            defaultValue={answer}
            className="flex-1 font-[Satoshi-Medium] text-[1.05rem] bg-[var(--neutral)] text-[var(--primary)] p-[10px] border border-[var(--secondary)] rounded-[10px] box-border resize-none"
        ></textarea>
        <button className="w-0 text-transparent bg-transparent my-auto transition-all duration-200 ease-linear hover:bg-[var(--delete-red)] hover:text-[var(--delete-white)] group-hover:w-[35px]">
            <svg fill="currentColor" height="24" viewBox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg">
                <path d="M4.2097 4.3871L4.29289 4.29289C4.65338 3.93241 5.22061 3.90468 5.6129 4.2097L5.70711 4.29289L12 10.585L18.2929 4.29289C18.6834 3.90237 19.3166 3.90237 19.7071 4.29289C20.0976 4.68342 20.0976 5.31658 19.7071 5.70711L13.415 12L19.7071 18.2929C20.0676 18.6534 20.0953 19.2206 19.7903 19.6129L19.7071 19.7071C19.3466 20.0676 18.7794 20.0953 18.3871 19.7903L18.2929 19.7071L12 13.415L5.70711 19.7071C5.31658 20.0976 4.68342 20.0976 4.29289 19.7071C3.90237 19.3166 3.90237 18.6834 4.29289 18.2929L10.585 12L4.29289 5.70711C3.93241 5.34662 3.90468 4.77939 4.2097 4.3871L4.29289 4.29289L4.2097 4.3871Z"/>
            </svg>
        </button>
    </div>;
};

export default Flashcard;
