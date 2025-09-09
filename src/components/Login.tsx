const LoginPage = () => {
    const PlaceholderErrorMessage = "Incorrect password";

    return (
        <div className="flex flex-col gap-[20px] items-center justify-center absolute bg-[var(--neutral)] w-screen h-screen z-20000">
            <h1 className="font-[Satoshi-Bold] text-[2.10rem]">FlashForge</h1>
            <textarea rows={1} placeholder="Enter username" className="w-[300px] bg-[var(--accent)] text-[var(--primary)] border border-[var(--secondary)] p-[10px] rounded-[10px] resize-none text-[1.05rem]" id=""></textarea>
            <textarea rows={1} placeholder="Enter password" className="w-[300px] bg-[var(--accent)] text-[var(--primary)] border border-[var(--secondary)] p-[10px] rounded-[10px] resize-none text-[1.05rem]" id=""></textarea>
            <div className="w-[300px] flex gap-[20px]">
                <button className="flex-1 text-[1.05rem] py-[10px] font-[Satoshi-Regular] bg-[var(--secondary)] hover:bg-[var(--primary)] hover:text-[var(--neutral)] rounded-[10px] cursor-pointer">Create</button>
                <button className="flex-1 text-[1.05rem] py-[10px] font-[Satoshi-Regular] bg-[var(--secondary)] hover:bg-[var(--primary)] hover:text-[var(--neutral)] rounded-[10px] cursor-pointer">Sign in</button>
            </div>
            <div className="w-[300px] text-[1.05rem] font-[Satoshi-Regular] text-center text-red-400 mt-[10px]">{PlaceholderErrorMessage}</div>
        </div>
    );
};

export default LoginPage;
