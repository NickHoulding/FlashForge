import type { UserQueryProps } from '../types';

export function UserQuery({ content }: UserQueryProps) {
    return (
        <div className="user-query-root">
            <p className="user-query-text">{content}</p>
        </div>
    )
}
