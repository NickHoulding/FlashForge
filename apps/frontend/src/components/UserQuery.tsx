import type { UserQueryProps } from '../types';

const UserQuery = ({ content }: UserQueryProps) => {
    return <div className="flex justify-end w-full">
        <p className="font-[Satoshi-Medium] text-[1.05rem] bg-[var(--accent)] text-[var(--primary)] py-[10px] px-[15px] m-0 max-w-[80%] break-words border border-[var(--secondary)] rounded-[20px] rounded-br-[5px] box-border">
            {content}
        </p>
    </div>;
};

export default UserQuery;
