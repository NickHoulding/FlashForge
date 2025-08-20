const ChatEntry = () => {
    return <div className="bg-transparent items-center rounded-[10px] flex gap-[5px] p-[5px] box-border flex-row hover:bg-[var(--secondary)]">
        <textarea
            rows={1}
            className="flex-1 font-[Satoshi-Medium] text-[1.05rem] leading-[1.05rem] bg-transparent text-[var(--primary)] rounded-[5px] border-0 resize-none box-border overflow-hidden whitespace-nowrap h-min p-[6px]"
        ></textarea>
        <button className="text-transparent p-[2.5px] w-min hover:bg-[var(--accent)] group-hover:text-[var(--primary)] rounded-[5px] cursor-pointer">
            <svg fill="currentColor" height="24" viewBox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg">
                <path d="M8 12C8 13.1046 7.10457 14 6 14C4.89543 14 4 13.1046 4 12C4 10.8954 4.89543 10 6 10C7.10457 10 8 10.8954 8 12Z"/><path d="M14 12C14 13.1046 13.1046 14 12 14C10.8954 14 10 13.1046 10 12C10 10.8954 10.8954 10 12 10C13.1046 10 14 10.8954 14 12Z"/><path d="M18 14C19.1046 14 20 13.1046 20 12C20 10.8954 19.1046 10 18 10C16.8954 10 16 10.8954 16 12C16 13.1046 16.8954 14 18 14Z"/>
            </svg>
        </button>
    </div>;
};

export default ChatEntry;
